# A11yPreserve V4 Anonymous Artifact Package

## Status

This directory is the prepared anonymous V4 manuscript/artifact entry point. It contains the manuscript source and a machine-readable summary of the frozen results. A compiled PDF is intentionally absent: the built-in compiler and the installed MiKTeX engine both failed to produce one during final hardening.

## Contents

- `main.tex` — anonymous manuscript source copied from the reviewed source.
- `v4_summary.json` — frozen counts, provenance commit, and build status.

## Reproduction entry point

From the repository root, run:

```text
python reproduce_v4.py --full-analysis
```

That command verifies the frozen source manifest, completed LO/Google conversion manifests, calibration counts, analysis summaries, and cross-pipeline summary without requiring Google authentication.

## Submission note

Compile `main.tex` in a functioning TeX environment, visually inspect the resulting PDF, and remove any venue-inappropriate supplementary provenance before upload. Do not add Word or external-corpus claims: Word produced no accepted PDF and the external corpus count is zero.
