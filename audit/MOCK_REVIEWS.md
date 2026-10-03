# Mock Hostile Reviews

## Reviewer A — Accessibility / ASSETS

### Strengths
The source-grounded distinction between preservation fidelity and destination accessibility is valuable; alt text, language, lists, tables, and notes are accessibility-relevant.

### Major concerns
There is no disabled-user evaluation; synthetic one-page fixtures may not predict real screen-reader experience; some “partial” findings are parser/representation limits rather than user-observed failures.

### Minor concerns
No audio/interaction test, limited locale diversity, no reading-order fixture, and no validator triangulation.

### Questions
Which findings change a screen-reader user's task? Which semantic mutations remain usable?

### Likely recommendation
Weak accept/revise if claims remain methodological and feature-specific; reject if framed as a comprehensive accessibility evaluation.

## Reviewer B — Document Engineering / DocEng

### Strengths
Frozen OOXML manifests, real conversion engines, tagged-PDF object inspection, and reproducible hashes are strong engineering artifacts.

### Major concerns
Google Docs is cloud-versioned; only two engines and one instance per feature are tested; PDF equivalence is not uniform; F11 remains unresolved; Google import and export stages are confounded.

### Minor concerns
No Word denominator, no ODT source, limited page complexity, and parser dependence on pypdf.

### Questions
How are role mappings, inheritance, text spans, `/Scope`, `/ActualText`, and artifact semantics independently verified?

### Likely recommendation
Accept as a scoped benchmark/measurement paper after clarifying unsupported equivalence claims and adding comparator regression cases.

## Reviewer C — Software Testing

### Strengths
The oracle is explicit, hashes and evidence are retained, and the design is naturally differential.

### Major concerns
26 rows are not a statistical sample; feature-level units have unequal complexity; the comparator has a list-order/text-association hardening gap; test cases are mostly synthetic.

### Minor concerns
Freeze did not record a test-result hash; no automated rerun of Google Docs; no mutation testing of the extractor.

### Questions
Can a reordered list or duplicate node be detected? Can missing parser output be distinguished from missing destination semantics?

### Likely recommendation
Minor revision, not additional large-scale data collection, if scope and test-oracle limits are explicit.
