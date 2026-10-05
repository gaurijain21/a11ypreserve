# V4 TeX Build Attempt

## Attempts

1. Built-in Codex LaTeX compiler: failed before compilation with `Unable to find standard directories for platform`.
2. Local MiKTeX `pdflatex` 25.12.0.0 in the workspace: failed during fresh-install initialization because the restricted process could not create the default MiKTeX registry/user tree.
3. Local MiKTeX with elevated per-user initialization: reached package loading but produced no PDF or non-empty log and stalled. A bounded wait was followed by termination of the compiler process.
4. Local MiKTeX with `--enable-installer=no`: reached `hyperref` package loading but again stalled without a PDF. The process was terminated after a bounded wait.

No source repair was attempted based on a partial log, and no PDF was copied from another version. Compilation therefore remains unverified. The exact source to compile is `submission/ICST2027_V4/main.tex`.
