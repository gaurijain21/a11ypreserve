# V5 LibreOffice export-profile audit

## Authoritative interpretation

LibreOffice documents `SelectPdfVersion=1` as **PDF/A-1b** and `0` as the
default **PDF 1.7** selection. The exporter source separately handles
`UseTaggedPDF` and `PDFUACompliance`; selecting PDF/A-1b also forces tagged
output and applies archival restrictions. Therefore the V4 LibreOffice arm
was not ordinary tagged PDF/UA-only export: it was a PDF/A-1b + tagged/PDF-UA
condition.

## V5 robustness condition

V5 condition B retains the same frozen 65 DOCX inputs, source contracts,
extractor, comparator, and classification taxonomy while using
`UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=0`. Its outputs and
manifest are under `experiments/v5/conversions/libreoffice_profile_b/`; the
derived analysis is `experiments/v5/LIBREOFFICE_PROFILE_B_ANALYSIS.json`.

The report must be read together with the machine-derived counts in that JSON:
per-fixture classification changes, per-family changes, PDF header/profile
markers, tagging, producer, and measurement errors. V4 output and labels are
not overwritten.

## Measured result

The completed run produced 65/65 valid PDFs. Condition B is classified as
**A. NO MATERIAL EFFECT** for the frozen semantic classifier: the V5 counts are
38 VERIFIED_PRESERVED, 11 OBSERVED_PARTIAL, 9 ALTERED, 1 CONFIRMED_LOST,
1 UNRESOLVED_EQUIVALENCE, and 5 MEASUREMENT_ERROR, with zero classification
changes relative to V4. All 65 outputs were tagged, and the raw PDF/A marker
totals were zero (`SelectPdfVersion=0` produced normal PDF 1.7 output rather
than PDF/A markers). This is a condition result, not evidence that the two
profiles are byte-identical or that all PDF/UA requirements are satisfied.

The condition is not directly comparable to Google Docs or Word as a product
ranking: it is a robustness comparison isolating one LibreOffice export
setting. The end-to-end primary question remains source-contract preservation.
