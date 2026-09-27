# Prior-Art Audit

## Bottom line

The broad claim—“a tool/benchmark that tests accessibility after document conversion”—is not novel. The closest peer-reviewed prior art is Roig and Ribera’s office-editor-to-EPUB evaluation, which compared ideal EPUB structures with converted artifacts and reported that accessibility information was often lost. A defensible contribution remains, but only as a narrower, source-grounded differential method with explicit preservation/loss/regeneration/measurement states and reproducible semantic fixtures.

## Relevant work

| Work | What it does | Overlap | Remaining gap |
|---|---|---|---|
| Roig & Ribera, 2015/2016, *Creación de documentos EPUB accesibles...* / *Creación de EPUB accesibles...* | Quantitatively evaluates office/WYSIWYG to EPUB conversions, including headings, images, lists, tables and metadata, with code/visual comparison. | Directly establishes that conversion can lose accessibility semantics. | Does not provide the proposed explicit differential outcome taxonomy, modern cross-format fixture harness, or provenance-aware machine-readable comparator. |
| SciA11y (Wang et al., 2021) | Audits scholarly PDFs and reconstructs accessible HTML; 11,397-PDF sample and BLV user study. | PDF accessibility and PDF→HTML. | Reconstructs/remediates outputs; it is not source-author-intent preservation testing. |
| ASSETS 2024 scholarly-PDF crisis study | Measures tagged PDF, language, tables, tab order and alt text with checkers/manual review. | Output accessibility evaluation. | No controlled source/output differential or conversion provenance. |
| ASSETS 2025 PDF benchmark | 125 PDFs, expert annotations, seven accessibility criteria, evaluator benchmark. | Benchmarking accessibility evaluation. | Tests document state, not semantic preservation across a conversion edge. |
| iTagPDF (CHI 2026) | Uses source pixels/content to predict PDF tags, order, alt text and table/formula structure. | PDF tagging/remediation and destination semantics. | Regenerates destination semantics; does not distinguish regeneration from preservation. |
| DAISY, *PDF Conversions Put to the Test* (2026) | Seven PDF conversion services, four PDFs, 12 fidelity/accessibility criteria. | Very close source-fidelity conversion benchmark; non-peer-reviewed. | Public methodology is not the same as a controlled authored semantic fixture with an explicit provenance taxonomy. |
| DocAccessible benchmark (current project) | Public 50-document PDF→HTML benchmark with text fidelity, visual coverage and human markup review. | Current near-duplicate threat for public conversion benchmarking. | PDF-only, project-owner review, not a controlled multi-format authoring-source experiment. |
| TransPAc | Ontology-driven accessible transformations for PDF forms, validated on 856 forms and a blind-user study. | Representation-aware transformation and user validation. | Form-specific; not general authored-document semantic preservation. |

## Positioning decision

Do not claim “first,” “general conversion accessibility benchmark,” or “PDF→HTML accessibility evaluation.” Claim instead: “a reproducible, source-grounded differential test harness for determining whether accessibility-relevant semantics are preserved, degraded, lost, mutated, regenerated, unsupported, or merely unmeasured across a specified conversion edge.” The paper must cite Roig/Ribera as foundational rather than presenting the problem as newly discovered.

## Sources

- [Roig & Ribera, Interacción 2016 proceedings](https://gredos.usal.es/bitstream/10366/131452/1/978-84-9012-629-5_Interaccion2016_ActasCompletas.pdf)
- [Roig & Ribera, Interacción 2015 proceedings](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf)
- [SciA11y](https://arxiv.org/abs/2105.00076)
- [Scholarly PDF accessibility crisis](https://arxiv.org/abs/2410.03022)
- [iTagPDF](https://peyajm29.github.io/itagpdf.html)
- [DAISY conversion benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/)
- [DocAccessible research](https://docaccessible.com/research)

