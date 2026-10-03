"""Separate raw OOXML checks for Variant Set B.

This deliberately reads only the V3 variant manifest and DOCX ZIP/XML; it does
not import the variant generator, ASIR, or the PDF comparator.
"""
from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "corpus" / "v3_variant_set_b"
REPORT = BASE / "SOURCE_ORACLE.json"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
DC = "{http://purl.org/dc/elements/1.1/}"
DC = "{http://purl.org/dc/elements/1.1/}"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def txt(node):
    return "".join((x.text or "") for x in node.iter() if x.tag in {W+"t", M+"t"})

def inspect(path):
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist()); doc=ET.fromstring(z.read("word/document.xml")); styles=ET.fromstring(z.read("word/styles.xml")); core=ET.fromstring(z.read("docProps/core.xml")); rels=ET.fromstring(z.read("word/_rels/document.xml.rels")); numbering=ET.fromstring(z.read("word/numbering.xml")); foot=ET.fromstring(z.read("word/footnotes.xml")) if "word/footnotes.xml" in names else None
    rel_targets={n.attrib.get("Id"):n.attrib.get("Target") for n in rels if n.attrib.get("Type","").endswith("/hyperlink")}
    headings=[]; lists=[]; inline=[]; figures=[]; links=[]; captions=[]; equations=[]; notes=[]; tables=[]
    formats={}
    for a in numbering.findall(W+"abstractNum"):
        aid=a.attrib.get(W+"abstractNumId");
        for l in a.findall(W+"lvl"):
            n=l.find(W+"numFmt"); formats[(aid,l.attrib.get(W+"ilvl","0"))]=n.attrib.get(W+"val","") if n is not None else ""
    nums={n.attrib.get(W+"numId"):n.find(W+"abstractNumId").attrib.get(W+"val") for n in numbering.findall(W+"num") if n.find(W+"abstractNumId") is not None}
    for p in doc.iter(W+"p"):
        ppr=p.find(W+"pPr"); style=None
        if ppr is not None and ppr.find(W+"pStyle") is not None: style=ppr.find(W+"pStyle").attrib.get(W+"val")
        v=txt(p)
        if style and style.lower().startswith("heading"): headings.append({"text":v,"level":int(style[-1])})
        if style and style.lower()=="caption": captions.append(v)
        if ppr is not None and ppr.find(W+"numPr") is not None:
            np=ppr.find(W+"numPr"); nid=np.find(W+"numId"); il=np.find(W+"ilvl"); level=il.attrib.get(W+"val","0") if il is not None else "0"; num=nid.attrib.get(W+"val") if nid is not None else ""; fmt=formats.get((nums.get(num),level),""); lists.append({"type":"ordered" if fmt in {"decimal","upperRoman","lowerRoman","upperLetter","lowerLetter"} else "unordered","depth":int(level),"text":v})
        for r in p.iter(W+"r"):
            rv=txt(r); n=r.find(W+"rPr/"+W+"lang")
            if rv and n is not None and n.attrib.get(W+"val"): inline.append({"text":rv,"language":n.attrib.get(W+"val")})
        for a in p.findall(".//"+W+"hyperlink"): links.append({"text":txt(a),"target":rel_targets.get(a.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")),"order":len(links)+1})
    for i,n in enumerate(doc.iter(WP+"docPr"),1): figures.append({"alt":n.attrib.get("descr",""),"order":i})
    for tbl in doc.iter(W+"tbl"):
        rows=[]; hdr=[]
        for ri,tr in enumerate(tbl.findall(W+"tr")):
            cells=[txt(tc) for tc in tr.findall(W+"tc")]; rows.append(cells)
            if tr.find(W+"trPr/"+W+"tblHeader") is not None: hdr.append(ri)
        tables.append({"dimensions":{"rows":len(rows),"columns":max([len(x) for x in rows],default=0)},"header_rows":hdr,"cells":rows})
    for m in doc.iter(M+"oMath"): equations.append({"tokens":[x.text or "" for x in m.iter(M+"t")]})
    if foot is not None:
        bodies={int(n.attrib[W+"id"]):txt(n) for n in foot.findall(W+"footnote") if n.attrib.get(W+"id","").lstrip("-").isdigit() and int(n.attrib[W+"id"])>0}
        for ref in doc.iter(W+"footnoteReference"): notes.append({"kind":"footnote","id":int(ref.attrib.get(W+"id","0")),"text":bodies.get(int(ref.attrib.get(W+"id","0")),"").strip()})
    langs=[n.attrib.get(W+"val") for n in styles.iter(W+"lang") if n.attrib.get(W+"val")]
    corevals={n.tag:n.text for n in core.iter() if n.tag in {DC+"title",DC+"subject",DC+"language"}}
    return {"headings":headings,"lists":lists,"inline_languages":inline,"figures":figures,"hyperlinks":links,"captions":captions,"equations":equations,"footnotes":notes,"tables":tables,"language_values":langs,"core":corevals}

def check(rec, obs):
    f=rec["feature_family"]; g=rec["ground_truth"]
    if f=="headings": return len(obs["headings"])==len(g["headings"]) and all(a["level"]==b["level"] and a["text"]==b["text"] for a,b in zip(obs["headings"],g["headings"]))
    if f in {"alt_text","decorative_image"}: return len(obs["figures"])==len(g["figures"]) and all(a["alt"]==b["alt"] for a,b in zip(obs["figures"],g["figures"]))
    if f in {"lists"}: return obs["lists"]==g["lists"]
    if f == "table": return obs["tables"]==[g]
    if f == "complex_table": return obs["tables"]==[g["table"]]
    if f=="document_language": return g["document_language"] in obs["language_values"]
    if f=="inline_language": return all(x in obs["inline_languages"] for x in g["runs"])
    if f=="links": return obs["hyperlinks"]==g["hyperlinks"]
    if f=="document_title": return obs["core"].get(DC+"title")==g["document_identity"]["core_title"]
    if f=="footnotes": return sorted(obs["footnotes"], key=lambda x:x["id"]) == sorted(g["notes"], key=lambda x:x["id"])
    if f=="equation": return len(obs["equations"])==len(g["equations"])
    if f=="captions": return obs["captions"]==[x["caption"] for x in g["figure_caption_pairs"]]
    return False

if __name__=="__main__":
    records=[]; errors=[]
    for mp in sorted((BASE/"manifests").glob("B*.json")):
        rec=json.loads(mp.read_text(encoding="utf-8")); path=ROOT/rec["fixture_path"]; obs=inspect(path); ok=check(rec,obs); row={"variant_id":rec["variant_id"],"feature_family":rec["feature_family"],"source_sha256":sha(path),"manifest_sha256":sha(mp),"status":"PASS" if ok else "DISAGREEMENT","observed":obs}; records.append(row)
        if not ok: errors.append(rec["variant_id"])
    report={"variant_count":len(records),"passed":len(records)-len(errors),"disagreements":errors,"status":"PASS" if not errors else "STOP","records":records}
    REPORT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"); print(json.dumps({k:report[k] for k in ("variant_count","passed","disagreements","status")},indent=2)); raise SystemExit(1 if errors else 0)
