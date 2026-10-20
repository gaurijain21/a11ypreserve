# A11yPreserve V6 final release manifest

Release preparation date: 2026-10-20

This manifest describes a local ICST 2027 submission candidate. It is not a
submission receipt, author approval, license decision, or authorization to
upload.

## Release artifacts

| Artifact | Path | SHA-256 / property |
|---|---|---|
| Canonical manuscript | `submission/ICST2027_V6/main.pdf` | `99880229FD6230D49890299AA77B02DA9B9C4E4ADC2E64B79CEE2A4C864BE321` |
| Manuscript format | canonical PDF | 10 pages; US letter; IEEE two-column |
| Anonymous upload candidate | `submission/ICST2027_V6/ICST2027_V6_anonymous_upload.zip` | `F2CDAC843FEDF9AC23EB788C84A4647D9955147216B604F61CD5E5F61650B9E5` |
| Archive payload | nested `replication_package.zip` | `EFF9552667FB4719A838E745E03D1767650867CA91A416347A2846E243E7F8EF` |
| Archive file count | nested replication package | 1,725 files |

## Technical validation

| Area | Status | Evidence |
|---|---|---|
| V5 historical reproduction | PASS | `python scripts/reproduce_v5.py` |
| Scientific accounting | PASS | `python scripts/verify_v6_scientific_accounting.py` |
| Manuscript consistency | PASS | `python scripts/audit_v6_manuscript_consistency.py` |
| Genuine controls | PASS: 65/65; 0 disagreements; 0 extraction failures; 0 evidence differences | `experiments/v6/V6_CONTROL_RERUN.json` and case traces |
| Mutation audit | PASS: historical 65 attempts; 59 valid; 46 coarse detections; 59 evidence-drift alerts; 10 historical meaningful survivors; 6 unsupported. Independent raw-object audit: 59/59 direct contract faults, 13 coarse-classification survivors. | `experiments/v6/`; `experiments/v8/V8_MUTATION_GROUND_TRUTH.json`; `reports/v8/MUTATION_GROUND_TRUTH_AUDIT.md` |
| Baselines/ablations | PASS: executable; no independent primary labels claimed | `experiments/v6/V6_BASELINE_ABLATION.json` |
| Regression tests | PASS | `python tests/test_v6_scientific_hardening.py` |
| Package manifest and bundle verifier | PASS: 1,725 packaged files, including additive adversarial evidence, V8 ground-truth traces, and fresh rerun traces | `V6_PACKAGE_MANIFEST.json`; `V6_UPLOAD_BUNDLE_CHECK.json`; `experiments/v7/`; `experiments/v8/`; `reports/v8/` |
| Anonymity audit | PASS pending human archive/HotCRP inspection | `FINAL_ANONYMITY_AUDIT.md` |
| PDF visual QA | PASS | all ten rendered pages under `.pdf-qa-v8/` |
| Fresh source compilation | PASS under elevated MiKTeX access | `v8_final.log`; 10 pages and no unresolved citation/reference diagnostics after BibTeX and sequential pdfTeX passes |
| Anonymous archive refresh | PASS | `python scripts/verify_v6_upload_bundle.py`; refreshed with disposable external staging because the local staging directory is a reparse point |
| Repository safety and diff checks | PASS at audit time | `scripts/audit_repository_safety.py`; `git diff --check` |

## Provenance and commit

The canonical PDF is byte- and text-identical to the verified alternate-
jobname build `v8_final.pdf`; the updated build provenance is recorded
in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

Scientific implementation and package commits: `c7dbe3430cab9dafc757bce01cd0a865d1d0ac21`,
`9b0d980`, `506c2a3`, and local release commit `ed42484`.
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
- Push to remote: **NOT PERFORMED in this release cycle**.

## Known limitations

The primary corpus is controlled and purposive; the holdout is within-design,
not a natural independent corpus; Word is supplementary; Google is an
end-to-end cloud import/export condition; no stage-level causal localization,
PDF/UA conformance, rights-cleared natural corpus, external expert
adjudication, human usability study, or authenticated time-separated Google
repeatability experiment is claimed. The historical ten meaningful destination
mutants remain coarse-classification survivors under the frozen definition; the
stronger bounded raw-object audit identifies 13 direct contract faults not
coarse-detected. The additive evidence-drift alert flags all 59 valid applied
mutants. The additive association diagnostic detected 11/12 valid scorable
one-per-family attacks; the complex-table attack remained already
`OBSERVED_PARTIAL`, while a separate role-delta diagnostic surfaced 5/5 valid
cases. The blinded adjudication packet is pending human review.
