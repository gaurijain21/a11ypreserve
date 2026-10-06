"""V4 comparator boundary around the historical observation comparator.

The V4 boundary preserves the existing feature-specific evidence logic but
forces an abstention when a calibration control is explicitly marked as an
ambiguous representation. This is a diagnostic calibration hook, not a claim
that every real PDF ambiguity can be detected automatically.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact" / "src"))
from phase4_compare import compare_feature  # type: ignore  # noqa: E402


def compare_feature_v4(source: dict, destination: dict, feature: str, *, explicit_ambiguity: bool = False) -> dict:
    result = compare_feature(source, destination, feature)
    if explicit_ambiguity:
        result = dict(result)
        result["fidelity_classification"] = "NOT_REPRESENTABLE"
        result["destination_accessibility"] = "UNKNOWN"
        result["confidence"] = "ABSTAIN"
        result["notes"] = (result.get("notes", "") + "; V4 calibration ambiguity rule: abstain").strip("; ")
    return result
