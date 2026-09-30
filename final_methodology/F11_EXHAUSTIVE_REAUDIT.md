# F11 Google Docs exhaustive loss re-audit

## Contract

The source contract requires a native footnote reference, note body, and machine-verifiable association. The claim is limited to that association.

## Destination search

The stored loss certificate and parser-triangulation record were re-read. The audit searches the Google PDF's `StructTreeRoot`, `RoleMap`, `ParentTree`, MCID references, structure elements, `/Note`, `/Reference`, `/Link`, `/Annot`, annotation actions, object streams, raw serialized objects, page-text order, and possible reference/body/backlink patterns. It separately confirms that the visible marker and note text remain.

## Findings

- The Google PDF contains the visible reference marker and note body.
- No `/Note`, `/Footnote`, or equivalent machine-verifiable reference/body association was found through the stored pypdf traversal, PyMuPDF/object scan, or serialized-object search.
- The comparison is not based solely on a missing text extraction field: the alternate object path and a pipeline comparator output are consistent with absence of the required association.
- The LibreOffice output demonstrates that a comparable tagged-note representation is expressible, but its own note-body association remains unmeasured and is retained as `MEASUREMENT_ERROR`.

## Decision

The Google result survives as `CONFIRMED_LOST` for the machine-verifiable footnote association. It is not a claim that note text disappeared, that the Google backend's internal stage is known, or that a user necessarily experienced harm.

