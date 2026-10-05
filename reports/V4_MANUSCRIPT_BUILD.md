# V4 Manuscript Build

- Source: `submission/ICST2027_V4/main.tex`
- Manuscript source status: present and derived from actual frozen V4 results.
- Built-in Codex LaTeX compiler: attempted; it reported `Unable to find standard directories for platform`.
- Local MiKTeX `pdflatex` 25.12.0.0: attempted first in the restricted workspace, then with the required per-user initialization permission. It reached package loading but produced no PDF or non-empty log and remained stalled; the process was terminated after bounded waits.
- A second local attempt used `--enable-installer=no`; it reached `hyperref` package loading and again stalled without producing a PDF. No package or manuscript source was changed by the attempt.
- No PDF was fabricated, copied from V3, or included in the artifact package. The source remains available for compilation in a functioning TeX environment.
