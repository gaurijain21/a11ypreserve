# Comparator Robustness Audit

Existing tests cover the frozen taxonomy cases: exact preservation, semantic equivalence, partial preservation, mutation, regeneration, loss, not-representable, measurement error, and invalid conversion. The real matrix also exercises extra heading structure, missing list type, missing inline language, missing `/Note`, `/Formula` vs visible-text math, `/Caption` vs adjacency, and `/Scope` differences.

A Phase 6 hostile regression suite was added and passed 17 cases, including taxonomy, extra/duplicated headings, list reordering and duplication, alt-text mutation, missing inline language, and missing hyperlinks. Its output is `audit/phase6_comparator_tests.json`. The list comparator now checks item-text order when both source and destination extractors provide item text. The frozen LibreOffice PDF exposes list structure but not item text in the current marked-content extraction, so its preserved F03 result remains based on structural evidence plus independent page-text corroboration; lack of text association is retained as a documented measurement limit rather than silently treated as proof of item identity.

The comparator does not equate every string match with preservation, does not treat missing parser output as loss for F11 LibreOffice, and does not treat extra heading structure as harmless.
