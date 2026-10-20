from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject

from common import V6, load_atomic_records, run_case, sha256, tool_versions, normalized_hash


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


def mutate(reader: PdfReader, family: str) -> tuple[bool, str, str]:
    root = deref(reader.trailer.get("/Root"))
    struct = deref(root.get("/StructTreeRoot")) if isinstance(root, DictionaryObject) else None
    if family == "document_language":
        if isinstance(root, DictionaryObject) and root.get("/Lang") is not None:
            del root[NameObject("/Lang")]
            return True, "removed catalog /Lang", "catalog /Lang"
        return False, "catalog /Lang absent", "catalog /Lang"
    if family == "inline_language":
        changed = walk(struct, lambda node: node.get("/S") not in {NameObject("/Document"), NameObject("/Part")} and node.pop(NameObject("/Lang"), None) is not None)
        return changed, "removed first inline StructElem /Lang" if changed else "inline /Lang absent", "inline /Lang"
    if family == "hyperlinks":
        for page in reader.pages:
            for annotation_ref in page.get("/Annots", []) or []:
                annotation = deref(annotation_ref)
                if isinstance(annotation, DictionaryObject) and str(annotation.get("/Subtype")) == "/Link":
                    action = deref(annotation.get("/A"))
                    if isinstance(action, DictionaryObject) and action.get("/URI") is not None:
                        del action[NameObject("/URI")]
                        return True, "removed first Link /URI", "link URI"
        return False, "URI absent", "link URI"
    if family == "document_metadata":
        info = deref(reader.trailer.get("/Info"))
        if isinstance(info, DictionaryObject):
            info[NameObject("/Title")] = TextStringObject("V6 MUTATED TITLE")
            return True, "changed document title", "document title"
        return False, "document info dictionary absent", "document title"
    roles = {"headings": "/H1", "lists": "/L", "basic_tables": "/TH", "complex_tables": "/TH", "footnotes": "/Note", "equations": "/Formula", "captions": "/Caption"}
    if family in roles:
        role = roles[family]

        def change(node: DictionaryObject) -> bool:
            if node.get("/S") != NameObject(role):
                return False
            if family == "headings":
                node[NameObject("/S")] = NameObject("/P")
            elif family in {"basic_tables", "complex_tables"}:
                node[NameObject("/S")] = NameObject("/TD")
            else:
                del node[NameObject("/S")]
            return True

        changed = walk(struct, change)
        return changed, f"mutated first {role} role" if changed else f"{role} role absent", role
    if family == "alt_text":
        changed = walk(struct, lambda node: node.get("/S") == NameObject("/Figure") and node.pop(NameObject("/Alt"), None) is not None)
        return changed, "removed first Figure /Alt" if changed else "Figure /Alt absent", "figure alt text"
    if family == "decorative_images":

        def change_artifact(node: DictionaryObject) -> bool:
            if node.get("/S") != NameObject("/Artifact"):
                return False
            node[NameObject("/S")] = NameObject("/Figure")
            return True

        changed = walk(struct, change_artifact)
        return changed, "changed first Artifact to Figure" if changed else "Artifact role absent", "decorative image role"
    return False, "unsupported mutation operator", "unsupported"


def valid_pdf(path: Path) -> tuple[bool, str | None]:
    try:
        return len(PdfReader(str(path)).pages) > 0, None
    except Exception as exc:
        return False, repr(exc)


