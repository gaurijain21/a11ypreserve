# Final V4 Adversarial Review

## Decision

**GO WITH LIMITATIONS.** The frozen V4 experiment has two legitimate, independently identified converter arms and supports replacing V3 as the primary submission basis. The decision does not imply that Word, external real-world documents, reading order, complete PDF conformance, or disabled-user performance were established.

## Hostile checks

| Attack | Result | Evidence / disposition |
|---|---|---|
| Frozen protocol changed after seeing outputs | PASS | `reports/V4_FINAL_HARDENING_BASELINE.md`; frozen protocol and decision-rule hashes retained. |
| Primary result files overwritten | PASS | Existing LO, Google, holdout, cross-pipeline, and repeatability result artifacts retained; post-result work is separately marked diagnostic or manuscript-only. |
| Fake or relabeled PDFs | PASS | Conversion manifests retain source/output hashes, timestamps, producer observations, and routes; Word zero-byte pilot was deleted and counted as no output. |
| V3 PDF reused as V4 | PASS | No V3 PDF is used as a V4 conversion output. |
| Print-to-PDF or screenshot substituted | PASS | LO used Writer export; Google used Docs PDF download; no print or screenshot route is claimed. |
| Missing/altered source fixture | PASS | Reproducibility entry point verifies the 65 source-manifest hashes and 75 records per completed pipeline. |
| Holdout leakage | PASS | Holdout remains separately reported and was not used to tune the comparator or contracts. |
| Comparator overclaim | PASS | 78 calibration controls include 0 false positives, 5 conservative false negatives, and 13 correct abstentions; false-negative audit explains the evidence boundary. |
| Source-oracle circularity | PASS WITH LIMITATIONS | Oracle path is separately implemented and detected 39/39 mutations; final audit documents that it was not externally validated. |
| Repeatability instability hidden | PASS | Six selected variants x three runs are reported. Normalized semantic evidence is stable 6/6 for both pipelines; raw extraction identity is not claimed as stable. |
| LO measurement errors silently resolved | PASS | Five footnote cases remain `MEASUREMENT_ERROR`; the measurement-error audit documents the unresolved representation limitation. |
| Unresolved cases silently forced | PASS | Five Google footnote cases and one LO caption case remain unresolved/measurement-bound as specified by the frozen evidence boundary. |
| Reading-order result invented | PASS | Final feasibility decision is `NO-GO — ORACLE NOT DEFENSIBLE`; reading order is excluded from the 13-feature denominator. |
| Word claimed after failed export | PASS | Direct GUI launch/open worked, but the native pilot produced a persistent zero-byte PDF; Word is excluded. |
| External corpus inflated | PASS | External count is zero; public candidates were identified but not downloaded, uploaded, or analyzed. |
| Validator conformance invented | PASS | PAC/Acrobat/veraPDF comparison is explicitly unavailable; pdfinfo/PyMuPDF are not presented as complete validators. |
| Prior-art novelty overstated | PASS | Related work and final prior-art audit use bounded wording and do not claim first-ever or universal coverage. |
| Manuscript numbers inconsistent | PASS | Abstract, atomic table, feature table, holdout text, readiness, and analysis artifacts use the frozen counts; `reproduce_v4.py` passes. |
| Anonymity or licensing leak | PASS WITH LIMITATIONS | Manuscript author is anonymous; artifact audit excludes credentials and user identifiers. Public candidate URLs are documented as provenance leads only; no external files were redistributed. |
| Compiled PDF fabricated | PASS | The PDF was generated directly from the reviewed V4 LaTeX source with MiKTeX, parsed as three pages, and visually inspected page by page. |

## Residual threats

The strongest remaining threats are the dated Google service condition, the controlled rather than representative corpus, the project-created realistic corpus, Word non-coverage, and lack of a defensible reading-order oracle. These are limitations of scope, not hidden successful arms.

## Final reviewer disposition

The evidence is sufficient for a V4 submission package with limitations and for replacing V3 as the primary experimental basis. The manuscript now compiles in the local MiKTeX environment and the three rendered pages have been visually reviewed. Venue-format and submission-policy review remain separate human submission steps.
