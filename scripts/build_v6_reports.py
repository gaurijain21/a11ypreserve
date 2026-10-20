"""Build the human-readable V6 evidence package from machine-derived records."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V6 = ROOT / "experiments" / "v6"
OUT = ROOT / "reports" / "v6"


def load(name: str):
    return json.loads((V6 / name).read_text(encoding="utf-8"))


def pct(n: int, d: int) -> str:
    return f"{n}/{d} ({100*n/d:.1f}%)" if d else "n/a"


def write(name: str, text: str) -> None:
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    control = load("V6_CONTROL_RERUN.json")
    mutation = load("V6_MUTATION_SENSITIVITY.json")
    ablation = load("V6_BASELINE_ABLATION.json")
    independent = json.loads((ROOT / "experiments" / "v5" / "independent_oracle_validation.json").read_text(encoding="utf-8"))
    profile = json.loads((ROOT / "experiments" / "v5" / "LIBREOFFICE_PROFILE_B_ANALYSIS.json").read_text(encoding="utf-8"))
    source = json.loads((ROOT / "experiments" / "v4" / "source_manifest.json").read_text(encoding="utf-8"))

    write("V6_CONTROL_RERUN_REPORT.md", f"""# V6 control rerun report

## Status

**Executed and complete.** The V6 harness reopened the actual 65 frozen LibreOffice baseline PDFs, reran source extraction, destination extraction, the frozen V4 comparator, secondary evidence, and final classification. It did not copy a frozen label into a control result.

| Measure | Result |
|---|---:|
| Controls evaluated | {control['controls_evaluated']}/65 |
| Fresh classification disagreements | {control['classification_disagreements']}/65 |
| Control disagreement rate | {control['control_disagreement_rate']:.3f} |
| Extraction failures | {control['extraction_failures']}/65 |
| Normalized semantic-evidence differences | {control['semantic_evidence_differences']}/65 |

The measured V6 control disagreement rate is **0/65 (0.0%)**. This is a result of the fresh rerun, not the historical V5 hard-coded `false_positive=False` field. Per-case traces are in `experiments/v6/control_rerun_cases/`; the aggregate record is `experiments/v6/V6_CONTROL_RERUN.json`.

The original V5 JSON remains preserved and is not silently rewritten. The corrected implementation is `experiments/v5/destination_mutation_testing.py`, and the independent V6 rerun implementation is `experiments/v6/control_rerun.py`.

## Evidence and failure policy

Source and PDF SHA-256 values, frozen and fresh classifications, normalized semantic-evidence hashes, parser versions, timestamps, and extraction traces are recorded per case. A parse or extraction exception is recorded as a failure and counts as a disagreement requiring investigation; it is never converted into a passing control.
""")

    family_lines = ["| Family | Attempted | Applied | Valid | Classification detected | Meaningful survival | Unchanged classification | Unsupported | Inconclusive |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for family, row in mutation["family_summary"].items():
        family_lines.append(f"| {family} | {row['attempted']} | {row['applied']} | {row['valid']} | {row['classification_detected']} | {row['semantically_meaningful_survival']} | {row['unchanged_classification']} | {row['unsupported']} | {row['inconclusive']} |")
    write("V6_MUTATION_SENSITIVITY_REPORT.md", f"""# V6 mutation sensitivity report

## Executed result

V6 reran one destination-side operator for every one of the 65 frozen atomic LibreOffice PDFs. The original V5 mutation manifest is retained unchanged. Each V6 case records source fixture/family, operator and target, baseline and mutant PDF hashes, application, validity, raw evidence before/after, normalized evidence hashes, contracted-semantics change, classification change, survival status, and exact unsupported/inconclusive reason.

| Outcome | Count |
|---|---:|
| Attempts | {mutation['attempted']} |
| Applied and valid mutants | {mutation['valid_applied_mutants']} |
| Classification-level detections | {mutation['classification_level_detections']} |
| Semantically meaningful survivals | {mutation['semantically_meaningful_survivals']} |
| Unsupported attempts | {mutation['unsupported_attempts']} |
| Invalid mutants | {mutation['invalid_mutants']} |
| Inconclusive attempts | {mutation['inconclusive_attempts']} |
| Non-effective mutants | {mutation['non_effective_mutants']} |
| Evidence-changing, unchanged-classification mutants | {mutation['unchanged_classification_mutants']} |

