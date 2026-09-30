# ICST 2027 V3 final desk-rejection audit

## Status

No known scientific or anonymity defect is established, but the V3 package is **not cleared for submission** because no valid V3 PDF was produced. Page count, final PDF metadata, embedded-font checks, and visual inspection therefore remain unverified.

## Official ICST requirements checked

The current official [ICST 2027 Research Papers CFP](https://conf.researchr.org/track/icst-2027/icst-2027-research-papers) was checked on 2026-09-29. It states that full research papers must use the two-column IEEE conference format and must not exceed 10 pages including text, figures, tables, and appendices; up to two additional pages containing only references are permitted. It also requires double-blind reviewing and says associated replication material is expected to provide the information needed to replicate results. The CFP lists the submission deadline as 2 November 2026 (AoE) and identifies HotCRP as the submission system.

## Administrative checks

| Check | Current status | Evidence or remaining action |
|---|---|---|
| Research-paper track | PASS | The source is an IEEEtran conference-format full-paper candidate; no short-paper claim is made. |
| Page limit | UNVERIFIED | CFP limit is verified, but no V3 PDF exists, so the 10-page content limit and reference-only allowance cannot be measured. |
| IEEE template | PARTIAL | The source includes IEEEtran class/bibliography files and an anonymous author block; final rendering in a working trusted TeX environment remains required. |
| Double anonymity in source | PASS | `Anonymous for review`; no author, institution, repository, personal URL, or local path appears in the V3 source. |
| AI disclosure | PASS IN SOURCE | The anonymous acknowledgment names OpenAI ChatGPT and OpenAI Codex, identifies affected sections and uses, and preserves human responsibility. |
| Citation/bibliography source checks | PASS | Citation-key audit found no undefined citation keys in the V3 source; final compiler log is unavailable. |
| Replication package | PASS AS CANDIDATE | The V3 ZIP contains 299 entries; no private-runtime directory names were found; evidence, scripts, fixtures, outputs, and instructions are present. Human license and portal checks remain. |
| PDF validity, fonts, metadata | UNVERIFIED | No V3 PDF exists. Do not substitute the V2 PDF. |
| Visual layout | UNVERIFIED | No V3 pages can be rendered or inspected without a successful compile. |
| Concurrent submission/originality/authorship | HUMAN CHECK | These facts cannot be established from the workspace. |

## Compilation blocker

Exhausted local routes were:

1. Direct MiKTeX `pdflatex` and `--disable-installer`: fresh-install initialization fails with Windows `Access is denied` while creating/configuring `Software\\MiKTeX.org\\MiKTeX\\2.9\\Setup` and the default per-user MiKTeX directory.
2. Isolated workspace-local `MIKTEX_USERCONFIG`, `MIKTEX_USERDATA`, `MIKTEX_USERINSTALL`, and `initexmf --user-roots`: the same registry write fails.
3. Codex built-in LaTeX compiler: reports `Unable to find standard directories for platform`.
4. TeX Live, latexmk, Tectonic, XeLaTeX, LuaLaTeX, BibTeX outside MiKTeX, Docker, and Podman: no usable alternate installation was found. WSL is present, but distro enumeration is denied and no usable local TeX distribution was available through it.
5. Native Windows MiKTeX Console was opened and its private-mode setup notice was dismissed. A subsequent direct pdfTeX attempt still failed during per-user initialization with the same access-denied error; no update or package installation was performed.
6. A native TeXworks launch was attempted as a GUI compilation route, but the Windows-control approval timed out before a TeXworks window became available; no manuscript upload or compile action occurred through that route.

This is a package-verification blocker, not an experiment result. No stale V2 PDF was copied into the V3 directory.

## Desk-rejection conclusion

There is one known blocker before submission: V3 compilation and the resulting page/anonymity/visual checks. The minimum repair is to compile the unchanged V3 source in a trusted local IEEEtran environment, render every page, inspect the generated PDF and metadata, then rebuild or reverify the anonymous artifact archive. No new experiment is required.
