from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "v4"
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import extract  # type: ignore  # noqa: E402
from v4_source_oracle import contract_ok, parse, sha256  # type: ignore  # noqa: E402


def primary_supports(feature: str, observed: dict) -> bool:
    mapping = {
        "headings": bool(observed.get("headings")),
        "alt_text": bool(observed.get("figures")),
        "lists": bool(observed.get("lists")),
        "basic_tables": bool(observed.get("tables")),
        "document_language": bool(observed.get("document")) and bool(observed.get("language")),
        "inline_language": bool(observed.get("inline_languages")),
        "decorative_images": bool(observed.get("figures")),
        "hyperlinks": bool(observed.get("hyperlinks")),
        "document_metadata": bool(observed.get("document", {}).get("metadata")),
        "complex_tables": bool(observed.get("tables")),
        "footnotes": bool(observed.get("footnotes")),
        "equations": bool(observed.get("equations")),
        "captions": bool(observed.get("captions")),
    }
    return mapping[feature]


def main() -> None:
    manifest = json.loads((BASE / "source_manifest.json").read_text(encoding="utf-8"))
    output_dir = BASE / "source_extractions"
    output_dir.mkdir(exist_ok=True)
    rows = []
    for record in manifest["records"]:
        path = ROOT / record["fixture"]
        raw = parse(path)
        contract_pass, problems = contract_ok(raw, json.loads((ROOT / record["manifest"]).read_text(encoding="utf-8")))
        primary = extract(path)
        extraction_path = output_dir / f"{record['variant_id']}.json"
        extraction_path.write_text(json.dumps(primary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        primary_pass = primary_supports(record["feature_family"], primary)
        rows.append({"variant_id": record["variant_id"], "feature_family": record["feature_family"], "source_sha256": sha256(path), "raw_oracle": "PASS" if contract_pass else "FAIL", "raw_problems": problems, "primary_extractor": "SUPPORTED" if primary_pass else "INSUFFICIENT", "primary_extraction": str(extraction_path.relative_to(ROOT))})
    report = {"status": "PASS" if all(row["raw_oracle"] == "PASS" and row["primary_extractor"] == "SUPPORTED" for row in rows) else "FAIL", "fixture_count": len(rows), "raw_oracle_pass": sum(row["raw_oracle"] == "PASS" for row in rows), "primary_supported": sum(row["primary_extractor"] == "SUPPORTED" for row in rows), "rows": rows}
    (BASE / "SOURCE_VALIDATION.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["status", "fixture_count", "raw_oracle_pass", "primary_supported"]}, indent=2))


if __name__ == "__main__":
    main()