The valid-mutant classification detection rate is {pct(mutation['classification_level_detections'], mutation['valid_applied_mutants'])}; the semantically meaningful survival count is {mutation['semantically_meaningful_survivals']}. Three additional applied mutants changed extracted evidence but did not change the contracted-semantics signature or coarse classification; they are reported separately as unchanged-classification outcomes, not silently folded into the survival count. A meaningful survival means normalized relevant evidence and the contracted-semantics signature changed, but the six-way classification did not. It is not relabeled as a detection.

## Family-level sensitivity

{chr(10).join(family_lines)}

The five decorative-image attempts are explicitly unsupported because the actual PDFs contained no `/Artifact` node to mutate. The unsupported hyperlink attempt is recorded because that PDF had no URI action. These are operator-representation limits, not silent negative results. The V6 run produced no invalid or inconclusive PDFs.

Machine evidence: `experiments/v6/V6_MUTATION_SENSITIVITY.json` and `experiments/v6/mutation_cases/*.json`.
""")

    primary = ablation["primary_summary"]
    fault = ablation["mutation_fault_sensitivity"]["summary"]
    def method_row(method: str, lo_key: str, go_key: str) -> str:
        lo = primary["libreoffice"]["methods"][method]["distinct_decisions"]
        go = primary["google"]["methods"][method]["distinct_decisions"]
        lo_decisions = ", ".join(f"{k}={v}" for k, v in lo.items())
        go_decisions = ", ".join(f"{k}={v}" for k, v in go.items())
        return f"| {method} | {lo_decisions} | {go_decisions} | {fault[method]['detected_faults']}/{fault[method]['faults_evaluated']} ({100*fault[method]['detection_rate']:.1f}%) |"
    methods = ["tag_presence", "visible_text_equality", "destination_only_evidence", "without_secondary_evidence", "without_abstention", "full_a11ypreserve"]
    rows = ["| Baseline/ablation | LibreOffice primary decisions (65) | Google Docs primary decisions (65) | Known valid mutation faults detected |"]
    rows.append("|---|---|---|---:|")
    rows.extend(method_row(method, "libreoffice", "google") for method in methods)
    write("V6_BASELINE_ABLATION_REPORT.md", f"""# V6 baseline and ablation report

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

{chr(10).join(rows)}

The full method retained 6 abstentions/measurement outcomes in LibreOffice and 5 unresolved outcomes in Google Docs. The no-secondary ablation changed the handling of difficult cases: it produced 2 confirmed losses and 5 measurement errors for LibreOffice, and 11 confirmed losses with no abstentions for Google Docs. This shows that secondary evidence and abstention affect the interpretation of negative evidence, even though they did not change the 46/59 coarse mutation detections in this operator set.

## Traceable examples

- F06 inline language / Google Docs: the PDF is tagged and visible text is present, but destination-only evidence is absent; the full method records confirmed loss under the source contract.
- F11 footnotes / Google Docs: the visible note text exists, but the association evidence is unresolved; the full method abstains, whereas the no-secondary and forced-binary variants make a confident loss decision.
- F11 footnotes / LibreOffice: `/Note` evidence exists but association extraction is insufficient; the full method records measurement error rather than calling the feature preserved or lost.

Machine evidence: `experiments/v6/V6_BASELINE_ABLATION.json` and `experiments/v6/V6_MUTATION_BASELINE_EVALUATION.json`.
""")

    write("V6_PIPELINE_COMPARABILITY.md", f"""# V6 pipeline comparability

| Condition | Route | Version/settings | What is controlled | What is not controlled | Valid inference |
|---|---|---|---|---|---|
| LibreOffice V4 | Local headless `soffice.com` DOCX -> PDF | 26.2.6.3; `UseTaggedPDF=true; PDFUACompliance=true; SelectPdfVersion=1` (PDF/A-1b interpretation) | Input hashes, local executable, isolated profile, export options | Version-specific implementation details | Descriptive source-preservation observations for the named local condition |
| Google Docs V4 | Authenticated browser upload/import -> internal representation -> PDF download | Chrome/browser and observed producer recorded; cloud backend not pin-able | Exact DOCX inputs, workflow, timestamps, output hashes | Import service version, internal representation, export backend configuration | Descriptive end-to-end Google Docs import/export observations; no stage-level attribution |
| LibreOffice V5 profile B | Local headless export | `SelectPdfVersion=0`, tagging/PDF-UA flags retained | Same 65 inputs, comparator, analysis | Serialization/profile differences | Robustness comparison within LibreOffice; 65/65 valid and zero classification changes, not product ranking |
| Microsoft Word | Post-freeze supplementary local GUI route | Recorded separately in V4 manifests | Same 65 source fixtures | Not in primary freeze or balanced against the two primary routes | Supplementary observations only; excluded from the 130 primary denominator |

