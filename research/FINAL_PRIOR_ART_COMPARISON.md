# Final prior-art comparison

This review uses the current project pages and primary/authoritative papers.
The comparison is deliberately conservative: `Unknown` means the source does
not establish the property, not that the property is absent.

| Work | Source format | Destination | Controlled source contracts | Identical frozen inputs across pipelines | Source→destination preservation comparison | Explicit uncertainty | Reusable conformance suite |
|---|---|---|---|---|---|---|---|
| A11yPreserve | DOCX | PDF | Yes; feature-specific JSON contracts bound to frozen hashes | Yes; the same 13 DOCX fixtures are used for both tested pipelines | Yes; source properties are compared against destination structure | Yes; evidence-status overlay and partial-case audit | Yes; contracts, certificates, calibration harness, and adapter protocol |
| DocAccessible research and benchmark | Public PDF corpus | Accessible HTML | No controlled authored-source contracts established on the cited benchmark pages | No paired identical DOCX inputs across converters | Fidelity and markup/destination review, not DOCX source-contract preservation | Yes; source-linked evidence and review layers are described | Benchmark artifact, but not the A11yPreserve DOCX-to-PDF protocol |
| DAISY, *PDF Conversions Put to the Test* | PDF/source documents described by the project | PDF | Not established as A11yPreserve-style machine-readable source contracts | Multiple services are compared, but identical frozen-input protocol is not established here | Yes; conversion fidelity/accessibility criteria | Consensus scoring and criteria are explicit | Benchmark methodology; interface reuse is not established |
| Roig/Ribera accessible office-to-EPUB conversion | Office/WYSIWYG documents | EPUB | Partly; expected accessible structures are compared, but not the present JSON contract schema | Comparative conversion evaluation; exact frozen cross-pipeline input protocol is not established here | Yes; converted structure is compared with ideal/accessibility expectations | Methodological comparison, but not the present evidence-status taxonomy | Evaluation approach, not the present adapter suite |
| SciA11y | Scientific papers, commonly PDF | Accessible HTML | No source-contract preservation protocol | Not a paired multi-converter DOCX experiment | Destination reconstruction/remediation and user evaluation | Evaluation and user-study limitations are explicit | Conversion/remediation system, not a preservation conformance suite |
| iTagPDF | PDF plus visual/content cues | Tagged/accessibility-enhanced PDF | Source-aware cues, but not a frozen DOCX contract corpus | Not an identical DOCX-to-PDF pipeline comparison | Destination tagging/generation, not preservation across an edge | Model/system limitations are reported | Tagging/remediation system, not a converter-preservation suite |
| Kumar et al. PDF accessibility evaluation benchmark | PDF | PDF evaluation labels | No source-document preservation contracts | Not a conversion comparison | Destination-only evaluator benchmarking | Cannot-tell/label uncertainty is explicit | Evaluator benchmark, not a source-to-destination suite |

The defensible boundary is therefore narrow. A11yPreserve does not claim that
accessible conversion has not been studied. Its contribution is the controlled
source-to-destination preservation protocol and empirical benchmark: explicit
source contracts, identical frozen inputs across real pipelines, evidence-aware
equivalence decisions, and reusable provenance artifacts for a specified
DOCX-to-PDF edge.

## Sources

- [DocAccessible research](https://docaccessible.com/research) and [PDF-to-HTML benchmark](https://docaccessible.com/benchmarks/pdf-to-html)
- [DocAccessible Google Docs guide](https://docaccessible.com/guides/google-docs-to-accessible-pdf)
- [DAISY PDF conversions benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/)
- [Kumar et al., PDF accessibility evaluation benchmark](https://doi.org/10.1145/3663547.3746380)
- [SciA11y](https://doi.org/10.1145/3441852.3476545)
- [iTagPDF](https://doi.org/10.1145/3772318.3790289)
- [Roig and Ribera, Interacción 2015 proceedings](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf)
- [Microsoft Word PDF accessibility documentation](https://learn.microsoft.com/en-us/office/pdf/word/wordpdfaccessibility)
