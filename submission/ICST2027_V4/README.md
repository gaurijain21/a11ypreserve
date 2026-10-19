# A11yPreserve V4 ICST 2027 submission

This directory contains the anonymous IEEE conference-format V4 manuscript built from the frozen V4 evidence. It reports 65 atomic fixtures and 130 prospectively frozen primary fixture--pipeline cases across LibreOffice and Google Docs, plus the separately frozen supplementary Microsoft Word desktop arm with 65 additional atomic observations. It also reports the separate 26-case holdout, calibration, repeatability, and project-created realistic/integrated evidence. The complete archive contains 195 atomic observations, but Word is not part of the primary denominator and the realistic corpus is not called real-world.

## Verified build

From this directory, run:

```powershell
./build.ps1
```

The script runs three `pdflatex` passes with `--enable-installer=no` and a `bibtex` pass between the first and second passes. The first cold MiKTeX package load can take roughly two minutes; subsequent builds are normally much faster. The deterministic output is `main.pdf`.

## Evidence and consistency checks

From the repository root:

```powershell
python check_v4_manuscript_consistency.py
python reproduce_v4.py --full-analysis
```

The first command checks primary and supplementary manuscript numbers and feature-matrix values against the canonical frozen analysis JSON. The second verifies source hashes, conversion manifests, calibration, and frozen analysis summaries without requiring Google authentication. Word PDFs and analyses are under experiments/v4/conversions/word/; Word classifications can be reproduced from the PDFs without running Word.

## Submission package

`final/` contains the anonymous manuscript PDF/source and a machine-readable summary. The exact upload bundle is prepared under `upload/` after final compilation and sanitization. The repository's V3 submission remains historical and is not overwritten.
