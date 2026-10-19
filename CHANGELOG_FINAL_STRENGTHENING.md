# Final-strengthening changelog

| Change | Previous behavior | New behavior | Evidence/history impact |
|---|---|---|---|
| Canonical state | Root documents mixed V1/V2 Core and V3 accounts | `CANONICAL_SUBMISSION_STATE.md` and `results/V3_PRIMARY_RESULTS.json` define one current account | Historical files and 26-row Core result remain unchanged. |
| Consistency | Counts were duplicated across prose and JSON | `tools/audit_submission_consistency.py` derives and checks counts | No result classification changed. |
| Reproduction | Verification steps were distributed across artifact notes | `reproduce.py` provides one evidence-only command | Does not claim to reproduce external/session-dependent conversions. |
| Source oracle | Independence wording risked overclaiming | Wording is now “separately implemented raw-OOXML oracle” | 13/13 existing source results unchanged. |
| Calibration | “Calibrated” could imply performance estimation | Diagnostic control counts and false negatives are explicit | No frozen output was rewritten. |
| External validity | Integrated documents could be mistaken for real-world corpus | Integrated arm is labeled synthetic and secondary | 3-document/42-observation arm remains separate. |
| Word/reading order/Variant C | Missing arms could be read as silently omitted | NO-GO/deferred decisions are recorded | No fabricated evidence added. |
