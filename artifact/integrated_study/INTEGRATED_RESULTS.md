# Integrated sanity-check results

This is a secondary evaluation of three multi-feature documents. It uses only existing feature contracts and the same two named pipelines. Its property instances are not merged into the primary 13-fixture × 2-pipeline denominator.

- Documents: 3
- Property instances: 21
- Pipeline cases: 42
- Independent integrated source contracts: 21/21

| Document | Property instance | Pipeline | Result | Evidence status | Observation |
|---|---|---|---|---|---|
| I01_REALISTIC_REPORT | I01-heading-hierarchy | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | heading level/order preserved; PDF marked-content text was not available for every heading node |
| I01_REALISTIC_REPORT | I01-alternative-text | LibreOffice | ALTERED | OBSERVED_DIFFERENCE | destination retains non-decorative figures with different alternative text |
| I01_REALISTIC_REPORT | I01-lists | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF /L, /LI, nesting, and /ListNumbering match the source contract |
| I01_REALISTIC_REPORT | I01-table-headers | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF Table/TR/TH/TD structure and header-cell count match the source table contract |
| I01_REALISTIC_REPORT | I01-document-language | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I01_REALISTIC_REPORT | I01-hyperlink | LibreOffice | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure |
| I01_REALISTIC_REPORT | I01-title | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I01_REALISTIC_REPORT | I01-heading-hierarchy | Google Docs | OBSERVED_PARTIAL | OBSERVED_PARTIAL | PDF contains heading structure but the level/order sequence differs from source |
| I01_REALISTIC_REPORT | I01-alternative-text | Google Docs | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I01_REALISTIC_REPORT | I01-lists | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | list items and nesting survive, but PDF extraction found no explicit ordered/unordered type representation |
| I01_REALISTIC_REPORT | I01-table-headers | Google Docs | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF Table/TR/TH/TD structure and header-cell count match the source table contract |
| I01_REALISTIC_REPORT | I01-document-language | Google Docs | ALTERED | OBSERVED_DIFFERENCE |  |
| I01_REALISTIC_REPORT | I01-hyperlink | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure |
| I01_REALISTIC_REPORT | I01-title | Google Docs | ALTERED | OBSERVED_DIFFERENCE |  |
| I02_EDUCATIONAL_HANDOUT | I02-heading-hierarchy | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | heading level/order preserved; PDF marked-content text was not available for every heading node |
| I02_EDUCATIONAL_HANDOUT | I02-inline-language | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I02_EDUCATIONAL_HANDOUT | I02-equation | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF /Formula structure is present and the visible expression is retained; token-level math extraction remains limited |
| I02_EDUCATIONAL_HANDOUT | I02-footnote | LibreOffice | MEASUREMENT_ERROR | MEASUREMENT_FAILURE | PDF /Note structure exists, but marked-content extraction did not recover note-body text for association verification |
| I02_EDUCATIONAL_HANDOUT | I02-caption | LibreOffice | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |  |
| I02_EDUCATIONAL_HANDOUT | I02-hyperlink | LibreOffice | ALTERED | OBSERVED_DIFFERENCE | destination link target or count differs from source |
| I02_EDUCATIONAL_HANDOUT | I02-heading-hierarchy | Google Docs | OBSERVED_PARTIAL | OBSERVED_PARTIAL | PDF contains heading structure but the level/order sequence differs from source |
| I02_EDUCATIONAL_HANDOUT | I02-inline-language | Google Docs | CONFIRMED_LOST | INDEPENDENTLY_CONFIRMED_ABSENCE | document language may survive while inline override is absent |
| I02_EDUCATIONAL_HANDOUT | I02-equation | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | equation rendering is present in page text/content, but no machine-readable PDF math structure was extracted |
| I02_EDUCATIONAL_HANDOUT | I02-footnote | Google Docs | CONFIRMED_LOST | INDEPENDENTLY_CONFIRMED_ABSENCE |  |
| I02_EDUCATIONAL_HANDOUT | I02-caption | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE |  |
| I02_EDUCATIONAL_HANDOUT | I02-hyperlink | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure |
| I03_POLICY_NOTE | I03-heading-hierarchy | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | heading level/order preserved; PDF marked-content text was not available for every heading node |
| I03_POLICY_NOTE | I03-lists | LibreOffice | OBSERVED_PARTIAL | OBSERVED_PARTIAL | some list structure survives but item count or nesting differs |
| I03_POLICY_NOTE | I03-table-headers | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF Table/TR/TH/TD structure and header-cell count match the source table contract |
| I03_POLICY_NOTE | I03-image-alt | LibreOffice | OBSERVED_PARTIAL | OBSERVED_PARTIAL | figure count or decorative/alternative-text state differs |
| I03_POLICY_NOTE | I03-decorative-image | LibreOffice | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | destination uses Figure elements with empty alternative text; no explicit PDF Artifact/decorative representation was established |
| I03_POLICY_NOTE | I03-document-language | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I03_POLICY_NOTE | I03-inline-language | LibreOffice | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I03_POLICY_NOTE | I03-hyperlink | LibreOffice | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure |
| I03_POLICY_NOTE | I03-heading-hierarchy | Google Docs | OBSERVED_PARTIAL | OBSERVED_PARTIAL | PDF contains heading structure but the level/order sequence differs from source |
| I03_POLICY_NOTE | I03-lists | Google Docs | OBSERVED_PARTIAL | OBSERVED_PARTIAL | some list structure survives but item count or nesting differs |
| I03_POLICY_NOTE | I03-table-headers | Google Docs | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE | PDF Table/TR/TH/TD structure and header-cell count match the source table contract |
| I03_POLICY_NOTE | I03-image-alt | Google Docs | VERIFIED_PRESERVED | VERIFIED_EQUIVALENCE |  |
| I03_POLICY_NOTE | I03-decorative-image | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | destination uses Figure elements with empty alternative text; no explicit PDF Artifact/decorative representation was established |
| I03_POLICY_NOTE | I03-document-language | Google Docs | ALTERED | OBSERVED_DIFFERENCE |  |
| I03_POLICY_NOTE | I03-inline-language | Google Docs | CONFIRMED_LOST | INDEPENDENTLY_CONFIRMED_ABSENCE | document language may survive while inline override is absent |
| I03_POLICY_NOTE | I03-hyperlink | Google Docs | UNRESOLVED_EQUIVALENCE | UNRESOLVED_EQUIVALENCE | URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure |

## Interpretation

The protocol remained executable when multiple existing accessibility properties coexisted in realistic documents. The secondary check is a usability demonstration of the conformance procedure, not a prevalence estimate, converter ranking, or independent generalization study. Any unresolved rows retain that status rather than being promoted to loss.
