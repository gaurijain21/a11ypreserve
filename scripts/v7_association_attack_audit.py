"""Generate valid PDF semantic/association attacks and evaluate the frozen comparator."""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
OUT = ROOT / "experiments" / "v7" / "association_cases"
REPORT = ROOT / "experiments" / "v7" / "V7_ASSOCIATION_ATTACKS.json"
sys.path.insert(0, str(V6))
from common import load_atomic_records, run_case, sha256, tool_versions  # noqa: E402


def deref(value):
    return value.get_object() if hasattr(value, "get_object") else value


def walk(value, fn, seen=None):
    seen = set() if seen is None else seen
    value = deref(value)
    if id(value) in seen:
        return False
    seen.add(id(value))
    if isinstance(value, dict) and fn(value):
        return True
    if isinstance(value, dict):
        return any(walk(child, fn, seen) for child in value.values())
    if isinstance(value, (list, tuple)):
        return any(walk(child, fn, seen) for child in value)
    return False


def mutate(reader: PdfReader, family: str) -> tuple[bool, str]:
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, dict) else None
    roles = {"headings": "/H1", "lists": "/L", "basic_tables": "/TH", "complex_tables": "/TH", "footnotes": "/Note", "equations": "/Formula", "captions": "/Caption"}
    if family == "hyperlinks":
        for page in reader.pages:
            for ref in page.get("/Annots", []) or []:
                annotation = deref(ref)
                action = deref(annotation.get("/A")) if isinstance(annotation, dict) else None
                if isinstance(action, dict) and action.get("/URI"):
                    action[NameObject("/URI")] = TextStringObject("https://example.org/association-break")
                    return True, "changed first hyperlink target while preserving link annotation"
        return False, "no URI action available"
    if family == "document_language" and isinstance(root, dict) and root.get("/Lang"):
        del root[NameObject("/Lang")]
        return True, "removed catalog language association"
    if family == "inline_language":
        changed = walk(struct, lambda node: node.get("/S") not in {"/Document", "/Part"} and node.pop(NameObject("/Lang"), None) is not None)
        return changed, "removed first inline language association" if changed else "no inline language association"
    if family == "alt_text":
        changed = walk(struct, lambda node: node.get("/S") == "/Figure" and node.pop(NameObject("/Alt"), None) is not None)
        return changed, "removed first figure alternative-text association" if changed else "no figure alternative text"
    if family == "decorative_images":
        changed = walk(struct, lambda node: node.get("/S") == "/Artifact" and node.__setitem__(NameObject("/S"), NameObject("/Figure")) is None)
        return changed, "changed first decorative Artifact role" if changed else "no Artifact representation"
    if family in roles:
        role = roles[family]
        def change(node):
            if node.get("/S") != role:
                return False
            node[NameObject("/S")] = NameObject("/P")
            return True
        changed = walk(struct, change)
        return changed, f"changed first {role} semantic association" if changed else f"no {role} structure"
    if family == "document_metadata":
        info = deref(reader.trailer.get("/Info"))
        if isinstance(info, dict):
            info[NameObject("/Title")] = TextStringObject("Association attack title")
            return True, "changed document title metadata association"
    return False, "operator not available"


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    chosen = {}
    for record in load_atomic_records():
        chosen.setdefault(record["family"], record)
    rows = []
    for record in chosen.values():
        baseline = record["pdf_path"]
        mutant = OUT / f"{record['fixture_id']}_association.pdf"
        applied = False
        reason = ""
        valid = False
        before = after = None
        try:
            reader = PdfReader(str(baseline), strict=False)
            applied, reason = mutate(reader, record["family"])
            writer = PdfWriter()
            writer.clone_document_from_reader(reader)
            with mutant.open("wb") as handle:
                writer.write(handle)
            valid = len(PdfReader(str(mutant), strict=False).pages) > 0
            if applied and valid:
                before = run_case(record["source_path"], baseline, record["family"])
                after = run_case(record["source_path"], mutant, record["family"])
        except Exception as exc:
            reason = repr(exc)
        row = {
            "fixture_id": record["fixture_id"],
            "family": record["family"],
            "operator": reason,
            "baseline_pdf_sha256": sha256(baseline),
            "mutated_pdf_sha256": sha256(mutant) if mutant.exists() else None,
            "mutation_applied": applied,
            "valid_pdf": valid,
            "baseline_classification": before.get("classification") if before else None,
            "mutated_classification": after.get("classification") if after else None,
            "classification_changed": bool(before and after and before.get("classification") != after.get("classification")),
            "attack_scorable": bool(applied and valid and before and after),
            "comparator_result": "DETECTED" if before and after and before.get("classification") != after.get("classification") else "NOT_DETECTED_OR_UNSCORED",
            "timestamp_utc": timestamp,
            "tool_versions": tool_versions(),
        }
        (OUT / f"{record['fixture_id']}.json").write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append(row)
    report = {
        "protocol": "V7 valid semantic and association attack audit",
        "attempted": len(rows),
        "applied": sum(row["mutation_applied"] for row in rows),
        "valid": sum(row["valid_pdf"] and row["mutation_applied"] for row in rows),
        "scorable": sum(row["attack_scorable"] for row in rows),
        "classification_detections": sum(row["comparator_result"] == "DETECTED" for row in rows),
        "unsupported_or_unscored": sum(not row["attack_scorable"] for row in rows),
        "family_summary": {},
        "rows": rows,
        "interpretation": "These attacks alter a contracted role, target, or association-bearing field. They are fault injections, not independent human ground truth; unsupported families remain explicitly unscored.",
        "timestamp_utc": timestamp,
    }
    for family in sorted({row["family"] for row in rows}):
        subset = [row for row in rows if row["family"] == family]
        report["family_summary"][family] = {"attempted": len(subset), "applied": sum(x["mutation_applied"] for x in subset), "valid": sum(x["valid_pdf"] and x["mutation_applied"] for x in subset), "scorable": sum(x["attack_scorable"] for x in subset), "detected": sum(x["comparator_result"] == "DETECTED" for x in subset)}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("attempted", "applied", "valid", "scorable", "classification_detections", "unsupported_or_unscored")}, indent=2))


if __name__ == "__main__":
    main()
