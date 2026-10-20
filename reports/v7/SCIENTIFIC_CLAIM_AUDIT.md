# Scientific claim audit

## Scope

This audit is additive to the frozen V4 experiment, historical V5 records, and
the released V6 hardening. No V4/V5/V6 fixture, classification, denominator, or
PDF was rewritten. The audit date is 2026-10-19/20 UTC.

| Claim area | Evidence | Status | Boundary |
|---|---|---|---|
| 130 primary fixture--pipeline cases | `experiments/v4/conversions/*/analysis/` | VERIFIED WITH LIMITATIONS | Controlled purposive fixtures; not a prevalence sample |
| Genuine no-op controls | `experiments/v6/V6_CONTROL_RERUN.json` and 65 case files | VERIFIED | 65/65 rerun; 0 disagreements, 0 extraction failures, 0 evidence differences |
| Destination mutation accounting | `experiments/v6/V6_MUTATION_SENSITIVITY.json` | VERIFIED WITH LIMITATIONS | 65 attempts, 59 valid, 46 coarse detections, 10 meaningful survivors, 6 unsupported |
| Evidence drift | `experiments/v6/V6_OBJECTION_MITIGATIONS.json` | VERIFIED AS DIAGNOSTIC | 59/59 valid mutants flagged; not equivalent to semantic-fault detection |
| Baseline/ablation comparison | `experiments/v6/V6_BASELINE_ABLATION.json` | VERIFIED WITH LIMITATIONS | Known-fault sensitivity arm; no independent primary ground truth |
| Independent destination audit | `experiments/v7/V7_INDEPENDENT_ORACLE.json` | EXECUTED | 195/195 cases, 0 extraction errors; internal independent implementation, not human adjudication |
| Benign equivalence controls | `experiments/v7/V7_SEMANTIC_EQUIVALENCE.json` | EXECUTED | 13/13 metadata-only rewrites retained the independent contract projection |
| Association/semantic attacks | `experiments/v7/V7_ASSOCIATION_ATTACKS.json` | EXECUTED | 12 valid/scorable attacks; 11 detected; one family unsupported |
| Competent source-aware baseline | `experiments/v7/V7_COMPETITIVE_BASELINE.json` | EXECUTED | 25/59 known faults detected; bounded baseline, not ground truth |
| Natural-document generalization | `reports/EXTERNAL_VALIDITY_ARM.md` | NOT ESTABLISHED | No rights-cleared independently authored corpus with contracts |
| Human adjudication | `reports/v6/V6_BLINDED_ADJUDICATION_PROTOCOL.md` | NOT EXECUTED | Packet and rubric exist; no external reviewer result claimed |
| PDF/UA conformance | local tool audit | NOT RUN | PAC and veraPDF were not available in the environment |

## Falsification outcome

The new attacks strengthen the claim that source-aware contracts expose some
faults missed by simpler destination checks, but they do not establish oracle
correctness for every primary case. The complex-table attack was valid and
scorable but not detected by the frozen comparator. This is a retained
comparator blind spot, not a successful validation result.

## Final claim boundary

The defensible contribution is an auditable, source-grounded preservation test
protocol for selected machine-observable semantics under recorded conversion
conditions. It is not a complete PDF accessibility validator, a human-usability
study, a standards-conformance result, a natural-corpus prevalence estimate, or
a global converter ranking.
