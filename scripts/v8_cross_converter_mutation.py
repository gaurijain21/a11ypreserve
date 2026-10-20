"""Cross-pipeline mutation audit on one frozen variant per feature family.

This is additive diagnostic evidence. It applies raw PDF fault operators to
archived LibreOffice, Google Docs, and Word outputs; it never changes those
archived PDFs. Contract-fault status comes from the independent V8 raw-object
reference rules, while the historical comparator is evaluated only as a
detector under test.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments" / "v8" / "cross_converter_mutation_cases"
REPORT = ROOT / "experiments" / "v8" / "V8_CROSS_CONVERTER_MUTATIONS.json"
sys.path.insert(0, str(ROOT / "scripts"))
from v8_mutation_ground_truth_audit import expected_fault, pdf_structures, sha256, source_contract  # noqa: E402
sys.path.insert(0, str(ROOT / "experiments" / "v6"))
from common import run_case  # noqa: E402


def deref(value):
    return value.get_object() if hasattr(value, "get_object") else value


def walk(value, fn, seen=None):
    seen = set() if seen is None else seen
    value = deref(value)
    marker = id(value)
    if marker in seen:
        return False
    seen.add(marker)
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
    role_map = {
        "headings": "/H1", "lists": "/L", "basic_tables": "/TH",
        "complex_tables": "/TH", "footnotes": "/Note", "equations": "/Formula",
        "captions": "/Caption",
    }
    if family == "document_language":
        if isinstance(root, dict) and root.get("/Lang"):
            del root[NameObject("/Lang")]
            return True, "removed catalog /Lang"
        return False, "no catalog /Lang"
    if family == "document_metadata":
        info = deref(reader.trailer.get("/Info"))
        if isinstance(info, dict) and info.get("/Title"):
            info[NameObject("/Title")] = TextStringObject("V8 cross-pipeline mutation")
            return True, "changed PDF Info /Title"
        return False, "no PDF Info /Title"
    if family == "inline_language":
        changed = walk(struct, lambda node: node.get("/S") not in {"/Document", "/Part"} and node.pop(NameObject("/Lang"), None) is not None)
        return changed, "removed first structural /Lang" if changed else "no structural /Lang"
    if family == "alt_text":
        changed = walk(struct, lambda node: node.get("/S") == "/Figure" and node.pop(NameObject("/Alt"), None) is not None)
        return changed, "removed first Figure /Alt" if changed else "no Figure /Alt"
    if family == "decorative_images":
        changed = walk(struct, lambda node: node.get("/S") == "/Artifact" and node.__setitem__(NameObject("/S"), NameObject("/Figure")) is None)
        return changed, "changed first /Artifact role" if changed else "no /Artifact target"
    if family == "hyperlinks":
        for page in reader.pages:
            for ref in page.get("/Annots", []) or []:
                annotation = deref(ref)
                action = deref(annotation.get("/A")) if isinstance(annotation, dict) else None
                if isinstance(action, dict) and action.get("/URI"):
                    del action[NameObject("/URI")]
                    return True, "removed first link URI"
        return False, "no URI action"
    role = role_map.get(family)
    if role:
        changed = walk(struct, lambda node: node.get("/S") == role and node.__setitem__(NameObject("/S"), NameObject("/P")) is None)
        return changed, f"changed first {role} role" if changed else f"no {role} target"
    return False, f"no operator for {family}"


def load_records() -> list[dict]:
    paths = {
        "LibreOffice": ROOT / "experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json",
        "Google Docs": ROOT / "experiments/v4/conversions/google/analysis/V4_GOOGLE_ANALYSIS.json",
        "Microsoft Word desktop": ROOT / "experiments/v4/conversions/word/analysis/V4_WORD_ANALYSIS.json",
    }
    grouped: dict[tuple[str, str], dict] = {}
    for pipeline, path in paths.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        for record in data["records"]:
            grouped.setdefault((pipeline, record["feature_family"]), record)
    return list(grouped.values())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    rows = []
    for record in load_records():
        baseline = ROOT / record["output_path"]
        source = ROOT / record["source_path"]
        pipeline = record["converter"]
        fixture = record["fixture_id"]
        target = OUT / f"{pipeline.replace(' ', '_')}_{fixture}.pdf"
        before = after = None
        applied = False
        reason = ""
        try:
            reader = PdfReader(str(baseline), strict=False)
            applied, reason = mutate(reader, record["feature_family"])
            if applied:
                writer = PdfWriter()
                writer.clone_document_from_reader(reader)
                with target.open("wb") as handle:
                    writer.write(handle)
                before = pdf_structures(baseline)
                after = pdf_structures(target)
            valid = target.exists() and after is not None and after["pypdf_reopened"] and after["pymupdf_reopened"] is not False
        except Exception as exc:
            valid = False
            reason = f"{reason}; exception={exc!r}" if reason else repr(exc)
        tier = established = None
        if applied and valid:
            tier, established, _ = expected_fault(record["feature_family"], record["feature_family"], before, after, source_contract(fixture))
        comparator_changed = None
        if applied and valid:
            try:
                base_result = run_case(source, baseline, record["feature_family"])
                mutant_result = run_case(source, target, record["feature_family"])
                comparator_changed = base_result.get("classification") != mutant_result.get("classification")
            except Exception as exc:
                reason = f"{reason}; comparator_exception={exc!r}"
        row = {
            "pipeline": pipeline, "fixture_id": fixture, "feature_family": record["feature_family"],
            "source_path": record["source_path"], "baseline_pdf_path": record["output_path"],
            "source_sha256": sha256(source), "baseline_pdf_sha256": sha256(baseline),
            "mutated_pdf_sha256": sha256(target) if target.exists() else None,
            "mutation_applied": applied, "valid_pdf": bool(valid), "operator": reason,
            "reference_tier": tier, "independently_established_fault": bool(established),
            "comparator_classification_changed": comparator_changed, "timestamp_utc": timestamp,
        }
        (OUT / f"{pipeline.replace(' ', '_')}_{fixture}.json").write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
        rows.append(row)
    family_summary = {}
    for key in sorted({(r["pipeline"], r["feature_family"]) for r in rows}):
        subset = [r for r in rows if (r["pipeline"], r["feature_family"]) == key]
        family_summary[f"{key[0]}::{key[1]}"] = {
            "attempted": len(subset), "applied": sum(r["mutation_applied"] for r in subset),
            "valid": sum(r["mutation_applied"] and r["valid_pdf"] for r in subset),
            "ground_truth_faults": sum(r["independently_established_fault"] for r in subset),
            "comparator_detections": sum(r["comparator_classification_changed"] is True for r in subset),
        }
    report = {
        "protocol": "V8 cross-converter mutation audit",
        "timestamp_utc": timestamp,
        "unit": "one pre-existing variant-A output per family and pipeline; no new converter run",
        "attempted": len(rows),
        "application_success": sum(r["mutation_applied"] for r in rows),
        "valid": sum(r["mutation_applied"] and r["valid_pdf"] for r in rows),
        "independently_established_faults": sum(r["independently_established_fault"] for r in rows),
        "comparator_detections": sum(r["comparator_classification_changed"] is True for r in rows),
        "family_summary": family_summary,
        "rows": rows,
        "limitations": ["This reuses archived converter outputs and does not establish temporal or stage-level causality.", "The independent oracle is limited to direct object transitions named by the operator.", "No human adjudication or PDF/UA conformance claim is made."],
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("attempted", "application_success", "valid", "independently_established_faults", "comparator_detections")}, indent=2))


if __name__ == "__main__":
    main()
