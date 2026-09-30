# V3 primary results

## Atomic benchmark

The V3 atomic benchmark contains 26 controlled fixtures (13 Core + 13 Variant B) x 2 named pipelines = 52 fixture--pipeline cases. The primary unit is one controlled fixture/converter pair; the cases are not a representative sample.

| Outcome | Count |
|---|---:|
| VERIFIED_PRESERVED | 18 |
| OBSERVED_PARTIAL | 4 |
| ALTERED | 7 |
| CONFIRMED_LOST | 4 |
| UNRESOLVED_EQUIVALENCE | 18 |
| MEASUREMENT_ERROR | 1 |

The complete machine-readable record is `results/V3_PRIMARY_RESULTS.json`. The frozen Core V2 result file remains unchanged and is included only as provenance.

## Separate studies

- Google repeatability: 13 Core fixtures x 3 runs = 39 conversions; classification stable 13/13 and byte-identical 13/13.
- Integrated sanity check: 3 project-generated multi-feature documents, 21/21 source assertions, and 42 property--pipeline observations; separate denominator.

Unresolved equivalence is a conservative abstention, not a loss finding. The study measures machine-verifiable source-information preservation, not complete accessibility or disabled-user impact.
