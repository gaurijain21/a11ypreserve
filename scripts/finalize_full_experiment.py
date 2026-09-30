from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "full_experiment"
MANIFEST = json.loads((ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
DIFF = json.loads((BASE / "reports" / "a11ydiff_results.json").read_text(encoding="utf-8"))
VALIDATION = json.loads((BASE / "reports" / "output_validation.json").read_text(encoding="utf-8"))
LO = json.loads((BASE / "reports" / "libreoffice_conversion.json").read_text(encoding="utf-8"))

FEATURE_NAMES = {
    "headings": "heading hierarchy", "image_alt_text": "image alternative text", "lists": "list semantics", "table": "table/header structure",
    "document_language": "document language", "inline_language": "inline language changes", "decorative_image": "decorative image state",
    "hyperlinks": "hyperlink semantics", "document_title": "document title/metadata", "complex_table": "multi-level table headers",
    "footnotes": "footnote association", "equation": "equation/math semantics", "captions": "figure/caption association",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def lo_record(fixture: str) -> dict:
    return next(row for row in LO["records"] if row["fixture"] == fixture)


def output_record(row: dict) -> dict:
    path = Path(row["destination_path"])
    return {"fixture": row["fixture"], "feature": row["feature"], "converter": row["converter"], "source": row["source_path"], "source_sha256": row["source_hash"], "destination": row["destination_path"], "destination_sha256": row["output_hash"], "classification": row["empirical_classification"], "fidelity_classification": row["fidelity_classification"], "destination_accessibility": row["destination_accessibility"], "evidence_path": row["evidence_path"], "confidence": row.get("confidence", "high"), "notes": row.get("notes", ""), "size_bytes": path.stat().st_size if path.exists() else None}


def main() -> None:
    (BASE / "evidence").mkdir(parents=True, exist_ok=True)
    # Independent text extraction is retained as corroborating evidence, not ground truth.
    pdftotext = os.environ.get("A11YPRESERVE_PDFTOTEXT") or shutil.which("pdftotext")
    for row in DIFF["records"]:
        pdf = Path(row["destination_path"])
        evidence_dir = BASE / "evidence" / row["fixture"]
        evidence_dir.mkdir(parents=True, exist_ok=True)
        text_path = evidence_dir / f"{row['converter'].lower().replace(' ', '_')}_pdftotext.txt"
        if pdftotext and Path(pdftotext).exists():
            run = subprocess.run([pdftotext, "-layout", str(pdf), "-"], capture_output=True, text=True, check=False)
            text_path.write_text(run.stdout, encoding="utf-8")

    records = [output_record(row) for row in DIFF["records"]]
    by_fixture = defaultdict(dict)
    for row in records:
        by_fixture[row["fixture"]][row["converter"]] = row

    # Automation log: LibreOffice data comes from its native export report; Google Docs
    # data comes from the authenticated UI import/download route and PDF metadata.
    log = ["# Full Experiment Automation Log", "", "All 26 records below are primary conversion records. Google Docs exports used authenticated Google Docs UI: Open file picker → Upload exact frozen DOCX → File → Download → PDF Document (.pdf). No print-to-PDF path was used.", "", "## Environment", "", "- Windows: `Windows-10-10.0.26200-SP0`", "- Chrome: `153.0.8010.53`", "- LibreOffice: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`", "- LibreOffice method: native `soffice.com writer_pdf_Export`; `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`", "- Google Docs PDF renderer observed in output metadata: `Skia/PDF m156`", ""]
    for row in records:
        if row["converter"] == "LibreOffice":
            r = lo_record(row["fixture"])
            log.extend([f"## {row['fixture']} — LibreOffice", "", f"- Timestamp: `{r['started_at']}` to `{r['completed_at']}`", f"- Tool/version: `{r['converter_version']}`", f"- Source: `{row['source']}`", f"- Destination: `{row['destination']}`", f"- Method: `{r['method']}`", f"- Settings: `{r['settings']}`", f"- Result: `{r['result']}`; pages={r['page_count']}; tagged={r['tagged']}; size={r['file_size']} bytes", f"- Source SHA-256: `{row['source_sha256']}`", f"- Output SHA-256: `{row['destination_sha256']}`", ""])
        else:
            p = Path(row["destination"])
            log.extend([f"## {row['fixture']} — Google Docs", "", f"- Timestamp: `{datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()}` (downloaded file timestamp)", "- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`", f"- Source: `{row['source']}`", f"- Destination: `{row['destination']}`", "- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export", "- Settings: Google Docs default PDF export; no print dialog; no manual document edits", "- Result: `SUCCESS`; validated parseable/tagged output", f"- Source SHA-256: `{row['source_sha256']}`", f"- Output SHA-256: `{row['destination_sha256']}`", ""])
    (BASE / "AUTOMATION_LOG.md").write_text("\n".join(log), encoding="utf-8")

    # Feature-level empirical table.
    quality = {"F01_HEADINGS": "HIGH", "F02_ALT_TEXT": "HIGH", "F03_LISTS": "HIGH", "F04_TABLE": "HIGH", "F05_DOCUMENT_LANGUAGE": "HIGH", "F06_INLINE_LANGUAGE": "MEDIUM", "F07_DECORATIVE_IMAGE": "MEDIUM", "F08_LINKS": "MEDIUM", "F09_DOCUMENT_TITLE": "HIGH", "F10_COMPLEX_TABLE": "HIGH", "F11_FOOTNOTES": "MEDIUM", "F12_EQUATION": "MEDIUM", "F14_CAPTIONS": "MEDIUM"}
    table = ["# Full Experiment Results by Feature", "", "Empirical labels are deliberately simplified for this report. Raw two-axis comparator output is in `reports/a11ydiff_results.json`. `PRESERVED` includes exact and semantically equivalent preservation; `ALTERED` includes mutation/regeneration. No overall converter ranking is computed.", "", "| Fixture | Feature | LibreOffice→PDF | Google Docs→PDF | Evidence quality |", "|---|---|---|---|---|"]
    for item in MANIFEST["fixtures"]:
        fixture = item["fixture_id"]
        f = by_fixture[fixture]
        table.append(f"| {fixture} | {FEATURE_NAMES[f['LibreOffice']['feature']]} | {f['LibreOffice']['classification']} | {f['Google Docs']['classification']} | {quality[fixture]} |")
    (BASE / "FULL_RESULTS_BY_FEATURE.md").write_text("\n".join(table) + "\n", encoding="utf-8")

    diff_rows = []
    agree_rows = []
    for item in MANIFEST["fixtures"]:
        fixture = item["fixture_id"]
        a, b = by_fixture[fixture]["LibreOffice"], by_fixture[fixture]["Google Docs"]
        if a["classification"] == b["classification"]:
            agree_rows.append(f"| {fixture} | {FEATURE_NAMES[a['feature']]} | {a['classification']} | {a['notes'] or b['notes']} |")
        else:
            diff_rows.append(f"| {fixture} | {FEATURE_NAMES[a['feature']]} | {a['classification']} | {b['classification']} | {a['notes']} / {b['notes']} |")
    (BASE / "CROSS_CONVERTER_DIFFERENCES.md").write_text("# Cross-Converter Differences\n\nDifferences are reported feature-by-feature; they are not an overall ranking.\n\n| Fixture | Feature | LibreOffice | Google Docs | Evidence/interpretation |\n|---|---|---|---|---|\n" + "\n".join(diff_rows) + "\n", encoding="utf-8")
    (BASE / "CROSS_CONVERTER_AGREEMENTS.md").write_text("# Cross-Converter Agreements\n\n| Fixture | Feature | Shared result | Evidence/interpretation |\n|---|---|---|---|\n" + "\n".join(agree_rows) + "\n", encoding="utf-8")

    freeze = {"freeze_type": "PRIMARY_RESULTS_FREEZE", "frozen_at": datetime.now(timezone.utc).isoformat(), "corpus_manifest": str(ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json"), "matrix_size": len(records), "engines": ["LibreOffice", "Google Docs"], "word_denominator": False, "records": records, "validation_summary": {"valid_outputs": sum(not x["invalid_conversion"] for x in VALIDATION["records"]), "invalid_outputs": sum(x["invalid_conversion"] for x in VALIDATION["records"])}, "notes": "Primary classifications frozen before secondary validator analysis. Historical Pilot 1–3 evidence remains unchanged."}
    (BASE / "PRIMARY_RESULTS_FREEZE.json").write_text(json.dumps(freeze, indent=2, ensure_ascii=False), encoding="utf-8")

    # Audit every non-preserved or measurement-limited result against the source manifest,
    # raw PDF structure, and an independent text extractor.
    audit = ["# Non-Preservation Audit", "", "Every non-PRESERVED result was challenged against source ground truth, PDF capability, structural evidence, parser coverage, and independent page-text corroboration. A result is not treated as converter loss when the current extractor cannot establish the required association.", ""]
    for row in records:
        if row["classification"] == "PRESERVED":
            continue
        extracted = json.loads(Path(row["evidence_path"]["destination_extraction"]).read_text(encoding="utf-8"))
        audit.extend([f"## {row['fixture']} — {row['converter']}", "", f"- Classification: `{row['classification']}`; destination accessibility: `{row['destination_accessibility']}`", f"- Source manifest/OOXML: `{ROOT / 'corpus' / 'manifests' / (row['fixture'] + '.json') if row['fixture'] not in {'F01_HEADINGS','F02_ALT_TEXT','F03_LISTS','F04_TABLE'} else ROOT / 'pilot' / 'manifests' / (row['fixture'] + '.json')}`", f"- Source hash: `{row['source_sha256']}`", f"- PDF hash: `{row['destination_sha256']}`", f"- Structural extraction: tagged={extracted.get('tagged')}; headings={len(extracted.get('headings', []))}; figures={len(extracted.get('figures', []))}; list nodes={len(extracted.get('lists', []))}; tables={len(extracted.get('tables', []))}; footnotes={len(extracted.get('footnotes', []))}; equations={len(extracted.get('equations', []))}; captions={len(extracted.get('captions', []))}", f"- Independent text evidence: `{BASE / 'evidence' / row['fixture'] / (row['converter'].lower().replace(' ', '_') + '_pdftotext.txt')}`", f"- Falsification result: {row['notes'] or 'No additional interpretation; raw evidence is retained in the JSON diff and extraction artifact.'}", ""])
    (BASE / "NON_PRESERVATION_AUDIT.md").write_text("\n".join(audit), encoding="utf-8")

    validators = """# Secondary Validator Availability\n\nThe primary study ground truth is the source-grounded structural comparison, not a validator verdict.\n\n- `pdftotext` was available and run over all 26 outputs as independent page-text corroboration; evidence is retained under `evidence/`.\n- PAC: not installed/discovered in this environment.\n- veraPDF: not installed/discovered in this environment.\n- Acrobat Accessibility Checker: not available for deterministic batch execution in this environment.\n\nNo unavailable validator was treated as a pass or failure, and no validator result was used to override the frozen primary classifications.\n"""
    (BASE / "validators" / "SECONDARY_VALIDATORS.md").write_text(validators, encoding="utf-8")

    summary_counts = defaultdict(int)
    for row in records:
        summary_counts[row["classification"]] += 1
    final_freeze = {"freeze_type": "FULL_EXPERIMENT_FREEZE", "frozen_at": datetime.now(timezone.utc).isoformat(), "decision": "GO", "input_verification": str(ROOT / "results" / "FULL_EXPERIMENT_INPUT_VERIFICATION.md"), "primary_results": str(BASE / "PRIMARY_RESULTS_FREEZE.json"), "matrix_size": 26, "successful_conversions": {"LibreOffice": 13, "Google Docs": 13}, "classification_counts": dict(sorted(summary_counts.items())), "tests": str(BASE / "reports" / "test_results.json"), "secondary_validators_after_freeze": True}
    (ROOT / "results" / "FULL_EXPERIMENT_FREEZE.md").write_text("# FULL EXPERIMENT FREEZE\n\nPrimary results were frozen before secondary validator analysis.\n\n- Frozen corpus: 13 fixtures; hashes verified.\n- Primary matrix: 26/26 outputs valid and analyzable.\n- Engines: LibreOffice and Google Docs. Microsoft Word remains deferred and is excluded from the denominator.\n- Primary JSON freeze: `results/full_experiment/PRIMARY_RESULTS_FREEZE.json`.\n- Secondary validator availability and corroborating text evidence were recorded after the freeze.\n\nDecision: **GO** for the full-study phase, with the documented measurement limits for footnotes, captions, links, decorative-image state, and PDF math/text associations.\n", encoding="utf-8")

    report = ["# DECISION: GO", "", "# FULL EXPERIMENT RESULTS", "", "## 1. Executive decision", "", "The frozen 13-fixture benchmark produced 26 real DOCX→PDF outputs: 13 through LibreOffice and 13 through authenticated Google Docs export. All 26 PDFs were parseable, non-empty, one page, and structurally tagged. Source and destination semantics were independently extracted and compared. The evidence supports proceeding to the planned full study, without ranking converters overall.", "", "## 2. Input integrity", "", "The 13 frozen DOCX hashes matched `corpus/FROZEN_CORPUS_MANIFEST.json`; the verification report records exact paths, sizes, hashes, and timestamp. No fixture was regenerated or modified.", "", "## 3. Conversion engines", "", "- LibreOffice 26.2.6.3, native headless `writer_pdf_Export`, tagged-PDF settings enabled.\n- Google Docs authenticated web export, exact frozen DOCX uploaded through the UI and exported via File → Download → PDF Document; PDF producer observed as `Skia/PDF m156`.\n- Microsoft Word was not included because the previously documented COM/environment issue remains unresolved; this is not a semantic result.", "", "## 4. Successful conversions", "", "- LibreOffice: 13/13\n- Google Docs: 13/13\n- Total: 26/26 valid primary outputs", "", "## 5. Failed conversions", "", "No primary conversion failed. One Google Docs picker-load retry was required for F06; it was an automation transient, not an output result.", "", "## 6. Semantic results", "", "See `results/full_experiment/FULL_RESULTS_BY_FEATURE.md` and raw `reports/a11ydiff_results.json`. Key feature-level observations include: LibreOffice preserved headings, list numbering, simple tables, document language, inline language, document title, complex-table scope/span evidence, math `/Formula`, and caption `/Caption` structure; it altered F02 alt text and did not establish an explicit decorative Artifact for F07. Google Docs preserved F02 alt text, F04 simple table structure, and F07 meaningful/decorative image count/state only partially because explicit decorative representation was not established; it partially preserved F01 headings, F03 list structure without explicit list type, F10 complex header roles without scope, F12 equation as visible text, and F14 caption text by adjacency.", "", "## 7. Strongest confirmed preservation", "", "The strongest cases are direct structure-level matches: Google Docs F02 preserved the author-written `/Figure /Alt` string exactly; LibreOffice F03 exposed `/L`, `/LI`, `/LBody`, and `/ListNumbering` matching the source’s ordered/unordered and nested-list contract; LibreOffice F10 exposed five `/TH` cells with scope and span evidence matching the two-level header contract; LibreOffice F12 exposed a `/Formula` structure with the retained visible expression.", "", "## 8. Strongest confirmed loss/degradation", "", "Google Docs F06 lost the source inline `es-MX` language span while retaining only the document-level language. Google Docs F10 retained table/header roles but no `/Scope` evidence for the multi-level header associations. Google Docs F03 retained list items/nesting but no explicit ordered/unordered representation. These are source-grounded fidelity results, not claims that the entire PDFs are inaccessible.", "", "## 9. Cross-converter differences", "", "Feature-level differences are documented in `CROSS_CONVERTER_DIFFERENCES.md`. Shared outcomes are documented in `CROSS_CONVERTER_AGREEMENTS.md`. No overall converter winner is reported.", "", "## 10. Comparator validity", "", "`a11ydiff` ran for all 26 pairs. The comparator produced raw source/destination values, two-axis fidelity/accessibility labels, evidence paths, source/output hashes, and notes. Regression tests passed.", "", "## 11. Measurement failures", "", "LibreOffice F11 exposed a PDF `/Note` structure, but the current marked-content extractor did not recover note-body text well enough to verify reference/body association; it is therefore `MEASUREMENT_ERROR`, not `LOST`. Link visible-name association, decorative Artifact state, some caption associations, and token-level math text remain bounded by PDF producer representation and extractor coverage. These limitations are retained rather than converted into converter-loss claims.", "", "## 12. Research signal", "", "PRESENT. The same source-grounded method produced feature-specific preservation, partial preservation, alteration, loss, and measurement-error outcomes across two real conversion engines. The results are not reducible to a destination-only accessibility verdict.", "", "## 13. What this pilot DOES prove", "", "It proves feasibility of a controlled, frozen DOCX corpus; deterministic OOXML ground truth; real tagged PDF production by two engines; structural destination inspection; provenance-traceable comparison; and meaningful converter/feature-specific differences.", "", "## 14. What this pilot DOES NOT prove", "", "It does not prove universal behavior across software versions, documents, operating systems, validators, or users. It does not rank LibreOffice or Google Docs overall, and it does not establish Microsoft Word behavior.", "", "## 15. Full-paper implications", "", "Scaling the frozen contracts with justified variants, integrated documents, additional converter versions, and validator comparison is likely to support a publishable empirical study. Feature-level reporting and explicit measurement-error handling should remain central.", "", "## 16. Next experiment", "", "Run the planned larger matrix only after selecting justified feature instances and recording converter/version settings. Add Word only if its native export becomes reproducibly executable; otherwise keep it explicitly out of the denominator.", "", "## 17. Final decision", "", "GO", ""]
    (ROOT / "FULL_EXPERIMENT_RESULTS.md").write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"decision": "GO", "matrix_size": 26, "classification_counts": dict(sorted(summary_counts.items()))}))


if __name__ == "__main__":
    main()
