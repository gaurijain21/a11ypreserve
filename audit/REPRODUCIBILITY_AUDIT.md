# Reproducibility Audit

Reproducible locally: frozen fixture paths/hashes, manifests, source OOXML verification, LibreOffice executable/version/settings, deterministic output names, PDF extraction, a11ydiff commands, raw hashes, evidence paths, and passing tests are retained.

Cloud/proprietary limitation: Google Docs is authenticated and its service version is not pinned independently of the observed PDF renderer/browser/date. Reproduction requires a Google account and may be affected by service updates. Microsoft Word was not reproducibly executable and is explicitly excluded. Exact experiment date and output hashes are retained in the automation log and freeze records.
