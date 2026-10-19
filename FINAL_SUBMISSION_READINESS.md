# GO WITH MINOR LIMITATIONS

## Canonical experiment

- feature families: 13 selected families; F13 reading order deferred
- controlled fixtures: 26 (13 Core + 13 Variant B)
- converters: LibreOffice 26.2.6.3 and recorded Google Docs workflow
- primary cases: 52 fixture–pipeline rows
- classification counts: 18 preserved, 4 partial, 7 altered, 4 confirmed lost, 18 unresolved, 1 measurement error

## Additional evidence

- holdout: Variant C not completed; no holdout result claimed
- calibration: 27 diagnostic controls; 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, 7 other unresolved/indeterminate
- repeatability: 39 Google Core runs; 13/13 classifications stable and 13/13 byte-identical
- integrated/realistic corpus: 3 synthetic integrated documents, 42 observations; no natural corpus
- Word pipeline: not added; COM activation failed before export
- reading order: not added; no defensible automated oracle

## Consistency

- repository: PASS under `tools/audit_submission_consistency.py`
- manuscript: current V3 source/PDF reports the 52-row state; older 26-row documents are historical
- evidence: artifact self-check PASS for 52 rows; raw-OOXML oracle PASS 13/13
- documentation: canonical state, limitations, fault model, prior-art, route, Word, anonymity, and adversarial reports are present

## Novelty

A11yPreserve does not claim to be the first conversion or PDF-accessibility study. Its narrow distinction from Roig/Ribera, DocAccessible, DAISY, SciA11y, iTagPDF, and Kumar et al. is a controlled DOCX source whose selected accessibility semantics are separately verified, paired with feature-specific contracts and evidence-aware comparison of PDF outputs from named DOCX-to-PDF pipelines. The method abstains when alternate equivalence cannot be established.

## Remaining limitations

- two pipelines and an opaque/version-variable Google backend;
- purposive, small corpus with two instances per family;
- 18 unresolved primary rows and imperfect calibration;
- no Word arm, reading-order arm, Variant C holdout, natural external corpus, or disabled-user study;
- post-hoc strengthening of the initial Core taxonomy, disclosed rather than hidden.

## Submission blockers

None for the narrowed scientific claim. A final venue/template, licensing/provenance, and archive metadata check is still required before upload.

## Required human actions

1. Recheck venue rules and final author metadata in the submission copy.
2. Verify redistribution rights and choose the artifact license.
3. Re-run the anonymity scan on the final archive/PDF immediately before upload.
