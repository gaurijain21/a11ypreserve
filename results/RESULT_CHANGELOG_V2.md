# Results changelog V2

## No primary outcome changes

No genuine factual error was proven in the frozen primary results. Therefore:

- `PRIMARY_RESULTS_FREEZE.json` remains unchanged and authoritative for outcome
  counts and the denominator.
- No `PRIMARY_RESULTS_FREEZE_V2.json` is created.
- No fixture, PDF, manifest, hash, converter, or full-experiment rerun was
  introduced.

## Evidence-status additions

The new `EVIDENCE_STATUS_FREEZE_V2.json` adds a second axis to each record:

- 11 `VERIFIED_EQUIVALENCE`
- 3 `OBSERVED_DIFFERENCE`
- 3 `OBSERVED_PARTIAL`
- 6 `UNRESOLVED_EQUIVALENCE`
- 2 `INDEPENDENTLY_CONFIRMED_ABSENCE`
- 1 `MEASUREMENT_FAILURE`

The nine frozen partial outcomes are retained. Seven are reported as unresolved
equivalence or observed partial in the re-audit; no partial is silently promoted
to a converter-induced loss. The two confirmed losses have independent source
certificates and two destination evidence paths.
