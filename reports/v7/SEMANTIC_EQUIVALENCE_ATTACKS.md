# Semantic-equivalence attacks

## Executed control

`python scripts/v7_semantic_equivalence_audit.py` selected one archived
LibreOffice baseline PDF per feature family and rewrote only the PDF producer
metadata using pypdf. Each rewritten PDF was reopened, page-count checked, and
compared using the independent contract projection from the V7 oracle audit.

| Outcome | Count |
|---|---:|
| Attempted | 13 |
| Valid benign controls | 13 |
| Ambiguous rewrites | 0 |
| False semantic-regression alerts | 0 |

These controls establish only that this conservative non-contract rewrite did
not change the measured contract projection. They do not prove that every
alternate PDF serialization, role-map substitution, or equivalent association
representation is accepted correctly. The result is therefore a sanity control,
not a complete metamorphic-equivalence validation.
