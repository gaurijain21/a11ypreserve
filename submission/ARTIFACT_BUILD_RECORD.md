# Reviewer artifact build record

- Canonical directory: `artifact_v3/`
- Canonical archive: `submission/A11yPreserve_artifact_ICST2027_V3.zip`
- Directory inventory: 356 files before packaging exclusions; 342 files in the archive
- Archive SHA-256: `C0F0326DBF40E169BD6A0E101B27F486EB001F5A04518E2AF68B5890528D4908`
- Archive size: 4,633,014 bytes
- Build script: `scripts/package_v3_artifact.py`
- Packaging exclusions: `.git`, `.miktex`, and `__pycache__` directories are excluded; canonical internal evidence is otherwise included.
- Sanitization: the reviewer boundary omits browser state, cookies, credentials, and private account material.
- Verification: the public-package verifier checks the 52 result rows, source/output hashes, provenance links, all 39 repeatability outputs, and release-path sanitization.
- Status: ready for anonymous venue review; not yet licensed for public release.
- Terminology alignment: the reviewer README now states that semantic preservation is evaluated through machine-observable evidence and feature-specific cross-format equivalence; frozen evidence is unchanged.
