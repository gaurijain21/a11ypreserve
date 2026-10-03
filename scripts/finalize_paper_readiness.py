from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
RESULTS = ROOT / "results" / "full_experiment"
DIFF = json.loads((RESULTS / "reports" / "a11ydiff_results.json").read_text(encoding="utf-8"))["records"]
CORPUS = json.loads((ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))

FEATURE_NAMES = {
    "headings": "heading hierarchy",
    "image_alt_text": "image alternative text",
    "lists": "list semantics",
    "table": "table/header structure",
    "document_language": "document language",
    "inline_language": "inline language change",
    "decorative_image": "decorative image state",
    "hyperlinks": "hyperlink semantics",
    "document_title": "document title/metadata",
    "complex_table": "multi-level table headers",
    "footnotes": "footnote association",
    "equation": "equation/math semantics",
    "captions": "figure/caption association",
}

FIXTURE_FEATURE = {item["fixture_id"]: item["feature_family"] for item in CORPUS["fixtures"]}
BY_FIXTURE = {}
for row in DIFF:
    BY_FIXTURE.setdefault(row["fixture"], {})[row["converter"]] = row


def write(name: str, content: str) -> None:
    cleaned = dedent(content).strip()
    cleaned = "\n".join(line[4:] if line.startswith("    ") else line for line in cleaned.splitlines())
    (RESEARCH / name).write_text(cleaned + "\n", encoding="utf-8")


def compact(value: object, limit: int = 280) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return text if len(text) <= limit else text[: limit - 3] + "..."


def observation(fixture: str, lo: dict, gd: dict) -> str:
    special = {
        "F01_HEADINGS": "Google Docs adds an extra H1, changing the heading sequence; LibreOffice matches the source level/order sequence.",
        "F02_ALT_TEXT": "LibreOffice prefixes the author-written alt text with `Enrollment chart -`; Google Docs retains the exact source string.",
        "F03_LISTS": "LibreOffice exposes `/ListNumbering` for list type; Google Docs preserves list nesting but does not expose equivalent ordered/unordered evidence.",
        "F05_DOCUMENT_LANGUAGE": "LibreOffice preserves `en-US`; Google Docs emits the less specific `en` value.",
        "F06_INLINE_LANGUAGE": "LibreOffice exposes an `es-MX` `/Lang` span; Google Docs retains document language but no inline language span.",
        "F09_DOCUMENT_TITLE": "LibreOffice preserves the source title; Google Docs uses `F09_DOCUMENT_TITLE` rather than the author title.",
        "F10_COMPLEX_TABLE": "LibreOffice exposes scope and span evidence for the multi-level headers; Google Docs exposes header roles but not complete associations.",
        "F11_FOOTNOTES": "LibreOffice exposes a `/Note` structure but the association is measurement-limited; Google Docs exposes no footnote structure or source note body.",
        "F12_EQUATION": "LibreOffice emits `/Formula`; Google Docs retains visible equation text without machine-readable math structure.",
        "F14_CAPTIONS": "LibreOffice exposes `/Caption` plus ordered text; Google Docs retains caption text but association is established only by adjacency.",
    }
    return special.get(fixture, f"LibreOffice: {lo['empirical_classification']}; Google Docs: {gd['empirical_classification']}.")


