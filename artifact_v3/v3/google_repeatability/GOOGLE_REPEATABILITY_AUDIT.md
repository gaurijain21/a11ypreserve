# Google Docs Core repeatability audit

## Design

The historical frozen Google output is Run 1. Runs 2 and 3 were independently uploaded from the same 13 frozen Core DOCX sources through the recorded authenticated workflow. Repeatability is secondary and does not enter the frozen V2 denominator.

## Completion

Run 2: 13/13 valid PDFs.

Run 3: 13/13 valid PDFs.

Total: 13 fixtures x 3 runs = 39 Google conversions.

## Result

All 13 fixtures were `BYTE_IDENTICAL` across Runs 1, 2, and 3. Because the files were byte-identical, the evidence-aware classification remained stable for 13/13 fixtures. The complete per-fixture hashes and class labels are in `REPEATABILITY_RESULTS.json` and `GOOGLE_REPEATABILITY_FINAL.md`.

## Boundary

This is a dated workflow observation, not a guarantee about all future Google Docs service versions or accounts. The backend version cannot be fully pinned. The Core runs used the visible Google Docs File -> Download -> PDF workflow; the separate Variant B arm records a documented in-session export-backend recovery route.
