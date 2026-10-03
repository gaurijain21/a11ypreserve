# Final Feature Results

| Fixture | Accessibility property | LibreOffice | Google Docs | Key observation |
|---|---|---|---|---|
| F01 | Heading hierarchy | PRESERVED | PARTIALLY_PRESERVED | Google Docs adds an extra H1. |
| F02 | Image alternative text | ALTERED | PRESERVED | LibreOffice prefixes the author string; Google Docs retains it. |
| F03 | List semantics | PRESERVED | PARTIALLY_PRESERVED | Google Docs lacks independently established list type. |
| F04 | Table/header structure | PRESERVED | PRESERVED | Table, cells, and header roles are retained. |
| F05 | Document language | PRESERVED | ALTERED | Google Docs emits `en` rather than `en-US`. |
| F06 | Inline language change | PRESERVED | LOST | Google Docs lacks the source inline `/Lang` span. |
| F07 | Decorative image state | PARTIALLY_PRESERVED | PARTIALLY_PRESERVED | Empty-alt evidence does not establish explicit artifact state. |
| F08 | Hyperlink semantics | PARTIALLY_PRESERVED | PARTIALLY_PRESERVED | URI/annotation survives; accessible-name association is incomplete. |
| F09 | Document title/metadata | PRESERVED | ALTERED | Google Docs changes the metadata title value. |
| F10 | Multi-level table headers | PRESERVED | PARTIALLY_PRESERVED | Google Docs does not establish complete associations. |
| F11 | Footnote association | MEASUREMENT_ERROR | LOST | LibreOffice `/Note` association is unresolved; Google Docs has no recovered note structure. |
| F12 | Equation/math semantics | PRESERVED | PARTIALLY_PRESERVED | Google Docs retains visible text without machine-readable math structure. |
| F14 | Figure/caption association | PRESERVED | PARTIALLY_PRESERVED | Google Docs retains caption text but only adjacency establishes association. |

The table is feature-specific and does not rank converters.
