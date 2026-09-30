# Cross-Converter Results

This comparison uses the same frozen DOCX source semantics and the same PDF structural extraction for both converters. It does not rank the converters overall.

| Fixture | Feature | LibreOffice fidelity | Google Docs fidelity | LibreOffice accessibility | Google Docs accessibility |
|---|---|---|---|---|---|
| F01_HEADINGS | heading hierarchy | SEMANTICALLY_EQUIVALENT | PARTIAL_PRESERVATION | ACCESSIBLE_EQUIVALENT | ACCESSIBLE_BUT_ALTERED |
| F02_ALT_TEXT | image alternative text | MUTATED | EXACT_PRESERVATION | ACCESSIBLE_BUT_ALTERED | ACCESSIBLE_EQUIVALENT |
| F03_LISTS | list structure | SEMANTICALLY_EQUIVALENT | PARTIAL_PRESERVATION | ACCESSIBLE_EQUIVALENT | DEGRADED_ACCESSIBILITY |
| F04_TABLE | table structure | SEMANTICALLY_EQUIVALENT | SEMANTICALLY_EQUIVALENT | ACCESSIBLE_EQUIVALENT | ACCESSIBLE_EQUIVALENT |

## What Google Docs preserves that LibreOffice does not

For these fixtures, Google Docs preserves the author-written F02 `/Alt` string exactly, while LibreOffice mutates it by adding `Enrollment chart - `.

## What LibreOffice preserves that Google Docs does not

LibreOffice emits explicit PDF `/ListNumbering` attributes (`Disc` and `Decimal`) for the F03 list containers. Google Docs emits the `L`/`LI` nesting but no `/ListNumbering` attribute, so ordered-versus-unordered semantics are not independently established from the PDF structure.

## Is either converter clearly superior overall?

No. The converter behavior is feature-specific: Google Docs is stronger on F02 exact alt-text fidelity, while LibreOffice is stronger on F03 explicit list-type evidence. Both preserve analyzable table structure; Google Docs adds an extra H1 title in F01.

## Does source-grounded comparison reveal differences validators might miss?

Yes. A generic tagged-PDF check would see tagged output from both engines. The source-grounded comparison additionally reveals the LibreOffice F02 string mutation, the Google Docs F01 extra H1, and the Google Docs F03 missing `/ListNumbering` evidence.

## Did the second converter strengthen feasibility?

Yes. The same frozen source semantics produced reproducible, feature-specific signals across two independent conversion routes. That supports the methodology as a cross-converter experiment rather than a single-engine observation.

## What should be tested next?

Scale the same design to more converters and feature families: complex nested lists, table header scope/associations, figure captions and long descriptions, document language, links, bookmarks, reading order, footnotes, and forms. Preserve the two-axis reporting model and keep validator output secondary.