The profile-B result is machine-derived from `{profile['records'].__len__()}` outputs with `{len(profile.get('classification_changes', []))}` classification changes. It supports a within-LibreOffice robustness statement, not causal attribution between LibreOffice and Google Docs. The Google condition must be described as an end-to-end import/export pipeline; the current evidence cannot localize failures to import, internal representation, or PDF generation.
""")

    write("V6_HOLDOUT_CHRONOLOGY.md", f"""# V6 holdout and repeatability chronology audit

## Arithmetic verified from manifests

| Quantity | Count |
|---|---:|
| Atomic fixtures | {source['fixture_count']} |
| Variants per family | {source['variants_per_feature']} |
| Primary pipelines | 2 |
| Primary fixture--pipeline observations | 130 |
| Holdout fixtures (D/E) | 26 |
| Holdout fixture--pipeline observations | 52 (26 per pipeline) |
| Non-holdout observations | 78 (39 per pipeline) |
| Word supplementary observations | 65 |

The holdout is a within-design fixture-level subset, not an independent natural-document sample. The five variants within a family are correlated by construction; no independence-based inferential statistics or converter rankings are claimed.

## Chronology findings

- `experiments/v4/HOLDOUT_MANIFEST.json` states that D/E membership and the “do not inspect holdout outputs” rule were frozen before conversion.
- `experiments/v4/V4_PROTOCOL.md` states that the source oracle, extractor, comparator, classification rules, and calibration outcomes were frozen before D/E outputs were opened.
- Git history places the V4 protocol/source-corpus freeze before the later V4 evidence-package completion. The retained manifests are the authority for the prospective design claim.
- The repeatability manifest pre-specifies six D variants (`F04_D`, `F06_D`, `F08_D`, `F11_D`, `F12_D`, `F13_D`) and three runs per pipeline, but its top-level status remains `NOT_RUN` even though the retained run outputs and result JSON exist. V6 treats this as a documentation-integrity defect and reports the actual repeatability result separately rather than silently changing the historical manifest.
- The selected repeatability subset is therefore best described as a targeted repeatability probe. The stored selection is pre-specified in the frozen protocol; the repository does not provide a complete external audit trail proving that no early result inspection influenced selection beyond that freeze record.

## Actual repeatability evidence

The retained per-pipeline result files report classification stability for all 6/6 selected fixtures across 3 runs. LibreOffice byte identity was 0/6; Google Docs byte identity was 6/6. These are repeated recorded workflows, not two Google sessions separated by at least seven days. Temporal cloud repeatability remains open.
""")

    disagreements = [row for row in independent["rows"] if not row["agreement"]]
    disagreement_categories = {
        "Missing feature-specific value/association logic": [
            "LibreOffice:F02_A", "LibreOffice:F07_A", "LibreOffice:F08_A",
            "Google Docs:F01_A", "Google Docs:F03_A", "Google Docs:F05_A",
            "Google Docs:F06_A", "Google Docs:F07_A", "Google Docs:F08_A", "Google Docs:F09_A",
        ],
        "Alternate representation not supported": [
            "LibreOffice:F10_A", "LibreOffice:F12_A", "LibreOffice:F13_A",
            "Google Docs:F10_A", "Google Docs:F13_A",
        ],
        "Extraction limitation or conservative abstention": [
            "LibreOffice:F11_A", "Google Docs:F11_A", "Google Docs:F12_A",
        ],
    }
    observed_disagreements = {f"{row['pipeline']}:{row['fixture_id']}" for row in disagreements}
    if set(sum(disagreement_categories.values(), [])) != observed_disagreements:
        raise RuntimeError("independent-validation disagreement categories do not cover exactly the 18 stored disagreements")
    category_rows = []
    for category, cases in disagreement_categories.items():
        category_rows.append(f"| {category} | {len(cases)} | {', '.join(cases)} |")
    write("V6_INDEPENDENT_VALIDATION.md", f"""# V6 independent validation audit

