# Scientific-strengthening baseline

Recorded: 2026-10-03

This file records the state protected before the additive scientific-strengthening pass. It is a provenance record, not a replacement for the frozen experiment.

## Repository state

- Repository: `<REPOSITORY_ROOT>`
- Branch: `master`
- HEAD before this pass: `7043a2164dce6ef162aeed7655d90c3e92bbbb68`
- No remote is configured.
- The worktree was clean with respect to tracked files. The only pre-existing untracked file was `docs/FINAL_PRIOR_ART_RED_TEAM.md`; it was not modified or removed.
- No frozen evidence file was changed as part of recording this baseline.

## Submission files

| File | SHA-256 | Bytes |
|---|---|---:|
| `submission/ICST2027_V3/main.pdf` | `E720EB8EB58898F592491E7BB67DB739E09BA1D670E222350E2465B5C435199D` | 143,861 |
| `submission/A11yPreserve_artifact_ICST2027_V3.zip` | `EE599CC68956390D3A608AFC1D80AF016CF3680A86F3E9137C1BB14202DD2E62` | 4,757,239 |

The manuscript PDF had already passed visual/build QA before this pass. The artifact ZIP is the frozen submission artifact; any later additive artifact must not silently replace it.

## Frozen experiment status

- Controlled fixtures: 26 total (13 Core and 13 Variant B).
- Converter pipelines: LibreOffice 26.2.6.3 and the Google Docs DOCX-to-PDF route.
- Canonical fixture-pipeline rows: 52.
- Canonical outcome counts: 18 `VERIFIED_PRESERVED`, 4 `OBSERVED_PARTIAL`, 7 `ALTERED`, 4 `CONFIRMED_LOST`, 18 `UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR`.
- Google repeatability: 13 fixtures × 3 runs = 39 outputs; all were byte-identical and classifications were stable.
- Integrated multi-feature sanity check: 3 project-generated documents and 42 property-pipeline observations, reported separately from the 52 canonical rows.
- Artifact verification command: `python artifact_v3/src/verify_public_package.py`.
- Verification result at baseline: PASS; 52 records checked and no failures.

## Protected evidence

The following remain the baseline and are not rewritten by this pass:

- Core and Variant B fixtures;
- existing LibreOffice and Google converted outputs;
- frozen classifications, hashes, and provenance links;
- canonical result rows and the current artifact ZIP;
- existing comparator and extractor behavior, unless a separate additive analysis explicitly demonstrates a safe measurement improvement without rewriting baseline rows.

New interaction fixtures, Word-feasibility attempts, unresolved-case analyses, baselines, and testing-literature material are additive and must be labeled as such. If any additive analysis identifies a possible defect in frozen evidence, it must be documented separately rather than silently repaired.

