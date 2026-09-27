# Novelty Matrix

| Candidate claim | Prior-art status | Decision |
|---|---|---|
| Accessibility can be lost in document conversion | Established by Roig/Ribera and standards guidance | Drop as novelty claim. |
| A general benchmark for accessibility of converted PDFs/HTML | Crowded by SciA11y, ASSETS benchmarks, DAISY and DocAccessible | Drop or make this only background. |
| A checker that reports whether an output is accessible | Existing checker/remediation space | Out of scope. |
| Compare source semantics with output semantics using a fixture manifest | Partial overlap; not clearly established as a common reusable harness | Retain as method contribution. |
| Distinguish preserved source semantics from regenerated AI/heuristic semantics | Under-specified in adjacent work; directly important in current conversion systems | Retain as a central claim. |
| Explicit `MEASUREMENT_ERROR` and `NOT_REPRESENTABLE` states | Needed by standards and observed in pilot; not a claim of universal firstness | Retain as a rigor requirement. |
| Multi-format, multi-engine reproducible evidence package | Valuable but threatened by existing benchmarks | Retain only with a narrow conversion matrix. |

## Surviving contribution statement

This project is publishable only if framed as a provenance-aware differential methodology, validated on a deliberately authored semantic fixture set, with route-specific capability declarations and independent confirmation of ambiguous output semantics. The unit of analysis is the conversion edge and source/output relationship—not the output file alone.

