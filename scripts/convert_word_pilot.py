from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "pilot"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    output_dir = PILOT / "outputs" / "word"
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    try:
        import win32com.client
    except Exception as exc:
        records.append({"status": "unavailable", "error": f"pywin32 import failed: {exc}"})
        (PILOT / "logs" / "word_conversion.json").write_text(json.dumps({"records": records}, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"records": records}, indent=2))
        return
    word = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        version = str(word.Version)
        for source in sorted((PILOT / "fixtures").glob("F*.docx")):
            doc = None
            record = {"fixture_id": source.stem, "source": str(source), "source_sha256": sha256(source), "converter": "Microsoft Word", "converter_version": version, "pathway": "Document.ExportAsFixedFormat", "settings": {"format": "PDF", "optimize_for": "print", "use_iso_19005_1": True, "include_doc_props": True}}
            try:
                doc = word.Documents.Open(str(source), ReadOnly=True, AddToRecentFiles=False)
                pdf = output_dir / f"{source.stem}.pdf"
                # ExportAsFixedFormat(OutputFileName, ExportFormat=wdExportFormatPDF,
                # OpenAfterExport=False, OptimizeFor=wdExportOptimizeForPrint,
                # Range=wdExportAllDocument, Item=wdExportDocumentContent,
                # IncludeDocProps=True, KeepIRM=True, CreateBookmarks=wdExportCreateHeadingBookmarks,
                # DocStructureTags=True, BitmapMissingFonts=True, UseISO19005_1=True)
                doc.ExportAsFixedFormat(str(pdf), 17, False, 0, 0, 1, 1, 0, True, False, 0, True, True, True)
                record.update({"status": "ok", "output": str(pdf), "output_sha256": sha256(pdf), "output_bytes": pdf.stat().st_size})
            except Exception as exc:
                record.update({"status": "failed", "error": repr(exc)})
            finally:
                if doc is not None:
                    try:
                        doc.Close(False)
                    except Exception:
                        pass
            records.append(record)
    except Exception as exc:
        records.append({"status": "failed", "error": repr(exc), "stage": "Word.Application"})
    finally:
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
    result = {"recorded_utc": datetime.now(timezone.utc).isoformat(), "os": platform.platform(), "python": sys.version, "records": records}
    (PILOT / "logs" / "word_conversion.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
