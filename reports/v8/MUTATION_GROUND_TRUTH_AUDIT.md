# Mutation ground-truth audit

Status: COMPLETED AND VERIFIED (additive audit; frozen V4/V5/V6 evidence unchanged).

The historical mutation record contains 65 attempts. The new reference audit
reopens each archived baseline and mutant with raw `pypdf` object inspection and
a separate PyMuPDF reopen check. It does not import the frozen comparator,
cached classifications, or V6 extraction code. Tier A is intentionally narrow:
it establishes only the named source-contract transition (for example, a
decrease in `/TH`, removal of a catalog `/Lang`, or loss of a link URI).

| Outcome | Count |
|---|---:|
| Attempts | 65 |
| Applied | 59 |
| Tier-A direct contract faults | 59 |
| Tier-B unsupported | 6 |
| Structurally valid applied mutants | 59 |
| Frozen comparator classification detections | 46/59 |
| Evidence-level alerts | 59/59 |
| Direct contract faults not coarse-detected | 13/59 |
| Human adjudications | 0 |

The 13 mechanically undetected faults are `F03_D`, `F03_E`, `F08_C`, `F08_D`,
`F10_A`, `F10_B`, `F10_E`, `F11_B`, `F11_E`, `F12_E`, `F13_B`, `F13_C`, and
`F13_E`. The old V6 count of ten remains a historical count under the narrower
“evidence drift plus contracted signature” definition; it is not silently
rewritten. The independent audit shows that three additional caption cases
also have a direct role-count fault despite unchanged coarse classification.

Family-level detection counts (five variants per family) are: alt text 5/5,
basic tables 5/5, captions 2/5, complex tables 2/5, document language 5/5,
document metadata 5/5, equations 4/5, footnotes 3/5, headings 5/5,
hyperlinks 2/4 applied, inline language 5/5, and lists 3/5. Decorative-image
operators were unsupported in all five cases because no `/Artifact` target was
present. One hyperlink operator was unsupported because no URI action existed.

Per-case hashes and raw before/after evidence are in
`experiments/v8/V8_MUTATION_GROUND_TRUTH.json` and
`experiments/v8/mutation_ground_truth_cases/*.json`. The executable protocol is
`scripts/v8_mutation_ground_truth_audit.py`; rerun it with
`python scripts/v8_mutation_ground_truth_audit.py`.

Interpretation: the result repairs the circularity concern for this bounded
mutation question, but it does not establish human accessibility, PDF/UA
conformance, or an independent adjudicated ground truth for arbitrary PDFs.
