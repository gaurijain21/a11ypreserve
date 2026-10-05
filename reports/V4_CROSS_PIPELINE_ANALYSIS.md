# V4 Cross-Pipeline Analysis

This report compares the independently analyzed LibreOffice and Google Docs outputs using the frozen V4 classification taxonomy. It does not alter classifications or create a combined converter score.

## Atomic corpus

- Cases: 65
- Same classification: 16
- Different classification: 49
- LibreOffice counts: `{"ALTERED": 9, "CONFIRMED_LOST": 1, "MEASUREMENT_ERROR": 5, "OBSERVED_PARTIAL": 11, "UNRESOLVED_EQUIVALENCE": 1, "VERIFIED_PRESERVED": 38}`
- Google Docs counts: `{"ALTERED": 11, "CONFIRMED_LOST": 6, "OBSERVED_PARTIAL": 32, "UNRESOLVED_EQUIVALENCE": 5, "VERIFIED_PRESERVED": 11}`

## Holdout

- Cases: 26
- Same classification: 7
- Different classification: 19
- LibreOffice counts: `{"ALTERED": 4, "CONFIRMED_LOST": 1, "MEASUREMENT_ERROR": 2, "OBSERVED_PARTIAL": 5, "VERIFIED_PRESERVED": 14}`
- Google Docs counts: `{"ALTERED": 5, "CONFIRMED_LOST": 2, "OBSERVED_PARTIAL": 13, "UNRESOLVED_EQUIVALENCE": 2, "VERIFIED_PRESERVED": 4}`

## Realistic/integrated corpus

- Property observations: 78
- Same classification: 15
- Different classification: 63
- LibreOffice counts: `{"ALTERED": 15, "MEASUREMENT_ERROR": 5, "OBSERVED_PARTIAL": 5, "VERIFIED_PRESERVED": 53}`
- Google Docs counts: `{"ALTERED": 10, "CONFIRMED_LOST": 15, "OBSERVED_PARTIAL": 33, "VERIFIED_PRESERVED": 20}`

## Per-feature atomic comparison

| Feature family | Cases | Same | Different | LibreOffice | Google Docs |
|---|---:|---:|---:|---|---|
| alt_text | 5 | 0 | 5 | `{"ALTERED": 5}` | `{"VERIFIED_PRESERVED": 5}` |
| basic_tables | 5 | 5 | 0 | `{"VERIFIED_PRESERVED": 5}` | `{"VERIFIED_PRESERVED": 5}` |
| captions | 5 | 0 | 5 | `{"UNRESOLVED_EQUIVALENCE": 1, "VERIFIED_PRESERVED": 4}` | `{"CONFIRMED_LOST": 1, "OBSERVED_PARTIAL": 4}` |
| complex_tables | 5 | 3 | 2 | `{"OBSERVED_PARTIAL": 3, "VERIFIED_PRESERVED": 2}` | `{"OBSERVED_PARTIAL": 5}` |
| decorative_images | 5 | 4 | 1 | `{"ALTERED": 1, "OBSERVED_PARTIAL": 4}` | `{"OBSERVED_PARTIAL": 4, "VERIFIED_PRESERVED": 1}` |
| document_language | 5 | 0 | 5 | `{"VERIFIED_PRESERVED": 5}` | `{"ALTERED": 5}` |
| document_metadata | 5 | 0 | 5 | `{"VERIFIED_PRESERVED": 5}` | `{"ALTERED": 5}` |
| equations | 5 | 0 | 5 | `{"VERIFIED_PRESERVED": 5}` | `{"OBSERVED_PARTIAL": 5}` |
| footnotes | 5 | 0 | 5 | `{"MEASUREMENT_ERROR": 5}` | `{"UNRESOLVED_EQUIVALENCE": 5}` |
| headings | 5 | 0 | 5 | `{"VERIFIED_PRESERVED": 5}` | `{"OBSERVED_PARTIAL": 5}` |
| hyperlinks | 5 | 2 | 3 | `{"ALTERED": 2, "CONFIRMED_LOST": 1, "OBSERVED_PARTIAL": 2}` | `{"ALTERED": 1, "OBSERVED_PARTIAL": 4}` |
| inline_language | 5 | 0 | 5 | `{"ALTERED": 1, "VERIFIED_PRESERVED": 4}` | `{"CONFIRMED_LOST": 5}` |
| lists | 5 | 2 | 3 | `{"OBSERVED_PARTIAL": 2, "VERIFIED_PRESERVED": 3}` | `{"OBSERVED_PARTIAL": 5}` |

## Interpretation

The two pipelines are analyzed as distinct converter arms. Classification disagreements are retained as evidence of converter-dependent behavior or evidence-boundary differences; they are not resolved by choosing one pipeline after seeing results.
