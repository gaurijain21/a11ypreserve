# V6 objection mitigation plan

This plan records the strongest technically honest improvements for the three remaining reviewer objections. It is intentionally separate from the frozen V4/V5 evidence and does not claim that a human adjudication, natural-document study, or usability study occurred.

| Objection | V6 mitigation | What it establishes | What remains open |
|---|---|---|---|
| No independent adjudicated ground truth | Prepare a blinded 26-case packet index, rubric, and explicit label-separation protocol. Keep the known-fault arm separate because its labels are construction-known. | Makes the next human validation executable and prevents internal diagnostic agreement from being misreported as correctness. | Human reviewers and adjudication are still required. |
| Controlled fixtures and within-design holdout | Add a machine-derived family-level/paired-condition accounting layer and retain the three-document integrated project-created arm as a separately labeled applicability check. | Shows coverage and cross-family heterogeneity without pretending to estimate real-world prevalence. | Rights-cleared natural documents and independent holdout remain future work. |
| Ten meaningful survivors | Add an evidence-drift alert whenever normalized extracted evidence changes, even when the six-way category is unchanged. Report 59/59 evidence alerts alongside the frozen 46/59 coarse detections. | Makes every valid injected evidence change operationally visible while preserving the scientifically important coarse-survivor result. | The six-way comparator remains fault-model limited; survivors are not erased. |

The executable implementation and trace are `scripts/audit_v6_objection_mitigations.py`, `experiments/v6/V6_OBJECTION_MITIGATIONS.json`, and `reports/v6/V6_OBJECTION_MITIGATIONS.md`.
