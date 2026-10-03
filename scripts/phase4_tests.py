from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import docx_extract  # noqa: E402
from phase4_compare import ACCESSIBILITY, FIDELITY, classify_observation, compare_feature  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    frozen = json.loads((ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
    assert frozen["frozen"] is True and frozen["fixture_count"] == 13
    old = json.loads((ROOT / "pilot" / "manifests" / "hashes.json").read_text(encoding="utf-8"))
    for fixture_id, record in old.items():
        assert sha256(ROOT / "pilot" / "fixtures" / f"{fixture_id}.docx") == record["source_docx"]
    source_rows = {row["fixture_id"]: row for row in frozen["fixtures"]}
    for fixture_id in ("F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE", "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE", "F11_FOOTNOTES", "F12_EQUATION", "F14_CAPTIONS"):
        row = source_rows[fixture_id]
        assert row["verification_status"] == "PASS"
        assert sha256(Path(row["path"])) == row["sha256"]
        source = docx_extract(Path(row["path"]))
        assert source["format"] == "docx" and source["extraction"]["independent_raw_package"] is True
    cases = {
        "EXACT_PRESERVATION": classify_observation("x", "x", exact=True),
        "SEMANTICALLY_EQUIVALENT": classify_observation("x", {"equivalent": True}, equivalent=True),
        "PARTIAL_PRESERVATION": classify_observation("x", "partial", partial=True),
        "MUTATED": classify_observation("x", "changed", mutated=True),
        "REGENERATED": classify_observation("x", "generated", regenerated=True),
        "LOST": classify_observation("x", None),
        "NOT_REPRESENTABLE": classify_observation("x", None, representable=False),
        "MEASUREMENT_ERROR": classify_observation("x", "?", measured=False),
        "INVALID_CONVERSION": classify_observation("x", None, valid_conversion=False),
    }
    assert set(cases) == FIDELITY - {"NOT_APPLICABLE"}
    assert all(row["fidelity_classification"] in FIDELITY for row in cases.values())
    assert all(row["destination_accessibility"] in ACCESSIBILITY for row in cases.values())

    source = docx_extract(ROOT / "corpus" / "fixtures" / "F06_INLINE_LANGUAGE.docx")
    destination = {"format": "pdf", "document": {"language": "en-US"}, "language": "en-US", "inline_languages": [], "tagged": True}
    row = compare_feature(source, destination, "inline_language")
    assert row["fidelity_classification"] == "PARTIAL_PRESERVATION"
    assert row["destination_accessibility"] == "DEGRADED_ACCESSIBILITY"
    report = {"passed": True, "fixture_count": frozen["fixture_count"], "taxonomy_cases": len(cases), "inline_language_case": row["fidelity_classification"], "existing_pilot_tests": "run separately by scripts/test_pilot.py, scripts/pilot2_tests.py, scripts/pilot3_tests.py"}
    (ROOT / "results").mkdir(parents=True, exist_ok=True)
    (ROOT / "results" / "phase4_test_results.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
