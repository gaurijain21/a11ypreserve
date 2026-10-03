from __future__ import annotations

"""Validate the primary Phase 5 conversion outputs without judging accessibility."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
OUT_ROOT = ROOT / "results" / "full_experiment" / "outputs"
REPORT = ROOT / "results" / "full_experiment" / "reports" / "output_validation.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate(path: Path, fixture_id: str, converter: str) -> dict:
    item = {
        "fixture": fixture_id,
        "converter": converter,
        "path": str(path),
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "sha256": sha256(path) if path.exists() else None,
        "parseable": False,
        "page_count": None,
        "tagged": None,
        "struct_tree_root": None,
        "content_present": False,
        "invalid_conversion": False,
        "errors": [],
    }
    if not path.exists():
        item["errors"].append("missing output")
        item["invalid_conversion"] = True
        return item
    if item["size_bytes"] == 0:
        item["errors"].append("zero-byte output")
        item["invalid_conversion"] = True
        return item
    try:
        reader = PdfReader(str(path))
        item["parseable"] = True
        item["page_count"] = len(reader.pages)
        root = reader.trailer.get("/Root")
        root = root.get_object() if root is not None else None
        struct_root = root.get("/StructTreeRoot") if root is not None else None
        item["struct_tree_root"] = struct_root is not None
        item["tagged"] = struct_root is not None
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        item["content_present"] = bool(text.strip())
        if not item["content_present"]:
            item["errors"].append("no extractable text; inspect image-only content separately")
    except Exception as exc:  # validation must retain the concrete parser failure
        item["errors"].append(f"{type(exc).__name__}: {exc}")
    item["invalid_conversion"] = not (item["parseable"] and item["page_count"] and item["content_present"])
    return item


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = []
    for fixture in manifest["fixtures"]:
        fixture_id = fixture["fixture_id"]
        for converter, directory, suffix in (("LibreOffice", "libreoffice", "LIBREOFFICE"), ("Google Docs", "google_docs", "GOOGLE_DOCS")):
            path = OUT_ROOT / directory / f"{fixture_id}__{suffix}.pdf"
            records.append(validate(path, fixture_id, converter))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "records": records}, indent=2), encoding="utf-8")
    print(json.dumps({"records": len(records), "valid": sum(not r["invalid_conversion"] for r in records), "invalid": sum(r["invalid_conversion"] for r in records)}))


if __name__ == "__main__":
    main()
