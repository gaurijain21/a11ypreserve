# V5 attribute-scope decision

| Candidate | Decision | Justification |
|---|---|---|
| Existing 13 families | GO | Each has a verified DOCX contract and a feature-specific PDF evidence boundary. |
| Reading order | DEFER | No defensible source-to-destination oracle across floating/layout constructs; see feasibility report. |
| Bookmarks / TOC / internal navigation | DEFER | Promising authored navigation property, but current frozen source contracts do not independently establish TOC/bookmark intent and destination identity across all variants. |
| Repeated page furniture / artifacting | DEFER | Requires page-layout and artifact boundary ground truth not present in the atomic corpus. |
| Unicode/text extraction/ActualText | DEFER | Fits preservation, but needs a dedicated source token and glyph/ActualText oracle rather than visible-text comparison. |
| Comments/annotations | DEFER | Destination semantics and export policy differ from the current accessibility contracts. |
| Form controls/content controls | DEFER | Requires a separate interactive-widget contract and behavior oracle. |
| Color contrast/font-size scoring | REJECT | Broad visual accessibility properties are outside the authored semantic-preservation question and would require a different construct. |

Fewer strong, source-grounded attributes are preferred to a larger benchmark
with weak or human-inferred equivalence rules.
