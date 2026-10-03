# Paper Evidence Map

| Paper claim | Supporting artifact |
|---|---|
| 13 verified source fixtures | `corpus/FROZEN_CORPUS_MANIFEST.json`; source verification reports |
| 26 genuine conversion outputs | conversion automation logs; output validation; frozen output hashes |
| All outputs parseable and tagged | `results/full_experiment/reports/output_validation.json` |
| Source ground truth is independently checked | manifests, raw OOXML audits, source ASIR |
| Frozen classifications are stable | `PRIMARY_RESULTS_FREEZE.json`; Phase 6 freeze audit |
| F06 Google Docs inline language is LOST | `audit/lost_cases/F06_INLINE_LANGUAGE_Google_Docs.md`; raw PDF and extraction evidence |
| F11 Google Docs footnote association is LOST | `audit/lost_cases/F11_FOOTNOTES_Google_Docs.md`; raw PDF and extraction evidence |
| F11 LibreOffice remains MEASUREMENT_ERROR | `audit/MEASUREMENT_ERROR_ANALYSIS.md`; measurement note |
| Ten feature rows differ across pipelines | `research/FINAL_CROSS_CONVERTER_DIFFERENCES.md` |
| Comparator robustness | hostile comparator tests, 17/17 passed |
| Limitations and claims | Phase 6 audit; `research/CLAIM_BOUNDARIES.md`; threat notes |

Every final primary result is traceable from source hash and manifest through converter condition, output hash, destination extraction, comparison, and evidence.
