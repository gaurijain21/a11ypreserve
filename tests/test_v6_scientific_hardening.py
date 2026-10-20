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


def main() -> None:
    tests = [
        test_control_disagreement_is_not_derived_from_expected_label,
        test_v5_mutation_source_has_no_tautological_control_assignment,
        test_v6_reports_have_complete_denominators,
    ]
    for test in tests:
        test()
    print("V6 scientific regression assertions: PASS")


if __name__ == "__main__":
    main()
