# V3 Variant Set B final results

This is a secondary 13-fixture x 2-pipeline robustness arm. It is not merged with the frozen Core denominator.

| Variant | Feature | LibreOffice | Google Docs |
|---|---|---|---|
| B01 | Headings | VERIFIED_PRESERVED | OBSERVED_PARTIAL |
| B02 | Alt text | ALTERED | VERIFIED_PRESERVED |
| B03 | Lists | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |
| B04 | Table | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |
| B05 | Document language | VERIFIED_PRESERVED | ALTERED |
| B06 | Inline language | VERIFIED_PRESERVED | CONFIRMED_LOST |
| B07 | Decorative image | ALTERED | VERIFIED_PRESERVED |
| B08 | Links | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |
| B09 | Document title | VERIFIED_PRESERVED | ALTERED |
| B10 | Complex table | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |
| B11 | Footnotes | UNRESOLVED_EQUIVALENCE | CONFIRMED_LOST |
| B12 | Equation | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |
| B13 | Captions | VERIFIED_PRESERVED | UNRESOLVED_EQUIVALENCE |

## Interpretation

The decisions use the frozen V3 precedence and treat unresolved cross-format equivalence conservatively. They are not prevalence estimates, converter rankings, or evidence of disabled-user impact. B06 and B11 Google are the only Variant B rows classified as confirmed loss, based on the dedicated two-path serialized-structure audit.
