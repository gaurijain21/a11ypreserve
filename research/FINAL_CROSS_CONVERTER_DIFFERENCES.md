# Final Cross-Converter Differences

The two tested pipelines differ on 10 of 13 fixture rows. This is not an overall ranking.

| Fixture | Property | LibreOffice | Google Docs | Observed difference | Accessibility information usable? |
|---|---|---|---|---|---|
| F01 | Headings | PRESERVED | PARTIALLY_PRESERVED | Google Docs adds an H1. | Yes, but hierarchy changes. |
| F02 | Alt text | ALTERED | PRESERVED | LibreOffice prefixes the source string. | Yes in both; exact source text only in Google Docs. |
| F03 | Lists | PRESERVED | PARTIALLY_PRESERVED | Google Docs lacks list-type evidence. | Partly in Google Docs. |
| F05 | Document language | PRESERVED | ALTERED | `en-US` becomes `en`. | Yes, with reduced specificity. |
| F06 | Inline language | PRESERVED | LOST | Google Docs lacks inline `es-MX`. | Not established in Google Docs. |
| F09 | Title/metadata | PRESERVED | ALTERED | Google Docs changes title value. | Related metadata remains. |
| F10 | Complex table | PRESERVED | PARTIALLY_PRESERVED | Complete associations are not established in Google Docs. | Partial. |
| F11 | Footnotes | MEASUREMENT_ERROR | LOST | LibreOffice association unresolved; Google Docs has no recovered footnote structure. | Unresolved versus absent. |
| F12 | Equation | PRESERVED | PARTIALLY_PRESERVED | Google Docs retains visible text only. | Visible content remains. |
| F14 | Captions | PRESERVED | PARTIALLY_PRESERVED | Google Docs relies on adjacency. | Text remains; association is weaker. |

The correct unit of interpretation is a named pipeline under a named configuration, not a product-wide winner.
