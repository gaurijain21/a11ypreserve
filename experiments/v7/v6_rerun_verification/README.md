# Fresh verification of the frozen V6 computations

This directory preserves the fresh outputs produced by running
`python scripts/reproduce_v6.py` during the additive adversarial audit. The
outputs are retained separately so that the frozen V6 result files and their
historical timestamps are not overwritten by a later rerun.

The rerun independently reopened the recorded baseline PDFs and recomputed
the controls, mutation audit, and baselines. It reproduced 65/65 controls with
zero classification disagreements, 59 valid mutants with 46 coarse detections
and 10 meaningful survivors, and the published baseline/ablation counts.
The per-case traces retain the raw extraction evidence and rerun timestamps.
These traces are verification evidence, not a redefinition of the V4/V5/V6
freeze.
