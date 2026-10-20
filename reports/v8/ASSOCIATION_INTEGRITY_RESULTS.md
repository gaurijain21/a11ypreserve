# Association-integrity results

Status: COMPLETED WITH LIMITATIONS.

The prior one-per-family association attack remains preserved: 13 attempts, 12
applied/valid/scorable, and 11 coarse-classification detections. The separate
complex-table role-delta diagnostic detected a `/TH` delta in 5/5 cases while
the historical category could remain `OBSERVED_PARTIAL`. The new ground-truth
audit confirms that complex-table `F10_A`, `F10_B`, and `F10_E` are direct
contract faults not coarse-detected, and that caption cases `F13_B`, `F13_C`,
and `F13_E` are also direct role faults despite unchanged coarse labels.

The available fixtures generally contain one relevant semantic object, so a
multi-object swap oracle was not promoted. This is an honest design boundary,
not a claim that association integrity is fully tested.

Evidence: `experiments/v7/V7_ASSOCIATION_ATTACKS.json`,
`experiments/v7/V7_COMPLEX_TABLE_DIAGNOSTIC.json`, and
`experiments/v8/V8_MUTATION_GROUND_TRUTH.json`.
