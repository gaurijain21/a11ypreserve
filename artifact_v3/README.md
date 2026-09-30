# A11yPreserve V3 artifact candidate

A11yPreserve is a controlled, source-grounded, uncertainty-aware conformance method for testing whether machine-verifiable accessibility information present in DOCX survives DOCX-to-PDF conversion. It is not a complete PDF accessibility validator and does not measure disabled-user usability.

## Contents

- `corpus/fixtures/`: the frozen Core DOCX fixtures.
- `corpus/v3_variant_set_b/`: the 13 pre-specified Variant B DOCX fixtures, manifests, and source-oracle report.
- `corpus/outputs/`: frozen Core V2 outputs.
- `v3/google_repeatability/`: 26 new Core Google PDFs, hashes, run manifest, and repeatability reports.
- `v3/variant_set_b/`: LibreOffice and Google Variant B PDFs, extraction records, hashes, and final matrix.
- `contracts/`: machine-readable source/destination contracts and V3 classification rules.
- `results/V3_PRIMARY_RESULTS.json`: the 52-case atomic result record.
- `results/V3_WITHIN_FEATURE_CONSISTENCY.md`: Core-versus-Variant feature-family interpretation.
- `final_methodology/`: calibration false-negative impact and related evidence.
- `src/`: source-oracle, extraction, audit, freezing, and V3 analysis scripts.

## V3 denominators

- Atomic benchmark: 26 controlled fixtures x 2 named pipelines = 52 cases.
- Google repeatability: 13 Core fixtures x 3 runs = 39 conversions.
- Integrated sanity check: 3 project-generated multi-feature documents and 42 property--pipeline observations; separate denominator.

The atomic counts are 18 VERIFIED_PRESERVED, 4 OBSERVED_PARTIAL, 7 ALTERED, 4 CONFIRMED_LOST, 18 UNRESOLVED_EQUIVALENCE, and 1 MEASUREMENT_ERROR. Unresolved is a conservative abstention, not a loss finding.

## Reproducibility levels

### Level 1 — verify existing evidence

Inspect contracts, manifests, source hashes, PDF hashes, extraction records, and the machine-readable V3 results. Existing PDF analysis can be rerun with the included extractor and comparator dependencies.

### Level 2 — reproduce LibreOffice conversion

Use LibreOffice 26.2.6.3 with the recorded tagged-PDF/PDF-UA settings. Compare any new output by hash and then by evidence-aware classification; a changed binary hash is not automatically a classification change.

### Level 3 — repeat Google Docs conversion

Upload the exact DOCX through an authenticated Google Docs session and use the recorded DOCX-to-PDF workflow. The service backend cannot be fully pinned. The Variant B report documents that its saved outputs used the in-session export backend after the visible download action did not register. No credentials, cookies, browser profiles, or account state are included.

## Commands

From the artifact root, after installing the documented Python dependencies:

```powershell
python src/independent_source_oracle.py
python src/v3_difficult_variant_audit.py
python src/v3_finalize_repeatability.py
```

The V3 output PDFs and hashes are already included; no conversion is required to inspect or reproduce the analysis reports.

## Limitations

The corpus is controlled and purposive, not representative. Feature families have unequal complexity, F13 reading order was deferred because reliable automated equivalence was unavailable, and no comprehensive adequacy metric is claimed. Results concern machine-verifiable structural preservation under two named pipelines, not complete accessibility, user impact, product superiority, or all future software versions.

This is a candidate artifact package. Human review is still required for the final license, author metadata, venue anonymity, and public-release decision.
