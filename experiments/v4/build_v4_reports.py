from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "v4"


def main() -> None:
    source = json.loads((BASE / "source_manifest.json").read_text(encoding="utf-8"))
    validation = json.loads((BASE / "SOURCE_VALIDATION.json").read_text(encoding="utf-8"))
    oracle = json.loads((BASE / "SOURCE_ORACLE_MUTATION_AUDIT.json").read_text(encoding="utf-8"))
    calibration = json.loads((BASE / "COMPARATOR_CALIBRATION.json").read_text(encoding="utf-8"))
    realistic = json.loads((BASE / "realistic" / "REALISTIC_SOURCE_VALIDATION.json").read_text(encoding="utf-8"))
    inventory = json.loads((BASE / "converter_inventory.json").read_text(encoding="utf-8"))
    primary = {"status": "NOT_RUN", "reason": "No legitimate V4 converter pipeline was available in the recorded environment.", "feature_families": source["feature_family_count"], "variants_per_feature": source["variants_per_feature"], "atomic_fixtures": source["fixture_count"], "converters": [], "primary_cases": 0, "records": []}
    (BASE / "results").mkdir(exist_ok=True)
    (BASE / "results" / "V4_PRIMARY_RESULTS.json").write_text(json.dumps(primary, indent=2) + "\n", encoding="utf-8")
    accounting = {"status": "NOT_RUN", "development_cases": 0, "holdout_cases": 0, "primary_cases": 0, "unresolved_cases": None, "measurement_errors": None, "reason": primary["reason"]}
    (BASE / "results" / "V4_ACCOUNTING.json").write_text(json.dumps(accounting, indent=2) + "\n", encoding="utf-8")
    (BASE / "results" / "V4_ACCOUNTING.md").write_text("# V4 Machine-Generated Accounting\n\n| Quantity | Value |\n|---|---:|\n| Atomic fixtures | 65 |\n| Established primary converters | 0 |\n| Primary conversion cases | 0 |\n| Unresolved conversion cases | Not applicable |\n| Measurement errors | Not applicable |\n\nNo V4 converter output was available; these are not preservation results.\n", encoding="utf-8")

    (ROOT / "V3_V4_STRENGTHENING_REPORT.md").write_text("""# V3–V4 Strengthening Report

V3 remains frozen historical evidence. V4 is a prospective extension; because no legitimate V4 converter was available, V4 conversion-result cells are explicitly not run.

| Dimension | V3 | V4 |
|---|---:|---:|
| Feature families | 13 | 13 |
| Atomic variants per feature | 2 | 5 |
| Atomic fixtures | 26 | 65 |
| Converters | 2 | 0 established |
| Primary cases | 52 | 0 |
| Calibration controls | 27 | 78 |
| Source mutation tests | 6 | 39 |
| Holdout cases | 0 | 26 |
| Realistic documents | 3 project-created | 10 project-created |
| Realistic observations | 42 | 78 |
| Repeatability runs | 39 | 0 |
| Unresolved cases | 18 | not applicable |
| Measurement errors | 1 | not applicable |

The V4 extensions directly address fixture depth, oracle mutation evidence, calibration breadth, prospective holdout control, realistic coexistence, and explicit converter feasibility. The missing V4 conversion arm is a submission blocker, not a hidden zero-failure result.
""", encoding="utf-8")

    (ROOT / "FINAL_V4_ADVERSARIAL_REVIEW.md").write_text("""# Final V4 Adversarial Review

| Attack | Classification | Evidence / remaining issue |
|---|---|---|
| Novelty claims “first accessibility conversion study” | RESOLVED | Prior-art audit rejects that claim and states a combination-based contribution. |
| Too few variants per feature | RESOLVED | 65 fixtures, five meaningful variants per retained family. |
| Source truth is extractor-dependent | SUBSTANTIALLY MITIGATED | Raw-OOXML oracle, primary extractor, 65/65 certificates, and 39/39 mutation detections. |
| Comparator is biased or overconfident | SUBSTANTIALLY MITIGATED | 78 frozen controls, 0 false positives, 0 unsupported confident classifications; 5 false negatives remain. |
| Holdout is post-hoc | RESOLVED | D/E split and inspection rule frozen before converter execution. |
| Synthetic atomic corpus lacks external validity | SUBSTANTIALLY MITIGATED | Ten coherent project-created multi-page documents and 78 property contracts; no external documents. |
| Only two or three converters | ACCEPTED LIMITATION | No V4 converter environment was available; Word failed before conversion and LibreOffice was absent. |
| No actual V4 conversion results | SUBMISSION BLOCKER | Primary denominator is zero. |
| Reading order omitted | ACCEPTED LIMITATION | No defensible calibrated bounded oracle was established. |
| User impact not measured | ACCEPTED LIMITATION | Structural preservation, PDF accessibility, assistive technology, usability, and harm are explicitly separated. |
| Cloud route reproducibility | ACCEPTED LIMITATION | No authenticated Google session was available; no upload was attempted. |
| Artifact reproducibility | SUBSTANTIALLY MITIGATED | Source-only and calibration entry points plus manifests and hashes exist. |

Overall decision: NO-GO until at least one legitimate V4 converter pipeline produces a complete traceable output set and the frozen analysis is rerun.
""", encoding="utf-8")

    readiness = f"""# NO-GO

## Primary V4 experiment
- feature families: {source['feature_family_count']}
- variants: {source['variants_per_feature']} per feature
- fixtures: {source['fixture_count']}
- converters: 0 successfully established
- primary cases: 0

## Calibration
- controls: {calibration['control_count']}
- correct determinate: {calibration['counts']['correct']}
- false positives: {calibration['counts']['false_positives']}
- false negatives: {calibration['counts']['false_negatives']}
- correct unresolved: {calibration['counts']['correct_unresolved']}
- other unresolved: 0 unsupported confident classifications

## Holdout
- size: 26
- results: not run; outputs were not available
- unexpected failures: not applicable

## Realistic corpus
- documents: 10
- external: 0
- project-created: 10
- property observations: 78

## Repeatability
- runs: 0
- classification consistency: not run
- byte identity where relevant: not run

## Reading order
- excluded
- justification: a defensible bounded oracle did not pass calibration before conversion.

## Word
- unavailable for V4
- evidence: Word COM `DispatchEx` failed before conversion with `0x80070520`; no output was fabricated.

## Unresolved cases
- total: not applicable because primary conversion cases are zero
- reason categories: not applicable; no conversion evidence exists to classify.

## Novelty

A11yPreserve’s strongest defensible contribution is a prospective source-grounded preservation-testing protocol that combines known DOCX semantics, contract-level source truth, raw-OOXML checking, identical inputs across converter conditions, destination structure evidence, calibrated equivalence mapping, conservative abstention, and provenance certificates. It asks whether a particular author-supplied semantic known to exist before transformation survived the transformation, which is a different question from destination-only accessibility checking.

## Remaining reviewer attacks

The central blocker is the absence of V4 converter outputs. Additional limitations are the project-created realistic corpus, no reading-order extension, five comparator false negatives in calibration, no Word/Google V4 arm, no validator comparison, and no user study. These are disclosed rather than converted into claims.

## Submission blockers

- Establish at least one legitimate V4 converter pipeline and run all 65 fixtures under the frozen protocol.
- Preserve output hashes, extraction evidence, classifications, unresolved causes, and repeatability records.
- Only then create a V4 manuscript; V3 remains the only manuscript with conversion results.

Source validation status: {validation['status']} ({validation['raw_oracle_pass']}/{validation['fixture_count']} raw-oracle and {validation['primary_supported']}/{validation['fixture_count']} primary-extractor supported).
Mutation status: {oracle['status']} ({oracle['detected']}/{oracle['mutations']}).
Converter inventory: {inventory['primary_converter_count']} established.
"""
    (ROOT / "FINAL_V4_SUBMISSION_READINESS.md").write_text(readiness, encoding="utf-8")
    submission = ROOT / "submission" / "ICST2027_V4"
    submission.mkdir(parents=True, exist_ok=True)
    (submission / "README.md").write_text("# ICST2027 V4 Submission Placeholder\n\nV4 is currently **NO-GO** because no legitimate V4 converter pipeline produced output in the recorded environment. The V3 manuscript remains frozen at `submission/ICST2027_V3/`; do not replace it with this placeholder. Generate a V4 manuscript only after conversion-dependent results are frozen.\n\nRead `FINAL_V4_SUBMISSION_READINESS.md`, `FINAL_V4_ADVERSARIAL_REVIEW.md`, and `V3_V4_STRENGTHENING_REPORT.md`.\n", encoding="utf-8")
    print(json.dumps({"verdict": "NO-GO", "atomic_fixtures": source["fixture_count"], "calibration_controls": calibration["control_count"], "realistic_documents": realistic["documents"], "primary_cases": 0}, indent=2))


if __name__ == "__main__":
    main()
