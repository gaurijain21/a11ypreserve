# Non-Preservation Audit

Every non-PRESERVED result was challenged against source ground truth, PDF capability, structural evidence, parser coverage, and independent page-text corroboration. A result is not treated as converter loss when the current extractor cannot establish the required association.

## F01_HEADINGS — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\manifests\F01_HEADINGS.json`
- Source hash: `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407`
- PDF hash: `d6a8a93a8cd0a347448aeb65a86fd1b386dfd6204a23ab449d35da28255ce9bc`
- Structural extraction: tagged=True; headings=5; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F01_HEADINGS\google_docs_pdftotext.txt`
- Falsification result: PDF contains heading structure but the level/order sequence differs from source

## F02_ALT_TEXT — LibreOffice

- Classification: `ALTERED`; destination accessibility: `ACCESSIBLE_BUT_ALTERED`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\manifests\F02_ALT_TEXT.json`
- Source hash: `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da`
- PDF hash: `1837537f7f2a4b59c3cab974a9a1f0bb1f527e2271181a685e31986d98fdc272`
- Structural extraction: tagged=True; headings=0; figures=1; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F02_ALT_TEXT\libreoffice_pdftotext.txt`
- Falsification result: destination retains non-decorative figures with different alternative text

## F03_LISTS — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\pilot\manifests\F03_LISTS.json`
- Source hash: `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f`
- PDF hash: `d4342499a757d4cd54f07f5d077502e0c33a9c1294b3d036c62021c0d07b4289`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=11; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F03_LISTS\google_docs_pdftotext.txt`
- Falsification result: list items and nesting survive, but PDF extraction found no explicit ordered/unordered type representation

## F05_DOCUMENT_LANGUAGE — Google Docs

- Classification: `ALTERED`; destination accessibility: `ACCESSIBLE_BUT_ALTERED`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F05_DOCUMENT_LANGUAGE.json`
- Source hash: `5a90d6861d7ec96c573733bd8668718cca584bd2d46702468ed0983fccc7ccec`
- PDF hash: `07fed6839014d52b1c555e68e969c055d500cd0d7ccce403b561c92ae34b8983`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F05_DOCUMENT_LANGUAGE\google_docs_pdftotext.txt`
- Falsification result: No additional interpretation; raw evidence is retained in the JSON diff and extraction artifact.

## F06_INLINE_LANGUAGE — Google Docs

- Classification: `LOST`; destination accessibility: `INACCESSIBLE_FEATURE`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F06_INLINE_LANGUAGE.json`
- Source hash: `388e3047d022a08a179858f40762c23b94e08429d3537eaeb1a876438a948d16`
- PDF hash: `81803dfa98d51e57dfa45addf12f92e674986103b440d95d0ed36a123c48ad1e`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F06_INLINE_LANGUAGE\google_docs_pdftotext.txt`
- Falsification result: document language may survive while inline override is absent

## F07_DECORATIVE_IMAGE — LibreOffice

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F07_DECORATIVE_IMAGE.json`
- Source hash: `02b65084773bfd96272411945bed53b1a0bf46edc6359f4e34206e972cb98d70`
- PDF hash: `ccedf4b1de29147c868c14d1823c9f278e123160483a523174099708933105fd`
- Structural extraction: tagged=True; headings=0; figures=2; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F07_DECORATIVE_IMAGE\libreoffice_pdftotext.txt`
- Falsification result: destination uses Figure elements with empty alternative text; no explicit PDF Artifact/decorative representation was established

## F07_DECORATIVE_IMAGE — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F07_DECORATIVE_IMAGE.json`
- Source hash: `02b65084773bfd96272411945bed53b1a0bf46edc6359f4e34206e972cb98d70`
- PDF hash: `73689a12630c5c667b327dc60f010db3dad2672fb70a4a3d301375a33146a755`
- Structural extraction: tagged=True; headings=1; figures=2; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F07_DECORATIVE_IMAGE\google_docs_pdftotext.txt`
- Falsification result: destination uses Figure elements with empty alternative text; no explicit PDF Artifact/decorative representation was established

## F08_LINKS — LibreOffice

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F08_LINKS.json`
- Source hash: `3220a74dbfccc059b8e77e490faa48d7540a56f22e93e0b78548ee6ae4c05c60`
- PDF hash: `537965f4107356e3c5e635996e6c85fe20e1680233777ff9a7f5dfb48a6838ca`
- Structural extraction: tagged=True; headings=0; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F08_LINKS\libreoffice_pdftotext.txt`
- Falsification result: URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure

## F08_LINKS — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F08_LINKS.json`
- Source hash: `3220a74dbfccc059b8e77e490faa48d7540a56f22e93e0b78548ee6ae4c05c60`
- PDF hash: `51fd966064ae00c340bf700392be61eccfa18f48466bab254b6179e8bc3afa93`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F08_LINKS\google_docs_pdftotext.txt`
- Falsification result: URI and link annotation survive; visible link-name association was not independently recoverable from the PDF structure

## F09_DOCUMENT_TITLE — Google Docs

- Classification: `ALTERED`; destination accessibility: `ACCESSIBLE_BUT_ALTERED`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F09_DOCUMENT_TITLE.json`
- Source hash: `314b57e9d2457fc4ae8adf79f55587ecef9232b2dd689ea7cc98cb96772260f2`
- PDF hash: `2ddc8917cb666d7286751a2ec840752e5917ad8374d66b69dfc553bddd137eb2`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F09_DOCUMENT_TITLE\google_docs_pdftotext.txt`
- Falsification result: No additional interpretation; raw evidence is retained in the JSON diff and extraction artifact.

## F10_COMPLEX_TABLE — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F10_COMPLEX_TABLE.json`
- Source hash: `eacf8f49328015d6ce66084a92173f73b63bed4878a60943c8dbf0a7beeae992`
- PDF hash: `864371121f6c47f0921111f941dd0de63c1cb9d87d951ab3bb874d95962a81e9`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=15; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F10_COMPLEX_TABLE\google_docs_pdftotext.txt`
- Falsification result: PDF table and header roles survive, but complete multi-level header associations are not established

## F11_FOOTNOTES — LibreOffice

- Classification: `MEASUREMENT_ERROR`; destination accessibility: `UNKNOWN`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F11_FOOTNOTES.json`
- Source hash: `72b7182ee9e677f7a302a2f937bac054b321545239bab97be126ea6a01cbce47`
- PDF hash: `cba3852936716ce0eb593a4d4241e607d4309a1968d2b1920e5c63bfcbe135c4`
- Structural extraction: tagged=True; headings=0; figures=0; list nodes=1; tables=0; footnotes=1; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F11_FOOTNOTES\libreoffice_pdftotext.txt`
- Falsification result: PDF /Note structure exists, but marked-content extraction did not recover note-body text for association verification

## F11_FOOTNOTES — Google Docs

- Classification: `LOST`; destination accessibility: `INACCESSIBLE_FEATURE`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F11_FOOTNOTES.json`
- Source hash: `72b7182ee9e677f7a302a2f937bac054b321545239bab97be126ea6a01cbce47`
- PDF hash: `91b81c06383c1c681023b3cd0a9c05cc9c4178bd696ad83287082d020f7372b9`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F11_FOOTNOTES\google_docs_pdftotext.txt`
- Falsification result: visible reference and note text survive, but pypdf traversal and PyMuPDF serialized-object inspection both find no `/Note`, `/Footnote`, or equivalent association structure. The frozen loss is therefore limited to the machine-verifiable footnote association.

## F12_EQUATION — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F12_EQUATION.json`
- Source hash: `c9a89fb6999a90ad0abc8bff4ea81a10905ce4843c28d55d8df83f5ee87ba9f8`
- PDF hash: `aafa553d252fe9db135d4fcb1e283aefe7c080094e8d6e783b883a19472848ca`
- Structural extraction: tagged=True; headings=1; figures=0; list nodes=0; tables=0; footnotes=0; equations=0; captions=0
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F12_EQUATION\google_docs_pdftotext.txt`
- Falsification result: equation rendering is present in page text/content, but no machine-readable PDF math structure was extracted

## F14_CAPTIONS — Google Docs

- Classification: `PARTIALLY_PRESERVED`; destination accessibility: `DEGRADED_ACCESSIBILITY`
- Source manifest/OOXML: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\corpus\manifests\F14_CAPTIONS.json`
- Source hash: `855438acee27f51c1f9e3a455a176ab73a4b18fc0a07b66ab38c59f8d9d52736`
- PDF hash: `25e91306391e2aac667a668d553343c5bf071d5195644fc4c2285cea0f355a02`
- Structural extraction: tagged=True; headings=1; figures=1; list nodes=0; tables=0; footnotes=0; equations=0; captions=1
- Independent text evidence: `C:\Users\iamga\OneDrive\Documents\ChatGPT\a11ypreserve\results\full_experiment\evidence\F14_CAPTIONS\google_docs_pdftotext.txt`
- Falsification result: No additional interpretation; raw evidence is retained in the JSON diff and extraction artifact.
