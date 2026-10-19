# V4 Google Conversion Run Log

- Route used for the primary corpus: authenticated Chrome session, Google Docs visible UI import, then `File -> Download -> PDF Document (.pdf)`.
- Pilot: F01_A imported as `F01_A.docx`, exported through the visible PDF download action, and validated before batching.
- Atomic batch result: 65/65 successful outputs; no fixture was dropped or source-edited.
- Realistic batch result: 10/10 successful outputs; these are project-created/integrated documents.
- Repeatability result: 18/18 successful outputs for the six frozen variants and three independent runs.
- Computer/browser use: yes; native Google file chooser was handled through the browser filechooser event and exact local DOCX paths.
- Authenticated session: usable; no credentials were requested or recorded.
- Recovery events: transient CDP/Playwright timing, file-chooser, and document-title readiness errors occurred on a small number of attempts. Dedicated retries with extended waits recovered every affected fixture. The initial filesystem watcher also encountered Windows download-file locks; outputs were then copied only after the browser download paths were complete.
- Unresolved Google conversions: 0.
- No print-to-PDF, screenshot, manual PDF repair, content edit, unrelated upload, or V3-output reuse occurred.

Machine-readable records: `experiments/v4/conversions/google/manifest.json` and `experiments/v4/conversions/google/repeatability/RUN_MANIFEST.json`.
