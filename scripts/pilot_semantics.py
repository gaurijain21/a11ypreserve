from __future__ import annotations

import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def deref(value: Any) -> Any:
    if isinstance(value, IndirectObject):
        return value.get_object()
    return value


def pdf_name(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).lstrip("/")


def text_from_xml(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.iter(W + "t"))


def extract_docx(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        core = ET.fromstring(archive.read("docProps/core.xml"))
        numbering = ET.fromstring(archive.read("word/numbering.xml"))
        rels = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
    core_title = next((x.text for x in core.iter() if x.tag.endswith("}title")), None)
    title = core_title
    lang_values = []
    for node in document.iter(W + "lang"):
        value = node.attrib.get(W + "val")
        if value:
            lang_values.append(value)
    if not lang_values:
        lang_values = ["en-US"]

    abstract_formats: dict[str, dict[str, str]] = {}
    for abstract in numbering.findall(W + "abstractNum"):
        abstract_id = abstract.attrib.get(W + "abstractNumId")
        levels: dict[str, str] = {}
        for level in abstract.findall(W + "lvl"):
            ilvl = level.attrib.get(W + "ilvl", "0")
            fmt = level.find(W + "numFmt")
            levels[ilvl] = fmt.attrib.get(W + "val", "") if fmt is not None else ""
        abstract_formats[abstract_id] = levels
    num_formats: dict[str, dict[str, str]] = {}
    for num in numbering.findall(W + "num"):
        num_id = num.attrib.get(W + "numId")
        abstract_ref = num.find(W + "abstractNumId")
        if abstract_ref is not None:
            num_formats[num_id] = abstract_formats.get(abstract_ref.attrib.get(W + "val"), {})

    rel_targets = {}
    for rel in rels:
        rel_targets[rel.attrib.get("Id")] = rel.attrib.get("Target")

    headings = []
    lists = []
    list_last: dict[str, list[dict[str, Any]]] = defaultdict(list)
    order = 0
    for paragraph in document.iter(W + "p"):
        order += 1
        text = text_from_xml(paragraph)
        ppr = paragraph.find(W + "pPr")
        style_id = None
        if ppr is not None:
            style = ppr.find(W + "pStyle")
            style_id = style.attrib.get(W + "val") if style is not None else None
        if style_id and style_id.lower().startswith("heading"):
            match = re.search(r"(\d+)$", style_id)
            if match:
                headings.append({"text": text, "level": int(match.group(1)), "order": order, "evidence": {"ooxml": "word/document.xml", "style": style_id}})
        num_id = ilvl = None
        if ppr is not None:
            num_pr = ppr.find(W + "numPr")
            if num_pr is not None:
                num = num_pr.find(W + "numId")
                lvl = num_pr.find(W + "ilvl")
                num_id = num.attrib.get(W + "val") if num is not None else None
                ilvl = int(lvl.attrib.get(W + "val", "0")) if lvl is not None else 0
        if num_id is not None:
            fmt = num_formats.get(num_id, {}).get(str(ilvl), "")
            list_type = "ordered" if fmt in {"decimal", "upperRoman", "lowerRoman", "upperLetter", "lowerLetter"} else "unordered"
            history = list_last[num_id]
            parent = None
            for previous in reversed(history):
                if previous["depth"] < ilvl:
                    parent = previous["text"]
                    break
            item = {"type": list_type, "depth": ilvl, "text": text, "parent": parent, "order": order, "evidence": {"ooxml": "word/document.xml", "numId": num_id, "ilvl": ilvl, "numFmt": fmt}}
            lists.append(item)
            history[:] = [x for x in history if x["depth"] < ilvl]
            history.append(item)

    figures = []
    for index, doc_pr in enumerate(document.iter(WP + "docPr"), start=1):
        figures.append({"identifier": f"figure-{index}", "alt": doc_pr.attrib.get("descr", ""), "decorative": not bool(doc_pr.attrib.get("descr", "")), "order": index, "evidence": {"ooxml": "word/document.xml", "docPr": doc_pr.attrib.get("id")}})

    tables = []
    for table_index, table in enumerate(document.iter(W + "tbl"), start=1):
        rows = list(table.findall(W + "tr"))
        cells = []
        for row_index, row in enumerate(rows):
            row_cells = []
            for cell in row.findall(W + "tc"):
                row_cells.append(text_from_xml(cell))
            cells.append(row_cells)
        header = bool(rows and rows[0].find(W + "trPr/" + W + "tblHeader") is not None)
        tables.append({"identifier": f"table-{table_index}", "dimensions": {"rows": len(cells), "columns": max((len(row) for row in cells), default=0)}, "cells": cells, "headers": cells[0] if header and cells else [], "header_row": 0 if header else None, "evidence": {"ooxml": "word/document.xml", "tblHeader": header}})

    return {
        "asir": "ASIR-pilot-1",
        "format": "docx",
        "document": {"title": title, "language": lang_values[0], "evidence": {"ooxml": ["docProps/core.xml", "word/document.xml"]}},
        "headings": headings,
        "figures": figures,
        "lists": lists,
        "tables": tables,
        "extraction": {"method": "deterministic OOXML inspection", "source": str(path)},
    }


def _collect_mcid_text(reader: PdfReader) -> dict[tuple[int, int], str]:
    # Best-effort marked-content text map. Structure objects remain authoritative
    # for roles and relationships; this map supplies text when a converter emits MCIDs.
    result: dict[tuple[int, int], str] = {}
    try:
        from pypdf._page import ContentStream
        from pypdf.generic import TextStringObject
    except Exception:
        return result
    for page_index, page in enumerate(reader.pages):
        try:
            stream = ContentStream(page.get_contents(), reader)
        except Exception:
            continue
        stack: list[int] = []
        chunks: dict[int, list[str]] = defaultdict(list)
        for operands, operator in stream.operations:
            if operator == b"BDC" and len(operands) >= 2:
                props = deref(operands[1])
                mcid = None
                if isinstance(props, DictionaryObject):
                    mcid = props.get("/MCID")
                stack.append(int(mcid) if mcid is not None else -1)
            elif operator == b"BMC":
                stack.append(-1)
            elif operator in {b"EMC"}:
                if stack:
                    stack.pop()
            elif stack and stack[-1] >= 0 and operator in {b"Tj", b"TJ", b"'", b'"'}:
                values = operands if operator == b"TJ" else operands[:1]
                for value in values:
                    if isinstance(value, ArrayObject):
                        for part in value:
                            if isinstance(part, TextStringObject):
                                chunks[stack[-1]].append(str(part))
                    elif isinstance(value, TextStringObject):
                        chunks[stack[-1]].append(str(value))
        for mcid, parts in chunks.items():
            result[(page_index, mcid)] = "".join(parts)
    return result


def extract_pdf(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    root = deref(reader.trailer.get("/Root"))
    struct_root = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    role_map = deref(struct_root.get("/RoleMap")) if isinstance(struct_root, DictionaryObject) else {}
    mcid_text = _collect_mcid_text(reader)
    page_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    headings, figures, lists, tables = [], [], [], []
    order = 0

    def role_name(role: Any) -> str:
        current = pdf_name(role) or ""
        seen = set()
        while isinstance(role_map, DictionaryObject) and current and current not in seen and role_map.get("/" + current) is not None:
            seen.add(current)
            current = pdf_name(role_map.get("/" + current)) or current
        return current

    def kid_text(kid: Any) -> str:
        kid = deref(kid)
        if isinstance(kid, DictionaryObject):
            if kid.get("/ActualText"):
                return str(kid.get("/ActualText"))
            page = deref(kid.get("/Pg"))
            page_index = next((i for i, p in enumerate(reader.pages) if p.indirect_reference == getattr(page, "indirect_reference", None)), None)
            mcid = kid.get("/MCID")
            if page_index is not None and mcid is not None:
                return mcid_text.get((page_index, int(mcid)), "")
        return ""

    def walk(node: Any, parent: str | None = None, depth: int = 0) -> None:
        nonlocal order
        node = deref(node)
        if isinstance(node, ArrayObject):
            for child in node:
                walk(child, parent, depth)
            return
        if not isinstance(node, DictionaryObject):
            return
        role = role_name(node.get("/S"))
        order += 1
        kids = node.get("/K")
        kid_values = list(kids) if isinstance(kids, ArrayObject) else ([kids] if kids is not None else [])
        direct_text = "".join(kid_text(kid) for kid in kid_values)
        evidence = {"pdf_role": role, "object": str(getattr(node, "indirect_reference", "inline"))}
        if re.fullmatch(r"H[1-6]", role):
            headings.append({"text": direct_text, "level": int(role[1]), "order": order, "evidence": evidence})
        elif role == "Figure":
            figures.append({"identifier": f"figure-{len(figures)+1}", "alt": str(node.get("/Alt", "")), "decorative": not bool(node.get("/Alt")), "order": order, "evidence": evidence})
        elif role == "L":
            lists.append({"type": "list", "depth": depth, "text": direct_text, "parent": parent, "order": order, "evidence": evidence})
        elif role in {"LI", "Lbl", "LBody"}:
            lists.append({"type": role, "depth": depth, "text": direct_text, "parent": parent, "order": order, "evidence": evidence})
        elif role == "Table":
            tables.append({"identifier": f"table-{len(tables)+1}", "dimensions": {}, "cells": [], "headers": [], "header_row": None, "evidence": evidence})
        elif role in {"TH", "TD"}:
            tables.append({"identifier": f"cell-{len(tables)+1}", "role": role, "text": direct_text, "evidence": evidence})
        for child in kid_values:
            child_obj = deref(child)
            if isinstance(child_obj, DictionaryObject) and child_obj.get("/S"):
                walk(child_obj, role or parent, depth + (1 if role in {"L", "LI"} else 0))

    if isinstance(struct_root, DictionaryObject):
        walk(struct_root.get("/K"))
    metadata = reader.metadata or {}
    lang = root.get("/Lang") if isinstance(root, DictionaryObject) else None
    return {
        "asir": "ASIR-pilot-1",
        "format": "pdf",
        "document": {"title": metadata.get("/Title"), "language": str(lang) if lang else None, "evidence": {"pdf": ["/Root", "/Info", "/StructTreeRoot"]}},
        "headings": headings,
        "figures": figures,
        "lists": lists,
        "tables": tables,
        "pdf": {"tagged": struct_root is not None, "role_map": {str(k): str(v) for k, v in role_map.items()} if isinstance(role_map, DictionaryObject) else {}, "pages": len(reader.pages)},
        "pdf_text": page_text,
        "extraction": {"method": "pypdf object-model and marked-content inspection", "source": str(path)},
    }


def extract(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".docx":
        return extract_docx(path)
    if path.suffix.lower() == ".pdf":
        return extract_pdf(path)
    raise ValueError(f"Unsupported file type: {path}")


if __name__ == "__main__":
    print(json.dumps(extract(Path(sys.argv[1])), indent=2, ensure_ascii=False))
