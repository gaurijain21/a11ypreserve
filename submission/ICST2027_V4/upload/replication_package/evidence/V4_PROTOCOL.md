# A11yPreserve V4 Prospective Protocol

Status: frozen before any V4 converter result was inspected.
Version: V4.0.0
Freeze rule: V3 remains immutable historical evidence. V4 is a prospective extension and does not retroactively modify V3.

## Central question and scope

When accessibility information is known to exist in a DOCX source document, does that accessibility information survive DOCX-to-PDF conversion? V4 measures source-semantic preservation; it is not a complete PDF checker, WCAG/PDF-UA conformance system, prevalence study, converter ranking, screen-reader study, or remediation system.

## Research questions

RQ1. For 13 retained feature families, what source-grounded preservation outcomes are observed under each successfully established DOCX-to-PDF pipeline?

RQ2. Does a calibrated, conservative comparator reduce unsupported confident classifications while making unresolved causes explicit?

RQ3. Does the frozen procedure operate on realistic multi-feature documents, scored per source property contract rather than by a global accessibility score?

RQ4. Are repeated conversions of identical inputs classification-stable under a pre-specified repeatability arm?

RQ5. Does source-grounded evidence reveal information not represented by destination-only checking? This is secondary and is omitted if a validator cannot be run consistently.

## Feature families and corpus

The retained families are headings, alternative text, lists, basic tables, document language, inline language, decorative images, hyperlinks, document title/metadata, complex tables, footnotes, equations, and figure/caption association. Reading order is a prospective extension only if a bounded oracle passes calibration; otherwise it remains excluded.

Each family has five meaningful variants (A-E), for a target of 65 atomic DOCX fixtures. Variants differ in encoding, value, structure, multiplicity, or locale; visible-text-only duplicates are prohibited. A-E roles are frozen before conversion: A-C development and D-E untouched holdout. The realistic corpus is analytically separate.

## Source fixture policy and contracts

Each fixture is generated once, SHA-256 hashed, inspected as raw OOXML, extracted by the primary deterministic source extractor, and checked by a separately implemented raw-OOXML oracle. A machine-readable contract records the feature, variant, expected values, source hash, and validation evidence. A fixture enters the benchmark only when the primary extractor and the oracle both support the contract.

## Converter conditions

The primary condition is the documented accessibility-preserving export mode of each genuinely available converter. LibreOffice is evaluated with its recorded tagged/PDF-UA-oriented settings when available. Google Docs, if available, uses one consistent authenticated upload/export route for all V4 cases and records browser, OS, date, producer, source hash, output hash, and timestamps. Microsoft Word is attempted through legitimate local automation; no output is fabricated. A third pipeline is included only if it is actually available, technically distinct, relevant, and fully documented. A failed or unavailable pipeline is reported outside the primary denominator.

## Destination evidence and extraction

The primary extractor reports raw observations only. Difficult features use corroborating paths where available: pypdf object/structure-tree traversal, marked-content, annotations, parent tree, role map, namespaces, metadata, and PyMuPDF/raw-object evidence. A parser's failure is not semantic absence. Destination evidence is retained with hashes and provenance certificates.

## Comparator and taxonomy

Feature-specific comparator rules are frozen before V4 conversion. Precedence is: MEASUREMENT_ERROR when evidence cannot support a valid observation; CONFIRMED_LOST only with corroborated absence of the required representation; ALTERED for a supported author-value or semantic difference; OBSERVED_PARTIAL for supported but incomplete correspondence; VERIFIED_PRESERVED only for contract-level equivalence; UNRESOLVED_EQUIVALENCE for safe abstention when alternate encoding, association, or parser disagreement prevents a decision. A feature-shaped node alone is never preservation.

Calibration uses 6-10 non-duplicate diagnostic controls per family, covering exact preservation, valid equivalent representation, altered value, partial preservation, confirmed absence, ambiguous representation, and unsupported alternate encoding where applicable. Expected decisions are frozen in machine-readable form before comparator execution. Reports include determinate correctness, false positives, false negatives, correct abstentions, incorrect abstentions, and measurement errors by family. Population sensitivity/specificity is not estimated.

## Holdout policy

The final source oracle, extractor, comparator, classification rules, and calibration outcomes are frozen before D/E converter outputs are opened or analyzed. Holdout outputs are stored with immutable hashes and analyzed by the same procedure. Development and holdout results are reported separately.

## Realistic/integrated evaluation

At least ten multi-page project-created realistic documents are targeted, with external documents added only when provenance and reuse rights permit. Documents are authored as coherent reports, handouts, policies, guides, or similar artifacts rather than concatenations of atomic fixtures. Each document has multiple source property contracts. Results are per property contract; no global accessibility score is assigned and counts are not merged with atomic denominators.

## Repeatability

Repeatability means repeated conversion of the identical source under the identical recorded workflow. It is distinct from cross-variant consistency. At least three runs are targeted for a pre-specified subset including inline language, tables, links, equations, footnotes, and captions where the pipeline permits. Byte, structural extraction, and classification identity are compared.

## Analysis, exclusions, and primary outcomes

Primary: feature-by-converter preservation classifications for the 65 controlled fixtures, with explicit denominators and failed conversions; holdout rows are primary once analyzed. Secondary: development rows, realistic/integrated property observations, repeatability, unresolved-cause analysis, and optional validator comparison. Exclusions are limited to corrupt/unreadable source files, failed conversions, or unsupported external service conditions; exclusions are never silently removed and do not become negative preservation outcomes.

The analysis reports controlled descriptive counts only. No population prevalence, global converter percentage, weighted score, or unsupported significance test is used. All numbers are regenerated from canonical JSON result records.

## Freeze and reproducibility

`PRE_RESULT_FREEZE.json` hashes this protocol, fixture-generation policy, contracts/schema, oracle, comparator, extraction policy, fault model, feature-selection matrix, holdout manifest, and prior-art audit seed before any V4 converter result is inspected. `reproduce_v4.py` provides source-only, calibration, existing-output, and full-analysis modes. External GUI/cloud conversion steps are documented separately and are not falsely claimed to be recreated offline.
