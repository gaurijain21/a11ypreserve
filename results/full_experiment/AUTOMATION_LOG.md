# Full Experiment Automation Log

All 26 records below are primary conversion records. Google Docs exports used authenticated Google Docs UI: Open file picker → Upload exact frozen DOCX → File → Download → PDF Document (.pdf). No print-to-PDF path was used.

## Environment

- Windows: `Windows-10-10.0.26200-SP0`
- Chrome: `153.0.8010.53`
- LibreOffice: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- LibreOffice method: native `soffice.com writer_pdf_Export`; `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Google Docs PDF renderer observed in output metadata: `Skia/PDF m156`

## F01_HEADINGS — LibreOffice

- Timestamp: `2026-09-27T21:18:33.991565-07:00` to `2026-09-27T21:18:57.916122-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F01_HEADINGS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F01_HEADINGS__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=67693 bytes
- Source SHA-256: `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407`
- Output SHA-256: `18e7b54ad373d7eb8187864b9bd8f6d495d147dffb59176a3b22296ab85aa898`

## F01_HEADINGS — Google Docs

- Timestamp: `2026-09-28T04:29:07.222648+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F01_HEADINGS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F01_HEADINGS__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407`
- Output SHA-256: `d6a8a93a8cd0a347448aeb65a86fd1b386dfd6204a23ab449d35da28255ce9bc`

## F02_ALT_TEXT — LibreOffice

- Timestamp: `2026-09-27T21:18:57.920757-07:00` to `2026-09-27T21:19:18.401199-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F02_ALT_TEXT.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F02_ALT_TEXT__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=69910 bytes
- Source SHA-256: `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da`
- Output SHA-256: `1837537f7f2a4b59c3cab974a9a1f0bb1f527e2271181a685e31986d98fdc272`

## F02_ALT_TEXT — Google Docs

- Timestamp: `2026-09-28T04:38:51.469043+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F02_ALT_TEXT.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F02_ALT_TEXT__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da`
- Output SHA-256: `f7d63f222cfe7413080018658f27ab3eadcf9e987e0b1166c66572aafa2dcc94`

## F03_LISTS — LibreOffice

- Timestamp: `2026-09-27T21:19:18.405804-07:00` to `2026-09-27T21:19:38.437535-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F03_LISTS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F03_LISTS__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=63731 bytes
- Source SHA-256: `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f`
- Output SHA-256: `93d6f5cf39ec84661368c2095aa0850d643734a17a65cc228d3fc11c83fa077b`

## F03_LISTS — Google Docs

- Timestamp: `2026-09-28T04:42:53.797426+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F03_LISTS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F03_LISTS__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f`
- Output SHA-256: `d4342499a757d4cd54f07f5d077502e0c33a9c1294b3d036c62021c0d07b4289`

## F04_TABLE — LibreOffice

- Timestamp: `2026-09-27T21:19:38.442551-07:00` to `2026-09-27T21:20:00.126125-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F04_TABLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F04_TABLE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=58095 bytes
- Source SHA-256: `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52`
- Output SHA-256: `cc7368bdca08aaa9906cc1d277fbfb9d68c29963e10e3247228a1d8c6b50a161`

## F04_TABLE — Google Docs

- Timestamp: `2026-09-28T04:43:56.295556+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\fixtures\F04_TABLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F04_TABLE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52`
- Output SHA-256: `32e260086253eb38625d3d740b2ee97ed58ce79c724268224d7d5cfd9487c232`

## F05_DOCUMENT_LANGUAGE — LibreOffice

- Timestamp: `2026-09-27T21:20:00.129534-07:00` to `2026-09-27T21:20:22.355271-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F05_DOCUMENT_LANGUAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F05_DOCUMENT_LANGUAGE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=48142 bytes
- Source SHA-256: `5a90d6861d7ec96c573733bd8668718cca584bd2d46702468ed0983fccc7ccec`
- Output SHA-256: `a8ad3f7e7106328b2190c8f80173a85ad73ac9d0285f46e0ccb8ae257e42b6ea`

## F05_DOCUMENT_LANGUAGE — Google Docs

