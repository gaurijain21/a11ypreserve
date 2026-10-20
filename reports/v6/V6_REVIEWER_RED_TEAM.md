# V6 adversarial reviewer red-team

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
