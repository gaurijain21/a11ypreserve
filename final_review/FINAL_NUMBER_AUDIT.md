# Final Number and Terminology Check

The check below reads `FINAL_EVIDENCE_AWARE_RESULTS.json`, `INTEGRATED_RESULTS.json`, `INTEGRATED_SOURCE_ORACLE.json`, and the final `.tex` sources. It recomputes the V2 and secondary counts, then scans for prohibited overclaims.

| Check | Expected/observed | Status |
|---|---:|---|
| total primary cases | 26 | PASS |
| verified preserved | 11 | PASS |
| observed partial | 3 | PASS |
| altered | 3 | PASS |
| confirmed lost | 2 | PASS |
| unresolved equivalence | 6 | PASS |
| measurement error | 1 | PASS |
| integrated documents | 3 | PASS |
| integrated observations | 42 | PASS |
| integrated source oracle | 21/21 | PASS |
| forbidden phrase absent: failure rate | absent | PASS |
| forbidden phrase absent: semantic failure | absent | PASS |
| forbidden phrase absent: Google's PDF exporter loses | absent | PASS |
| forbidden phrase absent: Google Docs is generally less accessible | absent | PASS |
| forbidden phrase absent: LibreOffice is generally better | absent | PASS |
| forbidden phrase absent: blind users could no longer | absent | PASS |
| forbidden phrase absent: all document conversion destroys accessibility | absent | PASS |

Overall status: **PASS**.

V2 counts are controlled-case observations, not population estimates. Integrated observations remain outside the primary denominator.
