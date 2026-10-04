# Prior-art and novelty audit

This audit uses the repository's cited literature plus a current web check of the closest public materials. The surviving contribution is narrow and makes no first/unique/no-prior-work claim.

| Work | Source → destination | Main goal | Difference from A11yPreserve |
|---|---|---|---|
| Roig & Ribera | Office documents → EPUB | Study accessibility and preservation in office-to-EPUB conversion | Similar transformation concern, but not this controlled DOCX→PDF contract benchmark. |
| SciA11y | Scientific PDF → accessible HTML | Reconstruct an accessible representation and support users | Destination reconstruction/user-facing system, not source-contract preservation testing. |
| iTagPDF | LaTeX/source cues + rendered PDF → tagged PDF | Automated PDF tagging/remediation | Generates or repairs destination metadata; A11yPreserve measures whether known DOCX semantics survive named conversion pipelines. |
| Kumar et al. | Scholarly PDFs | Expert-validated destination accessibility benchmark | Destination-only PDF evaluation with expert annotations, not paired DOCX source oracles. |
| DAISY PDF conversions benchmark | PDF → accessible documents | Compare conversion services on structure/content capture | Benchmarking conversion services, but not the same DOCX source-grounded contract and abstaining equivalence procedure. |
| DocAccessible | PDFs → HTML/accessibility workflows | Public fidelity measurement and remediation/conversion research | Strongest current conceptual threat: evidence-traceable conversion benchmarking. A11yPreserve differs in the fixed DOCX source, OOXML oracle, PDF destination, feature contract, and explicit uncertainty taxonomy. |
| ATAG 2.0 / Section 508 / EN 301 549 | Requirements/guidance | Motivate preservation of accessibility information during transformations | Normative motivation, not an empirical source-to-PDF test harness. |

The exact distinction is therefore: controlled DOCX inputs whose selected accessibility semantics are independently source-verified, named DOCX-to-PDF systems under test, feature-specific cross-format contracts, parser-triangulated destination evidence, and conservative abstention when equivalence is not established. That is a protocol/benchmark distinction, not a claim that conversion preservation or PDF accessibility benchmarking is new.

Current materials checked include [ATAG 2.0 transformation guidance](https://www.w3.org/TR/IMPLEMENTING-ATAG20/), [DocAccessible research](https://docaccessible.com/research), the [DAISY PDF-conversion benchmark](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/), [iTagPDF](https://doi.org/10.1145/3772318.3790289), and the [Kumar PDF accessibility benchmark](https://doi.org/10.1145/3663547.3746380). The manuscript must retain the bounded novelty wording.
