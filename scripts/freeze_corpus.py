from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_HASHES = json.loads((ROOT / "pilot" / "manifests" / "hashes.json").read_text(encoding="utf-8"))
NEW_IDS = ["F05_DOCUMENT_LANGUAGE", "F06_INLINE_LANGUAGE", "F07_DECORATIVE_IMAGE", "F08_LINKS", "F09_DOCUMENT_TITLE", "F10_COMPLEX_TABLE", "F11_FOOTNOTES", "F12_EQUATION", "F14_CAPTIONS"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    verification = json.loads((ROOT / "corpus" / "reports" / "source_verification.json").read_text(encoding="utf-8"))
    if not verification.get("passed"):
        raise SystemExit("source verification has not passed; corpus remains unfrozen")
    entries = []
    for fixture_id, record in OLD_HASHES.items():
        path = ROOT / "pilot" / "fixtures" / f"{fixture_id}.docx"
        actual = sha256(path)
        if actual != record["source_docx"]:
            raise SystemExit(f"frozen pilot fixture changed: {fixture_id}")
        manifest = ROOT / "pilot" / "manifests" / f"{fixture_id}.json"
        entries.append({"fixture_id": fixture_id, "feature_family": fixture_id.split("_", 1)[1].lower(), "source_format": "DOCX", "path": str(path), "size_bytes": path.stat().st_size, "sha256": actual, "source_manifest": str(manifest), "source_manifest_sha256": sha256(manifest), "verification_status": "PASS", "historical_fixture": True})
    for fixture_id in NEW_IDS:
        path = ROOT / "corpus" / "fixtures" / f"{fixture_id}.docx"
        manifest = ROOT / "corpus" / "manifests" / f"{fixture_id}.json"
        record = next(row for row in verification["fixtures"] if row["fixture"] == fixture_id)
        if not record["manifest_matches_ooxml"] or not record["source_extractor_matches"]:
            raise SystemExit(f"new fixture did not verify: {fixture_id}")
        entries.append({"fixture_id": fixture_id, "feature_family": json.loads(manifest.read_text(encoding="utf-8"))["feature"], "source_format": "DOCX", "path": str(path), "size_bytes": path.stat().st_size, "sha256": sha256(path), "source_manifest": str(manifest), "source_manifest_sha256": sha256(manifest), "verification_status": "PASS", "historical_fixture": False})
    now = datetime.now().astimezone().isoformat()
    frozen = {"corpus_version": "phase4-v1", "frozen_at": now, "fixture_count": len(entries), "fixtures": entries, "verification": {"raw_ooxml": "corpus/reports/source_verification.json", "frozen_pilot_hashes": "pilot/manifests/hashes.json"}, "frozen": True}
    target = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
    target.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    build = json.loads((ROOT / "corpus" / "BUILD_RECORD.json").read_text(encoding="utf-8"))
    for row in build["generated"]:
        match = next(entry for entry in entries if entry["fixture_id"] == row["fixture"])
        row.update({"size_bytes": match["size_bytes"], "sha256": match["sha256"], "verification_status": "PASS"})
    build["frozen"] = True
    build["frozen_manifest"] = str(target)
    (ROOT / "corpus" / "BUILD_RECORD.json").write_text(json.dumps(build, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"frozen": True, "fixture_count": len(entries), "manifest": str(target)}, indent=2))


if __name__ == "__main__":
    main()
