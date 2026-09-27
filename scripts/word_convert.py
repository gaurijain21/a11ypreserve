from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import win32com.client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
EVIDENCE = ROOT / "evidence"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source: str) -> None:
    src = Path(source).resolve()
    OUT.mkdir(exist_ok=True)
    EVIDENCE.mkdir(exist_ok=True)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    doc = None
    records = []
    try:
        doc = word.Documents.Open(str(src), ReadOnly=True, AddToRecentFiles=False)
        pdf = OUT / f"{src.stem}_word.pdf"
        doc.ExportAsFixedFormat(str(pdf), 17, False, 0, 0, 1, 1, 0, True, False, 0, True, True, False)
        records.append({"output": str(pdf), "method": "Word ExportAsFixedFormat", "version": word.Version, "hash": sha256(pdf)})
        html = OUT / f"{src.stem}_word.html"
        doc.SaveAs2(str(html), FileFormat=10)
        records.append({"output": str(html), "method": "Word SaveAs2 wdFormatFilteredHTML", "version": word.Version, "hash": sha256(html)})
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()
    record = {"source": str(src), "source_hash": sha256(src), "created_utc": datetime.now(timezone.utc).isoformat(),
              "os": platform.platform(), "python": sys.version, "records": records}
    (EVIDENCE / "word_conversions.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
