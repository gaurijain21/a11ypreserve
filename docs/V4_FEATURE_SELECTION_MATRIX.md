# V4 Feature-Selection Justification

| Feature | Accessibility relevance | DOCX encoding | PDF encoding | Machine observable | Conversion risk | Prior-art overlap | Included because |
|---|---|---|---|---|---|---|---|
| headings | navigation and structure | paragraph styles | H1-H6 structure elements | level/order/text | hierarchy and flattening | common destination checks | controlled structural contract |
| alternative text | non-text access | drawing description | Figure /Alt or alternate evidence | exact description | deletion/value mutation | PDF accessibility tools | author value is known |
| lists | navigation and grouping | numbering definitions | L/LI/ListNumbering | nesting/order/type | flattening and numbering | destination list checks | source relation is explicit |
| basic tables | data navigation | tbl/tr/tc/header | Table/TH/TD attributes | dimensions/header rows | header loss | table validators | bounded grid contract |
| document language | text interpretation | styles/core language | catalog /Lang | locale | normalization/omission | PDF checkers | document-level semantic value |
| inline language | pronunciation and language switching | run lang | StructElem /Lang or equivalent | span locale | association loss | language checks | source span is controlled |
| decorative images | suppresses non-information | empty/explicit decorative state | Artifact or empty Figure | state plus order | decoration substitution | image checks | distinguishes informative/decorative |
| hyperlinks | navigation | relationship/target | Link annotation/action | URI/count/text where available | target/association loss | link checks | target is exact |
| title/metadata | document identification | core properties/visible title | metadata/catalog | exact title/metadata | normalization | PDF metadata checks | source value is bounded |
| complex tables | multi-level data navigation | spans/header rows | TH/TD spans/headers | structural roles/attributes | association loss | table checks | stresses relationships |
| footnotes | references and supplementary content | footnote parts/refs | Note and page evidence | body/reference | loss/relocation | note checks | difficult source-target mapping |
| equations | mathematical meaning | OMML | Formula or alternate representation | token/expression evidence | flattening/substitution | math accessibility work | native structure is known |
| captions | figure identification | caption paragraph/order | Caption plus figure relation | text/order/association | association loss | image/caption checks | source relation is controlled |

These 13 families cover structure, navigation, metadata, language, image semantics, list semantics, table semantics, associations, and mathematical content. They define benchmark scope, not accessibility-standard completeness.
