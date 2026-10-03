# Full Experiment Results by Feature

Empirical labels are deliberately simplified for this report. Raw two-axis comparator output is in `reports/a11ydiff_results.json`. `PRESERVED` includes exact and semantically equivalent preservation; `ALTERED` includes mutation/regeneration. No overall converter ranking is computed.

| Fixture | Feature | LibreOffice→PDF | Google Docs→PDF | Evidence quality |
|---|---|---|---|---|
| F01_HEADINGS | heading hierarchy | PRESERVED | PARTIALLY_PRESERVED | HIGH |
| F02_ALT_TEXT | image alternative text | ALTERED | PRESERVED | HIGH |
| F03_LISTS | list semantics | PRESERVED | PARTIALLY_PRESERVED | HIGH |
| F04_TABLE | table/header structure | PRESERVED | PRESERVED | HIGH |
| F05_DOCUMENT_LANGUAGE | document language | PRESERVED | ALTERED | HIGH |
| F06_INLINE_LANGUAGE | inline language changes | PRESERVED | LOST | MEDIUM |
| F07_DECORATIVE_IMAGE | decorative image state | PARTIALLY_PRESERVED | PARTIALLY_PRESERVED | MEDIUM |
| F08_LINKS | hyperlink semantics | PARTIALLY_PRESERVED | PARTIALLY_PRESERVED | MEDIUM |
| F09_DOCUMENT_TITLE | document title/metadata | PRESERVED | ALTERED | HIGH |
| F10_COMPLEX_TABLE | multi-level table headers | PRESERVED | PARTIALLY_PRESERVED | HIGH |
| F11_FOOTNOTES | footnote association | MEASUREMENT_ERROR | LOST | MEDIUM |
| F12_EQUATION | equation/math semantics | PRESERVED | PARTIALLY_PRESERVED | MEDIUM |
| F14_CAPTIONS | figure/caption association | PRESERVED | PARTIALLY_PRESERVED | MEDIUM |
