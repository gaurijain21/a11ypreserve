# 1. Bottom line

## NOVELTY DEFENSIBLE WITH REQUIRED REPAIRS

I found no public work that appears to reproduce the complete A11yPreserve combination: controlled accessible DOCX fixtures; independently checked, feature-specific source contracts; named DOCX-to-tagged-PDF pipelines treated as systems under test; destination-structure extraction; explicit cross-format equivalence rules; provenance-linked case outcomes; and abstention when the evidence cannot establish equivalence. That is a defensible, but deliberately narrow, novelty claim.

The novelty is not the observation that conversion can lose accessibility information. That observation is already supported by standards, office-to-EPUB research, PDF accessibility studies, conversion-quality research, and vendor experience. Nor is the novelty a new PDF/UA validator, a general accessibility checker, or a new testing theory. The credible contribution is a source-grounded, representability-aware testing protocol for measuring selected accessibility-information preservation in a DOCX-to-PDF transformation.

The most credible rejection path is an ICST reviewer saying that this is a straightforward application of established test-oracle and differential-testing ideas to a small, synthetic document corpus. That attack is not fatal, but it becomes serious if the paper does not explicitly connect itself to the software-testing literature, distinguish itself from PDF/UA conformance suites and destination-only benchmarks, and make the minimum novelty claim instead of implying a first study of accessible conversion.

The current evidence is scientifically usable but not broad: 26 controlled fixtures, 52 atomic cases, two named pipelines, 18 unresolved equivalence cases, a cloud route deviation for Variant B, and no disabled-user evaluation. Those limitations are already unusually well disclosed. They should remain limitations; they should not be hidden by changing labels or by converting unresolved cases into failures or passes.

Search basis and confidence: this review used fresh searches of public scholarly metadata and full-text pages indexed from ACM, IEEE, Springer, ScienceDirect, arXiv, Google-like scholarly results, PDF Association, W3C, DAISY, and public conversion-benchmark pages on 2026-10-03. Some publisher pages did not expose full text. “No collision found” therefore means no collision found in the searched public record, not proof that no unpublished, non-indexed, industrial, or contemporaneous work exists.

# 2. Closest prior art

The table below separates direct empirical threats from methodological and standards precedents. “No” means that the searched description did not show the property; “not established” means that the public material was insufficient to make a reliable determination. It does not mean the authors could not have performed an unreported activity.

