# A11yPreserve migration inventory

## Destination repository

`C:\Gauri\a11ypreserve`

This is the canonical working repository. Its existing root `.git` metadata was preserved; the configured remote is `https://github.com/gaurijain21/a11ypreserve`.

## Previous working locations

| Source | Initial state | Disposition |
|---|---|---|
| `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve` | Most complete/current working tree; `master`, HEAD `55520e4` (`audit: record scope-change decision and pilot findings`), with V2/V3, submission, artifact, and uncommitted research files | Copied into the destination root, excluding Git metadata and machine-specific runtime/cache material; retained as backup and not modified by this migration |
| `C:\Gauri\a11ypreserve\a11ypreserve` | Older nested checkout; `master`, HEAD `55520e4`, no remote configured | Used only to identify the older 8-page PDF; that PDF was preserved as `paper/historical/main_pre_final_8page.pdf`. The nested checkout was moved to `C:\Gauri\a11ypreserve_nested_backup_20260929` after verification |

## Major project material

| Source location | Purpose | Destination | Decision |
|---|---|---|---|
| `paper/`, `paper/sections/`, `paper/references.bib` | Canonical manuscript source, audits, and bibliography | `paper/` | OneDrive version selected because it contains the final V2 wording repairs and freeze-aligned source hashes |
| `results/`, `evidence/`, `contracts/`, `corpus/` | Frozen V2 evidence, contracts, fixtures, manifests, and result files | Same relative paths | Copied and hash-checked |
| `v3/`, `research/v3/`, `artifact_v3/`, V3 reports/scripts | Internal V3 methodology-strengthening work | Same relative paths | Copied separately; not presented as part of the frozen V2 manuscript |
| `submission/`, `SUBMISSION_FREEZE.md`, `SUBMISSION_TARGETING_REPORT.md` | Submission package and venue preparation | Same relative paths | Copied; ICST package retained as the current submission candidate |
| `artifact/`, `submission/A11yPreserve_artifact_ICST2027.zip` | Sanitized V2 replication artifact source and archive | Same relative paths | Copied; archive remains available for later human license/metadata decisions |
| `scripts/`, `tests/` | Reproduction, analysis, packaging, and validation code | Same relative paths | Copied, excluding Python bytecode |
| `docs/`, `final_methodology/`, `final_review/`, `final_strengthening/`, `integrated_study/` | Methodology, review, strengthening, and secondary-study documentation | Same relative paths | Copied and retained |

## Intentionally excluded machine-specific material

The copy excluded `.git`, `.miktex`, Python bytecode/cache, LibreOffice runtimes and profiles, 7-Zip runtime files, downloaded installers, temporary execution logs, and generated LibreOffice profile trees. These are not required for repository-based reproduction and may contain machine-specific state. Their exclusion is recorded here rather than silently omitted.

## Conflict decisions

- The OneDrive `paper/main.tex`, bibliography, V2 evidence JSON, ICST submission package, and V2/V3 work were selected over the older nested checkout because the OneDrive tree contains the later freeze and submission work.
- The nested `paper/main.pdf` was an 8-page pre-final build with SHA-256 `be69b88cec82425d94a1807015037b8bc2352898232843440a3d0efb69f86480`; it was not allowed to overwrite the frozen V2 record and was moved to `paper/historical/main_pre_final_8page.pdf`.
- The current submission PDF is `submission/ICST2027/main.pdf`, 9 pages, SHA-256 `22AFD73963E0186B9E75A73DA022312E111930C14ED4AFF091FCF1D8C982CAC5`.

No source material was deleted from either previous working location during the initial copy.
