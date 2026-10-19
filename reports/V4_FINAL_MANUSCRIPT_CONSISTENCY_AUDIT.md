# V4 final manuscript consistency and visual audit

Audit date: 2026-10-05. No new primary experiment was run; this audit integrates the already completed supplementary Word arm.

## Machine checks

`python check_v4_manuscript_consistency.py` returned `PASS` after checking the expanded source and all section files against the canonical LibreOffice, Google Docs, and Word analysis JSON files.

Checked explicitly:

- 13 feature families, five variants per family, 65 atomic DOCX fixtures, 130 primary fixture--pipeline cases, and 26 holdout cases.
- LibreOffice: 38 preserved, 11 partial, 9 altered, 1 lost, 1 unresolved, and 5 measurement-error cases.
- Google Docs: 11 preserved, 32 partial, 11 altered, 6 lost, 5 unresolved, and zero measurement-error cases.
- Supplementary Word: 16 preserved, 26 partial, 16 altered, 2 lost, 0 unresolved, and 5 measurement-error cases; 65 total and excluded from the 130-case primary denominator.
- Complete archived atomic observation count: 130 primary plus 65 supplementary Word = 195.
- 78 calibration controls, 60 correct decisions, zero false positives, five conservative false negatives, 13 correct abstentions, and zero unsupported confident classifications.
- Source-oracle mutation testing: 39/39 detected.
- Realistic arm: 10 project-created documents, 78 contracts per pipeline, 20 primary PDFs plus 10 supplementary Word PDFs.
- Repeatability: six selected variants, three runs each, stable classification and normalized semantic evidence 6/6 for all three pipelines; LibreOffice byte identity 0/6, Google byte identity 6/6, and Word byte identity 0/6.
- Holdout: LibreOffice 14/5/4/1/2 and Google 4/13/5/2/2 in the reported preserved/partial/altered/lost/unresolved-or-error order. Word holdout is reported separately as a supplementary result.

The checker also rejects stale V3/V1 count phrases, obsolete Word no-go language, any claim that 195 cases are primary, and verifies the canonical Word feature matrix.

## Build checks

- Build route: `submission/ICST2027_V4/build.ps1`, MiKTeX `pdfTeX 3.141592653-2.6-1.40.28`, IEEEtran conference class.
- Three `pdflatex` passes with BibTeX between the first and second pass.
- Build exit status: PASS.
- Final PDF: 8 pages, letter size (612 x 792 points), PDF 1.5, unencrypted.
- Final build log: no unresolved citations/references. MiKTeX reported table overfull-box warnings, but visual inspection found no clipped content or page-boundary overflow; ordinary underfull-box warnings remain in narrow IEEE columns.
- No custom geometry, compressed spacing, or author/institution metadata was added.
- The repository read-only verifier `python reproduce_v4.py --full-analysis` passed for the frozen primary evidence; the manuscript consistency checker additionally verifies the supplementary Word totals and feature matrix.

## Visual checks

All eight rendered pages were inspected. The initial review found overlapping classification labels in the Method section; the labels were changed to a normal bullet list and rerendered. The final review found no overlapping text, clipped tables, malformed arrows, unreadable central tables, or broken reference layout. The final PDF contains the anonymous AI disclosure and references.

The full-paper expansion changes presentation and explanatory coverage only. It does not change contracts, fixture membership, holdout membership, classifications, analysis code, or frozen results.
