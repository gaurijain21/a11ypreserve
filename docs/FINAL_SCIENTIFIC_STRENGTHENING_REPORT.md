# 1. Final recommendation

**STRONGER — READY FOR SUBMISSION**

The highest-value issues were addressed without rewriting the frozen experiment. Four unresolved hyperlink rows are now supported by an independent deterministic geometry/text audit, the remaining abstentions are characterized rather than forced, the testing contribution is grounded in oracle and transformation-testing literature, and a six-document interaction source corpus is available with passing source contracts. Microsoft Word was tested and honestly excluded after a reproducible COM-session blocker. The new interaction sources were not converted because this environment had no LibreOffice executable and browser automation was unavailable; the existing three-document integrated conversion arm remains the conversion-based coexistence evidence.

# 2. Frozen baseline

- Protected commit at start: `7043a2164dce6ef162aeed7655d90c3e92bbbb68`, branch `master`.
- Manuscript before the final documentation repair: SHA-256 `E720EB8EB58898F592491E7BB67DB739E09BA1D670E222350E2465B5C435199D`.
- Artifact ZIP before the final documentation repair: SHA-256 `EE599CC68956390D3A608AFC1D80AF016CF3680A86F3E9137C1BB14202DD2E62`.
- The current manuscript and reviewer ZIP hashes are recorded in `submission/CANONICAL_SUBMISSION.md`. The ZIP was repackaged only to carry the repaired reviewer README; frozen evidence and result rows were unchanged.
- Frozen atomic experiment: 52 rows from 26 fixtures, with 18 `VERIFIED_PRESERVED`, 4 `OBSERVED_PARTIAL`, 7 `ALTERED`, 4 `CONFIRMED_LOST`, 18 `UNRESOLVED_EQUIVALENCE`, and 1 `MEASUREMENT_ERROR`.
- Google repeatability arm: 39 outputs, byte-identical within the recorded environment, with stable classifications.
- Existing integrated coexistence arm: three project-generated documents and 42 property-pipeline observations, kept separate from the 52-row denominator.
- Baseline verifier after the pass: PASS; 52 rows checked and no failures.

The complete starting snapshot is in `docs/SCIENTIFIC_STRENGTHENING_BASELINE.md`. Existing Core/Variant B fixtures, converted outputs, hashes, provenance, and canonical result rows were not rewritten.

# 3. Unresolved-case analysis

The frozen count was 18/52 (34.6%). The additive analysis leaves 14/52 (26.9%) unresolved and identifies four cases that can be resolved with a stricter independent evidence path:

- F08/LibreOffice and F08/Google Docs: one exact URI and visible-span match each.
- B08/LibreOffice and B08/Google Docs: two exact URI and visible-span matches per case.

The four cases are not silently changed in the frozen result file. The new `scientific_strengthening/unresolved_analysis/link_association_audit.py` uses PyMuPDF annotations and page-word geometry, requiring exact normalized source text and target matches. Its output is deterministic and bounded to the hyperlink contract.

Remaining primary reasons, using one mutually exclusive primary reason per row, are:

| Primary reason | Rows |
|---|---:|
| Target-format representability ambiguity | 11 |
| Semantic-equivalence ambiguity | 2 |
| Extraction incompleteness / measurement limitation | 1 |

The 14 remaining rows are the list, B04 table, complex-table, B11 footnote, equation, and caption cases documented row-by-row in `docs/UNRESOLVED_CASE_ANALYSIS.md`. They remain abstentions because the missing evidence is a semantic association or expression identity, not merely a missing tag count. The original extractor and comparator were not edited, so the existing 17-case comparator suite remains unchanged and passes when run with its required source path.

# 4. Microsoft Word pipeline

Microsoft Word is installed, but the feasibility pilot is **NO-GO**. Current PowerShell COM activation, prior native COM export, and the earlier Python attempt all stop before conversion with `0x80070520: A specified logon session does not exist`. The current representative pilot generated zero PDFs and no Word result rows. The full corpus was not attempted. Details and the exact method are in `docs/WORD_PIPELINE_FEASIBILITY.md`.

This is a pipeline-scope limitation, not evidence about Word's accessibility behavior. The paper remains correctly scoped to the two completed conditions.

# 5. Interaction corpus

Six additive fixtures were created under `scientific_strengthening/interaction_corpus/sources/`:

| Fixture | Combined semantics |
|---|---|
| IC01 | headings, hyperlinks, document language, inline language |
| IC02 | heading hierarchy, nested ordered/list structure, inline language |
| IC03 | headings, informative alternative text, captions, hyperlinks |
| IC04 | headings, table headers, nested lists |
| IC05 | headings, footnote association, hyperlinks |
| IC06 | multi-section hierarchy, lists, table headers, alternative text, captions, inline language, hyperlinks |

All 25 explicit source-contract assertions pass. These are controlled coexistence inputs, not randomly sampled real documents and not concatenated copies of the Core fixtures.

