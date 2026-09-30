# V3 classification decision specification

This specification is an audit artifact for the six-way evidence-aware interpretation. It is not a replacement for the frozen V2 result file.

## Inputs

The classifier consumes one evidence record containing: source-contract status, destination parse status, feature-specific evidence, representability status, independent corroboration, and whether the source and destination values/relationships are directly comparable. Historical outcome labels are not classifier inputs.

## Precedence

Apply the first applicable rule:

1. `MEASUREMENT_ERROR`: the output or relevant extraction is invalid, or a required association cannot be measured after the declared extraction attempts, and the evidence is insufficient to decide preservation or loss.
2. `CONFIRMED_LOST`: the source contract is verified; the required destination representation is representable under the contract; the representation is absent after the declared alternate-representation search; and an independent evidence path corroborates absence.
3. `OBSERVED_PARTIAL`: the contract has multiple required components; at least one required component is directly observed in the destination and at least one other required, representable component is directly demonstrated to differ or be absent. This rule does not apply when the missing component is only unmeasured.
4. `ALTERED`: the conceptual property remains present and measurable, but an author-relevant scalar or value differs from the source contract. `ALTERED` is a fidelity result, not a user-impact judgment.
5. `VERIFIED_PRESERVED`: every required contract component is directly observed or mapped through an explicitly accepted equivalent representation, and the evidence is sufficient for that feature-specific mapping.
6. `UNRESOLVED_EQUIVALENCE`: relevant destination evidence exists or the output is structurally valid, but the available evidence cannot establish equivalence or non-equivalence. This is a conservative abstention, not a loss finding.

If a record satisfies more than one description, precedence is normative. A measurement failure therefore cannot be converted into a loss merely because the visible text looks different; a directly observed component mismatch takes precedence over unresolved equivalence only when the contract requires that component and its absence/difference is actually evidenced.

## Frozen V2 vocabulary mapping

The historical category `PARTIALLY_PRESERVED` is not itself a V3 decision. It is retained as the frozen V1/V2 Core outcome category in provenance. The evidence-status overlay may mark such a row `OBSERVED_PARTIAL` or `UNRESOLVED_EQUIVALENCE`; those labels must remain separate from the historical primary outcome when counts are reported.