def main() -> None:
    started = datetime.now(timezone.utc).isoformat()
    mutant_dir = V6 / "destination_mutants"
    case_dir = V6 / "mutation_cases"
    mutant_dir.mkdir(parents=True, exist_ok=True)
    case_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for record in load_atomic_records():
        out = mutant_dir / f"{record['fixture_id']}.pdf"
        baseline_result = None
        mutant_result = None
        changed = False
        mutation_note = ""
        target = ""
        valid = False
        error = None
        try:
            baseline_result = run_case(record["source_path"], record["pdf_path"], record["family"])
            reader = PdfReader(str(record["pdf_path"]))
            changed, mutation_note, target = mutate(reader, record["family"])
            writer = PdfWriter()
            writer.clone_document_from_reader(reader)
            with out.open("wb") as stream:
                writer.write(stream)
            valid, error = valid_pdf(out)
            if valid and changed:
                mutant_result = run_case(record["source_path"], out, record["family"])
        except Exception as exc:
            error = repr(exc)

        baseline_evidence_hash = baseline_result["semantic_evidence_sha256"] if baseline_result else None
        mutant_evidence_hash = mutant_result["semantic_evidence_sha256"] if mutant_result else None
        evidence_changed = baseline_evidence_hash != mutant_evidence_hash if baseline_result and mutant_result else False
        # The contracted-semantics signature includes feature evidence, not just
        # the coarse label. This is what exposes a mutant that changes relevant
        # evidence while remaining in the same six-way category.
        contracted_before = {
            "signature_sha256": normalized_hash({"raw": baseline_result.get("raw"), "destination": baseline_result.get("destination")}) if baseline_result else None,
            "classification": baseline_result.get("classification") if baseline_result else None,
            "raw_fidelity": baseline_result.get("raw", {}).get("fidelity_classification") if baseline_result else None,
            "destination_accessibility": baseline_result.get("raw", {}).get("destination_accessibility") if baseline_result else None,
        }
        contracted_after = {
            "signature_sha256": normalized_hash({"raw": mutant_result.get("raw"), "destination": mutant_result.get("destination")}) if mutant_result else None,
            "classification": mutant_result.get("classification") if mutant_result else None,
            "raw_fidelity": mutant_result.get("raw", {}).get("fidelity_classification") if mutant_result else None,
            "destination_accessibility": mutant_result.get("raw", {}).get("destination_accessibility") if mutant_result else None,
        }
        contracted_changed = contracted_before != contracted_after if baseline_result and mutant_result else False
        classification_changed = bool(baseline_result and mutant_result and baseline_result["classification"] != mutant_result["classification"])
        semantically_meaningful_survival = bool(valid and changed and evidence_changed and not classification_changed and contracted_changed)
        if not changed:
            outcome_status = "UNSUPPORTED"
            inconclusive_reason = mutation_note
        elif not valid:
            outcome_status = "INVALID_MUTANT"
            inconclusive_reason = error or "mutated PDF did not reopen"
        elif error or mutant_result is None:
            outcome_status = "INCONCLUSIVE"
            inconclusive_reason = error or "mutant extraction did not complete"
        elif semantically_meaningful_survival:
            outcome_status = "SEMANTICALLY_MEANINGFUL_SURVIVAL"
            inconclusive_reason = "contracted evidence changed but coarse classification did not"
        elif classification_changed:
            outcome_status = "CLASSIFICATION_DETECTED"
            inconclusive_reason = "classification changed after a valid applied mutation"
        elif not evidence_changed:
            outcome_status = "NON_EFFECTIVE_MUTANT"
            inconclusive_reason = "operator applied but normalized semantic evidence did not change"
        else:
            outcome_status = "UNCHANGED_CLASSIFICATION"
            inconclusive_reason = "evidence changed without a contracted-semantics or classification change"
        row = {
            "protocol": "V6 destination mutation sensitivity",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "fixture_id": record["fixture_id"],
            "feature_family": record["family"],
            "mutation_operator": mutation_note,
            "mutation_target": target,
            "source_path": str(record["source_path"].relative_to(V6.parents[1])).replace("\\", "/"),
            "baseline_pdf_path": str(record["pdf_path"].relative_to(V6.parents[1])).replace("\\", "/"),
            "mutated_pdf_path": str(out.relative_to(V6.parents[1])).replace("\\", "/"),
            "baseline_pdf_sha256": sha256(record["pdf_path"]),
            "mutated_pdf_sha256": sha256(out) if out.exists() else None,
            "mutation_applied": changed,
            "valid_pdf": valid,
            "error": error,
            "baseline_classification": baseline_result["classification"] if baseline_result else "EXTRACTION_FAILURE",
            "mutated_classification": mutant_result["classification"] if mutant_result else None,
            "baseline_noncanonical_status": baseline_result["classification"] if baseline_result and baseline_result["classification"] not in {"VERIFIED_PRESERVED", "ALTERED", "CONFIRMED_LOST"} else None,
            "raw_semantic_evidence_before": baseline_result["raw"] if baseline_result else None,
            "raw_semantic_evidence_after": mutant_result["raw"] if mutant_result else None,
            "normalized_evidence_sha256_before": baseline_evidence_hash,
            "normalized_evidence_sha256_after": mutant_evidence_hash,
            "extracted_evidence_changed": evidence_changed,
            "contracted_semantics_before": contracted_before,
            "contracted_semantics_after": contracted_after,
            "contracted_semantics_changed": contracted_changed,
            "classification_changed": classification_changed,
            "genuinely_undetected": semantically_meaningful_survival,
            "semantically_meaningful_survival": semantically_meaningful_survival,
            "outcome_status": outcome_status,
            "inconclusive_or_unsupported_reason": inconclusive_reason,
            "tool_versions": tool_versions(),
        }
        (case_dir / f"{record['fixture_id']}.json").write_text(json.dumps(row, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append(row)

    family_summary = {}
    for family in sorted({row["feature_family"] for row in rows}):
        family_rows = [row for row in rows if row["feature_family"] == family]
        family_summary[family] = {
            "attempted": len(family_rows),
            "applied": sum(row["mutation_applied"] for row in family_rows),
            "valid": sum(row["valid_pdf"] and row["mutation_applied"] for row in family_rows),
            "classification_detected": sum(row["outcome_status"] == "CLASSIFICATION_DETECTED" for row in family_rows),
            "semantically_meaningful_survival": sum(row["semantically_meaningful_survival"] for row in family_rows),
            "unsupported": sum(row["outcome_status"] == "UNSUPPORTED" for row in family_rows),
            "inconclusive": sum(row["outcome_status"] in {"INVALID_MUTANT", "INCONCLUSIVE"} for row in family_rows),
            "non_effective": sum(row["outcome_status"] == "NON_EFFECTIVE_MUTANT" for row in family_rows),
            "unchanged_classification": sum(row["outcome_status"] == "UNCHANGED_CLASSIFICATION" for row in family_rows),
            "baseline_classifications": dict(Counter(row["baseline_classification"] for row in family_rows)),
        }
    counts = Counter(row["outcome_status"] for row in rows)
    report = {
        "protocol": "V6 Phase B destination mutation sensitivity",
        "status": "COMPLETE" if len(rows) == 65 else "INCOMPLETE",
        "started_at_utc": started,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "attempted": len(rows),
        "valid_applied_mutants": sum(row["valid_pdf"] and row["mutation_applied"] for row in rows),
        "classification_level_detections": sum(row["outcome_status"] == "CLASSIFICATION_DETECTED" for row in rows),
        "semantically_meaningful_survivals": sum(row["semantically_meaningful_survival"] for row in rows),
        "unsupported_attempts": sum(row["outcome_status"] == "UNSUPPORTED" for row in rows),
        "invalid_mutants": sum(row["outcome_status"] == "INVALID_MUTANT" for row in rows),
        "inconclusive_attempts": sum(row["outcome_status"] == "INCONCLUSIVE" for row in rows),
        "non_effective_mutants": sum(row["outcome_status"] == "NON_EFFECTIVE_MUTANT" for row in rows),
        "unchanged_classification_mutants": sum(row["outcome_status"] == "UNCHANGED_CLASSIFICATION" for row in rows),
        "outcome_counts": dict(counts),
        "family_summary": family_summary,
        "tool_versions": tool_versions(),
        "definition": {
            "application_success": "mutation_applied",
            "validity": "valid_pdf",
            "evidence_detection": "extracted_evidence_changed",
            "contract_detection": "contracted_semantics_changed",
            "classification_detection": "classification_changed",
            "meaningful_survival": "valid applied mutation with changed normalized evidence and contracted semantics but unchanged classification",
        },
        "rows": [{key: value for key, value in row.items() if key not in {"raw_semantic_evidence_before", "raw_semantic_evidence_after"}} for row in rows],
    }
    (V6 / "V6_MUTATION_SENSITIVITY.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "attempted", "valid_applied_mutants", "classification_level_detections", "semantically_meaningful_survivals", "unsupported_attempts", "invalid_mutants", "inconclusive_attempts")}, indent=2))
    if report["status"] != "COMPLETE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