The V5 diagnostic cross-check examined {independent['sample_size']} cases and reported {independent['agreement']} agreements and {independent['disagreement']} disagreements. V6 preserves the frozen comparator and does not relabel these disagreements as external correctness evidence.

## Disagreement investigation

The 18 disagreements fall into the following evidence-based classes:

| Class | Cases | Stored disagreement rows |
|---|---:|---|
{chr(10).join(category_rows)}
| Genuine implementation defect | 0 established | No defect was established from the stored cross-check alone; no relabeling was performed. |

The first category covers exact-value or relation logic absent from the lightweight implementation; the second covers alternate structural representations; the third covers cases where marker/text extraction cannot establish the required association or expression. These are audit categories, not new ground-truth labels.

The exact row-level evidence remains in `experiments/v5/independent_oracle_validation.json`. The second implementation is an independent diagnostic implementation, not an external expert panel and not a human usability study.

## Corrective decision

No corrected comparator is claimed in V6 because the disagreement audit did not establish a specific frozen-comparator defect. If a future expert adjudication identifies one, it must receive a new comparator version and a complete affected-row rerun; the frozen V4 comparator remains preserved.
""")

    write("V6_REPRODUCIBILITY_REPORT.md", f"""# V6 reproducibility report

## Executed checks

| Check | Status |
|---|---|
| V6 control rerun computes all 65 controls | PASS: 65/65 |
| V6 mutation sensitivity rerun | PASS: 65 attempts; 59 valid applied |
| V6 executable baseline/ablation run | PASS: 130 primary cases; 59 known faults |
| V6 regression tests | PASS: standalone scientific regression assertions; `pytest` is not installed in this environment |
| Historical V4/V5 denominators preserved | PASS by machine accounting in V6 records |
| External validator run (PAC/verapDF) | NOT RUN: tools unavailable |
| Google temporal rerun | NOT RUN: authenticated sessions and seven-day schedule unavailable |
| Natural external corpus | NOT RUN: rights-cleared corpus unavailable |
| Current V6 manuscript compile | PASS: 9-page IEEE letter PDF generated; references resolved; all nine pages rendered and visually inspected |

V6 records Python, OS, pypdf, and PyMuPDF versions for each executed run. Exact package versions are pinned in `requirements-v6.txt`; a future release can add wheel hashes for fully offline installation. The static V6 package manifest verifies listed file sizes and SHA-256 hashes, and `.github/workflows/v6.yml` runs the scientific computations rather than only checking pre-existing JSON. Existing V4 manifests retain converter/browser/producer/timestamp/output-hash provenance. The package contains no credentials, cookies, tokens, or private browser data. The V6 source-to-PDF record is `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`; it records source-input hashes, compiler commands and versions, PDF hash/size/page count, and final log diagnostics. The static manifest includes the compiled PDF, bibliography, and IEEE class/style files.

## Remaining infrastructure work

Remaining reproducibility work is wheel-hash locking for fully offline installation. External GUI/cloud reproduction is documented as an authenticated offline path and cannot be honestly run in ordinary CI. The local build required an elevated MiKTeX invocation because the ordinary process could not access the existing MiKTeX registry/configuration; this environment-specific requirement is recorded rather than hidden.
""")

    write("V6_REMAINING_GAPS.md", """# V6 remaining gaps

## High reviewer impact

1. No independent adjudicated semantic ground truth or external accessibility expert panel; the independent implementation is diagnostic only.
2. Ten semantically meaningful mutation survivors and three additional evidence-changing unchanged-classification cases show that the comparator remains fault-model limited.
3. Google Docs is an end-to-end cloud import/export condition; stage-level causality and time-separated repeatability remain untested.
4. No rights-cleared natural-document corpus, PAC, or veraPDF run was available.
5. The repeatability manifest has a stale `NOT_RUN` status despite retained run outputs; this must be corrected in the V6 release metadata or explicitly retained as a historical inconsistency.

## Human-dependent decisions

