# V6 baseline and ablation report

## Pre-specified comparison protocol

The six executable methods use the same 130 frozen atomic fixture--pipeline inputs. The primary set has no independent adjudicated reference labels, so the report does **not** claim false-preservation or false-loss rates for the primary cases. Instead, it reports observed decisions/abstentions and evaluates fault sensitivity against 59 known applied-and-parseable destination mutations. That mutation oracle is a known injected-fault reference, not a human semantic ground truth.

| Method | Definition |
|---|---|
| PDF tag presence | Tagged flag or `/StructTreeRoot`; no source-specific contract. |
| Visible-text equality | Normalized source visible-text stream found in extracted destination text; no structure/association check. |
| Destination-only evidence | Feature-specific destination role/marker presence without source expectation. |
| A11yPreserve without secondary evidence | Frozen comparator with PyMuPDF/object-marker corroboration suppressed. |
| A11yPreserve without abstention | Forced binary role-presence policy: `PRESERVED` if present, otherwise `LOST`. |
| Full A11yPreserve | Source contract + multiple evidence paths + explicit unresolved/measurement outcomes. |

## Results

| Baseline/ablation | LibreOffice primary decisions (65) | Google Docs primary decisions (65) | Known valid mutation faults detected |
|---|---|---|---:|
| tag_presence | TAGGED=65 | TAGGED=65 | 0/59 (0.0%) |
| visible_text_equality | EQUAL=65 | EQUAL=64, DIFFERENT=1 | 0/59 (0.0%) |
| destination_only_evidence | PRESENT=64, ABSENT=1 | PRESENT=49, ABSENT=16 | 16/59 (27.1%) |
| without_secondary_evidence | VERIFIED_PRESERVED=38, ALTERED=9, OBSERVED_PARTIAL=11, CONFIRMED_LOST=2, MEASUREMENT_ERROR=5 | OBSERVED_PARTIAL=32, VERIFIED_PRESERVED=11, ALTERED=11, CONFIRMED_LOST=11 | 46/59 (78.0%) |
| without_abstention | PRESERVED=64, LOST=1 | PRESERVED=49, LOST=16 | 16/59 (27.1%) |
| full_a11ypreserve | VERIFIED_PRESERVED=38, ALTERED=9, OBSERVED_PARTIAL=11, CONFIRMED_LOST=1, MEASUREMENT_ERROR=5, UNRESOLVED_EQUIVALENCE=1 | OBSERVED_PARTIAL=32, VERIFIED_PRESERVED=11, ALTERED=11, CONFIRMED_LOST=6, UNRESOLVED_EQUIVALENCE=5 | 46/59 (78.0%) |

The full method retained 6 abstentions/measurement outcomes in LibreOffice and 5 unresolved outcomes in Google Docs. The no-secondary ablation changed the handling of difficult cases: it produced 2 confirmed losses and 5 measurement errors for LibreOffice, and 11 confirmed losses with no abstentions for Google Docs. This shows that secondary evidence and abstention affect the interpretation of negative evidence, even though they did not change the 46/59 coarse mutation detections in this operator set.

## Traceable examples

- F06 inline language / Google Docs: the PDF is tagged and visible text is present, but destination-only evidence is absent; the full method records confirmed loss under the source contract.
- F11 footnotes / Google Docs: the visible note text exists, but the association evidence is unresolved; the full method abstains, whereas the no-secondary and forced-binary variants make a confident loss decision.
- F11 footnotes / LibreOffice: `/Note` evidence exists but association extraction is insufficient; the full method records measurement error rather than calling the feature preserved or lost.

Machine evidence: `experiments/v6/V6_BASELINE_ABLATION.json` and `experiments/v6/V6_MUTATION_BASELINE_EVALUATION.json`.
