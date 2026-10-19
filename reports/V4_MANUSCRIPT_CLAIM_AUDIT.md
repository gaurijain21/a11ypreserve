# V4 Manuscript Claim Audit

| Claim | Evidence | Supported? | Overclaim risk | Action |
|---|---|---|---|---|
| 13 feature families, 5 variants, 65 fixtures | `source_manifest.json` | Yes | Low | Retain |
| 130 atomic cases | Two 65-row analysis files | Yes | Low | Retain |
| Two real DOCX-to-PDF pipelines | Conversion manifests and route logs | Yes | Must not imply all software versions | Scope to tested conditions |
| LibreOffice/Google outcome counts | Per-pipeline analysis JSON | Yes | Low | Retain separate columns |
| 26-case holdout | `HOLDOUT_MANIFEST.json`, analyses | Yes | Must explain freeze order | Add explicit holdout paragraph |
| 78 calibration controls, 60 correct, 0 false positives, 5 false negatives, 13 abstentions | `COMPARATOR_CALIBRATION.json` | Yes | “Validated comparator” would overclaim | Call diagnostic calibration |
| 39/39 source mutations detected | `SOURCE_ORACLE_MUTATION_AUDIT.json` | Yes | Does not establish external oracle validity | Say separately implemented |
| Google classifications are repeatable | Normalized repeatability audit | Yes | Cloud service is dated | Report 6/6 classification stability |
| Realistic corpus | Realistic manifest and analyses | Yes | “Real-world” would overclaim | Use project-created realistic/integrated |
| Accessibility preservation | Source contracts plus destination evidence | Yes | Not user task success or PDF certification | Define scope explicitly |
| V4 is novel/first | Prior-art audits | No as a broad claim | High | Use bounded combination/method wording |
| V4 can replace V3 | Two complete arms and frozen analyses | Supported with limitations | Word absent, cloud versioning, synthetic corpus | GO WITH LIMITATIONS |

No unsupported “first,” “universal,” “complete checker,” or disabled-user usability claim remains in the V4 source.