- Timestamp: `2026-09-28T04:49:51.333584+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F05_DOCUMENT_LANGUAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F05_DOCUMENT_LANGUAGE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `5a90d6861d7ec96c573733bd8668718cca584bd2d46702468ed0983fccc7ccec`
- Output SHA-256: `07fed6839014d52b1c555e68e969c055d500cd0d7ccce403b561c92ae34b8983`

## F06_INLINE_LANGUAGE — LibreOffice

- Timestamp: `2026-09-27T21:20:22.358599-07:00` to `2026-09-27T21:20:44.518490-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F06_INLINE_LANGUAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F06_INLINE_LANGUAGE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=45993 bytes
- Source SHA-256: `388e3047d022a08a179858f40762c23b94e08429d3537eaeb1a876438a948d16`
- Output SHA-256: `26ba1995f163388a2372a330173f5890c0c71f33d39d79d5f0eb421af6289434`

## F06_INLINE_LANGUAGE — Google Docs

- Timestamp: `2026-09-28T04:51:06.127532+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F06_INLINE_LANGUAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F06_INLINE_LANGUAGE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `388e3047d022a08a179858f40762c23b94e08429d3537eaeb1a876438a948d16`
- Output SHA-256: `81803dfa98d51e57dfa45addf12f92e674986103b440d95d0ed36a123c48ad1e`

## F07_DECORATIVE_IMAGE — LibreOffice

- Timestamp: `2026-09-27T21:20:44.522259-07:00` to `2026-09-27T21:21:06.439491-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F07_DECORATIVE_IMAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F07_DECORATIVE_IMAGE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=49923 bytes
- Source SHA-256: `02b65084773bfd96272411945bed53b1a0bf46edc6359f4e34206e972cb98d70`
- Output SHA-256: `ccedf4b1de29147c868c14d1823c9f278e123160483a523174099708933105fd`

## F07_DECORATIVE_IMAGE — Google Docs

- Timestamp: `2026-09-28T04:52:14.799164+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F07_DECORATIVE_IMAGE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F07_DECORATIVE_IMAGE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `02b65084773bfd96272411945bed53b1a0bf46edc6359f4e34206e972cb98d70`
- Output SHA-256: `73689a12630c5c667b327dc60f010db3dad2672fb70a4a3d301375a33146a755`

## F08_LINKS — LibreOffice

- Timestamp: `2026-09-27T21:21:06.443021-07:00` to `2026-09-27T21:21:28.141933-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F08_LINKS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F08_LINKS__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=44223 bytes
- Source SHA-256: `3220a74dbfccc059b8e77e490faa48d7540a56f22e93e0b78548ee6ae4c05c60`
- Output SHA-256: `537965f4107356e3c5e635996e6c85fe20e1680233777ff9a7f5dfb48a6838ca`

## F08_LINKS — Google Docs

- Timestamp: `2026-09-28T04:53:03.862073+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F08_LINKS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F08_LINKS__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `3220a74dbfccc059b8e77e490faa48d7540a56f22e93e0b78548ee6ae4c05c60`
- Output SHA-256: `51fd966064ae00c340bf700392be61eccfa18f48466bab254b6179e8bc3afa93`

## F09_DOCUMENT_TITLE — LibreOffice

- Timestamp: `2026-09-27T21:21:28.145941-07:00` to `2026-09-27T21:21:48.490946-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F09_DOCUMENT_TITLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F09_DOCUMENT_TITLE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=45800 bytes
- Source SHA-256: `314b57e9d2457fc4ae8adf79f55587ecef9232b2dd689ea7cc98cb96772260f2`
- Output SHA-256: `dee063ecbfc8e34ff768823918a27d5f91ec808b17e0987b7c3dea7f2bd43573`

## F09_DOCUMENT_TITLE — Google Docs

- Timestamp: `2026-09-28T04:53:51.665624+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F09_DOCUMENT_TITLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F09_DOCUMENT_TITLE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `314b57e9d2457fc4ae8adf79f55587ecef9232b2dd689ea7cc98cb96772260f2`
- Output SHA-256: `2ddc8917cb666d7286751a2ec840752e5917ad8374d66b69dfc553bddd137eb2`

## F10_COMPLEX_TABLE — LibreOffice

- Timestamp: `2026-09-27T21:21:48.494136-07:00` to `2026-09-27T21:22:09.313271-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F10_COMPLEX_TABLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F10_COMPLEX_TABLE__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=58901 bytes
- Source SHA-256: `eacf8f49328015d6ce66084a92173f73b63bed4878a60943c8dbf0a7beeae992`
- Output SHA-256: `bf4152725ea25a1d286437db4f6f361a1946e2bc1571674293ea4a1cc36fa0ce`

