# V5 calibration ground-truth audit

Status: **COMPLETE**. Expected labels come from the frozen diagnostic control file, not from the comparator under evaluation.

- Controls: 78
- Correct: 60
- False positives: 0
- Conservative false negatives: 5
- Correct abstentions: 13

The five conservative false negatives are retained and reviewed as evidence-boundary cases involving decorative-image alternatives, hyperlink visible-name relations, and complex-table associations. They are not re-labeled to improve the score. The full row-level audit is machine-readable at `experiments/v5/calibration_ground_truth_audit.json`.

| Interpretation category | V5 decision |
|---|---|
| Appropriate conservative abstention/failure | Retain unless independent evidence proves the accepted equivalent. |
| Missing accepted equivalent | Open for a new contract version; do not edit frozen labels. |
| Extractor limitation | Add corroborating extraction only with standards/evidence support. |
| Comparator bug | Requires a new frozen V5 comparator and affected-row rerun. |
