# MINOR FIXES BEFORE PAPER

## 1. Executive conclusion

The experiment survives the hostile audit: no frozen source or output hash changed, the reconstructed 26-row matrix agrees with the frozen classifications, both LOST cases are independently supported, and the one unresolved case remains MEASUREMENT_ERROR rather than being forced into loss. The evidence is strong enough for a scoped paper, but a few paper-grade tooling/documentation fixes should be completed first.

## 2. Freeze integrity

See `audit/PHASE6_FREEZE_INTEGRITY.md`. All 13 source hashes and 26 output hashes match. The freeze did not record a test-results hash; add that to future freeze metadata, but it does not invalidate this experiment.

## 3. Final result counts

11 PRESERVED, 9 PARTIALLY_PRESERVED, 3 ALTERED, 2 LOST, 1 MEASUREMENT_ERROR across 26 valid conversions.

## 4. Denominator rules

Rates should use 25 classifiable cases when excluding the measurement error: PRESERVED 44.0%, PARTIALLY_PRESERVED 36.0%, ALTERED 12.0%, LOST 8.0%. Raw 26-case counts remain primary.

## 5. LOST-case audit

F06 Google Docs and F11 Google Docs are CONFIRMED_LOST under the frozen contracts. Raw PDF markers, tagged validity, pypdf extraction, and independent pdftotext corroborate absence. See `audit/lost_cases/`.

## 6. PARTIAL-case audit

The nine partials each retain deterministic structure but lack a required contract component. The audit does not upgrade them to preserved or downgrade them to lost.

## 7. ALTERED-case audit

All three altered cases change author-relevant values: alt text wording, locale specificity, or document metadata title. They are not harmless encoding differences.

## 8. PRESERVED-case audit

All eleven preserved cases have direct source/destination evidence; residual text-span limitations are documented and not hidden.

## 9. Measurement error

F11 LibreOffice exposes `/Note` but the note body/association is not recoverable with the current extractor plus pdftotext. It remains MEASUREMENT_ERROR.

## 10. Fixture quality

Fixtures are strong or acceptable-with-limitation for causal feasibility testing. They are not a representative population and should not be weighted equally in an overall accessibility score.

## 11. Converter methodology

Both workflows are legitimate native exports. LibreOffice settings are pinned locally; Google Docs is a dated authenticated cloud pipeline. No print-to-PDF or fabricated output was used.

## 12. Comparator validity

The comparator taxonomy passes existing tests and agrees with the frozen matrix. The Phase 6 hostile comparator suite passes 17 explicit cases, and list item-text order checking was added without changing frozen primary classifications. Retain the conservative treatment of parser-limited evidence.

## 13. Reproducibility

Local conversion and extraction are reproducible from retained artifacts. Google Docs requires an account and is vulnerable to cloud updates; Word remains excluded.

## 14. Statistical limits

Report descriptive counts/proportions and feature-level differences only. Do not use inferential statistics or population-level generalizations.

## 15. Novelty recheck

The gap remains defensible but narrower than initially implied. DAISY, DocAccessible, SciA11y, and iTagPDF are adjacent/overlapping work. Position A11yPreserve as source-grounded semantic-preservation measurement for controlled DOCX→PDF pipelines, not as the first accessibility-conversion benchmark.

## 16. Strongest contribution

A reproducible chain from frozen author semantics to real destination structure and differential classification, while separating fidelity from destination accessibility.

## 17. Weakest point

Single-instance feature families and PDF representation/parser limits, especially link names, caption association, decorative artifacts, and footnotes.

## 18. Top reviewer risks

The highest risks are equivalence/oracle limits, small synthetic corpus, cloud-version confounding, no disabled-user study, and unequal feature-unit complexity. Full details are in `audit/TOP_10_REJECTION_RISKS.md`.

## 19. Required fixes

Add explicit freeze hashes for test outputs in future runs; sharpen paper language around Google pipeline attribution and measurement-limited partials; retain feature-level tables as primary.

## 20. Whether additional experiments are necessary

No additional large experiment is required before writing. The targeted comparator-hardening test is complete; duplicate feature instances or an integrated document are optional strengthening experiments, not blockers.

## 21. Recommended final research questions

RQ1–RQ4 remain appropriate, with RQ5 used only if framed around observed cases of accessible-but-altered output.

## 22. Recommended paper contribution statements

Claim a source-grounded framework, frozen controlled corpus, provenance-traceable differential tool, and scoped empirical observations across two DOCX→PDF pipelines.

## 23. Claims we CAN make

Across 13 controlled fixtures and two real pipelines, the method measured a mixture of preservation, partial preservation, alteration, loss, and measurement error; destination accessibility alone did not characterize source-semantic fidelity.

## 24. Claims we CANNOT make

Do not claim that document conversion generally destroys accessibility, that one converter is globally better, that results generalize to all documents/versions, or that validators/users were comprehensively evaluated.

## 25. Recommended publication positioning

A scoped measurement/framework plus controlled empirical benchmark paper, with prior-art differentiation from destination-only validators, PDF reconstruction systems, and broad conversion benchmarks.

## 26. Final recommendation

Complete the minor comparator/documentation fixes, then proceed to paper writing. Do not add converters or fixtures as a reflexive response to the audit.
