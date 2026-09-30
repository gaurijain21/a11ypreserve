from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot3_analyze import text_contains  # noqa: E402
from pilot_compare import compare  # noqa: E402
from pilot_semantics import extract_docx, extract_pdf  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads((ROOT / "pilot" / "manifests" / "hashes.json").read_text(encoding="utf-8"))
    for fixture, record in manifest.items():
        path = ROOT / "pilot" / "fixtures" / f"{fixture}.docx"
        assert path.exists(), path
        assert sha256(path) == record["source_docx"], fixture

    validation = json.loads((ROOT / "pilot3" / "reports" / "output_validation.json").read_text(encoding="utf-8"))
    assert validation["summary"]["expected_outputs"] == 8
    assert validation["summary"]["valid_parseable_outputs"] == 8
    assert validation["summary"]["all_required_outputs_valid"] is True

    diff = json.loads((ROOT / "pilot3" / "reports" / "semantic_diff_results.json").read_text(encoding="utf-8"))
    rows = diff["results"]
    assert len(rows) == 8
    by_key = {(row["fixture"], row["converter"]): row for row in rows}
    expected = {
        ("F01_HEADINGS", "LibreOffice"): ("SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT"),
        ("F01_HEADINGS", "Google Docs"): ("PARTIAL_PRESERVATION", "ACCESSIBLE_BUT_ALTERED"),
        ("F02_ALT_TEXT", "LibreOffice"): ("MUTATED", "ACCESSIBLE_BUT_ALTERED"),
        ("F02_ALT_TEXT", "Google Docs"): ("EXACT_PRESERVATION", "ACCESSIBLE_EQUIVALENT"),
        ("F03_LISTS", "LibreOffice"): ("SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT"),
        ("F03_LISTS", "Google Docs"): ("PARTIAL_PRESERVATION", "DEGRADED_ACCESSIBILITY"),
        ("F04_TABLE", "LibreOffice"): ("SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT"),
        ("F04_TABLE", "Google Docs"): ("SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT"),
    }
    for key, (fidelity, accessibility) in expected.items():
        assert key in by_key, key
        assert by_key[key]["fidelity_classification"] == fidelity, key
        assert by_key[key]["destination_accessibility"] == accessibility, key

    assert text_contains("Prior  W ork appears in extracted text", "Prior Work")
    assert text_contains("Completion  Rate", "Completion Rate")
    assert not text_contains("Completion percentage", "Completion Rate")

    # The existing ASIR comparator remains executable against every real PDF.
    # Pilot 3's two-axis wrapper retains richer distinctions where the legacy
    # single-label taxonomy is intentionally too coarse.
    for fixture in ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE"):
        source = extract_docx(ROOT / "pilot" / "fixtures" / f"{fixture}.docx")
        for pdf in (
            ROOT / "pilot2" / "outputs" / "libreoffice_pdf" / f"{fixture}__LIBREOFFICE.pdf",
            ROOT / "pilot3" / "outputs" / "google_docs_pdf" / f"{fixture}__GOOGLE_DOCS.pdf",
        ):
            assert compare(source, extract_pdf(pdf)), f"legacy comparator returned no rows for {pdf.name}"

    print(json.dumps({"passed": True, "assertions": 8 + len(expected) * 2 + 3 + 8, "semantic_rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
