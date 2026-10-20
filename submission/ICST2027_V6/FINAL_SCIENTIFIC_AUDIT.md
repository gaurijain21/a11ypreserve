# A11yPreserve V6 final scientific audit

Recorded 2026-10-19. This is an evidence audit of the current V6 submission
candidate. It does not replace author review of the sources, and it does not
claim external adjudication or human usability evidence.

## Verdict

**GO WITH LIMITATIONS.** The executable V6 checks pass and the manuscript
numbers are consistent with the current machine-readable records. The claims
remain descriptive of controlled, purposive fixtures and named conversion
conditions. The method is not a PDF/UA validator, a user study, a natural-
document corpus study, or a converter ranking.

## Claim-to-evidence audit

Locations refer to the nine-page canonical PDF
`submission/ICST2027_V6/main.pdf`; section names are authoritative when page
pagination changes.

| Claim | Manuscript location | Evidence | Verification | Issue or boundary |
|---|---|---|---|---|
| A11yPreserve tests preservation of selected source semantics | Abstract; Introduction; Conclusion | `submission/ICST2027_V6/main.tex`; V4/V5 reports | PASS: framing matches the implemented source-contract/comparison pipeline | Selected machine-observable semantics only |
| V4 primary design has 13 families, five variants, 65 fixtures and 130 primary cases | Abstract; Design; Results Table I | V4 manifests and `experiments/v5/evidence/results/V4_ACCOUNTING.json` | PASS: accounting checks preserve 13 x 5 x 2 | Purposive controlled cases, not a prevalence sample |
| Word is a post-freeze supplementary 65-observation arm | Abstract; Results Table I; Threats | V4 Word manifest and analysis; `reports/v6/V6_HOLDOUT_CHRONOLOGY.md` | PASS | Not prospective primary treatment data |
| Google is an end-to-end import/internal-representation/PDF-download condition | Method; V6 hardening; Discussion | `reports/v6/V6_PIPELINE_COMPARABILITY.md`; V5 Google boundary evidence | PASS: causal stage localization is expressly not claimed | No intermediate Google representation was independently inspected |
| The former no-op control was repaired | V6 hardening, control subsection | `experiments/v6/control_rerun.py`; `experiments/v6/V6_CONTROL_RERUN.json`; 65 case files | PASS: fresh classifications and evidence are computed from reopened PDFs; no expected label is copied | Same frozen comparator family is used; not external correctness validation |
| Control rerun disagreed in 0/65 cases | Abstract; V6 hardening; Results | `experiments/v6/V6_CONTROL_RERUN.json` | PASS: 65 evaluated, 0 disagreements, 0 extraction failures, 0 evidence differences | Descriptive rerun result |
| Destination mutation audit has 65 attempts, 59 valid mutants, 46 coarse detections | Abstract; V6 hardening; Results | `experiments/v6/V6_MUTATION_SENSITIVITY.json`; `experiments/v6/mutation_cases/` | PASS: accounting verifier recomputes the categories | Fault-model sensitivity, not complete fault coverage |
| Ten meaningful survivors remain | Abstract; V6 hardening; Mutation report | Same mutation JSON and per-case traces | PASS: semantic evidence and contract signature changed without coarse-classification change | Survivors are comparator blind spots and are not relabeled as detections |
| Six attempts are unsupported | V6 hardening; Mutation report | Mutation JSON and unsupported per-case records | PASS: five decorative-image attempts lacked `/Artifact`; one hyperlink lacked a URI action | Unsupported is separated from invalid, inconclusive, and surviving |
| Tag presence and visible-text equality detect 0/59 known faults | Abstract; V6 ablation Table V | `experiments/v6/V6_BASELINE_ABLATION.json`; baseline case records | PASS: known-fault denominator is 59 | Known injected faults are the reference, not human ground truth |
| Destination-only evidence detects 16/59; full method detects 46/59 | Abstract; V6 ablation Table V | Same ablation JSON and case records | PASS | Detection is operator-set sensitivity, not accuracy or prevalence |
| Abstention changes observed decisions | V6 ablation subsection/Table V; Discussion | Ablation JSON, especially F06/F11 traces | PASS: full method retains unresolved/measurement outcomes; forced binary policy does not | No independent adjudicated labels were available |
| Source-oracle mutations were detected 39/39 | Results checks; Threats | V5 source-oracle mutation audit and frozen package | PASS as historical V5 evidence | Same-team oracle implementation; not external validation |
| Holdout is 52 observations within the 130-case primary design | Design; Threats; V6 hardening | `reports/v6/V6_HOLDOUT_CHRONOLOGY.md`; V4 holdout manifest | PASS: 26 per primary pipeline, 78 non-holdout observations | Not an independent natural-document test set |
| Six targeted variants are stable across three recorded runs | Results; Discussion; V6 repeatability report | `reports/v6/V6_REPEATABILITY_METADATA.md`; historical manifests | QUALIFIED: 6/6 classification/evidence stability per pipeline | Historical temporal Google repeatability remains `NOT_RUN`; no seven-day claim |
| Pipeline profile comparison is descriptive | V6 hardening; Pipeline report | V5 LibreOffice profile-B analysis | PASS: 65/65 valid and 0 classification changes | Within-LibreOffice robustness only; not balanced pipeline attribution |
| No PDF/UA, natural-corpus, external-adjudication or human-usability result is claimed | Threats; Data availability; Conclusion | `reports/v6/V6_REMAINING_GAPS.md` and manuscript text | PASS: explicit non-claims are present | Author must retain these boundaries in submission metadata |
| The PDF corresponds to the current source | Data availability; release artifact | `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`; `v6_rebuild2.log` | PASS: byte/text identity and current SHA are recorded | Rebuild requires the recorded MiKTeX environment |

## Recomputed accounting

The following checks were executed in the current checkout:

```text
python scripts/reproduce_v5.py                         PASS (historical V5)
python scripts/verify_v6_scientific_accounting.py      PASS
python scripts/audit_v6_manuscript_consistency.py      PASS
python tests/test_v6_scientific_hardening.py           PASS
```

The machine-derived headline results are 65/65 genuine controls with 0/65
classification disagreements, 59/59 valid applied destination mutants with
46/59 coarse detections and 10 meaningful survivors, and 0/59, 0/59, 16/59,
and 46/59 detections for tag presence, visible-text equality, destination-only
evidence, and full A11yPreserve respectively. The primary denominator remains
130; the Word supplement remains 65; the holdout remains 52 observations.

## Independent-validation boundary

The historical diagnostic cross-check reported eight agreements and 18
disagreements over 26 cases. Both implementations were developed or reviewed
by the same research team. The disagreements are retained in
`reports/v6/V6_INDEPENDENT_VALIDATION.md`; this audit does not call that
external validation and does not relabel disagreements as ground truth.

## Frozen-artifact integrity

No V4/V5 fixture, frozen classification, manifest, raw conversion, historical
report, holdout membership, or denominator was rewritten to improve V6. V6
records are additive under `experiments/v6/` and `reports/v6/`. Release
packaging changes are separate from scientific evidence.

## Human review still required

An authorized author must read the complete manuscript and cited sources,
confirm that each claim is appropriately worded, inspect the exact archive and
HotCRP fields, and approve the final declarations. Those actions are recorded
in `AUTHOR_SIGNOFF_CHECKLIST.md` and are not represented as completed here.
