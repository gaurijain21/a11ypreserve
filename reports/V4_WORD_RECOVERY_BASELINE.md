# V4 Microsoft Word recovery baseline

Baseline date: 2026-10-04. This is an additive diagnostic record; the frozen 130-case LibreOffice + Google V4 experiment is not changed.

## Repository state

- Git HEAD: `3913a9e8553fe52d89db7667c8e3046149f51c94`.
- V4 protocol freeze provenance remains `41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1`.
- Worktree already contains the final manuscript/package preparation changes from the preceding task; no Word diagnostic output is being added to the primary corpus.

## Windows and Office environment

- Windows version: `Microsoft Windows NT 10.0.26200.0`.
- Word executable: `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`.
- Office product: `O365ProPlusRetail`.
- Office platform: `x64`.
- Office/Word build reported by file and Click-to-Run registry: `16.0.20430.20092`.
- No `WINWORD.EXE` process was running at baseline.
- TEMP/TMP: `C:\Users\iamga\AppData\Local\Temp`; both existed at baseline. Personal path is recorded only as local diagnostic provenance, not as an upload artifact.
- Activation/license state: not classified by this diagnostic; the native Word File → Account page was not exposed through the available computer-use surface, and no account identity was recorded.

## Existing Word evidence

The repository contains prior COM, WSH, safe-mode, and GUI-attempt notes in `reports/WORD_PIPELINE_FEASIBILITY.md`, `reports/V4_WORD_FINAL_NO_GO.md`, `docs/WORD_FINAL_RESOLUTION_ATTEMPT.md`, and `scientific_strengthening/word_pipeline/word_com_probe.vbs`. These notes report earlier `0x80070520` failures and a later safe-mode `ExportAsFixedFormat` attempt that returned a zero-byte file. They do not establish the current root cause for the now-observed successful GUI launch/open state, so they are not treated as conclusive.

## Diagnostic sources

- Pilot fixture: `experiments/v4/fixtures/F01_A.docx` (development variant; not holdout).
- Pilot source SHA-256: `62643E92F2A7E40FF87C94795C6AD4CDA019AF8870F0B2F16EEBC625A3A40FC2`.
- A separate heading/paragraph-only DOCX will be created solely as a Word diagnostic document; it is not a V4 fixture and will not enter any analysis denominator.

## Safety boundary

No credentials, account email, license keys, tokens, Credential Manager entries, registry identity settings, Office repair, Trust Center settings, or security settings were changed. Existing V4 outputs remain untouched.
