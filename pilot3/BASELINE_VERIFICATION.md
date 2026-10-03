# Pilot 2 LibreOffice Baseline Verification

Verified at (UTC): `2026-09-28T02:56:46.294414+00:00`

Pilot 2 LibreOffice outputs were reused as the frozen baseline; no LibreOffice conversion was rerun in Pilot 3.

| Fixture | Baseline PDF | Recorded SHA-256 | Current SHA-256 | Parseable/tagged |
|---|---|---|---|---|
| F01_HEADINGS | `F01_HEADINGS__LIBREOFFICE.pdf` | `e9329b05d628fcea4c6745e8e0b8fb2eea548d9525e82e4a9d1f6b94634c1b74` | `e9329b05d628fcea4c6745e8e0b8fb2eea548d9525e82e4a9d1f6b94634c1b74` | PASS |
| F02_ALT_TEXT | `F02_ALT_TEXT__LIBREOFFICE.pdf` | `ffb98539b1b315c97a495f6039ca85fd27f5f5ff9d9406d8e6c75aec83ed8c7d` | `ffb98539b1b315c97a495f6039ca85fd27f5f5ff9d9406d8e6c75aec83ed8c7d` | PASS |
| F03_LISTS | `F03_LISTS__LIBREOFFICE.pdf` | `6af505d11f532228fa38e9c0441b68ff9d9d54a5f0682b5526b5620ae894b27e` | `6af505d11f532228fa38e9c0441b68ff9d9d54a5f0682b5526b5620ae894b27e` | PASS |
| F04_TABLE | `F04_TABLE__LIBREOFFICE.pdf` | `6d2bcc38193eaa1f44b02212352273dd9484625c275c6070510e37bd021b5221` | `6d2bcc38193eaa1f44b02212352273dd9484625c275c6070510e37bd021b5221` | PASS |

Baseline verification status: **PASS**

Pilot 2's Microsoft Word rows remain conversion-layer `INVALID_CONVERSION` records and are not reused as semantic evidence.
