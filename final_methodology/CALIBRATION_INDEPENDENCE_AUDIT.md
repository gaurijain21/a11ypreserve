# Calibration independence audit

## Finding

The control intent and expected outcomes were authored as a separate synthetic table, but the existing calibration driver imports comparator logic to obtain the observed result. Therefore the calibration is not an end-to-end independently implemented oracle benchmark: it is an independent-control-intent check of a shared implementation.

The ground-truth descriptions are not generated from the comparator, and the rows identify expected equivalence, difference, or deliberate unresolved status before observation. However, the observed field and verdict are computed by the same comparison implementation used in the study. The team authors also wrote both the comparator and the controls. “Independent calibration” would overstate the evidence.

## Correct wording

Use “synthetic calibration controls with separately authored expected outcomes” or “calibration controls” rather than “independent calibration oracle.” Report the two false negatives and seven other unresolved/indeterminate rows.

## Consequence

This is a methodological limitation, not a reason to discard the Core outputs. The Core source ground truth has a separate raw-OOXML oracle; the destination comparator remains conservative and parser-sensitive. A future release should implement expected-control adjudication in a separate runner and include hand-audited serialized PDF control fixtures.

