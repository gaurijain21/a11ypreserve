from __future__ import annotations

import base64
import json
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def set_run_language(run, language: str) -> None:
    rpr = run._r.get_or_add_rPr()
    lang = rpr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rpr.append(lang)
    lang.set(qn("w:val"), language)


def set_image_alt(inline, description: str) -> None:
    inline._inline.docPr.set("descr", description)


def set_list_level(paragraph, level: int) -> None:
    ppr = paragraph._p.get_or_add_pPr()
    num_pr = ppr.find(qn("w:numPr"))
    if num_pr is None:
        num_pr = OxmlElement("w:numPr")
        ppr.append(num_pr)
    ilvl = num_pr.find(qn("w:ilvl"))
    if ilvl is None:
        ilvl = OxmlElement("w:ilvl")
        num_pr.append(ilvl)
    ilvl.set(qn("w:val"), str(level))
    num_id = num_pr.find(qn("w:numId"))
    if num_id is None:
        num_id = OxmlElement("w:numId")
        num_pr.append(num_id)
    num_id.set(qn("w:val"), "1")


def add_lang_paragraph(document: Document, text: str, language: str):
    paragraph = document.add_paragraph()
    run = paragraph.add_run(text)
    set_run_language(run, language)
    return paragraph


def make_docx(path: Path) -> None:
    document = Document()
    document.core_properties.title = "A11yPreserve Golden Fixture"
    document.core_properties.language = "en-US"

    title = document.add_paragraph(style="Title")
    set_run_language(title.add_run("A11yPreserve Golden Fixture"), "en-US")
    heading = document.add_paragraph("Semantic Features", style="Heading 1")
    set_run_language(heading.runs[0], "en-US")
    add_lang_paragraph(document, "This paragraph contains a Spanish phrase.", "en-US")
    add_lang_paragraph(document, "Información pública", "es-MX")

    for text, level in (("Nested list item one", 0), ("Nested list item one.a", 1), ("Nested list item two", 0)):
        paragraph = document.add_paragraph(text, style="List Bullet")
        set_run_language(paragraph.runs[0], "en-US")
        set_list_level(paragraph, level)

    image_path = CORPUS / "fixture.png"
    image_path.write_bytes(PNG_1X1)
    first = document.add_picture(str(image_path), width=Inches(1))
    set_image_alt(first, "Bar chart showing enrollment increasing from 2021 to 2025")
    second = document.add_picture(str(image_path), width=Inches(1))
    set_image_alt(second, "")

    table = document.add_table(rows=2, cols=2)
    table.style = "Table Grid"
    for cell, value in zip(table.rows[0].cells, ("Year", "Enrollment")):
        cell.text = value
    for cell, value in zip(table.rows[1].cells, ("2021", "500")):
        cell.text = value
    header = table.rows[0]._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    header.append(tbl_header)
    document.save(path)


def make_html(path: Path) -> None:
    html = '''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><title>A11yPreserve Golden Fixture</title></head>
<body>
<h1>A11yPreserve Golden Fixture</h1><h2>Semantic Features</h2>
<p>This paragraph contains a Spanish phrase.</p><p lang="es-MX">Información pública</p>
<ul><li>Nested list item one<ul><li>Nested list item one.a</li></ul></li><li>Nested list item two</li></ul>
<figure><img src="fixture.png" alt="Bar chart showing enrollment increasing from 2021 to 2025"><figcaption>Enrollment</figcaption></figure>
<img src="decorative.png" alt="" role="presentation" aria-hidden="true">
<table><thead><tr><th scope="col">Year</th><th scope="col">Enrollment</th></tr></thead><tbody><tr><td>2021</td><td>500</td></tr></tbody></table>
</body></html>'''
    path.write_text(html, encoding="utf-8")
    (path.parent / "fixture.png").write_bytes(PNG_1X1)
    (path.parent / "decorative.png").write_bytes(PNG_1X1)


def main() -> None:
    CORPUS.mkdir(exist_ok=True)
    make_docx(CORPUS / "G01_semantic_fixture.docx")
    make_html(CORPUS / "G01_semantic_fixture.html")
    manifest = {
        "fixture": "G01_semantic_fixture",
        "features": {
            "document_title": "A11yPreserve Golden Fixture",
            "document_language": "en-US",
            "headings": ["H1", "H2"],
            "image_1.alt": "Bar chart showing enrollment increasing from 2021 to 2025",
            "image_1.decorative": False,
            "image_2.decorative": True,
            "inline_language": {"Información pública": "es-MX"},
            "list_depths": [0, 1, 0],
            "table_header_scope": ["col", "col"],
        },
        "verification": "Ground truth authored independently of extractors; OOXML and HTML source inspected by hand.",
    }
    (CORPUS / "G01_semantic_fixture.manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
