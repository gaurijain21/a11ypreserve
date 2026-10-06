from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments/v4/conversions/word/outputs/repeatability"
SOURCE_MANIFEST = json.loads((ROOT / "experiments/v4/source_manifest.json").read_text(encoding="utf-8"))
SELECTED = ["F04_D", "F06_D", "F08_D", "F11_D", "F12_D", "F13_D"]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


records = []
for fixture_id in SELECTED:
    source = next(x for x in SOURCE_MANIFEST["records"] if x["variant_id"] == fixture_id)
    for run in range(1, 4):
        path = OUT / f"{fixture_id}__WORD_DESKTOP__run{run}.pdf"
        reader = PdfReader(str(path))
        metadata = reader.metadata or {}
        root = reader.trailer.get("/Root")
        records.append(
            {
                "fixture_id": fixture_id,
                "feature_family": source["feature_family"],
                "source_path": source["fixture"].replace("\\", "/"),
                "source_sha256": source["source_sha256"],
                "run": run,
                "output_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "output_sha256": digest(path),
                "size_bytes": path.stat().st_size,
                "page_count": len(reader.pages),
                "parseable": True,
                "tagged": bool(root and root.get("/StructTreeRoot")),
                "producer": str(metadata.get("/Producer")) if metadata.get("/Producer") else None,
                "creator": str(metadata.get("/Creator")) if metadata.get("/Creator") else None,
                "converter": "Microsoft Word desktop",
                "route": "Word GUI File -> Export -> Create PDF/XPS Document -> Create PDF/XPS",
                "settings": "Document structure tags for accessibility=true; Open file after publishing=false",
            }
        )

byte_identity = {}
for fixture_id in SELECTED:
    group = [x for x in records if x["fixture_id"] == fixture_id]
    byte_identity[fixture_id] = len({x["output_sha256"] for x in group}) == 1

manifest = {
    "manifest_version": "v4-word-gui-repeatability-1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "selected_variants": SELECTED,
    "runs_per_source": 3,
    "comparison_fields": ["byte_identity", "structure_identity", "extraction_identity", "classification_identity"],
    "byte_identity_by_fixture": byte_identity,
    "byte_identity_status": "PASS" if all(byte_identity.values()) else "NONIDENTICAL_BYTES",
    "classification_status": "PENDING_FROZEN_ANALYSIS",
    "records": records,
}
path = ROOT / "experiments/v4/conversions/word/repeatability_manifest.json"
path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"records": len(records), "byte_identity_status": manifest["byte_identity_status"], "path": str(path)}, indent=2))
