# Calibration ground-truth table

The 27 controls in `final_strengthening/COMPARATOR_CALIBRATION.json` are diagnostic controls, not samples of converter behavior. The table below separates independently authored control intent from comparator output. `CORRECT_UNRESOLVED` is a safe abstention only when the control was deliberately designed to be unresolved; it is not successful recognition of equivalence.

| Control outcome | Count | Interpretation |
|---|---:|---|
| correct determinate | 12 | comparator made the expected definitive call |
| correct deliberate abstention | 6 | control expected unresolved and comparator abstained |
| false positive | 0 | comparator claimed equivalence for a known-different control |
| false negative | 2 | control expected equivalence but comparator abstained |
| other unresolved/indeterminate | 7 | control outcome was not a definitive equivalence/difference decision |

The two false negatives are `hyperlinks/alternate_named_association` and `complex_table/positive`. They show conservative incompleteness in accepted-equivalence recognition. They are not silently relabeled as correct. The calibration also contains negative controls observed as unresolved; this prevents the calibration from being interpreted as a complete sensitivity/specificity estimate.

## Calibration conclusion

The comparator is empirically supported for the tested direct representations and is conservative for several alternate encodings. The evidence justifies surfacing `UNRESOLVED_EQUIVALENCE`; it does not justify a claim of complete oracle coverage.

