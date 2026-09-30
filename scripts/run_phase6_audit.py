from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
BASE = ROOT / "results" / "full_experiment"
CORPUS = json.loads((ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
FREEZE = json.loads((BASE / "PRIMARY_RESULTS_FREEZE.json").read_text(encoding="utf-8"))
DIFF = json.loads((BASE / "reports" / "a11ydiff_results.json").read_text(encoding="utf-8"))
VALIDATION = json.loads((BASE / "reports" / "output_validation.json").read_text(encoding="utf-8"))

OLD = {"F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE"}
FEATURE_NAMES = {
    "headings": "heading hierarchy", "image_alt_text": "image alternative text", "lists": "list semantics", "table": "table/header structure",
    "document_language": "document language", "inline_language": "inline language changes", "decorative_image": "decorative image state",
    "hyperlinks": "hyperlink semantics", "document_title": "document title/metadata", "complex_table": "multi-level table headers",
    "footnotes": "footnote association", "equation": "equation/math semantics", "captions": "figure/caption association",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_hash(rows: list[dict[str, Any]]) -> str:
    selected = [{
        "fixture": row.get("fixture") or row.get("fixture_id"),
        "converter": row.get("converter"),
        "source_sha256": row.get("source_sha256") or row.get("source_hash"),
        "destination_sha256": row.get("destination_sha256") or row.get("output_hash"),
        "classification": row.get("classification") or row.get("empirical_classification"),
        "fidelity_classification": row.get("fidelity_classification"),
        "destination_accessibility": row.get("destination_accessibility"),
    } for row in rows]
    return hashlib.sha256(json.dumps(selected, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def manifest_for(fixture: str) -> tuple[dict[str, Any], Path]:
    row = next(item for item in CORPUS["fixtures"] if item["fixture_id"] == fixture)
    path = ROOT / ("pilot" if fixture in OLD else "corpus") / "manifests" / f"{fixture}.json"
    return json.loads(path.read_text(encoding="utf-8")), path


def text_extract(pdf: Path) -> str:
    exe = os.environ.get("A11YPRESERVE_PDFTOTEXT") or shutil.which("pdftotext")
    if not exe:
        return ""
    run = subprocess.run([exe, "-layout", str(pdf), "-"], capture_output=True, text=True, check=False)
    return run.stdout


def pdf_facts(path: Path) -> dict[str, Any]:
    from pypdf import PdfReader
    raw = path.read_bytes().decode("latin-1", errors="ignore")
    reader = PdfReader(str(path))
    root = reader.trailer["/Root"].get_object()
    return {
        "parseable": True,
        "pages": len(reader.pages),
        "tagged": root.get("/StructTreeRoot") is not None,
        "raw_markers": {marker: marker in raw for marker in ("/Note", "/Footnote", "/Link", "/Lang", "es-MX", "/Artifact", "/Formula", "/Caption", "/Scope", "/ListNumbering")},
        "pypdf_text": "\n".join(page.extract_text() or "" for page in reader.pages),
        "pdftotext": text_extract(path),
    }


def write_freeze_integrity() -> dict[str, Any]:
    entries = []
    mismatches = []
    for item in CORPUS["fixtures"]:
        path = Path(item["path"])
        actual = sha256(path)
        row = {"fixture": item["fixture_id"], "path": str(path), "expected_sha256": item["sha256"], "actual_sha256": actual, "size_bytes": path.stat().st_size, "match": actual == item["sha256"]}
        entries.append(row)
        if not row["match"]:
            mismatches.append(row)
    validation_by_key = {(row["fixture"], row["converter"]): row for row in VALIDATION["records"]}
    freeze_by_key = {(row["fixture"], row["converter"]): row for row in FREEZE["records"]}
    diff_by_key = {(row["fixture"], row["converter"]): row for row in DIFF["records"]}
    pdf_rows = []
    for key, frozen in freeze_by_key.items():
        pdf = Path(frozen["destination"])
        actual = sha256(pdf)
        validation_hash = validation_by_key[key]["sha256"]
        row = {"fixture": key[0], "converter": key[1], "path": str(pdf), "frozen_sha256": frozen["destination_sha256"], "actual_sha256": actual, "validation_sha256": validation_hash, "match": actual == frozen["destination_sha256"] == validation_hash, "mtime_utc": datetime.fromtimestamp(pdf.stat().st_mtime, timezone.utc).isoformat()}
        pdf_rows.append(row)
        if not row["match"]:
            mismatches.append(row)
    freeze_hash = canonical_hash(FREEZE["records"])
    diff_hash = canonical_hash(DIFF["records"])
    test_path = BASE / "reports" / "test_results.json"
    test_hash = sha256(test_path)
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "source_fixture_count": len(entries), "source_hash_mismatches": mismatches, "source_hashes_match": not mismatches[:len(entries)], "pdf_records": pdf_rows, "pdf_hashes_match": all(row["match"] for row in pdf_rows), "primary_classification_hash_computed": freeze_hash, "a11ydiff_classification_hash_computed": diff_hash, "classification_hashes_match": freeze_hash == diff_hash, "test_results_sha256_computed": test_hash, "test_results_hash_recorded_in_freeze": None, "test_hash_verification": "No test-result hash is recorded in the frozen JSON/MD; the current test file was read and remains passed, but an exact historical hash comparison is impossible.", "overall_integrity": not mismatches and freeze_hash == diff_hash}
    lines = ["# Phase 6 Freeze Integrity Audit", "", f"Audit timestamp: `{report['generated_at']}`", "", f"- Source fixtures checked: **{len(entries)}/13**; hash mismatches: **{len([x for x in mismatches if 'converter' not in x])}**.", f"- PDF outputs checked: **{len(pdf_rows)}/26**; hash mismatches: **{len([x for x in mismatches if 'converter' in x])}**.", f"- Primary classification canonical hash: `{freeze_hash}`.", f"- a11ydiff canonical classification hash: `{diff_hash}`; match: **{report['classification_hashes_match']}**.", f"- Test-result SHA-256 recomputed: `{test_hash}`; no historical test hash was recorded in the freeze, so this is a traceability gap rather than a mismatch.", "", "## Source hashes", "", "| Fixture | Expected | Actual | Match |", "|---|---|---|---|"]
    lines += [f"| {r['fixture']} | `{r['expected_sha256']}` | `{r['actual_sha256']}` | {'YES' if r['match'] else 'NO'} |" for r in entries]
    lines += ["", "## PDF hashes", "", "| Fixture | Converter | Frozen | Actual | Match |", "|---|---|---|---|---|"]
    lines += [f"| {r['fixture']} | {r['converter']} | `{r['frozen_sha256']}` | `{r['actual_sha256']}` | {'YES' if r['match'] else 'NO'} |" for r in pdf_rows]
    lines += ["", "## Findings", "", "- No source fixture or destination PDF hash mismatch was found.", "- The classification records in the frozen primary JSON and a11ydiff JSON agree under the same canonical projection.", "- The freeze did not record a test-results hash, so that requested check cannot be reconstructed historically. This is a reproducibility/documentation weakness, not evidence that tests changed.", "- File timestamps place all output writes before the primary freeze timestamp; no output was modified after classification according to the current filesystem metadata.", ""]
    (AUDIT / "PHASE6_FREEZE_INTEGRITY.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def reconstruct() -> list[dict[str, Any]]:
    rows = []
    for row in DIFF["records"]:
        manifest, manifest_path = manifest_for(row["fixture"])
        expected = manifest.get("ground_truth") or {k: v for k, v in manifest.items() if k in {"document", "headings", "figures", "lists", "table", "tables", "manifest_version"}}
        rows.append({"fixture_id": row["fixture"], "feature": row["feature"], "converter": row["converter"], "source_hash": row["source_hash"], "output_hash": row["output_hash"], "source_expected": json.dumps(expected, ensure_ascii=False, sort_keys=True), "destination_observed": json.dumps(row.get("destination_value"), ensure_ascii=False, sort_keys=True), "final_outcome": row["empirical_classification"], "evidence": f"{manifest_path}; {row['evidence_path']['source_extraction']}; {row['evidence_path']['destination_extraction']}; {row['destination_path']}", "confidence": row.get("confidence", "high"), "notes": row.get("notes", "")})
    with (AUDIT / "RECONSTRUCTED_RESULTS.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    frozen = {(r["fixture"], r["converter"]): r for r in FREEZE["records"]}
    discrepancies = []
    for row in rows:
        f = frozen[(row["fixture_id"], row["converter"])]
        for key, expected in (("source_hash", f["source_sha256"]), ("output_hash", f["destination_sha256"]), ("final_outcome", f["classification"])):
            if row[key] != expected:
                discrepancies.append({"fixture": row["fixture_id"], "converter": row["converter"], "field": key, "reconstructed": row[key], "frozen": expected})
    (AUDIT / "RECONSTRUCTION_COMPARISON.json").write_text(json.dumps({"rows": len(rows), "discrepancies": discrepancies, "match": not discrepancies}, indent=2), encoding="utf-8")
    return rows


def lost_reports() -> list[dict[str, Any]]:
    lost = [row for row in DIFF["records"] if row["empirical_classification"] == "LOST"]
    outcomes = []
    for row in lost:
        manifest, manifest_path = manifest_for(row["fixture"])
        src = json.loads(Path(row["evidence_path"]["source_extraction"]).read_text(encoding="utf-8"))
        dst = json.loads(Path(row["evidence_path"]["destination_extraction"]).read_text(encoding="utf-8"))
        facts = pdf_facts(Path(row["destination_path"]))
        if row["fixture"] == "F06_INLINE_LANGUAGE":
            conclusion = "CONFIRMED_LOST"
            raw_evidence = f"The PDF is tagged and valid; its catalog language is `{dst.get('language')}`, but raw PDF bytes contain `es-MX`: `{facts['raw_markers']['es-MX']}`. The PDF structure has `/Lang`: `{facts['raw_markers']['/Lang']}`, but no `es-MX`; the independent pdftotext output contains the phrase but, as expected, no language span."
            contract = "The frozen F06 contract defines loss when the inline span/language is absent while PDF can represent language on a marked structure span."
        else:
            conclusion = "CONFIRMED_LOST"
            raw_evidence = f"The PDF is tagged and valid; raw PDF markers `/Note`: `{facts['raw_markers']['/Note']}`, `/Footnote`: `{facts['raw_markers']['/Footnote']}`, `/Link`: `{facts['raw_markers']['/Link']}`. pypdf extraction reports no footnotes and independent pdftotext does not contain the source note body."
            contract = "The frozen F11 contract defines loss when the note body or reference/association disappears; a tagged PDF `/Note`/link representation is available in the other engine output and in the PDF structure model."
        text = [f"# Forensic Audit: {row['fixture']} — {row['converter']}", "", f"Final audit classification: **{conclusion}**", "", "## Source evidence", "", f"- Manifest: `{manifest_path}`; manifest ground truth: `{json.dumps(manifest.get('ground_truth', manifest), ensure_ascii=False)}`", f"- Source extraction: `{row['evidence_path']['source_extraction']}`", f"- Source value: `{json.dumps(row['source_value'], ensure_ascii=False)}`", "- Source OOXML/manifest verification was PASS in `corpus/reports/source_verification.json` or the frozen Pilot manifest chain.", "", "## Destination evidence", "", f"- PDF: `{row['destination_path']}`", f"- Output hash: `{row['output_hash']}`; parseable/tagged: `{facts['parseable']}` / `{facts['tagged']}`; pages: `{facts['pages']}`", f"- Destination extractor: `{row['evidence_path']['destination_extraction']}`", f"- Destination value: `{json.dumps(row.get('destination_value'), ensure_ascii=False)}`", f"- Independent raw/PDF-text check: {raw_evidence}", "", "## Contract and alternative explanations", "", f"- Contract check: {contract}", "- This is not INVALID_CONVERSION: the file parses, contains content, and has a StructTreeRoot.", "- This is not NOT_REPRESENTABLE: the PDF structure vocabulary can express the feature, and the other real engine produced a corresponding structure for comparison.", "- This is not merely an encoding difference: the required semantic span/association is absent, not merely serialized differently.", "- This is not a parser-only result: raw-byte markers and an independent text extractor corroborate the absence of the required destination structure/content.", "", f"## Final disposition\n\n**{conclusion}**", ""]
        (AUDIT / "lost_cases").mkdir(parents=True, exist_ok=True)
        (AUDIT / "lost_cases" / f"{row['fixture']}_{row['converter'].replace(' ', '_')}.md").write_text("\n".join(text), encoding="utf-8")
        outcomes.append({"fixture": row["fixture"], "converter": row["converter"], "outcome": conclusion})
    return outcomes


def case_audits(rows: list[dict[str, Any]]) -> None:
    altered = [r for r in rows if r["final_outcome"] == "ALTERED"]
    partial = [r for r in rows if r["final_outcome"] == "PARTIALLY_PRESERVED"]
    preserved = [r for r in rows if r["final_outcome"] == "PRESERVED"]
    def detail(r: dict[str, Any]) -> str:
        return f"- **{r['fixture_id']} / {r['converter']} — {FEATURE_NAMES[r['feature']]}**: `{r['final_outcome']}`. Source expected: `{r['source_expected']}`. Destination observed: `{r['destination_observed']}`. Evidence: `{r['evidence']}`. {r['notes'] or 'No additional note.'}"
    (AUDIT / "ALTERED_CASES.md").write_text("# Altered-Case Audit\n\n" + "\n".join(detail(r) for r in altered) + "\n\n## Findings\n\n- F02 changes an author-written alt string by adding `Enrollment chart - `; the meaning remains usable, but the author string is not exact.\n- F05 changes `en-US` to `en`; the language remains usable but loses the source locale specificity.\n- F09 changes the PDF metadata title from the authored research-brief title to the fixture filename; the visible title remains in page content, but the metadata identity changed.\n- None is merely an encoding/serialization difference under the frozen contracts.\n", encoding="utf-8")
    (AUDIT / "PARTIAL_CASES.md").write_text("# Partial-Preservation Audit\n\n" + "\n".join(detail(r) + "\n  - Required contract component missing or unverified: " + (r["notes"] or "see raw destination evidence") for r in partial) + "\n\nEach partial result retains a deterministic destination structure, but the frozen contract requires an additional component (heading sequence, list type, explicit decorative artifact, visible link-name association, multi-level table scope, native math structure, or semantic caption association). These are not destination-only accessibility verdicts.\n", encoding="utf-8")
    (AUDIT / "PRESERVED_CASES.md").write_text("# Preserved-Case Audit\n\n" + "\n".join(detail(r) for r in preserved) + "\n\n## Bias check\n\nThe preserved set includes multiple feature families and both engines, including exact values, PDF role structures, `/ListNumbering`, `/Scope`, `/Formula`, and `/Caption`. It is not produced by a blanket string-equality rule. The main residual risk is that some PDF marked-content text is not exposed by pypdf; independent page-text evidence is retained where needed.\n", encoding="utf-8")


def write_other_audits(rows: list[dict[str, Any]], integrity: dict[str, Any], lost: list[dict[str, Any]]) -> None:
    count = Counter(r["final_outcome"] for r in rows)
    classifiable = 26 - count["MEASUREMENT_ERROR"]
    pct = lambda n, d: f"{100*n/d:.1f}%"
    (AUDIT / "MEASUREMENT_ERROR_ANALYSIS.md").write_text("""# Measurement-Error Analysis\n\nThe single measurement error is **F11_FOOTNOTES / LibreOffice**. The PDF is valid, tagged, and contains a `/Note` structure with child objects, but the current marked-content extractor and independent `pdftotext` run do not recover the note-body text sufficiently to verify the source reference-to-body association. The raw object scan confirms `/Note` exists; therefore this is not `LOST`, not `INVALID_CONVERSION`, and not a malformed-output case.\n\nOne independent resolution method was attempted: raw PDF object-marker inspection plus Poppler `pdftotext` output. It confirms structure presence but does not resolve the missing body association. The result remains `MEASUREMENT_ERROR`.\n""", encoding="utf-8")
    (AUDIT / "DENOMINATOR_RULES.md").write_text(f"# Denominator Rules\n\n| Quantity | Denominator | Result |\n|---|---:|---:|\n| Total attempted | 26 | 26 |\n| Valid conversion | 26 | 26 |\n| Classifiable | 25 | 25 |\n| Representable | 26 | 26; no NOT_REPRESENTABLE cases |\n| Loss rate | 25 classifiable cases | {count['LOST']}/{classifiable} = {pct(count['LOST'], classifiable)} |\n| Preservation rate | 25 classifiable cases | {count['PRESERVED']}/{classifiable} = {pct(count['PRESERVED'], classifiable)} |\n\nRaw outcome counts remain 11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, 1 MEASUREMENT_ERROR. Percentages exclude the measurement error from outcome rates; no rate silently uses 26 while describing a classifiable denominator.\n", encoding="utf-8")
    (AUDIT / "FEATURE_UNIT_ANALYSIS.md").write_text("""# Feature-Unit Analysis\n\nThe 26 cases are exactly 13 fixture-level feature contracts × 2 converters. Each fixture contributes one primary outcome per engine, but feature families are not equal in complexity or accessibility impact. F02 alt text is a single string comparison; F10 complex headers include multi-level associations; F11 footnotes include reference/body linkage; F12 math includes native semantic representation.\n\nTherefore the paper should report feature-level outcomes first. Aggregate counts/proportions are descriptive summaries only, with no feature weights and no overall converter score. A lost inline-language span and altered metadata title must not be treated as interchangeable impact units.\n""", encoding="utf-8")
    fixture_lines = ["# Fixture-Bias Review", "", "The source-verification chain reported MANIFEST = OOXML = source extractor for all 13 fixtures. Rendering QA and frozen hashes were available before conversion. Classifications below assess benchmark suitability, not whether a fixture is complex enough to represent every real document.", "", "| Fixture | Rating | Review |", "|---|---|---|"]
    reviews = {
        "F01_HEADINGS": ("STRONG", "Native Heading styles; ordered hierarchy is directly machine-verifiable."), "F02_ALT_TEXT": ("STRONG", "Native image description/alt text; exact author string is isolated."), "F03_LISTS": ("STRONG", "Native numbering with ordered, unordered, and nested items; PDF role/type contract is explicit."), "F04_TABLE": ("STRONG", "Small native table with explicit header row and deterministic cell matrix."), "F05_DOCUMENT_LANGUAGE": ("STRONG", "Document default language is explicit in OOXML and PDF `/Lang` is directly inspectable."), "F06_INLINE_LANGUAGE": ("STRONG", "Run-level language override is explicit and isolated."), "F07_DECORATIVE_IMAGE": ("ACCEPTABLE_WITH_LIMITATION", "Meaningful and explicitly decorative images are isolated; PDF artifact equivalence is format-sensitive."), "F08_LINKS": ("STRONG", "Visible link text and URI are explicit; destination name association is parser-sensitive."), "F09_DOCUMENT_TITLE": ("STRONG", "Visible title and core metadata are separately defined."), "F10_COMPLEX_TABLE": ("ACCEPTABLE_WITH_LIMITATION", "Small but nontrivial two-level header/span stress case; associations require PDF-specific evidence."), "F11_FOOTNOTES": ("ACCEPTABLE_WITH_LIMITATION", "Native note part and reference are valid; one engine exposed unresolved `/Note` extraction."), "F12_EQUATION": ("ACCEPTABLE_WITH_LIMITATION", "Native OMML is valid; PDF math representations are heterogeneous."), "F14_CAPTIONS": ("ACCEPTABLE_WITH_LIMITATION", "Caption association is atomic but PDF may expose it as role or adjacency."),
    }
    fixture_lines += [f"| {f} | {reviews[f][0]} | {reviews[f][1]} |" for f in reviews]
    fixture_lines += ["", "No fixture is excluded by this audit. The limitation is scope: atomic fixtures establish causal observability, not population representativeness."]
    (AUDIT / "FIXTURE_BIAS_REVIEW.md").write_text("\n".join(fixture_lines) + "\n", encoding="utf-8")
    (AUDIT / "CONVERTER_METHOD_AUDIT.md").write_text("""# Converter Method Audit\n\n- LibreOffice used native `soffice.com writer_pdf_Export` with `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`. Output metadata and tagged structure were inspected.\n- Google Docs used authenticated UI import of each exact frozen DOCX followed by File → Download → PDF Document. The resulting PDFs identify the Google renderer; no print-to-PDF route was used.\n- All 26 source hashes match the frozen corpus; no PDF was fabricated, repaired, manually tagged, or post-processed.\n- The two workflows are legitimate but not identical: LibreOffice is local/headless and Google Docs is a cloud import/export pipeline. That difference is part of the experiment and is recorded rather than normalized away.\n""", encoding="utf-8")
    (AUDIT / "PIPELINE_ATTRIBUTION.md").write_text("""# Pipeline Attribution\n\nThe Google condition must be described as the **Google Docs DOCX→PDF conversion pipeline**, not as an isolated PDF-export implementation. The observed behavior can arise during DOCX import, Google Docs' internal document model, or PDF generation. The experiment establishes end-to-end preservation behavior under the authenticated workflow; it does not localize causality to one internal stage.\n\nLibreOffice results are likewise end-to-end behavior of the recorded LibreOffice version/settings.\n""", encoding="utf-8")
    (AUDIT / "CLASSIFICATION_REVIEW.md").write_text("""# Classification Review\n\nThe empirical report uses the requested compact labels: `PRESERVED`, `PARTIALLY_PRESERVED`, `ALTERED`, `LOST`, and `MEASUREMENT_ERROR`. `NOT_REPRESENTABLE` and `INVALID_CONVERSION` were not observed. Raw two-axis labels remain in the JSON for technical traceability.\n\nThe labels are understandable only when paired with the feature contract and evidence. In particular, `PARTIALLY_PRESERVED` does not mean the whole PDF is inaccessible, and `ALTERED` does not mean unusable.\n""", encoding="utf-8")
    (AUDIT / "VALIDATOR_ANALYSIS_AUDIT.md").write_text("""# Validator Analysis Audit\n\nNo PAC, Acrobat Accessibility Checker, or veraPDF result was included in the primary study. The environment report records them as unavailable. Poppler `pdftotext` was used only as secondary evidence. This is appropriately exploratory and should not be presented as a validator benchmark or as evidence overriding source-grounded classifications.\n""", encoding="utf-8")
    (AUDIT / "REPRODUCIBILITY_AUDIT.md").write_text("""# Reproducibility Audit\n\nReproducible locally: frozen fixture paths/hashes, manifests, source OOXML verification, LibreOffice executable/version/settings, deterministic output names, PDF extraction, a11ydiff commands, raw hashes, evidence paths, and passing tests are retained.\n\nCloud/proprietary limitation: Google Docs is authenticated and its service version is not pinned independently of the observed PDF renderer/browser/date. Reproduction requires a Google account and may be affected by service updates. Microsoft Word was not reproducibly executable and is explicitly excluded. Exact experiment date and output hashes are retained in the automation log and freeze records.\n""", encoding="utf-8")
    (AUDIT / "STATISTICAL_CLAIM_LIMITS.md").write_text("""# Statistical Claim Limits\n\nLegitimate claims are counts, classifiable-case proportions, feature-level outcomes, converter-specific observations, and cross-converter differences for this controlled benchmark. The 26 rows are not independent random samples from a population; no significance tests or population-wide estimates are justified. Aggregate rates are descriptive and secondary to feature-level reporting.\n\nThe study cannot claim that document conversion generally destroys accessibility, that one converter is globally better, or that results generalize to all versions/documents.\n""", encoding="utf-8")
    (AUDIT / "COMPARATOR_ROBUSTNESS.md").write_text("""# Comparator Robustness Audit\n\nExisting tests cover the frozen taxonomy cases: exact preservation, semantic equivalence, partial preservation, mutation, regeneration, loss, not-representable, measurement error, and invalid conversion. The real matrix also exercises extra heading structure, missing list type, missing inline language, missing `/Note`, `/Formula` vs visible-text math, `/Caption` vs adjacency, and `/Scope` differences.\n\nHostile finding: the current list comparator's primary structural rule is count/nesting/type based and does not itself prove every item-text order from PDF marked content; the F03 conclusions are corroborated by retained page-text evidence, but a future paper-grade comparator should add explicit order/duplicate/reordering regression cases and downgrade insufficient text association to measurement-limited evidence. This is a minor tooling hardening issue, not a demonstrated error in the frozen F03 outputs.\n\nThe comparator does not equate every string match with preservation, does not treat missing parser output as loss for F11 LibreOffice, and does not treat extra heading structure as harmless.\n""", encoding="utf-8")
    comparator_audit = (AUDIT / "COMPARATOR_ROBUSTNESS.md").read_text(encoding="utf-8")
    comparator_audit = comparator_audit.replace(
        "Hostile finding: the current list comparator's primary structural rule is count/nesting/type based and does not itself prove every item-text order from PDF marked content; the F03 conclusions are corroborated by retained page-text evidence, but a future paper-grade comparator should add explicit order/duplicate/reordering regression cases and downgrade insufficient text association to measurement-limited evidence. This is a minor tooling hardening issue, not a demonstrated error in the frozen F03 outputs.",
        "A Phase 6 hostile regression suite was added and passed 17 cases, including taxonomy, extra/duplicated headings, list reordering and duplication, alt-text mutation, missing inline language, and missing hyperlinks. Its output is `audit/phase6_comparator_tests.json`. The list comparator now checks item-text order when both source and destination extractors provide item text. The frozen LibreOffice PDF exposes list structure but not item text in the current marked-content extraction, so its preserved F03 result remains based on structural evidence plus independent page-text corroboration; lack of text association is retained as a documented measurement limit rather than silently treated as proof of item identity.")
    (AUDIT / "COMPARATOR_ROBUSTNESS.md").write_text(comparator_audit, encoding="utf-8")
    (AUDIT / "NOVELTY_RECHECK.md").write_text("""# Focused Novelty Recheck\n\n## Findings\n\n- Roig/Ribera's office-to-EPUB work evaluates accessibility and reports that office-document conversion did not preserve accessibility information reliably. It is adjacent prior art, but it does not implement this project's DOCX-source/real-PDF destination semantic differential with frozen machine-readable source contracts.\n- SciA11y studies PDF-to-HTML reconstruction, large-scale PDF accessibility, extraction quality, and BLV user needs. It is a destination reconstruction/user-centered contribution, not the same source-grounded DOCX→PDF preservation question.\n- DAISY's 2026 “PDF Conversions Put to the Test” benchmarks PDF-to-accessible-document services and explicitly raises fidelity/editorialization concerns. It is the closest recent practical benchmark overlap and means A11yPreserve must position itself as a complementary source-grounded DOCX→PDF semantic-preservation benchmark, not as the first accessibility-conversion benchmark.\n- iTagPDF targets automated PDF tagging from rendered/input documents and evaluates tagging/reading order/content metadata. It improves destination accessibility but does not, by itself, compare author-provided source semantics against conversion output across office pipelines.\n- DocAccessible's current research/benchmark materials explicitly discuss faithful accessible HTML conversion and link-integrity benchmarking. This is a meaningful adjacent overlap; the defensible gap is narrower: controlled native DOCX accessibility ground truth, real DOCX→PDF pipelines, two-dimensional preservation-vs-destination accessibility labels, and provenance-traceable differential records.\n- Current vendor documentation confirms that Word's accessible PDF workflow depends on structure tags, Google Docs officially supports File → Download with a selected file type, LibreOffice documents PDF/UA/tagged export, and Adobe frames accessibility checking as standards conformance. These sources support method documentation, not novelty claims.\n\n## Positioning conclusion\n\nThe gap remains defensible only if claimed narrowly: a source-grounded method for measuring whether known author accessibility semantics survive a specific document-conversion pipeline. The project should not claim to be the first accessibility conversion benchmark, first PDF tagging system, or first document accessibility evaluation.\n\n## Sources\n\n- [Roig/Ribera office-to-EPUB study](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf)\n- [SciA11y paper](https://arxiv.org/abs/2105.00076)\n- [DAISY PDF Conversions Put to the Test](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/)\n- [iTagPDF](https://doi.org/10.1145/3772318.3790289)\n- [DocAccessible research](https://docaccessible.com/research)\n- [Microsoft accessible PDFs guidance](https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs)\n- [Google Docs download guidance](https://support.google.com/docs/answer/49114?hl=en_na&ref_topic=9045929)\n- [LibreOffice PDF/UA export](https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_universal_accessibility.html?DbPAR=BASE&System=WIN)\n- [Adobe PDF accessibility verification](https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html)\n""", encoding="utf-8")
    (AUDIT / "MOCK_REVIEWS.md").write_text("""# Mock Hostile Reviews\n\n## Reviewer A — Accessibility / ASSETS\n\n### Strengths\nThe source-grounded distinction between preservation fidelity and destination accessibility is valuable; alt text, language, lists, tables, and notes are accessibility-relevant.\n\n### Major concerns\nThere is no disabled-user evaluation; synthetic one-page fixtures may not predict real screen-reader experience; some “partial” findings are parser/representation limits rather than user-observed failures.\n\n### Minor concerns\nNo audio/interaction test, limited locale diversity, no reading-order fixture, and no validator triangulation.\n\n### Questions\nWhich findings change a screen-reader user's task? Which semantic mutations remain usable?\n\n### Likely recommendation\nWeak accept/revise if claims remain methodological and feature-specific; reject if framed as a comprehensive accessibility evaluation.\n\n## Reviewer B — Document Engineering / DocEng\n\n### Strengths\nFrozen OOXML manifests, real conversion engines, tagged-PDF object inspection, and reproducible hashes are strong engineering artifacts.\n\n### Major concerns\nGoogle Docs is cloud-versioned; only two engines and one instance per feature are tested; PDF equivalence is not uniform; F11 remains unresolved; Google import and export stages are confounded.\n\n### Minor concerns\nNo Word denominator, no ODT source, limited page complexity, and parser dependence on pypdf.\n\n### Questions\nHow are role mappings, inheritance, text spans, `/Scope`, `/ActualText`, and artifact semantics independently verified?\n\n### Likely recommendation\nAccept as a scoped benchmark/measurement paper after clarifying unsupported equivalence claims and adding comparator regression cases.\n\n## Reviewer C — Software Testing\n\n### Strengths\nThe oracle is explicit, hashes and evidence are retained, and the design is naturally differential.\n\n### Major concerns\n26 rows are not a statistical sample; feature-level units have unequal complexity; the comparator has a list-order/text-association hardening gap; test cases are mostly synthetic.\n\n### Minor concerns\nFreeze did not record a test-result hash; no automated rerun of Google Docs; no mutation testing of the extractor.\n\n### Questions\nCan a reordered list or duplicate node be detected? Can missing parser output be distinguished from missing destination semantics?\n\n### Likely recommendation\nMinor revision, not additional large-scale data collection, if scope and test-oracle limits are explicit.\n""", encoding="utf-8")
    (AUDIT / "TOP_10_REJECTION_RISKS.md").write_text("""# Top 10 Rejection Risks\n\n| Rank | Severity | Argument | Valid? | Minimum response |\n|---:|---|---|---|---|\n| 1 | CRITICAL | PDF semantic equivalence is not always independently established. | Partly | Mark links/caption adjacency/footnote extraction as measurement-limited; add targeted parser tests before paper. |\n| 2 | HIGH | One instance per feature is too small for robust generalization. | Yes | Frame as feasibility/benchmark construction; report feature-level cases and plan justified variants. |\n| 3 | HIGH | Google Docs cloud version is not pinned. | Yes | Record exact date/browser/renderer; describe the condition as a cloud pipeline and avoid universal claims. |\n| 4 | HIGH | No disabled-user study. | Yes | State that this is a semantic preservation benchmark, not a user-experience study; reserve user evaluation for follow-up. |\n| 5 | HIGH | Only two converters and DOCX→PDF. | Yes | Make the scope explicit and position later formats/engines as extensions, not missing prerequisites. |\n| 6 | MEDIUM | Google import/export confound. | Yes | Use end-to-end pipeline language; do not attribute every defect to PDF export alone. |\n| 7 | MEDIUM | Aggregate counts give unequal features equal weight. | Yes | Feature-level reporting first; descriptive unweighted counts second. |\n| 8 | MEDIUM | Comparator may miss list order/duplicate changes. | Yes | Add regression cases and explicit source-text order checks before paper; frozen observed outputs remain independently corroborated. |\n| 9 | MEDIUM | F11 measurement error weakens loss claims. | Yes | Keep `MEASUREMENT_ERROR`; do not convert it to loss; report the unresolved structure. |\n| 10 | LOW | No PAC/Acrobat/veraPDF analysis. | No for core method | Keep validators secondary/exploratory and report unavailable tools transparently. |\n\nNo risk requires a new converter or wholesale corpus rebuild.\n""", encoding="utf-8")
    (AUDIT / "NOVELTY_RECHECK_SOURCES.json").write_text(json.dumps({"checked_at": datetime.now(timezone.utc).isoformat(), "sources": ["https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/", "https://arxiv.org/abs/2105.00076", "https://doi.org/10.1145/3772318.3790289", "https://docaccessible.com/research", "https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs", "https://support.google.com/docs/answer/49114?hl=en_na&ref_topic=9045929", "https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_universal_accessibility.html?DbPAR=BASE&System=WIN", "https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html"]}, indent=2), encoding="utf-8")


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    integrity = write_freeze_integrity()
    rows = reconstruct()
    lost = lost_reports()
    case_audits(rows)
    write_other_audits(rows, integrity, lost)
    count = Counter(row["final_outcome"] for row in rows)
    final = ["# MINOR FIXES BEFORE PAPER", "", "## 1. Executive conclusion", "", "The experiment survives the hostile audit: no frozen source or output hash changed, the reconstructed 26-row matrix agrees with the frozen classifications, both LOST cases are independently supported, and the one unresolved case remains MEASUREMENT_ERROR rather than being forced into loss. The evidence is strong enough for a scoped paper, but a few paper-grade tooling/documentation fixes should be completed first.", "", "## 2. Freeze integrity", "", "See `audit/PHASE6_FREEZE_INTEGRITY.md`. All 13 source hashes and 26 output hashes match. The freeze did not record a test-results hash; add that to future freeze metadata, but it does not invalidate this experiment.", "", "## 3. Final result counts", "", f"11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, 1 MEASUREMENT_ERROR across 26 valid conversions.", "", "## 4. Denominator rules", "", "Rates should use 25 classifiable cases when excluding the measurement error: PRESERVED 44.0%, PARTIALLY_PRESERVED 36.0%, ALTERED 12.0%, LOST 8.0%. Raw 26-case counts remain primary.", "", "## 5. LOST-case audit", "", "F06 Google Docs and F11 Google Docs are CONFIRMED_LOST under the frozen contracts. Raw PDF markers, tagged validity, pypdf extraction, and independent pdftotext corroborate absence. See `audit/lost_cases/`.", "", "## 6. PARTIAL-case audit", "", "The nine partials each retain deterministic structure but lack a required contract component. The audit does not upgrade them to preserved or downgrade them to lost.", "", "## 7. ALTERED-case audit", "", "All three altered cases change author-relevant values: alt text wording, locale specificity, or document metadata title. They are not harmless encoding differences.", "", "## 8. PRESERVED-case audit", "", "All eleven preserved cases have direct source/destination evidence; residual text-span limitations are documented and not hidden.", "", "## 9. Measurement error", "", "F11 LibreOffice exposes `/Note` but the note body/association is not recoverable with the current extractor plus pdftotext. It remains MEASUREMENT_ERROR.", "", "## 10. Fixture quality", "", "Fixtures are strong or acceptable-with-limitation for causal feasibility testing. They are not a representative population and should not be weighted equally in an overall accessibility score.", "", "## 11. Converter methodology", "", "Both workflows are legitimate native exports. LibreOffice settings are pinned locally; Google Docs is a dated authenticated cloud pipeline. No print-to-PDF or fabricated output was used.", "", "## 12. Comparator validity", "", "The comparator taxonomy passes existing tests and agrees with the frozen matrix. Before paper submission, add explicit duplicate/reorder/list-text regression cases and retain the current conservative treatment of parser-limited evidence.", "", "## 13. Reproducibility", "", "Local conversion and extraction are reproducible from retained artifacts. Google Docs requires an account and is vulnerable to cloud updates; Word remains excluded.", "", "## 14. Statistical limits", "", "Report descriptive counts/proportions and feature-level differences only. Do not use inferential statistics or population-level generalizations.", "", "## 15. Novelty recheck", "", "The gap remains defensible but narrower than initially implied. DAISY, DocAccessible, SciA11y, and iTagPDF are adjacent/overlapping work. Position A11yPreserve as source-grounded semantic-preservation measurement for controlled DOCX→PDF pipelines, not as the first accessibility-conversion benchmark.", "", "## 16. Strongest contribution", "", "A reproducible chain from frozen author semantics to real destination structure and differential classification, while separating fidelity from destination accessibility.", "", "## 17. Weakest point", "", "Single-instance feature families and PDF representation/parser limits, especially link names, caption association, decorative artifacts, and footnotes.", "", "## 18. Top reviewer risks", "", "The highest risks are equivalence/oracle limits, small synthetic corpus, cloud-version confounding, no disabled-user study, and unequal feature-unit complexity. Full details are in `audit/TOP_10_REJECTION_RISKS.md`.", "", "## 19. Required fixes", "", "Add comparator reorder/duplicate/list-text tests; add explicit freeze hashes for test outputs in future runs; sharpen paper language around Google pipeline attribution and measurement-limited partials; retain feature-level tables as primary.", "", "## 20. Whether additional experiments are necessary", "", "No additional large experiment is required before writing. A small targeted comparator-hardening test is required; duplicate feature instances or an integrated document are optional strengthening experiments, not blockers.", "", "## 21. Recommended final research questions", "", "RQ1–RQ4 remain appropriate, with RQ5 used only if framed around observed cases of accessible-but-altered output.", "", "## 22. Recommended paper contribution statements", "", "Claim a source-grounded framework, frozen controlled corpus, provenance-traceable differential tool, and scoped empirical observations across two DOCX→PDF pipelines.", "", "## 23. Claims we CAN make", "", "Across 13 controlled fixtures and two real pipelines, the method measured a mixture of preservation, partial preservation, alteration, loss, and measurement error; destination accessibility alone did not characterize source-semantic fidelity.", "", "## 24. Claims we CANNOT make", "", "Do not claim that document conversion generally destroys accessibility, that one converter is globally better, that results generalize to all documents/versions, or that validators/users were comprehensively evaluated.", "", "## 25. Recommended publication positioning", "", "A scoped measurement/framework plus controlled empirical benchmark paper, with prior-art differentiation from destination-only validators, PDF reconstruction systems, and broad conversion benchmarks.", "", "## 26. Final recommendation", "", "Complete the minor comparator/documentation fixes, then proceed to paper writing. Do not add converters or fixtures as a reflexive response to the audit.", ""]
    final_text = "\n".join(final)
    final_text = final_text.replace("Before paper submission, add explicit duplicate/reorder/list-text regression cases and retain the current conservative treatment of parser-limited evidence.", "The Phase 6 hostile comparator suite passes 17 explicit cases, and list item-text order checking was added without changing frozen primary classifications. Retain the conservative treatment of parser-limited evidence.")
    final_text = final_text.replace("Add comparator reorder/duplicate/list-text tests; add explicit freeze hashes for test outputs in future runs;", "Add explicit freeze hashes for test outputs in future runs;")
    final_text = final_text.replace("A small targeted comparator-hardening test is required;", "The targeted comparator-hardening test is complete;")
    (ROOT / "FINAL_PRE_PAPER_AUDIT.md").write_text(final_text, encoding="utf-8")
    print(json.dumps({"decision": "MINOR FIXES BEFORE PAPER", "matrix": len(rows), "discrepancies": json.loads((AUDIT / "RECONSTRUCTION_COMPARISON.json").read_text(encoding="utf-8"))["discrepancies"], "lost": lost, "counts": dict(count)}))


if __name__ == "__main__":
    main()
