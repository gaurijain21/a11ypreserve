# Top 10 Rejection Risks

| Rank | Severity | Argument | Valid? | Minimum response |
|---:|---|---|---|---|
| 1 | CRITICAL | PDF semantic equivalence is not always independently established. | Partly | Mark links/caption adjacency/footnote extraction as measurement-limited; add targeted parser tests before paper. |
| 2 | HIGH | One instance per feature is too small for robust generalization. | Yes | Frame as feasibility/benchmark construction; report feature-level cases and plan justified variants. |
| 3 | HIGH | Google Docs cloud version is not pinned. | Yes | Record exact date/browser/renderer; describe the condition as a cloud pipeline and avoid universal claims. |
| 4 | HIGH | No disabled-user study. | Yes | State that this is a semantic preservation benchmark, not a user-experience study; reserve user evaluation for follow-up. |
| 5 | HIGH | Only two converters and DOCX→PDF. | Yes | Make the scope explicit and position later formats/engines as extensions, not missing prerequisites. |
| 6 | MEDIUM | Google import/export confound. | Yes | Use end-to-end pipeline language; do not attribute every defect to PDF export alone. |
| 7 | MEDIUM | Aggregate counts give unequal features equal weight. | Yes | Feature-level reporting first; descriptive unweighted counts second. |
| 8 | MEDIUM | Comparator may miss list order/duplicate changes. | Yes | Add regression cases and explicit source-text order checks before paper; frozen observed outputs remain independently corroborated. |
| 9 | MEDIUM | F11 measurement error weakens loss claims. | Yes | Keep `MEASUREMENT_ERROR`; do not convert it to loss; report the unresolved structure. |
| 10 | LOW | No PAC/Acrobat/veraPDF analysis. | No for core method | Keep validators secondary/exploratory and report unavailable tools transparently. |

No risk requires a new converter or wholesale corpus rebuild.
