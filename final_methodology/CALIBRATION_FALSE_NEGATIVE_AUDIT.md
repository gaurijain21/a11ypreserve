# Calibration false-negative audit

## Scope

The calibration file records two false negatives among 27 controls. This audit follows both controls and checks whether their limitations could silently invalidate a frozen Core result.

| Control | Expected | Observed | Failure mode | Effect on Core result |
|---|---|---|---|---|
| hyperlinks / `alternate_named_association` | equivalent | unresolved | URI and annotation survived, but visible link-name association was not recovered | No frozen Core row is promoted to loss. The two F08 rows remain `UNRESOLVED_EQUIVALENCE`, which is the conservative response to this limitation. |
| complex_table / `positive` | equivalent | unresolved | table/header roles survived, but complete multi-level associations were not established | F10/Google remains `UNRESOLVED_EQUIVALENCE`; the method does not convert the unresolved row into a failure. |

## Audit conclusion

The false negatives expose incompleteness, not false-positive risk. They are consistent with the Core evidence overlay and are specifically why absence from one extracted encoding is not treated as semantic absence. A future comparator may add accepted mappings, but doing so is outside the frozen Core study.

