# V6 pipeline comparability

| Condition | Route | Version/settings | What is controlled | What is not controlled | Valid inference |
|---|---|---|---|---|---|
| LibreOffice V4 | Local headless `soffice.com` DOCX -> PDF | 26.2.6.3; `UseTaggedPDF=true; PDFUACompliance=true; SelectPdfVersion=1` (PDF/A-1b interpretation) | Input hashes, local executable, isolated profile, export options | Version-specific implementation details | Descriptive source-preservation observations for the named local condition |
| Google Docs V4 | Authenticated browser upload/import -> internal representation -> PDF download | Chrome/browser and observed producer recorded; cloud backend not pin-able | Exact DOCX inputs, workflow, timestamps, output hashes | Import service version, internal representation, export backend configuration | Descriptive end-to-end Google Docs import/export observations; no stage-level attribution |
| LibreOffice V5 profile B | Local headless export | `SelectPdfVersion=0`, tagging/PDF-UA flags retained | Same 65 inputs, comparator, analysis | Serialization/profile differences | Robustness comparison within LibreOffice; 65/65 valid and zero classification changes, not product ranking |
| Microsoft Word | Post-freeze supplementary local GUI route | Recorded separately in V4 manifests | Same 65 source fixtures | Not in primary freeze or balanced against the two primary routes | Supplementary observations only; excluded from the 130 primary denominator |

The profile-B result is machine-derived from `65` outputs with `0` classification changes. It supports a within-LibreOffice robustness statement, not causal attribution between LibreOffice and Google Docs. The Google condition must be described as an end-to-end import/export pipeline; the current evidence cannot localize failures to import, internal representation, or PDF generation.
