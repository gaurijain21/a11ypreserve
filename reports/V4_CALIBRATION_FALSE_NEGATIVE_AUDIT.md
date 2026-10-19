# V4 Calibration False-Negative Audit

This is a post-freeze diagnostic audit. The frozen 78-control calibration result and all frozen V4 classifications are unchanged.

The five false negatives are:

| Control | Family | Expected | Observed | Cause |
|---|---|---|---|---|
| decorative_images_alternate | decorative image | EQUIVALENT | PARTIAL | Empty alt text was represented as a Figure; no explicit PDF Artifact evidence was established. |
| hyperlinks_exact | hyperlinks | EQUIVALENT | PARTIAL | URI/annotation survived, but visible link-name association was not independently recoverable. |
| hyperlinks_alternate | hyperlinks | EQUIVALENT | PARTIAL | Same evidence boundary as the exact hyperlink control. |
| complex_tables_exact | complex tables | EQUIVALENT | PARTIAL | Header roles survived, but complete multi-level associations were not established. |
| complex_tables_alternate | complex tables | EQUIVALENT | PARTIAL | Same association-evidence limitation as the exact control. |

## Findings

These are conservative false negatives, not unsupported confident positives. The controls intentionally expose accepted cross-format evidence limits: a URI is not by itself a visible-name relation, a Figure with empty alt is not proof of a PDF Artifact, and header roles are not proof of complete multi-level associations. No comparator implementation bug was identified. No expected labels were changed and no diagnostic fix was promoted into the primary result.

Frozen calibration remains: 60 correct, 0 false positives, 5 false negatives, 13 correct abstentions, and 0 unsupported confident classifications.
