# Full experiment execution plan

## Frozen input

Use `corpus/FROZEN_CORPUS_MANIFEST.json` as the only source-of-truth list.
Never regenerate or edit a frozen fixture. Every run records source path,
source SHA-256, manifest SHA-256, converter/version, settings, timestamp, and
output SHA-256.

## Converter matrix

| Engine | Route | Required status |
|---|---|---|
| LibreOffice | DOCX to tagged PDF using the established export configuration | primary Engine A |
| Google Docs | upload identical frozen DOCX, export/download PDF using the Pilot 3 workflow | primary Engine B |
| Microsoft Word | native `ExportAsFixedFormat` only, if environment becomes usable | optional Engine C; never a blocker |

Do not use Print to PDF, screenshots, or generated replacement PDFs. Output
names are deterministic, for example
`F06_INLINE_LANGUAGE__LIBREOFFICE.pdf`.

## Validation and evidence

1. Validate existence, non-zero size, parseability, page count, reopenability,
   source-content presence, and PDF structure objects.
2. Classify corrupt or incomplete files as `INVALID_CONVERSION`, never as an
   accessibility loss.
3. Extract raw PDF catalog metadata, `/Lang`, structure roles, marked content,
   `/Alt`, link annotations, table roles, and other feature-specific evidence.
4. Run `a11ydiff` with the source manifest/ASIR and destination extraction.
5. Store raw observations separately from two-axis interpretation.
6. Run PAC, Acrobat, or veraPDF when available as secondary evidence only.

## Analysis unit

The primary unit is fixture × feature × converter. Report fidelity and
destination accessibility independently. Do not produce an overall converter
ranking or a weighted accessibility score without a later justified design.

## Reproducibility

Record operating-system and application versions, cloud export dates for
Google Docs, locale, export settings, parser versions, and validator versions.
Keep source, destination, extraction, comparison, and validator artifacts in
separate evidence paths. A conclusion is publishable only when it can be
traced from source hash through destination hash and extraction evidence.

## Stop rule for this phase

This plan is ready for execution, but the 26-primary-output conversion matrix
(13 fixtures × LibreOffice and Google Docs) must not be launched until the
researcher explicitly authorizes the full experiment.
