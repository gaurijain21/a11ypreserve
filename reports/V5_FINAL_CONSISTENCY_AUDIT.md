# V5 final consistency audit

Status: **PASS**.

The audit checks frozen corpus sizes, primary/supplementary denominators, holdout arithmetic, calibration, destination mutations, LibreOffice profile completion, realistic-document count, exact classification sums, manuscript tokens, and V4 provenance references.

- `atomic_fixture_count`: PASS
- `feature_family_count`: PASS
- `variants_per_family`: PASS
- `primary_denominator`: PASS
- `supplementary_denominator`: PASS
- `holdout_denominator`: PASS
- `calibration_denominator`: PASS
- `destination_mutations`: PASS
- `libreoffice_profile_b`: PASS
- `realistic_documents`: PASS
- `primary_counts_libreoffice`: PASS
- `primary_counts_google`: PASS
- `supplementary_counts_word`: PASS
- `manifest_record_composition`: PASS
- `manuscript_primary_numbers`: PASS
- `v4_provenance_exists`: PASS

The aggregate V4 accounting is 130 primary + 65 supplementary Word = 195 archived atomic observations. Supplementary Word rows are not included in the primary denominator.
