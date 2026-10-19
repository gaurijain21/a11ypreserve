# V5 environment and converter provenance

This report separates what is pinned locally from what is observable but not
pin-able for the cloud service. V4 records remain unchanged.

| Converter | Version/build | Route and relevant settings | Producer / reproducibility boundary |
|---|---|---|---|
| LibreOffice | `26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1` | Headless `soffice.com`, `writer_pdf_Export`, isolated profile. V4: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1` (PDF/A-1b). V5 B: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=0` (default PDF 1.7). | Local executable and OS are recorded in each manifest; producer is recorded in PDF metadata. |
| Google Docs | Web application; backend not pin-able | Authenticated Chrome UI: DOCX upload/import, then `File → Download → PDF Document (.pdf)`. V4 records Chrome `154.0.8037.97`, Windows build, timestamps, source/output hashes, and producer. | Observed producer: `Skia/PDF m156 Google Docs Renderer`. Import into Google’s internal representation is part of the system under test; backend drift is a remaining reliability threat. |
| Microsoft Word | Microsoft 365 O365ProPlusRetail x64 build `16.0.20430.20092` | Native GUI `File → Export → Create PDF/XPS`; Standard optimization; Document structure tags enabled; no print-to-PDF or post-processing. | Observed producer: `Microsoft® Word for Microsoft 365`. COM activation failure `0x80070520` is recorded separately from the successful GUI converter route. Word remains supplementary/post-freeze. |

All conditions use the frozen DOCX input hashes. Output records retain PDF hashes, parseability, page count, tagging observation, producer, timestamps, and route. Google account credentials/browser state are not distributed. V5 does not claim backend reproducibility beyond the recorded session and temporal evidence.

Authoritative LibreOffice references used for the profile interpretation:

- [LibreOffice PDF CLI parameters](https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html): `SelectPdfVersion=0` is PDF 1.7 and `1` is PDF/A-1b; `PDFUACompliance` and `UseTaggedPDF` are separate properties.
- [LibreOffice PDF exporter source](https://github.com/LibreOffice/core/blob/master/filter/source/pdf/pdfexport.cxx): the exporter maps selection 1 to `PDF_A_1`, selection 0 to the default PDF version, and enables tagged/PDF/UA behavior through distinct flags.
