"""Audit difficult V3 Google cases with two PDF inspection paths.

The audit is intentionally descriptive.  It does not change classifications or
infer user impact from serialized PDF evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import fitz
from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "v3" / "variant_set_b" / "google" / "DIFFICULT_CASE_AUDIT.json"
MARKERS = ["/StructTreeRoot", "/RoleMap", "/ParentTree", "/Lang", "/ActualText", "/Alt", "/Note", "/Footnote", "/Reference", "/Artifact", "/MCID", "es-MX", "es-ES", "fr-FR"]


def deref(value: Any) -> Any:
    return value.get_object() if isinstance(value, IndirectObject) else value


def pdf_name(value: Any) -> str | None:
    return str(value).lstrip("/") if value is not None else None


def pypdf_audit(path: Path) -> dict:
    reader = PdfReader(str(path))
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    nodes: list[dict] = []
    mcids: list[int] = []

    def walk(value: Any, depth: int = 0) -> None:
        value = deref(value)
        if isinstance(value, ArrayObject):
            for child in value:
                walk(child, depth)
            return
        if not isinstance(value, DictionaryObject):
            return
        role = pdf_name(value.get("/S"))
        kids = value.get("/K")
        children = list(kids) if isinstance(kids, ArrayObject) else ([kids] if kids is not None else [])
        item = {"depth": depth, "role": role, "lang": str(value.get("/Lang")) if value.get("/Lang") is not None else None, "alt": str(value.get("/Alt")) if value.get("/Alt") is not None else None, "actual_text": str(value.get("/ActualText")) if value.get("/ActualText") is not None else None, "reference": str(value.get("/Ref")) if value.get("/Ref") is not None else None, "mcids": []}
        for child in children:
            child_obj = deref(child)
            if isinstance(child_obj, DictionaryObject) and child_obj.get("/MCID") is not None:
                value_int = int(child_obj.get("/MCID"))
                item["mcids"].append(value_int)
                mcids.append(value_int)
        nodes.append(item)
        for child in children:
            child_obj = deref(child)
            if isinstance(child_obj, DictionaryObject) and child_obj.get("/S") is not None:
                walk(child_obj, depth + 1)

    if isinstance(struct, DictionaryObject):
        walk(struct.get("/K"))
    annotations = []
    for page_no, page in enumerate(reader.pages, start=1):
        for annotation in page.get("/Annots", []) or []:
            ann = deref(annotation)
            if isinstance(ann, DictionaryObject):
                action = deref(ann.get("/A"))
                annotations.append({"page": page_no, "subtype": pdf_name(ann.get("/Subtype")), "uri": str(action.get("/URI")) if isinstance(action, DictionaryObject) and action.get("/URI") else None, "struct_parent": str(ann.get("/StructParent")) if ann.get("/StructParent") is not None else None})
    raw = path.read_bytes()
    raw_text = raw.decode("latin-1", errors="ignore")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "pages": len(reader.pages),
        "catalog_keys": [pdf_name(k) for k in root.keys()] if isinstance(root, DictionaryObject) else [],
        "document_lang": str(root.get("/Lang")) if isinstance(root, DictionaryObject) and root.get("/Lang") is not None else None,
        "struct_tree_present": isinstance(struct, DictionaryObject),
        "role_map": {pdf_name(k): pdf_name(v) for k, v in deref(struct.get("/RoleMap")).items()} if isinstance(struct, DictionaryObject) and isinstance(deref(struct.get("/RoleMap")), DictionaryObject) else {},
        "parent_tree_present": bool(isinstance(struct, DictionaryObject) and struct.get("/ParentTree") is not None),
        "structure_nodes": nodes,
        "mcid_count": len(mkids := mcids),
        "annotation_summary": annotations,
        "raw_marker_counts": {marker: raw_text.count(marker) for marker in MARKERS},
    }


def pymupdf_audit(path: Path) -> dict:
    document = fitz.open(path)
    counts = {marker: 0 for marker in MARKERS}
    marker_objects = []
    for xref in range(1, document.xref_length()):
        try:
            obj = document.xref_object(xref, compressed=False)
        except Exception:
            continue
        present = {marker: obj.count(marker) for marker in MARKERS if marker in obj}
        if present:
            marker_objects.append({"xref": xref, "markers": present, "preview": obj[:600]})
            for marker, number in present.items():
                counts[marker] += number
    pages = []
    text = []
    links = []
    for page in document:
        page_text = page.get_text("text")
        text.append(page_text)
        pages.append({"text_chars": len(page_text), "image_count": len(page.get_images(full=True)), "link_count": len(page.get_links())})
        links.extend(page.get_links())
    return {"library": "PyMuPDF " + fitz.VersionBind, "pages": len(document), "page_summary": pages, "text": "\n".join(text), "links": links, "serialized_marker_counts": counts, "serialized_objects_with_markers": marker_objects}


def main() -> None:
    paths = {
        "F06_CORE_GOOGLE": ROOT / "results/full_experiment/outputs/google_docs/F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf",
        "F11_CORE_GOOGLE": ROOT / "results/full_experiment/outputs/google_docs/F11_FOOTNOTES__GOOGLE_DOCS.pdf",
        "B06_VARIANT_GOOGLE": ROOT / "v3/variant_set_b/google/outputs/B06__GOOGLE_DOCS.pdf",
        "B11_VARIANT_GOOGLE": ROOT / "v3/variant_set_b/google/outputs/B11__GOOGLE_DOCS.pdf",
    }
    records = []
    for case, path in paths.items():
        records.append({"case": case, "path": str(path.relative_to(ROOT)).replace("\\", "/"), "pypdf": pypdf_audit(path), "pymupdf": pymupdf_audit(path)})
    payload = {"audit_version": "v3-difficult-case-audit-1", "scope": "serialized PDF evidence for F06/F11 Core and Variant B Google outputs", "records": records, "interpretation_boundary": "These checks test for machine-verifiable destination representations; they do not establish screen-reader impact or internal cloud-pipeline state."}
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(records), "output": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
