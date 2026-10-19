"""Verify that the review artifact is self-contained and internally consistent.

This check uses only the Python standard library.  It validates result counts,
provenance links, frozen source/output hashes, repeatability outputs, and the
absence of machine-specific absolute paths in text-like release files.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "VERIFIED_PRESERVED": 18,
    "OBSERVED_PARTIAL": 4,
    "ALTERED": 7,
    "CONFIRMED_LOST": 4,
    "UNRESOLVED_EQUIVALENCE": 18,
    "MEASUREMENT_ERROR": 1,
}
FIXTURES = [
    "F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE",
    "F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE",
    "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE",
    "F11_FOOTNOTES", "F12_EQUATION", "F14_CAPTIONS",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve(relative: str) -> Path:
    return (ROOT / relative).resolve()


def destination_path(record: dict) -> Path:
    fixture = record["fixture"]
    pipeline = record["pipeline"]
    if record.get("study_arm") == "Variant B":
        folder = "libreoffice" if pipeline == "LibreOffice" else "google"
        suffix = "LIBREOFFICE" if pipeline == "LibreOffice" else "GOOGLE_DOCS"
        return ROOT / "v3" / "variant_set_b" / folder / "outputs" / f"{fixture}__{suffix}.pdf"
    folder = "libreoffice" if pipeline == "LibreOffice" else "google_docs"
    suffix = "LIBREOFFICE" if pipeline == "LibreOffice" else "GOOGLE_DOCS"
    return ROOT / "corpus" / "outputs" / folder / f"{fixture}__{suffix}.pdf"


def source_path(record: dict) -> Path:
    fixture = record["fixture"]
    if record.get("study_arm") == "Variant B":
        return ROOT / "corpus" / "v3_variant_set_b" / "fixtures" / f"{fixture}.docx"
    return ROOT / "corpus" / "fixtures" / f"{fixture}.docx"


def main() -> None:
    failures: list[str] = []
    results_path = ROOT / "results" / "V3_PRIMARY_RESULTS.json"
    data = json.loads(results_path.read_text(encoding="utf-8"))
    counts = {key: int(value) for key, value in data["counts"].items()}
    if data.get("record_count") != 52 or len(data.get("records", [])) != 52:
        failures.append("V3_PRIMARY_RESULTS.json does not contain 52 records")
    if counts != EXPECTED_COUNTS:
        failures.append(f"unexpected result counts: {counts}")

    checked_records = 0
    for record in data["records"]:
        checked_records += 1
        src = source_path(record)
        dst = destination_path(record)
        if not src.exists():
            failures.append(f"missing source: {src.relative_to(ROOT)}")
        elif sha256(src) != record["source_sha256"]:
            failures.append(f"source hash mismatch: {record['fixture']} {record['study_arm']}")
        if not dst.exists():
            failures.append(f"missing destination: {dst.relative_to(ROOT)}")
        elif sha256(dst) != record["destination_sha256"]:
            failures.append(f"destination hash mismatch: {record['fixture']} {record['pipeline']} {record['study_arm']}")

        for field in ("supporting_artifact", "source_manifest", "destination_extraction"):
            value = record.get(field)
            if isinstance(value, str) and not resolve(value).exists():
                failures.append(f"broken provenance link: {field}={value}")
        evidence_path = record.get("evidence_path", {})
        for field, value in evidence_path.items() if isinstance(evidence_path, dict) else ():
            if isinstance(value, str) and not resolve(value).exists():
                failures.append(f"broken provenance link: evidence_path.{field}={value}")

    repeatability = ROOT / "v3" / "google_repeatability" / "REPEATABILITY_RESULTS.json"
    repeatability_data = json.loads(repeatability.read_text(encoding="utf-8"))
    if repeatability_data.get("fixture_count") != 13 or repeatability_data.get("run_count") != 39:
        failures.append("repeatability report has unexpected dimensions")
    for record in repeatability_data.get("records", []):
        for field in ("run_1", "run_2", "run_3"):
            path = resolve(record[field])
            if not path.exists():
                failures.append(f"missing repeatability output: {record[field]}")
            elif sha256(path) not in record.get("hashes", []):
                failures.append(f"repeatability hash mismatch: {record['fixture']} {field}")

    machine_path = re.compile(r"(?i)(?:[a-z]:[\\/]+users[\\/]|<LOCAL_UNIX_PATH>")
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".pdf", ".docx", ".png"} or path.name == "verify_public_package.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if machine_path.search(text):
            failures.append(f"machine-specific absolute path: {path.relative_to(ROOT)}")

    summary = {"records_checked": checked_records, "expected_counts": EXPECTED_COUNTS, "failures": failures, "status": "PASS" if not failures else "FAIL"}
    print(json.dumps(summary, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
