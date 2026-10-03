# A11yPreserve Feasibility Pilot

## 1. Research Hypothesis

Provenance-aware comparison between an accessible DOCX source and its converted PDF output may reveal accessibility-semantic preservation failures that destination-only validators cannot identify or explain.

This pilot did not assume the hypothesis was true. It froze a small source corpus, built deterministic source extraction and comparison infrastructure, and attempted the required conversion and validator routes.

## 2. Pilot Scope

The scope was DOCX → PDF and exactly four feature families: headings, image alternative text, lists, and tables. Document language and title were recorded as secondary metadata. No HTML, EPUB, ODT, PowerPoint, spreadsheets, OCR, remediation, visual-fidelity benchmarking, user study, large corpus, or multi-hop conversion was added.

## 3. Environment

The full inventory is in [`pilot/ENVIRONMENT.md`](pilot/ENVIRONMENT.md). The primary tools were bundled Python 3.12.14, python-docx 1.2.0, pypdf 6.10.0, and Pillow 10.3.0. Microsoft Word 16.0.20326.20158, Chrome 153.0.8010.53, and Acrobat 26.2.21931.0 were installed. LibreOffice, PAC, and veraPDF were unavailable.

## 4. Controlled Corpus

- F01_HEADINGS contains the required H1 Research Overview, H2 Background, H3 Prior Work, and H2 Methods hierarchy.
- F02_ALT_TEXT contains a locally generated enrollment bar chart with the exact specified alternative text and non-duplicative surrounding prose.
- F03_LISTS contains separate native unordered, ordered, and nested list structures.
- F04_TABLE contains the specified four-row, three-column table with a native Word repeating/header row marker.

The fixture DOCX files are in [`pilot/fixtures`](pilot/fixtures), and the chart was visually inspected for legibility.

## 5. Ground Truth

The four JSON manifests were authored before conversion attempts and are in [`pilot/manifests`](pilot/manifests). SHA-256 hashes for every DOCX and manifest are in [`pilot/manifests/hashes.json`](pilot/manifests/hashes.json). The verification report confirms all four fixtures matched their manifests. No manifest was changed after a conversion result because no conversion result existed.

## 6. A11yPreserve Prototype

The pilot ASIR is `ASIR-pilot-1`. It represents document title and language, heading text/level/order, figure alternative text and decorative state, list type/depth/text/parent, and table dimensions/cells/header row/header cells. Each object includes OOXML or PDF evidence pointers.

DOCX extraction reads `word/document.xml`, `word/numbering.xml`, `docProps/core.xml`, and relationships directly. It deterministically extracted the intended four headings, one figure, seven list items, and one table.

PDF extraction uses pypdf to inspect `/Root`, `/Lang`, `/Info`, `/StructTreeRoot`, role maps, structure elements, `/Alt`, and marked-content text. A smoke test against the pre-existing tagged `outputs/G01_chrome.pdf` successfully recovered tagged structure, two headings, and two figures. That artifact was not a pilot conversion and is excluded from all result counts.

The comparator uses deterministic exact or structural comparisons and emits only the required classifications: PRESERVED, DEGRADED, LOST, MIS_MAPPED, NOT_REPRESENTABLE, or AMBIGUOUS. Synthetic unit tests passed for PRESERVED, DEGRADED, LOST, and MIS_MAPPED.

## 7. Conversion Methodology

The Word route attempted native `ExportAsFixedFormat` with PDF output, document structure tags, heading bookmarks, document properties, and ISO 19005-1 enabled. Both COM and process launch failed with Windows error `0x80070520`, so zero Word PDFs were produced.

LibreOffice was not installed. Google Docs was reachable in an authenticated Chrome tab, but the available browser surface did not provide a reliable local-file upload operation. No fixture was transmitted to Google and no Google Docs PDF is claimed. Details are in [`pilot/logs/converter_attempts.json`](pilot/logs/converter_attempts.json).

## 8. Validator Methodology

No generated PDF existed to validate. PAC and veraPDF were unavailable. Acrobat was installed but not run after the native session limitation blocked a reliable automated route. Therefore no validator PASS/FAIL result is reported, and no validator result is interpreted as evidence for or against preservation.

## 9. Results

Because all three conversion routes produced zero pilot PDFs, there are no source-to-destination semantic classifications. The table records every required fixture/converter attempt without manufacturing destination values.

