# DECISION: GO

# FULL EXPERIMENT RESULTS

## 1. Executive decision

The frozen 13-fixture benchmark produced 26 real DOCX→PDF outputs: 13 through LibreOffice and 13 through authenticated Google Docs export. All 26 PDFs were parseable, non-empty, one page, and structurally tagged. Source and destination semantics were independently extracted and compared. The evidence supports proceeding to the planned full study, without ranking converters overall.

## 2. Input integrity

The 13 frozen DOCX hashes matched `corpus/FROZEN_CORPUS_MANIFEST.json`; the verification report records exact paths, sizes, hashes, and timestamp. No fixture was regenerated or modified.

## 3. Conversion engines

- LibreOffice 26.2.6.3, native headless `writer_pdf_Export`, tagged-PDF settings enabled.
- Google Docs authenticated web export, exact frozen DOCX uploaded through the UI and exported via File → Download → PDF Document; PDF producer observed as `Skia/PDF m156`.
- Microsoft Word was not included because the previously documented COM/environment issue remains unresolved; this is not a semantic result.

## 4. Successful conversions

- LibreOffice: 13/13
- Google Docs: 13/13
- Total: 26/26 valid primary outputs

## 5. Failed conversions

No primary conversion failed. One Google Docs picker-load retry was required for F06; it was an automation transient, not an output result.

## 6. Semantic results

See `results/full_experiment/FULL_RESULTS_BY_FEATURE.md` and raw `reports/a11ydiff_results.json`. Key feature-level observations include: LibreOffice preserved headings, list numbering, simple tables, document language, inline language, document title, complex-table scope/span evidence, math `/Formula`, and caption `/Caption` structure; it altered F02 alt text and did not establish an explicit decorative Artifact for F07. Google Docs preserved F02 alt text, F04 simple table structure, and F07 meaningful/decorative image count/state only partially because explicit decorative representation was not established; it partially preserved F01 headings, F03 list structure without explicit list type, F10 complex header roles without scope, F12 equation as visible text, and F14 caption text by adjacency.

## 7. Strongest confirmed preservation

The strongest cases are direct structure-level matches: Google Docs F02 preserved the author-written `/Figure /Alt` string exactly; LibreOffice F03 exposed `/L`, `/LI`, `/LBody`, and `/ListNumbering` matching the source’s ordered/unordered and nested-list contract; LibreOffice F10 exposed five `/TH` cells with scope and span evidence matching the two-level header contract; LibreOffice F12 exposed a `/Formula` structure with the retained visible expression.

## 8. Strongest confirmed loss/degradation

Google Docs F06 lost the source inline `es-MX` language span while retaining only the document-level language. Google Docs F10 retained table/header roles but no `/Scope` evidence for the multi-level header associations. Google Docs F03 retained list items/nesting but no explicit ordered/unordered representation. These are source-grounded fidelity results, not claims that the entire PDFs are inaccessible.

## 9. Cross-converter differences

Feature-level differences are documented in `CROSS_CONVERTER_DIFFERENCES.md`. Shared outcomes are documented in `CROSS_CONVERTER_AGREEMENTS.md`. No overall converter winner is reported.

## 10. Comparator validity

`a11ydiff` ran for all 26 pairs. The comparator produced raw source/destination values, two-axis fidelity/accessibility labels, evidence paths, source/output hashes, and notes. Regression tests passed.

## 11. Measurement failures

LibreOffice F11 exposed a PDF `/Note` structure, but the current marked-content extractor did not recover note-body text well enough to verify reference/body association; it is therefore `MEASUREMENT_ERROR`, not `LOST`. Link visible-name association, decorative Artifact state, some caption associations, and token-level math text remain bounded by PDF producer representation and extractor coverage. These limitations are retained rather than converted into converter-loss claims.

## 12. Research signal

PRESENT. The same source-grounded method produced feature-specific preservation, partial preservation, alteration, loss, and measurement-error outcomes across two real conversion engines. The results are not reducible to a destination-only accessibility verdict.

## 13. What this pilot DOES prove

It proves feasibility of a controlled, frozen DOCX corpus; deterministic OOXML ground truth; real tagged PDF production by two engines; structural destination inspection; provenance-traceable comparison; and meaningful converter/feature-specific differences.

## 14. What this pilot DOES NOT prove

It does not prove universal behavior across software versions, documents, operating systems, validators, or users. It does not rank LibreOffice or Google Docs overall, and it does not establish Microsoft Word behavior.

## 15. Full-paper implications

Scaling the frozen contracts with justified variants, integrated documents, additional converter versions, and validator comparison is likely to support a publishable empirical study. Feature-level reporting and explicit measurement-error handling should remain central.

## 16. Next experiment

Run the planned larger matrix only after selecting justified feature instances and recording converter/version settings. Add Word only if its native export becomes reproducibly executable; otherwise keep it explicitly out of the denominator.

## 17. Final decision

GO
