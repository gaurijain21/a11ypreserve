# V5 holdout accounting audit

Status: **PASS**.

## Source of truth

The audit reads `experiments/v4/source_manifest.json`, `HOLDOUT_MANIFEST.json`, both primary conversion manifests, and `COMPARATOR_CALIBRATION.json`; it does not infer counts from manuscript prose.

## Derived accounting

| Quantity | Value |
|---|---:|
| Atomic fixtures | 65 |
| Primary pipelines | 2 |
| Holdout fixtures | 26 |
| Holdout fixture–pipeline cases | 52 |
| Non-holdout fixture–pipeline cases | 78 |
| Primary cases | 130 |
| Calibration controls | 78 |

The holdout is fixture-level: D and E are held out for every primary pipeline. Therefore each pipeline has 26 holdout cases and 39 non-holdout cases; across two pipelines the correct arithmetic is **130 − 52 = 78**, not 130 − 26 = 104.

Calibration controls are synthetic diagnostic destinations, not fixture–pipeline outcomes and do not overlap the primary fixture IDs.

## Automated assertions

- `fixture_count`: PASS
- `family_count`: PASS
- `variants_per_family`: PASS
- `holdout_manifest_count`: PASS
- `pipeline_case_counts`: PASS
- `arithmetic`: PASS
- `calibration_is_separate`: PASS

## Files corrected

No V4 file was rewritten by this audit. The V5 report and JSON audit are new. Any manuscript copy using 104 non-holdout cases must be corrected to 78; current V4 final sections already state 104 as the complement of the 26-case per-pipeline holdout, so the V5 manuscript revision must state both per-pipeline and aggregate denominators explicitly.
