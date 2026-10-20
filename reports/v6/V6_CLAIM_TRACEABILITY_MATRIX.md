# V6 evidence-to-claim traceability matrix

| Claim | Status | Evidence | Limitation |
|---|---|---|---|
| No-op controls are independently rerun | VERIFIED | `experiments/v6/V6_CONTROL_RERUN.json`; 65 per-case traces | Same frozen comparator implementation; no external oracle claim |
| Control disagreement rate is 0/65 | EXECUTED RESULT | V6 control JSON | Descriptive rerun result, not proof of comparator correctness |
| 59 destination mutants are valid/applied | EXECUTED RESULT | V6 mutation JSON and per-case traces | One operator per fixture; no multi-fault completeness |
| 46/59 coarse mutation detections | EXECUTED RESULT | V6 mutation JSON | Fault-model sensitivity only |
| 10 semantically meaningful survivors | EXECUTED RESULT | V6 per-case `semantically_meaningful_survival` fields | Survivors show blind spots; not a prevalence estimate |
| Tags and visible-text equality are insufficient | EXECUTED COMPARISON | V6 ablation JSON; 0/59 fault detections for each | Known-fault oracle, not independent human labels |
| Full method uses abstention | VERIFIED | V6 primary summary and comparator records | Abstention policy remains implementation-defined |
| V4 primary denominator remains 130 | VERIFIED | V4 manifests and analyses | Controlled purposive corpus |
| Word remains supplementary 65 | VERIFIED | V4 Word analysis | Not balanced against primary conditions |
| Google result is end-to-end import/export | VERIFIED INTERPRETATION | V5 Google boundary report and V6 pipeline matrix | No stage-level localization |
| LibreOffice profile comparison has zero classification changes | VERIFIED | V5 profile analysis JSON | Within-LibreOffice robustness only |
| Independent cross-check is not external validation | VERIFIED LIMITATION | V5 independent validation JSON/report | No expert adjudication |
| Standards conformance established | NOT CLAIMED | PAC/verapDF unavailable | Future validator arm |
| Natural-document generalization established | NOT CLAIMED | V5 external validation report | Rights-cleared corpus unavailable |
| Human usability established | NOT CLAIMED | Ethics/privacy audit and remaining gaps | No participants or approvals |
| V6 manuscript counts match machine records | VERIFIED | `reports/v6/V6_MANUSCRIPT_CONSISTENCY.json` | Headline-count check; human review still required |
| V6 PDF corresponds to current source | VERIFIED | `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`; package manifest | Build environment is recorded; reproducibility still depends on configured MiKTeX |
