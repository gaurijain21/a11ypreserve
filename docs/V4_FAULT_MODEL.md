# V4 Fault Model and Test-Adequacy Matrix

V4 treats a conversion pipeline as a system under test and a source contract as a bounded specification. The model is not exhaustive; it makes fixture selection auditable.

## Fault classes

| ID | Fault class | Meaning |
|---|---|---|
| F1 | semantic deletion | Required source semantics disappear from the destination. |
| F2 | author-value mutation | A preserved property changes value, locale, text, URI, or metadata. |
| F3 | hierarchy mutation | Heading, list, or table hierarchy changes. |
| F4 | structure flattening | Structured content becomes ordinary text or untyped objects. |
| F5 | association loss | An image, caption, note, link, header, or text span loses its relationship. |
| F6 | metadata normalization | Title, language, or related metadata is normalized or omitted. |
| F7 | semantic substitution | A different representation is emitted; it may be valid, invalid, or unresolved. |
| F8 | representational relocation | Semantics survive but move across objects or pages. |
| F9 | alternate valid representation | A legitimate equivalent encoding is not recognized by the comparator. |
| F10 | parser blind spot | Evidence exists but a chosen extractor fails to observe it. |
| F11 | ambiguous equivalence | Available evidence cannot safely decide equivalence. |
| F12 | output-generation failure | The converter or export route fails before a PDF is produced. |

## Coverage matrix

| Feature family | Primary fault classes exposed |
|---|---|
| headings | F2, F3, F4, F7, F8, F9, F10, F11 |
| alternative text | F1, F2, F5, F7, F9, F10, F11 |
| lists | F1, F2, F3, F4, F7, F8, F9, F10, F11 |
| basic tables | F1, F2, F3, F4, F5, F7, F9, F10, F11 |
| document language | F1, F2, F6, F7, F9, F10 |
| inline language | F1, F2, F5, F6, F7, F8, F9, F10, F11 |
| decorative images | F1, F2, F5, F7, F9, F10, F11 |
| hyperlinks | F1, F2, F5, F7, F8, F9, F10, F11 |
| document title/metadata | F1, F2, F6, F7, F9, F10 |
| complex tables | F1, F2, F3, F4, F5, F7, F8, F9, F10, F11 |
| footnotes | F1, F2, F4, F5, F7, F8, F9, F10, F11 |
| equations | F1, F2, F4, F7, F8, F9, F10, F11 |
| figure/caption association | F1, F2, F5, F7, F8, F9, F10, F11 |

The matrix supports systematic depth; it does not imply complete accessibility-standard coverage or exhaustive mutation coverage.
