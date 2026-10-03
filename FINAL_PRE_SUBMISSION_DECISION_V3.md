# READY FOR SUBMISSION TARGETING; PDF GATE OPEN

## 1. Final title

**A11yPreserve: An Uncertainty-Aware Conformance Suite for DOCX-to-PDF Accessibility Preservation**

## 2. Final paper thesis

Machine-verifiable accessibility information can be tested against explicit source contracts during document conversion, but destination-only structure checks cannot establish preservation by themselves.

## 3. Final contribution

A controlled source-to-destination DOCX-to-PDF preservation protocol combining versioned contracts, independent OOXML source verification, calibrated differential comparison, parser triangulation, evidence lineage, and explicit unresolved-equivalence states.

## 4. Primary empirical scope

13 controlled atomic DOCX fixtures, 26 genuine outputs, and two named pipelines: LibreOffice and the Google Docs DOCX-to-PDF conversion pipeline. Microsoft Word remains excluded from the denominator.

## 5. Integrated sanity-check scope

Three realistic two-page multi-feature documents, 21/21 independent source assertions, six tagged PDFs, and 42 secondary property–pipeline observations. The secondary observations are excluded from the primary denominator.

## 6. Source-oracle status

13/13 atomic contracts and 21/21 integrated contracts independently passed fresh raw-OOXML checks. ASIR is disclosed as implementation-grounded rather than independent human validation.

## 7. Comparator-calibration status

27 diagnostic controls: 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, and 7 other unresolved/indeterminate. The paper reports these as calibration diagnostics only.

## 8. Evidence-aware result distribution

11 VERIFIED_PRESERVED; 3 OBSERVED_PARTIAL; 3 ALTERED; 2 CONFIRMED_LOST; 6 UNRESOLVED_EQUIVALENCE; 1 MEASUREMENT_ERROR.

## 9. Confirmed losses

F06/Google Docs inline language and F11/Google Docs footnote association. Both claims are limited to machine-verifiable destination structure, not visible-text disappearance or user harm.

## 10. Unresolved cases

Six historical partial cases are now reported as UNRESOLVED_EQUIVALENCE: F03/Google Docs, both F08 cases, F10/Google Docs, F12/Google Docs, and F14/Google Docs.

## 11. Measurement errors

F11/LibreOffice remains MEASUREMENT_ERROR because the available evidence cannot resolve the note-body association.

## 12. Novelty boundary

No first, unique, or no-prior-work claim. The contribution is the controlled source-contract, identical-input, uncertainty-aware preservation protocol and benchmark. Related work includes DocAccessible, DAISY, Roig/Ribera, SciA11y, iTagPDF, and Kumar et al.

## 13. Closest prior art

Roig/Ribera is the closest conceptual office-document conversion precedent; DAISY and DocAccessible are current benchmark threats; SciA11y and iTagPDF concern accessible representation generation/remediation; Kumar et al. concerns destination-only PDF accessibility evaluation.

## 14. Largest remaining weakness

External validity: the atomic corpus is small, feature families are unequal, only two pipelines were tested, Google Docs is cloud-versioned, and no disabled-user study was performed.

## 15. Artifact status

The frozen V1 evidence is unchanged. V2 evidence-aware results, changelog, contracts, source certificates, loss certificates, calibration, integrated secondary study, parser triangulation, and manuscript audits are present. The sanitized artifact passes its self-check. No current V3 PDF is asserted: the V3 source remains uncompiled in this environment, so PDF metadata, page count, and final visual QA remain open. Public packaging still needs licensing/provenance review.

## 16. Recommended primary venue family

Document engineering / ACM DocEng.

## 17. Backup venue family

Accessibility research / ACM ASSETS, with the same structural-preservation and no-user-impact boundary.

## 18. Exact remaining fixes

Before submission/public release: compile and visually inspect the V3 venue copy in a trusted IEEEtran/LaTeX environment, freeze its PDF hash/page count/metadata, verify artifact licensing/provenance, and apply the target venue template. No new scientific experiment is required.

## 19. Submission recommendation

Use V2 as the primary result model and label V1 clearly as historical. Do not upload until the V3 PDF gate is closed. Do not submit as a general accessibility validator, universal conversion claim, product ranking, or disabled-user impact study.
