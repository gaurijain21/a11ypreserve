# Secondary parser audit

This additive audit reads the frozen PDFs with pypdf, PyMuPDF, and pdfplumber when available. It does not edit the frozen result record.

- Rows audited: 14
- Resolved by this audit: 0
- Remaining abstentions: 14
- Parser set: pypdf, PyMuPDF, pdfplumber-unavailable

## Decision

The independent parsers expose additional structure and text evidence, but no general standards-grounded equivalence relation sufficient to resolve the full source contracts. The 14 additive abstentions are retained.

## Rows

| Fixture | Pipeline | Reason | Pages | PDF roles | Links | Decision |
|---|---|---|---:|---|---:|---|
| F03_LISTS | Google Docs | target-format representability ambiguity | 1 | /Document:1, /H1:1, /L:3, /LBody:1, /LI:7, /P:3 | 0 | retain abstention |
| F10_COMPLEX_TABLE | Google Docs | target-format representability ambiguity | 1 | /Document:1, /H1:1, /P:16, /TD:9, /TH:5, /TR:5, /Table:1 | 0 | retain abstention |
| F12_EQUATION | Google Docs | target-format representability ambiguity | 1 | /Document:1, /H1:1, /P:2, /Span:2 | 0 | retain abstention |
| F14_CAPTIONS | Google Docs | target-format representability ambiguity | 1 | /Document:1, /Figure:1, /H1:1, /P:3, /Span:1 | 0 | retain abstention |
| B03 | LibreOffice | extraction incomplete / target-format representability ambiguity | 1 | /Document:1, /L:4, /LBody:5, /LI:5, /Lbl:5, /Standard:5, /Title:1 | 0 | retain abstention |
| B03 | Google Docs | extraction incomplete / target-format representability ambiguity | 1 | /Document:1, /H1:1, /L:6, /LI:7 | 0 | retain abstention |
| B04 | LibreOffice | semantic-equivalence ambiguity | 1 | /Document:1, /Standard:16, /TD:12, /TH:4, /TR:4, /Table:1, /Title:1 | 0 | retain abstention |
| B04 | Google Docs | semantic-equivalence ambiguity | 1 | /Document:1, /H1:1, /P:17, /TD:12, /TH:4, /TR:4, /Table:1 | 0 | retain abstention |
| B10 | LibreOffice | target-format representability and semantic-equivalence ambiguity | 1 | /Document:1, /Standard:18, /TD:12, /TH:6, /TR:5, /Table:1, /Title:1 | 0 | retain abstention |
| B10 | Google Docs | target-format representability and semantic-equivalence ambiguity | 1 | /Document:1, /H1:1, /P:19, /TD:12, /TH:6, /TR:5, /Table:1 | 0 | retain abstention |
| B11 | LibreOffice | extraction limitation | 1 | /Div:1, /Document:1, /Lbl:2, /Link:4, /Note:2, /Standard:3, /Title:1 | 0 | retain abstention |
| B12 | LibreOffice | target-format representability and semantic-equivalence ambiguity | 1 | /Document:1, /Formula:2, /Standard:3, /Title:1 | 0 | retain abstention |
| B12 | Google Docs | target-format representability ambiguity | 1 | /Document:1, /H1:1, /P:3, /Span:4 | 0 | retain abstention |
| B13 | Google Docs | target-format representability ambiguity | 1 | /Document:1, /Figure:2, /H1:1, /P:5, /Span:2 | 0 | retain abstention |
