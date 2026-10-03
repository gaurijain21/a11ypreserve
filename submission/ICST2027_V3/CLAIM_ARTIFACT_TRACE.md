# V3 claim-to-artifact trace

This trace binds the claims in the V3 ICST submission copy to the frozen evidence and derived package records. It is a packaging trace, not new scientific evidence.

| Manuscript claim or reported result | Artifact source | Verification boundary |
|---|---|---|
| 26 controlled fixtures and 52 atomic fixture--pipeline cases | `results/V3_PRIMARY_RESULTS.json`, `results/V3_PRIMARY_RESULTS.md` | One fixture/pipeline pair is the unit; this is not a representative sample. |
| 18 verified preserved, 4 observed partial, 7 altered, 4 confirmed lost, 18 unresolved equivalence, 1 measurement error | `results/V3_PRIMARY_RESULTS.json` | Machine-readable labels use the frozen evidence-aware names `VERIFIED_EQUIVALENCE`, `OBSERVED_PARTIAL`, `OBSERVED_DIFFERENCE`, `INDEPENDENTLY_CONFIRMED_ABSENCE`, `UNRESOLVED_EQUIVALENCE`, and `MEASUREMENT_FAILURE`; the manuscript presents their bounded terminology. |
| Feature-level Core/Variant B comparison | `results/V3_WITHIN_FEATURE_CONSISTENCY.md`, `v3/variant_set_b/V3_VARIANT_SET_B_FINAL_RESULTS.json` | Interpretations are feature-specific; no aggregate converter ranking is justified. |
| F06 inline-language and F11 footnote-association losses | `v3/variant_set_b/google/DIFFICULT_CASE_AUDIT.json`, `final_strengthening/loss/F06_GOOGLE_LOSS_CERTIFICATE.md`, `final_strengthening/loss/F11_GOOGLE_LOSS_CERTIFICATE.md` | Contract-level absence of required machine-verifiable structure in the tested Google Docs DOCX-to-PDF pipeline; no user-impact or export-stage causation claim. |
| Core source contracts and source ground truth | `corpus/FROZEN_CORPUS_MANIFEST.json`, `contracts/`, `evidence/source/` | Manifest, raw OOXML inspection, source-extractor agreement, and separately implemented raw-OOXML oracle; not external human validation. |
| Variant B source verification | `corpus/v3_variant_set_b/SOURCE_ORACLE.json`, `evidence/source/` | 13/13 source contracts passed under the separately implemented oracle. |
| Google repeatability | `v3/google_repeatability/RUN_MANIFEST.json`, `v3/google_repeatability/REPEATABILITY_RESULTS.json`, `v3/google_repeatability/GOOGLE_REPEATABILITY_FINAL.md` | 13 Core fixtures x 3 runs = 39; classifications stable 13/13 and bytes identical 13/13 under the recorded workflow. The cloud backend is not fully pinned. |
| Integrated sanity check | `integrated_study/INTEGRATED_RESULTS.md` | 3 project-generated multi-feature documents, 21/21 source assertions, and 42 property--pipeline observations; separate denominator. |
| Calibration and uncertainty handling | `final_strengthening/COMPARATOR_CALIBRATION.md`, `final_methodology/CALIBRATION_FALSE_NEGATIVE_IMPACT_FINAL.md` | 27 diagnostic controls: 12 correct determinate, 6 safe abstentions, 0 false positives, 2 false negatives, 7 unresolved/indeterminate; not sensitivity or specificity. |
| Reproducibility package | `artifact_v3/README.md`, `submission/A11yPreserve_artifact_ICST2027_V3.zip` | Level 1 evidence verification and Level 2 LibreOffice reproduction are documented; Level 3 Google repetition is workflow-repeatable but backend-dependent. |

The V3 submission source is `submission/ICST2027_V3/main.tex`. A final PDF claim is intentionally absent because compilation and visual inspection have not been verified in the current environment.
