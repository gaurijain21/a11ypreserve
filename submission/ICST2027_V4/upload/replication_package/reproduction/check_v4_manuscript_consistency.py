"""Machine-check the V4 manuscript against frozen V4 evidence."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "submission" / "ICST2027_V4" / "main.tex"
V4 = ROOT / "experiments" / "v4"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for section in sorted((MANUSCRIPT.parent / "sections").glob("*.tex")):
        text += "\n" + section.read_text(encoding="utf-8")
    require(text, "13 accessibility feature families", "feature-family count")
    require(text, "five controlled variants per family", "variant count")
    require(text, "65 atomic DOCX fixtures", "fixture count")
    require(text, "130 fixture--pipeline cases", "atomic case count")
    require(text, "195 archived atomic fixture--pipeline outcomes", "complete atomic archive count")
    require(text, "supplementary third pipeline", "Word supplementary role")
    require(text, "Word (S)", "Word supplementary table label")
    require(text, "26-case holdout", "holdout count")
    require(text, "78 calibration controls", "calibration count")
    require(text, "10 project-created realistic documents", "realistic-document count")
    require(text, "39/39 mutations", "mutation count")
    require(text, "20 PDFs", "realistic PDF count")
    require(text, "stable 6/6", "repeatability classification")
    if "normalized semantic evidence was stable 6/6" not in text and "normalized semantic evidence and classifications remained stable 6/6" not in text and "normalized semantic stability 6/6" not in text:
        raise AssertionError("missing repeatability semantic evidence")
    require(text, "14 preserved, 5 partial, 4 altered, 1 lost, 2 measurement errors", "LibreOffice holdout counts")
    require(text, "4 preserved, 13 partial, 5 altered, 2 lost, 2 unresolved", "Google holdout counts")
    require(text, "60 correct decisions, zero false positives, five conservative false negatives, 13 correct abstentions", "calibration counts")
    require(text, "detected all 39", "source-oracle result")
    require(text, "78 source property contracts per pipeline", "realistic contract count")
    require(text, "156 property--pipeline observations", "realistic observation count")
    require(text, "byte identity 0/6", "LibreOffice byte repeatability")
    require(text, "byte identity 6/6", "Google byte repeatability")
    require(text, "byte-identical for 0/6", "Word byte repeatability")
    for stale in ("52 atomic", "39 Google conversions", "13 atomic DOCX fixtures", "Word produced no accepted PDF", "Word is excluded", "Word export unavailable", "only two converters completed conversion"):
        if stale in text:
            raise AssertionError(f"stale prior-version phrase remains: {stale}")

    lo = json.loads((V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
    go = json.loads((V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json").read_text(encoding="utf-8"))
    word = json.loads((V4 / "conversions" / "word" / "analysis" / "V4_WORD_ANALYSIS.json").read_text(encoding="utf-8"))
    expected_lo = {"VERIFIED_PRESERVED": 38, "OBSERVED_PARTIAL": 11, "ALTERED": 9, "CONFIRMED_LOST": 1, "UNRESOLVED_EQUIVALENCE": 1, "MEASUREMENT_ERROR": 5}
    expected_go = {"VERIFIED_PRESERVED": 11, "OBSERVED_PARTIAL": 32, "ALTERED": 11, "CONFIRMED_LOST": 6, "UNRESOLVED_EQUIVALENCE": 5, "MEASUREMENT_ERROR": 0}
    lo_counts = {key: lo["summary"]["counts"].get(key, 0) for key in expected_lo}
    go_counts = {key: go["summary"]["counts"].get(key, 0) for key in expected_go}
    if lo_counts != expected_lo:
        raise AssertionError(f"LibreOffice counts mismatch: {lo_counts}")
    if go_counts != expected_go:
        raise AssertionError(f"Google counts mismatch: {go_counts}")
    expected_word = {"VERIFIED_PRESERVED": 16, "OBSERVED_PARTIAL": 26, "ALTERED": 16, "CONFIRMED_LOST": 2, "UNRESOLVED_EQUIVALENCE": 0, "MEASUREMENT_ERROR": 5}
    word_counts = {key: word["summary"]["counts"].get(key, 0) for key in expected_word}
    if word_counts != expected_word:
        raise AssertionError(f"Word counts mismatch: {word_counts}")
    if sum(expected_word.values()) != 65:
        raise AssertionError("Word supplementary total does not equal 65")
    for left, right in ((38, 11), (11, 32), (9, 11), (1, 6), (1, 5), (5, 0)):
        if f"& {left} & {right}" not in text:
            raise AssertionError(f"missing matrix count pair {left}/{right}")
    if len(re.findall(r"Headings & V/V/V/V/V", text)) != 1:
        raise AssertionError("feature matrix missing or duplicated")
    if sum(expected_lo.values()) != 65 or sum(expected_go.values()) != 65:
        raise AssertionError("canonical pipeline totals do not equal 65")
    word_rows = {
        "headings": "P/P/P/P/P",
        "alt_text": "A/A/A/A/A",
        "lists": "V/P/V/P/P",
        "basic_tables": "P/P/P/P/P",
        "document_language": "A/A/A/A/A",
        "inline_language": "A/A/A/A/A",
        "decorative_images": "P/A/P/P/P",
        "hyperlinks": "P/P/P/P/L",
        "document_metadata": "V/V/V/V/V",
        "complex_tables": "P/P/P/P/P",
        "footnotes": "M/M/M/M/M",
        "equations": "V/V/V/V/V",
        "captions": "V/V/L/V/V",
    }
    for family, sequence in word_rows.items():
        display = {"alt_text": "Alternative text", "basic_tables": "Basic tables", "document_language": "Document language", "inline_language": "Inline language", "decorative_images": "Decorative images", "document_metadata": "Document metadata", "complex_tables": "Complex tables"}.get(family, family.title())
        if f"{display} &" not in text or f"& {sequence}" not in text:
            raise AssertionError(f"Word feature matrix missing {family}: {sequence}")
    print(json.dumps({"status": "PASS", "lo": expected_lo, "google": expected_go, "word_supplementary": expected_word, "primary_total": 130, "archived_atomic_total": 195, "manuscript": str(MANUSCRIPT.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
