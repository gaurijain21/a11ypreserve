# Final strengthening baseline

This record was created before any final-strengthening edits.

- Repository: `A11yPreserve`
- Baseline timestamp: `2026-10-04T13:18:48.1691780-07:00`
- Baseline commit: `d189d533a6320a3015ec82083b4cde0cd4b40db9`
- Git status: clean on branch `master`
- Inventory: 1,214 paths from `rg --files -g '!\\.git/**'`; the working tree also contains vendored LibreOffice/runtime material.
- Canonical manuscript discovered: `submission/ICST2027_V3/main.tex`; PDF present at `submission/ICST2027_V3/main.pdf`.
- Historical manuscript: `paper/`; earlier V1/V2 freeze and submission records are retained.
- Current primary result candidate: `results/V3_PRIMARY_RESULTS.json` (52 records: 26 Core + 26 Variant B, two named pipelines).
- Existing historical result datasets: `results/full_experiment/PRIMARY_RESULTS_FREEZE.json`, `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json`, `results/full_experiment/EVIDENCE_STATUS_FREEZE_V2.json`, and the V1/V2 pilot records.
- Existing supplementary datasets: `v3/google_repeatability/REPEATABILITY_RESULTS.json`, `final_strengthening/COMPARATOR_CALIBRATION.json`, `integrated_study/INTEGRATED_RESULTS.json`, and `v3/variant_set_b/V3_VARIANT_SET_B_FINAL_RESULTS.json`.
- Scientifically scoped files counted at baseline: 2,133; DOCX 39; PDF 58; JSON 31. This scope includes corpus fixtures, frozen outputs, variant evidence, integrated sources/outputs, and associated machine-readable evidence.

## Baseline SHA-256 summary

The following key provenance files were hashed at baseline. The full scoped hash set is reproducible with the inventory command recorded in the task log; no experimental output was changed before this record was added.

| Path | SHA-256 |
|---|---|
| `corpus/FROZEN_CORPUS_MANIFEST.json` | `DBC7DA58773E4A15AFE2582E5FCBF271C8AC82D686833E0406BD24D539517376` |
| `corpus/v3_variant_set_b/V3_VARIANT_FREEZE.md` | `6C1C77CC22728E7D4AED476215D578D6E310E6C06D5560B2DB32DF13A73096B0` |
| `results/V3_PRIMARY_RESULTS.json` | `E4EEFDDB5C024DDB9FD5D0AE53198094C932C9839A9C19ADA9A7CFBF6C70595A` |
| `results/full_experiment/PRIMARY_RESULTS_FREEZE.json` | `6939351E01695D334FCC45C4823316CE4A3698D114091EB34C127E7FE5548D99` |
| `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` | `04FD89CF44FE9B158A4D1FB3FB5B396A87BF4EADC83081A13C6C4EA14994AEB3` |
| `v3/variant_set_b/V3_VARIANT_SET_B_FINAL_RESULTS.json` | `C46370679665A98614CB8C5B81004B694584BEB29E4BEC997A92013F4D68746A` |
| `final_strengthening/COMPARATOR_CALIBRATION.json` | `E03F35349D7BC3AE09899BD7715483564B43A1FC14419EF8DE6DDF1BBB7DBA0E` |
| `v3/google_repeatability/REPEATABILITY_RESULTS.json` | `5794A0F8347EF3E05BF9863318DF3C5CDD95A78033FEA24F741C08CA620F119D` |
| `integrated_study/INTEGRATED_RESULTS.json` | `444E9BDE1531F207F15C6E3DB0FED21E89AB89F7EA419DB0A5609D78907F5884` |
| `submission/ICST2027_V3/main.tex` | `16A3C606329DD066CB4AF4F92B95DE77187C9BAFEA8AC15D5F04554C25612940` |
| `submission/ICST2027_V3/main.pdf` | `4F4CC53B5783ADEECF418B645EDDC16D39A7CD17144B8CD2A76D6A32D8B46285` |

This baseline is historical provenance, not an endorsement of the discovered V3 state. In particular, the audit found contradictory root-level claims: the V3 result record contains 52 cases, while older readiness documents still describe a 26-case primary experiment. Those contradictions are intentionally preserved for the audit and must be resolved or labeled historical.
