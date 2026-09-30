# SCIENTIFIC CONTENT FROZEN FOR SUBMISSION TARGETING

This freeze records the canonical scientific content after the two final wording-only repairs requested for submission packaging. Venue formatting, anonymization, and artifact sanitization must be performed in separate copies.

## Freeze date

2026-09-29 (America/Los_Angeles)

## Canonical manuscript

- Source bundle: `paper/main.tex` plus every file under `paper/sections/*.tex`, sorted by path and hashed as a UTF-8 manifest of relative path and SHA-256.
- Manuscript source bundle SHA-256: `50F67F4970D5E10C9377BCEFC153017B7023B11375DB4BB2B043758DAEA28C0D`
- `paper/main.tex` SHA-256: `C589481C302D50AAEE949A4FE0AB5B5EDA415AEA0B1DDAB9B0D24459CF216D27`
- `paper/references.bib` SHA-256: `4B788CD0148D9800F6F47560A80B4376929C30D8BC914F95BC14ED078DED6F7B`

## Canonical PDF record

The historical final build record reports a 10-page canonical PDF with SHA-256
`BDD9FE6A31E17DA034117C66324389487E13B7F374A62F97F0BDF8B4B656EEF4`, but
`paper/main.pdf` is not present in the current checkout and could not be
rehashed here. The source and evidence hashes below remain the authoritative
scientific freeze.

## Verified venue PDF

- Path: `submission/ICST2027/main.pdf`
- Pages: 9
- Bytes: 143,213
- SHA-256: `22AFD73963E0186B9E75A73DA022312E111930C14ED4AFF091FCF1D8C982CAC5`
- Build: MiKTeX pdfTeX 25.12, BibTeX, and two final LaTeX passes.
- Visual QA: all 9 rendered pages under `submission/ICST2027/rendered/` were inspected; no clipping, overlap, unreadable table, malformed figure, broken reference, or overfull box was found.

## Frozen evidence result

- `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` SHA-256: `04FD89CF44FE9B158A4D1FB3FB5B396A87BF4EADC83081A13C6C4EA14994AEB3`
- Primary cases: 26.
- Evidence-aware distribution: 11 VERIFIED_PRESERVED, 3 OBSERVED_PARTIAL, 3 ALTERED, 2 CONFIRMED_LOST, 6 UNRESOLVED_EQUIVALENCE, and 1 MEASUREMENT_ERROR.
- Historical V1 classifications remain archived and are not the manuscript headline.

## Version-control state

- Repository: Git work tree confirmed.
- HEAD at freeze: `55520e491d6b8b1dcc407e429e5025e22cac73a5`
- This record does not imply that the work tree is clean or that a commit was created.

## Prohibited post-freeze changes

Do not change fixtures, source contracts, manifests, PDF outputs, result classifications, frozen result JSON, result counts, research questions, or scientific interpretations. Any venue adaptation must be a separate submission copy and must be checked against this record.
