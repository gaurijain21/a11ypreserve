# Standards and Requirements

## Normative anchor

Conversion is not merely a new output-file linting problem. Authoring/conversion guidance requires preservation of accessibility information when the destination supports an equivalent mechanism, and requires warnings or checks when it does not.

| Source | Requirement extracted | Test implication |
|---|---|---|
| [ATAG 2.0 B.1.2.1](https://www.w3.org/TR/ATAG20/) | Restructuring/recoding transformations preserve accessibility information when equivalent destination mechanisms exist, or provide warning/checking. | Compare source and destination semantics, and record unsupported/unknown separately. |
| [ATAG 2.0 B.1.2.4](https://www.w3.org/TR/ATAG20/) | Preserve text alternatives for preserved non-text content when an equivalent mechanism exists. | Alt text must be matched by identity/position and classified as preserved, mutated, lost or regenerated. |
| [Section 508, 504.2.1](https://www.access-board.gov/ict/) | Converting or saving in multiple formats shall preserve accessibility information to the extent supported by the destination. | Every edge needs a destination capability map; “not representable” is not the same as converter failure. |
| [Section 508, 504.2.2](https://www.access-board.gov/ict/) | PDF export tools must be capable of PDF/UA-1 export where applicable. | PDF export is a route-specific requirement, not proof that source semantics survived. |
| [EN 301 549 11.8.3](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf) | Accessibility information shall be preserved in restructuring/recoding transformations if equivalent mechanisms exist. | Record the transformation type and equivalence decision. |
| [WCAG 2.2](https://www.w3.org/TR/wcag/) | Relevant output semantics include text alternatives, info/relationships, headings/labels and language. | Use a feature manifest, not a single accessibility score. |
| [EPUB Accessibility 1.1](https://www.w3.org/TR/epub-a11y-11/) | EPUB accessibility metadata and discoverability/conformance are destination requirements. | Treat EPUB metadata and content semantics separately. |
| [PDF/UA overview](https://pdfa.org/accessibility) | Tagged PDF has destination-specific structural rules under ISO 14289/ISO 32000. | A tagged PDF is not automatically evidence that source intent was preserved. |

## Required model

Each feature result must include source value, output value, converter/route, evidence artifact, confidence, and one of:

`PRESERVED`, `DEGRADED`, `LOST`, `MUTATED`, `REGENERATED`, `NOT_REPRESENTABLE`, `NOT_APPLICABLE`, `INVALID_CONVERSION`, `MEASUREMENT_ERROR`.

The comparator must never turn an unimplemented parser into `LOST`. In the pilot, a tagged PDF with no PDF structure parser is `MEASUREMENT_ERROR`, not proof that headings, lists, tables, or alt text vanished.

