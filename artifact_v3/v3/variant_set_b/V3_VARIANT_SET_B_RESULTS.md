# Variant Set B final results

## Scope and completion

Variant Set B contains 13 pre-specified controlled DOCX fixtures, one for each selected feature family. The separately implemented raw-OOXML source oracle passed 13/13. LibreOffice converted 13/13 and the authenticated Google Docs DOCX-to-PDF conversion pipeline produced 13/13 valid, tagged PDFs.

The Google outputs were saved through the in-session Google export backend after the visible download action did not register for B01 despite retries. This route deviation is recorded in `v3/variant_set_b/google/CONVERSION_REPORT.json`; no print-to-PDF, screenshot, or manual accessibility repair was used.

## Evidence-aware rows

The final 26-row Variant B matrix is in `V3_VARIANT_SET_B_FINAL_RESULTS.md` and `V3_VARIANT_SET_B_FINAL_RESULTS.json`. Counts are 7 verified preserved, 1 observed partial, 4 altered, 2 confirmed lost, and 12 unresolved equivalence. There is no Variant B measurement-error row.

The two confirmed-loss rows are B06/Google inline language and B11/Google footnote association. Their evidence is separately audited in `google/DIFFICULT_CASE_AUDIT.json`. Unresolved rows are conservative abstentions and are not reported as failures.

## Interpretation boundary

The arm is a secondary robustness observation. It does not establish within-feature invariance, prevalence, a converter ranking, or general behavior across DOCX documents, software versions, or Google backend versions.
