from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "pilot2" / "libreoffice_runtime" / "program" / "soffice.com"
MANIFEST = ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"
BASE = ROOT / "results" / "full_experiment"
OUTPUT = BASE / "outputs" / "libreoffice"
STAGING = BASE / "lo_inputs"
PROFILES = BASE / "lo_profiles"
SETTINGS = "UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_info(path: Path) -> tuple[int | None, bool | None, str | None]:
    try:
        reader = PdfReader(str(path))
        root = reader.trailer.get("/Root")
        tagged = bool(root and root.get("/StructTreeRoot"))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return len(reader.pages), tagged, text[:1000]
    except Exception as exc:
        return None, None, f"PDF parse error: {exc}"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    PROFILES.mkdir(parents=True, exist_ok=True)
    version_result = subprocess.run([str(RUNTIME), "--version"], capture_output=True, text=True, timeout=30)
    version = (version_result.stdout or version_result.stderr).strip()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = []
    for entry in manifest["fixtures"]:
        fixture = entry["fixture_id"]
        source = Path(entry["path"])
        staging = STAGING / source.name
        destination = OUTPUT / f"{fixture}__LIBREOFFICE.pdf"
        shutil.copy2(source, staging)
        profile = PROFILES / fixture
        profile.mkdir(parents=True, exist_ok=True)
        profile_uri = "file:///" + str(profile).replace("\\", "/")
        command = [str(RUNTIME), f"-env:UserInstallation={profile_uri}", "--headless", "--invisible", "--nodefault", "--nologo", "--nolockcheck", "--norestore", "--nofirststartwizard", "--convert-to", f"pdf:writer_pdf_Export:{SETTINGS}", "--outdir", str(OUTPUT), str(staging)]
        started = datetime.now().astimezone().isoformat()
        error = None
        result = "SUCCESS"
        stdout = stderr = ""
        try:
            completed = subprocess.run(command, cwd=RUNTIME.parent, capture_output=True, text=True, timeout=180)
            stdout, stderr = completed.stdout, completed.stderr
            expected_generated = OUTPUT / f"{staging.stem}.pdf"
            if expected_generated.exists() and expected_generated != destination:
                if destination.exists():
                    destination.unlink()
                expected_generated.replace(destination)
            if completed.returncode != 0 or not destination.exists():
                result = "FAILED"
                error = f"returncode={completed.returncode}; stdout={stdout[-1000:]}; stderr={stderr[-1000:]}"
        except Exception as exc:
            result = "FAILED"
            error = repr(exc)
        pages, tagged, preview = pdf_info(destination) if destination.exists() else (None, None, None)
        records.append({"fixture": fixture, "source": str(source), "source_sha256": sha256(source), "converter": "LibreOffice", "converter_version": version, "build": "26.2.6.3 bundled runtime (recorded from Pilot 2/3 environment)", "os": platform.platform(), "executable": str(RUNTIME), "method": "headless soffice.com writer_pdf_Export", "settings": SETTINGS, "started_at": started, "completed_at": datetime.now().astimezone().isoformat(), "destination": str(destination), "output_sha256": sha256(destination) if destination.exists() else None, "file_size": destination.stat().st_size if destination.exists() else None, "page_count": pages, "tagged": tagged, "content_preview": preview, "result": result, "error": error})
    report = {"converter": "LibreOffice", "version": version, "settings": SETTINGS, "records": records, "successful": sum(row["result"] == "SUCCESS" for row in records)}
    (BASE / "reports").mkdir(parents=True, exist_ok=True)
    (BASE / "reports" / "libreoffice_conversion.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["successful"] != len(records):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
