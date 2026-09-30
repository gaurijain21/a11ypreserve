# DECISION: GO

## 1. Executive decision

Proceed with A11yPreserve. Pilot 3 produced four real Google Docs DOCX→PDF outputs and reused four unchanged, verified LibreOffice baseline PDFs. Source-grounded comparison produced reproducible, feature-specific differences across two conversion routes. The methodology is feasible and should be scaled carefully.

This is a feasibility decision, not a claim that either converter is universally superior or that these four fixtures establish general accessibility performance.

## 2. Input integrity

PASS. All four frozen DOCX fixtures matched the existing SHA-256 manifest, including filenames, sizes, and hashes. No fixture or frozen manifest was modified.

Evidence: `pilot3/FROZEN_INPUT_VERIFICATION.md` and `pilot3/FROZEN_INPUT_VERIFICATION.json`.

## 3. Conversion engines

- LibreOffice `26.2.6.3`: Pilot 2 headless PDF outputs were reused as the frozen baseline; no conversion was rerun.
- Google Docs: authenticated Google Docs web workflow in Chrome on Windows, using Upload/Open, then File → Download → PDF Document (.pdf). No print-to-PDF path was used.
- Microsoft Word: native `WINWORD.EXE` was found at `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE`, version `16.0.20326.20158`, but Word conversion was deferred in this focused Pilot 3 scope. The earlier Pilot 2 Word absence remains an infrastructure limitation, not a semantic result.

Exact workflow and per-output hashes are in `pilot3/AUTOMATION_LOG.md`.

## 4. Successful conversions

- LibreOffice baseline: 4/4 verified and analyzable.
- Google Docs: 4/4 produced, parseable, one page each, non-empty, and with a PDF structure tree.
- Pilot 3 target achieved: 8 analyzable PDFs across two real conversion routes.

## 5. Failed conversions

No Google Docs or LibreOffice conversion failed in Pilot 3. The Word path was deferred rather than counted as a Pilot 3 semantic result. A recoverable browser automation error occurred when a broad iframe selector matched multiple picker frames; using the exact picker frame completed F02 successfully.

## 6. Semantic results

| Fixture | Feature | LibreOffice fidelity | Google Docs fidelity | LibreOffice accessibility | Google Docs accessibility |
|---|---|---|---|---|---|
| F01 | heading hierarchy | SEMANTICALLY_EQUIVALENT | PARTIAL_PRESERVATION | ACCESSIBLE_EQUIVALENT | ACCESSIBLE_BUT_ALTERED |
| F02 | image alternative text | MUTATED | EXACT_PRESERVATION | ACCESSIBLE_BUT_ALTERED | ACCESSIBLE_EQUIVALENT |
| F03 | list structure | SEMANTICALLY_EQUIVALENT | PARTIAL_PRESERVATION | ACCESSIBLE_EQUIVALENT | DEGRADED_ACCESSIBILITY |
| F04 | table structure | SEMANTICALLY_EQUIVALENT | SEMANTICALLY_EQUIVALENT | ACCESSIBLE_EQUIVALENT | ACCESSIBLE_EQUIVALENT |

Raw records, destination representations, evidence paths, and confidence values are in `pilot3/reports/semantic_diff_results.json`.

## 7. Strongest confirmed preservation

Google Docs preserved the F02 author-written image alternative text exactly in the PDF `/Alt` entry. Both converters also produced F04 `Table`/`TR`/`TH`/`TD` structure with four rows, three header cells, nine data cells, and independently verified source cell text.

## 8. Strongest confirmed loss/degradation

Google Docs emitted the F03 list and nested-list roles but no explicit `/ListNumbering` attributes. Because visual bullets and numerals are not semantic proof, ordered-versus-unordered preservation could not be established from the PDF structure alone. This is reported as PARTIAL_PRESERVATION / DEGRADED_ACCESSIBILITY, not silently promoted to preservation.

LibreOffice changed the F02 `/Alt` value by adding `Enrollment chart - ` before the source text. The destination remains meaningful, so the refined classification is MUTATED / ACCESSIBLE_BUT_ALTERED rather than LOST.

## 9. Cross-converter differences

The behavior is feature-specific. Google Docs was stronger on exact alt-text fidelity. LibreOffice was stronger on explicit list-type evidence. Google Docs added an extra H1 title before the F01 source heading sequence; LibreOffice did not. Neither converter is declared the overall winner.

Details are in `pilot3/CROSS_CONVERTER_RESULTS.md` and `pilot3/F02_CLASSIFICATION_REFINEMENT.md`.

## 10. Comparator validity

PASS. The existing ASIR extractor and comparator tests remained green. The legacy comparator executed against all eight real PDFs. Pilot 3 added a narrow two-axis analysis layer so that preservation fidelity and destination accessibility are not collapsed into one coarse label. Frozen source truth and Pilot 2 reports were not changed.

## 11. Measurement failures

- PDF text extraction inserts layout whitespace and occasional glyph-run spaces; the analyzer uses a whitespace-tolerant independent text check and retains the raw extracted text as evidence.
- Google Docs list type is structurally ambiguous because `/ListNumbering` is absent. This is an unresolved destination representation limit, not assumed converter loss.
- Google Docs adds an H1 role for the document title in F01; the source four-heading sequence remains present afterward, so the result is reported as partial/altered.
- PAC, Acrobat, and veraPDF were not available as installed secondary validators. `pdfplumber` independently confirmed page count and non-empty content for all eight outputs; pypdf object-model traversal remained the primary structural evidence.
- Microsoft Word was not attempted in Pilot 3; its prior missing-output state is kept separate from semantic classifications.

## 12. Research signal

PRESENT. The source-grounded differential method reveals distinctions that a generic tagged-PDF presence check would miss: exact versus mutated alt text, an extra heading role, and missing explicit list-type evidence. The same source semantics were compared against two independent conversion routes.

## 13. What this pilot DOES prove

- Frozen source semantics can be verified and reused without regenerating fixtures.
- Real DOCX→PDF outputs from Google Docs and LibreOffice can be structurally parsed and compared.
- The ASIR/comparator approach produces reproducible, feature-level preservation signals across converters.
- A two-axis taxonomy is more informative than a single “accessible/inaccessible” label for at least these features.

## 14. What this pilot DOES NOT prove

- It does not prove universal accessibility of either converter.
- It does not establish performance across Word, other document families, complex layouts, or additional PDF consumers.
- It does not prove that Google Docs list semantics are absent in every export; it proves that these PDFs did not expose explicit `/ListNumbering` evidence under the inspected structure.
- It does not replace standards conformance testing or human/assistive-technology evaluation.

## 15. Full-paper implications

A scaled study is plausible and potentially publishable if it preserves this design: frozen source ground truth, multiple real converters, independent destination extraction, raw evidence retention, and separate fidelity/accessibility axes. The contribution should remain differential semantic preservation, not ordinary validator scoring.

## 16. Next experiment

Do not start the full experiment yet. First expand the same controlled protocol with ranked feature families: complex nested lists, table header scope and associations, figure captions/long descriptions, document language, links/bookmarks, reading order, footnotes, and forms. Add Word native export when its environment path is reproducible, then repeat across more than one document family.

## 17. Final decision

GO

The next study should scale the source-grounded semantic comparison while retaining explicit scope limits and measurement-error classifications.
