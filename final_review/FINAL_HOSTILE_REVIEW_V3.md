# Final Hostile Review V3

## Reviewer A — Document engineering

| Concern | Still valid? | Fixed? | Residual risk | Experiment required? |
|---|---|---|---|---|
| Cross-format contracts may confuse destination absence with semantic loss | Partly | Yes for the primary losses; unresolved cases are now separated | Some feature mappings remain parser-sensitive | No for the bounded paper; richer accepted representations are future work |
| Synthetic one-fixture-per-feature corpus | Yes | Partly, through three secondary multi-feature documents | External validity remains limited | No for submission; larger integrated/variant corpus is future work |
| Only two pipelines | Yes | Disclosed and named precisely | No ecosystem-wide conclusion is possible | No for the bounded claim |
| Oracle circularity | Reduced | Yes: separate OOXML oracle passed 13/13 atomic and 21/21 integrated assertions | No independent human expert panel | No; disclose limitation |
| Integrated-document applicability | Formerly valid | Yes: I01–I03 ran through both pipelines | Secondary check is not representative | No additional experiment required now |

## Reviewer B — Accessibility

| Concern | Still valid? | Fixed? | Residual risk | Experiment required? |
|---|---|---|---|---|
| No disabled-user or screen-reader study | Yes | Explicitly bounded | Structural preservation is not practical usability | No for this protocol paper; user study is future work |
| Structural labels may not equal accessibility | Yes | Explicitly stated | Severity and task impact remain unknown | No; do not make user-impact claims |
| Feature relevance and unequal complexity | Yes | Feature-level reporting and corpus limitation added | One instance per feature family | No for current scope |

## Reviewer C — Software testing

| Concern | Still valid? | Fixed? | Residual risk | Experiment required? |
|---|---|---|---|---|
| Comparator calibration is weak | Yes | Reported honestly: 27 controls, 12 correct determinate, 6 correctly unresolved, 0 false positives, 2 false negatives, 7 other unresolved/indeterminate | Alternate link/table encodings remain conservative | No; uncertainty is now a first-class result |
| Test suite reusability is asserted rather than demonstrated | Reduced | Contracts, certificates, conformance protocol, and integrated run added | Adapter API is conceptual and not a packaged public library | No for paper; packaging is future artifact work |
| Historical labels hide uncertainty | No | V2 evidence-aware taxonomy is primary; V1 is provenance only | Readers may still compare V1 and V2 without reading the changelog | No; table and changelog explain the distinction |

## Reviewer D — PDF expert

| Concern | Still valid? | Fixed? | Residual risk | Experiment required? |
|---|---|---|---|---|
| RoleMap, ParentTree, MCID, inheritance, or alternate encodings may be missed | Yes | Targeted parser triangulation and raw-object checks added | No finite parser audit proves complete PDF semantic coverage | No for bounded claims |
| F06/F11 LOSS may be parser artifacts | Reduced | Both have independent pypdf, PyMuPDF/text, and raw-object evidence; certificates are complete | Undocumented internal application state is unobservable | No; claim is limited to serialized machine-verifiable structure |
| F11/LibreOffice may be loss rather than measurement error | Yes, unresolved | Correctly retained as MEASUREMENT_ERROR | Association remains unmeasured | No; forcing a result would weaken the paper |

## Prior-art and novelty attack

The paper does not claim to be first, unique, or the first accessibility-preservation study. It acknowledges DocAccessible, DAISY, Roig/Ribera, SciA11y, iTagPDF, Kumar et al., and standards/vendor guidance. The defensible contribution is the controlled source-contract, identical-input, uncertainty-aware DOCX-to-PDF preservation protocol and empirical benchmark.

## Overall hostile decision

The strongest remaining rejection argument is limited external validity: a small controlled corpus, two named pipelines, cloud-version uncertainty, and no disabled-user evaluation. That objection is serious but not fatal because the paper now states the scope and does not convert structural observations into universal or user-impact claims. The project survives hostile review as a bounded conformance protocol and empirical benchmark.
