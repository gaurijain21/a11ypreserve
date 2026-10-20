from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
REPORTS = ROOT / "reports" / "v6"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def packet_id(pipeline: str, fixture_id: str) -> str:
    digest = hashlib.sha256(f"{pipeline}:{fixture_id}".encode("utf-8")).hexdigest()
    return f"P-{digest[:12].upper()}"


def main() -> None:
    mutation_path = V6 / "V6_MUTATION_SENSITIVITY.json"
    mutation = load_json(mutation_path)
    rows = mutation["rows"]
    valid = [row for row in rows if row["mutation_applied"] and row["valid_pdf"]]
    classification_detected = [row for row in valid if row["classification_changed"]]
    evidence_detected = [row for row in valid if row["extracted_evidence_changed"]]
    contract_detected = [row for row in valid if row["contracted_semantics_changed"]]
    coarse_survivors = [row for row in valid if row["extracted_evidence_changed"] and not row["classification_changed"]]
    meaningful_survivors = [row for row in rows if row["semantically_meaningful_survival"]]

    family_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        family_rows[row["feature_family"]].append(row)
    family_summary = {}
    for family, family_values in sorted(family_rows.items()):
        applied = [row for row in family_values if row["mutation_applied"] and row["valid_pdf"]]
        family_summary[family] = {
            "attempted": len(family_values),
            "valid_applied": len(applied),
            "classification_detections": sum(row["classification_changed"] for row in applied),
            "contracted_evidence_detections": sum(row["contracted_semantics_changed"] for row in applied),
            "evidence_drift_alerts": sum(row["extracted_evidence_changed"] for row in applied),
            "coarse_classification_survivors": sum(
                row["extracted_evidence_changed"] and not row["classification_changed"] for row in applied
            ),
            "meaningful_survivors": sum(row["semantically_meaningful_survival"] for row in family_values),
            "unsupported": sum(row["outcome_status"] == "UNSUPPORTED" for row in family_values),
        }

    independent_path = ROOT / "experiments" / "v5" / "independent_oracle_validation.json"
    independent = load_json(independent_path)
    source_manifest = load_json(ROOT / "experiments" / "v4" / "source_manifest.json")
    holdout_manifest = load_json(ROOT / "experiments" / "v4" / "HOLDOUT_MANIFEST.json")
    external_report_path = ROOT / "reports" / "EXTERNAL_VALIDITY_ARM.md"
    external_report = external_report_path.read_text(encoding="utf-8")
    natural_corpus = "no natural real-world corpus was added" in external_report.lower()
    integrated_match = re.search(r"three project-generated.*?(\d+) property.?pipeline observations", external_report)
    integrated_observations = int(integrated_match.group(1)) if integrated_match else None

    adjudication_rows = []
    for row in independent["rows"]:
        adjudication_rows.append(
            {
                "packet_id": packet_id(row["pipeline"], row["fixture_id"]),
                "pipeline": row["pipeline"],
                "source_case": row["fixture_id"],
                "pdf_sha256": row["evidence"]["pdf_sha256"],
                "source_evidence_path": "experiments/v5/independent_oracle_validation.json",
                "labels_in_packet": False,
                "adjudication_status": "PENDING_HUMAN_REVIEW",
            }
        )

    payload = {
        "protocol": "V6 additive objection mitigation audit",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "historical_artifacts_unchanged": True,
        "ground_truth_boundary": {
            "primary_cases": 130,
            "primary_adjudicated_ground_truth": False,
            "known_fault_reference_labels": "operator application and changed PDF hashes are construction-known for valid applied mutants",
            "known_fault_valid_applied": len(valid),
            "known_fault_classification_detections": len(classification_detected),
            "known_fault_evidence_detections": len(evidence_detected),
            "known_fault_contracted_evidence_detections": len(contract_detected),
            "independent_diagnostic_cases": independent["sample_size"],
            "independent_diagnostic_agreements": independent["agreement"],
            "independent_diagnostic_disagreements": independent["disagreement"],
            "human_adjudication": "NOT_EXECUTED",
            "mitigation": "A blinded packet index and rubric are prepared; no human adjudication result is claimed.",
        },
        "external_validity_boundary": {
            "atomic_fixtures": len(source_manifest["records"]),
            "primary_cases_per_pipeline": 65,
            "primary_cases_total": 130,
            "holdout_variants_per_family": 2,
            "holdout_fixture_count": holdout_manifest["holdout_count"],
            "holdout_cases_per_pipeline": 26,
            "holdout_is_independent_natural_corpus": False,
            "natural_document_corpus_available": not natural_corpus,
            "integrated_project_created_documents": 3,
            "integrated_property_pipeline_observations": integrated_observations,
            "integrated_arm_role": "secondary applicability sanity arm; excluded from primary denominator and prevalence claims",
            "mitigation": "Family-level mutation results, paired pipeline counts, and an explicitly labeled integrated arm are reported without population generalization.",
        },
        "survivor_mitigation": {
            "valid_applied_mutants": len(valid),
            "coarse_classification_detections": len(classification_detected),
            "evidence_drift_alerts": len(evidence_detected),
            "contracted_evidence_detections": len(contract_detected),
            "evidence_drift_alert_rate": f"{len(evidence_detected)}/{len(valid)}",
            "coarse_classification_survivors": len(coarse_survivors),
            "meaningful_survivors": len(meaningful_survivors),
            "alert_policy": "Raise EVIDENCE_DRIFT_ALERT whenever valid applied mutation changes normalized extracted evidence, even if six-way classification is unchanged.",
            "scope": "Additive V6 diagnostic layer; it does not rewrite frozen classifications or call evidence drift a six-way detection.",
            "family_summary": family_summary,
            "survivor_cases": [
                {
                    "fixture_id": row["fixture_id"],
                    "feature_family": row["feature_family"],
                    "operator": row["mutation_operator"],
                    "baseline_classification": row["baseline_classification"],
                    "mutated_classification": row["mutated_classification"],
                    "classification_changed": row["classification_changed"],
                    "evidence_drift_alert": row["extracted_evidence_changed"],
                    "contracted_semantics_changed": row["contracted_semantics_changed"],
                    "outcome_status": row["outcome_status"],
                }
                for row in meaningful_survivors
            ],
        },
        "adjudication_packet_index": adjudication_rows,
        "evidence": {
            "mutation": str(mutation_path.relative_to(ROOT)).replace("\\", "/"),
            "independent_validation": str(independent_path.relative_to(ROOT)).replace("\\", "/"),
            "external_validity": str(external_report_path.relative_to(ROOT)).replace("\\", "/"),
            "mutation_sha256": sha256(mutation_path),
            "independent_validation_sha256": sha256(independent_path),
        },
    }
    output_path = V6 / "V6_OBJECTION_MITIGATIONS.json"
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# V6 objection mitigation audit",
        "",
        "This is an additive V6 diagnostic and release-hardening artifact. It does not rewrite V4/V5/V6 frozen classifications, fixtures, evidence, or denominators.",
        "",
        "## 1. Independent ground truth",
        "",
        f"- Primary cases: **{payload['ground_truth_boundary']['primary_cases']}**; independent human adjudicated labels: **NO**.",
        f"- The known-fault arm has **{len(valid)}/{len(valid)}** valid applied mutants with construction-known fault application, **{len(classification_detected)}/{len(valid)}** coarse-classification detections, and **{len(evidence_detected)}/{len(valid)}** evidence-drift alerts.",
        f"- The historical diagnostic cross-check remains **{independent['agreement']}/{independent['sample_size']}** agreement with **{independent['disagreement']}** disagreements; it is not external ground truth.",
        "- Mitigation: a blinded packet index and adjudication rubric are prepared for human review. No adjudication result is claimed until an authorized independent reviewer actually completes it.",
        "",
        "## 2. External validity",
        "",
        f"- The primary design remains **{len(source_manifest['records'])} atomic fixtures × 2 pipelines = 130 cases**.",
        f"- The holdout remains **{holdout_manifest['holdout_count']} fixtures per pipeline**, a within-design holdout rather than an independent natural corpus.",
        f"- The secondary integrated arm contains **3 project-created documents and {integrated_observations} property–pipeline observations**; it is not a natural-document sample and is excluded from prevalence claims.",
        "- Mitigation: family-level sensitivity, paired pipeline counts, and the integrated applicability arm are reported as descriptive coverage evidence only. No converter ranking or population estimate is asserted.",
        "",
        "## 3. Ten survivors",
        "",
        f"- Frozen coarse result: **{len(classification_detected)}/{len(valid)}** detections and **{len(meaningful_survivors)}** meaningful survivors.",
        f"- Additive two-level mitigation: **{len(evidence_detected)}/{len(valid)}** valid mutants raised an evidence-drift alert; this includes the ten meaningful survivors and three additional unchanged-classification evidence changes.",
        "- The alert is operationally useful because it prevents a same-category result from being treated as unchanged evidence. It is deliberately not relabeled as a six-way classification detection.",
        "- Survivor cases and family-level rates are recorded in the JSON trace. The survivors remain visible as fault-model limitations.",
        "",
        "## Status",
        "",
        "- Executed: survivor derivation, family summary, evidence-drift alert accounting, packet indexing, and source-hash capture.",
        "- Not executed: independent human adjudication, rights-cleared natural corpus study, and assistive-technology usability study.",
        "- Result: the objections are narrowed and made actionable, but not falsely claimed to be eliminated.",
        "",
        f"Machine evidence: `experiments/v6/V6_OBJECTION_MITIGATIONS.json` (generated {payload['generated_at_utc']}).",
    ]
    (REPORTS / "V6_OBJECTION_MITIGATIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    protocol = """# V6 blinded adjudication protocol

## Purpose

This protocol is prepared to reduce the remaining independent-ground-truth objection without fabricating an adjudication. It is a future human-review arm and is not an executed V6 result.

## Packet population

The packet index covers the 26 cases in `experiments/v5/independent_oracle_validation.json`. Each packet has a stable opaque ID, the PDF hash, and a pointer to the preserved evidence record. The expected comparator and diagnostic labels are omitted from the packet index. A coordinator must create a separate key before review and must not give reviewers the historical labels.

## Reviewer task

For each packet, the reviewer receives the source contract, source OOXML excerpts needed for the feature, the destination PDF, and extracted evidence from the independent paths. The reviewer records one of: `PRESERVED`, `ALTERED`, `LOST`, `PARTIAL`, `UNRESOLVED`, or `MEASUREMENT_ERROR`, plus an evidence citation and confidence. If the evidence cannot establish the relation, the reviewer must abstain rather than infer from tags, visible text, or the expected result.

## Blinding and adjudication

Reviewers must not see fixture IDs, pipeline labels, historical classifications, or mutation outcomes. Two qualified reviewers should work independently. Disagreements should be resolved by a third adjudicator or a documented consensus procedure. Report agreement, abstention, disagreement reasons, and the final rubric version. Do not pool reviewer labels with V4/V5 classifications without a separately versioned analysis.

## Current status

`PENDING_HUMAN_REVIEW`. No reviewer, adjudication, agreement statistic, or independent ground-truth claim is asserted by this repository state.
"""
    (REPORTS / "V6_BLINDED_ADJUDICATION_PROTOCOL.md").write_text(protocol, encoding="utf-8")
    (V6 / "V6_ADJUDICATION_PACKET_INDEX.json").write_text(
        json.dumps({"protocol": "reports/v6/V6_BLINDED_ADJUDICATION_PROTOCOL.md", "status": "PENDING_HUMAN_REVIEW", "packets": adjudication_rows}, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "status": "PASS",
        "valid_applied_mutants": len(valid),
        "classification_detections": len(classification_detected),
        "evidence_drift_alerts": len(evidence_detected),
        "meaningful_survivors": len(meaningful_survivors),
        "adjudication_packets": len(adjudication_rows),
    }, indent=2))


if __name__ == "__main__":
    main()
