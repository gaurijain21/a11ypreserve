# Methodology evolution

The initial Core experiment used five labels: `PRESERVED`, `PARTIALLY_PRESERVED`, `ALTERED`, `LOST`, and `MEASUREMENT_ERROR`. The evidence-aware taxonomy was introduced after methodology review because a destination extractor could observe a difference without proving semantic loss, and because alternate valid PDF representations could not always be ruled out.

The final decision procedure adds `VERIFIED_PRESERVED`, `OBSERVED_PARTIAL`, `CONFIRMED_LOST`, `UNRESOLVED_EQUIVALENCE`, and `MEASUREMENT_ERROR`, with a separate evidence-status axis. The stored Core source files, PDFs, hashes, and raw observations were not changed. Label-hidden reclassification reproduced all 26 Core decisions under the final procedure; this is a reproducibility check, not independent adjudication.

The Core portion was not preregistered under the final taxonomy. The final rules and Variant B fixture mapping were frozen before Variant B outputs were collected, with the freeze recorded in `corpus/v3_variant_set_b/V3_VARIANT_FREEZE.md`. No Variant C was completed, so there is no unreported holdout result.
