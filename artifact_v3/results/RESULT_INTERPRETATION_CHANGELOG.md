# Result interpretation changelog

## V1 historical freeze

The historical V1 classification was created before the uncertainty and
cross-format-equivalence strengthening pass:

| V1 outcome | Count |
|---|---:|
| PRESERVED | 11 |
| PARTIALLY_PRESERVED | 9 |
| ALTERED | 3 |
| LOST | 2 |
| MEASUREMENT_ERROR | 1 |

These labels remain archived in `results/full_experiment/PRIMARY_RESULTS_FREEZE.json`
and are retained for provenance.

## V2 evidence-aware interpretation

Subsequent parser triangulation, independent source-oracle verification,
loss-certificate review, and feature-specific equivalence analysis separated
directly demonstrated partial preservation from cases where relevant structure
survived but cross-format equivalence could not be established:

| V2 result | Count |
|---|---:|
| VERIFIED_PRESERVED | 11 |
| OBSERVED_PARTIAL | 3 |
| ALTERED | 3 |
| CONFIRMED_LOST | 2 |
| UNRESOLVED_EQUIVALENCE | 6 |
| MEASUREMENT_ERROR | 1 |

The source files, PDF outputs, manifests, hashes, and frozen V1 evidence did
not change. The underlying evidence and its interpretation became more
explicit. The final manuscript therefore reports V2 as the primary scientific
result model while retaining V1 as a historical provenance record. This is a
refinement of interpretation, not data manipulation.
