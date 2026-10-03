# A11yPreserve V3 methodology-hardening plan

## Version boundary

V2 is the completed Core Study: 13 frozen DOCX fixtures, 26 frozen fixture--pipeline cases, frozen outputs/manifests/hashes, and the evidence-aware result file. V2 artifacts are immutable for this work. V3 adds methodology audit records and separately stored extension evidence; it does not overwrite V2 evidence or silently replace the V2 manuscript.

## V3 questions

1. Can the frozen outcomes be reproduced from an explicit classification decision specification without reading the historical labels?
2. Are source contracts, cross-format mappings, and destination evidence requirements explicit enough for an external testing reviewer to audit?
3. Does calibration show conservative abstention, false-negative behavior, or both, and is the calibration ground truth independent of comparator output?
4. Do pre-specified feature variants and repeated Google runs reveal within-feature or pipeline instability without changing the Core denominator?
5. Can an external user verify the frozen evidence and rerun the local analysis from a clean environment?

## Non-goals

V3 does not add a product ranking, a universal accessibility claim, a user study, an accessibility validator, a new headline result, or a new causal claim about the Google Docs pipeline. Variant and repeatability observations are secondary methodological evidence only.

## Work order and freeze gates

1. Freeze the chronology, decision rules, cross-format oracle specification, coverage matrix, and Variant Set B design before inspecting any V3 conversion output.
2. Independently reclassify the 26 existing cases from evidence summaries that omit the V2 labels.
3. Complete the calibration and loss audits from stored artifacts.
4. Freeze Variant Set B source files, contracts, and hashes before opening any converted output.
5. Run local variants and, only if the existing authenticated browser workflow is available without exposing credentials, the Google variants and repeatability runs.
6. Analyze V3 extensions in a separate report and update a V3 manuscript copy only after all V3 evidence is frozen.

Any incomplete gate is reported as incomplete; it is never represented as completed evidence.

