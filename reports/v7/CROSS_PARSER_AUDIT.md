# Cross-parser audit

`python scripts/v7_cross_parser_audit.py` compared fresh pypdf structure-role
counts with archived PyMuPDF serialized-marker counts for 195 cases.

| Metric | Count |
|---|---:|
| Cases | 195 |
| Marker comparison units | 2,145 |
| Units with differing counts | 275 |
| Cases with at least one difference | 195 |

The disagreement is an extraction diagnostic, not a correctness score. The two
parsers traverse different object boundaries and expose different views of the
PDF. It supports retaining multiple evidence paths and explicit measurement
error/abstention rather than treating one parser's output as complete truth.
