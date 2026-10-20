# Reproducibility audit

Status: COMPLETED WITH LIMITATIONS.

The additive checks are executable offline with the recorded Python libraries:
`pypdf 6.18.1`, `PyMuPDF 1.28.2`, and Python 3.11.9 on Windows. The unified
entry point is `python scripts/reproduce_v8.py`; `--verify-only` checks the
machine-derived totals without regenerating case files. It never overwrites
V4/V5/V6 freezes.

Verified totals are 65 mutation attempts, 59 applied, 59 direct Tier-A faults,
46 detections, 13 direct survivors, 6 unsupported attempts, 26 benign
controls with zero alerts, 39 cross-converter attempts, 13 families, and 65
atomic fixtures. Google Docs reruns still require authenticated external
access; PAC/veraPDF were not available in the execution environment.

The release package excludes credentials, cookies, browser profiles, and
private account state. Package verification and anonymity checks remain the
authoritative release gates.
