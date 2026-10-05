from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
V4 = ROOT / "experiments" / "v4"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().lower()


def verify_manifest(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    passed = 0
    for row in manifest["records"]:
        source, output = ROOT / row["source_path"], ROOT / row["output_path"]
        data = output.read_bytes()
        doc = fitz.open(output)
        checks = [source.exists(), sha(source) == row["source_sha256"].lower(), output.exists(), len(data) > 0, data.startswith(b"%PDF"), len(doc) > 0, b"/StructTreeRoot" in data]
        if not all(checks):
            raise SystemExit(f"verification failed: {row['fixture_id']} {row['output_path']}")
        passed += 1
    return {"records": passed, "manifest": str(path.relative_to(ROOT)).replace("\\", "/")}


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify and reproduce the committed V4 evidence without cloud authentication.")
    parser.add_argument("--existing-outputs", action="store_true", help="verify committed outputs and frozen analyses")
    parser.add_argument("--google-existing", action="store_true", help="verify the committed Google Docs arm")
    parser.add_argument("--source-only", action="store_true", help="verify frozen source-manifest hashes")
    parser.add_argument("--calibration", action="store_true", help="read the committed calibration result")
    parser.add_argument("--full-analysis", action="store_true", help="report the committed analysis summaries without cloud conversion")
    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.error("choose a verification mode")
    result = {}
    source = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    if args.source_only or args.existing_outputs or args.google_existing or args.full_analysis:
        result["source_fixtures"] = len(source["records"])
        for entry in source["records"]:
            p = ROOT / entry["fixture"]
            if sha(p) != entry["source_sha256"].lower():
                raise SystemExit(f"source hash mismatch: {entry['variant_id']}")
    if args.existing_outputs or args.google_existing or args.full_analysis:
        result["libreoffice"] = verify_manifest(V4 / "conversions" / "libreoffice" / "manifest.json")
        result["google_docs"] = verify_manifest(V4 / "conversions" / "google" / "manifest.json")
    if args.calibration or args.existing_outputs or args.full_analysis:
        result["calibration"] = json.loads((V4 / "COMPARATOR_CALIBRATION.json").read_text(encoding="utf-8"))["counts"]
    if args.full_analysis or args.existing_outputs:
        lo = json.loads((V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
        go = json.loads((V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json").read_text(encoding="utf-8"))
        result["analyses"] = {"libreoffice_atomic": lo["summary"], "google_atomic": go["summary"], "lo_holdout": lo["holdout"], "google_holdout": go["holdout"]}
        result["cross_pipeline"] = json.loads((V4 / "conversions" / "CROSS_PIPELINE_COMPARISON.json").read_text(encoding="utf-8"))["atomic"]
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
