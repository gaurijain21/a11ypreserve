# DECISION: RETRY PILOT

## 1. Executive decision

Retry the two-engine comparison in an interactive Windows environment where Microsoft Word can launch. The retry succeeded for all four LibreOffice conversions and produced the first real empirical A11yPreserve signal. Word remains blocked by Windows session activation, so the required cross-converter comparison is incomplete.

## 2. Input integrity

All four frozen DOCX files matched the existing manifest before conversion. No fixture or frozen manifest was modified.

| Fixture | Size | SHA-256 | Result |
|---|---:|---|---|
| F01_HEADINGS.docx | 37,029 bytes | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | PASS |
| F02_ALT_TEXT.docx | 41,331 bytes | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | PASS |
| F03_LISTS.docx | 37,064 bytes | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | PASS |
| F04_TABLE.docx | 37,043 bytes | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | PASS |

Evidence: [pilot2/FROZEN_INPUT_VERIFICATION.md](pilot2/FROZEN_INPUT_VERIFICATION.md).

## 3. Conversion engines

Microsoft Word 16.0.20326.20158 was present at `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`. COM activation, legacy Windows PowerShell COM activation, and direct native launch all failed before opening a fixture with `0x80070520` (“A specified logon session does not exist”). No print-to-PDF substitute was used.

LibreOffice 26.2.6.3 was installed from the verified official MSI into `pilot2/libreoffice_runtime`. The retry used `soffice.com` headless conversion with `writer_pdf_Export`, `UseTaggedPDF=true`, `PDFUACompliance=true`, and `SelectPdfVersion=1`.

## 4. Successful conversions

Word: **0/4**.

LibreOffice: **4/4**.

Total real, parseable PDFs: **4/8**.

All four LibreOffice outputs are one-page, non-zero, parseable PDFs with non-empty text and `/StructTreeRoot` present. Full hashes and metadata are in [pilot2/reports/output_validation.json](pilot2/reports/output_validation.json) and [pilot2/AUTOMATION_LOG.md](pilot2/AUTOMATION_LOG.md).

## 5. Failed conversions

- Microsoft Word could not activate in this Windows session; the failure occurred before any document opened.
- No Word PDF output or Word semantic result is claimed.
- PAC was not usable because its configured executable was missing; veraPDF, qpdf, and mutool were unavailable.

The Word failure is an infrastructure result, not accessibility loss.

## 6. Semantic results

| Fixture | Feature | Word→PDF | LibreOffice→PDF | Evidence quality |
|---|---|---|---|---|
| F01_HEADINGS | heading hierarchy | INVALID_CONVERSION | PRESERVED | HIGH |
| F02_ALT_TEXT | image alternative text | INVALID_CONVERSION | DEGRADED | HIGH |
| F03_LISTS | native list/nesting structure | INVALID_CONVERSION | PRESERVED | HIGH |
| F04_TABLE | table/header structure | INVALID_CONVERSION | PRESERVED | HIGH |

The LibreOffice results are based on source OOXML extraction plus independent PDF object-structure inspection and page-text extraction. Raw records are in [pilot2/reports/semantic_diff_results.json](pilot2/reports/semantic_diff_results.json).

## 7. Strongest confirmed preservation

F01 preserves four heading roles in order: `/H1`, `/H2`, `/H3`, `/H2`; the corresponding source heading text appears in the extracted PDF page text. F03 preserves seven list items with unordered/ordered roles and the source nesting depths. F04 preserves a `/Table` with 12 cell roles, including three `/TH` header cells, and all source cell values appear in the PDF text.

## 8. Strongest confirmed loss/degradation

F02 is a concrete mutation/degradation: the source author-written alt text is `Bar chart showing enrollment increasing from 120 students in 2024 to 180 students in 2026.`, while the PDF `/Figure` `/Alt` is `Enrollment chart - Bar chart showing enrollment increasing from 120 students in 2024 to 180 students in 2026.` The figure and meaningful alt text survive, but the exact source value is not preserved.

## 9. Cross-converter differences

No Word output exists, so no Word-versus-LibreOffice difference is claimed. The retry establishes a real LibreOffice destination signal only.

## 10. Comparator validity

Yes, with a narrow measurement correction. The existing `a11ydiff` logic distinguished `PRESERVED`, `DEGRADED`, `LOST`, and `MIS_MAPPED` in synthetic tests. The PDF adapter was corrected because raw marked-content strings were font-encoded and did not equal normal extracted page text. The corrected comparator now passes regression checks for all four real LibreOffice PDFs without changing frozen source truth.

## 11. Measurement failures

- Word conversion was blocked before destination creation; its four records remain `INVALID_CONVERSION`, not semantic loss.
- PDF structure elements did not expose decoded text through the initial marked-content byte reader. The parser now retains structure roles and independently records page text; evidence paths and the correction are documented in the automation log.
- The current parser does not claim exact per-cell text association from PDF marked-content bytes; F04 is classified from table/cell/header roles plus independent presence of all source cell values in page text.
- No secondary PAC/veraPDF result is reported.

## 12. Research signal

**PRESENT for the LibreOffice path; INCONCLUSIVE for the required two-engine comparison.** The source-grounded method produced a specific, inspectable mutation for alt text while distinguishing it from preserved headings, list structure, and table/header structure. This is evidence that the methodology works in practice for at least one real conversion engine.

## 13. What this pilot DOES prove

- The frozen source fixtures and source ASIR remain valid.
- A real DOCX→PDF engine can produce tagged, parseable output that is independently inspectable.
- Source-grounded semantic comparison can distinguish preservation from a specific alt-text mutation.
- A missing Word conversion can remain separate from destination accessibility outcomes.
- The comparator can be narrowly extended to handle PDF structure plus independently decoded page text.

## 14. What this pilot DOES NOT prove

- It does not establish Microsoft Word preservation behavior.
- It does not establish a Word-versus-LibreOffice comparison.
- It does not prove general PDF/UA conformance; tagged structure and PDF/UA export settings are evidence, not a full validator result.
- It does not generalize from four fixtures to all accessibility semantics or converters.

## 15. Full-paper implications

The result supports continued research rather than a pivot or kill decision. Scaling to more fixtures, more PDF engines, and an independent PDF/UA validator is plausibly publishable, but the next gate is completing the Word path and validating the table/list extraction against an independent structural tool.

## 16. Next experiment

Run the same frozen Pilot 2 tree on an interactive Windows desktop/session where Word COM or native export can launch, then produce the four Word PDFs with `ExportAsFixedFormat`. Reuse the current source ASIR and corrected destination adapter. Do not regenerate fixtures. After that, add one independent PDF structure validator and, if useful, the optional DOCX→HTML slice.

## 17. Final decision

**RETRY PILOT**

