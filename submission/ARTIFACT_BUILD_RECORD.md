# Reviewer artifact build record

- Canonical directory: `artifact_v3/`
- Canonical archive: `submission/A11yPreserve_artifact_ICST2027_V3.zip`
- Directory inventory: 356 files before packaging exclusions; 342 files in the archive
- Archive SHA-256: `B315C204C2E112909498B12D17F69B582ACA8813E8A9E42CC1E0E37D1EF08F49`
- Archive size: 4,632,945 bytes
- Build script: `scripts/package_v3_artifact.py`
- Packaging exclusions: `.git`, `.miktex`, and `__pycache__` directories are excluded; canonical internal evidence is otherwise included.
- Sanitization: the reviewer boundary omits browser state, cookies, credentials, and private account material.
- Verification: the public-package verifier checks the 52 result rows, source/output hashes, provenance links, all 39 repeatability outputs, and release-path sanitization.
- Status: ready for anonymous venue review; not yet licensed for public release.
