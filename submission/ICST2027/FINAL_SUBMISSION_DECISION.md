# READY WITH MINOR HUMAN CHECKS

Audit date: 2026-09-29

## Repository state

The canonical repository is `C:\Gauri\a11ypreserve`, on branch `main`, clean before this audit package was added, with `origin` configured as the GitHub remote. The frozen upload files were verified against baseline commit `4066cf79fd7043e904e285f09fd85ff179a4cb3b` and remain unchanged.

## V2 integrity

The candidate is the frozen V2 ICST package under `submission/ICST2027/`. The primary study remains 13 fixtures × 2 pipelines = 26 cases, with 11 VERIFIED PRESERVED, 3 OBSERVED PARTIAL, 3 ALTERED, 2 CONFIRMED LOST, 6 UNRESOLVED EQUIVALENCE, and 1 MEASUREMENT ERROR. The separate sanity check remains 3 documents, 21/21 source assertions, and 42 property–pipeline observations. No V3 result is part of the paper or upload artifact.

## Paper and artifact

- Paper: 9 pages; SHA-256 `22AFD73963E0186B9E75A73DA022312E111930C14ED4AFF091FCF1D8C982CAC5`.
- Artifact: 158 ZIP members; SHA-256 `EE343279DC86F9991D3C378D0676D17B2B8DF05545C40561B92FC81E0400E39D`.
- Full trace: `FINAL_CLAIM_ARTIFACT_TRACE.md`.
- Exact-file record: `FINAL_UPLOAD_FREEZE.md`.

## Audit results

- Visual QA: PASS on every page 1–9; no clipping, overprinting, malformed page, missing figure, broken character, or unreadable table observed.
- Citations and references: PASS; 13 unique citation keys match 13 unique bibliography entries, with no missing keys, duplicate keys, placeholders, or undefined-reference markers.
- Fonts and PDF technical checks: PASS; letter-sized pages, searchable text, parseable objects, and embedded font files.
- Double anonymity: PASS for paper and artifact scans; PDF metadata has no author identity, and artifact content has no credentials, browser state, Git metadata, or local-path leak.
- AI disclosure: PASS; the disclosure is anonymous and does not assign ground truth, independent human validation, or autonomous adjudication to AI systems.
- Artifact sanitization: PASS; target sensitive-leak scan found none. The only cookie match was explanatory README text stating that cookies are excluded.
- Paper/artifact consistency: PASS; see the claim trace.
- Desk-rejection audit: PASS with only ordinary human portal checks remaining; see `FINAL_DESK_REJECTION_AUDIT.md`.

## Git tag

After this audit package is committed and the working tree is confirmed clean, create and push the annotated tag `icst2027-submission-candidate-v1` with message `Frozen ICST 2027 V2 submission candidate`. The tag must point to the clean commit containing these final audit records. No force operation is authorized.

## Remaining human actions

Use the concise list in the repository-root `HUMAN_SUBMISSION_STEPS.md`. In particular, the researcher must enter real author metadata in the portal, complete originality/concurrency and any portal-specific AI or license declarations, inspect the portal-rendered PDF, and personally approve the final submission.

This decision does not submit the paper, upload to arXiv, publish the repository, or change the scientific content.
