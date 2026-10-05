# V4 Output Provenance Audit

Status: PASS for the completed LibreOffice arm.

| Check | Result |
|---|---:|
| Atomic manifest records | 65 |
| Realistic manifest records | 10 |
| Successful conversions | 75/75 |
| Source hash matched frozen manifest | 75/75 |
| Output exists and non-zero | 75/75 |
| `%PDF-` signature | 75/75 |
| Parseable by pypdf | 75/75 |
| Tagged structure present | 75/75 |
| Producer consistent | 75/75, `LibreOffice 26.2.6.3 (X86_64)` |
| Timestamp after conversion start | 75/75 |
| Primary extraction records | 75/75 |
| Independent PyMuPDF evidence records | 75/75 |

Each output was generated from the exact frozen DOCX path recorded in `source_manifest.json` or `REALISTIC_CORPUS_MANIFEST.json`. The converter route was the reconstructed V3 LibreOffice route with a per-fixture isolated profile and frozen export settings. No pre-existing V3 PDF was used.

Google has no V4 output record because the authenticated session was inspected but no local DOCX was transmitted without just-in-time confirmation. Word has no V4 output record because direct launch failed before conversion with `0x80070520`.
