from __future__ import annotations

"""Run source extraction, PDF extraction, and a11ydiff over the frozen matrix."""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import extract  # noqa: E402

MANIFEST = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
BASE = ROOT / "results" / "full_experiment"
VALIDATION = BASE / "reports" / "output_validation.json"

FEATURES = {
    "F01_HEADINGS": "headings",
    "F02_ALT_TEXT": "image_alt_text",
    "F03_LISTS": "lists",
    "F04_TABLE": "table",
    "F05_DOCUMENT_LANGUAGE": "document_language",
    "F06_INLINE_LANGUAGE": "inline_language",
    "F07_DECORATIVE_IMAGE": "decorative_image",
    "F08_LINKS": "hyperlinks",
    "F09_DOCUMENT_TITLE": "document_title",
    "F10_COMPLEX_TABLE": "complex_table",
    "F11_FOOTNOTES": "footnotes",
    "F12_EQUATION": "equation",
    "F14_CAPTIONS": "captions",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cli(source: Path, destination: Path, feature: str) -> dict:
    command = [sys.executable, str(ROOT / "scripts" / "a11ydiff.py"), str(source), str(destination), feature]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if completed.returncode:
        return {"command": command, "returncode": completed.returncode, "stderr": completed.stderr, "error": "a11ydiff failed"}
    return {"command": command, "returncode": 0, "report": json.loads(completed.stdout)}


def empirical_label(fidelity: str) -> str:
    return {
        "EXACT_PRESERVATION": "PRESERVED",
        "SEMANTICALLY_EQUIVALENT": "PRESERVED",
        "PARTIAL_PRESERVATION": "PARTIALLY_PRESERVED",
        "MUTATED": "ALTERED",
        "REGENERATED": "ALTERED",
    }.get(fidelity, fidelity)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validation = { (row["fixture"], row["converter"]): row for row in json.loads(VALIDATION.read_text(encoding="utf-8"))["records"] }
    all_results = []
    for item in manifest["fixtures"]:
        fixture = item["fixture_id"]
        feature = FEATURES[fixture]
        source = Path(item["path"])
        source_data = extract(source)
        source_json = BASE / "extracted" / "source" / f"{fixture}.json"
        source_json.parent.mkdir(parents=True, exist_ok=True)
        source_json.write_text(json.dumps(source_data, indent=2, ensure_ascii=False), encoding="utf-8")
        for converter, directory, suffix in (("LibreOffice", "libreoffice", "LIBREOFFICE"), ("Google Docs", "google_docs", "GOOGLE_DOCS")):
            destination = BASE / "outputs" / directory / f"{fixture}__{suffix}.pdf"
            destination_data = extract(destination)
            destination_json = BASE / "extracted" / directory / f"{fixture}.json"
            destination_json.parent.mkdir(parents=True, exist_ok=True)
            destination_json.write_text(json.dumps(destination_data, indent=2, ensure_ascii=False), encoding="utf-8")
            cli = run_cli(source, destination, feature)
            if "report" in cli:
                raw = cli["report"]["features"][0]
                raw["source_hash"] = sha256(source)
                raw["output_hash"] = sha256(destination)
                raw["converter"] = converter
                raw["fixture"] = fixture
                raw["source_path"] = str(source)
                raw["destination_path"] = str(destination)
                raw["validation"] = validation[(fixture, converter)]
                raw["empirical_classification"] = empirical_label(raw["fidelity_classification"])
                raw["evidence_path"] = {"source_extraction": str(source_json), "destination_extraction": str(destination_json)}
                raw["a11ydiff_command"] = cli["command"]
                all_results.append(raw)
            else:
                all_results.append({"fixture": fixture, "converter": converter, "feature": feature, "empirical_classification": "MEASUREMENT_ERROR", "error": cli})
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "matrix_size": len(all_results), "records": all_results}
    report_path = BASE / "reports" / "a11ydiff_results.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (BASE / "reports" / "semantic_diff_results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"records": len(all_results), "cli_failures": sum("error" in row for row in all_results), "classifications": {label: sum(row.get("empirical_classification") == label for row in all_results) for label in sorted({row.get("empirical_classification") for row in all_results})}}))


if __name__ == "__main__":
    main()
