# V4 Output Provenance Audit

LibreOffice has 65 atomic + 10 realistic validated outputs. Google Docs has 65 atomic + 10 realistic outputs from the authenticated visible route:

`Frozen DOCX -> Google Docs import -> File -> Download -> PDF Document (.pdf) -> Chrome download capture`

All 75 Google outputs passed source-hash, non-zero, `%PDF`, parseability, tagged-structure, producer, plausible-page-count, post-baseline-timestamp, and distinct-from-LibreOffice-hash checks. The observed producer was `Skia/PDF m156 Google Docs Renderer` for all 75. No print-to-PDF, screenshot, manual repair, V3 PDF reuse, or unrelated upload was used. Exact upload timestamps were not separately captured; output filesystem timestamps are retained as conversion timestamps.

Machine-readable gate: `experiments/v4/conversions/V4_CONVERSION_RECOVERY_AUDIT.json`.
