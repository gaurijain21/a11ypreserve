# Build Status

## Final build

- Source: `paper/main.tex`
- Local compiler: MiKTeX pdfTeX 25.12.0.0
- Bibliography: BibTeX 0.99e (MiKTeX 25.12)
- Command: MiKTeX `pdflatex -interaction=nonstopmode -halt-on-error main.tex` in `paper`, with BibTeX and two final LaTeX passes after the initial pass.
- Output: `paper/main.pdf`
- Result: **SUCCESS**, 10 pages, 233,158 bytes at final evidence-aware build after the two submission wording repairs.
- Final SHA-256: `BDD9FE6A31E17DA034117C66324389487E13B7F374A62F97F0BDF8B4B656EEF4`.

## Built-in editor compiler

The Codex built-in LaTeX compiler was attempted first and failed before source parsing with the environment diagnostic `Unable to find standard directories for platform`. The source was preserved and compiled with the locally installed MiKTeX toolchain instead. This fallback is recorded rather than presented as a successful built-in-editor compilation.

## Warnings

The final source pass has no undefined citation or cross-reference warnings and no overfull boxes. MiKTeX reports its routine update-check notice, and several narrow two-column paragraphs have underfull-box warnings, including one underfull vertical page break. These do not clip content or prevent PDF generation; all 10 rendered pages in `paper/rendered_v3/` were inspected for clipping, overlap, table overflow, unreadable content, and malformed references.
