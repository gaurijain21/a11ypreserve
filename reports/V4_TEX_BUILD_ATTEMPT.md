# V4 TeX Build Attempt

## Attempts

1. Built-in Codex LaTeX compiler: failed before compilation with `Unable to find standard directories for platform`.
2. Local MiKTeX `pdflatex` 25.12.0.0 in the workspace: failed during fresh-install initialization because the restricted process could not create the default MiKTeX registry/user tree.
3. Local MiKTeX with elevated per-user initialization: reached package loading but produced no PDF or non-empty log and stalled. A bounded wait was followed by termination of the compiler process.
4. Local MiKTeX with `--enable-installer=no`: reached `hyperref` package loading but again stalled without a PDF. The process was terminated after a bounded wait.

## Resolution

The local process was slow rather than deadlocked. A later attached run was allowed to continue through the cold package load and completed successfully with exit code 0. A second pass resolved all table references and outlines.

- Command: `powershell -ExecutionPolicy Bypass -File submission\\ICST2027_V4\\build.ps1`
- Output: `submission/ICST2027_V4/main.pdf`
- Pages: 8
- Producer: `MiKTeX pdfTeX-1.40.28`
- Parseability: PASS
- Visual page review: PASS
- No unresolved references: PASS. Table overfull-box warnings were reviewed visually; no clipped content or page-boundary overflow was present.
- Frozen scientific content changed: NO

The remaining built-in compiler error is host-tool specific and does not block the verified MiKTeX build route.
