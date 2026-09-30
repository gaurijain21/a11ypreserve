# Human Google Docs Conversion Checklist

Status: required because the current browser bridge opens the Google Docs Upload tab but cannot control the native Windows file chooser. No Google Variant Set B or repeatability result is claimed until the downloaded PDFs exist and pass validation.

## Before starting

Use the already authenticated Google Docs account and the existing Google Docs DOCX-to-PDF workflow. Do not change the DOCX files. Keep the experiment date, browser, workflow, and any visible Google Docs version information in the local provenance record. Do not share credentials, cookies, browser profiles, or account metadata.

For every conversion:

1. Open Google Docs.
2. Choose Open file, Upload, and Browse.
3. Select the exact source DOCX listed below.
4. Wait for the document to finish loading.
5. Download it as PDF using the same workflow used for the frozen Core Run 1.
6. Save the downloaded PDF with the exact target filename below.
7. Confirm the file is a non-empty, parseable, tagged PDF before moving to the next file.

## Existing Core Run 1

The historical Core Google outputs are already archived and may be used only as Run 1 after their hashes and provenance are checked by the analysis scripts. Do not overwrite them.

## New Core repeatability runs

Create two genuinely new conversions for each Core fixture. These are Runs 2 and 3; do not copy or rename an earlier PDF.

| Fixture | Source DOCX | Run 2 target PDF | Run 3 target PDF |
|---|---|---|---|
| F01_HEADINGS | `pilot/fixtures/F01_HEADINGS.docx` | `v3/google_repeatability/run2/F01_HEADINGS__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F01_HEADINGS__GOOGLE_DOCS__R3.pdf` |
| F02_ALT_TEXT | `pilot/fixtures/F02_ALT_TEXT.docx` | `v3/google_repeatability/run2/F02_ALT_TEXT__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F02_ALT_TEXT__GOOGLE_DOCS__R3.pdf` |
| F03_LISTS | `pilot/fixtures/F03_LISTS.docx` | `v3/google_repeatability/run2/F03_LISTS__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F03_LISTS__GOOGLE_DOCS__R3.pdf` |
| F04_TABLE | `pilot/fixtures/F04_TABLE.docx` | `v3/google_repeatability/run2/F04_TABLE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F04_TABLE__GOOGLE_DOCS__R3.pdf` |
| F05_DOCUMENT_LANGUAGE | `corpus/fixtures/F05_DOCUMENT_LANGUAGE.docx` | `v3/google_repeatability/run2/F05_DOCUMENT_LANGUAGE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F05_DOCUMENT_LANGUAGE__GOOGLE_DOCS__R3.pdf` |
| F06_INLINE_LANGUAGE | `corpus/fixtures/F06_INLINE_LANGUAGE.docx` | `v3/google_repeatability/run2/F06_INLINE_LANGUAGE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F06_INLINE_LANGUAGE__GOOGLE_DOCS__R3.pdf` |
| F07_DECORATIVE_IMAGE | `corpus/fixtures/F07_DECORATIVE_IMAGE.docx` | `v3/google_repeatability/run2/F07_DECORATIVE_IMAGE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F07_DECORATIVE_IMAGE__GOOGLE_DOCS__R3.pdf` |
| F08_LINKS | `corpus/fixtures/F08_LINKS.docx` | `v3/google_repeatability/run2/F08_LINKS__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F08_LINKS__GOOGLE_DOCS__R3.pdf` |
| F09_DOCUMENT_TITLE | `corpus/fixtures/F09_DOCUMENT_TITLE.docx` | `v3/google_repeatability/run2/F09_DOCUMENT_TITLE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F09_DOCUMENT_TITLE__GOOGLE_DOCS__R3.pdf` |
| F10_COMPLEX_TABLE | `corpus/fixtures/F10_COMPLEX_TABLE.docx` | `v3/google_repeatability/run2/F10_COMPLEX_TABLE__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F10_COMPLEX_TABLE__GOOGLE_DOCS__R3.pdf` |
| F11_FOOTNOTES | `corpus/fixtures/F11_FOOTNOTES.docx` | `v3/google_repeatability/run2/F11_FOOTNOTES__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F11_FOOTNOTES__GOOGLE_DOCS__R3.pdf` |
| F12_EQUATION | `corpus/fixtures/F12_EQUATION.docx` | `v3/google_repeatability/run2/F12_EQUATION__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F12_EQUATION__GOOGLE_DOCS__R3.pdf` |
| F14_CAPTIONS | `corpus/fixtures/F14_CAPTIONS.docx` | `v3/google_repeatability/run2/F14_CAPTIONS__GOOGLE_DOCS__R2.pdf` | `v3/google_repeatability/run3/F14_CAPTIONS__GOOGLE_DOCS__R3.pdf` |

## New Variant Set B Google outputs

Convert each source once using the same workflow. Save exactly:

`v3/variant_set_b/google/outputs/B01__GOOGLE_DOCS.pdf` through `B13__GOOGLE_DOCS.pdf`.

The source files are `corpus/v3_variant_set_b/fixtures/B01.docx` through `B13.docx`. Preserve the source-to-output pairing; do not substitute a Core fixture or an earlier PDF.

## Completion signal

When all 39 new PDFs are present, leave them in the specified directories and tell Codex only that the files are ready. Codex will then hash and validate every PDF, record the conversion provenance, run the frozen oracle, perform the F06/F11 audits, analyze repeatability, and resume the V3 manuscript and final-review work automatically.

If any conversion fails, retain the failure record and do not silently retry under a different workflow. Record the fixture, attempt number, visible error, date/time, and whether a PDF was actually downloaded.

## Automation blocker log — 2026-09-28

The following authorized interaction paths were attempted in the existing authenticated Chrome session:

1. Google Docs home → Open file → Upload opened successfully.
2. The Upload tab was selected through the browser accessibility tree.
3. The Browse button was activated through the browser accessibility tree.
4. Browse was activated again through the browser keyboard action (`Enter`).
5. Browser screenshots and accessibility refreshes were attempted after each activation.
6. Chrome tab inventory and native-app inventory were refreshed after each activation.
7. The browser was reopened/rebound in the same authenticated Chrome profile and the workflow was retried.

The browser bridge retained focus on the web-page Browse button after every attempt. No native Windows Open dialog, Explorer window, filename field, drag target, or file-input binding became available. The available computer-use surface exposes browser-tab controls only in this session; it does not expose a native Windows window handle or mouse/keyboard target for the dialog. No source file was uploaded and no Google PDF is claimed as a result of these attempts.
