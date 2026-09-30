from __future__ import annotations
import hashlib, json, platform, shutil, subprocess
from datetime import datetime
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"v3"/"variant_set_b"/"libreoffice"
SOURCE=ROOT/"corpus"/"v3_variant_set_b"/"fixtures"
RUNTIME=ROOT/"pilot2"/"libreoffice_runtime"/"program"/"soffice.com"
OUT=BASE/"outputs"; STAGE=BASE/"inputs"; PROFILES=BASE/"profiles"
SETTINGS="UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1"
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def info(p):
 try:
  r=PdfReader(str(p)); root=r.trailer.get("/Root"); return len(r.pages),bool(root and root.get("/StructTreeRoot"))
 except Exception: return None,None
OUT.mkdir(parents=True,exist_ok=True); STAGE.mkdir(parents=True,exist_ok=True); PROFILES.mkdir(parents=True,exist_ok=True)
version=(subprocess.run([str(RUNTIME),"--version"],capture_output=True,text=True,timeout=30).stdout or "").strip()
rows=[]
for src in sorted(SOURCE.glob("B*.docx")):
 dest=OUT/(src.stem+"__LIBREOFFICE.pdf"); shutil.copy2(src,STAGE/src.name); profile=PROFILES/src.stem; profile.mkdir(parents=True,exist_ok=True); uri="file:///"+str(profile).replace("\\","/")
 cmd=[str(RUNTIME),f"-env:UserInstallation={uri}","--headless","--invisible","--nodefault","--nologo","--nolockcheck","--norestore","--nofirststartwizard","--convert-to",f"pdf:writer_pdf_Export:{SETTINGS}","--outdir",str(OUT),str(STAGE/src.name)]
 started=datetime.now().astimezone().isoformat(); p=subprocess.run(cmd,cwd=RUNTIME.parent,capture_output=True,text=True,timeout=180); generated=OUT/(src.stem+".pdf")
 if generated.exists() and generated!=dest:
  if dest.exists(): dest.unlink()
  generated.replace(dest)
 pages,tagged=info(dest) if dest.exists() else (None,None)
 rows.append({"variant_id":src.stem,"source":"corpus/v3_variant_set_b/fixtures/"+src.name,"source_sha256":sha(src),"converter":"LibreOffice","version":version,"settings":SETTINGS,"started_at":started,"completed_at":datetime.now().astimezone().isoformat(),"destination":"v3/variant_set_b/libreoffice/outputs/"+dest.name,"output_sha256":sha(dest) if dest.exists() else None,"file_size":dest.stat().st_size if dest.exists() else None,"page_count":pages,"tagged":tagged,"returncode":p.returncode,"stdout":p.stdout[-1000:],"stderr":p.stderr[-1000:],"status":"PASS" if p.returncode==0 and dest.exists() else "FAIL"})
report={"converter":"LibreOffice","variant_count":len(rows),"passed":sum(x["status"]=="PASS" for x in rows),"records":rows}; (BASE/"CONVERSION_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"variant_count":len(rows),"passed":report["passed"]},indent=2)); raise SystemExit(0 if report["passed"]==len(rows) else 1)
