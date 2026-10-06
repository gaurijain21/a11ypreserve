# V4 Microsoft Word desktop GUI recovery result

Date: 2026-10-05

This report supersedes the earlier bounded GUI-unavailable disposition in
`reports/V4_WORD_EXPORT_ROOT_CAUSE_AUDIT.md`. That earlier report remains
historical evidence of the COM and zero-byte failures; it is not the final
Word disposition.

## Result

Microsoft Word desktop native PDF export is **RECOVERED** through the normal
interactive GUI. Word is retained as a supplementary third-pipeline arm. The
prospectively frozen LibreOffice + Google Docs primary denominator remains 130
cases and is unchanged.

## Environment and activation

- Word executable: `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`
- Product/build: Microsoft 365 `O365ProPlusRetail`, x64,
  `16.0.20430.20092`
- Windows: `Microsoft Windows NT 10.0.26200.0`
- Word launched and opened documents in the ordinary interactive user session.
- File → Account showed no activation or account-repair warning. No account
  identity, email address, license key, or token was recorded.

## Native GUI route

The recovered route was:

`File → More options → Export → Create PDF/XPS Document → Create PDF/XPS`

The Publish dialog used PDF, Standard optimization, all pages, Document,
bookmarks/properties, and `Document structure tags for accessibility` enabled.
`Open file after publishing` was disabled because enabling it invoked an
unrelated Font Capture application error (`0xc06d007e`) after export; disabling
it produced the valid PDF normally. No print route, browser route, Acrobat
conversion, tag repair, or post-processing was used.

The GUI Save As → PDF route was also tested on the trivial diagnostic document
and produced the same valid Word PDF. The Export/Create PDF-XPS route was used
for the frozen corpus because it was the documented batch condition.

## Pilot validation

| Input | Output | Size | PDF | Producer | Structure tree |
|---|---|---:|---|---|---|
| trivial diagnostic DOCX | `C:\A11yWordTest\manual_saveas.pdf` | 116,185 bytes | parseable, `%PDF-1.7` | Microsoft Word for Microsoft 365 | present |
| trivial diagnostic DOCX | `C:\A11yWordTest\manual_export.pdf` | 116,185 bytes | parseable, `%PDF-1.7` | Microsoft Word for Microsoft 365 | present |
| frozen `F01_A.docx` | `C:\A11yWordTest\F01_A_word.pdf` | 186,335 bytes | parseable, `%PDF-1.7` | Microsoft Word for Microsoft 365 | present |

The copied F01_A source SHA-256 matched the frozen source manifest:
`62643e92f2a7e40ff87c94795c6ad4cda019af8870f0b2f16eebc625a3a40fc2`.

## Batch output

- Atomic Word PDFs: **65/65**.
- Project-created realistic-document PDFs: **10/10**.
- Total validated Word PDFs: **75**.
- All 75 records are parseable, nonzero, and have a PDF structure tree.
- Observed producer/creator metadata is Microsoft Word for Microsoft 365.
- Default filenames produced by some GUI publishes were normalized only by
  byte-preserving copy into the repository’s deterministic output names. PDF
  bytes were not edited.

Machine-readable provenance is in:
`experiments/v4/conversions/word/manifest.json`.

## Root-cause conclusion

The earlier `0x80070520` failure remains reproducible for external Word COM
activation and is therefore an automation-interface/session problem, not proof
that Word’s desktop PDF engine is unavailable. Direct interactive GUI export
works. The zero-byte outputs arose in the earlier automation/native fixed-format
path, while the recovered GUI route produced valid output. A separate
Font Capture error occurred only when Word attempted to open the exported PDF;
disabling that optional open-after-publishing behavior removed the error without
changing the PDF export route.

## Scientific disposition

- Word is supplementary, not part of the frozen primary denominator.
- No frozen methodology, source contract, fixture membership, holdout, source
  oracle, comparator, classification taxonomy, LibreOffice output, or Google
  output changed.
- No Word accessibility classifications or repeatability results are claimed
  by this recovery report. Those require the separately frozen supplementary
  analysis pass.
- The manuscript should not replace the 130-case primary result with 195 cases.
  If Word is integrated, it should be described as a post-freeze supplementary
  arm after an explicit value assessment.

## Related artifacts

- `experiments/v4/word_supplement/WORD_SUPPLEMENT_PROTOCOL.md`
- `experiments/v4/conversions/word/manifest.json`
- `experiments/v4/conversions/word/outputs/atomic/`
- `experiments/v4/conversions/word/outputs/realistic/`
- `reports/V4_WORD_RECOVERY_BASELINE.md`
- `reports/V4_WORD_EXPORT_ROOT_CAUSE_AUDIT.md` (historical COM/zero-byte audit)
