# V4 External Corpus Report

## Decision

**No external documents were added to the V4 experiment.** The primary benchmark remains unchanged.

## Legitimate candidates identified

Public government and university sources expose candidate DOCX materials, including the Section 508 Word accessibility examples and baseline tests, and the University of Illinois Word accessibility exercise. These sources are suitable for future screening because they are publicly hosted and explicitly describe accessibility semantics.

## Why they were not included in this pass

The current authenticated Google upload authorization was explicitly scoped to the frozen V4 atomic corpus, the 10 project-created realistic documents, and the pre-specified repeatability subset. Uploading newly sourced external documents to Google Docs would exceed that authorization boundary without a fresh explicit approval. Local LibreOffice-only conversion would not provide the requested two-pipeline external arm.

No external file was therefore downloaded into the repository, uploaded, converted, or presented as real-world evidence. External document count remains **0**. The existing realistic corpus remains accurately labeled project-created realistic/integrated.

Potential future screening sources:

- Section 508 Word accessibility examples: `https://www.section508.gov/training/courses/microsoft-word-accessibility-designers/`
- Section 508 baseline tests: `https://www.section508.gov/create/documents/authoring-guides/`
- University of Illinois Word accessibility exercise: `https://doit.illinois.gov/initiatives/accessibility/guides/word/word-accessibility-exercise.html`
