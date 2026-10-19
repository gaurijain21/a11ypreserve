# A11yPreserve V4 Anonymous Artifact Package

## Status

This directory is the prepared anonymous V4 manuscript/artifact entry point. It contains the manuscript source, its verified IEEE conference-format PDF build, and a machine-readable summary of the frozen primary results plus the separately frozen supplementary Word arm.

## Contents

- `main.tex` — anonymous manuscript source copied from the reviewed source.
- `sections/` — section sources included by `main.tex`.
- `main.pdf` — eight-page MiKTeX IEEEtran conference build rendered and visually checked page by page.
- `IEEEtran.cls`, `IEEEtran.bst`, `references.bib` — local build inputs.
- `v4_summary.json` — frozen counts, provenance commit, and build status.
- The reviewer-facing upload bundle includes the Word protocol, manifests, analyses, and genuine native Word PDFs; Word contributes 65 supplementary atomic observations and does not change the 130-case primary denominator.

## Reproduction entry point

From the repository root, run:

```text
python reproduce_v4.py --full-analysis
```

That command verifies the frozen source manifest, completed LO/Google/Word conversion manifests, calibration counts, analysis summaries, and cross-pipeline summary without requiring Google authentication. Word classifications can be reproduced from the included Word PDFs without running Microsoft Word desktop.

## Submission note

The exact anonymous upload bundle is one directory above this entry point at `../ICST2027_V4_anonymous_upload.zip`. Review the venue template and submission policy before upload. Word is explicitly labeled a post-freeze supplementary third-pipeline arm; the external corpus count remains zero.
