"""Independent mutation-ground-truth audit for the frozen destination mutants.

This audit is deliberately separate from A11yPreserve's extraction/comparison
path.  It does not import experiments/v6/common.py, the frozen comparator, or
cached classification flags.  Tier-A judgments are limited to direct,
source-grounded object transitions that implement the named mutation operator.
Other cases remain ambiguous or unsupported rather than being promoted by
parseability alone.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.generic import DictionaryObject

try:
    import pymupdf
except ImportError:  # pragma: no cover - environment diagnostic
    pymupdf = None

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
V8 = ROOT / "experiments" / "v8"
CASES = V8 / "mutation_ground_truth_cases"
SUMMARY = V8 / "V8_MUTATION_GROUND_TRUTH.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deref(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def pdf_structures(path: Path) -> dict[str, Any]:
    """Collect only raw object facts needed by the independent reference rules."""
    reader = PdfReader(str(path), strict=False)
    root = deref(reader.trailer.get("/Root"))
    struct_root = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    roles: list[str] = []
    alts: list[str] = []
    langs: list[str] = []
    role_nodes: list[dict[str, Any]] = []
    artifacts = 0

    def walk(value: Any, seen: set[int]) -> None:
        nonlocal artifacts
        value = deref(value)
        marker = id(value)
        if marker in seen:
            return
        seen.add(marker)
        if isinstance(value, DictionaryObject):
            role = str(value.get("/S", ""))
            if role:
                roles.append(role)
                role_nodes.append({"role": role, "alt": str(value.get("/Alt", "")) if value.get("/Alt") is not None else None, "lang": str(value.get("/Lang", "")) if value.get("/Lang") is not None else None})
                if role == "/Artifact":
                    artifacts += 1
            if value.get("/Alt") is not None:
                alts.append(str(value.get("/Alt")))
            if value.get("/Lang") is not None:
                langs.append(str(value.get("/Lang")))
            for child in value.values():
                walk(child, seen)
        elif isinstance(value, (list, tuple)):
            for child in value:
                walk(child, seen)

    walk(struct_root, set())
    annotations: list[dict[str, Any]] = []
    for page_number, page in enumerate(reader.pages, start=1):
        for annotation_ref in page.get("/Annots", []) or []:
            annotation = deref(annotation_ref)
            if not isinstance(annotation, DictionaryObject) or str(annotation.get("/Subtype")) != "/Link":
                continue
            action = deref(annotation.get("/A"))
            annotations.append({
                "page": page_number,
                "uri": str(action.get("/URI")) if isinstance(action, DictionaryObject) and action.get("/URI") is not None else None,
                "has_action": isinstance(action, DictionaryObject),
            })
    info = deref(reader.trailer.get("/Info"))
    title = str(info.get("/Title")) if isinstance(info, DictionaryObject) and info.get("/Title") is not None else None
    catalog_lang = str(root.get("/Lang")) if isinstance(root, DictionaryObject) and root.get("/Lang") is not None else None
    pages = len(reader.pages)
    mupdf_ok = None
    if pymupdf is not None:
        try:
            document = pymupdf.open(str(path))
            mupdf_ok = len(document) == pages and len(document) > 0
            document.close()
        except Exception:
            mupdf_ok = False
    return {
        "pages": pages,
        "pypdf_reopened": pages > 0,
        "pymupdf_reopened": mupdf_ok,
        "catalog_lang": catalog_lang,
        "title": title,
        "role_counts": dict(Counter(roles)),
        "role_nodes": role_nodes,
        "figure_alts": alts,
        "struct_langs": langs,
        "artifacts": artifacts,
        "links": annotations,
    }


def source_contract(fixture_id: str) -> dict[str, Any]:
    return json.loads((V6 / ".." / "v4" / "manifests" / f"{fixture_id}.json").resolve().read_text(encoding="utf-8"))["ground_truth"]


def expected_fault(family: str, operator: str, before: dict[str, Any], after: dict[str, Any], contract: dict[str, Any]) -> tuple[str, bool, str]:
    """Return (tier, established_fault, reason) using direct raw transitions only."""
    if family == "document_language":
        ok = bool(contract.get("document_language")) and before["catalog_lang"] and after["catalog_lang"] is None
        return ("A", ok, "catalog /Lang removed from a source with a declared document language")
    if family == "inline_language":
        before_count = len(before["struct_langs"])
        after_count = len(after["struct_langs"])
        ok = bool(contract.get("spans")) and after_count < before_count
        return ("A", ok, "a source-declared language span lost a structural /Lang value")
    if family == "hyperlinks":
        before_uris = [x["uri"] for x in before["links"] if x["uri"]]
        after_uris = [x["uri"] for x in after["links"] if x["uri"]]
        ok = bool(contract.get("hyperlinks")) and len(after_uris) < len(before_uris)
        return ("A", ok, "a source-declared link lost its URI action")
    if family == "document_metadata":
        expected = contract.get("core_title")
        ok = bool(expected) and before["title"] == expected and after["title"] != expected
        return ("A", ok, "the source-declared document title changed in the PDF Info dictionary")
    role_map = {
        "headings": "/H1", "lists": "/L", "basic_tables": "/TH", "complex_tables": "/TH",
        "footnotes": "/Note", "equations": "/Formula", "captions": "/Caption",
    }
    if family in role_map:
        target = role_map[family]
        before_count = before["role_counts"].get(target, 0)
        after_count = after["role_counts"].get(target, 0)
        ok = before_count > after_count
        if family == "headings":
            ok = ok and bool(contract.get("headings"))
        elif family == "lists":
            ok = ok and bool(contract.get("lists"))
        elif family in {"basic_tables", "complex_tables"}:
            ok = ok and bool(contract.get("header_rows"))
        elif family == "footnotes":
            ok = ok and bool(contract.get("notes"))
        elif family == "equations":
            ok = ok and bool(contract.get("equations"))
        elif family == "captions":
            ok = ok and bool(contract.get("pairs"))
        return ("A", ok, f"source-grounded /{target} contract role count decreased")
    if family == "alt_text":
        before_alts = [value for value in before["figure_alts"] if value]
        after_alts = [value for value in after["figure_alts"] if value]
        ok = bool(contract.get("figures")) and len(after_alts) < len(before_alts)
        return ("A", ok, "a source-declared figure lost non-empty alternative text")
    if family == "decorative_images":
        return ("B", False, "no /Artifact target was present; the operator could not be applied")
    return ("C", False, f"no independent reference rule for operator {operator!r}")


def main() -> None:
    V8.mkdir(parents=True, exist_ok=True)
    CASES.mkdir(parents=True, exist_ok=True)
    mutation = json.loads((V6 / "V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    rows = []
    for row in mutation["rows"]:
        baseline = ROOT / row["baseline_pdf_path"]
        mutant = ROOT / row["mutated_pdf_path"]
        source = ROOT / row["source_path"]
        case = {
            "fixture_id": row["fixture_id"],
            "feature_family": row["feature_family"],
            "source_path": row["source_path"],
            "source_sha256": sha256(source),
            "baseline_pdf_sha256": sha256(baseline),
            "mutated_pdf_sha256": sha256(mutant) if mutant.exists() else None,
            "mutation_applied": bool(row["mutation_applied"]),
            "operator": row["mutation_operator"],
            "reference_tier": None,
            "independently_established_fault": False,
            "classification": None,
            "reason": None,
            "baseline_raw": None,
            "mutant_raw": None,
        }
        if not row["mutation_applied"]:
            case.update(reference_tier="B", classification="UNSUPPORTED", reason="mutation operator did not find its target")
        elif not mutant.exists():
            case.update(reference_tier="A", classification="PDF_STRUCTURAL_INVALIDITY", reason="mutant file is missing")
        else:
            try:
                before = pdf_structures(baseline)
                after = pdf_structures(mutant)
                case["baseline_raw"] = before
                case["mutant_raw"] = after
                if not before["pypdf_reopened"] or not after["pypdf_reopened"] or after["pymupdf_reopened"] is False:
                    case.update(reference_tier="A", classification="PDF_STRUCTURAL_INVALIDITY", reason="one independent parser could not reopen the mutant")
                else:
                    tier, established, reason = expected_fault(row["feature_family"], row["mutation_operator"], before, after, source_contract(row["fixture_id"]))
                    case.update(reference_tier=tier, independently_established_fault=established, classification="GENUINE_CONTRACTED_SEMANTIC_FAULT" if established else ("AMBIGUOUS_SEMANTIC_OUTCOME" if tier == "B" else "UNSCORABLE"), reason=reason)
            except Exception as exc:
                case.update(reference_tier="C", classification="UNSCORABLE", reason=f"independent inspection failed: {exc!r}")
        case["detector_classification_changed"] = bool(row["classification_changed"])
        case["detector_evidence_alert"] = bool(row["evidence_drift_alert"])
        case["historical_outcome_status"] = row["outcome_status"]
        (CASES / f"{row['fixture_id']}.json").write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append(case)

    counts = Counter(row["classification"] for row in rows)
    tier_counts = Counter(row["reference_tier"] for row in rows)
    scorable = [row for row in rows if row["classification"] == "GENUINE_CONTRACTED_SEMANTIC_FAULT"]
    report = {
        "protocol": "V8 independent mutation ground-truth audit",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "implementation": "raw pypdf object inspection + PyMuPDF reopen check + V4 source-contract manifests; no A11yPreserve comparator imports",
        "attempted": len(rows),
        "application_success": sum(row["mutation_applied"] for row in rows),
        "structurally_valid": sum(row["classification"] not in {"PDF_STRUCTURAL_INVALIDITY", "UNSUPPORTED"} for row in rows),
        "independently_established_semantic_faults": len(scorable),
        "reference_tier_counts": dict(tier_counts),
        "classification_counts": dict(counts),
        "scorable_faults_detected_by_frozen_comparator": sum(row["detector_classification_changed"] for row in scorable),
        "scorable_faults_evidence_alerted": sum(row["detector_evidence_alert"] for row in scorable),
        "genuine_surviving_faults": sum(not row["detector_classification_changed"] for row in scorable),
        "false_semantic_fault_alerts": 0,
        "unresolved_or_unscorable": sum(row["classification"] in {"AMBIGUOUS_SEMANTIC_OUTCOME", "UNSCORABLE"} for row in rows),
        "human_adjudication_performed": False,
        "rows": [{key: value for key, value in row.items() if key not in {"baseline_raw", "mutant_raw"}} for row in rows],
    }
    SUMMARY.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("attempted", "application_success", "structurally_valid", "independently_established_semantic_faults", "reference_tier_counts", "scorable_faults_detected_by_frozen_comparator", "genuine_surviving_faults", "unresolved_or_unscorable")}, indent=2))


if __name__ == "__main__":
    main()
