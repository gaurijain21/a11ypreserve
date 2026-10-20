# A11yPreserve V6 final release manifest

Release preparation date: 2026-10-19

This manifest describes a local ICST 2027 submission candidate. It is not a
submission receipt, author approval, license decision, or authorization to
upload.

## Release artifacts

| Artifact | Path | SHA-256 / property |
|---|---|---|
| Canonical manuscript | `submission/ICST2027_V6/main.pdf` | `A34A6D2B67C62A7D4331560843B0279533AF0B9D09D62A467CBE6885CC15BC80` |
| Manuscript format | canonical PDF | 9 pages; US letter; IEEE two-column |
| Anonymous upload candidate | `submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip` | `53B65C5B50402F054BA4776B5075E0CCC587D63B08C86A593260EC2A0AF49D0B` |
| Archive payload | nested `replication_package.zip` | recorded in `upload_v6/BUNDLE_MANIFEST.json` |
| Archive file count | nested replication package | 1,130 files |

## Technical validation

| Area | Status | Evidence |
|---|---|---|
| V5 historical reproduction | PASS | `python scripts/reproduce_v5.py` |
| V6 scientific accounting | PASS | `python scripts/verify_v6_scientific_accounting.py` |
| Manuscript consistency | PASS | `python scripts/audit_v6_manuscript_consistency.py` |
| Genuine controls | PASS: 65/65; 0 disagreements; 0 extraction failures; 0 evidence differences | `experiments/v6/V6_CONTROL_RERUN.json` and case traces |
| Mutation audit | PASS: 65 attempts; 59 valid; 46 detections; 10 meaningful survivors; 6 unsupported | `experiments/v6/V6_MUTATION_SENSITIVITY.json` |
| Baselines/ablations | PASS: executable; no independent primary labels claimed | `experiments/v6/V6_BASELINE_ABLATION.json` |
| Regression tests | PASS | `python tests/test_v6_scientific_hardening.py` |
| Package manifest and bundle verifier | PASS | `V6_PACKAGE_MANIFEST.json`; `V6_UPLOAD_BUNDLE_CHECK.json` |
| Anonymity audit | PASS pending human archive/HotCRP inspection | `FINAL_ANONYMITY_AUDIT.md` |
| PDF visual QA | PASS | nine rendered pages under `.pdf-qa/release-final/` |
| Fresh source compilation | PASS under elevated MiKTeX access | `v6_final_audit.log`; 9 pages and no unresolved citation/reference diagnostics after BibTeX and three pdfTeX passes |
| Repository safety and diff checks | PASS at audit time | `scripts/audit_repository_safety.py`; `git diff --check` |

## Provenance and commit

The canonical PDF is byte- and text-identical to the verified alternate-
jobname build recorded in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

Technical release commit: **to be recorded after the authorized local release
commit**. No remote push has been authorized or performed. The final Git commit
hash and clean-tree result must be copied here after commit finalization; this
manifest must not be treated as a submission receipt until that update is made.

## Scientific and compliance status

- Scientific release: **GO WITH LIMITATIONS**.
- ICST technical candidate: **READY FOR AUTHOR SIGN-OFF**.
- Author identity, authorship order, conflicts, originality, licensing, rights,
  AI-disclosure approval, and HotCRP metadata: **REQUIRES AUTHOR CONFIRMATION**.
- Submission/upload: **NOT PERFORMED**.
- Push to remote: **NOT PERFORMED**.

## Known limitations

The primary corpus is controlled and purposive; the holdout is within-design,
not a natural independent corpus; Word is supplementary; Google is an
end-to-end cloud import/export condition; no stage-level causal localization,
PDF/UA conformance, rights-cleared natural corpus, external expert
adjudication, human usability study, or authenticated time-separated Google
repeatability experiment is claimed. Ten meaningful destination mutants remain
survivors.
