"""Independent structural checks for difficult frozen PDF cases.

Path A uses pypdf's object model and marked-content parser. Path B uses
PyMuPDF's page/text/link API plus direct scans of every serialized PDF object.
The two paths are deliberately not derived from the project extractor.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import fitz
from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "final_strengthening" / "PDF_PARSER_TRIANGULATION.json"
PDFS = {
    "F06_GOOGLE": ROOT / "results/full_experiment/outputs/google_docs/F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf",
    "F11_GOOGLE": ROOT / "results/full_experiment/outputs/google_docs/F11_FOOTNOTES__GOOGLE_DOCS.pdf",
    "F11_LIBREOFFICE": ROOT / "results/full_experiment/outputs/libreoffice/F11_FOOTNOTES__LIBREOFFICE.pdf",
}


def deref(value: Any) -> Any:
    return value.get_object() if isinstance(value, IndirectObject) else value


def name(value: Any) -> str:
    return str(value).lstrip("/") if value is not None else ""


def pypdf_path(path: Path) -> dict:
    reader = PdfReader(str(path))
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    role_map = deref(struct.get("/RoleMap")) if isinstance(struct, DictionaryObject) else None
    parent_tree = deref(struct.get("/ParentTree")) if isinstance(struct, DictionaryObject) else None
    nodes = []
    mcids = []
    def walk(value: Any, depth: int = 0) -> None:
        value = deref(value)
        if isinstance(value, ArrayObject):
            for child in value:
                walk(child, depth)
            return
        if not isinstance(value, DictionaryObject):
            return
        role = name(value.get("/S"))
        kids = value.get("/K")
        kids_list = list(kids) if isinstance(kids, ArrayObject) else ([kids] if kids is not None else [])
        node = {
            "depth": depth,
            "role": role,
            "lang": str(value.get("/Lang")) if value.get("/Lang") is not None else None,
            "alt": str(value.get("/Alt")) if value.get("/Alt") is not None else None,
            "actual_text": str(value.get("/ActualText")) if value.get("/ActualText") is not None else None,
            "mcids": [],
            "has_parent": value.get("/P") is not None,
            "attribute_keys": [],
        }
        attrs = deref(value.get("/A"))
        if isinstance(attrs, DictionaryObject):
            node["attribute_keys"] = [name(key) for key in attrs.keys()]
        elif isinstance(attrs, ArrayObject):
            node["attribute_keys"] = sorted({name(key) for attr in attrs for key in deref(attr).keys()} if all(isinstance(deref(attr), DictionaryObject) for attr in attrs) else [])
        for kid in kids_list:
            kid_obj = deref(kid)
            if isinstance(kid_obj, DictionaryObject) and kid_obj.get("/MCID") is not None:
                node["mcids"].append(int(kid_obj.get("/MCID")))
                mcids.append(int(kid_obj.get("/MCID")))
        nodes.append(node)
        for child in kids_list:
            child_obj = deref(child)
            if isinstance(child_obj, DictionaryObject) and child_obj.get("/S") is not None:
                walk(child_obj, depth + 1)
    if isinstance(struct, DictionaryObject):
        walk(struct.get("/K"))
    annotations = []
    for page_index, page in enumerate(reader.pages, start=1):
        for annotation in page.get("/Annots", []) or []:
            ann = deref(annotation)
            if isinstance(ann, DictionaryObject):
                action = deref(ann.get("/A"))
                annotations.append({"page": page_index, "subtype": name(ann.get("/Subtype")), "uri": str(action.get("/URI")) if isinstance(action, DictionaryObject) and action.get("/URI") else None})
    raw = path.read_bytes()
    raw_text = raw.decode("latin-1", errors="ignore")
    return {
        "library": f"pypdf {getattr(__import__('pypdf'), '__version__', 'unknown')}",
        "pages": len(reader.pages),
        "catalog_keys": [name(key) for key in root.keys()] if isinstance(root, DictionaryObject) else [],
        "struct_tree_present": isinstance(struct, DictionaryObject),
        "role_map": {name(key): name(value) for key, value in role_map.items()} if isinstance(role_map, DictionaryObject) else {},
        "parent_tree_present": isinstance(parent_tree, DictionaryObject),
        "parent_tree_keys": [name(key) for key in parent_tree.keys()] if isinstance(parent_tree, DictionaryObject) else [],
        "structure_nodes": nodes,
        "mcid_count": len(mkids := mcids),
        "annotation_summary": annotations,
        "raw_marker_counts": {marker: raw_text.count(marker) for marker in ["/StructTreeRoot", "/ParentTree", "/RoleMap", "/Lang", "/Alt", "/ActualText", "/Note", "/Footnote", "/Artifact", "/Formula", "es-MX"]},
        "raw_sha256": hashlib.sha256(raw).hexdigest(),
    }


def pymupdf_path(path: Path) -> dict:
    document = fitz.open(path)
    objects = []
    marker_set = ["/StructTreeRoot", "/ParentTree", "/RoleMap", "/Lang", "/Alt", "/ActualText", "/Note", "/Footnote", "/Artifact", "/Formula", "es-MX"]
    marker_counts = {marker: 0 for marker in marker_set}
    for xref in range(1, document.xref_length()):
        try:
            value = document.xref_object(xref, compressed=False)
        except Exception:
            continue
        present = {marker: value.count(marker) for marker in marker_set if marker in value}
        if present:
            objects.append({"xref": xref, "markers": present, "preview": value[:500]})
            for marker, count in present.items():
                marker_counts[marker] += count
    pages = []
    text = []
    links = []
    for page in document:
        page_text = page.get_text("text")
        text.append(page_text)
        for link in page.get_links():
            links.append({"kind": link.get("kind"), "xref": link.get("xref"), "from": list(link["from"]) if link.get("from") is not None else None, "uri": link.get("uri"), "id": link.get("id")})
        pages.append({"text_chars": len(page_text), "image_count": len(page.get_images(full=True)), "link_count": len(page.get_links())})
    return {
        "library": "PyMuPDF " + fitz.VersionBind,
        "pages": len(document),
        "metadata": document.metadata,
        "page_summary": pages,
        "text": "\n".join(text),
        "links": links,
        "serialized_object_markers": marker_counts,
        "serialized_objects_with_markers": objects,
    }


def main() -> None:
    results = {}
    for label, path in PDFS.items():
        primary = pypdf_path(path)
        secondary = pymupdf_path(path)
        results[label] = {"path": str(path.relative_to(ROOT)), "sha256": primary["raw_sha256"], "pypdf": primary, "pymupdf": secondary}
    OUT.write_text(json.dumps({"status": "COMPLETE", "paths": results, "interpretation": "Path A and Path B are independent parser/evidence paths; absence from one serialized encoding is not by itself a proof of semantic absence."}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({label: {"pypdf_nodes": len(data["pypdf"]["structure_nodes"]), "pypdf_markers": data["pypdf"]["raw_marker_counts"], "pymupdf_markers": data["pymupdf"]["serialized_object_markers"], "text_contains_note": "This note records the source-to-note association." in data["pymupdf"]["text"], "text_contains_inline": "Buenos días" in data["pymupdf"]["text"]} for label, data in results.items()}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
