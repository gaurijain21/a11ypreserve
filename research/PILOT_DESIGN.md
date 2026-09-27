# Pilot Design

## Fixture

`G01_semantic_fixture` contains: document title, H1/H2 hierarchy, document language `en-US`, an inline `es-MX` span, nested lists with depths 0/1/0, one informative image alternative, one decorative image, and a table with a header row. The HTML and DOCX forms are paired with an author manifest.

## Planned matrix

| Source | Target | Engine | Status |
|---|---|---|---|
| HTML | PDF | Chrome headless | Completed in pilot |
| DOCX | PDF | Word/Acrobat | Attempted; output not confirmed |
| DOCX | HTML | Word filtered HTML | Script exists; COM unavailable in this environment |
| HTML | EPUB | Calibre/other | Deferred until a reproducible engine is available |

## Outcome rules

- `PRESERVED`: equivalent value and structure verified.
- `DEGRADED`: feature survives with reduced fidelity.
- `LOST`: absence verified by a capable output adapter or independent manual check.
- `MUTATED`: output value differs without evidence of intentional regeneration.
- `REGENERATED`: output value is newly created by the converter, with provenance.
- `NOT_REPRESENTABLE`: destination lacks an equivalent mechanism.
- `NOT_APPLICABLE`: feature is not present in the source/route.
- `INVALID_CONVERSION`: artifact cannot be opened/validated as the declared format.
- `MEASUREMENT_ERROR`: artifact may contain the feature but the current measurement path cannot establish it.

## Pass criteria

The method passes when it produces a machine-readable per-feature record, refuses to overclaim from missing parser fields, identifies a known negative control, and agrees with manual/AT checks on a selected subset. A publication-grade pilot additionally needs two independent engines and pre-registered fixture expectations.

