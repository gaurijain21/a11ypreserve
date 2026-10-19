# GO WITH LIMITATIONS

V4 now has two complete prospectively frozen primary converter arms and a
separately frozen supplementary Microsoft Word desktop arm. The primary V4
experiment remains unchanged and can replace V3 as the primary submission
evidence.

## Experimental accounting

### Primary prospective experiment

- 65 frozen atomic DOCX fixtures.
- LibreOffice: 65 atomic cases.
- Google Docs: 65 atomic cases.
- Primary total: **130 fixture--pipeline cases**.

### Supplementary Word experiment

- Microsoft Word desktop native GUI export.
- Same 65 frozen atomic fixtures.
- Word total: **65 supplementary atomic observations**.
- Word was added after completion of the primary two-pipeline experiment.

### Complete archived atomic evidence

- 130 primary observations + 65 supplementary Word observations = **195 total archived atomic observations**.
- The archive must not describe all 195 as primary cases or describe the study as a three-pipeline prospective benchmark.

## Atomic results

| Classification | LibreOffice (Primary) | Google Docs (Primary) | Word (Supplementary) |
|---|---:|---:|---:|
| VERIFIED_PRESERVED | 38 | 11 | 16 |
| OBSERVED_PARTIAL | 11 | 32 | 26 |
| ALTERED | 9 | 11 | 16 |
| CONFIRMED_LOST | 1 | 6 | 2 |
| UNRESOLVED_EQUIVALENCE | 1 | 5 | 0 |
| MEASUREMENT_ERROR | 5 | 0 | 5 |

No overall converter score or global ranking is used.

## Holdout and diagnostics

- LibreOffice holdout: 14 preserved, 5 partial, 4 altered, 1 lost, 2 unresolved/error.
- Google Docs holdout: 4 preserved, 13 partial, 5 altered, 2 lost, 2 unresolved/error.
- Word holdout: 6 preserved, 11 partial, 6 altered, 1 lost, 2 measurement errors.
- Calibration: 78 controls; 60 correct, 0 false positives, 5 conservative false negatives, 13 correct abstentions.
- Source-oracle mutation testing: 39/39 detected.

## Realistic arm

- Primary LibreOffice + Google Docs realistic evaluation: 20 PDFs and 156 property--pipeline observations.
- Supplementary Word realistic evaluation: 10 additional PDFs and 78 contract observations.
- Total realistic PDFs archived: **30**.
- All realistic documents are project-created/integrated, not natural real-world documents.

## Repeatability

- LibreOffice: 18 runs; classification and normalized semantic stability 6/6.
- Google Docs: 18 runs; classification and normalized semantic stability 6/6; byte identity 6/6.
- Word: 18 runs; classification and normalized semantic stability 6/6; byte identity 0/6.

## Word recovery

Word desktop GUI export succeeded through File -> Export -> Create PDF/XPS with
document-structure tags enabled. All 75 Word PDFs are valid, nonzero,
parseable, and tagged. COM activation remains limited by 0x80070520; this is
documented as an automation/session limitation, not converter unavailability.

## Limitations

The atomic corpus is controlled and purposive. The realistic corpus is
project-created. Google Docs is a dated cloud condition. Word was added after
primary-result completion and is supplementary rather than prospective. The
Word condition uses GUI automation because COM activation failed in the local
Windows session. No disabled-user study, complete reading-order oracle, or
universal accessibility claim is made.

The V4 protocol, contracts, fixtures, source oracle, comparator taxonomy,
holdout rules, calibration expectations, and primary decision rules were not
changed after result inspection.

## Final artifacts

- Manuscript source/PDF: submission/ICST2027_V4/.
- Reviewer-facing artifact bundle: submission/ICST2027_V4/upload/replication_package.zip.
- Exact anonymous upload bundle: submission/ICST2027_V4/ICST2027_V4_anonymous_upload.zip.
- Word recovery report: reports/V4_WORD_GUI_RECOVERY_RESULT.md.
- Word value assessment: reports/V4_WORD_SUPPLEMENT_VALUE_ASSESSMENT.md.
- Word protocol: experiments/v4/word_supplement/WORD_SUPPLEMENT_PROTOCOL.md.
- Word manifest and analysis: experiments/v4/conversions/word/.

## Decision

**GO WITH LIMITATIONS.** The manuscript may include Word as a clearly labeled
post-freeze supplementary third-pipeline result. The primary V4 claim remains
the 130-case LibreOffice + Google Docs experiment.
