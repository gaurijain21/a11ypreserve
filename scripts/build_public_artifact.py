"""Build the sanitized, review-ready A11yPreserve artifact candidate.

This script copies only frozen research inputs, outputs, contracts, evidence,
and analysis code. It never edits the canonical corpus or result files.
"""

from __future__ import annotations

import re
import shutil
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "artifact"


def copy_file(relative: str, target: str | None = None) -> None:
    source = ROOT / relative
    if not source.exists():
        raise FileNotFoundError(source)
    destination = DEST / (target or relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(relative: str, target: str | None = None) -> None:
    source = ROOT / relative
    destination = DEST / (target or relative)
    if not source.exists():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, dirs_exist_ok=True)


def sanitize_text_files() -> None:
    root_text = str(ROOT)
    replacements = [
        (root_text, "<ARTIFACT_ROOT>"),
        (root_text.replace("\\", "/"), "<ARTIFACT_ROOT>"),
        (root_text.replace("\\", "\\\\"), "<ARTIFACT_ROOT>"),
        ("C:/Users/iamga", "<LOCAL_USER_ROOT>"),
        ("C:\\\\Users\\\\iamga", "<LOCAL_USER_ROOT>"),
        ("C:\\Users\\iamga", "<LOCAL_USER_ROOT>"),
    ]
    sensitive = re.compile(
        r"(?i)(oauth|cookie|access[_ -]?token|refresh[_ -]?token|api[_ -]?key|password|secret)"
    )
    for path in DEST.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for old, new in replacements:
            text = text.replace(old, new)
        if sensitive.search(text) and any(word in path.name.lower() for word in ("cookie", "token", "auth", "secret", "credential")):
            path.unlink()
            continue
        path.write_text(text, encoding="utf-8", newline="")


def normalize_public_manifests() -> None:
    frozen = DEST / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
    data = json.loads(frozen.read_text(encoding="utf-8"))
    for item in data.get("fixtures", []):
        name = Path(item["path"]).name
        item["path"] = "corpus/fixtures/" + name
        item["source_manifest"] = "corpus/manifests/" + Path(name).with_suffix(".json").name
    if "verification" in data and "frozen_pilot_hashes" in data["verification"]:
        data["verification"]["frozen_pilot_hashes"] = "corpus/manifests/hashes.json"
    frozen.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    build = DEST / "corpus" / "BUILD_RECORD.json"
    if build.exists():
        record = json.loads(build.read_text(encoding="utf-8"))
        for item in record.get("generated", []):
            name = Path(item["path"]).name
            item["path"] = "corpus/fixtures/" + name
            item["manifest"] = "corpus/manifests/" + Path(name).with_suffix(".json").name
        if "frozen_manifest" in record:
            record["frozen_manifest"] = "corpus/FROZEN_CORPUS_MANIFEST.json"
        build.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    # Existing artifact directories are intentionally reused; this function
    # overwrites only the curated files below and does not touch canonical data.
    for relative in [
        "results/full_experiment/lo_inputs",
        "results/full_experiment/outputs",
        "results/full_experiment/evidence",
        "evidence/source",
        "corpus/manifests",
        "pilot/manifests",
        "contracts",
        "integrated_study/outputs",
        "integrated_study/sources",
        "final_strengthening/loss",
    ]:
        target = relative
        if relative == "results/full_experiment/lo_inputs":
            target = "corpus/fixtures"
        elif relative == "results/full_experiment/outputs":
            target = "corpus/outputs"
        elif relative == "results/full_experiment/evidence":
            target = "corpus/evidence/full_experiment"
        elif relative == "evidence/source":
            target = "corpus/evidence/source"
        elif relative == "corpus/manifests":
            target = "corpus/manifests"
        elif relative == "pilot/manifests":
            target = "corpus/manifests"
        elif relative == "final_strengthening/loss":
            target = "corpus/evidence/loss"
        elif relative == "integrated_study/outputs":
            target = "integrated_study/outputs"
        elif relative == "integrated_study/sources":
            target = "integrated_study/sources"
        copy_tree(relative, target)

    # The internal V3 classification audit is not part of the frozen V2
    # submission artifact.  Remove only its generated public copy; the
    # canonical internal contracts remain untouched.
    public_v3_contracts = DEST / "contracts" / "v3"
    if public_v3_contracts.exists():
        for child in public_v3_contracts.iterdir():
            if child.is_file():
                child.unlink()

    for relative in [
        "corpus/FROZEN_CORPUS_MANIFEST.json",
        "corpus/BUILD_RECORD.json",
        "results/FINAL_EVIDENCE_AWARE_RESULTS.md",
        "results/RESULT_INTERPRETATION_CHANGELOG.md",
        "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json",
        "integrated_study/INTEGRATED_CONTRACTS.json",
        "integrated_study/INTEGRATED_RESULTS.json",
        "integrated_study/INTEGRATED_RESULTS.md",
        "integrated_study/INTEGRATED_SOURCE_ORACLE.json",
        "integrated_study/INTEGRATED_SOURCE_ORACLE.md",
        "integrated_study/LIBREOFFICE_RESULTS.json",
        "integrated_study/PARSER_TRIANGULATION.json",
        "integrated_study/PARSER_TRIANGULATION.md",
        "docs/CONFORMANCE_SUITE.md",
        "final_strengthening/PARTIAL_CASE_REAUDIT.md",
        "final_strengthening/PDF_PARSER_TRIANGULATION.md",
        "final_strengthening/INDEPENDENT_SOURCE_ORACLE.md",
        "final_strengthening/COMPARATOR_CALIBRATION.md",
        "final_strengthening/COMPARATOR_CALIBRATION.json",
        "results/full_experiment/EVIDENCE_STATUS_FREEZE_V2.json",
    ]:
        copy_file(relative)

    source_scripts = [
        "a11ydiff.py",
        "extract_semantics.py",
        "phase4_compare.py",
        "independent_source_oracle.py",
        "pdf_parser_triangulation.py",
        "comparator_calibration.py",
        "verify_corpus_ooxml.py",
        "validate_full_outputs.py",
    ]
    for name in source_scripts:
        copy_file("scripts/" + name, "src/" + name)

    test_scripts = [
        "phase4_tests.py",
        "phase6_comparator_tests.py",
        "full_experiment_tests.py",
    ]
    for name in test_scripts:
        copy_file("scripts/" + name, "tests/" + name)

    normalize_public_manifests()
    sanitize_text_files()


if __name__ == "__main__":
    main()
