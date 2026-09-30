# V3 reproduction audit

## Level 1 — existing evidence

The separate `artifact_v3` candidate was exercised from its root using the included dependencies. The Core raw-OOXML source oracle passed 13/13, and the Variant B raw-OOXML source oracle passed 13/13. Existing PDF hashes, extraction records, repeatability reports, and the 52-case result record are included.

## Level 2 — LibreOffice

The Variant B LibreOffice outputs and conversion report are included with the recorded LibreOffice version and settings. A fresh reconversion was not required for the completed V3 evidence and was not used to redefine any result.

## Level 3 — Google Docs

The workflow is repeatable only through an authenticated Google Docs session. The cloud backend cannot be fully pinned, and no authentication state is included. The 13-fixture, three-run Core arm provides dated workflow repeatability evidence; the Variant B report discloses its in-session export-backend recovery route.

## Environment boundary

Installing dependencies in a newly isolated environment remains constrained by the current package/network configuration. This is not described as independent third-party replication. The artifact therefore supports evidence verification and analysis reruns more strongly than clean-machine reconversion.
