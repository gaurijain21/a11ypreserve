# PDF parser triangulation

Three difficult frozen outputs were examined through two independent paths:

- Path A: pypdf object-model traversal of the Catalog, StructTreeRoot,
  RoleMap, ParentTree, structure-element hierarchy, attributes, `/Lang`,
  `/Alt`, `/ActualText`, MCID references, and page annotations.
- Path B: PyMuPDF page/text/link extraction plus direct serialized-object scans
  across the PDF xref table for the same structural markers.

The generated machine-readable evidence is
`final_strengthening/PDF_PARSER_TRIANGULATION.json`.

| Case | Path-A result | Path-B result | Interpretation |
|---|---|---|---|
| F06/Google Docs | StructTreeRoot and ParentTree exist; no `es-MX` or inline language node | Same marker absence; visible “Buenos días” text is present | Confirmed absence of the required inline language representation, not absence of visible text |
| F11/Google Docs | StructTreeRoot and ParentTree exist; no Note/Footnote/Link structure | Same marker absence; note body is visible as ordinary page text | Confirmed absence of the required machine-verifiable footnote association, while acknowledging visible text survival |
| F11/LibreOffice | `/Note` node exists with nested label/link/standard nodes; note-body association text is not recovered | `/Note` object exists; page text exposes the reference but not the note body | Measurement remains ambiguous; frozen `MEASUREMENT_ERROR` is retained |

The triangulation does not claim complete PDF semantics. It establishes
independent corroboration for the two confirmed losses and an explicit
measurement boundary for F11/LibreOffice. Absence from a single extracted
encoding is not treated as semantic absence for the partial cases.
