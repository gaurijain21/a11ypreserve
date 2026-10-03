# Variant Set B source freeze

**Status: SOURCE INPUTS FROZEN BEFORE CONVERSION OUTPUT INSPECTION**

Variant Set B is separate from the V2 Core corpus and denominator. The source design was written in `VARIANT_SET_B_DESIGN_SPEC.md` before converted output review. The generator then created exactly 13 DOCX variants and manifests. The raw-OOXML source oracle is run separately by `scripts/v3_variant_source_oracle.py`.

| Variant | Core family | DOCX SHA-256 | Manifest SHA-256 |
|---|---|---|---|
| B01 | F01 headings | `9f1df6ab640a6103c76a939da2f6ef9caa91259f6755f245763b784092eb0bfc` | `ce7225b7ef4f5c21a592e53310735303cf0ec2b45f11f2e938153ab81db87ef5` |
| B02 | F02 alt text | `1cead1de4f9f0bef290aeeb197dd821f6b2997ae2dd41497006805084ade6573` | `8203cf6abc6a83ef92a5bbb23011144cc62d1f8d5f2ac05f66813e6c7da788d7` |
| B03 | F03 lists | `9b43093cd128f30bd4deb0198626c54e369acdcf9c77519ace0384930d4ada39` | `068763dbc2be6a1905b2864ebd34ff5cf8e7508b639d6e016c865023d3f541c6` |
| B04 | F04 table | `6553600a2b9a3020b28f710437b16877e03564bb686acb45d87cf784187e60d2` | `aa2c8ac22fabdb42a78ed2a4074f1bf7cb3e4eaf5647f2d01d92a22f3e8814ee` |
| B05 | F05 document language | `8b48703bde441d8e8f80363a990a402b66373c671ed19a1d355fe5dc46a14630` | `796ecd28b2228c42f4f39a5ef756108fea811d119bb2d505fc984bb4a9a5e840` |
| B06 | F06 inline language | `fd39901d30a5cd595b71919f39950543e27e3b14708823b4b65be3a5de3c6180` | `6e3a5ae463d6cdba333b488599ba68f8c5bc6721b22caec03b662d503db8d45b` |
| B07 | F07 decorative image | `f508aae9ce27d4255f2245b4fa4277775898c9772aabf106bcfda8b8d49933a9` | `3c0084554331695f18507dc694c19cb9f1dcba99fe57ae0f75d7f9e5087dfe3` |
| B08 | F08 links | `6a5c9de8c6d86f183e69aa8d600d90f9f96303032a6acb50818686f04cb3639e` | `8d73cff145216ea8fae566dfc8f43f404736c549ee773dfed60ef6a91c7542de` |
| B09 | F09 title/metadata | `85cae9bf566e725e281b5592b18ed3ffdc9155c28e4befed69e117a7b817c36b` | `4257a2e92174ab30260978b71b1c62f5e9363e5d82a159679fda70ff4308cf9b` |
| B10 | F10 complex table | `f511362eb8ea6848a1906d1224582e0439d35190a4a2e3b559149a53bc8f8b1b` | `a91aa358dda8937a70305300e32d8b9bee6af513e9974a957a2e0ac371359d81` |
| B11 | F11 footnotes | `6ea7f908792a052591e5dd5fd55d1be9278fb080b70988c85172f3086e25d5db` | `921eabb3fb790f807113f1fcbbb5ec107345e9bc0268f6ce76a018a4eaaaf1c9` |
| B12 | F12 equation | `d2338440d2cbfe1ac9310c1a0e033dd5ee8c285f552eeed734cec125118c6b4b` | `09c88bb40cab8bc02609c91435e6d61ea25fda992b5644e6d529dfc1ca80796a` |
| B13 | F14 captions | `4010a76ff3715c5c487158f87c89cf7a2b7fa3e429739b15c6a9bac8c7b6e91c` | `901267ddf7211c71c5f23d2c4c48a06a6e0598c5fdfbbb21e2f5838d56680ecb` |

No Variant Set B PDF was inspected when this freeze was created. If a source-oracle disagreement occurs, conversion is stopped and the source artifact is repaired or excluded in a separately documented V3 decision; the V2 Core remains untouched.
