# F06 Google Docs exhaustive loss re-audit

## Contract

The source contract requires the `Buenos días` run to retain an `es-MX` inline language override inside an `en-US` document. The claim is limited to the machine-verifiable inline-language representation.

## Destination search

The stored loss certificate and parser-triangulation record were re-read. The audit searches both the pypdf object model and PyMuPDF/serialized objects for: catalog `/Lang`; structure-element `/Lang` including inherited values; `/ActualText`; `Span`/language-bearing structure; `RoleMap`; `StructTreeRoot`; `ParentTree`; MCID-bearing content; annotations; and raw serialized `es-MX`/language tokens. The PDF is also checked for visible text separately.

## Findings

- The Google output has a tagged structure tree and a document-level language value, but no target-bound `es-MX` inline span was found.
- The visible phrase `Buenos días` remains; visible text is not the contracted language association.
- No `/ActualText` or alternate text encoding carrying the required `es-MX` value was found.
- A second parser/object path agrees with the primary traversal.

## Decision

The absence claim survives at the contract level: `CONFIRMED_LOST` for the machine-verifiable inline-language property. This does not identify the internal stage responsible, does not claim PDF-export-only causation, and does not claim user harm.

