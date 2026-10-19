# 1. Bottom line

**DISTINCTION IS CLEAR** after small reviewer-facing wording repairs. The
paper now states explicitly that A11yPreserve tests accessibility semantics
through machine-observable source and PDF evidence, uses feature-specific
cross-format equivalence rules, and abstains when the evidence cannot support
a defensible decision. No experiment, frozen result, classification, or
unresolved-case taxonomy changed.

# 2. What A11yPreserve actually measures

A11yPreserve measures whether selected accessibility-relevant properties and
relationships encoded in controlled DOCX source contracts have a defensible
semantic realization in the tagged PDF produced by one of the two tested
conversion pipelines. The test input is the DOCX fixture, the system under test
is the named conversion pipeline, the oracle is the source contract, and the
comparator evaluates destination evidence against the contract. It is not a
complete PDF accessibility validator or an end-user accessibility study.

# 3. Semantic vs syntactic distinction

Accessibility semantics are the intended properties or relationships, not a
particular OOXML element, PDF tag, or byte sequence. Machine-observable
structure is evidence used to test those properties. Some mappings are direct;
others require normalization or feature-specific equivalence rules. Therefore
different syntax can preserve meaning, while a destination tag with the right
name can still be insufficient if it does not establish the source
relationship.

# 4. Machine-verifiable feature categories

The detailed feature inventory is in
`docs/SEMANTIC_MEASUREMENT_BOUNDARY.md`. The classification is:

| Category | Meaning | A11yPreserve examples |
|---|---|---|
| A | Directly machine-verifiable semantic property with minimal normalization | document language; clear heading role; explicit alternative-text value |
| B | Machine-verifiable through a documented semantic mapping | heading hierarchy; lists; tables and headers; inline language; links; title metadata; footnotes; equations; captions |
| C | Not reliably machine-resolvable under current evidence for the affected case | unresolved list item/type correspondence; multi-level table association; B11 note mapping; equation token identity; figure-caption association |

Category C is a measurement boundary, not a statement that the underlying
semantic is inherently non-computational.

# 5. Measurement coverage vs preservation outcome

The method first asks whether the evidence supports a defensible equivalence
judgment. Only determinate cases receive `VERIFIED_PRESERVED`,
`OBSERVED_PARTIAL`, `ALTERED`, or `CONFIRMED_LOST`. `UNRESOLVED_EQUIVALENCE`
and `MEASUREMENT_ERROR` remain explicit coverage/measurement outcomes. The
frozen primary count is 18 unresolved of 52; the separate additive analysis
resolved four hyperlink rows and leaves 14 unresolved. These denominators are
not silently combined.

# 6. Interpretation of unresolved cases

The current additive taxonomy is unchanged:

- 11 representability ambiguities;
- 2 semantic-equivalence ambiguities; and
- 1 extraction limitation.

The four hyperlink cases moved from unresolved to determinate only after an
independent deterministic URI/geometry/text check supplied the missing visible
name association. The remaining 14 were independently inspected with pypdf
and PyMuPDF and retained as abstentions. They are not automatically converter
failures or losses.

# 7. Why abstention is scientifically necessary

Abstention protects against both false preservation and false loss. A PDF may
contain related tags or visible text while omitting the relationship needed by
the source contract, and it may encode an equivalent relationship in a form a
particular extractor does not expose. Calling every such case `LOST` would
conflate non-observability with semantic loss. The additive hyperlink result
also shows that abstention is responsive to stronger evidence rather than a
fixed refusal to decide.

# 8. Why presence-only checking is insufficient

The presence-only baseline found feature-shaped destination structure in 16 of
the 18 frozen unresolved rows. This does not establish preservation: presence
does not verify source values, item identity, scope, order, or association.
The baseline therefore supports the need for source-grounded semantic
comparison, but is not presented as a comparison against every PDF/UA
validator.

# 9. End-user accessibility boundary

The results concern preservation of selected machine-verifiable accessibility
semantics. They do not establish equivalent assistive-technology behavior,
screen-reader usability, task completion, perceived accessibility, or user
impact. Semantic preservation is relevant structural evidence, not a guarantee
of equivalent end-user experience.

# 10. Reviewer attacks and defenses

| Attack | Defense | Current support |
|---|---|---|
| “If semantics require interpretation, how can an automated oracle judge them?” | The oracle tests explicit contracts using structured evidence and documented feature-specific equivalence rules; it abstains at the evidence boundary. | Supported after the methodology repair. |
| “You are only checking tags, not meaning.” | Tags are evidence, not the definition of meaning. The comparator also uses values, relationships, annotations, text, geometry, and normalization. | Supported; presence-only is explicitly identified as insufficient. |
| “Fourteen unresolved cases make the method incomplete.” | They bound measurement coverage and identify representation/equivalence limits; forcing outcomes would reduce validity. | Supported, with the 18-versus-14 distinction explicit. |
| “Why not call unresolved cases failures?” | A failure claim requires evidence that a representable contracted property is absent; unresolved cases do not meet that evidentiary standard. | Supported by the taxonomy and loss definitions. |
| “Why does this matter without a screen reader?” | The contribution is machine-verifiable preservation testing, useful for regression and conversion analysis; the paper explicitly does not claim user-equivalence. | Supported by methodology, discussion, and threats. |

# 11. Manuscript changes made

- Added explicit semantic-measurement-boundary wording to the methodology's
  opening framing.
- Defined accessibility semantics, machine-observable evidence, and the
  two-stage measurement/outcome decision.
- Clarified in results that preservation labels apply only to determinate
  cases and that 18 frozen versus 14 additive unresolved rows are separate.
- Added threats-to-validity wording distinguishing semantic properties from
  their extracted evidence and rejecting syntax-equality reasoning.
- Updated the artifact README to use the same boundary terminology.
- Added this audit and the feature-level boundary document.

# 12. Did any scientific result change?

**No.** Frozen primary outputs, classifications, hashes, contracts, and the
14-case additive taxonomy are unchanged.

# 13. Final recommended terminology

- **Accessibility semantic:** a meaningful accessibility-relevant property or
  relationship.
- **Machine-observable evidence:** structured, textual, annotation, metadata,
  or geometric evidence exposed by a representation.
- **Semantic equivalence:** an accepted feature-specific correspondence
  between source contract meaning and destination realization.
- **Measurement coverage:** whether a defensible decision can be made.
- **Determinate:** a case with sufficient evidence for a preservation outcome.
- **Unresolved / abstention:** insufficient evidence for a defensible
  equivalence judgment; not automatically loss.
- **Lost:** independently supported absence of a required, representable
  destination realization.
- **End-user accessibility:** usability or assistive-technology experience,
  which is outside this study.

# 14. Submission impact

**Resolved.** This was a conceptual and terminology risk, not a frozen-science
or artifact-integrity blocker. The paper now makes the measurement boundary
explicit while retaining the principled unresolved cases and the boundary
between structural semantic preservation and end-user accessibility.
