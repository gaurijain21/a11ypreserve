# A11yPreserve V6 final release manifest

Release preparation date: 2026-10-19

This manifest describes a local ICST 2027 submission candidate. It is not a
submission receipt, author approval, license decision, or authorization to
upload.

## Release artifacts

| Artifact | Path | SHA-256 / property |
|---|---|---|
| Canonical manuscript | `submission/ICST2027_V6/main.pdf` | `2FD2D4C738D1B5C175B02EAC7A589F664DBFDD73528A7E5A7147F666D89D26A3` |
| Manuscript format | canonical PDF | 9 pages; US letter; IEEE two-column |
| Anonymous upload candidate | `submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip` | `37C537CBA6BBF4D4AAA3B6ECF6DABF761CC3EA189CDD703845866F96077B1F34` |
| Archive payload | nested `replication_package.zip` | `1B2B12669F36F37952711229F3F95DE62CDBB7ED98E20509557CC520B1FB331A` |
| Archive file count | nested replication package | 1,136 files |

## Technical validation

| Area | Status | Evidence |
|---|---|---|
| V5 historical reproduction | PASS | `python scripts/reproduce_v5.py` |
| Scientific accounting | PASS | `python scripts/verify_v6_scientific_accounting.py` |
| Manuscript consistency | PASS | `python scripts/audit_v6_manuscript_consistency.py` |
| Genuine controls | PASS: 65/65; 0 disagreements; 0 extraction failures; 0 evidence differences | `experiments/v6/V6_CONTROL_RERUN.json` and case traces |
| Mutation audit | PASS: 65 attempts; 59 valid; 46 coarse detections; 59 evidence-drift alerts; 10 meaningful survivors; 6 unsupported | `experiments/v6/V6_MUTATION_SENSITIVITY.json`; `experiments/v6/V6_OBJECTION_MITIGATIONS.json` |
| Baselines/ablations | PASS: executable; no independent primary labels claimed | `experiments/v6/V6_BASELINE_ABLATION.json` |
| Regression tests | PASS | `python tests/test_v6_scientific_hardening.py` |
| Package manifest and bundle verifier | PASS: 1,136 packaged files | `V6_PACKAGE_MANIFEST.json`; `V6_UPLOAD_BUNDLE_CHECK.json` |
| Anonymity audit | PASS pending human archive/HotCRP inspection | `FINAL_ANONYMITY_AUDIT.md` |
| PDF visual QA | PASS | nine rendered pages under `.pdf-qa/direct-language/` |
| Fresh source compilation | PASS under elevated MiKTeX access | `v6_direct_language.log`; 9 pages and no unresolved citation/reference diagnostics after BibTeX and three pdfTeX passes |
| Anonymous archive refresh | PASS | `python scripts/verify_v6_upload_bundle.py`; refreshed with disposable external staging because the local staging directory is a reparse point |
| Repository safety and diff checks | PASS at audit time | `scripts/audit_repository_safety.py`; `git diff --check` |

## Provenance and commit

The canonical PDF is byte- and text-identical to the verified alternate-
jobname build `v6_direct_language.pdf`; the updated build provenance is recorded
in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

Scientific implementation commit: `0cd03b2ea1bc6ecb716469fd4de9f9d3cb6c0ad5`.
Final bundle/provenance commit: pending the archive-refresh commit below.
The refreshed bundle was generated from the validated source state using
disposable external staging; its outer ZIP and nested package hashes above were
independently verified.
No remote push has been authorized or performed, and this is not a submission
receipt.

## Scientific and compliance status

- Scientific release: **GO WITH LIMITATIONS**.
- ICST technical candidate: **READY FOR AUTHOR SIGN-OFF**.
- Author identity, authorship order, conflicts, originality, licensing, rights,
  AI-disclosure approval, and HotCRP metadata: **REQUIRES AUTHOR CONFIRMATION**.
- Submission/upload: **NOT PERFORMED**.
- Push to remote: **PENDING EXPLICIT GITHUB UPDATE**.

## Known limitations

The primary corpus is controlled and purposive; the holdout is within-design,
not a natural independent corpus; Word is supplementary; Google is an
end-to-end cloud import/export condition; no stage-level causal localization,
PDF/UA conformance, rights-cleared natural corpus, external expert
adjudication, human usability study, or authenticated time-separated Google
repeatability experiment is claimed. Ten meaningful destination mutants remain
coarse-classification survivors, while the additive evidence-drift alert flags
all 59 valid applied mutants. The blinded adjudication packet is pending human
review.
