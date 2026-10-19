"""Regression assertions for the additive A11yPreserve V5 evidence layer."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str):
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    holdout = load("reports/V5_HOLDOUT_ACCOUNTING_AUDIT.json")
    assert holdout["status"] == "PASS"
    assert holdout["primary_cases"] == 130
    assert holdout["arithmetic"]["holdout"] == 52
    assert holdout["arithmetic"]["non_holdout"] == 78

    calibration = load("experiments/v5/calibration_ground_truth_audit.json")
    assert calibration["status"] == "COMPLETE"
    assert calibration["counts"] == {
        "correct": 60,
        "false_positives": 0,
        "false_negatives": 5,
        "correct_abstentions": 13,
    }

    mutation = load("experiments/v5/destination_mutation_manifest.json")
    assert mutation["status"] == "COMPLETE"
    assert mutation["valid_mutants"] == mutation["detected_mutants"] == 12
    assert mutation["surviving_mutants"] == 0
    assert mutation["measurement_errors"] == 0
    assert mutation["controls_evaluated"] == 13
    assert mutation["false_positive_controls"] == 0

    oracle = load("experiments/v5/independent_oracle_validation.json")
    assert oracle["status"] == "COMPLETE"
    assert oracle["sample_size"] == 26
    assert oracle["agreement"] + oracle["disagreement"] == oracle["sample_size"]

    manuscript_root = ROOT / "submission" / "ICST2027_V5"
    manuscript_paths = [manuscript_root / "main.tex", manuscript_root / "v5_hardening.tex"]
    manuscript_paths.extend(sorted((manuscript_root / "sections").glob("*.tex")))
    manuscript = "\n".join(path.read_text(encoding="utf-8") for path in manuscript_paths if path.exists())
    assert "104 non-holdout" not in manuscript
    assert "38 & 11 & 16" in manuscript
    assert "11 & 32 & 26" in manuscript

    print("V5 hardening regression assertions: PASS")


if __name__ == "__main__":
    main()
