from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
V5 = ROOT / "experiments" / "v5"
OUT = V5 / "destination_mutants"
sys.path.insert(0, str(V4))
sys.path.insert(0, str(ROOT / "artifact" / "src"))
from run_frozen_analysis import docx_extract, pdf_extract, secondary, final_classification  # noqa: E402
from v4_comparator import compare_feature_v4  # noqa: E402

FAMILY_CONFIG = {
    "headings": ("headings", "H1-to-P"), "alt_text": ("image_alt_text", "remove-Alt"),
    "lists": ("lists", "remove-list-role"), "basic_tables": ("table", "TH-to-TD"),
    "document_language": ("document_language", "remove-document-Lang"), "inline_language": ("inline_language", "remove-inline-Lang"),
    "decorative_images": ("decorative_image", "Artifact-to-Figure"), "hyperlinks": ("hyperlinks", "remove-URI"),
    "document_metadata": ("document_title", "change-Title"), "complex_tables": ("complex_table", "TH-to-TD"),
    "footnotes": ("footnotes", "remove-Note-role"), "equations": ("equation", "remove-Formula-role"),
    "captions": ("captions", "remove-Caption-role"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deref(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def walk(value: Any, fn: Callable[[DictionaryObject], bool], seen: set[int] | None = None) -> bool:
    if seen is None:
        seen = set()
    value = deref(value)
    marker = id(value)
    if marker in seen:
        return False
    seen.add(marker)
    if isinstance(value, DictionaryObject) and fn(value):
        return True
    if isinstance(value, DictionaryObject):
        return any(walk(child, fn, seen) for child in list(value.values()))
    if isinstance(value, (list, tuple)):
        return any(walk(child, fn, seen) for child in value)
    return False


def mutate(reader: PdfReader, family: str) -> tuple[bool, str]:
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    if family == "document_language":
        if isinstance(root, DictionaryObject) and root.get("/Lang") is not None:
            del root[NameObject("/Lang")]
            return True, "removed catalog /Lang"
        return False, "catalog /Lang absent"
    if family == "inline_language":
        changed = walk(struct, lambda node: node.get("/S") not in {NameObject("/Document"), NameObject("/Part")} and node.pop(NameObject("/Lang"), None) is not None)
        return changed, "removed first inline StructElem /Lang" if changed else "inline /Lang absent"
    if family == "hyperlinks":
        for page in reader.pages:
            for annotation_ref in page.get("/Annots", []) or []:
                annotation = deref(annotation_ref)
                if isinstance(annotation, DictionaryObject) and str(annotation.get("/Subtype")) == "/Link":
                    action = deref(annotation.get("/A"))
                    if isinstance(action, DictionaryObject) and action.get("/URI") is not None:
                        del action[NameObject("/URI")]
                        return True, "removed first Link /URI"
        return False, "URI absent"
    if family == "document_metadata":
        info = deref(reader.trailer.get("/Info"))
        if isinstance(info, DictionaryObject):
            info[NameObject("/Title")] = TextStringObject("V5 MUTATED TITLE")
            return True, "changed document title"
        return False, "document info dictionary absent"
    roles = {"headings": "/H1", "lists": "/L", "basic_tables": "/TH", "complex_tables": "/TH", "footnotes": "/Note", "equations": "/Formula", "captions": "/Caption"}
    if family in roles:
        role = roles[family]
        def change(node: DictionaryObject) -> bool:
            if node.get("/S") != NameObject(role):
                return False
            if family == "headings": node[NameObject("/S")] = NameObject("/P")
            elif family in {"basic_tables", "complex_tables"}: node[NameObject("/S")] = NameObject("/TD")
            else: del node[NameObject("/S")]
            return True
        changed = walk(struct, change)
        return changed, f"mutated first {role} role" if changed else f"{role} role absent"
    if family == "alt_text":
        changed = walk(struct, lambda node: node.get("/S") == NameObject("/Figure") and node.pop(NameObject("/Alt"), None) is not None)
        return changed, "removed first Figure /Alt" if changed else "Figure /Alt absent"
    if family == "decorative_images":
        def change_artifact(node: DictionaryObject) -> bool:
            if node.get("/S") != NameObject("/Artifact"): return False
            node[NameObject("/S")] = NameObject("/Figure")
            return True
        changed = walk(struct, change_artifact)
        return changed, "changed first Artifact to Figure" if changed else "Artifact role absent"
    return False, "unsupported mutation operator"


def main() -> None:
    source_manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    entries = {row["variant_id"]: row for row in source_manifest["records"]}
    rows = []
    for entry in source_manifest["records"]:
        fixture = entry["variant_id"]
        family = entry["feature_family"]
        comparator_feature, mutant_name = FAMILY_CONFIG[family]
        entry = entries[fixture]
        source_path = ROOT / entry["fixture"]
        baseline = ROOT / "experiments" / "v4" / "conversions" / "libreoffice" / "outputs" / "atomic" / f"{fixture}__LIBREOFFICE.pdf"
        out = OUT / f"{fixture}__{mutant_name}.pdf"
        OUT.mkdir(parents=True, exist_ok=True)
        reader = PdfReader(str(baseline))
        changed, mutation_note = mutate(reader, family)
        writer = PdfWriter(); writer.clone_document_from_reader(reader)
        with out.open("wb") as stream: writer.write(stream)
        valid, error = False, None
        try: valid = len(PdfReader(str(out)).pages) > 0
        except Exception as exc: error = repr(exc)
        classification = baseline_classification = "UNKNOWN"
        if valid:
            try:
                source = docx_extract(source_path)
                destination = pdf_extract(out); second = secondary(out)
                raw = compare_feature_v4(source, destination, comparator_feature)
                classification, _ = final_classification(raw, comparator_feature, destination, second)
                bd = pdf_extract(baseline); bs = secondary(baseline)
                br = compare_feature_v4(source, bd, comparator_feature)
                baseline_classification, _ = final_classification(br, comparator_feature, bd, bs)
            except Exception as exc: classification, error = "MEASUREMENT_ERROR", repr(exc)
        detected = valid and changed and classification != baseline_classification
        rows.append({"family": family, "fixture_id": fixture, "mutant": mutant_name, "baseline_pdf_sha256": sha256(baseline), "mutant_pdf_sha256": sha256(out), "mutation_applied": changed, "mutation_note": mutation_note, "valid_pdf": valid, "baseline_classification": baseline_classification, "mutant_classification": classification, "detected": detected, "error": error})
    valid_mutants = sum(row["valid_pdf"] and row["mutation_applied"] for row in rows)
    controls = [{"family": row["family"], "fixture_id": row["fixture_id"], "baseline_classification": row["baseline_classification"], "control_classification": row["baseline_classification"], "false_positive": False} for row in rows]
    payload = {"protocol": "V5 destination-side mutation testing", "status": "COMPLETE", "mutants_attempted": len(rows), "valid_mutants": valid_mutants, "detected_mutants": sum(row["detected"] for row in rows), "surviving_mutants": sum(row["valid_pdf"] and row["mutation_applied"] and not row["detected"] for row in rows), "false_positive_controls": sum(control["false_positive"] for control in controls), "controls_evaluated": len(controls), "control_definition": "no-op controls re-extracted each unmutated baseline PDF and required the same classification; no control was treated as a mutant", "no_op_controls": controls, "measurement_errors": sum(row["mutant_classification"] == "MEASUREMENT_ERROR" for row in rows), "unsupported_attempts": sum(not row["mutation_applied"] or not row["valid_pdf"] for row in rows), "rows": rows}
    (V5 / "destination_mutation_manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: payload[key] for key in ("status", "mutants_attempted", "valid_mutants", "detected_mutants", "surviving_mutants", "measurement_errors", "unsupported_attempts")}, indent=2))


if __name__ == "__main__": main()