def make_tables() -> tuple[str, str]:
    rows = ["| Fixture | Accessibility property | LibreOffice | Google Docs | Key observation |", "|---|---|---|---|---|"]
    for fixture in [item["fixture_id"] for item in CORPUS["fixtures"]]:
        lo, gd = BY_FIXTURE[fixture]["LibreOffice"], BY_FIXTURE[fixture]["Google Docs"]
        rows.append(f"| {fixture} | {FEATURE_NAMES.get(lo['feature'], lo['feature'])} | {lo['empirical_classification']} | {gd['empirical_classification']} | {observation(fixture, lo, gd)} |")
    feature_table = "\n".join(rows)

    diff_rows = ["| Fixture | Accessibility property | LibreOffice | Google Docs | Exact observed difference | Accessibility information remained usable? |", "|---|---|---|---|---|---|"]
    for fixture in [item["fixture_id"] for item in CORPUS["fixtures"]]:
        lo, gd = BY_FIXTURE[fixture]["LibreOffice"], BY_FIXTURE[fixture]["Google Docs"]
        if lo["empirical_classification"] == gd["empirical_classification"]:
            continue
        usable = {
            "F01_HEADINGS": "Yes, but the hierarchy is altered in the Google Docs output.",
            "F02_ALT_TEXT": "Yes in both; LibreOffice changes the author string.",
            "F03_LISTS": "Yes, but Google Docs lacks independently established list type.",
            "F05_DOCUMENT_LANGUAGE": "Yes, but Google Docs loses locale specificity.",
            "F06_INLINE_LANGUAGE": "LibreOffice: yes; Google Docs: inline language information not established.",
            "F09_DOCUMENT_TITLE": "Yes, but Google Docs changes the metadata value.",
            "F10_COMPLEX_TABLE": "Yes, but Google Docs does not establish complete header associations.",
            "F11_FOOTNOTES": "LibreOffice: unresolved; Google Docs: no association found.",
            "F12_EQUATION": "LibreOffice: machine-readable structure; Google Docs: visible text only.",
            "F14_CAPTIONS": "LibreOffice: structural association; Google Docs: text adjacency only.",
        }.get(fixture, "Feature-specific usability requires the cited evidence.")
        diff_rows.append(f"| {fixture} | {FEATURE_NAMES.get(lo['feature'], lo['feature'])} | {lo['empirical_classification']} | {gd['empirical_classification']} | {observation(fixture, lo, gd)} | {usable} |")
    return feature_table, "\n".join(diff_rows)


