# A11yPreserve V5 research readiness

## 1. Final verdict

**GO — READY FOR FINAL HUMAN SUBMISSION**. The central claim is supported by
the frozen V4 controlled evidence and the completed V5 oracle hardening. The
paper states its evidence boundary precisely; no avoidable scientific,
consistency, build, anonymity, or packaging blocker remains.

## 2. What changed from V4

- Preserved V4 fixtures, contracts, labels, outputs, and chronology as historical provenance.
- Added machine-derived holdout audit: 130 primary cases = 52 holdout + 78 non-holdout; holdout is fixture-level.
- Resolved LibreOffice setting interpretation: V4 `SelectPdfVersion=1` is PDF/A-1b; V5 condition B tests default PDF 1.7 with tagging/PDF-UA flags.
- Added explicit environment/provenance table and cross-format equivalence contract.
- Added destination-side mutation testing, independent technical oracle validation, and calibration ground-truth audit.
- Added explicit reading-order, external-document, Google-boundary, temporal-repeatability, attribute-scope, prior-art, and adversarial-review reports.
- Revised manuscript copy: `submission/ICST2027_V5/main.tex`.

## 3. Final experimental design

- Pipelines: LibreOffice and Google Docs primary; Microsoft Word supplementary/post-freeze.
- Corpus: 65 atomic DOCX fixtures, 13 families, five variants per family; 10 project-created realistic documents per primary pipeline.
- Primary cases: 130; supplementary Word atomic observations: 65; archived atomic observations: 195.
- Validation arms: 78 calibration controls, 39 source mutations, 13 destination mutation attempts, 26 independent technical validation rows, repeatability, and realistic integrated documents.

## 4. Final primary results

Frozen V4 counts are machine-derived and unchanged:

| Classification | LibreOffice | Google Docs | Word supplementary |
|---|---:|---:|---:|
| VERIFIED_PRESERVED | 38 | 11 | 16 |
| OBSERVED_PARTIAL | 11 | 32 | 26 |
| ALTERED | 9 | 11 | 16 |
| CONFIRMED_LOST | 1 | 6 | 2 |
| UNRESOLVED_EQUIVALENCE | 1 | 5 | 0 |
| MEASUREMENT_ERROR | 5 | 0 | 5 |

V5 condition B completed with 65/65 valid outputs, zero classification changes,
and the same six-category counts as frozen V4. All 65 outputs were tagged and
the raw PDF/A marker totals were zero. This is classified as **A. NO MATERIAL
EFFECT** for the semantic classifier; it does not imply byte identity or full
PDF/UA conformance.

## 5. Oracle validation

- Source mutation: 39/39 detected.
- Destination mutation: 12 valid mutants, 12 detected, 0 surviving; 1 unsupported attempt retained.
- Calibration: 60 correct, 0 false positives, 5 conservative false negatives, 13 correct abstentions.
- Independent validation: 26 rows, 8 agreements and 18 disagreements with the original classification; the second path is intentionally lightweight and does not claim full contract equivalence.
- Holdout: 52 aggregate fixture–pipeline cases; 78 aggregate non-holdout cases.

## 6. External validity

The realistic arm is project-created and remains separate from the atomic
denominator. A natural-document arm and time-separated Google sessions were
not fabricated; both remain explicit limitations. The reading-order attribute
is deferred because a defensible source/destination oracle was not established.

## 7. Prior-art position

A11yPreserve does not claim the first accessibility-conversion benchmark or
first source-aware accessibility study. Its defensible position is a testing
methodology that combines verified DOCX source contracts, named real
DOCX-to-PDF pipelines, feature-specific cross-format equivalence, uncertainty-
aware abstention, holdout accounting, mutation testing, and provenance.

## 8. Remaining limitations

- purposive controlled corpus and limited converter/version scope;
- cloud-service drift and no intermediate Google import representation;
- incomplete generality of destination mutation models;
- no external expert adjudication or disabled-user usability study;
- footnote association and some complex-equivalence cases remain uncertain;
- no rights-cleared natural DOCX corpus in this run.

## 9. Reviewer kill attempts

The strongest remaining rejection arguments are limited natural-document and
temporal cloud evidence, incomplete generality of mutations, and disagreement
from the lightweight independent implementation. These are mitigated or
explicitly open, but they do not invalidate the source-grounded research
question.

## 10. Submission recommendation

Submit the V5 manuscript and anonymous upload bundle as an ICST Research
Papers submission. The V5 profile-B manifest, analysis, consistency audit,
regression tests, three-pass MiKTeX build, nine-page render inspection, font
embedding check, and sanitized bundle verification all pass. The paper should
retain its precise evidence boundary; that is scientific accuracy, not an
unfinished limitation repair.

## 10a. Final package verification

- Manuscript PDF: `submission/ICST2027_V5/main.pdf`; 9 pages; SHA-256
  `96D56804D6E84447AB66E2268BDA86BCEE62BAC15199BA5C77F038386EB7BD5F`.
- Anonymous upload bundle: `submission/ICST2027_V5/ICST2027_V5_anonymous_upload.zip`.
- Replication package: `submission/ICST2027_V5/upload_v5/replication_package.zip`;
  812 files; cache/profile binaries excluded. Exact hashes are recorded in
  `upload_v5/BUNDLE_MANIFEST.json`.
- Visual QA: all nine rendered pages inspected; no clipping, overlap, broken
  table, unreadable reference, or page-size defect found.
- Final human-controlled steps remain HotCRP author/COI metadata, originality
  and simultaneous-submission declarations, artifact license/access settings,
  portal-generated PDF inspection, and author approval.

## 11. Reproducibility

- V4 provenance commit: `e881a7a3d2cd491bea1ecc7c422e6e4e3fdd8ec3`.
- V4 evidence: `experiments/v4/`, `submission/ICST2027_V4/`.
- V5 evidence: `experiments/v5/`, `contracts/v5/`, `reports/V5_*.md`.
- Main commands: `python scripts/audit_v5_holdout_accounting.py`,
  `python scripts/audit_v5_calibration.py`,
  `python experiments/v5/destination_mutation_testing.py`,
  `python experiments/v5/independent_oracle_validation.py`,
  `python experiments/v5/run_libreoffice_profile_b.py`,
  `python experiments/v5/analyze_libreoffice_profile_b.py`,
  `python scripts/audit_v5_final_consistency.py`, and
  `python tests/test_v5_hardening.py`.
- All new manifests retain source/output hashes and condition settings; no
  credentials or browser state are distributed.
