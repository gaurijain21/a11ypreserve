"""Run a deliberately weak destination-presence baseline on frozen outputs.

This is additive and does not alter A11yPreserve classifications.  It asks
only whether the destination extractor exposes some feature-shaped node; it
does not compare source values, associations, order, or equivalence.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CORE_FEATURES = {
    "F01_HEADINGS": "headings",
    "F02_ALT_TEXT": "alt_text",
    "F03_LISTS": "lists",
    "F04_TABLE": "table",
    "F05_DOCUMENT_LANGUAGE": "document_language",
    "F06_INLINE_LANGUAGE": "inline_language",
    "F07_DECORATIVE_IMAGE": "decorative_image",
    "F08_LINKS": "links",
    "F09_DOCUMENT_TITLE": "document_title",
    "F10_COMPLEX_TABLE": "complex_table",
    "F11_FOOTNOTES": "footnotes",
    "F12_EQUATION": "equation",
    "F14_CAPTIONS": "captions",
}


def extraction_path(row: dict) -> Path:
    fixture = row["fixture"]
    pipeline = row["pipeline"]
    if row["study_arm"] == "Core":
        arm = "google_docs" if pipeline == "Google Docs" else "libreoffice"
        return ROOT / "artifact_v3/results/full_experiment/extracted" / arm / f"{fixture}.json"
    arm = "google" if pipeline == "Google Docs" else "libreoffice"
    return ROOT / "artifact_v3/v3/variant_set_b" / arm / "extracted" / f"{fixture}.json"


def feature_name(row: dict) -> str:
    return (row.get("feature") or row.get("feature_family") or CORE_FEATURES.get(row["fixture"], "")).lower().replace(" ", "_")


def presence(extracted: dict, feature: str) -> bool:
    if feature in {"headings", "heading_hierarchy"}:
        return bool(extracted.get("headings"))
    if feature in {"alt_text", "image_alt_text", "decorative_image"}:
        return bool(extracted.get("figures"))
    if feature in {"lists", "nested_lists"}:
        return bool(extracted.get("lists"))
    if feature in {"table", "tables", "complex_table", "table_headers"}:
        return bool(extracted.get("tables"))
    if feature == "document_language":
        return bool(extracted.get("document", {}).get("language"))
    if feature in {"inline_language", "inline_languages"}:
        return bool(extracted.get("inline_languages"))
    if feature in {"links", "hyperlinks"}:
        return bool(extracted.get("hyperlinks"))
    if feature in {"document_title", "title"}:
        return bool(extracted.get("document", {}).get("title"))
    if feature in {"footnotes", "footnote"}:
        return bool(extracted.get("footnotes"))
    if feature in {"equation", "equations"}:
        return bool(extracted.get("equations")) or bool(re.search(r"E\s*=\s*m\s*c", extracted.get("pdf_text", "")))
    if feature in {"captions", "caption"}:
        return bool(extracted.get("captions"))
    raise ValueError(f"Unsupported feature: {feature}")


def main() -> None:
    results = json.loads((ROOT / "artifact_v3/results/V3_PRIMARY_RESULTS.json").read_text(encoding="utf-8"))
    rows = []
    for row in results["records"]:
        extracted = json.loads(extraction_path(row).read_text(encoding="utf-8"))
        feature = feature_name(row)
        rows.append({
            "fixture": row["fixture"],
            "pipeline": row["pipeline"],
            "study_arm": row["study_arm"],
            "feature": feature,
            "a11ypreserve": row["final_evidence_aware_result"],
            "presence_only": "PRESENT" if presence(extracted, feature) else "ABSENT",
        })
    cross = Counter((row["presence_only"], row["a11ypreserve"]) for row in rows)
    print(json.dumps({"rows": len(rows), "cross_tab": {f"{a} / {b}": n for (a, b), n in sorted(cross.items())}}, indent=2))


if __name__ == "__main__":
    main()
