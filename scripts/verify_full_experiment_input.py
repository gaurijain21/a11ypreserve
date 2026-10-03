from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest_path = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = []
    for entry in manifest["fixtures"]:
        path = Path(entry["path"])
        actual = sha256(path) if path.exists() else None
        rows.append({"fixture": entry["fixture_id"], "path": str(path), "expected_sha256": entry["sha256"], "actual_sha256": actual, "size_bytes": path.stat().st_size if path.exists() else None, "matches": actual == entry["sha256"]})
    report = {"verified_at": datetime.now().astimezone().isoformat(), "manifest": str(manifest_path), "expected_fixtures": 13, "matched_fixtures": sum(row["matches"] for row in rows), "passed": len(rows) == 13 and all(row["matches"] for row in rows), "fixtures": rows}
    target = ROOT / "results" / "FULL_EXPERIMENT_INPUT_VERIFICATION.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Full experiment input verification", "", f"Verified: {report['verified_at']}", f"Manifest: `{manifest_path}`", "", f"Result: **{'PASS' if report['passed'] else 'FAIL'}** ({report['matched_fixtures']}/{report['expected_fixtures']} exact SHA-256 matches)", "", "| Fixture | Size (bytes) | SHA-256 | Match |", "|---|---:|---|---|"]
    lines += [f"| {row['fixture']} | {row['size_bytes']} | `{row['actual_sha256']}` | {'YES' if row['matches'] else 'NO'} |" for row in rows]
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
