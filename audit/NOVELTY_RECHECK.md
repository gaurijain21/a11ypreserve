# Focused Novelty Recheck

## Findings

- Roig/Ribera's office-to-EPUB work evaluates accessibility and reports that office-document conversion did not preserve accessibility information reliably. It is adjacent prior art, but it does not implement this project's DOCX-source/real-PDF destination semantic differential with frozen machine-readable source contracts.
- SciA11y studies PDF-to-HTML reconstruction, large-scale PDF accessibility, extraction quality, and BLV user needs. It is a destination reconstruction/user-centered contribution, not the same source-grounded DOCX→PDF preservation question.
- DAISY's 2026 “PDF Conversions Put to the Test” benchmarks PDF-to-accessible-document services and explicitly raises fidelity/editorialization concerns. It is the closest recent practical benchmark overlap and means A11yPreserve must position itself as a complementary source-grounded DOCX→PDF semantic-preservation benchmark, not as the first accessibility-conversion benchmark.
- iTagPDF targets automated PDF tagging from rendered/input documents and evaluates tagging/reading order/content metadata. It improves destination accessibility but does not, by itself, compare author-provided source semantics against conversion output across office pipelines.
- DocAccessible's current research/benchmark materials explicitly discuss faithful accessible HTML conversion and link-integrity benchmarking. This is a meaningful adjacent overlap; the defensible gap is narrower: controlled native DOCX accessibility ground truth, real DOCX→PDF pipelines, two-dimensional preservation-vs-destination accessibility labels, and provenance-traceable differential records.
- Current vendor documentation confirms that Word's accessible PDF workflow depends on structure tags, Google Docs officially supports File → Download with a selected file type, LibreOffice documents PDF/UA/tagged export, and Adobe frames accessibility checking as standards conformance. These sources support method documentation, not novelty claims.

## Positioning conclusion

The gap remains defensible only if claimed narrowly: a source-grounded method for measuring whether known author accessibility semantics survive a specific document-conversion pipeline. The project should not claim to be the first accessibility conversion benchmark, first PDF tagging system, or first document accessibility evaluation.

## Sources

- [Roig/Ribera office-to-EPUB study](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf)
- [SciA11y paper](https://arxiv.org/abs/2105.00076)
- [DAISY PDF Conversions Put to the Test](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/)
- [iTagPDF](https://doi.org/10.1145/3772318.3790289)
- [DocAccessible research](https://docaccessible.com/research)
- [Microsoft accessible PDFs guidance](https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs)
- [Google Docs download guidance](https://support.google.com/docs/answer/49114?hl=en_na&ref_topic=9045929)
- [LibreOffice PDF/UA export](https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_universal_accessibility.html?DbPAR=BASE&System=WIN)
- [Adobe PDF accessibility verification](https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html)
