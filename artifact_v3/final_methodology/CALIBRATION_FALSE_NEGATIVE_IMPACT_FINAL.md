# Calibration false-negative impact — final V3 audit

## Scope

The frozen 27-control calibration audit records 12 correct determinate decisions, 6 safe abstentions, 0 false positives, 2 false negatives, and 7 unresolved or indeterminate controls. The two false negatives are the hyperlink alternate-named-association control and the complex-table positive control.

## Impact on the completed V3 evidence

| Calibration limitation | Related V3 rows | Impact |
|---|---|---|
| Hyperlink visible-name association not recovered | Core F08 and Variant B08 | These rows remain `UNRESOLVED_EQUIVALENCE`; no row is promoted to loss or preservation solely from an annotation/URI match. |
| Complete multi-level table association not established | Core F10 and Variant B10 | These rows remain `UNRESOLVED_EQUIVALENCE` where the destination evidence does not establish the full contract. |

Neither false negative targets the inline-language or footnote-association controls. The F06 and F11 Google loss decisions are supported separately by the two-path serialized-structure audits, which found no required inline-language or Note/Reference representation in either the traversed structure tree or the serialized PDF objects. Visible text is not treated as an equivalent substitute for those required associations.

## Boundary

The calibration results demonstrate conservative abstention and expose comparator incompleteness; they do not establish complete oracle sensitivity. The V3 benchmark therefore reports unresolved cases explicitly and does not convert them into failures, successes, or user-impact claims.
