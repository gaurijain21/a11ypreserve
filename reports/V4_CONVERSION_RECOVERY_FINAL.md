# V4 Conversion Recovery Final Audit

Generated: `2026-10-05T01:38:54.747993+00:00`

Overall audit status: **PASS**

## Adversarial checks

| Check | Result |
|---|---|
| frozen_hashes_match | PASS |
| google_output_records | PASS |
| google_outputs_all_pass | PASS |
| google_atomic_analysis_65 | PASS |
| google_holdout_26 | PASS |
| calibration_60_correct | PASS |
| calibration_zero_false_positive | PASS |
| calibration_five_false_negative | PASS |
| calibration_thirteen_correct_unresolved | PASS |
| source_oracle_39_of_39 | PASS |
| google_repeatability_18 | PASS |
| google_repeatability_classification_stable_6 | PASS |
| cross_pipeline_atomic_65 | PASS |
| no_identity_hits_in_google_artifacts | PASS |

## Frozen hash verification

| Component | Expected | Actual | Match |
|---|---|---|---|
| source_manifest | `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7` | `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7` | YES |
| realistic_manifest | `E09C8EE8A5569B789E6BAC92DA8D5FF03CEBEBFA18DFF497FD9CDBA284985ED4` | `E09C8EE8A5569B789E6BAC92DA8D5FF03CEBEBFA18DFF497FD9CDBA284985ED4` | YES |
| protocol | `B4A2F974B7E14CB6C5847EB8667BF3A7E9CDF5C38C60AFE9C47391F476648556` | `B4A2F974B7E14CB6C5847EB8667BF3A7E9CDF5C38C60AFE9C47391F476648556` | YES |
| comparator | `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4` | `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4` | YES |
| source_oracle | `7B5C309D80BD2DC32438A8EACE499ED145A0BF77E880616A0AA0875935EC1DE6` | `7B5C309D80BD2DC32438A8EACE499ED145A0BF77E880616A0AA0875935EC1DE6` | YES |
| destination_extractor | `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7` | `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7` | YES |
| frozen_analysis | `08FF23F71DE46D1DB31AC459878B5165506EAC83311FD7510222AD0A51C9D13D` | `08FF23F71DE46D1DB31AC459878B5165506EAC83311FD7510222AD0A51C9D13D` | YES |
| holdout_manifest | `CC228687B6097886DF66CFFE3F112499AA83BE7056B90394D0C60869DB075E9E` | `CC228687B6097886DF66CFFE3F112499AA83BE7056B90394D0C60869DB075E9E` | YES |

## Google provenance gate

- Records: **75/75** (65 atomic + 10 realistic documents).
- All output checks passed: **True**.
- Observed producer: `Skia/PDF m156 Google Docs Renderer` for the completed corpus.
- Route: authenticated Google Docs visible UI import followed by `File -> Download -> PDF Document (.pdf)` and Chrome download capture.
- No print-to-PDF, screenshot, post-export repair, or V3 PDF reuse was used.

## Frozen analysis and holdout

- Google atomic analysis: **65/65**.
- Google holdout: **26/26**.
- Cross-pipeline atomic comparison: **16 same / 49 different** classifications.

## Repeatability

- Google: **6 fixtures × 3 runs = 18 outputs**.
- Classification stable: **6/6**.
- Byte-identical: **6/6**.
- Extraction-identical: **0/6**.

## Scope and integrity

The V4 protocol, feature families, fixture corpus, source oracle, comparator boundary, taxonomy, and holdout rules were not changed after result inspection. Implementation repairs were limited to output capture and JSON/report plumbing.

No credentials or unrelated documents were uploaded. The Google artifacts contain no detected email, account-name, OAuth, token, password, or secret strings.
