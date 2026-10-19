# A11yPreserve

A11yPreserve is a source-grounded, contract-based, uncertainty-aware method for testing whether selected accessibility semantics in DOCX survive DOCX-to-PDF conversion. It is not a general PDF accessibility checker, a WCAG/PDF/UA validator, a prevalence study, a universal converter ranking, or a disabled-user usability study.

## Current release: V5 / ICST 2027

The current submission is the anonymous V5 manuscript and replication bundle under [`submission/ICST2027_V5/`](submission/ICST2027_V5/). The verified paper contains 13 feature families, five variants per family, 65 atomic DOCX fixtures, and 130 primary fixture--pipeline cases across LibreOffice and Google Docs. Microsoft Word contributes 65 post-freeze supplementary observations and is not pooled into the primary denominator.

V5 adds machine-derived holdout accounting, a LibreOffice profile comparison, source and destination mutation testing, calibration ground truth, independent technical cross-checks, repeatability evidence, and explicit scope decisions. The final readiness assessment is [`FINAL_V5_RESEARCH_READINESS.md`](FINAL_V5_RESEARCH_READINESS.md).

Primary outcome counts are:

| Classification | LibreOffice | Google Docs | Word supplementary |
|---|---:|---:|---:|
| Verified preserved | 38 | 11 | 16 |
| Observed partial | 11 | 32 | 26 |
| Altered | 9 | 11 | 16 |
| Confirmed lost | 1 | 6 | 2 |
| Unresolved equivalence | 1 | 5 | 0 |
| Measurement error | 5 | 0 | 5 |

These are descriptive observations under recorded conditions, not population estimates or complete accessibility scores.

## Reproduce the V5 checks

From the repository root:

```powershell
python scripts/audit_v5_holdout_accounting.py
python scripts/audit_v5_calibration.py
python scripts/audit_v5_final_consistency.py
python tests/test_v5_hardening.py
```

The V5 evidence and analysis scripts are under [`experiments/v5/`](experiments/v5/), [`contracts/v5/`](contracts/v5/), and the [`reports/`](reports/) directory. Re-running LibreOffice profile B requires the recorded local LibreOffice runtime; repeating Google Docs requires an authorized interactive session. Credentials, cookies, browser profiles, and private account material are not distributed.

To rebuild the paper, run `powershell -ExecutionPolicy Bypass -File build.ps1` from `submission/ICST2027_V5/`. To rebuild the sanitized upload bundle, run `python build_v5_upload_bundle.py` from the repository root.

## Repository structure

| Path | Purpose |
|---|---|
| `submission/ICST2027_V5/` | Current anonymous manuscript, PDF, source, and final upload ZIP |
| `experiments/v5/` | V5 profile, mutation, extraction, and independent-validation evidence |
| `contracts/v5/` | V5 cross-format equivalence contract |
| `reports/V5_*.md` | V5 audits, adversarial review, scope decisions, and provenance notes |
| `experiments/v4/` | Frozen V4 primary corpus, manifests, outputs, and analyses |
| `artifact/`, `artifact_v3/` | Earlier review-artifact generations retained for provenance |
| `audit/`, `final_review/`, `final_strengthening/` | Historical audits and methodology-development records |
| `scripts/`, `tests/`, `tools/` | Analysis, audit, and regression code |

## Evidence boundary

The corpus is controlled and purposive. The realistic documents are project-created, Google Docs is cloud-versioned, reading order is deferred because a defensible automated oracle was not established, and no screen-reader or disabled-user task study was performed. The method therefore makes claims about selected machine-verifiable source semantics under named conversion conditions—not about overall accessibility or human impact.