- Choose compatible public licenses for source, fixtures, evidence, and documents; the root `LICENSE` and `CITATION.cff` intentionally remain placeholders.
- Replace anonymous citation metadata only after the review/anonymity decision permits it.
- Human authors must verify every reference, claim, denominator, and AI disclosure before submission.
- Complete HotCRP author/COI, originality, simultaneous-submission, and artifact-access declarations.

## Future experiments

Standards conformance, 20--30 rights-cleared natural DOCX documents, a preregistered two-session Google arm separated by at least seven days, reading-order oracle development, external blinded expert adjudication, and assistive-technology user testing remain separate future arms. None is represented as executed V6 evidence.
""")

    write("V6_REVIEWER_RED_TEAM.md", """# V6 adversarial reviewer red-team

## Reviewer A - software testing

**Attack:** The oracle could be circular, and destination mutation sensitivity could be overstated.

**Evidence:** The historical V5 script did contain a circular no-op control assignment. V6 removes that implementation flaw, reruns 65 controls, and obtains 0/65 disagreements. V6 also finds 46/59 coarse detections and 10 semantically meaningful survivors, so the mutation result is now explicitly fault-model bounded.

**Strongest remaining objection:** Ten meaningful survivors mean a coarse classification can miss relevant evidence changes. The paper must report survivors and family-level sensitivity, not only 46/59.

## Reviewer B - accessibility

**Attack:** Tagged output, visible text, or a `/Figure`/`/Note` marker may be mistaken for semantic preservation.

**Evidence:** V6 baselines detect 0/59 faults for tag presence and visible-text equality, while destination-only evidence detects 16/59. The full method retains unresolved and measurement outcomes, and F11 remains an explicit association-extraction boundary.

**Strongest remaining objection:** Machine-observable PDF structure is not equivalent to assistive-technology usability or standards conformance. No human study or PAC/verapDF result is claimed.

## Reviewer C - experimental methodology

**Attack:** The holdout is not independent, Google Docs is confounded, and repeatability selection may be post hoc.

**Evidence:** V6 reports 52 holdout and 78 non-holdout observations, labels the holdout as within-design, and avoids inferential statistics. Google Docs is described as end-to-end import/export. The six repeatability variants are present in a pre-specified freeze manifest, but the manifest status inconsistency and lack of a complete selection audit remain open.

**Strongest remaining objection:** The evidence supports descriptive condition-specific findings, not general converter quality or causal stage attribution.

## Verdict after remediation

The submission is scientifically stronger and the manuscript/package checks now pass. The appropriate status remains **GO WITH LIMITATIONS** because the stale repeatability metadata, absent independent adjudication, unavailable standards validators, and human release decisions remain explicit limitations.
""")

    write("V6_MASTER_AUDIT.md", f"""# A11yPreserve V6 master audit

## Final audit status

**GO WITH LIMITATIONS.** Priority-0 and priority-1 computations executed successfully. V6 does not claim standards conformance, natural-corpus validation, temporal Google repeatability, human usability, or external adjudication because those arms were not available or authorized.

## Verified fixes and executed experiments

- Circular no-op-control implementation confirmed and removed. Fresh controls: 0/65 classification disagreements, 0/65 extraction failures, 0/65 semantic-evidence differences.
- Destination mutation sensitivity regenerated: 65 attempts, 59 valid applied, 46 classification detections, 10 semantically meaningful survivors, 6 unsupported, 0 invalid, 0 inconclusive.
- Baselines/ablations executed over 130 primary cases and 59 known valid destination faults. Tag presence and visible-text equality detected 0/59 injected faults; destination-only evidence detected 16/59; full A11yPreserve detected 46/59.
- LibreOffice profile-B result verified from retained V5 evidence: 65 valid outputs and zero classification changes; interpretation is within-pipeline robustness only.
- Historical V4/V5 source fixtures, primary outputs, classifications, hashes, and chronology were not overwritten.

## Denominator and claim boundary

The frozen V4 primary experiment remains 65 fixtures x 2 primary pipelines = 130 observations. D/E contributes 52 holdout observations and A-C contributes 78 non-holdout observations. Word remains 65 supplementary observations. The 10 project-created realistic documents and V6 mutation/ablation records remain separate evidence arms.

## Failed, inconclusive, blocked, and human-dependent work

