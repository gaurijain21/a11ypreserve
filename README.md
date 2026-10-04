# A11yPreserve

A11yPreserve is a source-grounded, contract-based, uncertainty-aware conformance-testing methodology for one question:

> When accessibility information is known to exist in a DOCX source, does that information survive DOCX-to-PDF conversion?

It is not a general PDF accessibility checker, a WCAG/PDF-UA validator, a converter ranking, a prevalence study, or a disabled-user study. It tests selected machine-verifiable source semantics against destination PDF evidence and abstains when semantic equivalence cannot be established safely.

## Current state

The authoritative submission state is [`CANONICAL_SUBMISSION_STATE.md`](CANONICAL_SUBMISSION_STATE.md). The current machine-readable benchmark is [`results/V3_PRIMARY_RESULTS.json`](results/V3_PRIMARY_RESULTS.json): 26 controlled DOCX fixtures, two named pipelines, and 52 fixture–pipeline cases.

Current outcomes are 18 `VERIFIED_PRESERVED`, 4 `OBSERVED_PARTIAL`, 7 `ALTERED`, 4 `CONFIRMED_LOST`, 18 `UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR`. These are controlled-case observations, not prevalence estimates or a global accessibility score.

## Reproduce the evidence

From the repository root:

```powershell
python reproduce.py
```

For the artifact-only self-check:

```powershell
python artifact_v3/src/verify_public_package.py
python artifact_v3/src/independent_source_oracle.py
```

The evidence-only workflow validates stored hashes, source contracts, PDF provenance, result accounting, repeatability records, and artifact sanitization. It does not claim to recreate authenticated Google Docs conversion or Word export without those external conditions.

## Repository layout

| Path | Purpose |
|---|---|
| `corpus/` | Frozen Core source manifests, fixtures, and evidence |
| `corpus/v3_variant_set_b/` | Pre-specified Variant B sources and freeze record |
| `contracts/` | Feature-specific source/destination contracts |
| `results/` | Canonical and historical machine-readable result records |
| `v3/` | Variant B, Google repeatability, and V3 evidence |
| `integrated_study/` | Separate project-generated multi-feature sanity arm |
| `final_strengthening/` | Calibration and difficult-case evidence |
| `tools/` | Consistency and source-oracle corruption checks |
| `submission/ICST2027_V3/` | Current anonymous manuscript source and verified PDF |
| `artifact_v3/` | Review artifact and self-checking replication candidate |
| `docs/current/` | Current methodology, results, limitations, and reproduction notes |
| `docs/archive/` | Archive policy for historical states |

## Benchmark scope

The 13 selected families are headings, alternative text, lists, basic tables, document language, inline language, decorative images, hyperlinks, document title/metadata, complex tables, footnotes, equations, and captions. The selection rationale and fault model are documented in [`docs/FEATURE_SELECTION_RATIONALE.md`](docs/FEATURE_SELECTION_RATIONALE.md) and [`docs/TEST_ADEQUACY_AND_FAULT_MODEL.md`](docs/TEST_ADEQUACY_AND_FAULT_MODEL.md). Reading order was considered but excluded from the atomic denominator because a defensible automated equivalence oracle was not established.

The primary conditions are LibreOffice with recorded tagged/PDF-UA export settings and the recorded authenticated Google Docs DOCX-to-PDF workflow. Microsoft Word is documented as a genuine attempted but unavailable pipeline; no Word result is included.

## Outcome taxonomy

`VERIFIED_PRESERVED` requires contract-supported equivalence. `OBSERVED_PARTIAL` records measured partial correspondence. `ALTERED` records a measured author-value or semantic difference without equating it to complete inaccessibility. `CONFIRMED_LOST` is reserved for independently corroborated absence of the required machine-verifiable representation. `UNRESOLVED_EQUIVALENCE` is a conservative abstention. `MEASUREMENT_ERROR` means the evidence path failed to support a valid decision.

## Evidence and limitations

The 26-row Core result is historical evidence retained unchanged; Variant B is a separate, pre-specified second instance per family. Google repeatability (39 runs), calibration (27 controls), and the integrated three-document arm are supplementary and remain out of the 52-case denominator. The project has no disabled-user task study, no representative real-world corpus, no Word arm, and no claim that structural preservation equals complete accessibility.

Run [`tools/audit_submission_consistency.py`](tools/audit_submission_consistency.py) to regenerate [`reports/FINAL_CONSISTENCY_AUDIT.md`](reports/FINAL_CONSISTENCY_AUDIT.md). Read [`FINAL_SUBMISSION_READINESS.md`](FINAL_SUBMISSION_READINESS.md) for the final adversarial gate and the exact remaining human actions.
