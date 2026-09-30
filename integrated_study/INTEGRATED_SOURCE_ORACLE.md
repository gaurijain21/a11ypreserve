# Integrated source-oracle audit

The separate ZIP/XML verifier checked 21/21 integrated source contracts. It does not import the integrated-document generator, ASIR, or the frozen comparator.

| Document | Instance | Feature | Status | Observation |
|---|---|---|---|---|
| I01_REALISTIC_REPORT | I01-heading-hierarchy | headings | PASS | heading levels=[1, 1, 2, 2, 1, 1, 1] |
| I01_REALISTIC_REPORT | I01-alternative-text | image_alt_text | PASS | image descriptions=['A simple upward trend showing completed appointments increasing from 2024 to 2025.'] |
| I01_REALISTIC_REPORT | I01-lists | lists | PASS | list depths=[0, 0, 1, 1, 0] |
| I01_REALISTIC_REPORT | I01-table-headers | table | PASS | rows=4 headers=['Measure', '2024', '2025'] header_marked=True |
| I01_REALISTIC_REPORT | I01-document-language | document_language | PASS | default language=en-US |
| I01_REALISTIC_REPORT | I01-hyperlink | hyperlinks | PASS | hyperlink targets=['https://www.w3.org/WAI/standards-guidelines/wcag/'] |
| I01_REALISTIC_REPORT | I01-title | document_title | PASS | core title='Community Access Report: Service Improvements and Next Steps' |
| I02_EDUCATIONAL_HANDOUT | I02-heading-hierarchy | headings | PASS | heading levels=[1, 1, 1, 1, 1] |
| I02_EDUCATIONAL_HANDOUT | I02-inline-language | inline_language | PASS | language runs include target=True |
| I02_EDUCATIONAL_HANDOUT | I02-equation | equation | PASS | OMML equations=1 |
| I02_EDUCATIONAL_HANDOUT | I02-footnote | footnotes | PASS | footnote body present=True |
| I02_EDUCATIONAL_HANDOUT | I02-caption | captions | PASS | captions=['Equation 1. A compact expression used in the classroom example.', 'Figure 1. Evidence and conclusion are connected through an explicit reasoning step.'] |
| I02_EDUCATIONAL_HANDOUT | I02-hyperlink | hyperlinks | PASS | hyperlink targets=['https://www.w3.org/WAI/standards-guidelines/wcag/'] |
| I03_POLICY_NOTE | I03-heading-hierarchy | headings | PASS | heading levels=[1, 1, 2, 2, 1, 1, 1, 1] |
| I03_POLICY_NOTE | I03-lists | lists | PASS | list depths=[0, 0, 1, 1, 0, 0, 0] |
| I03_POLICY_NOTE | I03-table-headers | table | PASS | rows=4 headers=['Phase', 'Owner', 'Evidence'] header_marked=True |
| I03_POLICY_NOTE | I03-image-alt | image_alt_text | PASS | image descriptions=['A process diagram showing draft, review, and release stages.', ''] |
| I03_POLICY_NOTE | I03-decorative-image | decorative_image | PASS | image descriptions=['A process diagram showing draft, review, and release stages.', ''] |
| I03_POLICY_NOTE | I03-document-language | document_language | PASS | default language=en-US |
| I03_POLICY_NOTE | I03-inline-language | inline_language | PASS | language runs include target=True |
| I03_POLICY_NOTE | I03-hyperlink | hyperlinks | PASS | hyperlink targets=['https://www.w3.org/WAI/standards-guidelines/wcag/'] |
