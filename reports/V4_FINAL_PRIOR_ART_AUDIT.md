# V4 Final Prior-Art Audit

The current review rechecked the closest cited lines of work and the methodological framing. The defensible contribution is not “first” conversion research, a PDF checker, or a remediation system.

| Work/line | Source ground truth | Source-to-destination preservation relation | Controlled contracts | Cross-format oracle | Explicit abstention | Goal |
|---|---|---|---|---|---|---|
| Roig/Ribera office-to-EPUB conversion | Adjacent/partial | Conversion accessibility consequences | Not the same contract model | Not the same PDF relation | Not the same uncertainty taxonomy | Accessible office conversion |
| SciA11y | Destination/content reconstruction | Not source-preservation testing | No frozen DOCX contracts | Different target representation | Not the same | Accessibility-oriented extraction |
| iTagPDF | Destination PDF tagging | Remediation/tagging, not source fidelity | Not the same | Not the same | Not the same | Automated PDF tagging |
| DAISY conversion benchmark | Conversion fidelity benchmarking | Related, broader conversion context | Different contract scope | Different oracle boundary | Different | Conversion benchmarking |
| DocAccessible and validator work | Destination evaluation | Destination conformance/usability | Not source contracts | Not the same | Not the same | Accessible document evaluation |
| A11yPreserve V4 | Verified DOCX source semantics | Explicit source-to-PDF preservation relation | 13 feature-specific contracts | Accepted PDF evidence + frozen comparator | Yes; unresolved equivalence is retained | Preservation conformance testing |

## Conclusion

The novelty claim survives only as a bounded method contribution: operationalizing accessibility preservation as a source-grounded conformance-testing problem with feature contracts, two real DOCX-to-PDF pipelines, a frozen holdout, calibration, mutation tests, and explicit abstention. The manuscript must avoid first-ever, universal, or product-wide claims.
