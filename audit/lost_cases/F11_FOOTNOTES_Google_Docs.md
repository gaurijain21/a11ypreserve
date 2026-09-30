# Forensic Audit: F11_FOOTNOTES — Google Docs

Final audit classification: **CONFIRMED_LOST**

## Source evidence

- Manifest: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F11_FOOTNOTES.json`; manifest ground truth: `{"notes": [{"kind": "footnote", "reference_text": "The benchmark uses an explicit footnote association.", "id": 1, "text": "This note records the source-to-note association."}]}`
- Source extraction: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\extracted\source\F11_FOOTNOTES.json`
- Source value: `[{"kind": "footnote", "id": 1, "text": "This note records the source-to-note association.", "evidence": {"ooxml": "word/footnotes.xml", "reference": "word/document.xml/w:footnoteReference"}}]`
- Source OOXML/manifest verification was PASS in `corpus/reports/source_verification.json` or the frozen Pilot manifest chain.

## Destination evidence

- PDF: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F11_FOOTNOTES__GOOGLE_DOCS.pdf`
- Output hash: `91b81c06383c1c681023b3cd0a9c05cc9c4178bd696ad83287082d020f7372b9`; parseable/tagged: `True` / `True`; pages: `1`
- Destination extractor: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\extracted\google_docs\F11_FOOTNOTES.json`
- Destination value: `[]`
- Independent raw/PDF-text check: The PDF is tagged and valid; raw PDF markers `/Note`: `False`, `/Footnote`: `False`, `/Link`: `False`. pypdf extraction reports no footnotes. Independent page-text extraction does contain the visible note body, so the loss claim is specifically the machine-verifiable reference-to-note association, not disappearance of visible note text.

## Contract and alternative explanations

- Contract check: The frozen F11 contract defines loss when the note body or reference/association disappears; a tagged PDF `/Note`/link representation is available in the other engine output and in the PDF structure model.
- This is not INVALID_CONVERSION: the file parses, contains content, and has a StructTreeRoot.
- This is not NOT_REPRESENTABLE: the PDF structure vocabulary can express the feature, and the other real engine produced a corresponding structure for comparison.
- This is not merely an encoding difference: the required semantic association is absent even though the visible note body survives as ordinary page text.
- This is not a parser-only result: pypdf structure traversal and PyMuPDF serialized-object inspection independently find no `/Note`, `/Footnote`, or equivalent association marker.

## Final disposition

**CONFIRMED_LOST**
