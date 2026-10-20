# Fresh adversarial review

## Software-testing reviewer

**Objection:** The full comparator still lacks human-adjudicated ground truth.
The V7 195-case audit is a second implementation, not an independent expert.

**Evidence:** `V7_INDEPENDENT_ORACLE.json` reports 195/195 extraction success,
but explicitly marks the audit as not human adjudication.

**Disposition:** High-severity limitation remains. The blinded 26-case expert
packet is prepared; no reviewer result is invented.

## Accessibility reviewer

**Objection:** Structure-role evidence does not establish assistive-technology
usability or PDF/UA conformance.

**Evidence:** 13/13 benign metadata controls retained the measured contract
projection; 12 association attacks were valid and 11 were detected, but the
complex-table attack survived.

**Disposition:** The result supports selected machine-observable semantics only.
The complex-table blind spot must remain visible in the paper and release notes.

## Experimental-methodology reviewer

**Objection:** The corpus and holdout are controlled and correlated, not a
natural independent sample.

**Evidence:** `HOLDOUT_AND_COUNT_RECONCILIATION.md` preserves 130 primary cases,
52 within-design holdout observations, and 65 supplementary Word observations.

**Disposition:** External validity remains limited but is now explicitly
accounted for; no prevalence or converter-ranking claim is justified.

## Reproducibility reviewer

**Objection:** Parser disagreement may create extraction-dependent conclusions.

**Evidence:** 275/2,145 pypdf-versus-PyMuPDF marker comparisons differed.

**Disposition:** Multiple evidence paths and abstention are justified, but the
parser boundary remains a measurement limitation.

## Novelty reviewer

**Objection:** The central ingredients are established testing practices.

**Disposition:** Narrow the contribution to the documented preservation-testing
protocol, benchmark, evidence accounting, and measured limitations. Do not claim
a new general theory of test-oracle construction.
