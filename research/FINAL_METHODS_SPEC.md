# Final Methods Specification

## Research objective

A11yPreserve measures whether accessibility information explicitly present in a controlled source document survives conversion into a destination representation. The method compares verified source properties with independently extracted destination structure; it does not reduce the question to whether the destination passes a general accessibility checker.

## Source corpus

The corpus contains 13 small, atomic DOCX fixtures covering headings, alternative text, lists, tables, language, decorative images, hyperlinks, metadata, complex table headers, footnotes, equations, and captions. Fixtures were created by controlled scripts using native WordprocessingML constructs where needed. Atomic design isolates a target property and limits incidental layout effects.

## Ground truth

Each fixture entered the frozen corpus only when its machine-readable manifest, raw OOXML inspection, and source extractor's ASIR agreed on the target property. This establishes encoded source ground truth; it is not a claim of panel-based expert or disabled-user validation.

## Conversion pipelines

The first condition used LibreOffice 26.2.6.3, build `8221e31b3ac356a1623c672912a3d2b492f7e3d1`, on Windows `10.0.26200.0`. Conversion used native headless `soffice.com writer_pdf_Export` with `UseTaggedPDF=true`, `PDFUACompliance=true`, and `SelectPdfVersion=1`. The second condition was the authenticated Google Docs DOCX-to-PDF conversion pipeline on the same Windows environment with Chrome 153.0.8010.53: upload the exact frozen DOCX and select File -> Download -> PDF Document. The Google condition includes import, internal representation, and PDF generation; the experiment does not isolate those stages. Microsoft Word was excluded because it was not a completed primary pipeline.

## Destination extraction

All 26 outputs were checked for existence, non-zero size, parseability, expected page count, structural tagging, and a PDF structure tree. Extraction inspected roles and structures relevant to each contract, including headings, figure `/Alt`, list containers and `/ListNumbering`, tables and header cells, `/Lang`, link annotations, metadata, `/Note`, `/Formula`, and `/Caption`. Poppler `pdftotext` and raw object inspection were used as independent checks where marked-content or association evidence was incomplete.

## a11ydiff

`a11ydiff` pairs the source contract and ASIR with destination extraction records. It records exact source and destination values, representation type, evidence paths, and a conservative outcome. It is a comparison component, not a general PDF accessibility checker.

## Classification rules

- **PRESERVED:** exact or contractually equivalent accessibility information is present.
- **PARTIALLY PRESERVED:** a defined subset survives, but a required sub-property is absent or not independently established.
- **ALTERED:** related accessibility information remains, but author-relevant value or structure changes.
- **LOST:** the source feature is verified, the destination can represent it, and independent checks find no equivalent destination information.
- **MEASUREMENT ERROR:** available evidence cannot establish preservation or loss without forcing an unsupported conclusion.

`NOT_REPRESENTABLE` and `INVALID_CONVERSION` are methodological safeguards and did not occur in the frozen primary result set.

## Independent verification

Non-preserved cases were reviewed against source OOXML, manifests, source ASIR, output validation, primary PDF extraction, raw PDF structure, and independent text/object checks. The two LOST cases were retained only after these checks. The LibreOffice F11 footnote case remained a measurement error because `/Note` was present but association could not be resolved.

## Result freezing

Source fixtures and PDF outputs were SHA-256 frozen. Phase 6 independently recomputed all source and output hashes, reconstructed all 26 result rows, and found zero discrepancies with the frozen primary classifications. Provenance links each result from source file and manifest through converter/version, output hash, extraction, comparison, and evidence.

## Secondary validators

No systematic PAC, Acrobat Accessibility Checker, or veraPDF dataset covering all 26 outputs was obtained. Validator comparison is therefore future work and is not part of the core research question or ground truth.
