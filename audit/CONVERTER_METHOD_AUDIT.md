# Converter Method Audit

- LibreOffice used native `soffice.com writer_pdf_Export` with `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`. Output metadata and tagged structure were inspected.
- Google Docs used authenticated UI import of each exact frozen DOCX followed by File → Download → PDF Document. The resulting PDFs identify the Google renderer; no print-to-PDF route was used.
- All 26 source hashes match the frozen corpus; no PDF was fabricated, repaired, manually tagged, or post-processed.
- The two workflows are legitimate but not identical: LibreOffice is local/headless and Google Docs is a cloud import/export pipeline. That difference is part of the experiment and is recorded rather than normalized away.
