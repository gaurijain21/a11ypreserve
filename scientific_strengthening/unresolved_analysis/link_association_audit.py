"""Additive, deterministic audit for the frozen unresolved hyperlink rows.

This does not edit the frozen results.  It uses PyMuPDF page geometry as an
independent check: every expected target must have one PDF link annotation and
the annotation rectangle must cover the expected visible link words in order.
The audit intentionally requires the linked span itself to match the source
contract; surrounding prose is not counted as part of the link.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf  # PyMuPDF


ROOT = Path(__file__).resolve().parents[2]

CASES = [
    {
        "fixture": "F08_LINKS",
        "pipeline": "LibreOffice",
        "pdf": ROOT / "artifact_v3/corpus/outputs/libreoffice/F08_LINKS__LIBREOFFICE.pdf",
        "links": [("Accessibility Guidelines", "https://www.w3.org/WAI/standards-guidelines/wcag/")],
    },
    {
        "fixture": "F08_LINKS",
        "pipeline": "Google Docs",
        "pdf": ROOT / "artifact_v3/corpus/outputs/google_docs/F08_LINKS__GOOGLE_DOCS.pdf",
        "links": [("Accessibility Guidelines", "https://www.w3.org/WAI/standards-guidelines/wcag/")],
    },
    {
        "fixture": "B08",
        "pipeline": "LibreOffice",
        "pdf": ROOT / "artifact_v3/v3/variant_set_b/libreoffice/outputs/B08__LIBREOFFICE.pdf",
        "links": [
            ("the WCAG standard", "https://www.w3.org/TR/WCAG22/"),
            ("the PDF reference", "https://pdfa.org/"),
        ],
    },
    {
        "fixture": "B08",
        "pipeline": "Google Docs",
        "pdf": ROOT / "artifact_v3/v3/variant_set_b/google/outputs/B08__GOOGLE_DOCS.pdf",
        "links": [
            ("the WCAG standard", "https://www.w3.org/TR/WCAG22/"),
            ("the PDF reference", "https://pdfa.org/"),
        ],
    },
]


def norm(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower())


def words_in_rect(page: pymupdf.Page, rect: pymupdf.Rect) -> list[str]:
    words = []
    for word in page.get_text("words"):
        wrect = pymupdf.Rect(word[:4])
        # A linked word should be substantially covered by the annotation.
        if wrect.get_area() and pymupdf.Rect(rect).intersect(wrect).get_area() / wrect.get_area() >= 0.80:
            words.append((word[1], word[0], word[4]))
    words.sort(key=lambda item: (round(item[0], 2), round(item[1], 2)))
    return [text for _, _, text in words]


def audit(case: dict) -> dict:
    document = pymupdf.open(case["pdf"])
    annotations = []
    for page_no, page in enumerate(document, start=1):
        for link in page.get_links():
            if link.get("uri"):
                annotations.append(
                    {
                        "page": page_no,
                        "target": link["uri"],
                        "words": words_in_rect(page, link["from"]),
                        "rect": [round(float(v), 3) for v in link["from"]],
                    }
                )

    checks = []
    for expected_text, expected_target in case["links"]:
        candidates = [a for a in annotations if a["target"] == expected_target]
        expected_words = norm(expected_text)
        observed = []
        for candidate in candidates:
            observed_words = norm(" ".join(candidate["words"]))
            # B08's source contract includes the leading article in the prose
            # phrase, while the actual OOXML hyperlink span starts at WCAG/PDF.
            # Do not silently accept this as exact equivalence.
            exact = observed_words == expected_words
            observed.append({**candidate, "expected_words": expected_words, "exact_span": exact})
        checks.append(
            {
                "expected_text": expected_text,
                "expected_target": expected_target,
                "candidate_count": len(candidates),
                "candidates": observed,
                "exact_span_match": any(item["exact_span"] for item in observed),
            }
        )

    return {
        "fixture": case["fixture"],
        "pipeline": case["pipeline"],
        "pdf": str(case["pdf"].relative_to(ROOT)).replace("\\", "/"),
        "annotation_count": len(annotations),
        "checks": checks,
        "strict_additive_resolution": all(item["exact_span_match"] for item in checks),
    }


if __name__ == "__main__":
    print(json.dumps([audit(case) for case in CASES], indent=2))
