# Fixture coverage audit

Status: COMPLETED AND VERIFIED.

The primary design contains 13 feature families, five variants per family, 65
atomic fixtures, and 130 fixture-pipeline observations across LibreOffice and
Google Docs. The five variants within a family are correlated design variants,
not independent observations. Coverage is therefore reported as branch and
feature coverage, not as a natural-document prevalence estimate.

The machine-readable audit is `experiments/v8/V8_FIXTURE_COVERAGE.json` and the
executable check is `scripts/v8_fixture_coverage_audit.py`. Frozen holdout and
chronology documentation remains under `reports/v6/` and is not overwritten.
