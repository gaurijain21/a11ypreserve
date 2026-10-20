# A11yPreserve V6 final reference audit

Recorded 2026-10-19. The structural checks and source lookups below were
performed against the current 13-entry bibliography. Semantic claim support
still requires an author to read the cited works before submission.

## Structural result

- 13 unique citation keys are used by the manuscript.
- All 13 keys resolve to `submission/ICST2027_V6/references.bib`.
- Every entry has author, title, year, and a DOI or URL.
- The fresh rebuild has no unresolved citation or reference diagnostics.
- Three unused legacy entries were removed; no experimental result depends on
  that cleanup.

## Entry audit

| Key | Type and metadata check | Source check | Claim-support status |
|---|---|---|---|
| `atag20` | W3C ATAG 2.0, 2015 | [W3C recommendation](https://www.w3.org/TR/ATAG20/) | Metadata verified; author claim-strength review required |
| `section508` | U.S. Access Board ICT guidance | [Access Board ICT page](https://www.access-board.gov/ict/) | Metadata and preservation context verified; author review required |
| `etsi301549` | EN 301 549 V3.2.1, 2021 | [Official ETSI PDF](https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf) | Metadata verified; author review required |
| `roig2015` | 2015 proceedings record | [Proceedings PDF](https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf) | Metadata and office-to-EPUB context checked; author review required |
| `barr2015oracle` | IEEE TSE oracle survey record | [UCL repository record](https://discovery.ucl.ac.uk/id/eprint/1471263/) | Metadata verified; author review required |
| `segura2016metamorphic` | IEEE TSE metamorphic-testing survey | [Author publication record](https://www.isa.us.es/publications/type/article-journal/2016/survey-metamorphic-testing) | Metadata verified; author review required |
| `sperberg2011conversion` | IJDC format-conversion article | [Journal record/PDF](https://www.ijdc.net/index.php/ijdc/article/download/179/238/760) | Full title and DOI corrected and checked; author review required |
| `wang2021scia11y` | ASSETS 2021 paper | [Author-hosted paper](https://llwang.net/assets/pdf/2021_wang_scia11ydemo_assets.pdf) | Metadata and scope checked; author review required |
| `mowar2026` | CHI 2026 iTagPDF record | [Author project page](https://peyajm29.github.io/itagpdf.html) and DOI record | Metadata checked; author review required |
| `kumar2025` | ASSETS 2025 PDF accessibility benchmark | [ACM DOI record](https://doi.org/10.1145/3663547.3746380) | Metadata and benchmark scope checked; author review required |
| `daisy2026` | DAISY technical benchmark page | [DAISY project page](https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/) | Web-source status is explicit; author review required |
| `docaccessible2026` | Current web resource | URL resolves in the prior audit | Web guidance, not peer-reviewed evidence; author must confirm wording |
| `docaccessible-google` | Current Google Docs export web resource | URL resolves in the prior audit | Web guidance, not peer-reviewed evidence; author must confirm wording |

## Integrity conclusions

No citation was fabricated by this audit, and no entry was marked as
independently authoritative merely because its DOI resolved. The bibliography
supports the manuscript's bounded motivation and related-work context, but the
author remains responsible for confirming that every surrounding sentence is
supported and for checking the exact final venue requirements.
