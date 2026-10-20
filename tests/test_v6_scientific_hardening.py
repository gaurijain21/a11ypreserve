from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_control_disagreement_is_not_derived_from_expected_label() -> None:
    import sys

    sys.path.insert(0, str(ROOT / "experiments" / "v6"))
    from common import control_disagreement

    assert control_disagreement("VERIFIED_PRESERVED", "VERIFIED_PRESERVED") is False
    assert control_disagreement("ALTERED", "VERIFIED_PRESERVED") is True
    assert control_disagreement("EXTRACTION_FAILURE", "VERIFIED_PRESERVED") is True


def test_v5_mutation_source_has_no_tautological_control_assignment() -> None:
    source = (ROOT / "experiments" / "v5" / "destination_mutation_testing.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            text = ast.unparse(node)
            assert "control_classification = baseline_classification" not in text
            assert "false_positive = False" not in text


def test_v6_reports_have_complete_denominators() -> None:
    control_path = ROOT / "experiments" / "v6" / "V6_CONTROL_RERUN.json"
    mutation_path = ROOT / "experiments" / "v6" / "V6_MUTATION_SENSITIVITY.json"
    if not control_path.exists() or not mutation_path.exists():
        return
    control = json.loads(control_path.read_text(encoding="utf-8"))
    mutation = json.loads(mutation_path.read_text(encoding="utf-8"))
    assert control["controls_evaluated"] == 65
    assert mutation["attempted"] == 65


def test_v6_objection_mitigation_preserves_survivors_and_adds_evidence_alerts() -> None:
    path = ROOT / "experiments" / "v6" / "V6_OBJECTION_MITIGATIONS.json"
    if not path.exists():
        return
    mitigation = json.loads(path.read_text(encoding="utf-8"))
    ground_truth = mitigation["ground_truth_boundary"]
    survivor = mitigation["survivor_mitigation"]
    assert ground_truth["primary_adjudicated_ground_truth"] is False
    assert ground_truth["human_adjudication"] == "NOT_EXECUTED"
    assert survivor["valid_applied_mutants"] == 59
    assert survivor["coarse_classification_detections"] == 46
    assert survivor["evidence_drift_alerts"] == 59
    assert survivor["meaningful_survivors"] == 10
    assert all(packet["labels_in_packet"] is False for packet in mitigation["adjudication_packet_index"])


def main() -> None:
    tests = [
        test_control_disagreement_is_not_derived_from_expected_label,
        test_v5_mutation_source_has_no_tautological_control_assignment,
        test_v6_reports_have_complete_denominators,
        test_v6_objection_mitigation_preserves_survivors_and_adds_evidence_alerts,
    ]
    for test in tests:
        test()
    print("V6 scientific regression assertions: PASS")


if __name__ == "__main__":
    main()