def main() -> None:
    RESEARCH.mkdir(parents=True, exist_ok=True)
    feature_table, difference_table = make_tables()

    write("FINAL_METHODS_SPEC.md", """
    # Final Methods Specification

    ## 5.1 Research objective

    A11yPreserve measures whether accessibility information present in controlled DOCX source documents remains preserved, partially preserved, altered, or lost after conversion through a specified DOCX-to-PDF pipeline. The unit of analysis is a fixture-level accessibility property under a recorded converter condition; the study does not treat destination accessibility as equivalent to preservation fidelity.

    ## 5.2 Source corpus

    The frozen corpus contains 13 small, atomic DOCX fixtures covering heading hierarchy, image alternative text, list semantics, table/header structure, document language, inline language changes, decorative image state, hyperlinks, document title/metadata, multi-level table headers, footnote association, equation/math semantics, and figure/caption association. Fixtures were constructed by controlled generation scripts using `python-docx` together with explicit native WordprocessingML/OOXML constructs where needed, and were kept visually simple so the target property could be isolated. Atomic fixtures support causal interpretation; they are not a statistically representative document population.

    The corpus includes the historical F01-F04 fixtures and the expanded F05-F12/F14 fixtures. The frozen corpus manifest records each source path, size, SHA-256 hash, feature family, and verification status. F13 was not part of the frozen corpus.

    ## 5.3 Ground truth

    Source ground truth was established as a three-way agreement:

    1. a machine-readable source manifest states the expected accessibility property;
    2. raw OOXML was independently inspected, including `word/document.xml`, `word/footnotes.xml`, run properties, numbering, relationships, and native document parts as applicable;
    3. the source extractor produced an ASIR record matching the manifest.

    No claim of human accessibility-expert validation is made. The source-verification chain is recorded in the corpus reports and frozen manifests.

    ## 5.4 Conversion pipelines

    The primary conditions were:

    - **LibreOffice DOCX→PDF conversion pipeline:** LibreOffice `26.2.6.3`, build `8221e31b3ac356a1623c672912a3d2b492f7e3d1`, Windows `10.0.26200.0`, native headless `soffice.com writer_pdf_Export`, with `UseTaggedPDF=true`, `PDFUACompliance=true`, and `SelectPdfVersion=1`.
    - **Google Docs DOCX→PDF conversion pipeline:** Windows `10.0.26200.0`, Chrome `153.0.8010.53`, authenticated Google Docs web UI, exact frozen DOCX upload, then `File → Download → PDF Document (.pdf)`. The observed PDF producer was `Skia/PDF m156`; no print dialog, manual content repair, or post-export accessibility repair was used.

    Google results are end-to-end pipeline results. They may reflect DOCX import, Google Docs' internal representation, and PDF generation; the experiment does not isolate those stages. Microsoft Word was excluded from the denominator because it was not a completed primary pipeline.

    ## 5.5 Destination extraction

    PDF outputs were validated for existence, non-zero size, parseability, page count, structural tagging, and `StructTreeRoot`. The destination extractor inspected PDF structure elements and roles, including headings, figures and `/Alt`, list roles and `/ListNumbering`, tables and header cells, `/Lang`, link annotations, metadata, `/Note`, `/Formula`, `/Caption`, and related evidence. Raw object-marker inspection and Poppler `pdftotext` were used as independent secondary checks where parser coverage was limited. PAC, Acrobat, and veraPDF were not available as systematic validators in this experiment.

    ## 5.6 a11ydiff

    `a11ydiff` loads the source ASIR and destination PDF extraction for the same fixture/output pair, compares the feature-specific contract, records source and destination values, stores evidence paths and hashes, and emits a structured classification. The implementation also records a secondary destination-accessibility axis, but the paper's primary outcomes use the compact preservation categories below. It is a differential measurement tool, not a complete accessibility checker or user-experience measure.

    ## 5.7 Classification rules

    - **PRESERVED:** the destination expresses the contracted accessibility information exactly or through a verified equivalent representation.
    - **PARTIALLY_PRESERVED:** some required information or structure survives, but at least one contract component is absent or not independently established.
    - **ALTERED:** the destination retains the feature but changes an author-relevant value, such as alt text wording, locale specificity, or title metadata.
    - **LOST:** the source feature is valid and representable in the destination, but the required destination representation is absent and independent checks support absence.
    - **MEASUREMENT_ERROR:** the output is valid and some relevant structure is present, but the available extraction evidence cannot resolve the contract sufficiently for a reliable preservation judgment.

    `NOT_REPRESENTABLE` and `INVALID_CONVERSION` were available methodological categories but did not occur in the 26 final cases.

    ## 5.8 Independent verification

    All non-preserved outcomes were reviewed against source manifests, raw OOXML, source ASIR, destination validity, primary PDF extraction, raw PDF structure, and independent PDF text/object checks where applicable. The two LOST cases were retained only after those checks. The LibreOffice F11 footnote case was retained as `MEASUREMENT_ERROR` rather than being forced into `LOST`.

    ## 5.9 Result freezing

    Source fixture hashes, PDF output hashes, source/destination extraction paths, converter metadata, and primary classification records were frozen. Phase 6 independently recalculated all 13 source hashes and 26 output hashes and reconstructed all 26 rows with zero discrepancies. A future freeze should additionally record the test-results hash; its absence is a documentation limitation, not a change to the current results.

    ## 5.10 Secondary validators

    Conventional validators are not the ground truth for this study. The core result is based on source-grounded comparison with PDF structure. No systematic PAC, Acrobat Accessibility Checker, or veraPDF dataset was available, so validator comparison is reserved for future work rather than treated as a core research question.
    """)

    write("FINAL_RESULT_ACCOUNTING.md", """
    # Final Result Accounting

    These counts are copied from the frozen primary result set and were not recalculated by changing any primary classification.

    | Outcome | Count | Share of 26 attempted cases | Share of 25 classifiable cases |
    |---|---:|---:|---:|
    | PRESERVED | 11 | 42.3% | 44.0% |
    | PARTIALLY_PRESERVED | 9 | 34.6% | 36.0% |
    | ALTERED | 3 | 11.5% | 12.0% |
    | LOST | 2 | 7.7% | 8.0% |
    | MEASUREMENT_ERROR | 1 | 3.8% | excluded |
    | **Total** | **26** | **100.0%** | **25 determined outcomes** |

    ## Denominator definitions

    - **Attempted cases:** 26 fixture/converter pairs.
    - **Successfully converted cases:** 26. All outputs were parseable, non-empty, tagged, and validated.
    - **Classifiable cases:** 25, excluding the one `MEASUREMENT_ERROR`.
    - **Determined preservation outcomes:** 25.
    - **Representable cases:** 26. No `NOT_REPRESENTABLE` case occurred.

    Counts are primary because this is a small, intentionally designed benchmark. When proportions are reported for preservation outcomes, the denominator must be stated. The 25-case outcome proportions are: PRESERVED 11/25 = 44.0%; PARTIALLY_PRESERVED 9/25 = 36.0%; ALTERED 3/25 = 12.0%; LOST 2/25 = 8.0%. The 26-case shares are descriptive experiment-wide shares and include the measurement error in the denominator.

    The 13 fixtures are not interchangeable population samples. Feature-level tables therefore take precedence over aggregate percentages, and no weighted overall converter score is reported.
    """)

    write("FINAL_FEATURE_RESULTS.md", f"""
    # Final Feature Results

    The table reports frozen fixture-level outcomes. It does not rank converters.

    {feature_table}

    `PRESERVED` includes exact and verified equivalent destination representations. `MEASUREMENT_ERROR` is retained where evidence could not resolve the contract.
    """)

    write("FINAL_CROSS_CONVERTER_DIFFERENCES.md", f"""
    # Final Cross-Converter Differences

    This table includes only fixtures whose frozen primary outcome differs between the two tested pipelines. It is a feature-specific comparison, not an overall converter ranking.

    {difference_table}

    The table demonstrates converter-dependent behavior for the tested conditions while avoiding claims about either converter in general.
    """)

    write("CONFIRMED_LOST_CASES.md", """
    # Confirmed Lost Cases

    ## Case 1 — F06 / Google Docs / inline language

    - **Source information:** document language `en-US`; the run `Buenos días` has an explicit `es-MX` language override in OOXML and the source ASIR.
    - **Expected PDF representation:** a marked structure span carrying `/Lang es-MX` or an equivalent inline language representation.
    - **Destination:** the PDF is valid and tagged, with catalog/document language `en`, but the destination extractor finds no inline language span and raw PDF inspection finds no `es-MX` marker. `pdftotext` confirms the visible phrase is present but does not supply the missing language association.
    - **Independent confirmation:** pypdf structure extraction, raw PDF marker inspection, and Poppler text extraction agree that the required inline language structure is absent.
    - **Disposition:** `LOST`. This is not invalid conversion, non-representability, or a harmless encoding difference; the other real engine demonstrates that PDF can represent the feature.

    Evidence: `audit/lost_cases/F06_INLINE_LANGUAGE_Google_Docs.md`, the frozen F06 manifest, source/destination extraction JSON, and `F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf`.

    ## Case 2 — F11 / Google Docs / footnote association

    - **Source information:** a native footnote with reference text `The benchmark uses an explicit footnote association.` and note body `This note records the source-to-note association.`; OOXML uses `word/footnotes.xml` and a `w:footnoteReference`.
    - **Expected PDF representation:** a PDF `/Note`/footnote structure or equivalent reference-to-note association retaining the note body.
    - **Destination:** the PDF is valid and tagged, but raw inspection finds no `/Note`, `/Footnote`, or `/Link` markers; the destination extractor returns no footnote, and `pdftotext` does not contain the source note body.
    - **Independent confirmation:** pypdf extraction, raw PDF marker inspection, and Poppler text extraction agree that the required note structure/body association is absent.
    - **Disposition:** `LOST`. This is not invalid conversion, non-representability, or a serialization-only difference; LibreOffice produced a comparable `/Note` structure in the same benchmark.

    Evidence: `audit/lost_cases/F11_FOOTNOTES_Google_Docs.md`, the frozen F11 manifest, source/destination extraction JSON, and `F11_FOOTNOTES__GOOGLE_DOCS.pdf`.

    These findings establish loss under the tested source contracts and pipeline conditions. They do not establish that every Google Docs conversion loses all footnotes or inline language.
    """)

    write("MEASUREMENT_ERROR_NOTE.md", """
    # Measurement Error Note

    The single `MEASUREMENT_ERROR` case is F11 / LibreOffice / footnote association.

    The source footnote is valid and independently verified. The destination PDF is parseable, tagged, and contains a `/Note` structure with child objects. However, the current marked-content extractor does not recover enough note-body text to verify the source reference-to-body association, and an independent Poppler `pdftotext` run does not resolve that association either.

    The case was not forced into `PRESERVED` because the available evidence cannot establish the complete contract. It was not classified as `LOST` because `/Note` structure is present, and it was not classified as `INVALID_CONVERSION` because the PDF is valid and contains the source content. The unresolved issue is a measurement limitation at the intersection of the current extractor and heterogeneous PDF representation, not evidence that the converter definitely removed the feature.

    Excluding this case from determined-outcome percentages is therefore appropriate: 26 cases were attempted, but only 25 support a determinate preservation outcome. The raw count remains visible in all accounting tables.

    Evidence: `audit/MEASUREMENT_ERROR_ANALYSIS.md`, F11 source/destination extraction JSON, the raw LibreOffice PDF, and the independent Poppler text check.
    """)

    write("CLAIM_BOUNDARIES.md", """
    # Claims Supported

    - Accessibility information was not uniformly preserved across the tested DOCX-to-PDF conversion pipelines.
    - The same frozen source fixture sometimes produced different preservation outcomes across the tested LibreOffice and Google Docs pipelines.
    - Some converted PDFs remained tagged while particular source accessibility properties were partially preserved, altered, or lost.
    - Source-grounded comparison exposed preservation changes that a destination-only inspection is not designed to reconstruct, such as author-alt-text mutation or loss of an inline language association.
    - A controlled, provenance-traceable source-grounded preservation benchmark is technically feasible.
    - The 26 observed cases contain a mixture of preservation, partial preservation, alteration, confirmed loss, and one measurement error under the frozen contracts.

    # Claims Not Supported

    - Document conversion generally destroys accessibility.
    - Google Docs is generally less accessible, or LibreOffice is generally better.
    - These results generalize to all DOCX files, all documents, or all software versions.
    - Observed structural changes necessarily affect every screen-reader user or have a known uniform practical severity.
    - Every altered value causes practical harm.
    - `a11ydiff` measures complete document accessibility or user experience.
    - Destination-only accessibility validators are defective because they do not answer the source-preservation question.
    - PDF itself caused every observed change.
    - Google Docs PDF export alone caused every Google-pipeline change; the tested condition is an end-to-end Google Docs DOCX-to-PDF pipeline including import and internal representation.
    - The study is a disabled-user evaluation, a general PDF compliance benchmark, or an overall converter ranking.
    """)

    write("FINAL_RQS.md", """
    # Final Research Questions

    ## RQ1

    To what extent do the tested DOCX-to-PDF conversion pipelines preserve accessibility information present in controlled source documents?

    ## RQ2

    Which tested accessibility properties are preserved, partially preserved, altered, or lost during conversion?

    ## RQ3

    How do preservation outcomes differ between the tested LibreOffice and Google Docs conversion pipelines?

    A validator-comparison question is not included in the core RQs. Validator evidence was not systematic or complete enough for a defensible primary analysis and is reserved for future work.
    """)

    write("FINAL_CONTRIBUTIONS.md", """
    # Final Contribution Statements

    1. A source-grounded method for measuring whether known accessibility information survives document conversion.
    2. A controlled benchmark of 13 verified DOCX accessibility fixtures with explicit machine-readable source ground truth.
    3. `a11ydiff`, an automated comparison framework that relates source accessibility properties to converted PDF structure with retained evidence and hashes.
    4. An empirical study of 26 real outputs from two DOCX-to-PDF conversion pipelines, showing preservation, partial preservation, alteration, and confirmed loss across tested accessibility properties.

    These are scoped framework and benchmark contributions. The paper should not claim novelty using “first” language unless a later literature review establishes a precise, supportable basis.
    """)

    write("RELATED_WORK_POSITIONING.md", """
    # Related-Work Positioning Notes

    These notes are for later writing, not a finished related-work section.

    ## Accessibility-aware document conversion

    Roig and Ribera's office-to-EPUB work studies accessibility consequences of office-document conversion. It overlaps in asking what survives transformation, but A11yPreserve uses controlled native DOCX source ground truth, real DOCX-to-PDF pipelines, machine-readable source contracts, and provenance-traceable source/destination comparison. Avoid claiming that A11yPreserve is the first accessibility-preservation study.

    Citation: [Roig/Ribera office-to-EPUB study](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf)

    ## Accessible representation generation and remediation

    SciA11y and PDF-to-HTML work address reconstruction, extraction, accessibility, and user needs in destination representations. iTagPDF addresses automated PDF tagging and related structure. These works are adjacent because they inspect or improve accessible representations; the remaining difference is that A11yPreserve starts with known author-provided source accessibility information and asks whether it survives a specified conversion pipeline. Avoid framing the contribution as a general PDF tagging system.

    Citations: [SciA11y](https://arxiv.org/abs/2105.00076), [iTagPDF](https://doi.org/10.1145/3772318.3790289)

    ## PDF conversion benchmarks

    DAISY's “PDF Conversions Put to the Test” and DocAccessible materials overlap in benchmarking conversion fidelity and accessible output. A11yPreserve is narrower: controlled DOCX source semantics, two real DOCX-to-PDF conditions, and a preservation-vs-destination-accessibility distinction. Avoid claiming that the benchmark is the first or broadest PDF conversion benchmark.

    Citations: [DAISY PDF conversion benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/), [DocAccessible research](https://docaccessible.com/research)

    ## PDF accessibility evaluation

    PAC, Acrobat Accessibility Checker, veraPDF, and standards-oriented PDF evaluation ask whether destination files satisfy implemented checks or conformance requirements. Those are valuable but answer a different question from whether author-provided source accessibility information survived. The A11yPreserve validator study is future work, not a core result.

    Method references: [Microsoft accessible PDFs guidance](https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs), [LibreOffice PDF/UA export](https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_universal_accessibility.html?DbPAR=BASE&System=WIN), [Adobe PDF accessibility verification](https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html)
    """)

    write("FINAL_NOVELTY_STATEMENT.md", """
    # Final Novelty Statement

    Existing work has studied accessible document conversion, PDF accessibility evaluation, accessibility remediation, and destination reconstruction. A11yPreserve instead evaluates accessibility preservation from known source ground truth: it begins with controlled DOCX documents whose target accessibility properties are explicitly verified, converts identical sources through multiple real pipelines, and compares resulting destination structures against those source properties. The resulting contribution is a narrowly scoped source-grounded preservation measurement framework and benchmark, not a claim to be the first accessibility-conversion study or a replacement for destination validators.
    """)

    write("CORPUS_LIMITATION_NOTE.md", """
    # Corpus Limitation Note

    The benchmark contains 13 intentionally controlled atomic fixtures. Each isolates a specific accessibility property so that a change can be attributed to a known source contract rather than to a large mixture of formatting and content. This improves causal interpretability but does not make the corpus statistically representative of real documents.

    The fixtures are small and mostly synthetic, each feature family has one primary instance, and feature families differ in complexity and practical impact. The study therefore reports feature-level results first and does not assign an overall weighted accessibility score. Realistic integrated documents and justified variants are future strengthening work, not silently implied by the current corpus.
    """)

    write("GOOGLE_DOCS_REPRODUCIBILITY_NOTE.md", """
    # Google Docs Reproducibility Note

    Google Docs is a cloud service. The experiment recorded the authenticated browser workflow, Windows environment, Chrome `153.0.8010.53`, observed PDF producer `Skia/PDF m156`, experiment date, source hashes, output hashes, and exact download procedure. The backend service version cannot necessarily be pinned independently of the observed condition, and future reruns may change as Google updates its import, internal representation, or PDF generation.

    Results should therefore be described as behavior of the dated Google Docs DOCX-to-PDF conversion pipeline, not as a timeless property of Google Docs or as an isolated PDF-export defect.
    """)

    write("USER_STUDY_SCOPE_NOTE.md", """
    # User-Study Scope Note

    A11yPreserve measures preservation of accessibility information at the document-structure level. It does not directly measure task completion by disabled users, screen-reader usability, perceived accessibility, or the severity experienced by users.

    A disabled-user study is not required to answer the structural preservation question tested here, but it would be an important follow-up for determining which preservation changes affect real tasks and users. The manuscript must not present this benchmark as a user-experience evaluation.
    """)

    write("VALIDATOR_ROLE_DECISION.md", """
    # Validator Role Decision

    ## FUTURE WORK

    Validator analysis is not a core research question in the current paper. PAC, Acrobat Accessibility Checker, and veraPDF were not available as a systematic, complete validator dataset for all 26 outputs. Poppler text extraction and raw PDF inspection were used as independent evidence for specific cases, not as accessibility-validator verdicts.

    The core contribution stands without validator results because A11yPreserve asks whether source accessibility information survived conversion, while conventional validators ask whether destination checks pass. A future study can compare the two questions systematically for each confirmed preservation defect.
    """)

    write("PAPER_EVIDENCE_MAP.md", """
    # Paper Evidence Map

    | Paper claim | Supporting artifact |
    |---|---|
    | 13 controlled source fixtures were frozen | `corpus/FROZEN_CORPUS_MANIFEST.json`, `audit/PHASE6_FREEZE_INTEGRITY.md` |
    | Source semantics were independently verified | `corpus/reports/source_verification.json`, source manifests, source extraction JSON, `audit/FIXTURE_BIAS_REVIEW.md` |
    | 26 genuine DOCX-to-PDF outputs were produced | `results/full_experiment/AUTOMATION_LOG.md`, `results/full_experiment/reports/output_validation.json` |
    | All 26 outputs were parseable/tagged/validated | `results/full_experiment/reports/output_validation.json` |
    | Frozen classifications are internally consistent | `results/full_experiment/PRIMARY_RESULTS_FREEZE.json`, `audit/RECONSTRUCTED_RESULTS.csv`, `audit/RECONSTRUCTION_COMPARISON.json` |
    | F06 Google Docs inline language was lost | `audit/lost_cases/F06_INLINE_LANGUAGE_Google_Docs.md`, `research/CONFIRMED_LOST_CASES.md` |
    | F11 Google Docs footnote association was lost | `audit/lost_cases/F11_FOOTNOTES_Google_Docs.md`, `research/CONFIRMED_LOST_CASES.md` |
    | F11 LibreOffice remains unresolved rather than forced to loss | `audit/MEASUREMENT_ERROR_ANALYSIS.md`, `research/MEASUREMENT_ERROR_NOTE.md` |
    | Cross-pipeline differences exist | `research/FINAL_FEATURE_RESULTS.md`, `research/FINAL_CROSS_CONVERTER_DIFFERENCES.md` |
    | Comparator robustness was tested | `audit/phase6_comparator_tests.json`, `audit/COMPARATOR_ROBUSTNESS.md`, `scripts/phase6_comparator_tests.py` |
    | Counts and denominators are explicit | `research/FINAL_RESULT_ACCOUNTING.md`, `audit/DENOMINATOR_RULES.md` |
    | Google pipeline attribution is appropriately scoped | `audit/PIPELINE_ATTRIBUTION.md`, `research/GOOGLE_DOCS_REPRODUCIBILITY_NOTE.md` |
    """)

    write("PAPER_FIGURE_TABLE_PLAN.md", """
    # Paper Figure and Table Plan

    ## Figure 1 — A11yPreserve workflow

    Verified accessible source → DOCX-to-PDF conversion pipeline → destination PDF → structural accessibility extraction → source-grounded comparison → preservation outcome.

    ## Table 1 — Fixture corpus

    List the 13 fixture IDs, feature families, source contract, and verification status.

    ## Table 2 — Feature × converter result matrix

    Use `research/FINAL_FEATURE_RESULTS.md` as the source for the 13-row feature-level matrix. Keep feature-level outcomes primary and avoid an overall converter ranking.

    ## Figure 2 — Outcome counts

    Show the five frozen primary outcome counts: 11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, and 1 MEASUREMENT_ERROR. Label the figure as descriptive and small-sample; do not imply population estimates.

    ## Table 3 — Cross-converter differences

    Use `research/FINAL_CROSS_CONVERTER_DIFFERENCES.md` to show only fixtures where the two pipelines differ.

    ## Figure 3 — Concrete source/output example

    Prefer F02 alt text or F06 inline language. Show the source contract, the destination structure, and the resulting classification with evidence paths. Do not use a destination-only accessibility score as the figure's conclusion.
    """)

    write("PAPER_OUTLINE.md", """
    # Paper Outline

    ## 1. Introduction

    Motivate the distinction between accessible source documents and preservation of their accessibility information during conversion. State the narrow research gap, final RQs, and bounded contributions.

    ## 2. Background and related work

    Introduce relevant accessibility semantics, conversion pipelines, PDF structure, destination evaluation, and the positioning in `research/RELATED_WORK_POSITIONING.md`.

    ## 3. A11yPreserve

    Explain the source-grounded workflow, source contracts, frozen corpus, destination extraction, a11ydiff, and the compact outcome categories.

    ## 4. Experimental method

    Describe 13 fixtures, source verification, the LibreOffice and Google Docs pipelines, output validation, evidence retention, denominator rules, and limitations of PDF equivalence.

    ## 5. Results

    Answer RQ1 with accounting and feature-level outcomes, RQ2 with the feature matrix and confirmed-loss/measurement-error cases, and RQ3 with cross-pipeline differences. Do not include a validator RQ in the core results.

    ## 6. Discussion

    Discuss converter-dependent behavior, preservation versus destination accessibility, practical interpretation without user-impact overclaiming, and the narrow contribution.

    ## 7. Threats to validity

    Cover synthetic fixtures, single instances, cloud versioning, PDF representation ambiguity, parser limits, limited converter coverage, no user study, and unequal feature complexity.

    ## 8. Future work

    Discuss justified fixture variants, integrated documents, systematic validators, additional converters, and disabled-user evaluation.

    ## 9. Conclusion

    Restate only the evidence-supported claim that known accessibility information can be measured across real conversion pipelines and is not uniformly preserved in the tested cases.
    """)

    write("PAPER_THESIS.md", """
    # Paper Thesis Candidates

    1. Accessible source documents do not necessarily retain all of their accessibility information during conversion, and source-grounded comparison can reveal preservation changes that destination-only assessment cannot reconstruct.
    2. A controlled source-grounded benchmark makes it possible to measure feature-specific accessibility preservation across real DOCX-to-PDF conversion pipelines.
    3. In the tested DOCX-to-PDF conditions, accessibility preservation was feature-specific: the same source corpus produced preserved, partial, altered, lost, and measurement-limited outcomes.
    4. Destination PDFs may be structurally tagged while still failing to preserve particular source accessibility properties, making preservation fidelity a distinct measurement target.
    5. Comparing verified source accessibility information with destination PDF structure provides a reproducible way to study conversion behavior without treating a destination-only validator as the preservation oracle.
    """)

    write("PAPER_TITLE_OPTIONS.md", """
    # Paper Title Options

    1. A11yPreserve: Measuring Accessibility Preservation Across DOCX-to-PDF Conversion Pipelines
    2. A11yPreserve: Source-Grounded Testing of Accessibility Preservation in Document Conversion
    3. What Happens to Accessibility Information During DOCX-to-PDF Conversion?
    4. Measuring Source Accessibility Preservation in Real DOCX-to-PDF Pipelines
    5. From Accessible DOCX to Tagged PDF: A Source-Grounded Preservation Benchmark
    6. A11yPreserve: Differential Analysis of Accessibility Information Across Document Conversion
    7. Beyond Tagged Output: Measuring Accessibility-Information Preservation in DOCX-to-PDF Conversion
    8. A Controlled Benchmark for Accessibility Preservation Across DOCX-to-PDF Pipelines

    Titles should retain the DOCX-to-PDF scope. The framework may generalize, but the completed experiment does not evaluate every document format or converter.
    """)

    write("PAPER_READINESS.md", """
    # READY TO WRITE PAPER

    ## Frozen corpus

    13 controlled DOCX fixtures are frozen, hash-verified, and independently checked through manifest, raw OOXML, and source-extractor agreement.

    ## Frozen experiment

    26 genuine DOCX-to-PDF outputs are frozen: 13 LibreOffice and 13 Google Docs. All are parseable, non-empty, tagged, and validated. Microsoft Word is explicitly excluded from the denominator.

    ## Final outcome counts

    11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, and 1 MEASUREMENT_ERROR. There are 25 classifiable/determined outcomes after excluding the measurement error.

    ## Confirmed LOST cases

    F06 / Google Docs / inline language and F11 / Google Docs / footnote association are independently confirmed lost under their frozen contracts.

    ## Measurement error

    F11 / LibreOffice remains a measurement error because `/Note` structure is present but the current extraction evidence cannot resolve note-body association.

    ## Final RQs

    RQ1: extent of preservation; RQ2: property-level preserved/partial/altered/lost outcomes; RQ3: differences between the tested LibreOffice and Google Docs pipelines. Validator comparison is future work.

    ## Final contribution statements

    The paper can claim a source-grounded preservation method, a verified 13-fixture DOCX benchmark, a11ydiff with provenance-traceable comparison, and a scoped 26-output empirical study.

    ## Novelty statement

    The defensible gap is narrow: measuring whether known source accessibility information survives specific DOCX-to-PDF pipelines. The project does not claim to be the first accessibility-conversion benchmark, tagging system, or validator.

    ## Main limitations

    Single instances per feature family, synthetic atomic fixtures, two pipelines, cloud-version dependence, PDF representation/parser ambiguity, unequal feature complexity, and no disabled-user study.

    ## Validator role

    FUTURE WORK. Validator evidence is incomplete and is not part of the core RQs.

    ## Claims supported

    The tested pipelines did not uniformly preserve source accessibility information; outcomes varied by feature and pipeline; tagged destination output did not fully characterize source-information fidelity; and source-grounded comparison was technically feasible.

    ## Claims prohibited

    No general converter ranking, population-wide generalization, universal claim about Google Docs or LibreOffice, universal user-impact claim, complete accessibility-checker claim, or attribution of every Google result to PDF export alone.

    ## Remaining documentation issues

    No blocking issues remain for paper writing. Future experiment freezes should record a test-results hash in addition to source/output/classification hashes. The manuscript should preserve feature-level reporting and the end-to-end Google pipeline wording.

    ## Final recommendation

    The project is ready to write the paper. Do not modify frozen experiment evidence or launch additional experiments as a prerequisite for manuscript drafting.
    """)

    print(json.dumps({"status": "READY TO WRITE PAPER", "documents": 21, "fixture_rows": len(CORPUS["fixtures"]), "matrix_rows": len(DIFF)}))


if __name__ == "__main__":
    main()
