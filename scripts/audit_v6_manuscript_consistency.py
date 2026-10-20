"""Check that V6 manuscript headline claims match machine-derived evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"


def main() -> None:
    control = json.loads((V6 / "V6_CONTROL_RERUN.json").read_text(encoding="utf-8"))
    mutation = json.loads((V6 / "V6_MUTATION_SENSITIVITY.json").read_text(encoding="utf-8"))
    ablation = json.loads((V6 / "V6_BASELINE_ABLATION.json").read_text(encoding="utf-8"))
    source = "\n".join(path.read_text(encoding="utf-8") for path in [
        ROOT / "submission" / "ICST2027_V6" / "main.tex",
        ROOT / "submission" / "ICST2027_V6" / "v6_hardening.tex",
    ])
    checks = {
        "control_denominator_and_result": f"{control['classification_disagreements']}/65" in source and control["controls_evaluated"] == 65,
        "mutation_attempts_and_valid": str(mutation["attempted"]) in source and str(mutation["valid_applied_mutants"]) in source,
        "mutation_detection_and_survival": f"{mutation['classification_level_detections']}/59" in source and str(mutation["semantically_meaningful_survivals"]) in source,
        "baseline_denominator": ablation["primary_cases"] == 130 and "130" in source,
        "baseline_fault_counts": all(f"{ablation['mutation_fault_sensitivity']['summary'][key]['detected_faults']}/59" in source for key in ["tag_presence", "visible_text_equality", "destination_only_evidence", "full_a11ypreserve"]),
        "frozen_denominators": all(token in source for token in ["13 accessibility feature families", "65 atomic", "130 fixture"]),
        "scope_boundary": all(token in source for token in ["end-to-end", "general PDF checker", "No standards-validator"]),
        "anonymous_manuscript": "Anonymous for review" in source,
    }
    result = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    output = ROOT / "reports" / "v6" / "V6_MANUSCRIPT_CONSISTENCY.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
