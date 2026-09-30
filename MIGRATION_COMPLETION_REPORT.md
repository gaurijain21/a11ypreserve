# A11yPreserve migration completion report

## Canonical repo

`C:\Gauri\a11ypreserve`

This is now the authoritative A11yPreserve working repository. Its root Git metadata is connected to `https://github.com/gaurijain21/a11ypreserve`, and future development should start here.

## Source locations consolidated

- `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve` — complete V2/V3 research, artifact, manuscript, submission, script, evidence, and report source; retained unchanged as backup.
- `C:\Gauri\a11ypreserve\a11ypreserve` — older nested checkout; retained as `C:\Gauri\a11ypreserve_nested_backup_20260929` after its older PDF was inspected.

## Files migrated

The canonical root contains the V2 corpus, contracts, evidence, results, integrated study, V3 methodology work, scripts, tests, manuscript sources, venue/submission copies, sanitized artifact sources and archives, methodology audits, review reports, and project documentation. The V2 and V3 materials remain separated by directory and filename conventions.

Machine-specific runtimes, downloads, profiles, logs, caches, Python bytecode, and LaTeX build products were excluded. No credentials, browser state, or personal environment artifacts were copied.

## Scientific freezes verified

- `paper/main.tex`: `C589481C302D50AAEE949A4FE0AB5B5EDA415AEA0B1DDAB9B0D24459CF216D27`
- `paper/references.bib`: `4B788CD0148D9800F6F47560A80B4376929C30D8BC914F95BC14ED078DED6F7B`
- V2 evidence-aware result JSON: `04FD89CF44FE9B158A4D1FB3FB5B396A87BF4EADC83081A13C6C4EA14994AEB3`
- ICST submission PDF: `22AFD73963E0186B9E75A73DA022312E111930C14ED4AFF091FCF1D8C982CAC5`
- V2 artifact ZIP: `EE343279DC86F9991D3C378D0676D17B2B8DF05545C40561B92FC81E0400E39D`

The older nested 8-page PDF was preserved as `paper/historical/main_pre_final_8page.pdf`; it is not the frozen V2 canonical PDF. `submission/ICST2027/main.pdf` is the verified current submission PDF.

## Tests and validation

- Hash comparison of 1,623 intended migrated source files: 0 mismatches.
- Python syntax parsing: 78 repository Python files parsed successfully.
- `scripts/phase4_tests.py`: passed; 13 fixtures and 9 taxonomy cases.
- `scripts/full_experiment_tests.py`: passed; 26 validation records and 26 differential records.
- Sensitive-pattern scan: no private keys, API keys, credential assignments, tokens, cookies, or browser-state artifacts found.
- Executable-script old-path scan: no references to the old OneDrive project path remain.
- No Google Docs experiment or new scientific experiment was rerun.

## Sensitive-data scan

Passed. The migration excluded machine-specific runtimes, profiles, downloads, logs, caches, bytecode, and temporary TeX products. Historical internal reports may retain provenance paths, as documented in `MIGRATION_INVENTORY.md`; executable scripts no longer depend on the old project path.

## Git branch

`main`

## Final commit

`a6cc060` — `Consolidate A11yPreserve research and submission materials`

## Push status

The commit was pushed successfully without force options. `main` now tracks `origin/main`.

## Remaining files outside canonical repo

- The old OneDrive/ChatGPT checkout remains unchanged as a safety backup.
- The older nested checkout remains at `C:\Gauri\a11ypreserve_nested_backup_20260929` as a separate backup, not as an active working copy.
- Excluded runtime/profile/download/cache material remains only in the prior source locations and was not copied into the canonical repository.

## Safe to use canonical repo?

**YES.** Use `C:\Gauri\a11ypreserve` for all future A11yPreserve work.