## F10_COMPLEX_TABLE — Google Docs

- Timestamp: `2026-09-28T04:54:47.095127+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F10_COMPLEX_TABLE.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F10_COMPLEX_TABLE__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `eacf8f49328015d6ce66084a92173f73b63bed4878a60943c8dbf0a7beeae992`
- Output SHA-256: `864371121f6c47f0921111f941dd0de63c1cb9d87d951ab3bb874d95962a81e9`

## F11_FOOTNOTES — LibreOffice

- Timestamp: `2026-09-27T21:22:09.317256-07:00` to `2026-09-27T21:22:29.445261-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F11_FOOTNOTES.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F11_FOOTNOTES__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=46929 bytes
- Source SHA-256: `72b7182ee9e677f7a302a2f937bac054b321545239bab97be126ea6a01cbce47`
- Output SHA-256: `cba3852936716ce0eb593a4d4241e607d4309a1968d2b1920e5c63bfcbe135c4`

## F11_FOOTNOTES — Google Docs

- Timestamp: `2026-09-28T04:55:43.199342+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F11_FOOTNOTES.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F11_FOOTNOTES__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `72b7182ee9e677f7a302a2f937bac054b321545239bab97be126ea6a01cbce47`
- Output SHA-256: `91b81c06383c1c681023b3cd0a9c05cc9c4178bd696ad83287082d020f7372b9`

## F12_EQUATION — LibreOffice

- Timestamp: `2026-09-27T21:22:29.448600-07:00` to `2026-09-27T21:22:49.535874-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F12_EQUATION.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F12_EQUATION__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=59815 bytes
- Source SHA-256: `c9a89fb6999a90ad0abc8bff4ea81a10905ce4843c28d55d8df83f5ee87ba9f8`
- Output SHA-256: `b75f3d27673d0066f5ac05c5f1aa7580fb998f9f2e48717a91a2c9d3454e15c5`

## F12_EQUATION — Google Docs

- Timestamp: `2026-09-28T04:56:45.680720+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F12_EQUATION.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F12_EQUATION__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `c9a89fb6999a90ad0abc8bff4ea81a10905ce4843c28d55d8df83f5ee87ba9f8`
- Output SHA-256: `aafa553d252fe9db135d4fcb1e283aefe7c080094e8d6e783b883a19472848ca`

## F14_CAPTIONS — LibreOffice

- Timestamp: `2026-09-27T21:22:49.539652-07:00` to `2026-09-27T21:23:11.493376-07:00`
- Tool/version: `LibreOffice 26.2.6.3 8221e31b3ac356a1623c672912a3d2b492f7e3d1`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F14_CAPTIONS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\libreoffice\F14_CAPTIONS__LIBREOFFICE.pdf`
- Method: `headless soffice.com writer_pdf_Export`
- Settings: `UseTaggedPDF=true;PDFUACompliance=true;SelectPdfVersion=1`
- Result: `SUCCESS`; pages=1; tagged=True; size=55390 bytes
- Source SHA-256: `855438acee27f51c1f9e3a455a176ab73a4b18fc0a07b66ab38c59f8d9d52736`
- Output SHA-256: `fc2ca62c2fb7b06ac249d708f23e36cbd8b5211e854efa223ad2ae4c208a6b2e`

## F14_CAPTIONS — Google Docs

- Timestamp: `2026-09-28T04:57:35.598825+00:00` (downloaded file timestamp)
- Tool/version: Google Docs authenticated web application; PDF producer `Skia/PDF m156`; Chrome `153.0.8010.53`
- Source: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\fixtures\F14_CAPTIONS.docx`
- Destination: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\outputs\google_docs\F14_CAPTIONS__GOOGLE_DOCS.pdf`
- Method: authenticated browser UI upload followed by File → Download → PDF Document (.pdf); native Google Docs export
- Settings: Google Docs default PDF export; no print dialog; no manual document edits
- Result: `SUCCESS`; validated parseable/tagged output
- Source SHA-256: `855438acee27f51c1f9e3a455a176ab73a4b18fc0a07b66ab38c59f8d9d52736`
- Output SHA-256: `25e91306391e2aac667a668d553343c5bf071d5195644fc4c2285cea0f355a02`
