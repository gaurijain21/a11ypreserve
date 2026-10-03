# V3 within-feature consistency

Comparisons are feature-family observations across Core and Variant B. The two arms have separate denominators; this table does not estimate prevalence.

| Feature | Interpretation |
|---|---|
| Headings | EXACTLY CONSISTENT: both LibreOffice rows are preserved; both Google rows are partial. |
| Alt text | EXACTLY CONSISTENT: LibreOffice alters the author value; Google preserves it. |
| Lists | UNRESOLVED: Core and Variant B Google are unresolved; the Variant B LibreOffice extraction does not establish full text/type equivalence. |
| Table | UNRESOLVED: Variant B destination structure is observed in both pipelines, but full source-cell equivalence is not established. |
| Document language | EXACTLY CONSISTENT: LibreOffice preserves the tested value; Google reduces specificity. |
| Inline language | EXACTLY CONSISTENT: LibreOffice preserves the tested inline languages; Google loses the required inline representations. |
| Decorative image | FIXTURE-SENSITIVE: both Google rows retain the tested decorative state, while the Core Google row is partial and the Variant B LibreOffice row alters it. |
| Links | EXACTLY CONSISTENT AT EVIDENCE LEVEL: all Core and Variant B rows remain unresolved because visible-text association is not established. |
| Document title | EXACTLY CONSISTENT: LibreOffice preserves the tested metadata contract; Google alters/reduces it. |
| Complex table | UNRESOLVED: both Variant B rows remain unresolved on multi-level association equivalence; Core Google is also unresolved. |
| Footnotes | PIPELINE-CONSISTENT BUT LO-UNCERTAIN: Google Core and Variant B are confirmed lost; LibreOffice Core is measurement error and Variant B is unresolved. |
| Equation | UNRESOLVED: the Core and Variant B Google rows remain unresolved; Variant B LibreOffice formula structure is observed without expression equivalence. |
| Captions | FIXTURE-SENSITIVE AT EVIDENCE LEVEL: Variant B LibreOffice preserves Caption structure while Variant B Google remains unresolved on association. |

Unresolved means the available destination evidence did not establish equivalence or non-equivalence under the feature-specific contract. It is not treated as degradation.
