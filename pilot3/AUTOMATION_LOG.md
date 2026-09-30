# Pilot 3 Automation Log

All four DOCX fixtures were uploaded through the authenticated Google Docs web UI and exported with File → Download → PDF Document (.pdf). No print-to-PDF path, screenshot, manual content repair, or generated substitute PDF was used.

Environment: Windows `10.0.26200.0`; Chrome browser profile with an authenticated Google Docs session; Google Docs web UI; date 2026-09-27 (America/Los_Angeles). The account identity and credentials were not recorded.

LibreOffice baseline: version `26.2.6.3`, reused from Pilot 2; no conversion rerun.

| Timestamp (local) | Tool / method | Source | Destination | Source SHA-256 | Output SHA-256 | Result |
|---|---|---|---|---|---|---|
| 2026-09-27T19:37:52.168198-07:00 | Chrome → Google Docs import → File → Download → PDF Document (.pdf) | `F01_HEADINGS.docx` | `F01_HEADINGS__GOOGLE_DOCS.pdf` | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | `d6a8a93a8cd0a347448aeb65a86fd1b386dfd6204a23ab449d35da28255ce9bc` | PASS |
| Pilot 2 baseline timestamp retained | LibreOffice `soffice --headless` PDF export (Pilot 2 record) | `F01_HEADINGS.docx` | `F01_HEADINGS__LIBREOFFICE.pdf` | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | `e9329b05d628fcea4c6745e8e0b8fb2eea548d9525e82e4a9d1f6b94634c1b74` | REUSED BASELINE, PASS |
| 2026-09-27T19:42:59.734219-07:00 | Chrome → Google Docs import → File → Download → PDF Document (.pdf) | `F02_ALT_TEXT.docx` | `F02_ALT_TEXT__GOOGLE_DOCS.pdf` | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | `f7d63f222cfe7413080018658f27ab3eadcf9e987e0b1166c66572aafa2dcc94` | PASS |
| Pilot 2 baseline timestamp retained | LibreOffice `soffice --headless` PDF export (Pilot 2 record) | `F02_ALT_TEXT.docx` | `F02_ALT_TEXT__LIBREOFFICE.pdf` | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | `ffb98539b1b315c97a495f6039ca85fd27f5f5ff9d9406d8e6c75aec83ed8c7d` | REUSED BASELINE, PASS |
| 2026-09-27T19:46:07.260621-07:00 | Chrome → Google Docs import → File → Download → PDF Document (.pdf) | `F03_LISTS.docx` | `F03_LISTS__GOOGLE_DOCS.pdf` | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | `d4342499a757d4cd54f07f5d077502e0c33a9c1294b3d036c62021c0d07b4289` | PASS |
| Pilot 2 baseline timestamp retained | LibreOffice `soffice --headless` PDF export (Pilot 2 record) | `F03_LISTS.docx` | `F03_LISTS__LIBREOFFICE.pdf` | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | `6af505d11f532228fa38e9c0441b68ff9d9d54a5f0682b5526b5620ae894b27e` | REUSED BASELINE, PASS |
| 2026-09-27T19:47:32.554403-07:00 | Chrome → Google Docs import → File → Download → PDF Document (.pdf) | `F04_TABLE.docx` | `F04_TABLE__GOOGLE_DOCS.pdf` | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | `32e260086253eb38625d3d740b2ee97ed58ce79c724268224d7d5cfd9487c232` | PASS |
| Pilot 2 baseline timestamp retained | LibreOffice `soffice --headless` PDF export (Pilot 2 record) | `F04_TABLE.docx` | `F04_TABLE__LIBREOFFICE.pdf` | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | `6d2bcc38193eaa1f44b02212352273dd9484625c275c6070510e37bd021b5221` | REUSED BASELINE, PASS |

One recoverable browser automation issue occurred while opening the F02 picker: an overly broad iframe selector matched multiple frames. The run was resumed with the exact picker iframe selector; the F02 export succeeded. This was an automation-recovery event, not a conversion failure.

Microsoft Word: native WINWORD.EXE was found at `C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE` (file version `16.0.20326.20158`). Word conversion was deliberately deferred in Pilot 3 per scope; the earlier Pilot 2 Word absence remains a conversion-layer limitation, not a semantic result.
