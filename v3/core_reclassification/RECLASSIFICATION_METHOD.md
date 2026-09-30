# Blinded-at-label-level Core reclassification

The runner `scripts/v3_classify_core.py` applies the V3 precedence rules to 26 evidence-fact records whose historical V1/V2 outcome labels are not inputs. The records encode the observed destination evidence, source verification, measurement validity, representability, and corroboration needed by the rule specification. This is procedural blinding from the historical label field, not an external-team or independent-human adjudication; the evidence facts were assembled by the project team.

## Result

The runner produced 26/26 decisions with this distribution:

| V3 decision | Count |
|---|---:|
| VERIFIED_PRESERVED | 11 |
| OBSERVED_PARTIAL | 3 |
| ALTERED | 3 |
| CONFIRMED_LOST | 2 |
| UNRESOLVED_EQUIVALENCE | 6 |
| MEASUREMENT_ERROR | 1 |

The counts agree with the V2 evidence-aware distribution. This agreement is a reproducibility check on the decision boundary, not independent validation of the destination evidence. The original frozen files and V2 result records were not modified.

