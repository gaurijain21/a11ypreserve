# A11yPreserve

A11yPreserve is a source-grounded, contract-based, uncertainty-aware method for testing whether selected accessibility semantics in DOCX survive DOCX-to-PDF conversion. It is not a general PDF accessibility checker, a WCAG/PDF/UA validator, a prevalence study, a universal converter ranking, or a disabled-user usability study.

## Current release: V5 / ICST 2027

The canonical submission is the anonymous V5 manuscript and replication bundle under [`submission/ICST2027_V5/`](submission/ICST2027_V5/). V3 and V4 material is retained as historical provenance, not as alternate current submissions. The verified paper contains 13 feature families, five variants per family, 65 atomic DOCX fixtures, and 130 primary fixture--pipeline cases across LibreOffice and Google Docs. Each primary conversion manifest has 75 records: 65 atomic plus 10 project-created realistic integrated records. Microsoft Word contributes 65 post-freeze supplementary observations and is not pooled into the primary denominator.

V5 adds machine-derived holdout accounting, a LibreOffice profile comparison, source and destination mutation testing, calibration ground truth, an independent diagnostic cross-check, repeatability evidence, and explicit scope decisions. The final readiness assessment is [`FINAL_V5_RESEARCH_READINESS.md`](FINAL_V5_RESEARCH_READINESS.md); the issue-by-issue closure is [`reports/V5_GAP_CLOSURE_REPORT.md`](reports/V5_GAP_CLOSURE_REPORT.md).

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
python scripts/reproduce_v5.py
```

Install Python dependencies first with `python -m pip install -r requirements-v5.txt`. Use `python scripts/reproduce_v5.py --refresh-artifacts` only when intentionally regenerating the 65-row destination mutation audit and anonymous bundle. The V5 evidence and analysis scripts are under [`experiments/v5/`](experiments/v5/), [`contracts/v5/`](contracts/v5/), and the [`reports/`](reports/) directory. Re-running LibreOffice profile B requires the recorded local LibreOffice runtime; repeating Google Docs requires an authorized interactive session. Credentials, cookies, browser profiles, and private account material are not distributed.

To rebuild the paper, run `powershell -ExecutionPolicy Bypass -File build.ps1` from `submission/ICST2027_V5/`. To rebuild the sanitized upload bundle, run `python build_v5_upload_bundle.py` from the repository root. Release details are in [`docs/V5_RELEASE.md`](docs/V5_RELEASE.md).

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

The corpus is controlled and purposive. The holdout is within-family/within-variant, not a fully independent natural corpus. The realistic documents are project-created, Google Docs is cloud-versioned, reading order is deferred because a defensible automated oracle was not established, and no screen-reader or disabled-user task study was performed. No PDF/A or PDF/UA conformance claim is made because a standards validator was unavailable. The method therefore makes claims about selected machine-verifiable source semantics under named conversion conditions—not about overall accessibility, serialization identity, standards conformance, or human impact.
