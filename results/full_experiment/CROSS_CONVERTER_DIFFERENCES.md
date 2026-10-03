# Cross-Converter Differences

Differences are reported feature-by-feature; they are not an overall ranking.

| Fixture | Feature | LibreOffice | Google Docs | Evidence/interpretation |
|---|---|---|---|---|
| F01_HEADINGS | heading hierarchy | PRESERVED | PARTIALLY_PRESERVED | heading level/order preserved; PDF marked-content text was not available for every heading node / PDF contains heading structure but the level/order sequence differs from source |
| F02_ALT_TEXT | image alternative text | ALTERED | PRESERVED | destination retains non-decorative figures with different alternative text /  |
| F03_LISTS | list semantics | PRESERVED | PARTIALLY_PRESERVED | PDF /L, /LI, nesting, and /ListNumbering match the source contract / list items and nesting survive, but PDF extraction found no explicit ordered/unordered type representation |
| F05_DOCUMENT_LANGUAGE | document language | PRESERVED | ALTERED |  /  |
| F06_INLINE_LANGUAGE | inline language changes | PRESERVED | LOST |  / document language may survive while inline override is absent |
| F09_DOCUMENT_TITLE | document title/metadata | PRESERVED | ALTERED |  /  |
| F10_COMPLEX_TABLE | multi-level table headers | PRESERVED | PARTIALLY_PRESERVED | PDF TH cells, scope attributes, and span evidence establish the multi-level header structure / PDF table and header roles survive, but complete multi-level header associations are not established |
| F11_FOOTNOTES | footnote association | MEASUREMENT_ERROR | LOST | PDF /Note structure exists, but marked-content extraction did not recover note-body text for association verification /  |
| F12_EQUATION | equation/math semantics | PRESERVED | PARTIALLY_PRESERVED | PDF /Formula structure is present and the visible expression is retained; token-level math extraction remains limited / equation rendering is present in page text/content, but no machine-readable PDF math structure was extracted |
| F14_CAPTIONS | figure/caption association | PRESERVED | PARTIALLY_PRESERVED | caption text and PDF /Caption structure are present /  |
