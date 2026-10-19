# Converter-condition rationale

The two primary conditions are not product-quality rankings.

| Condition | Recorded setup | Interpretation |
|---|---|---|
| LibreOffice | `26.2.6.3`, native headless Writer PDF export, `UseTaggedPDF=true`, `PDFUACompliance=true`, `SelectPdfVersion=1` | A deliberately tagged/PDF-UA-oriented export condition. A default-export condition was not added to the primary denominator. |
| Google Docs | Authenticated upload of the frozen DOCX followed by the recorded PDF download workflow; Variant B used the documented in-session export backend after the visible download action did not register | An end-to-end cloud conversion condition whose import, internal representation, and export stages are not isolated. |

The settings are conceptually different: LibreOffice exposes explicit tagged-export controls, while the Google workflow exposes a file-download route rather than equivalent PDF/UA switches. Results therefore support only condition-specific observations. Variant B's route deviation is retained in `v3/variant_set_b/google/CONVERSION_REPORT.json`.
