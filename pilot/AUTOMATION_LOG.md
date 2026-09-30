# A11yPreserve Pilot Automation Log

## Automated work completed

- Created the four DOCX fixtures and the locally generated chart with the bundled Python runtime.
- Wrote and froze four JSON ground-truth manifests before any conversion attempt.
- Calculated SHA-256 hashes for every source DOCX and manifest.
- Extracted source OOXML semantics deterministically and verified them against the manifests.
- Implemented a pilot ASIR representation and deterministic comparison logic.
- Ran synthetic comparator tests for PRESERVED, DEGRADED, LOST, and MIS_MAPPED.
- Ran the PDF structure adapter against an older tagged PDF only as a software smoke test; it was not included in empirical pilot results.
- Attempted DOCX rendering through the document skill's renderer.
- Attempted Microsoft Word native PDF export through COM.
- Inspected installed converter and validator availability.
- Opened the authenticated Google Docs home page through the available browser connector.

## GUI applications and limitations

- Microsoft Word is installed, but COM and process launch both failed with Windows error `0x80070520`: “A specified logon session does not exist.”
- The Windows computer-use native-app surface reported no controllable apps, and its native helper was unavailable. No manual UI fallback was requested from the user.
- LibreOffice was not installed, so its DOCX→PDF route was skipped.
- Google Docs was reachable in an authenticated Chrome tab, but the available browser surface did not expose a reliable local-file upload action. No fixture was uploaded to Google; therefore no Google Docs PDF is claimed.
- Acrobat is installed, but no Acrobat export or validator run was attempted after the same Windows session limitation blocked native Office automation.
- PAC and veraPDF were not installed or available on PATH.
- DOCX visual rendering was attempted but failed because the bundled/system LibreOffice renderer was unavailable. The chart PNG itself was visually inspected and is legible.

## User intervention

No repetitive manual conversion, validation, adjudication, or file checking was assigned to the user.

