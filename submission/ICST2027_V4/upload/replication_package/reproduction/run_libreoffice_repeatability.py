from __future__ import annotations
import hashlib, json, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "pilot2/libreoffice_runtime/program/soffice.com"
SETTINGS = "UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"
SELECTED = ["F04_D", "F06_D", "F08_D", "F11_D", "F12_D", "F13_D"]
BASE = ROOT / "experiments/v4/conversions/libreoffice/repeatability"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    manifest = json.loads((ROOT / "experiments/v4/source_manifest.json").read_text(encoding="utf-8"))
    entries = {x["variant_id"]: x for x in manifest["records"]}
    runs = []
    for run_index in range(1, 4):
        for fixture in SELECTED:
            source = ROOT / entries[fixture]["fixture"]
            run_dir = BASE / f"run{run_index}"
            out = run_dir / f"{fixture}__LIBREOFFICE__R{run_index}.pdf"
            stage = BASE / "staging" / f"run{run_index}" / source.name
            profile = BASE / "profiles" / f"run{run_index}" / fixture
            run_dir.mkdir(parents=True, exist_ok=True); stage.parent.mkdir(parents=True, exist_ok=True); profile.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, stage)
            uri = "file:///" + str(profile).replace("\\", "/")
            cmd = [str(RUNTIME), f"-env:UserInstallation={uri}", "--headless", "--invisible", "--nodefault", "--nologo", "--nolockcheck", "--norestore", "--nofirststartwizard", "--convert-to", f"pdf:writer_pdf_Export:{SETTINGS}", "--outdir", str(run_dir), str(stage)]
            started = datetime.now(timezone.utc).isoformat()
            result = subprocess.run(cmd, cwd=RUNTIME.parent, capture_output=True, text=True, timeout=180)
            generated = run_dir / f"{source.stem}.pdf"
            if generated.exists() and generated != out:
                if out.exists(): out.unlink()
                generated.replace(out)
            runs.append({"fixture_id": fixture, "run": run_index, "source_path": str(source.relative_to(ROOT)).replace("\\", "/"), "source_sha256": sha(source), "output_path": str(out.relative_to(ROOT)).replace("\\", "/"), "output_sha256": sha(out) if out.exists() else None, "started_at": started, "completed_at": datetime.now(timezone.utc).isoformat(), "returncode": result.returncode, "stdout_tail": result.stdout[-500:], "stderr_tail": result.stderr[-500:], "status": "SUCCESS" if result.returncode == 0 and out.exists() else "FAILED"})
    payload = {"protocol": "experiments/v4/REPEATABILITY_MANIFEST.json", "pipeline": "LibreOffice", "selected_variants": SELECTED, "target_runs_per_identical_source": 3, "records": runs, "successful": sum(x["status"] == "SUCCESS" for x in runs), "total": len(runs)}
    (BASE / "RUN_MANIFEST.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if payload["successful"] != payload["total"]: raise SystemExit(1)
    print(json.dumps({"successful": payload["successful"], "total": payload["total"], "manifest": str(BASE / "RUN_MANIFEST.json")}, indent=2))
if __name__ == "__main__": main()
