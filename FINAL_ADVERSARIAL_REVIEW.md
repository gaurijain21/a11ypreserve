# Final adversarial review

## Summary

A11yPreserve is a bounded source-to-destination preservation protocol with a 52-row atomic V3 record, explicit abstention, and a reproducible evidence package. The repository now has one canonical account and machine-checkable count agreement.

## Strengths

- Source contracts are tied to controlled DOCX fixtures and frozen hashes.
- The separately implemented raw-OOXML oracle passes 13/13 Core contracts.
- Core and Variant B provide two controlled instances per selected family.
- Unresolved equivalence is retained instead of being relabeled as loss or preservation.
- The artifact self-check validates all 52 rows and provenance links.
- Google repeatability, calibration, difficult-case audits, and integrated applicability are separated from the primary denominator.

## Fatal concerns

None found for the narrowed protocol claim. A venue demanding a representative corpus, Word comparison, or user study would be asking for a broader contribution than the one claimed.

## Major concerns

| Concern | Status |
|---|---|
| Only two named conversion conditions | Accepted limitation; claims are condition-specific. |
| 18 unresolved atomic rows | Accepted limitation; abstention is a result, not hidden failure. |
| Calibration has two false negatives and seven other unresolved/indeterminate controls | Mitigated by disclosure; still reduces confidence in difficult mappings. |
| Google Variant B route differs from the Core visible workflow | Mitigated by route audit; residual threat remains. |
| Core taxonomy evolved post hoc | Mitigated by chronology and unchanged evidence; not preregistered. |
| Same-team source oracle and comparator | Mitigated by separate implementation and corruption tests; not external validation. |
| No untouched Variant C | Accepted limitation; no holdout claim is made. |
| No natural real-world corpus | Accepted limitation; integrated arm is explicitly synthetic. |
| No user study | Accepted limitation; no user-impact claim is made. |
| Novelty overlaps conversion benchmarks and PDF accessibility work | Mitigated only by a narrow, non-first distinction; significance remains venue-dependent. |

## Minor concerns

- Historical root files can still confuse a casual reader despite the archive policy.
- The repository contains vendored runtime noise that is unnecessary for a polished public release.
- The missing `pytest` dependency prevents running the repository's pytest wrapper in this environment; equivalent precedence and corruption checks run without it.

## Questions for authors

1. Will the venue accept a domain-specific testing protocol with no user study?
2. Are all bundled fixture assets redistributable under the chosen artifact license?
3. Is the Google route deviation acceptable for the final paper's exact comparison?

## Reproducibility concerns

Evidence verification is automated. LibreOffice reproduction is documented. Google and Word require external authenticated/session conditions; Word failed before export. The PDF and artifact must be checked again after any final packaging change.

## Novelty assessment

Partially novel. The contribution is not the first conversion-preservation or PDF-accessibility study. Its defensible distinction is the controlled DOCX source oracle plus feature contract, paired PDF evidence, and uncertainty-aware abstention protocol.

## Methodology assessment

Acceptable for the bounded claim, but not comprehensive. The fault model and calibration make the limits visible; they do not establish broad oracle accuracy or ecosystem behavior.

## Artifact assessment

Strong review candidate: the artifact self-check passes, hashes and provenance are present, and identity-bearing source control is excluded. Final licensing and archive metadata remain human checks.

## Recommendation

Weak Accept for a venue receptive to testing methodology and document engineering; Borderline for a venue requiring broad empirical external validity. The recommendation is not an endorsement of complete PDF accessibility.
