# Manuscript-to-Evidence Reconciliation

This review covers the actual final manuscript source, including the abstract, all eight sections, tables, and figures. Evidence strength is DIRECT, DERIVED, or INTERPRETIVE.

| Section | Empirical claim | Source artifact | Strength | Correct? | Revision |
|---|---|---|---|---|---|
| Abstract | 13 fixtures and 26 genuine DOCX-to-PDF outputs | Frozen corpus manifest; output validation; automation logs | DIRECT | Yes | None |
| Abstract | All outputs were parseable, tagged, non-empty, and validated | `output_validation.json` | DIRECT | Yes | None |
| Abstract | 11/9/3/2/1 outcome counts and 25 determinate cases | `PRIMARY_RESULTS_FREEZE.json`; denominator audit | DIRECT/DERIVED | Yes | None |
| Abstract | Two confirmed losses concern F06 and F11 in Google Docs | Lost-case forensic reports | DIRECT | Yes | None |
| Introduction | Source accessibility properties are intentionally encoded before conversion | Frozen manifests, OOXML, ASIR | DIRECT | Yes | None |
| Introduction | Standards motivate preservation testing | W3C ATAG 2.0; Section 508; EN 301 549 | DIRECT | Yes | None |
| Introduction | Prior work covers office conversion, PDF-to-HTML, remediation, and evaluation | Verified bibliography and related-work notes | DIRECT | Yes | None |
| Method | Ground truth requires manifest, OOXML, and ASIR agreement | Source verification reports | DIRECT | Yes | None |
| Method | Exact LibreOffice version/settings and Google workflow | Full-experiment automation log | DIRECT | Yes | None |
| Method | Destination structure and independent text evidence were inspected | Extractor code, evidence files, validation report | DIRECT | Yes | None |
| Method | Rules/contracts were fixed before final classification review | Phase 6 audit and frozen contracts | DIRECT | Yes | Added explicit sentence |
| Experiment | 13 x 2 = 26 fixture/pipeline cases | Frozen corpus and primary freeze | DERIVED | Yes | None |
| Results | Ten of 13 fixture rows differ across pipelines | Cross-converter table | DIRECT | Yes | None |
| Results | F06 and F11 Google Docs cases are LOST | Forensic lost-case reports and raw evidence | DIRECT | Yes | None |
| Results | F11 LibreOffice is MEASUREMENT_ERROR | Measurement-error analysis | DIRECT | Yes | None |
| Results | Three ALTERED cases retain related information but change author-relevant values | Altered-case audit and primary freeze | DIRECT | Yes | None |
| Discussion | Behavior is feature-specific and pipeline-dependent | Feature matrix | DERIVED | Yes, scoped | None |
| Discussion | The Google condition does not isolate import, internal representation, and export | Pipeline attribution audit | DIRECT | Yes | None |
| Threats | Synthetic corpus, unequal feature complexity, two pipelines, cloud versioning, parser sensitivity, and no user study limit generalization | Phase 6 audits and research limitation notes | DIRECT | Yes | None |
| Conclusion | Source-grounded preservation measurement is feasible | Complete frozen chain and 26-row matrix | DERIVED | Yes, bounded | None |

No unsupported central empirical claim remains. Interpretive statements are explicitly scoped to the controlled benchmark and named pipeline conditions.
