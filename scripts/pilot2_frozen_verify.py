from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT2 = ROOT / "pilot2"
FIXTURES = ROOT / "pilot" / "fixtures"
HASHES = ROOT / "pilot" / "manifests" / "hashes.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    expected = json.loads(HASHES.read_text(encoding="utf-8"))
    verified_at = datetime.now(timezone.utc).isoformat()
    rows = []
    failures = []
    for fixture_id in ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE"):
        path = FIXTURES / f"{fixture_id}.docx"
        actual = sha256(path)
        expected_hash = expected[fixture_id]["source_docx"]
        row = {
            "fixture_id": fixture_id,
            "filename": path.name,
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "expected_sha256": expected_hash,
            "actual_sha256": actual,
            "match": actual == expected_hash,
            "verified_at_utc": verified_at,
        }
        rows.append(row)
        if not row["match"]:
            failures.append(fixture_id)
    result = {
        "verified_at_utc": verified_at,
        "host_os": platform.platform(),
        "manifest": str(HASHES),
        "fixture_count": len(rows),
        "all_match": not failures,
        "failures": failures,
        "fixtures": rows,
    }
    out = PILOT2 / "FROZEN_INPUT_VERIFICATION.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    md = [
        "# Frozen Input Verification",
        "",
        f"Verification timestamp (UTC): {verified_at}",
        "",
        "The four source DOCX files were checked against `pilot/manifests/hashes.json` before conversion. All fixture hashes must match before the experiment may continue.",
        "",
        "| Fixture | Filename | Size (bytes) | Expected SHA-256 | Actual SHA-256 | Match |",
        "|---|---|---:|---|---|---|",
    ]
    for row in rows:
        md.append(f"| {row['fixture_id']} | `{row['filename']}` | {row['size_bytes']} | `{row['expected_sha256']}` | `{row['actual_sha256']}` | {'PASS' if row['match'] else 'FAIL'} |")
    md.extend(["", f"Overall result: **{'PASS' if not failures else 'FAIL'}**.", ""])
    (PILOT2 / "FROZEN_INPUT_VERIFICATION.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    PILOT2.mkdir(parents=True, exist_ok=True)
    main()
