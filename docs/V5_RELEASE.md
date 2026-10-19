# A11yPreserve V5 release record

V5 is the canonical ICST 2027 submission state. The anonymous manuscript and
bundle are under `submission/ICST2027_V5/`; V3 and V4 directories remain
historical provenance and are not alternate current submissions.

## Reproduction

Install `requirements-v5.txt`, then run:

```powershell
python scripts/reproduce_v5.py
```

To regenerate the expanded destination-mutation evidence and bundle:

```powershell
python scripts/reproduce_v5.py --refresh-artifacts
```

Paper compilation additionally requires `pdflatex` and `bibtex`; converter
reruns require the recorded LibreOffice installation or an authorized Google
Docs session. No credentials, browser profiles, or cloud account material are
part of the release.

## Release contents

- 13 feature families, 65 atomic fixtures, and 130 primary fixture--pipeline cases;
- 75 records per primary conversion manifest: 65 atomic plus 10 realistic integrated;
- 52 within-family/within-variant holdout cases and 78 aggregate non-holdout cases;
- 39/39 source mutations detected;
- 65 destination mutation attempts: 59 valid, 46 detected, 13 surviving, 6 unsupported, and 2 measurement errors;
- an 8/26 agreement and 18/26 disagreement independent diagnostic cross-check;
- explicit non-claims for PDF/A/PDF/UA conformance, byte identity, human usability, natural-corpus generalization, and cloud temporal stability.

The anonymous ZIP is a generated release artifact. Its outer and inner
manifests record hashes and exclude generated upload working directories from
version control.