| Work | Exact question or scope | Source → target; converters | Accessibility semantics studied | Controlled fixtures | Explicit source oracle | Conversion preservation measured | Equivalence / abstention | Multiple converters | Software-testing framing | Reusable harness/corpus | Overlap with A11yPreserve | Meaningful difference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Roig & Ribera, 2015, Interacción 2015, DOI [10.1145/2829875.2829926](https://doi.org/10.1145/2829875.2829926) | Whether non-technical users can create accessible EPUB from office documents; reports that conversion results do not meet accessibility standards or preserve accessibility information. | Office documents → EPUB; common office/editor conversion routes. | Accessibility criteria and EPUB3-related structure. | Quantitative conversion evaluation, but feature-isolated DOCX fixtures and a two-instance-per-feature design are not established from the public record. | No explicit machine-readable source contract in the available record. | Yes, and this is the closest direct precedent for accessibility-aware office-document transformation. | Not an explicit cross-format semantic-equivalence/abstention taxonomy in the available record. | Yes or multiple tool routes are discussed, but not DOCX→tagged-PDF pipelines. | Not presented primarily as SUT/oracle testing. | Not an A11yPreserve-like open DOCX-to-PDF harness. | Serious precedent against any claim that accessibility preservation during document conversion is new. | Different target format, different instrumentation, no demonstrated source-contract oracle, and no direct DOCX→PDF evidence. |
| Sperberg-McQueen, 2011, International Journal of Digital Curation, DOI [10.2218/ijdc.v6i1.179](https://doi.org/10.2218/ijdc.v6i1.179) | How to formalize successful format conversion in terms of preservation of the “intellectual content” licensed by markup. | General digital formats and markup vocabularies; conceptual rather than a named converter study. | General document semantics, not accessibility-specific properties. | No empirical fixture suite. | A semantic formalization, not feature-specific source contracts for accessibility. | Defines the preservation problem and discusses quantifying loss or distortion, but does not run the A11yPreserve experiment. | Discusses semantic equivalence difficulties, not an empirical abstention mechanism. | No. | Not an empirical testing paper. | No executable conformance suite shown. | Directly threatens any broad claim that A11yPreserve invented the idea of semantic-preservation measurement. | A11yPreserve operationalizes a small accessibility-specific subset for DOCX→PDF and makes uncertainty an observed outcome. |
| Bajcsy et al., 2010, ACM workshop, DOI [10.1145/2039274.2039284](https://doi.org/10.1145/2039274.2039284) | How to find, execute, and compare file-format conversions and evaluate information loss at scale. | Many file formats and third-party converters; Polyglot/Versus framework. | Generic information retention, not accessibility semantics. | Heterogeneous conversion files rather than source-grounded accessibility fixtures. | User-defined comparison features, not accessibility contracts. | Yes, through conversion execution and information-loss comparison. | Similarity/dissimilarity choices are acknowledged; no accessibility equivalence/abstention taxonomy. | Yes, through conversion paths and third-party software. | Conversion-quality/information-loss infrastructure, not ICST oracle research. | Yes: conversion registry, engine, comparison infrastructure. | Serious precedent for a reusable conversion-testing harness and configurable comparison mechanism. | Does not address DOCX accessibility properties, tagged PDF structure, representability, or conservative unresolved outcomes. |
| Suri & El-Saad, 2018/2021, Library Hi Tech, DOI [10.1108/LHT-10-2017-0220](https://doi.org/10.1108/LHT-10-2017-0220) | How reliably heterogeneous files can be batch-converted to PDF/A and what reproducibility/content errors occur. | DOC/DOCX, PPT/PPTX, Excel, PDF, images, email, and web pages → PDF/A-1b; LuraTech, Adobe Acrobat, and 3-Heights. | Links, missing text/content, fields, graphics, spelling, and visual faithfulness; not accessibility-semantic preservation. | 80 heterogeneous files with varied complexity; not feature-isolated accessibility fixtures. | Visual/source familiarity rather than explicit accessibility contracts. | Yes, multi-converter conversion quality and reproducibility. | No cross-format accessibility-equivalence or principled abstention. | Yes, three tools. | Not primarily a software-testing contribution. | Public supplementary material and test files are associated with the study. | Serious precedent for multi-converter document migration evaluation and for the reviewer’s “two converters are too few” concern. | Different target profile, no accessible DOCX contracts, no tagged-PDF semantics, no feature-level source oracle. |
| Brady, Zhong & Bigham, 2015, W4A, DOI [10.1145/2745555.2746665](https://doi.org/10.1145/2745555.2746665) | How accessible published PDFs are in accessibility/HCI conference proceedings, plus experiences making papers accessible. | Published papers → PDF as encountered; not a controlled conversion experiment. | Tags, alt text, structure, and manual/automatic PDF accessibility. | Large real corpus: 1,811 papers; manual sample. | No known source contract because original accessible semantics were not controlled. | No source-to-destination preservation measurement. | No cross-format equivalence or abstention. | Not a converter comparison. | Accessibility evaluation, not SUT testing. | Corpus and evaluation process, but not a DOCX-to-PDF converter harness. | Threatens claims about the importance and novelty of PDF accessibility evaluation, not the source-preservation method. | Destination-only and real-corpus study; it cannot answer whether an authored DOCX property survived conversion. |
| Wang et al., 2021, SciA11y, ASSETS, DOI [10.1145/3441852.3476545](https://doi.org/10.1145/3441852.3476545) | How to convert scientific PDFs into accessible HTML. | PDF → HTML; SciA11y pipeline. | Reading order, structure, figures, equations, tables, and accessible navigation. | Scientific papers and evaluation examples, not paired controlled DOCX source fixtures. | No source accessibility contract from a known pre-conversion authoring state. | It evaluates destination generation, not preservation from a verified source. | No explicit unresolved cross-format equivalence taxonomy. | Not principally a multi-converter comparison. | Not framed as software testing of a converter against source contracts. | Software/system, but not the same reusable conformance suite. | Important adjacent accessibility-aware document conversion work; it weakens any claim to be first in accessibility-aware document transformation. | Opposite direction, PDF→HTML; generation/remediation rather than testing preservation of source information through DOCX→PDF. |
| Kumar, Padath & Wang, 2025, ASSETS, DOI [10.1145/3663547.3746380](https://doi.org/10.1145/3663547.3746380) | How automated and LLM-based approaches perform when evaluating PDF accessibility. | PDF → evaluator labels; PAC/Acrobat/LLMs and expert-validated PDF data. | Alt-text quality, reading order, semantic tagging, tables, links, contrast, font readability. | 125 scholarly PDFs with expert-validated annotations. | Expert-validated destination labels, not source-document contracts. | No conversion preservation; evaluates assessment approaches. | Yes, a four-label framework includes Passed, Failed, Not Present, and Cannot Tell. | Multiple evaluators. | Accessibility-evaluation benchmark, not source-to-destination SUT testing. | Public benchmark/data repository. | Strongest precedent for nuanced labels and explicit “Cannot Tell”; it means A11yPreserve must explain why its unresolved category is not merely renamed prior art. | It is destination-only, not DOCX→PDF, and does not test preservation of author-provided source semantics. |
| Mowar, Steinfeld & Bigham, 2026, CHI, DOI [10.1145/3772318.3790289](https://doi.org/10.1145/3772318.3790289) | How source cues and visual analysis can automate PDF tagging, reading order, alt text, and formula structure. | Source documents/LaTeX cues and rendered PDF → tagged/remediated PDF; iTagPDF. | Tags, reading order, figures, alt text, equations, captions/notes. | Case studies and document examples, not a DOCX feature-isolation conformance corpus. | Source cues are used, but not the same frozen source-contract oracle. | It improves/generates destination metadata; it is not a comparative preservation study of existing DOCX→PDF converters. | No A11yPreserve-style abstention taxonomy. | Not the primary contribution. | Not framed as converter SUT testing. | Software system and examples, not the same regression harness. | Serious adjacent threat because it also argues that semantics present before PDF rendering matter and uses source information. | Remediation/generation, especially LaTeX-oriented; A11yPreserve measures what existing pipelines preserve without repair. |
| DAISY AI SIG, 2026, “PDF Conversions Put to the Test,” [public benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/) | How seven conversion services turn PDFs into accessible documents under a shared quality framework. | PDF → accessible documents; MuPDF, Acrobat, Mistral OCR, Marker, PaddleOCR-VL, Claude, Gemini. | Text fidelity, headings/lists, tables, equations, footnotes, images, alt-text retention. | Four criterion-stressing documents, including a PDF generated from Word. | Shared criteria and consensus scoring, not controlled source contracts. | Yes, destination-conversion quality. | Three-point met/partial/not-met scoring and consensus; not explicit cross-format equivalence or abstention. | Yes, seven services. | Benchmarking, not an ICST source-oracle protocol. | Shared quality framework and results; public test corpus details are limited. | Strong contemporary precedent against claiming that no one benchmarks accessibility-aware conversion or uses feature-focused test documents. | Opposite direction (PDF→accessible output), consensus/manual scoring, no DOCX source oracle, and no one-way preservation classification. |
| DocAccessible, 2026, accessible HTML conversion benchmark, [research program](https://docaccessible.com/research) | Public program measuring what survives conversion and benchmarking accessible HTML conversion and validator disagreement. | Primarily PDF → HTML/accessible representations; public service/research pages. | Tagging errors, semantic structure, equations, validator disagreement, accessible HTML. | Real public documents and benchmark plans; not the controlled DOCX contract corpus. | Source-grounded claims are discussed, but the exact A11yPreserve contract protocol is not established. | Yes for conversion fidelity in adjacent direction. | Validator disagreement and quality categories; A11yPreserve-like unresolved cross-format cases not established. | Public program compares tools/validators in some studies. | Not primarily ICST testing. | Public benchmark/research materials, but not the same harness. | Close public gray literature; the paper already cites it and should continue to discuss it candidly. | Different source/target direction and no demonstrated DOCX-to-tagged-PDF preservation oracle. |
| Matterhorn Protocol 1.1, PDF Association, [PDF/UA conformance model](https://pdfa.org/download-area/publications/Matterhorn-Protocol-1-1.pdf), and [veraPDF validation](https://docs.verapdf.org/validation/) | How to test PDF/UA requirements through machine and human checkpoints. | Tagged PDF → PDF/UA conformance findings; veraPDF/PAC and other validators. | Tagged structure, language, headings, lists, tables, figures, links, metadata, and other PDF/UA requirements. | Reference/test suites exist for PDF conformance, not DOCX source contracts. | Destination conformance rules, not preservation contracts. | No source-to-destination preservation; destination conformance only. | Human checkpoints are not the same as cross-format equivalence abstention. | Multiple tools exist, but not an A11yPreserve pipeline comparison. | Explicit conformance testing, but not source-preservation testing. | Mature standards, rules, validators, and test corpora. | Serious threat if A11yPreserve is read as proposing another PDF accessibility checker or conformance suite. | A11yPreserve asks a different question: whether known source information survived. Matterhorn/veraPDF cannot answer that from a PDF alone. |
| `neurotic_docx_bench`, 2026, public benchmark, [project page](https://arthur.law/projects/docx-bench/) | How DOCX converters compare with Microsoft Word output for visual/rendering fidelity. | DOCX → PDF; multiple tools compared against Word-export PDFs. | Visual/page/text fidelity, redlines, layout; no accessibility semantics. | 6,427 documents and thousands of comparison pairs. | Word-rendered output is an execution/reference oracle, not accessibility contracts. | Yes, strong DOCX→PDF conversion fidelity benchmarking. | Visual similarity/diff, not accessibility equivalence or abstention. | Yes. | Benchmark/test-harness framing, but not accessibility testing. | Yes, substantial public benchmark. | Current practical threat to claims about DOCX-to-PDF benchmark infrastructure and converter comparison. | It does not measure tags, alt text, language, table semantics, footnotes, or accessibility-information preservation. |
| Jain, 2026, “PDFa11yMut,” arXiv [2609.33160](https://arxiv.org/abs/2609.33160) | How mutation-specific changes in PDF structure are detected by PDF accessibility checkers, with a small exploratory assistive-technology sample. | Tagged PDF reference suite → mutated PDFs; PAC, veraPDF, Acrobat, and one NVDA/Acrobat procedure. | PDF structure/conformance and selected semantic/assistive representations. | Paired reference/mutant PDFs and 30 conformance-oriented mutants. | Mutation purity and intended-delta oracles, not source DOCX contracts. | No DOCX→PDF preservation measurement. | Reports checker blind spots; not cross-format equivalence of a source and target. | Yes, several checkers. | Explicit mutation-testing study, not document-conversion SUT testing. | Reusable mutation operators and artifact. | Important adjacent testing work: it shows that a tagged-PDF checker is not a complete semantic oracle and that mutation-based validation is a separate contribution. | It deliberately studies PDF checker detection, not conversion preservation; A11yPreserve should not drift toward this problem. |

The strongest collision is therefore Roig and Ribera for the general accessibility-preservation idea, and the strongest methodological collisions are Sperberg-McQueen, Bajcsy et al., Suri and El-Saad, Kumar et al., Matterhorn/veraPDF, and the recent DAISY benchmark. None of the searched works combines the full A11yPreserve design. The paper must nevertheless cite and position these works so the contribution is not presented as a discovery that document conversion can be lossy.

## Novelty attacks

| Attack | Classification | Adversarial finding |
|---|---|---|
| 1. Has someone already systematically measured DOCX→PDF accessibility-semantic preservation? | NOT SUPPORTED as an exact collision; MODERATE residual risk | The search found adjacent office→EPUB preservation, PDF accessibility evaluation, and general DOCX→PDF fidelity work, but no direct public study with the full source-contract/semantic-preservation design. The absence claim must remain qualified. |
| 2. Has someone used feature-isolated fixtures for this? | NOT SUPPORTED for the exact DOCX→PDF accessibility task; MODERATE residual risk | DAISY uses criterion-stressing documents and `neurotic_docx_bench` uses extensive document corpora, but neither searched description shows A11yPreserve’s two controlled instances per accessibility family with source contracts. |
| 3. Has someone treated converters as systems under test? | MODERATE | This is standard software-testing language and is implicit in many converter benchmarks. It is not novel by itself. Its value here is the explicit mapping to source contracts and destination evidence, not the phrase “system under test.” |
| 4. Has someone used explicit source accessibility contracts as oracles? | NOT SUPPORTED for this exact cross-format setting; MODERATE residual risk | Standards and source-aware systems motivate preservation, and general testing literature covers contracts and oracles. The searched accessibility-conversion work did not show a directly comparable machine-readable DOCX contract set used to decide preservation row by row. |
| 5. Has someone compared several DOCX→PDF pipelines specifically for accessibility semantics? | MODERATE to SERIOUS | Multi-converter conversion research exists, and many tools compare PDF accessibility. The unfilled gap appears to be the intersection of DOCX source semantics, PDF destination structure, and explicit preservation outcomes. A reviewer may still regard two pipelines as a thin empirical demonstration. |
| 6. Has someone introduced equivalence/abstention for incomparable cross-format semantics? | MODERATE | Kumar et al. use “Cannot Tell,” and standards testing distinguishes machine from human checkpoints. A11yPreserve’s feature-specific cross-format unresolved outcome is plausible but not wholly unprecedented. The paper should claim a concrete operationalization, not invention of uncertainty-aware evaluation. |
| 7. Has someone published essentially the same corpus or harness? | NOT SUPPORTED | No searched public corpus matched the 26 controlled DOCX fixture design, contract files, PDF observations, and evidence certificates. This is the strongest artifact-level novelty claim, subject to a final exact-title/code search before submission. |
| 8. Does an existing conformance suite already provide everything claimed? | SERIOUS if the claim is read broadly; NOT FATAL under the current scope | Matterhorn, PAC, and veraPDF provide strong destination-PDF conformance infrastructure. They do not know whether a source DOCX author’s inline language, alt text, footnote association, title, or table relation survived. A11yPreserve must keep this distinction explicit and add the standards-testing citations. |
| 9. Is this merely applying existing testing methodology to a new file type? | SERIOUS | This is the best Reviewer-2 attack. Application novelty can be acceptable at ICST when the domain creates nontrivial oracle, equivalence, and reproducibility problems. Here the 18 unresolved cases and comparator calibration provide evidence that the application is not a trivial exact diff, but the paper should not claim a new general testing theory. |
| 10. Would reviewers consider the application insufficiently novel? | MODERATE | Some ICST reviewers may require stronger evidence that the domain-specific oracle, representability rules, and abstention materially change test outcomes relative to a naive baseline or PDF/UA validator. A low-cost baseline cross-tab would reduce this risk, but the current bounded method is not obviously unpublishable. |

# 3. Strongest novelty claim

A11yPreserve contributes a source-grounded, representability-aware testing protocol for one-way DOCX-to-tagged-PDF transformation: controlled DOCX accessibility contracts are independently checked before execution, named conversion pipelines are tested as systems under test, destination structure is extracted through evidence paths, and cases that cannot be responsibly compared are explicitly abstained rather than forced into pass/fail.

The empirical contribution is a reusable, provenance-linked benchmark instance demonstrating this protocol on selected accessibility properties across two real pipelines. It is not a claim to be the first accessible-conversion study, the first document benchmark, the first use of a test oracle, or a complete measure of PDF accessibility.

If this claim is removed, the paper loses its central source-preservation testing contribution. If the claim is broadened to “accessibility preservation during document conversion” without the DOCX, tagged-PDF, selected-property, and tested-pipeline qualifiers, it becomes indefensible.

# 4. Top five Reviewer-2 attacks

## 1. “This is obvious: accessible Word exports can lose accessibility.”

- Severity: SERIOUS.
- Current defense: The paper does not claim the observation is new. Its protocol makes the source property explicit, independently checks the source, compares destination representations, preserves provenance, and abstains for unresolved equivalence. The four confirmed losses are evidence that the protocol can expose concrete feature-specific outcomes, not a general prevalence claim.
- Action needed: REQUIRED paper-only repair. Add the testing-oracle and format-conversion precedents, state the minimum novelty claim, and include a sentence explaining why a destination-only checker cannot answer the preservation question.

## 2. “This is a small synthetic toy corpus, so the results do not matter.”

- Severity: HIGH.
- Current defense: The corpus is intentionally controlled, feature-focused, contract-verified, and supplemented by Variant B, repeatability, and a separate integrated sanity check. The paper explicitly disclaims representativeness, prevalence, and standards completeness.
- Action needed: No expansion is automatically required. The paper should say more sharply that diagnostic validity is the purpose of the controlled corpus and that ecological validity is deliberately out of scope. A small real-document set should not be merged into the main denominator.

## 3. “Two pipelines, no Microsoft Word, and a cloud route deviation cannot support a converter result.”

- Severity: HIGH.
- Current defense: The paper reports condition-specific observations, not a ranking or ecosystem claim; it records the LibreOffice version/settings, Google workflow, cloud-version limitation, observed producer, and Variant B export-backend deviation. Word is excluded from the denominator.
- Action needed: REQUIRED paper-only repair to make the denominator and route distinction visually unavoidable. A Word run would strengthen the paper but is not essential to the narrowly scoped question and should not be added merely to imply ecosystem coverage.

## 4. “The comparator is not an accessibility oracle; it is a structural diff written by the authors.”

- Severity: HIGH.
- Current defense: The paper defines the measurement target as machine-verifiable source-information preservation, not end-user accessibility; it uses multiple extraction paths, a separate source oracle, a calibration set, and an explicit unresolved/measurement-error category. It reports two false negatives and seven unresolved/indeterminate calibration controls rather than claiming sensitivity or specificity.
- Action needed: REQUIRED paper-only repair to replace any residual “ground truth,” “accessibility oracle,” or “preserved accessibility” wording with “contract-verified source encoding,” “source-preservation oracle,” or “preservation of the contracted machine-verifiable property.” A validator cross-tab is the highest-value optional baseline.

## 5. “Eighteen unresolved rows mean the method cannot answer the research question.”

- Severity: HIGH.
- Current defense: The method’s stated contribution is uncertainty-aware testing. The unresolved rows are concentrated in difficult cross-format mappings and are not silently counted as failure or success. The paper reports them in the primary denominator and distinguishes them from measurement error.
- Action needed: No forced reclassification. The discussion should explicitly state that the current study demonstrates measurable preservation for a subset of contracts and maps the boundary of automation. If the submission venue expects a lower unresolved rate, run focused comparator calibration only as a separate addition; do not change frozen classifications.

# 5. Methodology vulnerabilities

| Rank | Vulnerability | Severity | Adversarial assessment | Already mitigated? |
|---|---|---|---|---|
| 1 | Cross-format equivalence is under-specified for difficult mappings. | CRITICAL | “Same meaning” is not derivable from a tag name. Footnotes, table-header associations, equations, links, captions, and list encodings can be represented in multiple valid ways. Eighteen unresolved cases are evidence of this problem, but they also limit the number of determinate scientific findings. | Partly. Feature-specific contracts, alternate encodings, parser triangulation, calibration, and abstention help; no independent semantic adjudication exists. |
| 2 | The source contract is authored by the same research team. | HIGH | The contract is not an external ground truth in the strong epistemic sense. A wrong contract can be consistently validated by both source implementations. The paper openly says there was no external expert panel, but the limitation remains material. | Partly. Independent raw-OOXML assertions and ASIR agreement reduce extractor-only errors, not construct-validity bias. |
| 3 | Only two primary pipelines are evaluated. | HIGH | The result can show that outcomes differ by feature and pipeline, but it cannot establish converter-family behavior. The Google route is also not fully version-pinnable. | Yes for claim scope, not for external generalization. |
| 4 | No user-facing assistive-technology validation. | HIGH | PDF tags and structure-tree observations are not equivalent to screen-reader task success. A screen reader may expose a structurally imperfect PDF acceptably, or a structurally plausible PDF may behave poorly. | Yes for claim scope. The paper explicitly excludes usability and disabled-user impact. |
| 5 | Synthetic, low-complexity fixtures may omit interactions and layout failures. | HIGH | Feature isolation improves diagnostic attribution but can make the source unrealistically easy. Integrated documents help but are project-generated and excluded from the primary denominator. | Partly. Variant B and the integrated sanity check are useful, but not external validity. |
| 6 | Variant B demonstrates only one additional instance per feature. | MEDIUM | Two instances per family are better than one, but still do not establish robustness over authoring styles, layout, language, or document complexity. | Yes as a bounded adequacy claim; not as broad generalization. |
| 7 | Google Variant B used a recovered in-session export backend rather than the visible download path. | HIGH | This may be a route difference, not merely a UI implementation detail. It is disclosed, but the primary evidence should not imply identical Google execution conditions across all rows. | Yes for transparency; not for route equivalence. |
| 8 | Calibration is not a validation study. | MEDIUM | The 27 diagnostic controls are useful, but the two false negatives and seven unresolved/indeterminate controls show that the comparator’s error profile is not fully characterized. The counts cannot support sensitivity, specificity, or a general error rate. | Yes: the paper explicitly avoids those claims. |
| 9 | “Confirmed lost” may be read as semantic loss rather than absence of the contracted representation. | MEDIUM | The evidence supports absence of the tested machine-verifiable association under the available extraction paths. It does not establish absence of all equivalent semantics or user harm. | Partly. Definitions and discussion narrow the meaning, but the label remains rhetorically strong. |
| 10 | Byte-identical repeatability may be overinterpreted. | LOW | It shows operational determinism in the recorded Google environment, not semantic correctness, backend invariance, or real-world reliability. | Yes: the paper calls it a dated workflow observation. |
| 11 | Counts and percentages could be mistaken for prevalence. | LOW | The paper reports counts and avoids percentages, states unequal feature complexity, and disclaims prevalence. | ALREADY MITIGATED. |
| 12 | PDF/UA or a tagged structure could be mistaken for complete accessibility. | LOW | The paper repeatedly distinguishes destination structure from user accessibility and does not claim PDF/UA conformance or usability. | ALREADY MITIGATED. |

## Corpus-specific verdict

Thirteen feature families and two controlled instances per family are sufficient for a diagnostic testing paper whose unit is a contract–pipeline case, not sufficient for prevalence, population inference, or broad converter claims. Feature isolation is scientifically defensible because the claimed output is a failure localization and measurement protocol. It would be indefensible only if the paper used the resulting counts as a global accessibility score.

## Oracle-specific verdict

The source contract is a test oracle in the engineering sense, not an ontologically complete accessibility ground truth. The source oracle establishes that the intended OOXML encoding is present and that the contract is internally consistent. It does not prove that the contract fully captures the author’s accessibility intent or that the contract’s source-to-PDF mapping is the only valid one.

## Comparator-specific verdict

The comparator is a measurement mechanism for selected source-preservation contracts. It is not a complete accessibility checker. The most important scientific fact is not that it always decides; it is that calibration revealed alternate encodings that should not be declared lost. A reviewer can still reasonably ask for a simple baseline, because the paper currently explains the comparator’s value better conceptually than empirically.

## Abstention verdict

Abstention is principled when the contract is valid, relevant destination evidence exists, and the evidence does not establish equivalence or absence. It becomes an evasion only if every difficult case is placed into unresolved without documenting the missing evidence or if unresolved rows are omitted from denominators. A11yPreserve does document evidence paths and keeps unresolved cases in the denominator, so the mechanism is defensible; the unresolved rate remains a substantive limitation.

# 6. Missing baselines

## Necessary baselines

No additional baseline is strictly necessary to make the current narrow research question intelligible, because the paper is not proposing a ranking model and the central object is the source-preservation protocol. However, it is necessary that the paper explicitly position the following existing systems as different questions:

- Matterhorn/PDF/UA rules, PAC, and veraPDF: destination conformance, not source-preservation equivalence.
- A destination-only structural check: useful for output validity, unable to determine whether an author-supplied source value survived.
- A visual or text-only diff: useful for rendering/content fidelity, unable to establish accessibility semantics.

## Valuable baseline

The highest-value cheap baseline is a destination-only PDF/UA validator cross-tab on the same 52 output PDFs, using one reproducibly available validator and recording its exact version/profile. The analysis should report, for each A11yPreserve status, whether the validator passes, fails, or requires human review. It should not be used to call the validator wrong. The purpose is to show whether a clean destination conformance result can coexist with an altered/lost source contract, and whether a validator failure can coexist with a preserved contract. That directly supports the paper’s claim that destination accessibility and source-information preservation are different questions.

A second valuable baseline is a strict naive comparator: exact equality of selected PDF structure/property fields against the source-to-PDF mapping, with no alternate-encoding normalization and no unresolved state. Run it only on existing calibration controls or a separately marked analysis. Report cases where exact comparison would produce a false loss or false pass relative to the calibrated evidence-aware procedure. This would make the benefit of semantic equivalence and abstention empirical rather than only methodological.

## Nice-to-have only

Screen-reader cross-checks, a large real-world corpus, a global converter score, and a Word-versus-non-Word product ranking are not necessary baselines for this paper. They answer different or broader questions and would increase scope and interpretation risk.

# 7. Highest-value pre-submission improvements

At most three additions are justified. None authorizes changing frozen classifications or regenerating primary evidence during this red-team pass.

## 1. Add the missing software-testing and format-conversion positioning — REQUIRED

- Weakness addressed: The current manuscript uses the SUT/oracle language correctly but does not cite the canonical testing literature that makes the mapping meaningful to an ICST reviewer.
- Exact action: Add Barr et al., “The Oracle Problem in Software Testing,” DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785); Segura et al., “A Survey on Metamorphic Testing,” DOI [10.1109/TSE.2016.2532875](https://doi.org/10.1109/TSE.2016.2532875); and one differential-testing precedent such as McKeeman’s differential-testing work. Add Sperberg-McQueen, Bajcsy et al., and Suri & El-Saad to the format-conversion discussion. Explain exactly which established ideas are adopted and what domain-specific difficulty is added.
- Main experiment modified: No.
- Value: High. It changes the ICST reading from “accessibility benchmark” to “domain-specific testing method with an oracle/representation problem.”
- Risk: Low. Paper-only, no evidence change.
- Essential before ICST: Yes.

## 2. Add a destination-validator cross-tab, if reproducibly available — OPTIONAL

- Weakness addressed: The paper says its method differs from destination-only PDF/UA checking but does not show the relationship on the same outputs.
- Exact experiment: Run one pinned validator/profile over the existing 52 PDFs; retain raw reports and hashes in a separate derived analysis; cross-tab validator result against the six A11yPreserve statuses. Do not replace A11yPreserve classifications and do not infer that validator disagreement proves a tool defect.
- Main experiment modified: No; this is an appended baseline analysis.
- Value: High per unit effort. It would directly demonstrate what source-preservation testing adds.
- Risk: Medium. Validator availability, PDF/UA profile differences, and human checkpoints could create new interpretation work.
- Essential before ICST: No. Do not delay submission if the validator cannot be pinned and documented cleanly.

## 3. Focused comparator calibration for the highest-impact unresolved mappings — OPTIONAL

- Weakness addressed: The 18 unresolved cases and two false-negative calibration controls leave uncertainty about whether the comparator is conservative because of genuine representability limits or because extraction support is incomplete.
- Exact experiment: Construct a small, separately versioned calibration set for list numbering, hyperlink association, multi-level table headers, footnote/reference association, equations, captions, and inline language. For each control, specify the intended source contract, a known PDF encoding, an alternate valid encoding, and a deliberately absent encoding. Measure only control-level determinate/unresolved outcomes; do not report population sensitivity or specificity.
- Main experiment modified: No; keep the existing evidence and classifications frozen, and report the new calibration as a separate instrument-validation analysis.
- Value: Medium to high. It could convert a few unresolved cases into responsibly determined outcomes or strengthen the case that abstention is the correct result.
- Risk: Medium to high. It may expose additional parser or contract defects and could require provenance updates; it must not silently rewrite the primary results.
- Essential before ICST: No, provided the current calibration limitations and unresolved denominator remain explicit.

### Additions not recommended before submission

Microsoft Word would be the most obvious external converter, but adding it now would substantially change the empirical comparison and require licensing, reproducibility, and route documentation. A real-world corpus would add ecological validity but weaken known ground truth. Neither is essential to the present controlled-testing contribution.

**DO THIS BEFORE SUBMISSION:** perform the paper-only testing-literature/related-work and claim-scope repair.

**DO NOT DELAY SUBMISSION FOR THIS:** the validator cross-tab, Word pipeline, or real-world corpus, unless the venue specifically requires a converter benchmark or baseline comparison.

# 8. Things we should NOT add

- Do not add a repair/recommendation engine. It would move the paper toward accessibility remediation rather than testing conversion preservation.
- Do not add an AI or LLM component. It would create a new oracle and reproducibility problem without strengthening the central question.
- Do not add a disabled-user study solely to make the paper appear more accessibility-oriented. It would be valuable for a different user-impact question, but it is not required to establish the machine-verifiable preservation protocol.
- Do not add a global converter score, weighted accessibility rate, or ranking. The controlled feature units are heterogeneous, and the paper correctly refuses prevalence or product ranking claims.
- Do not merge the integrated sanity check into the 52-case denominator. It serves protocol applicability, not independent corpus evidence.
- Do not convert unresolved equivalence into lost, failed, or preserved merely to improve headline percentages.
- Do not add Microsoft Word, Acrobat, PAC, or a commercial cloud service unless the complete route, version, license, and repeatability evidence can be documented without changing the frozen main experiment.
- Do not pivot to PDF mutation testing, checker accuracy, LLM document understanding, screen-reader usability, or a generic PDF accessibility benchmark. Those are adjacent research programs, not the A11yPreserve question.
- Do not treat “tagged PDF,” “PDF/UA pass,” or “validator clean” as synonymous with preserved source semantics or end-user accessibility.
- Do not present the public artifact as if it contains internal logs, absolute paths, development history, or identity-bearing repository metadata. Only the sanitized artifact boundary is in scope.

# 9. Related-work repairs

The current related-work section already cites Roig and Ribera, SciA11y, iTagPDF, Kumar et al., DAISY, DocAccessible, and vendor guidance. It is directionally honest but still under-cites the software-testing and general format-conversion literature that an ICST reviewer will expect.

## Add or strengthen these citations

1. **Test-oracle theory:** Barr et al., “The Oracle Problem in Software Testing: A Survey,” IEEE TSE 2015, DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785). Use it to state that the contract is a domain-specific specification-based oracle and that unresolved equivalence is an oracle limitation, not a converter failure.
2. **Metamorphic/differential context:** Segura et al., “A Survey on Metamorphic Testing,” IEEE TSE 2016, DOI [10.1109/TSE.2016.2532875](https://doi.org/10.1109/TSE.2016.2532875). State that A11yPreserve is not a standard metamorphic relation study: it compares one source execution to a destination representation under a cross-format contract. This prevents a reviewer from thinking the testing language is decorative.
3. **Direct accessibility-preservation precedent:** Roig & Ribera, 2015, DOI [10.1145/2829875.2829926](https://doi.org/10.1145/2829875.2829926). The current citation should include the DOI and should describe the office→EPUB work as a genuine precedent, not merely “adjacent.”
4. **Generic semantic preservation:** Sperberg-McQueen, 2011, DOI [10.2218/ijdc.v6i1.179](https://doi.org/10.2218/ijdc.v6i1.179). Use this to acknowledge that semantic equivalence and information loss in format conversion were formalized before A11yPreserve.
5. **Conversion infrastructure:** Bajcsy et al., 2010, DOI [10.1145/2039274.2039284](https://doi.org/10.1145/2039274.2039284). Discuss the conversion registry/engine/comparison-engine precedent and state what A11yPreserve specializes: accessibility contracts and tagged-PDF evidence rather than generic format similarity.
6. **Multi-converter migration quality:** Suri & El-Saad, “Lost in migration: document quality for batch conversion to PDF/A,” DOI [10.1108/LHT-10-2017-0220](https://doi.org/10.1108/LHT-10-2017-0220). This is essential to preempt the claim that multiple-converter document conversion testing is new.
7. **Destination-PDF evaluation:** Brady et al., W4A 2015, DOI [10.1145/2745555.2746665](https://doi.org/10.1145/2745555.2746665), and Kumar et al., ASSETS 2025, DOI [10.1145/3663547.3746380](https://doi.org/10.1145/3663547.3746380). Use them to distinguish destination accessibility assessment, expert labels, and “Cannot Tell” from source-preservation testing.
8. **Conformance infrastructure:** Matterhorn Protocol 1.1 and [veraPDF’s PDF/UA validation documentation](https://docs.verapdf.org/validation/). State directly that these are important baselines and complementary test infrastructure, not substitutes for a source-preservation oracle.
9. **Recent non-peer-reviewed benchmarks:** DAISY’s [PDF Conversions Put to the Test](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/) and the public `neurotic_docx_bench` [project page](https://arthur.law/projects/docx-bench/). Cite them only with their status and exact direction/scope; do not treat either as peer-reviewed evidence equivalent to an ICST paper.

## Exact related-work gap to state

The gap should be written as an intersection, not an absolute absence claim:

> Existing work covers accessibility-aware office-document transformation, PDF accessibility evaluation, PDF remediation, general conversion fidelity, and PDF/UA conformance. The searched literature does not provide the same source-grounded DOCX-to-tagged-PDF preservation protocol in which feature-specific source contracts are independently checked, cross-format equivalence is explicit, and unresolved cases remain in the primary denominator. A11yPreserve studies that narrower intersection.

## Version-label cleanup discovered during review

The reviewer-facing paper currently uses “V3” in the abstract, introduction, results, conclusion, and historical-provenance sentences, while the manuscript path is `submission/ICST2027_V3`. These labels are useful internal provenance but are not appropriate as the scientific name of the submitted method. Before submission, replace reviewer-facing development labels with “Main experiment,” “Core corpus,” “Variant B,” “repeatability arm,” “integrated sanity check,” or “final source-contract protocol,” as applicable. Do not rename frozen internal directories or scripts if that would break provenance; instead keep the labels in internal records and remove unnecessary development history from the paper and public-facing narrative.

# 10. Claims needing narrowing

The paper is already cautious, but the following phrases remain vulnerable to adversarial reading and should be repaired in a later paper-only pass. This review does not change them.

| Location / current wording | Risk | Narrower defensible wording |
|---|---|---|
| Research question: “Does accessibility information present in a source document survive document conversion?” | Sounds universal and may invite a “complete accessibility” reading. | “For selected machine-verifiable source contracts, does the corresponding information survive the tested DOCX-to-tagged-PDF pipeline?” |
| Methodology: “The method begins with a document whose target accessibility properties are known.” | “Known” can sound like external semantic ground truth. | “The method begins with a DOCX whose selected source encodings are verified against explicit contracts.” |
| Methodology: “This establishes encoded source ground truth.” | Same-team contracts and source extractors do not establish complete semantic truth. | “This establishes contract-verified source encoding for the selected properties.” |
| Abstract and conclusion: “verified preserved” without an immediate “contracted property” qualifier | A reader may infer end-user accessibility preservation. | “verified preservation of the contracted, machine-verifiable source property.” |
| Abstract/results: “confirmed loss” | Stronger than the actual evidence when an alternate encoding cannot be ruled out in every case. | Preserve the defined label only with the qualification “absence of the required contracted destination representation under the available independent evidence paths.” |
| Introduction: “real DOCX-to-PDF pipelines” | True, but Google’s cloud backend and Variant B route are not fully pinned or identical. | “two named, recorded DOCX-to-PDF pipeline conditions, including a cloud service whose backend version is not fully pinnable.” |
| Contribution: “reusable conformance-suite design” | Could be read as a replacement for PDF/UA/Matterhorn or as a complete suite. | “reusable, adapter-oriented source-preservation conformance-suite design for the selected contracts.” |
| Discussion: “accessibility-information preservation can be tested” | Too broad without the measurability boundary. | “selected machine-verifiable accessibility-information preservation can be tested when representability and evidence rules are explicit.” |
| Any remaining use of “document converters” without a named set | Invites generalization from two conditions. | “the tested LibreOffice and Google Docs pipeline conditions.” |
| Any use of “reliable” for repeatability | Byte identity demonstrates dated operational determinism, not semantic or future reliability. | “classification-stable and byte-identical within the recorded environment.” |
| Any use of “ground truth” outside the source-oracle technical description | Overstates construct validity. | “contract-verified source state” or “source oracle state.” |
| Any use of “real-world” for the integrated documents | They are project-generated. | “multi-feature integrated sanity-check documents.” |
| Any phrase implying the Google route’s observed losses were caused by PDF export alone | The route includes DOCX import, internal representation, and PDF generation. | “observed under the tested Google Docs DOCX-import/export pipeline; causal stage is not isolated.” |

## Accessibility-validity boundary

The paper’s distinction between accessibility semantics and end-user accessibility is correct and should be retained prominently. A tagged PDF, a PDF/UA result, or a matching structure element is evidence about a representation, not proof of task completion, screen-reader usability, or absence of barriers. No screen-reader study is required for the current claim, but no sentence should imply that the current results establish user impact.

# 11. ICST fit

## Why this is a software-testing paper

A11yPreserve is an ICST paper if the paper makes the test system—not the PDF format—the primary object of contribution:

- **Test inputs:** controlled DOCX fixtures with feature isolation and a second controlled instance per family.
- **Specifications/oracles:** explicit source contracts, independently checked before conversion.
- **Systems under test:** the complete named conversion pipelines, including DOCX import, conversion settings, and PDF generation.
- **Observations:** destination structure-tree objects, metadata, marked content, links, text extraction, and secondary parser evidence.
- **Oracle decision:** feature-specific comparison rules with precedence, alternate representations, provenance, and explicit unresolved/measurement-error states.
- **Test outcomes:** preservation classifications at fixture–feature–pipeline granularity.
- **Test adequacy boundary:** selected feature families, two controlled instances, two pipeline conditions, and qualitative behavior classes—not standards completeness or mutation score.
- **Reproducibility infrastructure:** frozen inputs, hashes, manifests, output records, repeatability artifacts, verifier scripts, and a sanitized artifact package.

This is more than repeatedly inserting “software testing.” The testing contribution is the operationalization of a cross-format oracle problem: a test can fail because a source value changed, because the required destination representation is absent, or because the evidence is insufficient to know whether an alternate representation is valid. The abstention state is especially relevant to testing because it prevents an automated comparator from manufacturing oracle certainty.

## What is convincing for ICST

The strongest ICST evidence is the source-oracle separation, explicit SUT boundary, provenance-linked fixture cases, two-path destination evidence, adversarial comparator calibration, and refusal to treat unresolved rows as failures. The two confirmed inline-language and footnote losses under the Google condition are useful fault-localized outcomes, while the 18 unresolved rows show that the test method encounters a genuine oracle/representation boundary.

## What is missing for ICST

1. Canonical test-oracle and metamorphic/differential-testing citations are missing from the current bibliography.
2. The paper does not yet empirically show how a naive exact comparator or a destination-only PDF/UA validator would differ from A11yPreserve.
3. “Conformance suite” risks being confused with a PDF/UA conformance suite unless the distinction is stated near the contribution claim.
4. The adequacy boundary is honest but qualitative. It does not provide a formal coverage metric, fault model, mutation score, or sampling argument. That is acceptable only if no stronger adequacy claim is made.
5. The paper should say that the method is a domain-specific testing protocol and benchmark, not a new general test-theory result.

## ICST verdict

The fit is sufficiently clear to be defensible, but it is not self-evident from the current related-work section. Small paper-only repairs are needed. No new feature or product should be added merely to make the paper look like testing research.

# 12. Final recommendation

## MAKE SMALL PAPER-ONLY REPAIRS, THEN SUBMIT

The paper should not be rejected as materially non-novel on the current public evidence. The exact intersection—contract-verified accessible DOCX source, DOCX-to-tagged-PDF pipeline testing, cross-format preservation comparison, and explicit abstention—is defensible. The result is appropriately bounded and the unresolved cases are disclosed rather than hidden.

Before submission, make the following paper-only repairs:

1. Add the canonical software-testing/oracle/differential-testing and general format-conversion references listed above.
2. Strengthen the related-work paragraph around Roig & Ribera, Suri & El-Saad, Matterhorn/veraPDF, Kumar et al., DAISY, and the general semantic-preservation precedents.
3. Replace residual broad “ground truth,” “preserves accessibility,” “document converters,” “real-world,” and “confirmed loss” readings with the narrower contract/pipeline wording above.
4. Remove unnecessary V1/V2/V3 development labels from reviewer-facing scientific presentation while preserving internal provenance names.
5. If inexpensive and fully reproducible, add the validator cross-tab as an optional baseline. Do not delay submission for Microsoft Word, a real-world corpus, a screen-reader study, or a global converter comparison.

The paper should not change frozen classifications, merge integrated observations into the atomic denominator, or claim that a clean PDF structure or PDF/UA result proves source-semantic preservation. With those repairs, the narrow contribution is plausible for an ICST submission: not a universal accessibility result, but an empirical software-testing protocol that makes source-to-destination semantic uncertainty explicit and measurable.

