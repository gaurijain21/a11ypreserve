# A11yPreserve conformance suite

A11yPreserve is organized as a source-to-destination preservation suite. A
future converter adapter conceptually implements:

```text
run(adapter, source_docx, output_directory, environment) -> ConversionRecord
```

The adapter records the converter name, version or backend description, input
SHA-256, output SHA-256, invocation/workflow metadata, timestamps, and a
parseability/validity result. It does not decide preservation. The suite then:

1. loads the versioned source contract;
2. verifies the source hash and independent source certificate;
3. runs destination extraction through one or more evidence paths;
4. compares only the contract's feature-specific fields;
5. records both the frozen outcome category and the evidence status; and
6. emits raw observations, certificates, and a reproducibility manifest.

The low-level contract/comparator layer retains the historical outcome enums
`PRESERVED`, `PARTIALLY_PRESERVED`, `ALTERED`, `LOST`, and
`MEASUREMENT_ERROR` for provenance and compatibility. The paper's frozen V2
result model is evidence-aware and reports the primary outcomes as
`VERIFIED_PRESERVED`, `OBSERVED_PARTIAL`, `ALTERED`, `CONFIRMED_LOST`,
`UNRESOLVED_EQUIVALENCE`, and `MEASUREMENT_ERROR`. Its evidence statuses are
`VERIFIED_EQUIVALENCE`, `OBSERVED_DIFFERENCE`, `OBSERVED_PARTIAL`,
`INDEPENDENTLY_CONFIRMED_ABSENCE`, `UNRESOLVED_EQUIVALENCE`,
`INSUFFICIENT_EVIDENCE`, and `MEASUREMENT_FAILURE`.

The frozen primary distribution is 11 `VERIFIED_PRESERVED`, 3
`OBSERVED_PARTIAL`, 3 `ALTERED`, 2 `CONFIRMED_LOST`, 6
`UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR` across 26
fixture--pipeline cases. Historical V1 labels remain archived and are not the
scientific headline.

The interface is intentionally conceptual in this release. No new converter is
added and no frozen output is regenerated. The current artifact supplies the
contracts, source certificates, calibration harness, PDF triangulation, and
provenance needed for a future adapter implementation.
