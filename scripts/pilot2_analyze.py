from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_compare import compare  # noqa: E402
from pilot_semantics import extract_pdf  # noqa: E402

from pypdf import PdfReader


PILOT2 = ROOT / "pilot2"
FIXTURE_IDS = ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE")
CONVERTERS = {
    "Microsoft Word": {"key": "word", "dir": PILOT2 / "outputs" / "word_pdf"},
    "LibreOffice": {"key": "libreoffice", "dir": PILOT2 / "outputs" / "libreoffice_pdf"},
}
FEATURES = {
    "F01_HEADINGS": ("headings", "heading_hierarchy"),
    "F02_ALT_TEXT": ("figures", "image_alt_text"),
    "F03_LISTS": ("lists", "list_structure"),
    "F04_TABLE": ("tables", "table_structure"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_dirs() -> None:
    for spec in CONVERTERS.values():
        spec["dir"].mkdir(parents=True, exist_ok=True)
        (PILOT2 / "destination_semantics" / spec["key"]).mkdir(parents=True, exist_ok=True)
    (PILOT2 / "evidence").mkdir(parents=True, exist_ok=True)
    (PILOT2 / "reports").mkdir(parents=True, exist_ok=True)


def validate_pdf(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "status": "INVALID_CONVERSION", "reason": "expected output file does not exist", "path": str(path)}
    result: dict[str, Any] = {"exists": True, "path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)}
    if result["size_bytes"] == 0:
        result.update({"status": "INVALID_CONVERSION", "reason": "zero-byte output"})
        return result
    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        root = reader.trailer.get("/Root")
        root = root.get_object() if hasattr(root, "get_object") else root
        struct = root.get("/StructTreeRoot") if hasattr(root, "get") else None
        result.update({"status": "PASS", "parseable": True, "page_count": len(reader.pages), "page_count_minimum": 1, "content_text_nonempty": bool(text.strip()), "struct_tree_exists": struct is not None, "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()}})
    except Exception as exc:
        result.update({"status": "INVALID_CONVERSION", "parseable": False, "reason": repr(exc)})
    return result


def source_value(source: dict[str, Any], key: str) -> Any:
    if key == "figures":
        return [{k: item.get(k) for k in ("identifier", "alt", "decorative", "order")} for item in source.get(key, [])]
    if key == "headings":
        return [{k: item.get(k) for k in ("text", "level", "order")} for item in source.get(key, [])]
    return source.get(key, [])


def family_rows(source: dict[str, Any], destination: dict[str, Any], fixture_id: str) -> list[dict[str, Any]]:
    rows = compare(source, destination)
    if fixture_id == "F01_HEADINGS":
        return [row for row in rows if row["feature"].startswith("heading[")]
    if fixture_id == "F02_ALT_TEXT":
        return [row for row in rows if row["feature"].startswith("figure_alt[")]
    if fixture_id == "F03_LISTS":
        return [row for row in rows if row["feature"].startswith("list_item[")]
    if fixture_id == "F04_TABLE":
        return [row for row in rows if row["feature"].startswith("table[")]
    return []


def aggregate(classifications: list[str]) -> str:
    if not classifications:
        return "MEASUREMENT_ERROR"
    priority = ["INVALID_CONVERSION", "LOST", "MIS_MAPPED", "DEGRADED", "AMBIGUOUS", "NOT_REPRESENTABLE", "PRESERVED"]
    for label in priority:
        if label in classifications:
            return label
    return "MEASUREMENT_ERROR"


def main() -> None:
    ensure_dirs()
    source_dir = ROOT / "pilot" / "source_semantics"
    validations: dict[str, Any] = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "outputs": {}}
    diffs: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for fixture_id in FIXTURE_IDS:
        source = json.loads((source_dir / f"{fixture_id}.json").read_text(encoding="utf-8"))
        for converter, spec in CONVERTERS.items():
            pdf = spec["dir"] / f"{fixture_id}__{'WORD' if converter == 'Microsoft Word' else 'LIBREOFFICE'}.pdf"
            validation = validate_pdf(pdf)
            validations["outputs"][f"{converter}:{fixture_id}"] = validation
            feature_key, feature_name = FEATURES[fixture_id]
            if validation.get("status") != "PASS":
                dest = None
                row = {
                    "fixture": fixture_id,
                    "converter": converter,
                    "source_feature": feature_name,
                    "destination_feature": None,
                    "source_value": source_value(source, feature_key),
                    "destination_value": None,
                    "destination_representation": None,
                    "equivalence_determination": "No analyzable destination PDF exists; this is a conversion-layer result, not a semantic loss claim.",
                    "classification": "INVALID_CONVERSION",
                    "evidence_path": str(PILOT2 / "reports" / "output_validation.json"),
                    "confidence": 1.0,
                    "notes": validation.get("reason"),
                }
                diffs.append(row)
                summary_rows.append({"fixture": fixture_id, "feature": feature_name, "word": "INVALID_CONVERSION" if converter == "Microsoft Word" else None, "libreoffice": "INVALID_CONVERSION" if converter == "LibreOffice" else None, "evidence_quality": "HIGH"})
                continue
            dest_path = PILOT2 / "destination_semantics" / spec["key"] / f"{fixture_id}.json"
            dest = extract_pdf(pdf)
            dest_path.write_text(json.dumps(dest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            family = family_rows(source, dest, fixture_id)
            for item in family:
                diffs.append({
                    "fixture": fixture_id,
                    "converter": converter,
                    "source_feature": feature_name,
                    "destination_feature": item.get("feature"),
                    "source_value": item.get("source"),
                    "destination_value": item.get("destination"),
                    "destination_representation": item.get("destination"),
                    "equivalence_determination": item.get("evidence", {}).get("reason"),
                    "classification": item.get("classification"),
                    "evidence_path": str(dest_path),
                    "confidence": 1.0,
                    "notes": "Deterministic ASIR comparison",
                })
            summary_rows.append({"fixture": fixture_id, "feature": feature_name, "word": aggregate([x["classification"] for x in family]) if converter == "Microsoft Word" else None, "libreoffice": aggregate([x["classification"] for x in family]) if converter == "LibreOffice" else None, "evidence_quality": "HIGH"})

    # Merge the two converter columns for the feature summary.
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for row in summary_rows:
        key = (row["fixture"], row["feature"])
        current = merged.setdefault(key, {"fixture": row["fixture"], "feature": row["feature"], "word": None, "libreoffice": None, "evidence_quality": row["evidence_quality"]})
        if row["word"] is not None:
            current["word"] = row["word"]
        if row["libreoffice"] is not None:
            current["libreoffice"] = row["libreoffice"]
    validations["summary"] = {"total_expected_outputs": 8, "existing_outputs": sum(1 for x in validations["outputs"].values() if x.get("exists")), "valid_parseable_outputs": sum(1 for x in validations["outputs"].values() if x.get("status") == "PASS")}
    (PILOT2 / "reports" / "output_validation.json").write_text(json.dumps(validations, indent=2) + "\n", encoding="utf-8")
    (PILOT2 / "reports" / "semantic_diff_results.json").write_text(json.dumps({"generated_at_utc": datetime.now(timezone.utc).isoformat(), "results": diffs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md = ["# Pilot 2 Results", "", "| Fixture | Feature | Word->PDF | LibreOffice->PDF | Evidence quality |", "|---|---|---|---|---|"]
    for row in merged.values():
        md.append(f"| {row['fixture']} | {row['feature']} | {row['word'] or 'NOT_RUN'} | {row['libreoffice'] or 'NOT_RUN'} | {row['evidence_quality']} |")
    md.extend(["", "`INVALID_CONVERSION` means the expected converter output was not produced or was not analyzable. It is not counted as an accessibility-preservation failure.", ""])
    (PILOT2 / "PILOT2_RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"validation": validations["summary"], "diff_count": len(diffs)}, indent=2))


if __name__ == "__main__":
    main()
