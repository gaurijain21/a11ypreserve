# V6 reference audit

Recorded 2026-10-19. This audit covers metadata and source-level support; it
does not replace an author's final reading of every cited source.

## Structural checks

- 13 unique citation keys occur in the manuscript.
- All 13 keys resolve to `references.bib`.
- All 13 entries contain author, title, year, and a URL or DOI.
- Three unused legacy entries were removed from the V6 bibliography.
- The title of Sperberg-McQueen's article was corrected to include the verified
  subtitle, “Towards a Formalization of Intellectual Content.”
- The final LaTeX build has no unresolved citation or reference diagnostics.

## Source checks

| Keys | Check | Result |
|---|---|---|
| `atag20` | W3C technical report, authors, 2015 recommendation, and URL | Verified against the W3C recommendation: <https://www.w3.org/TR/ATAG20/> |
| `section508` | U.S. Access Board title and preservation provision | Verified against the official ICT page: <https://www.access-board.gov/ict/> |
| `etsi301549` | ETSI EN 301 549 V3.2.1, 2021, PDF URL | Verified against the ETSI PDF: <https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf> |
| `roig2015` | Authors, Spanish title, 2015 proceedings, DOI | Metadata and the office-to-EPUB accessibility claim verified against the proceedings PDF: <https://aipo.es/wp-content/uploads/2023/04/actas_interaccion_2015.pdf> |
| `barr2015oracle` | IEEE TSE volume, issue, pages, year, DOI | DOI and title/authors verified through the UCL record: <https://discovery.ucl.ac.uk/id/eprint/1471263/> |
| `segura2016metamorphic` | IEEE TSE volume, issue, pages, year, DOI | DOI, title, and survey scope verified against the authors' publication record: <https://www.isa.us.es/publications/type/article-journal/2016/survey-metamorphic-testing> |
| `sperberg2011conversion` | IJDC volume, issue, year, DOI, full title | DOI, issue, year, and full title verified against the journal record: <https://www.ijdc.net/index.php/ijdc/article/download/179/238/760> |
| `wang2021scia11y` | ASSETS '21, four pages, authors, DOI | Metadata and PDF-to-accessible-HTML scope verified against the author-hosted paper: <https://llwang.net/assets/pdf/2021_wang_scia11ydemo_assets.pdf> |
| `mowar2026` | CHI '26, authors, DOI, 17-page record | Metadata verified against the author-maintained page and ACM DOI record: <https://peyajm29.github.io/itagpdf.html> |
| `kumar2025` | ASSETS '25, authors, 24 pages, DOI | Metadata and benchmark scope verified against the ACM record: <https://doi.org/10.1145/3663547.3746380> |
| `daisy2026` | 2026 technical-meeting page | Verified against the DAISY page: <https://daisy.org/activities/projects/ai-special-interest-group/pdf-conversions-put-to-the-test/> |
| `docaccessible2026`, `docaccessible-google` | Current web resources and titles | URLs resolve as the cited web resources; authors should still confirm that each surrounding manuscript sentence is appropriately characterized as web guidance rather than peer-reviewed evidence. |

## Remaining author-only check

The machine and source audit cannot decide whether every sentence's strength is
exactly warranted by its cited source. The author should read the 13 cited
sources once before submission and confirm the claim-to-source mapping.
