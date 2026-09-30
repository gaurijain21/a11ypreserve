# Research Gap

## Defensible gap

Existing work establishes conversion loss, output accessibility evaluation, PDF remediation, and destination-specific standards. The unresolved methodological gap is a compact, reproducible way to test source-author semantics across a named conversion edge while separating true preservation from degradation, mutation, regeneration, unsupported representation, invalid conversion, and inability to measure.

## Hypotheses

- H1: Semantic fixtures with independent manifests expose failures that visual/text-only comparison misses.
- H2: Conversion results vary materially by engine even for the same source and destination.
- H3: A provenance-aware taxonomy reduces false claims of either preservation or loss compared with binary output checking.
- H4: Source semantics that have no equivalent destination mechanism are predictable when capability declarations are explicit.

## Boundaries

The main study should not include arbitrary web pages, every office suite, untagged scans, or user-facing remediation. PDF is one constrained endpoint, not the whole project. The first paper should use controlled semantic fixtures and a small number of conversion routes.

## Falsifiers

Kill the narrowed project if: two independent engines show no differential failures across the fixture set; source manifests cannot be validated independently; manual/AT checks disagree systematically with the declared outcome model; or the method adds no information beyond existing DAISY/DocAccessible-style scores.

