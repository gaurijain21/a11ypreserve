# V4 Final Hardening Baseline

Captured before publication-hardening changes, from clean commit `977ebe921458e1eeffb5bdee29a5b4adfbacff42`.

## Provenance boundary

- V4 protocol freeze commit: `41a7d3f8b84e98acbdafe14070f2ebe7ea6a59e1`
- Git status: clean at capture.
- Frozen protocol SHA-256: `B4A2F974B7E14AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7`
- Atomic source manifest SHA-256: `6D4E77423E84AA6B0038FDBC4EA1BD8C65425C2C9DEF1C8A8D0C057E6D1AB5D7`
- Realistic corpus manifest SHA-256: `E09C8EE8A5569B789E6BAC92DA8D5FF03CEBEBFA18DFF497FD9CDBA284985ED4`
- Calibration controls SHA-256: `DE736A1716945FF5FE960EF5BEE54B4AF516B5BE69FB82DC492FA85E3B28B677`
- Comparator SHA-256: `8BD28AF4E330D100290A049965834CFB47B388A89DE36E563C741CC3199F8EC4`
- Source-oracle SHA-256: `7B5C309D80BD2DC32438A8EACE499ED145A0BF77E880616A0AA0875935EC1DE6`
- Destination-extractor SHA-256: `BBDD736254F7AD08D9CAD81DF1335A480C7E81CD3094FC83924C36D6913160C7`
- Manuscript source SHA-256: `F0D9A522E414A0495203D44DDC384EBEC720CD2015A1A0451534894A2D7AF4BE`

## Conversion evidence snapshot

- LibreOffice conversion manifest SHA-256: `D8721205243F338FC2C2D6DBDFC4418BB83893C54299FBDAF9679F8635869C60`
- Google Docs conversion manifest SHA-256: `3FF606AF5B295DA81A307227E61094A7638EB1BD1D7824BDC9ED489847AD8066`
- LibreOffice analysis SHA-256: `3C1C672FBC17558A4CD39E85CE82CAB4A1F70918D99E03F77A82179F3AFE3F8D`
- Google Docs analysis SHA-256: `F0214A757CFA05FF757F3D6CB6CB6B1556B77D977051CBB0C88065D0C5041145`
- Cross-pipeline comparison SHA-256: `11A5ACCB5FF4826BFAA251F47AFD19146F74694AD5815361F0F4A9A102CA26A1`
- Google repeatability results SHA-256: `0BE54B1C2D99AFBD9C6B6C8E49328D6E2E4819FF99BB204EC57A4F480970E9F7`
- Atomic fixture/output hashes: retained per record in the two conversion manifests; 65 atomic records per pipeline.
- Realistic source/output hashes: retained per record in the two conversion manifests; 10 realistic records per pipeline.

## Change classification for this pass

- Frozen V4 primary result: preserved exactly.
- Diagnostic strengthening: repeatability normalization, calibration false-negative audit, measurement/unresolved audits, reading-order feasibility, source-oracle dependency audit, validator/external-corpus investigation.
- Manuscript-only changes: claim tables, limitations, result presentation, and final package assembly.
- Implementation-only changes: reproducibility scripts, normalization/reporting utilities, and build checks.

No post-result diagnostic finding is silently promoted into the frozen V4 primary classifications.
