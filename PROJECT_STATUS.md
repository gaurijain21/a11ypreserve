# A11yPreserve project status

## Canonical working repository

All future A11yPreserve work must be performed in:

`C:\Gauri\a11ypreserve`

This repository is connected to `https://github.com/gaurijain21/a11ypreserve`. The previous OneDrive/ChatGPT checkout is a backup/history source only and must not receive normal development changes.

## Frozen V2

The V2 scientific content is frozen for submission targeting. The current ICST candidate is under `submission/ICST2027/`; the canonical source is under `paper/`. The V2 primary benchmark remains 13 fixtures x 2 pipelines = 26 cases, with the evidence-aware distribution recorded in `SUBMISSION_FREEZE.md`. The three-document integrated sanity check remains a separate secondary evaluation.

No migration step changes V2 fixtures, contracts, evidence, classifications, counts, research questions, or scientific interpretations.

## V3

V3 is retained as internal methodology-strengthening and robustness work. It is separated under `v3/`, `research/v3/`, `artifact_v3/`, and explicitly named V3 reports/scripts. V3 material must not be presented as part of the frozen V2 manuscript or V2 headline results unless the manuscript is intentionally revised in a future research decision.

## Repository hygiene

Machine-specific runtimes, profiles, downloads, logs, caches, Python bytecode, and TeX build products are excluded by `.gitignore` and were excluded from the migration. Historical reports may retain provenance paths where scientifically necessary; executable project scripts should resolve paths from the repository root.

## Current migration state

The repository is being verified before its first normal consolidation commit on the existing `main` branch. The migration preserves the root Git metadata and remote; it does not rewrite history or force-push.
