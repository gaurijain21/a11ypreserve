from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_compare import synthetic_cases  # noqa: E402
from pilot_semantics import extract_docx, extract_pdf  # noqa: E402


def main() -> None:
    results = {"synthetic_comparator": synthetic_cases(), "source_extractors": {}, "pdf_extractor_smoke": None}
    for path in sorted((ROOT / "pilot" / "fixtures").glob("F*.docx")):
        asir = extract_docx(path)
        results["source_extractors"][path.stem] = {
            "headings": len(asir["headings"]),
            "figures": len(asir["figures"]),
            "lists": len(asir["lists"]),
            "tables": len(asir["tables"]),
        }
    prior_pdf = ROOT / "outputs" / "G01_chrome.pdf"
    if prior_pdf.exists():
        parsed = extract_pdf(prior_pdf)
        results["pdf_extractor_smoke"] = {"input": str(prior_pdf), "tagged": parsed.get("pdf", {}).get("tagged"), "headings": len(parsed.get("headings", [])), "figures": len(parsed.get("figures", []))}
    failed = [name for name, passed in results["synthetic_comparator"].items() if not passed]
    results["passed"] = not failed
    results["failures"] = failed
    out = ROOT / "pilot" / "reports" / "test_results.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