No new converter outputs were created for these six files: LibreOffice is not installed in the current environment, and the browser-automation helper failed during initialization. The existing integrated study remains the available conversion-based interaction evidence: three multi-feature documents, both recorded pipelines, and 42 separate observations. The new source corpus therefore strengthens test-input construction and oracle coverage, but it is not presented as new converter evidence.

# 6. Real-world sanity set

Not attempted. No clean set of 3–5 publicly distributable DOCX files with verifiable source accessibility semantics and artifact-compatible provenance was established during this pass. Adding files with uncertain author intent or licensing would weaken, rather than strengthen, the source-oracle argument. The paper continues to distinguish controlled diagnostic validity from external validity.

# 7. Testing-literature strengthening

The manuscript now explicitly positions A11yPreserve against:

- Barr et al., “The Oracle Problem in Software Testing: A Survey,” IEEE TSE 2015, DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785): the source contract is a specification-derived feature oracle, while cross-format representability makes the decision difficult.
- Segura et al., “A Survey on Metamorphic Testing,” IEEE TSE 2016, DOI [10.1109/TSE.2016.2532875](https://doi.org/10.1109/TSE.2016.2532875): metamorphic testing is acknowledged as a neighboring oracle strategy, not claimed as the method used here.
- Sperberg-McQueen, “What Constitutes Successful Format Conversion?”, IJDC 2011, DOI [10.2218/ijdc.v6i1.179](https://doi.org/10.2218/ijdc.v6i1.179): conversion success requires an explicit preservation notion, not only syntactic validity.
- Roig and Ribera, office-document-to-EPUB accessibility conversion, 2015, DOI [10.1145/2829875.2829926](https://doi.org/10.1145/2829875.2829926): closest direct transformation precedent, with a different target format and no demonstrated A11yPreserve-style DOCX-to-tagged-PDF oracle protocol.
- Kumar, Padath, and Wang, PDF accessibility-evaluation benchmark, ASSETS 2025, DOI [10.1145/3663547.3746380](https://doi.org/10.1145/3663547.3746380): destination-evaluation benchmark rather than source-contract preservation testing.
- DAISY AI SIG, “PDF Conversions Put to the Test,” 2026: strong contemporary conversion benchmark context, but opposite conversion direction and consensus scoring rather than DOCX source contracts.

The manuscript now states the narrow claim: A11yPreserve applies specification-derived contracts, evidence-aware cross-format comparison, and explicit abstention to DOCX-to-tagged-PDF pipeline testing. It does not claim to invent test oracles, differential testing, conversion evaluation, or accessibility validation.

# 8. Baseline comparison

An inexpensive structural-presence baseline was run against all frozen 52 destination extractions. It asks only whether a feature-shaped destination node is present and ignores source values, associations, order, and equivalence.

| Presence-only result / A11yPreserve result | Rows |
|---|---:|
| `PRESENT` / `VERIFIED_PRESERVED` | 18 |
| `PRESENT` / `OBSERVED_PARTIAL` | 4 |
| `PRESENT` / `ALTERED` | 7 |
| `PRESENT` / `MEASUREMENT_ERROR` | 1 |
| `PRESENT` / `UNRESOLVED_EQUIVALENCE` | 16 |
| `ABSENT` / `CONFIRMED_LOST` | 4 |
| `ABSENT` / `UNRESOLVED_EQUIVALENCE` | 2 |

The result supports, without declaring either method “wrong,” that destination presence alone cannot establish source-semantic preservation: 16 frozen abstentions contain a feature-shaped destination structure. The baseline is therefore useful as a contrast, not a replacement validator or a new primary classification.

# 9. Test adequacy

The final adequacy claim is feature-oriented and bounded, not exhaustive.

| Feature family | Core | Variant B | New interaction source coverage | Converter coverage | Frozen unresolved / measurement boundary |
|---|---|---|---|---|---|
| Headings | 2 pipeline rows | 2 pipeline rows | IC01, IC02, IC03, IC04, IC05, IC06 | LibreOffice + Google | no unresolved; heading-level evidence is feature-specific |
| Alternative text | 2 pipeline rows | 2 pipeline rows | IC03, IC06 | LibreOffice + Google | value changes can be altered without implying usability harm |
| Lists / nesting | 2 pipeline rows | 2 pipeline rows | IC02, IC04, IC06 | LibreOffice + Google | 3 unresolved atomic rows; item/type mapping remains incomplete |
| Tables / headers | 2 pipeline rows | 2 pipeline rows | IC04, IC06 | LibreOffice + Google | B04 has 2 unresolved rows; cell correspondence is incomplete |
| Complex multi-level tables | 2 pipeline rows | 2 pipeline rows | none | LibreOffice + Google | 3 unresolved rows; full header association is not established |
| Document language | 2 pipeline rows | 2 pipeline rows | IC01, IC02, IC06 | LibreOffice + Google | value specificity can be altered |
| Inline language | 2 pipeline rows | 2 pipeline rows | IC01, IC02, IC06 | LibreOffice + Google | confirmed loss is limited to the tested Google condition |
| Decorative image state | 2 pipeline rows | 2 pipeline rows | none | LibreOffice + Google | state/Artifact representability is limited |
| Hyperlinks | 2 pipeline rows | 2 pipeline rows | IC01, IC03, IC05, IC06 | LibreOffice + Google | 4 frozen unresolved rows are additively resolved by geometry; frozen file unchanged |
| Document title / metadata | 2 pipeline rows | 2 pipeline rows | source title in all six | LibreOffice + Google | metadata is not a complete accessibility judgment |
| Footnote association | 2 pipeline rows | 2 pipeline rows | IC05 | LibreOffice + Google | 1 unresolved plus one measurement error and confirmed Google losses |
| Equations | 2 pipeline rows | 2 pipeline rows | none | LibreOffice + Google | 3 unresolved rows; expression identity is not established |
| Captions | 2 pipeline rows | 2 pipeline rows | IC03, IC06 | LibreOffice + Google | 2 unresolved rows; text adjacency is weaker than association |

This matrix documents test-input and comparator coverage, not standards coverage, fault coverage, prevalence, or a mutation score.

# 10. Updated scientific findings

## Findings already present in the frozen baseline

- Conversion outcomes are feature- and pipeline-specific.
- Inline-language and footnote association losses were confirmed only for the tested Google condition.
- The evidence-aware taxonomy separates observed change, loss, uncertainty, and measurement failure.
- Google repeatability was stable within the recorded environment.
- The three-document integrated arm showed that the protocol can be applied when features coexist.

## Genuinely new findings

- Four hyperlink abstentions are determinately resolvable with independent PDF annotation geometry plus visible-word evidence; the original frozen rows remain unchanged.
- The remaining 14 unresolved rows are concentrated in representability and association problems, not indiscriminate extractor failure.
- The presence-only baseline would accept 16 rows that A11yPreserve correctly leaves unresolved, demonstrating the value of source contracts and equivalence-aware comparison.
- Six additional controlled interaction inputs pass 25/25 source-contract checks, but they do not add converter observations in this environment.
- Microsoft Word could not enter the study because the deterministic automation boundary was blocked before conversion.

# 11. Remaining vulnerabilities

1. The primary evidence still covers only two completed pipelines; Word remains unavailable and Google is cloud-versioned with a documented route deviation for Variant B.
2. The corpus is purposive and controlled, not representative; the new interaction corpus improves coexistence coverage but has no new converted outputs.
3. Fourteen primary rows remain unresolved because cross-format semantic equivalence is not established for list items, table associations, notes, equations, or captions.
4. The source contracts are independently checked but were not adjudicated by an external expert panel or disabled users.
5. The work measures machine-verifiable accessibility semantics, not screen-reader behavior, task success, perceived accessibility, or user harm.

These are genuine scope limits. They are not repaired by relabeling or by collapsing abstentions into losses.

# 12. Exact changes recommended for the paper

Completed in the manuscript and rebuilt PDF:

- cite and position the test-oracle, metamorphic-testing, and format-conversion foundations;
- explicitly define the source contract as a specification-derived cross-format oracle;
- state that abstention is an oracle decision under insufficient representability evidence;
- remove reviewer-facing V2/V3 development labels from the manuscript and use atomic/main/Variant B terminology;
- preserve the existing bounded claims and frozen 52-row numbers.

No paper change should add unconverted interaction fixtures or the Word pilot to the empirical denominator. No paper change should replace the frozen 18 unresolved labels with the four-row additive hyperlink audit; that audit belongs as derived evidence unless the authors deliberately freeze a new result file and update all provenance.

# 13. Final novelty statement

A11yPreserve's narrow defensible contribution is a contract-based testing protocol for measuring whether explicitly verified accessibility semantics in DOCX survive conversion into tagged PDF representations across named real pipelines. Its distinctive methodological combination is cross-format semantic comparison with evidence-aware equivalence and explicit abstention, accompanied by a controlled fixture/test harness; it is not a new general theory of test oracles or accessibility validation.

# 14. ICST fit

The work constitutes software-testing research because its primary unit is a fixture–pipeline test case: controlled DOCX files are test inputs, conversion pipelines are systems under test, source contracts are specification-derived oracles, PDF extraction is the observation mechanism, comparator rules produce test outcomes, and abstention represents oracle uncertainty. The comparator calibration, structural-presence baseline, repeatability arm, provenance records, and source-contract validation make the testing infrastructure falsifiable and reproducible. The contribution is appropriately framed as a domain-specific empirical testing protocol and benchmark with a bounded application, not as a user study, repair tool, or universal accessibility checker.
