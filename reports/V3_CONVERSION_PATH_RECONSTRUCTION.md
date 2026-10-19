# V3 Conversion Path Reconstruction

Reconstructed from the successful V3 scripts, manifests, conversion reports, repeatability records, and route audits before attempting V4 conversion recovery.

## LibreOffice

| Item | Reconstructed V3 path |
|---|---|
| Converter/interface | Bundled LibreOffice `soffice.com`, headless Writer conversion via `--convert-to pdf:writer_pdf_Export:<settings>` |
| Recorded executable | `pilot2/libreoffice_runtime/program/soffice.com` |
| Recorded version | LibreOffice 26.2.6.3, build `8221e31b3ac356a1623c672912a3d2b492f7e3d1` |
| Export settings | `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1` |
| Profile isolation | One temporary/user-isolated profile per fixture via `-env:UserInstallation=file:///...`; `--headless --invisible --nodefault --nologo --nolockcheck --norestore --nofirststartwizard` |
| Input path policy | Frozen DOCX copied or passed as the exact source; V3 staging was used in the full-core script and variant arm |
| Output path policy | Deterministic PDF output directory; generated `<source-stem>.pdf` renamed to the documented fixture output name |
| Environment | Windows; repository-bundled runtime; per-fixture profile directories |
| Evidence | `scripts/run_full_libreoffice.py`, `scripts/v3_run_libreoffice_variants.py`, `scripts/run_integrated_libreoffice.py`, `v3/variant_set_b/libreoffice/CONVERSION_REPORT.json` |
| Result | V3 Variant B: 13/13 parseable/tagged outputs. Integrated V3 documents were also converted. |

The V3 route is being reused for V4 without altering the frozen DOCX sources or export settings.

## Google Docs

| Item | Reconstructed V3 path |
|---|---|
| Converter/interface | Authenticated Google Docs import of the exact DOCX followed by Google PDF export |
| Core procedure | Google Docs/Drive Open file → Upload → Browse → select exact DOCX → wait for import/render → File → Download → PDF Document |
| Browser/authentication | Existing authenticated Chrome session; native Windows file chooser used for Browse |
| Output path policy | Capture downloaded PDF and place it at the deterministic fixture-specific output path; hash and parse after download |
| Core route | Visible Google Docs UI download route |
| Variant B route | After visible Download did not register for B01 despite retries, the authenticated in-session Google export backend route was used; no print-to-PDF, screenshot, or manual PDF repair |
| Backend/version | Google renderer/backend not observable or pinnable; Variant B observed producer was `Skia/PDF m156 Google Docs Renderer` |
| Repeatability | Core runs 1–3: 13 fixtures × 3; reports state 13/13 valid and byte-identical under the recorded workflow |
| Evidence | `scripts/v3_freeze_google_outputs.py`, `scripts/v3_finalize_repeatability.py`, `v3/variant_set_b/google/CONVERSION_REPORT.json`, `v3/google_repeatability/GOOGLE_REPEATABILITY_AUDIT.md`, `reports/GOOGLE_ROUTE_AUDIT.md` |
| Result | V3 core and Variant B Google outputs were genuinely produced and separately hashed/validated. |

V4 Google conversion will use one consistent route for the primary V4 corpus. If the current Chrome profile is not authenticated, upload will stop at the security boundary rather than silently substituting another converter.

## Microsoft Word

| Item | Reconstructed V3 path |
|---|---|
| Installed application | `C:\Program Files\Microsoft Office\Root\Office16\WINWORD.EXE` |
| Intended interface | Word native PDF export/Save As PDF with document-structure accessibility option where exposed |
| Attempted route | PowerShell COM, Python/pywin32 COM, 32/64-bit WSH, and direct application launch |
| Result | No pilot document opened/exported; activation failed before conversion with `0x80070520` (WSH also reported an access-denied settings error) |
| Evidence | `reports/WORD_PIPELINE_FEASIBILITY.md`, `docs/FINAL_LIMITATION_RESOLUTION_REPORT.md` |
| V3 output evidence | None; Word was correctly excluded from V3 denominators |

Word remains a required recovery attempt for V4 after securing the higher-probability LibreOffice and Google paths.

## Provenance boundary

These records describe V3 mechanisms only. No V3 PDF is used as a V4 output, copied into a V4 output directory, or relabeled as V4.
