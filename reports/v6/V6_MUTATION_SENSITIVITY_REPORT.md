# V6 mutation sensitivity report

## Executed result

V6 reran one destination-side operator for every one of the 65 frozen atomic LibreOffice PDFs. The original V5 mutation manifest is retained unchanged. Each V6 case records source fixture/family, operator and target, baseline and mutant PDF hashes, application, validity, raw evidence before/after, normalized evidence hashes, contracted-semantics change, classification change, survival status, and exact unsupported/inconclusive reason.

| Outcome | Count |
|---|---:|
| Attempts | 65 |
| Applied and valid mutants | 59 |
| Classification-level detections | 46 |
| Semantically meaningful survivals | 10 |
| Unsupported attempts | 6 |
| Invalid mutants | 0 |
| Inconclusive attempts | 0 |
| Non-effective mutants | 0 |
| Evidence-changing, unchanged-classification mutants | 3 |

The valid-mutant classification detection rate is 46/59 (78.0%); the semantically meaningful survival count is 10. Three additional applied mutants changed extracted evidence but did not change the contracted-semantics signature or coarse classification; they are reported separately as unchanged-classification outcomes, not silently folded into the survival count. A meaningful survival means normalized relevant evidence and the contracted-semantics signature changed, but the six-way classification did not. It is not relabeled as a detection.

## Family-level sensitivity

| Family | Attempted | Applied | Valid | Classification detected | Meaningful survival | Unchanged classification | Unsupported | Inconclusive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| alt_text | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| basic_tables | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| captions | 5 | 5 | 5 | 2 | 0 | 3 | 0 | 0 |
| complex_tables | 5 | 5 | 5 | 2 | 3 | 0 | 0 | 0 |
| decorative_images | 5 | 0 | 0 | 0 | 0 | 0 | 5 | 0 |
| document_language | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| document_metadata | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| equations | 5 | 5 | 5 | 4 | 1 | 0 | 0 | 0 |
| footnotes | 5 | 5 | 5 | 3 | 2 | 0 | 0 | 0 |
| headings | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| hyperlinks | 5 | 4 | 4 | 2 | 2 | 0 | 1 | 0 |
| inline_language | 5 | 5 | 5 | 5 | 0 | 0 | 0 | 0 |
| lists | 5 | 5 | 5 | 3 | 2 | 0 | 0 | 0 |

The five decorative-image attempts are explicitly unsupported because the actual PDFs contained no `/Artifact` node to mutate. The unsupported hyperlink attempt is recorded because that PDF had no URI action. These are operator-representation limits, not silent negative results. The V6 run produced no invalid or inconclusive PDFs.

Machine evidence: `experiments/v6/V6_MUTATION_SENSITIVITY.json` and `experiments/v6/mutation_cases/*.json`.
