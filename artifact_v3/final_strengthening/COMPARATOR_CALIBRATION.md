# Comparator calibration

The calibration harness (`scripts/comparator_calibration.py`) exercises 27
synthetic positive, negative, and alternate-equivalent controls across headings,
lists, images, links, complex tables, footnotes, equations, captions, and
inline language. It calls the existing comparator directly; it does not rerun
or rewrite the frozen experiment.

| Calibration result | Count |
|---|---:|
| Correct determinate result | 12 |
| Correctly retained unresolved | 6 |
| False positive | 0 |
| False negative | 2 |
| Other unresolved/indeterminate | 7 |

The two false negatives are deliberate warnings, not hidden successes: the
current normalized comparator cannot certify a link-name association when the
association is supplied as an alternate field, and it is conservative for one
complex-table control. The unresolved cases are evidence that a parser result
must not be promoted to semantic absence without feature-specific destination
evidence. The calibration set is small and hand-constructed; its counts are
diagnostic only and are not sensitivity, specificity, or population estimates.

The frozen classifications are unchanged. The calibration outcome supports the
paper's revised language: exact/equivalent results require an accepted
representation, while unresolved equivalence is a first-class evidence status.
