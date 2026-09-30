# Partial Evidence Review

## Frozen-result rule

The frozen primary classifications were not changed. PARTIALLY_PRESERVED remains the reported outcome category for all nine original partial cases. The table below is a separate evidence-status overlay, not a replacement taxonomy.

| Frozen case | Evidence status | Review disposition |
|---|---|---|
| F01 / Google Docs | OBSERVED_PARTIAL | Raw destination heading roles contain an extra H1, so the level/order contract differs from the source. |
| F03 / Google Docs | UNRESOLVED_EQUIVALENCE | List containers, items, and nesting survive, but ordered/unordered type is not independently established by the available PDF evidence. |
| F07 / LibreOffice | OBSERVED_PARTIAL | The meaningful image's author-provided alternative text is visibly prefixed, and the compound decorative contract is not fully retained. |
| F07 / Google Docs | OBSERVED_PARTIAL | Both independent PDF paths show the informative Figure and a second Figure with empty `/Alt`; no `/Artifact` representation is present. The bounded observation is a non-canonical decorative representation, not a universal claim about user impact. |
| F08 / LibreOffice | UNRESOLVED_EQUIVALENCE | URI/link annotation survives, but visible link-name association is not independently recoverable from the structural extraction. |
| F08 / Google Docs | UNRESOLVED_EQUIVALENCE | Same limitation as LibreOffice; the annotation is present but the cross-format association is not established. |
| F10 / Google Docs | UNRESOLVED_EQUIVALENCE | Table and header roles plus spans are present, but complete multi-level header associations are not established. |
| F12 / Google Docs | UNRESOLVED_EQUIVALENCE | The equation is visible in page content, but no machine-readable math structure was extracted; an alternative equivalent representation cannot be ruled out by this evidence alone. |
| F14 / Google Docs | UNRESOLVED_EQUIVALENCE | Caption text and ordered page-text adjacency survive, but a semantic figure/caption association is not established. |

## Measurement-error boundary

None of these nine partial cases is promoted to MEASUREMENT_ERROR. F11 / LibreOffice remains the only MEASUREMENT_ERROR because a `/Note` structure is present but the note-body association cannot be resolved with the available structural and independent text evidence.

## Interpretation repair

The paper now states that absence from one extracted encoding is not automatically proof of semantic absence. Partial outcomes therefore mix definite contract differences with unresolved cross-format equivalence, and the evidence status is reported separately so that the frozen primary category is not mistaken for a uniform degree of certainty.
