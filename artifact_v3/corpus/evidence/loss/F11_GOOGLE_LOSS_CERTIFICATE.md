# Loss certificate: F11 footnote association / Google Docs pipeline

Final status: **LOST**; evidence status: **INDEPENDENTLY_CONFIRMED_ABSENCE**.

Source evidence is present in `contracts/F11_FOOTNOTES.json`, the frozen
manifest, `word/document.xml/w:footnoteReference`,
`word/footnotes.xml`, and `evidence/source/F11_FOOTNOTES_certificate.json`:
footnote ID 1 has the body “This note records the source-to-note association.”
and is explicitly associated with the source sentence.

The destination is a valid, tagged, one-page PDF and visibly contains the
reference marker and note body. However, Path A (pypdf structure traversal) and
Path B (PyMuPDF serialized-object scan) both find no `/Note`, `/Footnote`, or
equivalent `/Link` association structure. The visible note text is therefore
not evidence that the source footnote association survived as machine-verifiable
PDF structure. The LibreOffice output supplies a structural `/Note` example,
showing that the destination format can express the contract, although its own
association measurement remains ambiguous.

The loss claim is limited to the machine-verifiable footnote association. It
does not claim absence of visible content, complete PDF inaccessibility, user
harm, or causation by PDF export alone. Confidence is high for the inspected
contract-level absence, with the usual residual uncertainty about unobserved
internal application state.
