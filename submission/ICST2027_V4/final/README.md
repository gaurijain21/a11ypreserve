# A11yPreserve V4 Anonymous Artifact Package

## Status

This directory is the prepared anonymous V4 manuscript/artifact entry point. It contains the manuscript source, its verified three-page PDF build, and a machine-readable summary of the frozen results.

## Contents

- `main.tex` — anonymous manuscript source copied from the reviewed source.
- `main.pdf` — MiKTeX build rendered and visually checked page by page.
- `v4_summary.json` — frozen counts, provenance commit, and build status.

## Reproduction entry point

From the repository root, run:

```text
python reproduce_v4.py --full-analysis
```

That command verifies the frozen source manifest, completed LO/Google conversion manifests, calibration counts, analysis summaries, and cross-pipeline summary without requiring Google authentication.

## Submission note

Review the venue template and submission policy before upload. Do not add Word or external-corpus claims: Word produced no accepted PDF and the external corpus count is zero.
