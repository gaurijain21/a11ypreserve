# V5 footnote oracle hardening

## Finding

The V4 evidence does not support converting footnote uncertainty into a pass
or loss. LibreOffice outputs contain `/Note` structure, while the current
marked-content path does not reliably recover the reference-to-body identity.
Google outputs retain visible reference/note text but the saved evidence does
not establish a machine-verifiable association. Word outputs had the same
measurement-boundary pattern. A `/Note` node alone is not a preserved
footnote.

## V5 action

The V5 specification now requires all of: reference evidence, `/Note` role (or
documented equivalent), note body, and identity mapping. Raw-object evidence,
structure-tree traversal, link/annotation inspection, parent-tree/marked
content checks, and page-text evidence are retained separately. No existing
V4 label is changed by this report. Dedicated regression fixtures and
destination mutants are included in the V5 mutation manifest; attempts that
cannot produce a valid, interpretable PDF are recorded as invalid/unsupported
rather than classified.

## Resulting interpretation

The correct V5 outcome is reduced overclaiming, not an artificially lower
uncertainty count. Footnotes remain `MEASUREMENT_ERROR` or
`UNRESOLVED_EQUIVALENCE` unless the complete association is independently
recoverable. This is a deliberate oracle-hardening result.
