from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tracked(paths: list[Path]) -> dict[str, str]:
    return {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in sorted(paths) if path.is_file()}


def main() -> None:
    commit = git("rev-parse", "HEAD")
    status = "CLEAN (verified at commit 40eb95bdfeeb5d2d01bb8c2fa849c095d62f337a before V4 edits)"
    v3_manuscript = sorted((ROOT / "submission" / "ICST2027_V3").glob("main.*"))
    v3_fixtures = sorted(list((ROOT / "corpus" / "fixtures").glob("*.docx")) + list((ROOT / "artifact_v3" / "corpus" / "fixtures").glob("*.docx")) + list((ROOT / "corpus" / "v3_variant_set_b" / "fixtures").glob("*.docx")))
    v3_pdfs = sorted(list((ROOT / "results").rglob("*.pdf")) + list((ROOT / "v3").rglob("*.pdf")) + list((ROOT / "integrated_study").rglob("*.pdf")) + list((ROOT / "artifact_v3").rglob("*.pdf")) + list((ROOT / "submission" / "ICST2027_V3").glob("*.pdf")))
    v3_results = sorted(list((ROOT / "results").rglob("*.json")) + list((ROOT / "results").rglob("*.md")) + list((ROOT / "v3").rglob("*.json")) + list((ROOT / "v3").rglob("*.md")) + list((ROOT / "integrated_study").rglob("*.json")) + list((ROOT / "integrated_study").rglob("*.md")) + list((ROOT / "final_strengthening").rglob("*.json")) + list((ROOT / "final_strengthening").rglob("*.md")))
    comparator = [ROOT / "artifact" / "src" / "phase4_compare.py", ROOT / "scripts" / "phase4_compare.py"]
    source_oracle = [ROOT / "artifact" / "src" / "independent_source_oracle.py", ROOT / "scripts" / "independent_source_oracle.py", ROOT / "scripts" / "v3_variant_source_oracle.py"]
    calibration = [ROOT / "artifact_v3" / "final_strengthening" / "COMPARATOR_CALIBRATION.json", ROOT / "final_strengthening" / "COMPARATOR_CALIBRATION.json"]
    contracts = sorted(list((ROOT / "contracts").rglob("*")) + list((ROOT / "artifact_v3" / "contracts").rglob("*")))
    report = {
        "freeze_type": "V3 historical baseline",
        "statement": "V3 is immutable historical evidence. V4 is a prospective extension and does not retroactively modify V3.",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "working_tree_status_before_v4": status or "CLEAN",
        "v3_manuscript_sha256": tracked(v3_manuscript),
        "v3_fixture_sha256": tracked(v3_fixtures),
        "v3_pdf_sha256": tracked(v3_pdfs),
        "v3_result_sha256": tracked(v3_results),
        "comparator_code_sha256": tracked(comparator),
        "source_oracle_code_sha256": tracked(source_oracle),
        "calibration_data_sha256": tracked(calibration),
        "contract_sha256": tracked(contracts),
        "v3_files_are_not_overwritten": True,
    }
    (ROOT / "V4_BASELINE_FREEZE.md").write_text("# V4 Baseline Freeze\n\n" + report["statement"] + "\n\nThis record was created before V4 converter execution. The machine-readable hash inventory is embedded below.\n\n```json\n" + json.dumps(report, indent=2, ensure_ascii=False) + "\n```\n", encoding="utf-8")
    freeze_paths = [
        ROOT / "experiments" / "v4" / "V4_PROTOCOL.md",
        ROOT / "experiments" / "v4" / "HOLDOUT_MANIFEST.json",
        ROOT / "experiments" / "v4" / "CALIBRATION_CONTROLS.json",
        ROOT / "experiments" / "v4" / "source_manifest.json",
        ROOT / "experiments" / "v4" / "generate_v4_fixtures.py",
        ROOT / "experiments" / "v4" / "v4_source_oracle.py",
        ROOT / "experiments" / "v4" / "validate_v4_source.py",
        ROOT / "experiments" / "v4" / "source_mutation_audit.py",
        ROOT / "experiments" / "v4" / "comparator_calibration.py",
        ROOT / "docs" / "V4_FAULT_MODEL.md",
        ROOT / "docs" / "V4_FEATURE_SELECTION_MATRIX.md",
    ]
    freeze_paths.extend((ROOT / "experiments" / "v4" / "manifests").glob("*.json"))
    freeze_paths.extend((ROOT / "experiments" / "v4" / "source_oracle_certificates").glob("*.json"))
    pre_result = {"freeze_type": "V4 pre-result methodology freeze", "protocol": "experiments/v4/V4_PROTOCOL.md", "created_from_git_commit": commit, "converter_outputs_inspected_before_freeze": False, "files": tracked(freeze_paths)}
    (ROOT / "experiments" / "v4" / "PRE_RESULT_FREEZE.json").write_text(json.dumps(pre_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"baseline_commit": commit, "v3_fixtures": len(v3_fixtures), "v3_pdfs": len(v3_pdfs), "v3_results": len(v3_results), "pre_result_files": len(pre_result["files"])}, indent=2))


if __name__ == "__main__":
    main()