| Fixture | Converter | Semantic | Source Value | Destination Value | Classification | Classification Method | PAC Finding | Acrobat Finding | veraPDF Finding |
|---|---|---|---|---|---|---|---|---|---|
| F01_HEADINGS | Word | headings | frozen in source ASIR | no PDF | not run | converter blocked | no report | not run | no report |
| F02_ALT_TEXT | Word | image alt text | frozen in source ASIR | no PDF | not run | converter blocked | no report | not run | no report |
| F03_LISTS | Word | lists | frozen in source ASIR | no PDF | not run | converter blocked | no report | not run | no report |
| F04_TABLE | Word | table structure | frozen in source ASIR | no PDF | not run | converter blocked | no report | not run | no report |
| F01_HEADINGS | LibreOffice | headings | frozen in source ASIR | no PDF | not run | converter unavailable | no report | not run | no report |
| F02_ALT_TEXT | LibreOffice | image alt text | frozen in source ASIR | no PDF | not run | converter unavailable | no report | not run | no report |
| F03_LISTS | LibreOffice | lists | frozen in source ASIR | no PDF | not run | converter unavailable | no report | not run | no report |
| F04_TABLE | LibreOffice | table structure | frozen in source ASIR | no PDF | not run | converter unavailable | no report | not run | no report |
| F01_HEADINGS | Google Docs | headings | frozen in source ASIR | no PDF | not run | upload route unavailable | no report | not run | no report |
| F02_ALT_TEXT | Google Docs | image alt text | frozen in source ASIR | no PDF | not run | upload route unavailable | no report | not run | no report |
| F03_LISTS | Google Docs | lists | frozen in source ASIR | no PDF | not run | upload route unavailable | no report | not run | no report |
| F04_TABLE | Google Docs | table structure | frozen in source ASIR | no PDF | not run | upload route unavailable | no report | not run | no report |

Semantic retention rate is **not estimable**, not zero: there are no applicable converted semantics in the denominator. Preservation-Blind Failure Count is **not estimable** and no verified preservation failure was observed. These are missing-evidence states, not negative empirical results.

## 10. Preservation Failures

None were observed because no converter produced a pilot PDF. No synthetic comparator mutations are counted as empirical converter failures.

## 11. Provenance-Dependent Findings

No provenance-dependent preservation failure can be claimed from this run. The prototype is capable of comparing source and destination objects, but the required destination evidence was not generated.

## 12. Converter Differences

No converter comparison was possible. The attempted Word route was blocked by the Windows session error; LibreOffice was absent; Google Docs could not be given a fixture through the available upload surface.

## 13. Validator Comparison

No validator comparison was possible. In particular, the pilot does not claim that any output-only validator would or would not expose a source-to-destination failure.

## 14. Ambiguous Cases

There are no empirical AMBIGUOUS classifications. The unexecuted conversion rows are marked `not run`, not `AMBIGUOUS`, because no destination evidence exists.

## 15. Automation

Fixture creation, manifest freezing, hashing, source extraction, comparison tests, environment inspection, and conversion attempts were automated. No repetitive manual validation was assigned to the user. The complete automation record is in [`pilot/AUTOMATION_LOG.md`](pilot/AUTOMATION_LOG.md).

## 16. Technical Problems

The principal blocker was Windows error `0x80070520` when launching or automating Word. LibreOffice, PAC, and veraPDF were unavailable. The document-skill renderer also could not render the DOCX files because no bundled or system LibreOffice executable was present. The authenticated Google Docs page was reachable, but the current browser connector did not expose a reliable local-file upload operation. These limitations prevented the empirical conversion stage.

## 17. Threats to Validity

The intended study has a small sample size and synthetic fixtures. Converter configuration can change preservation behavior. PDF extraction can miss semantics if a library does not expose a vendor-specific structure representation. Model-assisted adjudication was not needed here, but it would introduce another source of variance in a larger study. Destination validators have different scopes and profiles. DOCX-to-PDF mappings are format-specific and should not be generalized to other transformations.

This run adds a more immediate validity threat: the conversion and validator stages were not executable in the current environment. The source-side feasibility result must not be presented as evidence of converter behavior.

## 18. Research Assessment

- Does provenance provide information unavailable from output-only checking? **Unanswered empirically.** The prototype encodes the required comparison, but no pilot PDF was available.
- Do converter preservation differences exist? **Unanswered.** No converter output was produced.
- Can semantics be mapped reproducibly? **Yes for the frozen DOCX source fixtures; partially demonstrated for PDF structure through a separate smoke test.**
- How much analysis was deterministic? **All completed source extraction and synthetic comparison testing was deterministic.** No empirical destination classification was made.
- Did the method require excessive AI judgment? **No.** No model adjudication was needed.
- Are observed failures meaningful rather than trivial? **No observed conversion failures.** The pilot cannot assess this criterion.

The harness is technically feasible, but the research hypothesis remains untested. The problem is not strong enough to justify a full paper-scale study based on this run.

## 19. Recommendation

**PIVOT**

The next small experiment should keep the four frozen fixtures and ASIR, but run in an environment with at least two executable DOCX→PDF engines and one structural PDF validator. Before expanding the corpus, reproduce one complete fixture through two engines, verify the PDF structure adapter against independent object-level evidence, and require at least one observed converter difference or checker-clean provenance-dependent failure. Do not build the full paper project until that gate is met.

