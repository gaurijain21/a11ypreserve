from __future__ import annotations
import importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("extract_semantics",ROOT/"scripts"/"extract_semantics.py"); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
BASE=ROOT/"v3"/"variant_set_b"/"libreoffice"; OUT=BASE/"extracted"; OUT.mkdir(parents=True,exist_ok=True)
rows=[]
for mp in sorted((ROOT/"corpus"/"v3_variant_set_b"/"manifests").glob("B*.json")):
 rec=json.loads(mp.read_text(encoding="utf-8")); pdf=BASE/"outputs"/(rec["variant_id"]+"__LIBREOFFICE.pdf"); obs=mod.extract(pdf); (OUT/(rec["variant_id"]+".json")).write_text(json.dumps(obs,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 f=rec["feature_family"]; g=rec["ground_truth"]; note="observed destination representation retained for feature-specific review"; evidence={"tagged":obs.get("tagged"),"page_count":obs.get("pdf",{}).get("pages"),"headings":len(obs.get("headings",[])),"figures":len(obs.get("figures",[])),"lists":len(obs.get("lists",[])),"tables":len(obs.get("tables",[])),"links":len(obs.get("hyperlinks",[])),"footnotes":len(obs.get("footnotes",[])),"equations":len(obs.get("equations",[])),"captions":len(obs.get("captions",[])),"inline_languages":len(obs.get("inline_languages",[]))}
 rows.append({"variant_id":rec["variant_id"],"feature_family":f,"pipeline":"LibreOffice","output":"v3/variant_set_b/libreoffice/outputs/"+pdf.name,"evidence_summary":evidence,"note":note})
(BASE/"VARIANT_OBSERVATIONS.json").write_text(json.dumps({"variant_count":len(rows),"records":rows},indent=2)+"\n",encoding="utf-8"); print(json.dumps({"variant_count":len(rows),"records":rows},indent=2))
