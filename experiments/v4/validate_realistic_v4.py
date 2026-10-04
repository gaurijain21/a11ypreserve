from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "experiments" / "v4" / "realistic"
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import extract  # type: ignore  # noqa: E402
sys.path.insert(0, str(ROOT / "experiments" / "v4"))
from v4_source_oracle import parse, sha256  # type: ignore  # noqa: E402


def main() -> None:
    manifest = json.loads((BASE / "REALISTIC_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
    rows = []
    for record in manifest["records"]:
        path = ROOT / record["path"]
        raw = parse(path)
        primary = extract(path)
        expected = {contract["property"]: contract for contract in record["contracts"]}
        checks = {
            "headings": len(raw["headings"]) == expected["headings"]["expected_count"],
            "inline_language": any(item["language"] == expected["inline_language"]["expected_language"] for item in raw["inline_languages"]),
            "hyperlinks": any(item["target"] == expected["hyperlinks"]["expected_target"] for item in raw["hyperlinks"]),
            "basic_tables": bool(raw["tables"] and raw["tables"][0]["header_rows"] == expected["basic_tables"]["header_rows"]),
            "alternative_text": any(item["alt"] == expected["alternative_text"]["expected_alt"] for item in raw["figures"]),
            "captions": any(item["text"] == expected["captions"]["expected_text"] for item in raw["captions"]),
            "document_title": raw["metadata"]["title"] == expected["document_title"]["expected_title"],
        }
        if "footnotes" in expected:
            checks["footnotes"] = len(raw["footnotes"]) == expected["footnotes"]["expected_count"]
        if "equations" in expected:
            checks["equations"] = len(raw["equations"]) == expected["equations"]["expected_count"]
        rows.append({"document_id": record["document_id"], "source_sha256": sha256(path), "contract_checks": checks, "primary_extractor_nonempty": {"headings": bool(primary.get("headings")), "figures": bool(primary.get("figures")), "tables": bool(primary.get("tables")), "hyperlinks": bool(primary.get("hyperlinks")), "captions": bool(primary.get("captions"))}})
    report = {"status": "PASS" if all(all(row["contract_checks"].values()) for row in rows) else "FAIL", "documents": len(rows), "property_observations": sum(len(row["contract_checks"]) for row in rows), "rows": rows, "scoring": "contract-level only; no global accessibility score"}
    (BASE / "REALISTIC_SOURCE_VALIDATION.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["status", "documents", "property_observations"]}, indent=2))


if __name__ == "__main__":
    main()
