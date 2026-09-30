# Claims Supported

- Accessibility information was not uniformly preserved across the two tested DOCX-to-PDF pipelines.
- The same frozen source fixture sometimes produced different preservation outcomes across the LibreOffice and Google Docs pipelines.
- Tagged destination PDFs could retain accessibility structure while particular source properties were partially preserved, altered, or lost.
- Source-grounded comparison exposed changes that destination-only inspection cannot reconstruct as source-preservation facts.
- A controlled source-grounded preservation benchmark is technically feasible.

# Claims Not Supported

The manuscript must not claim that all converters lose accessibility, that Google Docs is generally less accessible, that LibreOffice is generally better, that results generalize to all DOCX files or software versions, that every change affects screen-reader users in the same way, that all altered information causes practical harm, that `a11ydiff` measures complete accessibility, that destination validators are defective, that PDF caused every change, or that PDF export alone caused every Google-pipeline change.
