# Final Prior-Art Check

## Search scope

Focused searches covered accessibility preservation in document conversion, DOCX-to-PDF accessibility, source-grounded comparison, accessibility differential testing, tagged-PDF conversion, and accessible document transformation. Current official/authoritative pages were checked for DAISY, DocAccessible, Microsoft Word PDF accessibility documentation, and the Kumar et al. benchmark.

## Findings

| Work | What it contributes | Overlap | Remaining difference |
|---|---|---|---|
| Roig/Ribera | Office-document conversion to accessible EPUB | Accessibility effects of transformation | Different source/destination and instrumentation; not the frozen DOCX-to-PDF benchmark here |
| SciA11y | PDF to accessible HTML conversion | Accessibility-aware representation generation | Remediation/generation rather than preservation of known DOCX properties |
| iTagPDF | Source-aware PDF tagging/remediation | Uses source/document cues | Improves a PDF rather than comparing an identical known source across converters |
| Kumar et al. | Benchmark of PDF accessibility evaluation systems | Structured destination criteria and benchmarking | Evaluator accuracy, not source-to-destination preservation |
| DAISY AI SIG 2026 | Seven-service PDF-to-accessible-document benchmark | Shared quality framework and source checking | PDF input, accessible-document output, consensus quality scoring; not DOCX source semantics |
| DocAccessible current benchmark | Source-linked PDF-to-HTML fidelity corpus | Hashes, source evidence, fidelity review | PDF-to-HTML corpus and fidelity workflow; not the 13-feature DOCX-to-PDF preservation question |
| Microsoft Word documentation | Describes tagged PDF export and structure | Official export semantics | Product documentation, not an independent comparative benchmark |

## Conclusion

No focused result located a study that subsumes the exact combination of verified native DOCX accessibility ground truth, identical frozen sources, real DOCX-to-PDF pipelines, destination structure extraction, and feature-level preservation classification. This supports a defensible but deliberately narrow novelty position. The manuscript does not use “first” or “unique.”

Sources checked include [DAISY's 2026 conversion benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/), [DocAccessible's benchmark corpus](https://docaccessible.com/benchmarks/pdf-to-html), [DocAccessible's current export guide](https://docaccessible.com/guides/which-apps-export-tagged-pdfs), [Microsoft's Word PDF accessibility documentation](https://learn.microsoft.com/en-us/office/pdf/word/wordpdfaccessibility), and the [Kumar et al. PDF accessibility-evaluation benchmark](https://doi.org/10.1145/3663547.3746380).
