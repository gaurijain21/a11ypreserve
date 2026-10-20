# A11yPreserve V6 final release manifest

Release preparation date: 2026-10-20

This manifest describes a local ICST 2027 submission candidate. It is not a
submission receipt, author approval, license decision, or authorization to
upload.

## Release artifacts

| Artifact | Path | SHA-256 / property |
|---|---|---|
| Canonical manuscript | `submission/ICST2027_V6/main.pdf` | `020F15E7A2612DBABD4CB6322A7BB80DEEA7F02C27984A92057A26DB069322B0` |
| Manuscript format | canonical PDF | 10 pages; US letter; IEEE two-column |
| Anonymous upload candidate | `submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip` | `17F8FF04277F8F75863A594E697DA93FA15FDC6536CB6A5252F78869E1267BC6` |
| Archive payload | nested `replication_package.zip` | `931E4F9BC75DCD64B71F6FC421ABC84EEE76FA6705E10925907C974918F500C0` |
| Archive file count | nested replication package | 1,542 files |

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
| Package manifest and bundle verifier | PASS: 1,542 packaged files, including additive adversarial evidence and fresh rerun traces | `V6_PACKAGE_MANIFEST.json`; `V6_UPLOAD_BUNDLE_CHECK.json`; `experiments/v7/`; `reports/v7/` |
| Anonymity audit | PASS pending human archive/HotCRP inspection | `FINAL_ANONYMITY_AUDIT.md` |
| PDF visual QA | PASS | ten rendered pages under `.pdf-qa/v7-adversarial/` |
| Fresh source compilation | PASS under elevated MiKTeX access | `v7_adversarial.log`; 10 pages and no unresolved citation/reference diagnostics after BibTeX and three pdfTeX passes |
| Anonymous archive refresh | PASS | `python scripts/verify_v6_upload_bundle.py`; refreshed with disposable external staging because the local staging directory is a reparse point |
| Repository safety and diff checks | PASS at audit time | `scripts/audit_repository_safety.py`; `git diff --check` |

## Provenance and commit

The canonical PDF is byte- and text-identical to the verified alternate-
jobname build `v7_adversarial.pdf`; the updated build provenance is recorded
in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

Scientific implementation and package commit: `c7dbe3430cab9dafc757bce01cd0a865d1d0ac21`.
The refreshed bundle was generated from the validated source state using
disposable external staging; its outer ZIP and nested package hashes above were
independently verified.
The final manifest is a small follow-up to the release commit and records the
exact hashes produced from that committed source state. This is not a
conference submission receipt.

## Scientific and compliance status

- Scientific release: **GO WITH LIMITATIONS**.
- ICST technical candidate: **READY FOR AUTHOR SIGN-OFF**.
- Author identity, authorship order, conflicts, originality, licensing, rights,
  AI-disclosure approval, and HotCRP metadata: **REQUIRES AUTHOR CONFIRMATION**.
- Submission/upload: **NOT PERFORMED**.
- Push to remote: **PENDING authorized GitHub update**.

## Known limitations

The primary corpus is controlled and purposive; the holdout is within-design,
not a natural independent corpus; Word is supplementary; Google is an
end-to-end cloud import/export condition; no stage-level causal localization,
PDF/UA conformance, rights-cleared natural corpus, external expert
adjudication, human usability study, or authenticated time-separated Google
repeatability experiment is claimed. Ten meaningful destination mutants remain
coarse-classification survivors, while the additive evidence-drift alert flags
all 59 valid applied mutants. The additive association diagnostic detected
11/12 valid scorable one-per-family attacks; the complex-table attack remained
already `OBSERVED_PARTIAL`, while a separate role-delta diagnostic surfaced 5/5
valid cases. The blinded adjudication packet is pending human review.
