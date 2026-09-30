# Prior-Art Repair

## Review date and scope

Focused review completed 2026-09-28 using primary or authoritative sources requested for this audit. The review covered source-grounded document conversion, PDF accessibility benchmarking, destination-only evaluation, PDF-to-HTML reconstruction, remediation/tagging, and vendor export documentation.

## Findings and positioning

| Work | What it studies | Boundary from A11yPreserve |
|---|---|---|
| Roig and Ribera (2015) | Office-document conversion to EPUB and accessibility preservation | Different destination and instrumentation; establishes that accessibility effects of conversion are prior work. |
| SciA11y (ASSETS 2021) | PDF-to-accessible-HTML reconstruction for scientific papers and BLV-oriented navigation | Destination generation/remediation from PDF, not DOCX source-contract preservation across office pipelines. |
| iTagPDF (CHI 2026) | Source-aware automated PDF tagging, reading order, and content-specific metadata | Improves destination PDF metadata; does not serve as the frozen source-to-destination preservation benchmark here. |
| Kumar et al. (ASSETS 2025) | Benchmarking automated and LLM-based PDF accessibility evaluation | Evaluates evaluator accuracy on destination PDFs, not whether known source properties survive conversion. |
| DAISY AI SIG (2026) | Seven-service PDF-to-accessible-document benchmark with 12 criteria and consensus scoring | PDF input and accessible-document output; not native DOCX ground truth followed by DOCX-to-PDF differential comparison. |
| DocAccessible (2026) | Public 50-document PDF-to-HTML fidelity benchmark and current Google Docs export guidance | Closest practical overlap in source-grounded fidelity and evidence, but different PDF-to-HTML direction and corpus; the Google guide is product guidance, not an independent comparative study. |
| Microsoft Word PDF Accessibility | Product documentation mapping Word constructs to PDF tags/artifacts | Format and representability context only; Word is excluded from the frozen denominator. |

## Repaired novelty statement

A11yPreserve is a controlled, source-grounded DOCX-to-PDF preservation benchmark that begins with explicitly verified source accessibility properties, runs identical frozen sources through multiple real conversion pipelines, and compares destination structure against source contracts. The contribution is the controlled source-to-destination preservation protocol and empirical benchmark.

The paper does not claim to be the first or unique accessibility-conversion study, does not claim that no prior work studied preservation, and does not conflate this work with PDF accessibility benchmarking, destination-only evaluation, remediation, PDF-to-HTML conversion, accessible document generation, or user studies.

## Sources inspected

- https://docaccessible.com/research
- https://docaccessible.com/benchmarks/pdf-to-html
- https://docaccessible.com/guides/google-docs-to-accessible-pdf
- https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/
- https://doi.org/10.1145/3663547.3746380
- https://doi.org/10.1145/3441852.3476545
- https://doi.org/10.1145/3772318.3790289
- https://learn.microsoft.com/en-us/office/pdf/word/wordpdfaccessibility
- https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf
