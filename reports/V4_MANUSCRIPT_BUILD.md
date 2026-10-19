# V4 Manuscript Build

- Source: `submission/ICST2027_V4/main.tex`
- Output: `submission/ICST2027_V4/main.pdf`
- Manuscript source status: present and derived from actual frozen V4 results.
- Built-in Codex LaTeX compiler: still unavailable on this host; it reports `Unable to find standard directories for platform`.
- Local MiKTeX `pdflatex` 25.12.0.0: **PASS** with package installation disabled. The build script runs three `pdflatex` passes with BibTeX between the first and second pass.
- Cross-references and citations resolved. The final PDF is 8 pages, parseable, unencrypted, letter-sized, IEEEtran conference two-column format, and produced by `MiKTeX pdfTeX-1.40.28`.
- Visual QA rendered all eight pages at 120 DPI and inspected them. One classification-list overlap was found and repaired as a presentation-only change; the rerender is clean. MiKTeX emitted table overfull-box warnings, but no content was visibly clipped or outside the page boundary.
- The expanded paper, tables, references, and anonymous AI disclosure use existing verified evidence only. No scientific text, count, result, contract, fixture, holdout, or methodology changed.
