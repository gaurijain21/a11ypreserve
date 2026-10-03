# Forensic Audit: F06_INLINE_LANGUAGE — Google Docs

Final audit classification: **CONFIRMED_LOST**

## Source evidence

- Manifest: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F06_INLINE_LANGUAGE.json`; manifest ground truth: `{"document_language": "en-US", "runs": [{"text": "Buenos días", "language": "es-MX"}]}`
- Source extraction: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\extracted\source\F06_INLINE_LANGUAGE.json`
- Source value: `[{"text": "Buenos días", "language": "es-MX", "order": 2, "evidence": {"ooxml": "word/document.xml", "element": "w:r/w:rPr/w:lang"}}]`
- Source OOXML/manifest verification was PASS in `corpus/reports/source_verification.json` or the frozen Pilot manifest chain.

## Destination evidence

- PDF: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf`
- Output hash: `81803dfa98d51e57dfa45addf12f92e674986103b440d95d0ed36a123c48ad1e`; parseable/tagged: `True` / `True`; pages: `1`
- Destination extractor: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\extracted\google_docs\F06_INLINE_LANGUAGE.json`
- Destination value: `[]`
- Independent raw/PDF-text check: The PDF is tagged and valid; its catalog language is `en`, but raw PDF bytes contain `es-MX`: `False`. The PDF structure has `/Lang`: `True`, but no `es-MX`; the independent pdftotext output contains the phrase but, as expected, no language span.

## Contract and alternative explanations

- Contract check: The frozen F06 contract defines loss when the inline span/language is absent while PDF can represent language on a marked structure span.
- This is not INVALID_CONVERSION: the file parses, contains content, and has a StructTreeRoot.
- This is not NOT_REPRESENTABLE: the PDF structure vocabulary can express the feature, and the other real engine produced a corresponding structure for comparison.
- This is not merely an encoding difference: the required semantic span/association is absent, not merely serialized differently.
- This is not a parser-only result: raw-byte markers and an independent text extractor corroborate the absence of the required destination structure/content.

## Final disposition

**CONFIRMED_LOST**
