# Reproducibility and provenance

## Executed commands

```text
python scripts/v7_independent_oracle_audit.py
python scripts/v7_semantic_equivalence_audit.py
python scripts/v7_association_attack_audit.py
python scripts/v7_competitive_baseline.py
python scripts/v7_cross_parser_audit.py
python scripts/verify_v6_scientific_accounting.py
python scripts/audit_v6_manuscript_consistency.py
python tests/test_v6_scientific_hardening.py
python scripts/verify_v6_upload_bundle.py
python scripts/verify_v6_package_manifest.py
python scripts/audit_v6_anonymity.py
python scripts/audit_repository_safety.py
git diff --check
```

## Environment

The V7 scripts used Python 3.11, pypdf 6.18.1, PyMuPDF 1.28.2, and the local
archived PDFs. GUI/cloud conversion was not rerun. PAC and veraPDF were not
installed, so no standards-conformance claim is made.

## Preservation

All new records are under `experiments/v7/`; V4/V5/V6 evidence remains in its
original paths. The manuscript remains under the established submission path,
and the anonymous package now includes the additive adversarial evidence and
the 10-page PDF. V7 is an additive research audit; it does not rewrite frozen
V4/V5/V6 classifications or denominators.
