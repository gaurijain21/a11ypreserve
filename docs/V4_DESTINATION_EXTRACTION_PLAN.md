# V4 Destination-Extraction Plan

Before any V4 PDF result is analyzed, the output must be retained by hash and extracted through the primary pypdf structure-tree/marked-content/annotation path plus independent evidence where applicable.

| Difficult family | Primary evidence | Corroborating evidence |
|---|---|---|
| hyperlinks | annotations and URI actions | PyMuPDF links and serialized objects |
| lists | `/L`, `/LI`, nesting, `/ListNumbering` | raw objects and text order |
| complex tables | `/Table`, `/TH`, `/TD`, `/Scope`, `/Headers`, spans | raw attributes, parent tree, second parser |
| equations | `/Formula`, alternate text, expression tokens | page text and serialized objects |
| captions | `/Caption`, figure relation, ordered text | marked content and page text |
| footnotes | `/Note`, reference/body correspondence | page text, object scans, second parser |

Absence from one parser is not semantic absence. A conversion case is `CONFIRMED_LOST` only when the frozen comparator has corroborating absence evidence; otherwise it remains unresolved or a measurement error. The plan is ready but unexecuted because no V4 PDF exists.
