# Claim-Evidence Audit V2

| Section | Substantive claim | Supporting artifact | Strength | Acceptable? |
|---|---|---|---|---|
| Introduction | The primary benchmark contains 13 fixtures and 26 outputs | `corpus/FROZEN_CORPUS_MANIFEST.json`; `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` | DIRECT | YES |
| Introduction | The primary V2 distribution is 11 verified preserved, 3 observed partial, 3 altered, 2 confirmed lost, 6 unresolved, and 1 measurement error | `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` | DIRECT | YES |
| Method | All 13 frozen source contracts agreed with the independent OOXML oracle | `final_strengthening/INDEPENDENT_SOURCE_ORACLE.md`; `evidence/source/*_certificate.json` | DIRECT | YES |
| Method | ASIR is implementation-grounded and is cross-checked by manifests, raw OOXML, and a separate oracle | `final_strengthening/INDEPENDENT_SOURCE_ORACLE.md` | DIRECT | YES |
| Method | LibreOffice and Google Docs conditions, versions, and workflow are recorded | `results/full_experiment/AUTOMATION_LOG.md`; `research/FINAL_METHODS_SPEC.md` | DIRECT | YES |
| Method | Destination evidence uses pypdf structure inspection plus secondary text/object checks | `final_strengthening/PDF_PARSER_TRIANGULATION.md`; `scripts/pdf_parser_triangulation.py` | DIRECT | YES |
| Method | Calibration contains 27 diagnostic controls with 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, and 7 other unresolved/indeterminate | `final_strengthening/COMPARATOR_CALIBRATION.md`; `final_strengthening/COMPARATOR_CALIBRATION.json` | DIRECT | YES, diagnostic only |
| Results | All 26 primary conversion attempts produced valid tagged PDFs | `results/full_experiment/reports/output_validation.json` | DIRECT | YES |
| Results | F06/Google Docs inline language is confirmed lost at the machine-verifiable contract level | `final_strengthening/loss/F06_GOOGLE_LOSS_CERTIFICATE.md` | DIRECT | YES, bounded |
| Results | F11/Google Docs footnote association is confirmed lost while visible note text remains | `final_strengthening/loss/F11_GOOGLE_LOSS_CERTIFICATE.md` | DIRECT | YES, bounded |
| Results | F11/LibreOffice remains measurement error | `final_strengthening/PDF_PARSER_TRIANGULATION.md` | DIRECT | YES |
| Results | Six historical partial cases are unresolved equivalence rather than directly observed partial preservation | `final_strengthening/PARTIAL_CASE_REAUDIT.md`; `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` | DIRECT | YES |
| Results | Three realistic integrated documents yielded 42 secondary property-pipeline observations | `integrated_study/INTEGRATED_RESULTS.md`; `integrated_study/INTEGRATED_RESULTS.json` | DIRECT | YES, secondary only |
| Results | The integrated source oracle passed 21/21 assertions | `integrated_study/INTEGRATED_SOURCE_ORACLE.md`; `integrated_study/INTEGRATED_SOURCE_ORACLE.json` | DIRECT | YES |
| Discussion | Preservation behavior is feature-specific and pipeline-dependent | `results/FINAL_EVIDENCE_AWARE_RESULTS.md`; feature-level matrix | DERIVED | YES, scoped |
| Threats | The corpus is controlled and not representative; no disabled-user study was performed | `research/CORPUS_LIMITATION_NOTE.md`; `research/USER_STUDY_SCOPE_NOTE.md` | DIRECT | YES |
| Threats | Google Docs backend version cannot be fully pinned | `audit/REPRODUCIBILITY_AUDIT.md`; `results/full_experiment/AUTOMATION_LOG.md` | DIRECT | YES |
| Conclusion | Source-grounded preservation measurement is feasible under the tested contracts and pipelines | Full method, V2 matrix, and integrated sanity artifacts | DERIVED | YES, bounded |

No central manuscript claim asserts universal converter behavior, general prevalence, disabled-user impact, complete accessibility checking, a global converter ranking, or PDF-export-only causation. V1 remains a historical provenance record; V2 is the primary evidence-aware result model.
