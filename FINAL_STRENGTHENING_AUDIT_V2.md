# SCIENTIFICALLY READY FOR SUBMISSION TARGETING

## Source oracle

The independent raw-OOXML oracle agreed with 13/13 frozen atomic source contracts. The secondary integrated oracle passed 21/21 assertions across I01–I03. ASIR remains implementation-grounded; no independent human expert panel was claimed.

## Comparator calibration

The calibration suite contained 27 hand-constructed controls: 12 correct determinate results, 6 correctly retained unresolved, 0 false positives, 2 false negatives, and 7 other unresolved/indeterminate cases. These are diagnostic calibration counts, not sensitivity, specificity, or population estimates. Alternate encodings are the main source of conservative unresolved behavior.

## Primary evidence-aware results

| Final result | Count |
|---|---:|
| VERIFIED_PRESERVED | 11 |
| OBSERVED_PARTIAL | 3 |
| ALTERED | 3 |
| CONFIRMED_LOST | 2 |
| UNRESOLVED_EQUIVALENCE | 6 |
| MEASUREMENT_ERROR | 1 |

The primary unit is one of 26 fixture–pipeline pairs. No percentages or inferential statistics are used.

## Historical V1 results

| V1 result | Count |
|---|---:|
| PRESERVED | 11 |
| PARTIALLY_PRESERVED | 9 |
| ALTERED | 3 |
| LOST | 2 |
| MEASUREMENT_ERROR | 1 |

V1 was created before the parser/equivalence strengthening pass. The source files, PDFs, manifests, hashes, and primary classifications did not change. V2 refines interpretation by separating directly observed partial preservation from unresolved equivalence; V1 remains archived for provenance.

## Confirmed losses

- F06 / Google Docs: `CONFIRMED_LOST` for the machine-verifiable inline `es-MX` language span; visible phrase text remains.
- F11 / Google Docs: `CONFIRMED_LOST` for the machine-verifiable footnote association; visible reference and note text remain.
- F11 / LibreOffice: `MEASUREMENT_ERROR` because a `/Note` exists but association cannot be resolved.

## Integrated sanity check

Performed: yes. Documents: 3 realistic two-page documents. Independent source assertions: 21/21. Property–pipeline observations: 42. The protocol remained usable when existing feature contracts coexisted. Results are secondary and excluded from the primary denominator.

## Closest prior art

Roig/Ribera is the closest conceptual office-document conversion precedent. DAISY and DocAccessible are current benchmark threats. SciA11y and iTagPDF address accessible representation generation or remediation, while Kumar et al. address destination-only PDF accessibility evaluation. A11yPreserve does not claim superiority or absence of prior work.

## Final novelty statement

The contribution is a controlled source-contract, identical-input, uncertainty-aware DOCX-to-PDF preservation protocol and empirical benchmark with independent source verification, calibrated comparison, destination evidence lineage, and reusable conformance artifacts.

## Remaining limitations

The corpus is small and controlled; feature families have unequal complexity; only two named pipelines were tested; Google Docs backend version cannot be fully pinned; cross-format equivalence remains feature-specific; no complete PDF accessibility, screen-reader, task-completion, perceived-usability, or disabled-user claim is supported; and the integrated check is not representative.

## Artifact readiness

Contracts, source certificates, V2 results, interpretation changelog, calibration artifacts, loss certificates, parser triangulation, integrated sources and outputs, hostile review, manuscript audits, and the final rendered PDF are present. Public release still requires path sanitization and licensing/provenance verification.

## Recommended venue

Primary: ACM DocEng or a document-engineering venue. Backup: ASSETS with the same structural-preservation boundary and no user-impact overclaim.

## Additional experiment required?

No. The integrated sanity check addresses protocol applicability sufficiently for the bounded paper. Larger corpora, more converters, and user studies are future work, not blockers for this claim.

## Final recommendation

Proceed toward submission targeting with V2 as the primary result model. Do not present the work as a general PDF accessibility validator, universal conversion law, converter ranking, or disabled-user impact study.
