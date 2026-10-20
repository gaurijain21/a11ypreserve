# A11yPreserve

A11yPreserve is a source-grounded, contract-based, uncertainty-aware method for testing whether selected accessibility semantics in DOCX survive DOCX-to-PDF conversion. It is not a general PDF accessibility checker, a WCAG/PDF/UA validator, a prevalence study, a universal converter ranking, or a disabled-user usability study.

## Current scientific-hardening release: V6 / ICST 2027

The V6 scientific-hardening source is under [`submission/ICST2027_V6/`](submission/ICST2027_V6/). The V5 manuscript and upload bundle under [`submission/ICST2027_V5/`](submission/ICST2027_V5/) remain preserved historical artifacts. V3 and V4 material is also retained as historical provenance. The frozen study contains 13 feature families, five variants per family, 65 atomic DOCX fixtures, and 130 primary fixture--pipeline cases across LibreOffice and Google Docs. Each primary conversion manifest has 75 records: 65 atomic plus 10 project-created realistic integrated records. Microsoft Word contributes 65 post-freeze supplementary observations and is not pooled into the primary denominator.

V6 adds a genuine 65-case control rerun, richer destination mutation traces, executable baselines/ablations, family-level mutation sensitivity, and static package-integrity checks. The evidence package is [`reports/v6/V6_MASTER_AUDIT.md`](reports/v6/V6_MASTER_AUDIT.md); remaining gaps are [`reports/v6/V6_REMAINING_GAPS.md`](reports/v6/V6_REMAINING_GAPS.md).

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

## Reproduce the V6 scientific checks

From the repository root:

```powershell
python -m pip install -r requirements-v6.txt
python scripts/reproduce_v6.py
```

The V6 run genuinely recomputes the 65 controls, 65 destination mutations, and 130 primary baseline observations. It writes only under `experiments/v6/` and `reports/v6/`; V4/V5 evidence is not overwritten. PAC/veraPDF, authenticated Google Docs temporal reruns, natural-document validation, and human usability studies are separate blocked/future arms.

## Reproduce the V5 checks

From the repository root:

```powershell
python scripts/reproduce_v5.py
```

Install Python dependencies first with `python -m pip install -r requirements-v5.txt`. V5 artifacts are historical and immutable; `python scripts/reproduce_v5.py` verifies them without refreshing outputs. Use `python scripts/reproduce_v6.py` for fresh control, mutation, and baseline computations. The V5 evidence and analysis scripts are under [`experiments/v5/`](experiments/v5/), [`contracts/v5/`](contracts/v5/), and the [`reports/`](reports/) directory. Re-running LibreOffice profile B requires the recorded local LibreOffice runtime; repeating Google Docs requires an authorized interactive session. Credentials, cookies, browser profiles, and private account material are not distributed.

To rebuild the paper, run `powershell -ExecutionPolicy Bypass -File build.ps1` from `submission/ICST2027_V5/`. To rebuild the sanitized upload bundle, run `python build_v5_upload_bundle.py` from the repository root. Release details are in [`docs/V5_RELEASE.md`](docs/V5_RELEASE.md).

## Repository structure

| Path | Purpose |
|---|---|
| `submission/ICST2027_V5/` | Current anonymous manuscript, PDF, source, and final upload ZIP |
| `submission/ICST2027_V6/` | Additive V6 manuscript source and compiled 9-page IEEE PDF; build provenance is recorded in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json` |
| `experiments/v5/` | V5 profile, mutation, extraction, and independent-validation evidence |
| `experiments/v6/` | V6 per-case control, mutation, baseline, and package-manifest evidence |
| `contracts/v5/` | V5 cross-format equivalence contract |
| `reports/V5_*.md` | V5 audits, adversarial review, scope decisions, and provenance notes |
| `reports/v6/` | V6 reports, traceability, remaining gaps, and human checklists |
| `experiments/v4/` | Frozen V4 primary corpus, manifests, outputs, and analyses |
| `artifact/`, `artifact_v3/` | Earlier review-artifact generations retained for provenance |
| `audit/`, `final_review/`, `final_strengthening/` | Historical audits and methodology-development records |
| `scripts/`, `tests/`, `tools/` | Analysis, audit, and regression code |

## Evidence boundary

The corpus is controlled and purposive. The holdout is within-family/within-variant, not a fully independent natural corpus. The realistic documents are project-created, Google Docs is cloud-versioned, reading order is deferred because a defensible automated oracle was not established, and no screen-reader or disabled-user task study was performed. No PDF/A or PDF/UA conformance claim is made because a standards validator was unavailable. The method therefore makes claims about selected machine-verifiable source semantics under named conversion conditions—not about overall accessibility, serialization identity, standards conformance, or human impact.
