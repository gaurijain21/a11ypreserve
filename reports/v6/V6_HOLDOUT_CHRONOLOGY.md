# V6 holdout and repeatability chronology audit

## Arithmetic verified from manifests

| Quantity | Count |
|---|---:|
| Atomic fixtures | 65 |
| Variants per family | 5 |
| Primary pipelines | 2 |
| Primary fixture--pipeline observations | 130 |
| Holdout fixtures (D/E) | 26 |
| Holdout fixture--pipeline observations | 52 (26 per pipeline) |
| Non-holdout observations | 78 (39 per pipeline) |
| Word supplementary observations | 65 |

The holdout is a within-design fixture-level subset, not an independent natural-document sample. The five variants within a family are correlated by construction; no independence-based inferential statistics or converter rankings are claimed.

## Chronology findings

- `experiments/v4/HOLDOUT_MANIFEST.json` states that D/E membership and the “do not inspect holdout outputs” rule were frozen before conversion.
- `experiments/v4/V4_PROTOCOL.md` states that the source oracle, extractor, comparator, classification rules, and calibration outcomes were frozen before D/E outputs were opened.
- Git history places the V4 protocol/source-corpus freeze before the later V4 evidence-package completion. The retained manifests are the authority for the prospective design claim.
- The repeatability manifest pre-specifies six D variants (`F04_D`, `F06_D`, `F08_D`, `F11_D`, `F12_D`, `F13_D`) and three runs per pipeline, but its top-level status remains `NOT_RUN` even though the retained run outputs and result JSON exist. V6 treats this as a documentation-integrity defect and reports the actual repeatability result separately rather than silently changing the historical manifest.
- The selected repeatability subset is therefore best described as a targeted repeatability probe. The stored selection is pre-specified in the frozen protocol; the repository does not provide a complete external audit trail proving that no early result inspection influenced selection beyond that freeze record.

## Actual repeatability evidence

The retained per-pipeline result files report classification stability for all 6/6 selected fixtures across 3 runs. LibreOffice byte identity was 0/6; Google Docs byte identity was 6/6. These are repeated recorded workflows, not two Google sessions separated by at least seven days. Temporal cloud repeatability remains open.
