# Final V3 completion kill audit

This audit treats the completed V3 work as hostile review evidence. V2 files and classifications remain frozen. V3 rows are secondary/extension evidence and are not retroactively substituted into V2.

| Attack | Severity | Evidence | Mitigation | Residual risk | Fatal? |
|---|---|---|---|---|---|
| Post-hoc taxonomy | HIGH | V2 taxonomy was introduced after methodology review. | Chronology is disclosed; label-hidden reclassification reproduced 26/26 stored Core labels; V3 rules were frozen before Variant B outputs. | Not preregistration or external adjudication. | No |
| Oracle subjectivity | HIGH | Cross-format mappings require feature-specific judgment. | Contracts, precedence, evidence statuses, calibration, and explicit abstention. | Some equivalence remains unresolved. | No |
| Classification overlap | MEDIUM | Partial, altered, lost, and unresolved can appear similar in raw observations. | Normative precedence puts measurement error and confirmed loss first and defines categories operationally. | A reviewer may dispute individual contract boundaries. | No |
| Calibration weakness | HIGH | 27 controls: 12 correct determinate, 6 safe abstentions, 0 false positives, 2 false negatives, 7 unresolved/indeterminate. | False-negative impact is documented; affected link/table rows remain unresolved. | Comparator sensitivity is not complete. | No |
| Calibration code dependence | MEDIUM | Comparator and calibration driver share project code. | Ground-truth controls and failure modes are disclosed; no sensitivity claim. | Limited independence. | No |
| False confirmed loss | HIGH | F06/B06 and F11/B11 Google lack required structure in pypdf traversal and serialized PyMuPDF scans, while visible text remains. | Dedicated two-path audit checks StructTreeRoot, RoleMap, ParentTree, roles, markers, annotations, and raw objects. | No finite parser audit proves absence from hidden internal state. | No |
| Within-feature inconsistency | HIGH | Variant B exposes mixed/unresolved rows for lists, tables, complex tables, equations, and captions. | Matrix reports fixture sensitivity and unresolved evidence; no forced consistency claim. | The suite does not establish invariance. | No |
| No formal adequacy metric | HIGH | Feature selection is purposive; no coverage percentage or complete fault model. | Explicit adequacy boundary and measurability-bias disclosure; F13 deferral named. | A reviewer may request mutation/standards coverage. | No |
| Google repeatability instability | MEDIUM | 13/13 Core classifications stable and byte-identical across three runs. | Reported with date/workflow/backend limitation. | Cloud backend can change after the study. | No |
| Only two pipelines | HIGH | Only LibreOffice and Google Docs pipeline evaluated. | Claims limited to two named pipelines; no ecosystem ranking. | External validity is narrow. | No |
| Opaque Google stages | MEDIUM | Import, internal representation, and export were not isolated. | Use end-to-end pipeline wording and disclose Variant B route. | Causal attribution is unavailable. | No |
| No disabled-user validation | MEDIUM | No users or screen-reader task study. | Explicit structural-preservation boundary; no user-impact claims. | Accessibility reviewers may prefer user evidence. | No |
| Synthetic integrated documents | MEDIUM | Integrated I01--I03 are project-generated. | Called multi-feature integrated documents and kept at 3 documents/42 observations. | No real-world representativeness. | No |
| No third-party reproduction | MEDIUM | Authors ran the analysis; fresh-environment install was previously constrained. | Hashes, contracts, scripts, evidence records, and three reproducibility levels documented. | Independent replication remains future work. | No |
| Prior-art overlap | HIGH | DocAccessible, DAISY, Roig/Ribera, Kumar, iTagPDF, and SciA11y address adjacent conversion/evaluation problems. | Narrow contribution: controlled source-grounded contract conformance with uncertainty and provenance; no first/unique claim. | Incremental novelty judgment remains plausible. | No |
| ICST relevance | HIGH | A reviewer could view this as document engineering rather than software testing. | Explicitly maps contracts to test oracles, fixtures to inputs, pipelines to SUTs, extraction to observations, and abstention to oracle uncertainty. | No general testing theory or broad fault model. | No |

## Top remaining weaknesses

1. The contribution may be judged incremental relative to current conversion benchmarks and too domain-specific for a software-testing venue.
2. The 18 unresolved atomic rows show that cross-format oracle coverage is incomplete, even though the method reports that uncertainty honestly.
3. Two controlled instances per feature family do not establish comprehensive adequacy or real-world prevalence.
4. The Variant B Google arm used a documented export-backend recovery route rather than a fully successful visible UI download path.
5. The V3 manuscript cannot be locally compiled in the current environment because MiKTeX has no permitted writable configuration and the built-in compiler reports missing standard directories; this is a packaging verification blocker, not a scientific result.

## Overall judgment

No attack demonstrates that the source/destination semantics are incomparable or that the confirmed losses are measurement artifacts. The project survives hostile methodological review with narrow claims. The most credible rejection remains significance/novelty or venue fit, not invalidity of the bounded preservation question.
