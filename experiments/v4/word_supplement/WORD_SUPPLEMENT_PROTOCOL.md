# Microsoft Word Desktop Supplementary Pipeline Protocol

Protocol status: **FROZEN BEFORE WORD ACCESSIBILITY ANALYSIS**  
Frozen: 2026-10-05  
Primary V4 protocol: `experiments/v4/V4_PROTOCOL.md`  
Primary V4 protocol SHA-256: `B4A2F974B7E14CB6C5847EB8667BF3A7E9CDF5C38C60AFE9C47391F476648556`

## Scope and denominator

Microsoft Word was added after completion of the prospectively frozen LibreOffice + Google Docs V4 primary experiment. It is therefore a **supplementary third-pipeline arm** and does not alter the frozen 130-case primary denominator.

The supplementary corpus is:

- 65 frozen atomic V4 DOCX fixtures, five variants in each of the 13 frozen feature families;
- 10 existing project-created realistic/integrated DOCX documents;
- the six pre-specified repeatability fixtures, three independent conversions each, only after the atomic and realistic conversion pass.

No source document, source contract, holdout assignment, comparator, extractor, classification taxonomy, or primary result is changed by this arm.

## Word condition

- Application: Microsoft Word desktop.
- Installed executable: `<INSTALLED_APPLICATION>
- Product/build observed: Microsoft 365 `O365ProPlusRetail`, x64, `16.0.20430.20092`.
- Windows: `Microsoft Windows NT 10.0.26200.0`.
- Session: ordinary logged-in interactive user session; no elevated Word process is used for conversion.
- Route: Word GUI `File -> Export -> Create PDF/XPS Document -> Create PDF/XPS`.
- PDF type: `PDF (*.pdf)`.
- Optimization: `Standard (publishing online and printing)`.
- Page range: all document pages.
- Publish target: document, not markup.
- Non-printing information: bookmarks from headings and document properties retained using Word defaults.
- Accessibility option: `Document structure tags for accessibility` enabled/verified in the Word PDF Options dialog.
- Post-export behavior: `Open file after publishing` disabled; the PDF is not reopened by Word/another registered PDF handler.
- No print-to-PDF, browser route, Word for Web, Acrobat conversion, LibreOffice conversion, screenshot, tag repair, or post-export PDF editing.

The diagnostic pilot verified the same route on `<LOCAL_WORD_WORKSPACE>\F01_A.docx` and produced `<LOCAL_WORD_WORKSPACE>\F01_A_word.pdf` before any classification inspection.

## Source provenance

- Atomic source manifest: `experiments/v4/source_manifest.json`.
- Atomic source manifest SHA-256: `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7`.
- Realistic source manifest: `experiments/v4/realistic/REALISTIC_CORPUS_MANIFEST.json`.
- Realistic source manifest SHA-256: `E09C8EE8A5569B789E6BAC92DA8D5FF03CEBEBFA18DFF497FD9CDBA284985ED4`.
- Every conversion record must retain the source path and SHA-256 from the frozen manifests.
- Inputs are copied byte-for-byte to the short local diagnostic/conversion workspace when needed; source hashes must match before export.

## Output policy

- Temporary Word export workspace: `<LOCAL_WORD_WORKSPACE>\word_inputs\` (the local, non-OneDrive folder used by the GUI publish dialog).
- Repository artifact directory: `experiments/v4/conversions/word/`.
- Atomic output naming: `<fixture_id>__WORD_DESKTOP.pdf`.
- Realistic output naming: `<realistic_id>__WORD_DESKTOP.pdf`.
- Repeatability naming: `<fixture_id>__WORD_DESKTOP__run<1-3>.pdf`.
- Repository output copies are byte-preserving copies of PDFs created by Word at the local target path.
- Every record must include output SHA-256, byte size, timestamp, page count, observed producer/creator, PDF parse status, structure-tree status, route, and retry count.

## Failure and retry policy

Each fixture receives at most two additional deterministic GUI retries after an export failure. A retry must reopen the unchanged source and use the same route/options. A failure is retained in the manifest with its observed dialog/error and is never silently omitted. Source documents are never edited.

## Analysis freeze

After all output conversion records are complete, use the existing frozen extraction/comparator implementation without tuning:

- comparator: `experiments/v4/v4_comparator.py`;
- comparator SHA-256: `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4`;
- destination extractor: `scripts/extract_semantics.py`;
- destination extractor SHA-256: `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7`;
- frozen analysis driver: `experiments/v4/run_frozen_analysis.py`;
- analysis driver SHA-256: `08FF23F71DE46D1DB31AC459878B5165506EAC83311FD7510222AD0A51C9D13D`.

Word results will be reported separately as supplementary observations. They will not be merged into the frozen LibreOffice + Google primary denominator.