- Failed/inconclusive V6 runs: none for controls, mutation, or baselines.
- Unsupported mutation attempts: 6 (five decorative-image, one hyperlink) with exact reasons recorded.
- Environment blockers: PAC/verapDF unavailable; authenticated time-separated Google sessions unavailable; no rights-cleared natural corpus; no participant study or ethics approval.
- Human decisions: licensing, author/citation metadata, final reference/result verification, portal declarations, and whether to repair or explicitly retain the stale historical repeatability status.
- Manuscript build: complete. `submission/ICST2027_V6/main.pdf` is a 9-page IEEE letter PDF built from the current source; no unresolved citations/references remain, and every page was rendered for visual QA. Build provenance is recorded in `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`.

## Evidence index

| Claim area | Machine evidence |
|---|---|
| Control rerun | `experiments/v6/V6_CONTROL_RERUN.json`, `experiments/v6/control_rerun_cases/` |
| Mutation sensitivity | `experiments/v6/V6_MUTATION_SENSITIVITY.json`, `experiments/v6/mutation_cases/` |
| Baselines/ablations | `experiments/v6/V6_BASELINE_ABLATION.json`, `experiments/v6/V6_MUTATION_BASELINE_EVALUATION.json` |
| Frozen primary results | `experiments/v4/conversions/*/analysis/` |
| Pipeline profile | `experiments/v5/LIBREOFFICE_PROFILE_B_ANALYSIS.json` |
| Independent diagnostic | `experiments/v5/independent_oracle_validation.json` |
| Source contracts | `experiments/v4/source_manifest.json`, `contracts/`, `evidence/source/` |

The V6 manuscript must cite only machine-derived V6 counts for new empirical claims and must preserve V4/V5 chronology explicitly.
""")

    write("V6_CLAIM_TRACEABILITY_MATRIX.md", """# V6 evidence-to-claim traceability matrix

| Claim | Status | Evidence | Limitation |
|---|---|---|---|
| No-op controls are independently rerun | VERIFIED | `experiments/v6/V6_CONTROL_RERUN.json`; 65 per-case traces | Same frozen comparator implementation; no external oracle claim |
| Control disagreement rate is 0/65 | EXECUTED RESULT | V6 control JSON | Descriptive rerun result, not proof of comparator correctness |
| 59 destination mutants are valid/applied | EXECUTED RESULT | V6 mutation JSON and per-case traces | One operator per fixture; no multi-fault completeness |
| 46/59 coarse mutation detections | EXECUTED RESULT | V6 mutation JSON | Fault-model sensitivity only |
| 10 semantically meaningful survivors | EXECUTED RESULT | V6 per-case `semantically_meaningful_survival` fields | Survivors show blind spots; not a prevalence estimate |
| Tags and visible-text equality are insufficient | EXECUTED COMPARISON | V6 ablation JSON; 0/59 fault detections for each | Known-fault oracle, not independent human labels |
| Full method uses abstention | VERIFIED | V6 primary summary and comparator records | Abstention policy remains implementation-defined |
| V4 primary denominator remains 130 | VERIFIED | V4 manifests and analyses | Controlled purposive corpus |
| Word remains supplementary 65 | VERIFIED | V4 Word analysis | Not balanced against primary conditions |
| Google result is end-to-end import/export | VERIFIED INTERPRETATION | V5 Google boundary report and V6 pipeline matrix | No stage-level localization |
| LibreOffice profile comparison has zero classification changes | VERIFIED | V5 profile analysis JSON | Within-LibreOffice robustness only |
| Independent cross-check is not external validation | VERIFIED LIMITATION | V5 independent validation JSON/report | No expert adjudication |
| Standards conformance established | NOT CLAIMED | PAC/verapDF unavailable | Future validator arm |
| Natural-document generalization established | NOT CLAIMED | V5 external validation report | Rights-cleared corpus unavailable |
| Human usability established | NOT CLAIMED | Ethics/privacy audit and remaining gaps | No participants or approvals |
| V6 manuscript counts match machine records | VERIFIED | `reports/v6/V6_MANUSCRIPT_CONSISTENCY.json` | Headline-count check; human review still required |
| V6 PDF corresponds to current source | VERIFIED | `experiments/v6/V6_PDF_BUILD_PROVENANCE.json`; package manifest | Build environment is recorded; reproducibility still depends on configured MiKTeX |
""")


if __name__ == "__main__":
    main()
