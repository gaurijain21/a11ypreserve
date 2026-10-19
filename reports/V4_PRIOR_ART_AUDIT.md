# V4 Prior-Art Audit

Audit date: 2026-10-04. The audit deliberately rejects a “first accessibility conversion study” claim.

| Work | Source → destination/task | Dataset/ground truth | Oracle/evaluation | Difference from A11yPreserve |
|---|---|---|---|---|
| [Roig & Ribera, 2015](https://doi.org/10.1145/2829875.2829926) | office documents → EPUB accessibility conversion | office-document examples; accessibility criteria aligned with ATAG 2.0 | quantitative conversion evaluation | closest direct preservation precedent, but different target format and no demonstrated DOCX source-contract → tagged-PDF evidence protocol |
| [SciA11y, Wang et al., 2021](https://doi.org/10.1145/3441852.3476545) | PDF → accessible HTML | large scholarly PDF corpus and extraction evaluation | intrinsic extraction/readability evaluation plus user study | generation/remediation in the opposite direction; not testing whether a known DOCX semantic survived conversion |
| [iTagPDF, Mowar et al., 2026](https://doi.org/10.1145/3772318.3790289) | source cues/rendered PDF → automated PDF accessibility metadata | research-paper examples | tagging/metadata quality and source-plus-visual modeling | uses source semantics to improve tagging, but is a remediation/generation system rather than a comparative DOCX-to-PDF preservation test |
| [Kumar, Padath & Wang, 2025](https://doi.org/10.1145/3663547.3746380) | destination PDF accessibility evaluation | expert-annotated scholarly PDFs across seven criteria | Passed/Failed/Not Present/Cannot Tell; checker and LLM comparison | destination-only benchmark; no paired known source contract or transformation relation |
| [DAISY AI SIG, 2026](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/) | PDF → accessible output across seven services | four criterion-stressing documents | shared framework and consensus scoring | strong current conversion benchmark precedent, but opposite direction and no frozen DOCX source oracle |
| [Barr et al., 2015](https://doi.org/10.1109/TSE.2014.2372785) | software-testing oracle problem | survey | specifications, contracts, metamorphic and other oracle strategies | motivates contracts and abstention; V4 applies the oracle problem to cross-format semantic equivalence |
| [Segura et al., 2016](https://doi.org/10.1109/TSE.2016.2532875) | metamorphic testing | literature survey | relations between executions to reduce oracle cost | informs mutation and relation thinking; V4 remains source-contract based and does not claim metamorphic completeness |
| [ATAG 2.0](https://www.w3.org/TR/ATAG20/) | authoring-tool accessibility | normative guidance | conformance-oriented authoring guidance | standards context and feature relevance; not an empirical DOCX-to-PDF conversion oracle |
| [EN 301 549](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/04.01.00_20/en_301549v040100ev.pdf) | ICT accessibility requirements | normative standard | requirements/conformance | scope context; V4 is not a claim of EN 301 549 or PDF/UA completeness |

## Surviving contribution claim

A11yPreserve should claim a bounded empirical testing contribution: a prospective, source-grounded protocol that combines controlled known DOCX semantics, feature-level preservation contracts, raw-OOXML source verification, identical inputs across converter conditions, destination structure evidence, explicit equivalence mappings, calibrated conservative abstention, and provenance certificates. The defensible distinction is not that accessibility-aware conversion research is new; it is that the method asks whether a particular author-supplied semantic known to exist before transformation survived that transformation, whereas destination-only evaluation asks what accessibility structure exists after transformation.

## Threats exposed by the audit

The literature makes clear that external validity, destination-only baselines, user impact, and converter coverage remain distinct questions. V4 therefore keeps standards completeness, assistive-technology behavior, usability, and prevalence outside its claims. The current V4 artifact is not submission-ready because no legitimate V4 converter run was available in the recorded environment.
