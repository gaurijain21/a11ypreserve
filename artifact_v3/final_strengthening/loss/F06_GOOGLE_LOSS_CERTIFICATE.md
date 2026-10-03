# Loss certificate: F06 inline language / Google Docs pipeline

Final status: **LOST**; evidence status: **INDEPENDENTLY_CONFIRMED_ABSENCE**.

Source evidence is present in `contracts/F06_INLINE_LANGUAGE.json`, the frozen
manifest, `word/document.xml`, and `evidence/source/F06_INLINE_LANGUAGE_certificate.json`:
the text “Buenos días” carries an explicit `w:rPr/w:lang` value of `es-MX`
inside an `en-US` document.

The destination is a valid, tagged, one-page PDF. It contains the visible
phrase, a StructTreeRoot, a ParentTree, and catalog language `en`; the other
real pipeline demonstrates that a PDF structure can carry a corresponding
inline language representation. The primary extractor reports no inline
language node. Path A (pypdf) and Path B (PyMuPDF plus serialized-object scan)
both find no `es-MX`, no `/Lang` span carrying `es-MX`, and no alternative
`/ActualText` or equivalent language marker. Independent page-text extraction
confirms that the phrase survives only as visible text.

The loss claim is therefore limited to the machine-verifiable inline language
contract. It does not claim that the entire document is inaccessible, that a
screen reader necessarily fails, or that the PDF export stage alone caused the
behavior; the tested unit is the end-to-end Google Docs DOCX-to-PDF conversion
pipeline. Remaining uncertainty is limited to undocumented internal semantics
that are not serialized in the inspected PDF; confidence in the contract-level
absence is high.
