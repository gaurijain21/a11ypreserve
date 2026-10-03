# Variant Set B pre-specification

Variant Set B is a secondary robustness set. It is not part of the V2 Core denominator. The 13 variants were specified before any Variant Set B PDF output was inspected.

| Variant | Core family | Pre-specified stress |
|---|---|---|
| B01 | F01 headings | deeper H1--H4 hierarchy and title/heading boundary |
| B02 | F02 alternative text | two informative images with punctuation and distinct descriptions |
| B03 | F03 lists | nested mixed ordered/unordered list with repeated depth |
| B04 | F04 table/header | four-column table with repeated header row and unequal text widths |
| B05 | F05 document language | `fr-FR` default language and accented body text |
| B06 | F06 inline language | two non-default language spans in one paragraph |
| B07 | F07 decorative image | one informative image, one decorative image, and a second informative image |
| B08 | F08 hyperlinks | two visible names with different external targets |
| B09 | F09 title/metadata | visible title, core title, subject, and keywords with longer punctuation-bearing values |
| B10 | F10 complex table | three header rows, a grouped header, and a column span |
| B11 | F11 footnotes | two footnotes with distinct references and bodies |
| B12 | F12 equation | two native OMML expressions in one document |
| B13 | F14 captions | two figures with distinct alt text and captions |

Each variant remains atomic with respect to one feature family, but exercises a different instance shape from its Core counterpart. No variant is chosen because a particular converter previously failed; the stress is defined from source-side structure before conversion.

## Freeze rule

Before any conversion output is opened, freeze each DOCX hash, manifest hash, contract, source-oracle status, and the variant-to-feature mapping in `V3_VARIANT_FREEZE.md`.

