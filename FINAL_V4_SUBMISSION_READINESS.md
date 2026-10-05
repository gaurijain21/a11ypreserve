# GO WITH LIMITATIONS

## Conversion-dependent readiness

- Frozen atomic fixtures: 65
- Established V4 pipelines: 1 (LibreOffice)
- LibreOffice atomic cases: 65/65
- LibreOffice realistic documents: 10/10
- LibreOffice realistic property contracts: 78
- Google Docs cases: 0; authenticated session usable, upload pending explicit confirmation
- Word cases: 0; launch failed before conversion with `0x80070520`

## LibreOffice atomic counts

| Classification | Count |
|---|---:|
| VERIFIED_PRESERVED | 38 |
| OBSERVED_PARTIAL | 11 |
| ALTERED | 9 |
| CONFIRMED_LOST | 1 |
| UNRESOLVED_EQUIVALENCE | 1 |
| MEASUREMENT_ERROR | 5 |

Holdout D/E: 26 cases; 14 VERIFIED_PRESERVED, 5 OBSERVED_PARTIAL, 4 ALTERED, 1 CONFIRMED_LOST, 2 MEASUREMENT_ERROR.

## Replacement decision

V4 is not approved to replace V3 as the repository’s primary submission evidence yet. V4 has a complete and auditable one-pipeline arm, but V3 has two completed pipelines and a completed Google repeatability arm. V4 is ready as a bounded LibreOffice extension and becomes materially stronger if the authenticated Google route is completed under one consistent V4 workflow.

## Frozen-methodology status

No frozen methodology, taxonomy, contract, fixture, protocol, comparator, oracle, or extractor changed after output inspection. The new runner is an implementation layer around the frozen extractor/comparator and does not manually select classifications.

See `reports/V4_CONVERSION_RECOVERY_FINAL.md` and `reports/V4_OUTPUT_PROVENANCE_AUDIT.md` for the complete decision and audit trail.
