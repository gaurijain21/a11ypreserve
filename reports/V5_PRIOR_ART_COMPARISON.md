# V5 prior-art comparison

The search was renewed against the named works and current primary/authoritative
sources. The conclusion is combination-based novelty, not a first-of-kind
claim.

| Work/source | Source → destination | Main accessibility question | Verified source semantics? | Multiple real converters? | Preservation oracle / abstention? | Position relative to A11yPreserve |
|---|---|---|---|---|---|---|
| Sperberg-McQueen, *What Constitutes Successful Format Conversion?* | General format conversion | Formalizes intellectual-content preservation and loss/distortion | Source/destination semantics in general | Not a DOCX/PDF converter benchmark | Operational semantic comparison, not this feature taxonomy | Foundational rationale for source-grounded conversion contracts, broader and not accessibility-specific. |
| Roig & Ribera, office-to-EPUB accessibility conversion | Office/XML → EPUB | Accessibility outcomes of office-document conversion | Not the same independently verified DOCX contract design | Conversion tools/paths are evaluated, but not this DOCX→PDF setup | Quantitative accessibility/conversion assessment; no V5 uncertainty oracle | Close preservation motivation, different destination and oracle. |
| SciA11y | Scholarly PDF → accessible HTML | Destination reconstruction, extraction, and user needs | Input PDFs are assessed, not known authored DOCX semantics | System pipeline, not cross-converter DOCX→PDF | Quality/user evaluation; not source-contract preservation | Destination transformation/remediation-oriented, not source semantic survival. |
| iTagPDF | PDF → tagged/metadata-enriched PDF | Automated tagging, reading order, and figure metadata | Existing PDF is input; source author semantics are not the experimental ground truth | Product/system evaluation, not DOCX→PDF comparison | Destination metadata generation, not cross-format equivalence | Related destination tagging work; separate research question. |
| Kumar et al., *Benchmarking PDF Accessibility Evaluation* | Existing scholarly PDFs / controlled PDF edits | Benchmark automated/LLM PDF accessibility evaluation | Expert-validated PDF annotations, not DOCX source contracts | Evaluates assessment approaches, not real DOCX exporters | Passed/Failed/Not Present/Cannot Tell, but not cross-format source equivalence | Close benchmark/oracle precedent; V5 differs by known DOCX source and conversion boundary. |
| DAISY PDF Conversions Put to the Test | PDF/document conversion services → accessible outputs | Practical destination quality across seven services | Shared test documents and consensus scoring; not DOCX source-contract preservation | Yes | Community quality framework/manual consensus | Strong current conversion benchmark; V5 is narrower, source-grounded, and machine-contract based. |
| DocAccessible benchmark/guidance | Public documents/PDF/HTML conversion and checking | Destination readiness and link integrity | Natural/public documents and destination checks | Depends on benchmark | Practical checker/benchmark, not the same source-to-PDF contract | Supports external-validity and destination-evaluation context; not a substitute for V5 question. |
| ATAG 2.0 / EN 301 549 transformation requirement | Standards | Preserve accessibility information when equivalent mechanisms exist | Normative requirement, not an empirical corpus | Not applicable | Normative basis, not an experimental oracle | Standards motivation for treating conversion as a preservation test. |
| Microsoft Word PDF accessibility documentation | Word DOCX → PDF | Documents how Word exporter emits PDF/UA tags and artifacts | Describes exporter mapping, not independent comparative experiment | One vendor route | No uncertainty-aware cross-format benchmark | Primary technical source for Word provenance and accepted destination structures. |

## Defensible contribution statement

A11yPreserve operationalizes accessibility preservation in DOCX-to-PDF
conversion as a source-contract testing problem: verified DOCX properties are
converted through named real pipelines and evaluated using feature-specific,
uncertainty-aware cross-format oracles. The distinction is explicit:

- destination evaluation asks whether the resulting PDF is accessible; and
- A11yPreserve asks whether a particular accessibility property known to exist
  in the DOCX survived, changed, partially represented, was lost, or could not
  be reliably measured.

The contribution is the tested combination of source verification, controlled
variants/holdout, real converter routes, feature-specific equivalence,
abstention, mutation tests, and provenance—not a claim to be the first
accessibility benchmark or first document-conversion study.

Primary references: [Sperberg-McQueen](https://www.ijdc.net/index.php/ijdc/article/download/179/238/760), [Roig & Ribera](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf), [SciA11y](https://arxiv.org/abs/2105.00076), [iTagPDF](https://itagpdf.com/), [Kumar et al.](https://doi.org/10.1145/3663547.3746380), [DAISY conversion benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/), [DocAccessible research](https://docaccessible.com/research), [ATAG 2.0](https://www.w3.org/TR/ATAG/Overview.html), [Section 508 PDF guidance](https://www.section508.gov/create/pdfs/), [EN 301 549 transformation text](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.01.01_20/en_301549v030101a.pdf), and [Microsoft Word PDF accessibility](https://learn.microsoft.com/en-us/office/pdf/word/wordpdfaccessibility).
