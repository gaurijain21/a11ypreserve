# A11yPreserve V6 master audit

## Final audit status

**GO WITH LIMITATIONS.** Priority-0 and priority-1 computations executed successfully. V6 does not claim standards conformance, natural-corpus validation, temporal Google repeatability, human usability, or external adjudication because those arms were not available or authorized.

## Verified fixes and executed experiments

- Circular no-op-control implementation confirmed and removed. Fresh controls: 0/65 classification disagreements, 0/65 extraction failures, 0/65 semantic-evidence differences.
- Destination mutation sensitivity regenerated: 65 attempts, 59 valid applied, 46 classification detections, 10 semantically meaningful survivors, 6 unsupported, 0 invalid, 0 inconclusive.
- Baselines/ablations executed over 130 primary cases and 59 known valid destination faults. Tag presence and visible-text equality detected 0/59 injected faults; destination-only evidence detected 16/59; full A11yPreserve detected 46/59.
- LibreOffice profile-B result verified from retained V5 evidence: 65 valid outputs and zero classification changes; interpretation is within-pipeline robustness only.
- Historical V4/V5 source fixtures, primary outputs, classifications, hashes, and chronology were not overwritten.

## Denominator and claim boundary

The frozen V4 primary experiment remains 65 fixtures x 2 primary pipelines = 130 observations. D/E contributes 52 holdout observations and A-C contributes 78 non-holdout observations. Word remains 65 supplementary observations. The 10 project-created realistic documents and V6 mutation/ablation records remain separate evidence arms.

## Failed, inconclusive, blocked, and human-dependent work

- Failed/inconclusive V6 runs: none for controls, mutation, or baselines.
- Unsupported mutation attempts: 6 (five decorative-image, one hyperlink) with exact reasons recorded.
- Environment blockers: PAC/verapDF unavailable; authenticated time-separated Google sessions unavailable; no rights-cleared natural corpus; no participant study or ethics approval.
- Human decisions: licensing, author/citation metadata, final reference/result verification, portal declarations, and whether to repair or explicitly retain the stale historical repeatability status.
- Manuscript build: complete. `submission/ICST2027_V6/main.pdf` is a 9-page IEEE letter PDF built from the current source; no unresolved citations/references remain, and every page was rendered for visual QA. Build provenance is recorded in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

## Evidence index

| Claim area | Machine evidence |
|---|---|
| Control rerun | `experiments/v6/V6_CONTROL_RERUN.json`, `experiments/v6/control_rerun_cases/` |
| Mutation sensitivity | `experiments/v6/V6_MUTATION_SENSITIVITY.json`, `experiments/v6/mutation_cases/` |
| Baselines/ablations | `experiments/v6/V6_BASELINE_ABLATION.json`, `experiments/v6/V6_MUTATION_BASELINE_EVALUATION.json` |
| Frozen primary results | `experiments/v4/conversions/*/analysis/` |
| Pipeline profile | `experiments/v5/LIBREOFFICE_PROFILE_B_ANALYSIS.json` |
| Independent diagnostic | `experiments/v5/independent_oracle_validation.json` |
| Source contracts | `experiments/v4/source_manifest.json`, `contracts/`, `evidence/source/` |

The V6 manuscript must cite only machine-derived V6 counts for new empirical claims and must preserve V4/V5 chronology explicitly.
