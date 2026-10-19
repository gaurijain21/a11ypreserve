from __future__ import annotations

import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
OUT = V4 / "conversions" / "google"
ATOMIC_OUT = OUT / "outputs" / "atomic"
REALISTIC_OUT = OUT / "outputs" / "realistic"

ROUTE = "Authenticated Google Docs visible UI import; File -> Download -> PDF Document (.pdf); Chrome download capture"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_pdf(path: Path) -> dict:
    data = path.read_bytes()
    if not data.startswith(b"%PDF"):
        raise ValueError(f"not a PDF signature: {path}")
    doc = fitz.open(path)
    raw = data.decode("latin-1", errors="ignore")
    metadata = doc.metadata or {}
    return {
        "exists": True,
        "size_bytes": path.stat().st_size,
        "pdf_header": data[:5].decode("ascii", errors="replace"),
        "sha256": sha256(path),
        "parseable": True,
        "page_count": len(doc),
        "tagged": "/StructTreeRoot" in raw,
        "producer": metadata.get("producer"),
        "creator": metadata.get("creator"),
        "last_write_time_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
    }


def record(corpus: str, fixture_id: str, source_path: Path, output_path: Path, role: str | None = None, document_id: str | None = None) -> dict:
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if not output_path.exists():
        raise FileNotFoundError(output_path)
    output = inspect_pdf(output_path)
    row = {
        "corpus": corpus,
        "fixture_id": fixture_id,
        "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": sha256(source_path),
        "expected_source_sha256": sha256(source_path),
        "converter": "Google Docs",
        "converter_version": "Google Docs web application; producer recorded per output",
        "route": ROUTE,
        "browser": "Chrome 154.0.8037.97; authenticated profile session",
        "upload_timestamp": None,
        "conversion_timestamp": output["last_write_time_utc"],
        "output_path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
        "output": output,
        "status": "SUCCESS",
        "error": None,
        "environment": platform.platform(),
    }
    if role is not None:
        row["role"] = role
    if document_id is not None:
        row["document_id"] = document_id
    return row


def main() -> None:
    source_manifest = json.loads((V4 / "source_manifest.json").read_text(encoding="utf-8"))
    realistic_manifest = json.loads((V4 / "realistic" / "REALISTIC_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
    records = []
    for entry in source_manifest["records"]:
        fixture_id = entry["variant_id"]
        output = ATOMIC_OUT / f"{fixture_id}__GOOGLE_DOCS.pdf"
        row = record("atomic", fixture_id, ROOT / entry["fixture"], output, entry["role"])
        row["expected_source_sha256"] = entry["source_sha256"]
        if row["source_sha256"] != entry["source_sha256"]:
            raise ValueError(f"source hash mismatch: {fixture_id}")
        records.append(row)
    for entry in realistic_manifest["records"]:
        document_id = entry["document_id"]
        output = REALISTIC_OUT / f"{document_id}__GOOGLE_DOCS.pdf"
        records.append(record("realistic", document_id, ROOT / entry["path"], output, document_id=document_id))
    payload = {
        "manifest_version": "v4-google-docs-conversion-1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "converter": "Google Docs",
        "route": ROUTE,
        "browser": "Chrome 154.0.8037.97; authenticated profile session",
        "settings": "Google Docs import followed by visible UI File -> Download -> PDF Document (.pdf)",
        "records": records,
        "summary": {"atomic": len([r for r in records if r["corpus"] == "atomic"]), "realistic_documents": len([r for r in records if r["corpus"] == "realistic"])},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
