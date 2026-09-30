# Number Audit

This audit was generated from `paper/main.tex` and all section files after the final bibliography-resolved build. It checks that V2 evidence-aware numbers are present and traceable to machine-readable result artifacts; it does not replace artifact-level verification.

| Claim family | Pattern | Occurrences | Frozen evidence | Status |
|---|---:|---:|---|---|
| source fixture count | `\b13\b` | 12 | corpus/FROZEN_CORPUS_MANIFEST.json | PASS |
| conversion case count | `\b26\b` | 17 | results/full_experiment/PRIMARY_RESULTS_FREEZE.json | PASS |
| verified preserved count | `\b11\b` | 11 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| observed partial count | `\b3\b` | 19 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| altered count | `\b3\b` | 19 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| confirmed lost count | `\b2\b` | 15 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| unresolved equivalence count | `\b6\b` | 11 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| measurement-error count | `\b1\b` | 18 | results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json | PASS |
| atomic source oracle count | `13` | 13 | final_strengthening/INDEPENDENT_SOURCE_ORACLE.json | PASS |
| integrated source oracle count | `21/21` | 1 | integrated_study/INTEGRATED_SOURCE_ORACLE.json | PASS |
| integrated property-pipeline observations | `\b42\b` | 2 | integrated_study/INTEGRATED_RESULTS.json | PASS |
| LibreOffice version | `26\.2\.6\.3` | 1 | results/full_experiment/AUTOMATION_LOG.md | PASS |
| Chrome version | `153\.0\.8010\.53` | 1 | results/full_experiment/AUTOMATION_LOG.md | PASS |
| Windows version | `10\.0\.26200\.0` | 1 | results/full_experiment/AUTOMATION_LOG.md | PASS |

Overall status: **PASS**.

The manuscript reports V2 counts as the primary result model, retains V1 only for provenance, and keeps the three-document integrated check outside the primary 26-case denominator. No headline percentages are used.
