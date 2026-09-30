# V2 Integrity Check

Date checked: 2026-09-28

This check records the hashes of the frozen V2 inputs and submission artifact before V3 work. The files listed below were verified with Windows `certutil -hashfile ... SHA256`; all observed hashes match the archived V2 integrity record.

| Frozen item | SHA-256 | Status |
|---|---|---|
| `corpus/FROZEN_CORPUS_MANIFEST.json` | `DBC7DA58773E4A15AFE2582E5FCBF271C8AC82D686833E0406BD24D539517376` | MATCH |
| `results/full_experiment/PRIMARY_RESULTS_FREEZE.json` | `6939351E01695D334FCC45C4823316CE4A3698D114091EB34C127E7FE5548D99` | MATCH |
| `results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json` | `04FD89CF44FE9B158A4D1FB3FB5B396A87BF4EADC83081A13C6C4EA14994AEB3` | MATCH |
| `submission/ICST2027/main.pdf` | `22AFD73963E0186B9E75A73DA022312E111930C14ED4AFF091FCF1D8C982CAC5` | MATCH |
| `submission/ICST2027/references.bib` | `4B788CD0148D9800F6F47560A80B4376929C30D8BC914F95BC14ED078DED6F7B` | MATCH |

The repository was at commit `55520e491d6b8b1dcc407e429e5025e22cac73a5` when this check was recorded. V3 outputs and any V3 manuscript copy are separate from the frozen V2 submission directory. No V2 fixture, PDF, manifest, primary-results JSON, or archived V2 manuscript was modified by this check.

## Scope note

This is an integrity check, not a claim that the V2 paper is the final V3 submission. V3 may add separately labelled analyses and a separate manuscript copy; the V2 files above remain the provenance anchor.
