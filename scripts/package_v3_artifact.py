"""Create the sanitized V3 candidate artifact ZIP."""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifact_v3"
TARGET = ROOT / "submission" / "A11yPreserve_artifact_ICST2027_V3.zip"
EXCLUDE_PARTS = {".git", ".miktex", "__pycache__"}


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"missing {SOURCE}")
    files = [p for p in SOURCE.rglob("*") if p.is_file() and not any(part in EXCLUDE_PARTS for part in p.parts)]
    with zipfile.ZipFile(TARGET, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, Path("artifact_v3") / path.relative_to(SOURCE))
    print({"path": str(TARGET), "files": len(files), "bytes": TARGET.stat().st_size})


if __name__ == "__main__":
    main()
