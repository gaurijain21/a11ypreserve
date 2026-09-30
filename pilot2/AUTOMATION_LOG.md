# Pilot 2 Automation Log

## Frozen-state verification

- Timestamp: 2026-09-28T01:04:47.083448Z.
- The four frozen DOCX hashes matched `pilot/manifests/hashes.json`.
- No fixture, manifest, or prior report was modified.
- Full evidence: `pilot2/FROZEN_INPUT_VERIFICATION.md` and `.json`.

## Microsoft Word

- Timestamp: 2026-09-28T01:07:21.4401419Z.
- Tool: Microsoft Word 16.0.20326.20158, `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`.
- Primary method: PowerShell `Word.Application` COM activation, then `Documents.Open` and `ExportAsFixedFormat`.
- Intended settings: PDF format 17; print optimization; all-document range; document content; document properties; KeepIRM; heading bookmarks; document structure tags; bitmap missing fonts; ISO 19005-1.
- Result: COM activation blocked before any fixture opened with `0x80070520: A specified logon session does not exist`.
- No output hash exists because no output was produced.
- A direct process-launch attempt with `/q /n` was repeated with both the workspace and `C:\Windows` as working directories; both failed with the same session error.
- The native Windows automation surface returned no controllable apps, so GUI export could not be performed.
- No print-to-PDF path was used.

## LibreOffice

- Timestamp: 2026-09-28 during engine discovery.
- Checked PATH, common 64-bit and 32-bit installation paths, AppX packages, uninstall registry, user-profile executable tree, and Start Menu entries.
- Result: no `soffice.exe` or `libreoffice.exe` was present; no CLI or GUI conversion was attempted.
- No output hash exists because no output was produced.

## Analysis automation

- Source ASIR was read from the prior frozen source-semantic artifacts.
- The existing deterministic PDF parser/comparator pipeline was run safely against the expected Pilot 2 output names.
- All eight missing expected outputs were recorded as `INVALID_CONVERSION` at the conversion layer, not as accessibility loss.
- Secondary validators were not run because no Pilot 2 PDF existed; PAC's registry entry pointed to a missing executable, and veraPDF was absent.

## Pilot 2 retry: real LibreOffice conversions

- Engine discovery timestamp: 2026-09-27T18:40:43-07:00 through 2026-09-27T19:05:19-07:00.
- Tool: LibreOffice 26.2.6.3 (`8221e31b3ac356a1623c672912a3d2b492f7e3d1`), installed from the verified official MSI `LibreOffice_26.2.6_Win_x86-64.msi` (MSI SHA-256 `f9877032fd908beb9c0ddf06df4af5c2e85f419c42e14876c4cce5aae5fb2660`).
- Executable: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot2\libreoffice_runtime\program\soffice.com`.
- Windows: `Microsoft Windows NT 10.0.26200.0`.
- Method: `soffice.com` headless conversion from byte-for-byte staged copies of the frozen DOCX inputs; staging was used only to avoid OneDrive first-run file locking. The source hash recorded below is the hash of the frozen fixture, and each staged copy was made with `Copy-Item` without modification.
- Exact settings: `--headless --invisible --nodefault --nologo --nolockcheck --norestore --nofirststartwizard --convert-to "pdf:writer_pdf_Export:UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1" --outdir pilot2\outputs\libreoffice_pdf <staged-source.docx>`.

| Timestamp | Source | Destination | Result | Source SHA-256 | Output SHA-256 | Size |
|---|---|---|---|---|---|---:|
| 2026-09-27T19:04:03.5080714-07:00 | `pilot/fixtures/F01_HEADINGS.docx` | `pilot2/outputs/libreoffice_pdf/F01_HEADINGS__LIBREOFFICE.pdf` | SUCCESS; parseable, 1 page, `/StructTreeRoot` present | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | `e9329b05d628fcea4c6745e8e0b8fb2eea548d9525e82e4a9d1f6b94634c1b74` | 67,693 |
| 2026-09-27T19:04:56.3325644-07:00 | `pilot/fixtures/F02_ALT_TEXT.docx` | `pilot2/outputs/libreoffice_pdf/F02_ALT_TEXT__LIBREOFFICE.pdf` | SUCCESS; parseable, 1 page, `/StructTreeRoot` present | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | `ffb98539b1b315c97a495f6039ca85fd27f5f5ff9d9406d8e6c75aec83ed8c7d` | 69,910 |
| 2026-09-27T19:05:08.8608047-07:00 | `pilot/fixtures/F03_LISTS.docx` | `pilot2/outputs/libreoffice_pdf/F03_LISTS__LIBREOFFICE.pdf` | SUCCESS; parseable, 1 page, `/StructTreeRoot` present | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | `6af505d11f532228fa38e9c0441b68ff9d9d54a5f0682b5526b5620ae894b27e` | 63,731 |
| 2026-09-27T19:05:19.2105404-07:00 | `pilot/fixtures/F04_TABLE.docx` | `pilot2/outputs/libreoffice_pdf/F04_TABLE__LIBREOFFICE.pdf` | SUCCESS; parseable, 1 page, `/StructTreeRoot` present | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | `6d2bcc38193eaa1f44b02212352273dd9484625c275c6070510e37bd021b5221` | 58,095 |

## Pilot 2 retry: Microsoft Word reattempt

- Timestamp: 2026-09-27T19:06:12-07:00.
- Tool: Microsoft Word 16.0.20326.20158, `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`.
- Methods attempted: Windows PowerShell 5.1 `Word.Application` COM activation; PowerShell 7 `Word.Application` COM activation; direct `WINWORD.EXE /q /n /w` launch.
- Native export settings for the COM route: `ExportAsFixedFormat` PDF format 17; all-document range; document content; document properties; heading bookmarks; document structure tags; bitmap missing fonts; ISO 19005-1.
- Result: all Word paths were blocked before a fixture opened with `0x80070520: A specified logon session does not exist. It may already have been terminated.`
- Result count: 0/4 real Word PDFs; no output hashes exist; no Word semantic result is claimed.
- Native Windows automation still exposed no controllable apps, so GUI export was unavailable. No print-to-PDF method was used.

## Retry analysis and measurement correction

- All four LibreOffice PDFs were parseable with pypdf, non-zero, one page, non-empty text, and a `/StructTreeRoot`.
- The initial PDF extractor pass falsely returned empty structure-element text because it read raw marked-content bytes without applying the PDF font decoding used by normal page text extraction. The narrow correction records page text separately and makes the comparator use structure roles plus independently extracted page text; it does not alter frozen source truth.
- Added regression coverage for the four real LibreOffice semantic comparisons and corrected the semantic-record test to validate eight unique fixture/converter pairs plus element-level records.
- Existing tests: PASS. Pilot 2 tests: PASS. New real-PDF regression checks: PASS.
- Secondary validator availability: Acrobat is installed, but PAC points to a missing executable; veraPDF, qpdf, and mutool were not available. Secondary validator results are therefore not claimed.
