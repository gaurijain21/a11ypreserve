from __future__ import annotations

import hashlib
import json
import platform
import re
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import pypdf
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
V6 = ROOT / "experiments" / "v6"

FEATURES = {
    "headings": "headings",
    "alt_text": "image_alt_text",
    "lists": "lists",
    "basic_tables": "table",
    "document_language": "document_language",
    "inline_language": "inline_language",
    "decorative_images": "decorative_image",
    "hyperlinks": "hyperlinks",
    "document_metadata": "document_title",
    "complex_tables": "complex_table",
    "footnotes": "footnotes",
    "equations": "equation",
    "captions": "captions",
}

DROP_SEMANTIC_KEYS = {
    "object", "source", "path", "source_path", "output_path", "pdf_sha256",
    "CreationDate", "creation_date", "started_at", "completed_at", "environment",
    "library", "method", "extraction",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tool_versions() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "pypdf": getattr(pypdf, "__version__", "unknown"),
        "pymupdf": str(pymupdf.VersionBind),
    }


def _clean(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _clean(child)
            for key, child in sorted(value.items(), key=lambda item: str(item[0]))
            if str(key) not in DROP_SEMANTIC_KEYS
        }
    if isinstance(value, (list, tuple)):
        return [_clean(child) for child in value]
    if isinstance(value, str):
        value = re.sub(r"IndirectObject\(\d+, \d+, \d+\)", "IndirectObject", value)
        value = re.sub(r"<REPOSITORY_ROOT>[\\/][^\"']+", "<REPOSITORY_ROOT>", value)
        return value
    return value


def public_evidence(value: Any) -> Any:
    """Remove checkout-specific absolute paths while retaining raw evidence."""
    if isinstance(value, Mapping):
        return {str(key): public_evidence(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [public_evidence(child) for child in value]
    if isinstance(value, str):
        root_text = str(ROOT).replace("\\", "/")
        text = value.replace("\\", "/")
        if text == root_text:
            return "<REPOSITORY_ROOT>"
        if text.startswith(root_text + "/"):
            return "<REPOSITORY_ROOT>" + text[len(root_text):]
        return value
    return value


def normalized(value: Any) -> Any:
    return _clean(value)


def normalized_hash(value: Any) -> str:
    encoded = json.dumps(normalized(value), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def semantic_evidence(raw: dict[str, Any] | None, destination: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
    secondary_projection = {
        "text_sha256": secondary.get("text_sha256"),
        "links": secondary.get("links", []),
        "page_image_counts": secondary.get("page_image_counts", []),
        "serialized_marker_counts": secondary.get("serialized_marker_counts", {}),
        "pages": secondary.get("pages"),
    }
    return normalized({
        "raw_comparison": raw or {},
        "destination": destination,
        "secondary": secondary_projection,
    })


def extracted_semantic_evidence(destination: dict[str, Any], secondary: dict[str, Any]) -> dict[str, Any]:
    return normalized({
        "destination": destination,
        "secondary": {
            "text_sha256": secondary.get("text_sha256"),
            "links": secondary.get("links", []),
            "page_image_counts": secondary.get("page_image_counts", []),
            "serialized_marker_counts": secondary.get("serialized_marker_counts", {}),
            "pages": secondary.get("pages"),
        },
    })


def run_case(source_path: Path, pdf_path: Path, family: str) -> dict[str, Any]:
    """Run the frozen V4 extraction/comparison boundary once for one PDF."""
    import sys as _sys

    _sys.path.insert(0, str(V4))
    _sys.path.insert(0, str(ROOT / "artifact" / "src"))
    from run_frozen_analysis import final_classification, secondary  # type: ignore
    from run_frozen_analysis import docx_extract, pdf_extract  # type: ignore
    from v4_comparator import compare_feature_v4  # type: ignore

    source = docx_extract(source_path)
    destination = pdf_extract(pdf_path)
    second = secondary(pdf_path)
    comparator_feature = FEATURES[family]
    raw = compare_feature_v4(source, destination, comparator_feature)
    classification, basis = final_classification(raw, comparator_feature, destination, second)
    return {
        "source": public_evidence(source),
        "destination": public_evidence(destination),
        "secondary": public_evidence(second),
        "raw": public_evidence(raw),
        "classification": classification,
        "classification_basis": public_evidence(basis),
        "semantic_evidence": semantic_evidence(raw, destination, second),
        "semantic_evidence_sha256": normalized_hash(semantic_evidence(raw, destination, second)),
        "extracted_evidence": extracted_semantic_evidence(destination, second),
        "extracted_evidence_sha256": normalized_hash(extracted_semantic_evidence(destination, second)),
    }


def control_disagreement(computed: str, frozen: str) -> bool:
    """Return whether a recomputed control disagrees with its frozen label."""
    return computed != frozen


def load_atomic_records() -> list[dict[str, Any]]:
    manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    analysis = json.loads((V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
    analysis_by_fixture = {row["fixture_id"]: row for row in analysis["records"] if row.get("corpus") == "atomic"}
    records = []
    for entry in manifest["records"]:
        fixture = entry["variant_id"]
        analysis_row = analysis_by_fixture[fixture]
        records.append({
            "fixture_id": fixture,
            "family": entry["feature_family"],
            "role": entry["role"],
            "source_path": ROOT / entry["fixture"],
            "pdf_path": ROOT / analysis_row["output_path"],
            "source_sha256": entry["source_sha256"],
            "pdf_sha256": analysis_row["output_sha256"],
            "frozen_classification": analysis_row["classification"],
            "frozen_raw_fidelity": analysis_row.get("raw_fidelity"),
        })
    return records
