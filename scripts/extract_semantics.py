from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup
from pypdf import PdfReader

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
WP = "{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}"


def docx_extract(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        doc = ET.fromstring(z.read("word/document.xml"))
        core = ET.fromstring(z.read("docProps/core.xml"))
    title = next((x.text for x in core.iter() if x.tag.endswith("}title")), None)
    language = next((x.attrib.get(W + "val") for x in doc.iter(W + "lang") if x.attrib.get(W + "val")), None)
    headings, lists, inline_languages, alts = [], [], [], []
    for p in doc.iter(W + "p"):
        style = p.find("./" + W + "pPr/" + W + "pStyle")
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        if style is not None and (style.attrib.get(W + "val", "").lower().startswith("heading") or style.attrib.get(W + "val") == "Title"):
            style_id = style.attrib.get(W + "val")
            # Normalize authoring-tool style identifiers to the destination-neutral
            # heading vocabulary used by the fixture manifest and comparator.
            if style_id and style_id.lower().startswith("heading"):
                style_id = "H" + style_id[len("heading"):]
            headings.append(style_id)
        num = p.find("./" + W + "pPr/" + W + "numPr")
        if num is not None:
            lvl = num.find(W + "ilvl")
            lists.append(int(lvl.attrib.get(W + "val", "0")) if lvl is not None else 0)
        for lang in p.iter(W + "lang"):
            if text and lang.attrib.get(W + "val"):
                inline_languages.append({"text": text, "lang": lang.attrib[W + "val"]})
    for dp in doc.iter(WP + "docPr"):
        alts.append({"name": dp.attrib.get("name"), "alt": dp.attrib.get("descr", ""), "decorative": not bool(dp.attrib.get("descr", ""))})
    table_headers = []
    for table in doc.iter(W + "tbl"):
        rows = list(table.iter(W + "tr"))
        if rows and rows[0].find("./" + W + "trPr/" + W + "tblHeader") is not None:
            table_headers.append(True)
    return {"format": "docx", "title": title, "language": language, "headings": headings, "lists": lists,
            "inline_languages": inline_languages, "images": alts, "table_headers": table_headers}


def html_extract(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    headings = [tag.name.upper() for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    lists = []
    for item in soup.find_all("li"):
        parent = item.parent
        lists.append(len(parent.find_parents(["ul", "ol"])))
    images = []
    for img in soup.find_all("img"):
        images.append({"alt": img.get("alt", ""), "decorative": img.get("role") == "presentation" or img.get("aria-hidden") == "true" or img.get("alt", "") == ""})
    table_headers = [bool(t.find("th")) for t in soup.find_all("table")]
    inline_languages = [{"text": x.get_text(strip=True), "lang": x.get("lang")} for x in soup.find_all(lang=True)]
    return {"format": "html", "title": soup.title.get_text() if soup.title else None, "language": soup.html.get("lang") if soup.html else None,
            "headings": headings, "lists": lists, "inline_languages": inline_languages, "images": images, "table_headers": table_headers}


def pdf_extract(path: Path) -> dict:
    reader = PdfReader(str(path))
    root = reader.trailer.get("/Root", {})
    metadata = reader.metadata or {}
    struct = root.get("/StructTreeRoot") if hasattr(root, "get") else None
    lang = root.get("/Lang") if hasattr(root, "get") else None
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return {"format": "pdf", "title": metadata.get("/Title"), "language": str(lang) if lang else None,
            "headings": [], "lists": [], "inline_languages": [], "images": [], "table_headers": [],
            "tagged": struct is not None, "text_preview": text[:1000]}


def extract(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".docx": return docx_extract(path)
    if suffix in {".html", ".htm"}: return html_extract(path)
    if suffix == ".pdf": return pdf_extract(path)
    raise ValueError(f"Unsupported format: {path}")


if __name__ == "__main__":
    print(json.dumps(extract(Path(sys.argv[1])), indent=2))
