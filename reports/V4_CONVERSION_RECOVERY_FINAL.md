# V4 Conversion Recovery Final

Date: 2026-10-04

## Decision

**GO WITH LIMITATIONS for the recovered V4 LibreOffice arm; V4 does not replace V3 as the repository’s primary submission evidence.**

One legitimate converter pipeline produced a complete, validated V4 corpus and frozen analysis. Google Docs remains unrun because the authenticated browser session requires just-in-time authorization before transmitting a local DOCX; Word failed before conversion. The one-pipeline V4 result is valid and useful, but it is not a like-for-like replacement for V3’s two-pipeline evidence.

## Provenance

- Pre-conversion baseline commit: `7abddc7ee5f25c245e445fdc953ae1add83b6ef0`
- V4 protocol freeze commit: `41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1`
- Protocol hash: `B4A2F974B7E14CB6C5847EB8667BF3A7E9CDF5C38C60AFE9C47391F476648556`
- Source-manifest hash: `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7`
- Comparator hash: `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4`
- Source-oracle hash: `7B5C309D80BD2DC32438A8EACE499ED145A0BF77E880616A0AA0875935EC1DE6`
- Destination-extractor hash: `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7`

## Pipeline results

| Pipeline | Attempted | Successful outputs | Primary cases analyzed | Result |
|---|---:|---:|---:|---|
| LibreOffice 26.2.6.3 | Yes | 65 atomic + 10 realistic | 65 | Complete |
| Google Docs | Browser/authentication checked; upload not authorized | 0 | 0 | Pending explicit upload confirmation |
| Microsoft Word | Direct launch/COM recovery attempted | 0 | 0 | Failed before pilot conversion: `0x80070520` |

LibreOffice used the reconstructed V3 route: bundled `soffice.com`, isolated per-fixture profiles, `writer_pdf_Export`, `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`. All 75 manifest records succeeded; all outputs were parseable, `%PDF-`, timestamped after conversion start, source-hash matched, tagged, and produced by `LibreOffice 26.2.6.3 (X86_64)`.

## Frozen analysis

LibreOffice atomic counts, 65/65 cases:

- `VERIFIED_PRESERVED`: 38
- `OBSERVED_PARTIAL`: 11
- `ALTERED`: 9
- `CONFIRMED_LOST`: 1
- `UNRESOLVED_EQUIVALENCE`: 1
- `MEASUREMENT_ERROR`: 5

Holdout D/E counts, 26/26 cases:

- `VERIFIED_PRESERVED`: 14
- `OBSERVED_PARTIAL`: 5
- `ALTERED`: 4
- `CONFIRMED_LOST`: 1
- `MEASUREMENT_ERROR`: 2
- `UNRESOLVED_EQUIVALENCE`: 0

Development A-C counts, 39/39 cases:

- `VERIFIED_PRESERVED`: 24
- `OBSERVED_PARTIAL`: 6
- `ALTERED`: 5
- `MEASUREMENT_ERROR`: 3
- `UNRESOLVED_EQUIVALENCE`: 1

Realistic corpus: 10 project-created documents, 78 property-contract observations, 53 preserved, 5 partial, 15 altered, and 5 measurement errors. This remains a project-created realistic/integrated corpus, not a real-world corpus.

Unresolved/measurement cases were not silently dropped: F13_C is `UNRESOLVED_EQUIVALENCE` because caption loss was not independently corroborated; F11_A–F11_E are `MEASUREMENT_ERROR` because the PDF `/Note` structure was present but the frozen marked-content extraction could not recover note-body association.

## Repeatability

LibreOffice repeatability used the frozen selected set F04_D, F06_D, F08_D, F11_D, F12_D, and F13_D: 6 sources × 3 independent conversions = 18 outputs. Byte identity was 0/6 and extraction identity was 0/6, but classification identity was 6/6. Stable classifications were 4 `VERIFIED_PRESERVED`, 1 `ALTERED`, and 1 `MEASUREMENT_ERROR`.

## Audit status

- Consistency audit: PASS for the new manifest and analysis counts.
- Calibration audit: preserved frozen result, 60 correct, 0 false positives, 5 false negatives, 13 correct unresolved.
- Source-oracle audit: preserved frozen result, 39/39 representative mutations detected.
- Output-provenance audit: PASS, 75/75 successful output records validated.
- Holdout audit: PASS, D/E were analyzed separately after the pre-result freeze.
- Artifact audit: PASS for source/output hashes, extraction records, secondary evidence, and repeatability records.
- Anonymity/provenance audit: no external documents added; realistic documents remain project-created; no V3 output was copied or relabeled.

## Methodology integrity

- No frozen methodology, decision rule, feature family, contract, taxonomy, fixture, protocol, comparator, source oracle, or destination extractor was changed after result inspection.
- Implementation repairs were limited to adding the missing conversion/analysis orchestration and provenance recording.
- No PDF was fabricated, copied from V3, relabeled, manually tagged, screenshot-generated, or print-generated.

## Remaining human action

To add the Google pipeline, one explicit confirmation is still required immediately before uploading a frozen local DOCX to the authenticated Google account. No bulk manual conversion is requested. Word would require a machine with a usable interactive Word session or native GUI-control surface.

## Exact artifacts

- Conversion manifest: `experiments/v4/conversions/libreoffice/manifest.json`
- Frozen analysis: `experiments/v4/conversions/libreoffice/analysis/V4_LIBREOFFICE_ANALYSIS.json`
- Repeatability manifest: `experiments/v4/conversions/libreoffice/repeatability/RUN_MANIFEST.json`
- Repeatability results: `experiments/v4/conversions/libreoffice/repeatability/REPEATABILITY_RESULTS.json`
- V3 reconstruction: `reports/V3_CONVERSION_PATH_RECONSTRUCTION.md`
- Baseline: `reports/V4_CONVERSION_RECOVERY_BASELINE.md`
