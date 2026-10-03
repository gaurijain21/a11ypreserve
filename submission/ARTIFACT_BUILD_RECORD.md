# Artifact build record

- Candidate directory: `artifact/`
- Candidate archive: `submission/A11yPreserve_artifact_ICST2027.zip`
- Directory inventory: 158 files, 2,659,966 bytes before compression
- Archive SHA-256: `EE343279DC86F9991D3C378D0676D17B2B8DF05545C40561B92FC81E0400E39D`
- Archive size: 2,098,006 bytes
- Build script: `scripts/build_public_artifact.py`
- Packaging exclusion: internal `contracts/v3` audit files are excluded from the public V2 candidate; canonical internal files are untouched.
- Sanitization: publication copies replace local workspace paths with `<ARTIFACT_ROOT>` and omit browser state, cookies, credentials, and private account material
- Verification: fresh-package source-oracle run passed 13/13 fixtures; focused OOXML checks, the 27-control calibration, the phase-4 verification aid, and the F06 comparator invocation completed; JSON files parsed; archive and directory scans found no local user paths, credentials, or sensitive binary remnants. Text mentions of cookies/tokens in README/checklists are explanatory exclusions, not included credentials.
- Status: ready for anonymous venue review; not yet licensed for public release.
