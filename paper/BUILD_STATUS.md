# Build Status

## Current build status

- Source: `paper/main.tex`
- Local compiler: MiKTeX pdfTeX 25.12.0.0
- Bibliography: BibTeX 0.99e (MiKTeX 25.12)
- Command: MiKTeX `pdflatex -interaction=nonstopmode -halt-on-error main.tex` in `paper`, with BibTeX and two final LaTeX passes after the initial pass.
- Output: `paper/main.pdf` is not present in the current checkout.
- Result: **UNVERIFIED**. A historical build record reported a 10-page PDF and hash, but that file is absent and cannot be rehashed here.
- The retained `paper/rendered_v3/` PNGs are historical QA material only; they are not treated as proof of a currently available PDF.

## Built-in editor compiler

The Codex built-in LaTeX compiler was attempted first and failed before source parsing with the environment diagnostic `Unable to find standard directories for platform`. The source was preserved and compiled with the locally installed MiKTeX toolchain instead. This fallback is recorded rather than presented as a successful built-in-editor compilation.

## Warnings

The historical source pass reported no undefined citation or cross-reference warnings and no overfull boxes, with routine MiKTeX and underfull-box warnings. The current environment cannot reproduce that build because MiKTeX fails during fresh-install initialization with an access-denied registry/configuration error. A trusted working TeX environment must compile and re-render the source before a PDF freeze record is created.
