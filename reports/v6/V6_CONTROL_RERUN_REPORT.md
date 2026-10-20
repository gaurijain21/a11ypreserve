# V6 control rerun report

## Status

**Executed and complete.** The V6 harness reopened the actual 65 frozen LibreOffice baseline PDFs, reran source extraction, destination extraction, the frozen V4 comparator, secondary evidence, and final classification. It did not copy a frozen label into a control result.

| Measure | Result |
|---|---:|
| Controls evaluated | 65/65 |
| Fresh classification disagreements | 0/65 |
| Control disagreement rate | 0.000 |
| Extraction failures | 0/65 |
| Normalized semantic-evidence differences | 0/65 |

The measured V6 control disagreement rate is **0/65 (0.0%)**. This is a result of the fresh rerun, not the historical V5 hard-coded `false_positive=False` field. Per-case traces are in `experiments/v6/control_rerun_cases/`; the aggregate record is `experiments/v6/V6_CONTROL_RERUN.json`.

The original V5 JSON remains preserved and is not silently rewritten. The corrected implementation is `experiments/v5/destination_mutation_testing.py`, and the independent V6 rerun implementation is `experiments/v6/control_rerun.py`.

## Evidence and failure policy

Source and PDF SHA-256 values, frozen and fresh classifications, normalized semantic-evidence hashes, parser versions, timestamps, and extraction traces are recorded per case. A parse or extraction exception is recorded as a failure and counts as a disagreement requiring investigation; it is never converted into a passing control.
