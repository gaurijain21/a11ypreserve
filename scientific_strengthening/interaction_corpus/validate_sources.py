"""Validate the additive interaction-corpus source contracts deterministically."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("extract_semantics", ROOT / "scripts" / "extract_semantics.py")
extract_semantics = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(extract_semantics)


def check(record: dict, extracted: dict, contract: dict) -> None:
    feature = contract["feature"]
    expected = contract["expected"]
    if feature == "headings":
        actual = [item["level"] for item in extracted["headings"]]
        assert actual == expected["levels"], (record["document_id"], feature, actual, expected)
    elif feature == "lists":
        actual = [item["depth"] for item in extracted["lists"]]
        assert actual == expected["depths"], (record["document_id"], feature, actual, expected)
        if "top_level_type" in expected:
            top_level = [item["type"] for item in extracted["lists"] if item["depth"] == 0]
            assert top_level and all(item == expected["top_level_type"] for item in top_level), (record["document_id"], feature, top_level, expected)
    elif feature == "hyperlinks":
        actual = extracted["hyperlinks"]
        assert any(item.get("text") == expected["text"] and item.get("target") == expected["target"] for item in actual), (record["document_id"], feature, actual, expected)
    elif feature == "inline_language":
        assert any(item.get("text") == expected["text"] and item.get("language") == expected["language"] for item in extracted["inline_languages"]), (record["document_id"], feature, extracted["inline_languages"], expected)
    elif feature == "document_language":
        assert extracted["document"]["language"] == expected["language"], (record["document_id"], feature, extracted["document"], expected)
    elif feature == "image_alt_text":
        assert any(item.get("alt") == expected["alt"] and not item.get("decorative") for item in extracted["figures"]), (record["document_id"], feature, extracted["figures"], expected)
    elif feature == "captions":
        assert any(item.get("text") == expected["text"] for item in extracted["captions"]), (record["document_id"], feature, extracted["captions"], expected)
    elif feature == "table":
        table = next((item for item in extracted["tables"] if item.get("headers") == expected["headers"]), None)
        assert table is not None and table["dimensions"]["rows"] == expected["rows"], (record["document_id"], feature, extracted["tables"], expected)
    elif feature == "footnotes":
        assert any(item.get("text") == expected["text"] for item in extracted["footnotes"]), (record["document_id"], feature, extracted["footnotes"], expected)
    else:
        raise AssertionError(f"unsupported contract feature: {feature}")


def main() -> None:
    manifest = json.loads((ROOT / "scientific_strengthening/interaction_corpus/INTERACTION_CONTRACTS.json").read_text(encoding="utf-8"))
    checked = 0
    for record in manifest["documents"]:
        extracted = extract_semantics.extract(ROOT / record["source_docx"])
        for contract in record["contracts"]:
            check(record, extracted, contract)
            checked += 1
    print(json.dumps({"documents_checked": len(manifest["documents"]), "contracts_checked": checked, "result": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
