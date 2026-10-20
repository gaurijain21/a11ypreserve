# V6 objection mitigation audit

This is an additive V6 diagnostic and release-hardening artifact. It does not rewrite V4/V5/V6 frozen classifications, fixtures, evidence, or denominators.

## 1. Independent ground truth

- Primary cases: **130**; independent human adjudicated labels: **NO**.
- The known-fault arm has **59/59** valid applied mutants with construction-known fault application, **46/59** coarse-classification detections, and **59/59** evidence-drift alerts.
- The historical diagnostic cross-check remains **8/26** agreement with **18** disagreements; it is not external ground truth.
- Mitigation: a blinded packet index and adjudication rubric are prepared for human review. No adjudication result is claimed until an authorized independent reviewer actually completes it.

## 2. External validity

- The primary design remains **65 atomic fixtures × 2 pipelines = 130 cases**.
- The holdout remains **26 fixtures per pipeline**, a within-design holdout rather than an independent natural corpus.
- The existing project-created realistic arm contains **10 documents, 78 contracts per pipeline, and 156 property–pipeline observations**; a separate 3-document/42-observation sanity arm is also retained. Neither is a natural-document sample or a prevalence estimate.
- Mitigation: family-level sensitivity, paired pipeline counts, and the integrated applicability arm are reported as descriptive coverage evidence only. No converter ranking or population estimate is asserted.

## 3. Ten survivors

- Frozen coarse result: **46/59** detections and **10** meaningful survivors.
- Additive two-level mitigation: **59/59** valid mutants raised an evidence-drift alert; this includes the ten meaningful survivors and three additional unchanged-classification evidence changes.
- The alert is operationally useful because it prevents a same-category result from being treated as unchanged evidence. It is deliberately not relabeled as a six-way classification detection.
- Survivor cases and family-level rates are recorded in the JSON trace. The survivors remain visible as fault-model limitations.

## Status

- Executed: survivor derivation, family summary, evidence-drift alert accounting, packet indexing, and source-hash capture.
- Not executed: independent human adjudication, rights-cleared natural corpus study, and assistive-technology usability study.
- Result: the objections are narrowed and made actionable, but not falsely claimed to be eliminated.

Machine evidence: `experiments/v6/V6_OBJECTION_MITIGATIONS.json` (generated 2026-10-20T05:56:35.915816+00:00).
