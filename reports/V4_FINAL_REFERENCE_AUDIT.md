# V4 final reference-integrity audit

Audit date: 2026-10-04. The bibliography used by the final build is `submission/ICST2027_V4/references.bib`, copied from the previously audited V3 reference set and extended with the oracle/metamorphic/format-conversion sources required by the expanded V4 paper. The final IEEE bibliography contains 13 cited entries; unused converter-help entries remain available in the source bibliography but are not emitted by BibTeX.

Metadata and claim support were checked against the official URL or DOI URL recorded for each entry. DOI redirects were used where available; the final PDF’s references show the DOI/URL supplied by the bibliography. The official pages for ATAG, Section 508, EN 301 549, DAISY, and DocAccessible were directly reachable on the audit date.

| Key | Bibliographic identity checked | DOI / official URL | Claim supported in manuscript |
|---|---|---|---|
| `atag20` | Richards, Spellman, Treviranus; *Authoring Tool Accessibility Guidelines (ATAG) 2.0*; W3C Recommendation, 2015 | https://www.w3.org/TR/ATAG20/ | Accessibility information should be preserved when an equivalent destination mechanism exists, or authors should be warned/prompted. |
| `section508` | U.S. Access Board; *Revised 508 Standards and 255 Guidelines*; 2017 | https://www.access-board.gov/ict/ | Preservation of accessibility information during format conversion. |
| `etsi301549` | ETSI; *EN 301 549 V3.2.1: Accessibility Requirements for ICT Products and Services*; 2021 | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf | Related transformation/preservation requirement. |
| `roig2015` | Roig and Ribera; accessible EPUB creation by nontechnical users; Interacción 2015, 2015 | DOI: 10.1145/2829875.2829926; https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf | Office-document conversion can have accessibility consequences; distinction is EPUB versus DOCX-to-PDF and method. |
| `barr2015oracle` | Barr, Harman, McMinn, Shahbaz, Yoo; *The Oracle Problem in Software Testing: A Survey*; IEEE TSE 41(5), 2015, 507–525 | DOI: 10.1109/TSE.2014.2372785 | Oracle uncertainty motivates an explicit evidence boundary. |
| `segura2016metamorphic` | Segura, Fraser, Sanchez, Ruiz-Cortes; *A Survey on Metamorphic Testing*; IEEE TSE 42(9), 2016, 805–824 | DOI: 10.1109/TSE.2016.2532875 | Metamorphic testing is related prior testing strategy, not the primary V4 oracle. |
| `sperberg2011conversion` | Sperberg-McQueen; *What Constitutes Successful Format Conversion?*; International Journal of Digital Curation 6(1), 2011 | DOI: 10.2218/ijdc.v6i1.179 | Conversion requires a declared notion of what must be preserved. |
| `wang2021scia11y` | Wang et al.; *SciA11y: Converting Scientific Papers to Accessible HTML*; ASSETS ’21, 2021, 1–4 | DOI: 10.1145/3441852.3476545 | Destination generation from scientific PDFs, distinguished from source-grounded DOCX-to-PDF preservation. |
| `mowar2026` | Mowar, Steinfeld, Bigham; *iTagPDF: Towards Finally Automating PDF Accessibility*; CHI ’26, 2026, 1–17 | DOI: 10.1145/3772318.3790289 | PDF tagging/accessibility automation context, distinguished from preservation testing. |
| `kumar2025` | Kumar, Padath, Wang; *Benchmarking PDF Accessibility Evaluation*; ASSETS ’25, 2025, 1–24 | DOI: 10.1145/3663547.3746380 | Automated/LLM-based PDF accessibility evaluation context. |
| `daisy2026` | DAISY Consortium AI Special Interest Group; *PDF Conversions Put to the Test*; DAISY Technical Meeting, 2026 | https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/ | Shared-criteria conversion benchmark context; not used as V4 ground truth. |
| `docaccessible2026` | DocAccessible; *The Accessible HTML Conversion Benchmark*; 2026 | https://docaccessible.com/research/accessible-html-conversion-benchmark | Source-grounded PDF-to-HTML benchmarking context. |
| `docaccessible-google` | DocAccessible; *Google Docs to Accessible PDF: What the Export Tags Now, and What You Still Have to Check*; 2026 | https://docaccessible.com/guides/google-docs-to-accessible-pdf | Practical Google Docs export context; not an independent V4 result source. |

The final paper does not cite the stale V1/V2 result reports, does not claim the cited works are strawmen, and does not claim first-ever accessible-conversion research. No citation key is unresolved in the final three-pass MiKTeX build.
