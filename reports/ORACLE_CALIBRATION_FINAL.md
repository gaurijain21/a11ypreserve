# Oracle calibration final report

The calibration set contains 27 synthetic destination controls with expected outcomes written before observation. Results are 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, and 7 other unresolved/indeterminate controls. The machine-readable record is `final_strengthening/COMPARATOR_CALIBRATION.json`.

The two false negatives concern alternate/association representations in links and complex tables; the affected study rows remain unresolved rather than being promoted to preservation or loss. The controls are diagnostic and team-authored. They are not independent expert labels and do not justify sensitivity, specificity, or population-performance estimates.

No frozen fixture or PDF was rewritten because of calibration. The calibration driver shares the observed-value comparator implementation, so the calibration demonstrates exercised decision behavior but not independent oracle validity.
