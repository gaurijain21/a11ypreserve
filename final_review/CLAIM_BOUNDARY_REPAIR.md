# Claim-Boundary Repair

## Claims retained

- The study measures machine-verifiable accessibility information in controlled DOCX sources and tested destination PDFs.
- The protocol is source accessibility -> conversion pipeline -> destination structure -> differential comparison.
- The benchmark contains 13 controlled atomic fixtures and 26 genuine outputs from two named pipelines.
- Counts and feature-level matrices are primary; percentages are descriptive summaries over 25 determinate cases.
- The two confirmed LOST cases are F06/Google Docs inline language and F11/Google Docs footnote association.
- F11/LibreOffice remains MEASUREMENT_ERROR.
- Results are feature-specific observations under recorded conditions.

## Claims explicitly prohibited

The repaired paper does not claim that:

- document conversion generally destroys accessibility;
- Google Docs is generally worse or LibreOffice generally better;
- findings generalize to all DOCX documents or software versions;
- altered information necessarily causes user harm;
- PDF export alone caused every observed change;
- a11ydiff measures complete accessibility;
- a destination-only validator proves source-semantic preservation;
- validators are defective because they miss preservation changes;
- the study measures task completion, screen-reader usability, perceived accessibility, or severity for disabled users;
- the work is the first or unique study of accessible conversion or preservation.

## Reproducibility boundary

LibreOffice is locally pinned by executable/version/settings. Google Docs is an authenticated, browser-mediated cloud pipeline: the backend version cannot be fully pinned, experiment date matters, reruns may change, and reproduction requires a Google account. The workflow, browser, operating system, observed producer, hashes, and validation records are retained. Microsoft Word is excluded from the denominator.

## Source-oracle boundary

Source ground truth is established by manifest, raw OOXML inspection, and source extractor agreement. The source extractor is implementation-grounded rather than an independent oracle. No independent human expert or disabled-user validation is claimed.
