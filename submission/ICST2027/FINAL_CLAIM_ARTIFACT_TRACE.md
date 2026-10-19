# Final paper–artifact claim trace

Audit date: 2026-09-29

This trace covers the frozen V2 ICST 2027 submission candidate. It does not add claims, alter classifications, or incorporate V3 internal work.

## Primary benchmark

| Paper claim | Artifact support | Verification status |
|---|---|---|
| 13 controlled atomic DOCX fixtures | `artifact/corpus/FROZEN_CORPUS_MANIFEST.json`; `artifact/corpus/fixtures/`; `artifact/contracts/` | PASS; manifest records the frozen corpus and source hashes |
| 26 primary fixture–pipeline cases and genuine outputs | `artifact/corpus/outputs/libreoffice/`; `artifact/corpus/outputs/google_docs/`; `artifact/corpus/BUILD_RECORD.json` | PASS; 13 outputs per tested pipeline |
| Evidence-aware result distribution: 11 VERIFIED PRESERVED, 3 OBSERVED PARTIAL, 3 ALTERED, 2 CONFIRMED LOST, 6 UNRESOLVED EQUIVALENCE, 1 MEASUREMENT ERROR | `artifact/results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json`; `artifact/results/FINAL_EVIDENCE_AWARE_RESULTS.md`; `artifact/results/full_experiment/EVIDENCE_STATUS_FREEZE_V2.json` | PASS; frozen JSON has `record_count: 26` and the six stated counts |
| Source-grounded preservation protocol | `artifact/contracts/`; `artifact/src/`; `artifact/docs/CONFORMANCE_SUITE.md` | PASS; contracts, extraction, comparison, and evidence paths are included |
| Independent source verification | `artifact/src/independent_source_oracle.py`; `artifact/results/INDEPENDENT_SOURCE_ORACLE.json`; `artifact/final_strengthening/INDEPENDENT_SOURCE_ORACLE.md`; `artifact/corpus/reports/source_verification.json` | PASS; retained oracle result records 13 passed fixtures |
| F06 inline-language confirmed loss | `artifact/contracts/F06_INLINE_LANGUAGE.json`; `artifact/corpus/evidence/loss/F06_GOOGLE_LOSS_CERTIFICATE.md`; F06 source/output PDFs and evidence | PASS; paper claim is limited to the tested Google Docs pipeline |
| F11 footnote-association confirmed loss | `artifact/contracts/F11_FOOTNOTES.json`; `artifact/corpus/evidence/loss/F11_GOOGLE_LOSS_CERTIFICATE.md`; F11 source/output PDFs and evidence | PASS; paper does not claim visible note text disappeared |

## Secondary integrated sanity check

| Paper claim | Artifact support | Verification status |
|---|---|---|
| Separate evaluation of 3 multi-feature documents | `artifact/integrated_study/INTEGRATED_RESULTS.md`; `artifact/integrated_study/INTEGRATED_RESULTS.json` | PASS; separate from the primary denominator |
| 21/21 integrated source assertions | `artifact/integrated_study/INTEGRATED_SOURCE_ORACLE.json`; `artifact/integrated_study/INTEGRATED_SOURCE_ORACLE.md` | PASS |
| 42 property–pipeline observations | `artifact/integrated_study/INTEGRATED_RESULTS.json` and retained integrated PDFs/evidence | PASS; explicitly not a prevalence estimate and not merged with the 26 primary cases |

## Provenance and reproducibility

`artifact/corpus/manifests/hashes.json`, `artifact/corpus/BUILD_RECORD.json`, the evidence directories, and `artifact/results/RESULT_INTERPRETATION_CHANGELOG.md` retain source/output provenance and the V2 interpretation boundary. `artifact/README.md` documents verification of existing evidence, local reproduction limits, and the non-pinned Google Docs cloud backend.

## Boundary check

The artifact supports the paper's bounded claim about measuring preservation of known DOCX accessibility information across the two tested pipelines. It does not support universal converter behavior, real-world prevalence, disabled-user usability, product superiority, or a conclusion that every unresolved case is degradation. V3 internal strengthening work is excluded from the upload artifact and is not part of the V2 paper.
