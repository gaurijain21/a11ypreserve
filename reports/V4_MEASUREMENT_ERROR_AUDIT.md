# V4 LibreOffice Measurement-Error Audit

This is a post-freeze diagnostic audit. The five frozen LibreOffice `MEASUREMENT_ERROR` classifications remain unchanged.

All five cases are the footnote family: F11_A, F11_B, F11_C, F11_D, and F11_E.

## Evidence

- Source OOXML contains one declared footnote with body text `One note body.` and a `w:footnoteReference`.
- Each LibreOffice PDF is valid, tagged, and contains a `/Note` structure with child object references.
- The pypdf destination extraction recovers a `/Note` role but an empty note text field.
- PyMuPDF recovers the visible document text and the footnote marker, but not a source-reference-to-note-body association.
- Raw PDF scans show `/StructTreeRoot`, `/ParentTree`, `/Note`, and list/label structure. They do not independently establish the required note-body association.
- `pdfinfo` confirms tagged, unencrypted, parseable PDFs. The available MiKTeX `pdftotext` executable was attempted but blocked by its first-run directory setup; PyMuPDF was the usable independent text path.
- qpdf, mutool, and veraPDF were not installed in the environment.

## Disposition

The cases remain `MEASUREMENT_ERROR`. The evidence establishes that the output is a valid tagged PDF with a note-like structure, but does not establish whether the source reference and note body are semantically associated under the frozen contract. Forcing these cases to preserved or lost would exceed the evidence boundary. This is an extractor/format-representation limitation, not evidence of malformed conversion.
