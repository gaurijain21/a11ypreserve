# V4 Manuscript Build

- Source: `submission/ICST2027_V4/main.tex`
- Output: `submission/ICST2027_V4/main.pdf`
- Manuscript source status: present and derived from actual frozen V4 results.
- Built-in Codex LaTeX compiler: still unavailable on this host; it reports `Unable to find standard directories for platform`.
- Local MiKTeX `pdflatex` 25.12.0.0: **PASS** with package installation disabled. The initial package-cache load required roughly two minutes; subsequent builds completed in about three seconds. Earlier attempts mistook the slow cold load for a stall.
- Cross-references resolved after the second pass. The final PDF is 3 pages, parseable, unencrypted, letter-sized, and produced by `MiKTeX pdfTeX-1.40.28`.
- Visual QA rendered all three pages at 150 DPI. No clipping, overlap, broken tables, unreadable glyphs, or unresolved references were observed.
- A literal `->` rendering defect and visible hyperlink borders found during QA were corrected as presentation-only LaTeX fixes. No scientific text, count, result, contract, or methodology changed.
