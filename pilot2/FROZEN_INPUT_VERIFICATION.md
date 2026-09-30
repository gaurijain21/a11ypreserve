# Frozen Input Verification

Verification timestamp (UTC): 2026-09-28T02:18:36.316629+00:00

The four source DOCX files were checked against `pilot/manifests/hashes.json` before conversion. All fixture hashes must match before the experiment may continue.

| Fixture | Filename | Size (bytes) | Expected SHA-256 | Actual SHA-256 | Match |
|---|---|---:|---|---|---|
| F01_HEADINGS | `F01_HEADINGS.docx` | 37029 | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | `367d8b6382e2446a387417a789e764968b98101e1fb0fd3381fb24d32c847407` | PASS |
| F02_ALT_TEXT | `F02_ALT_TEXT.docx` | 41331 | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | `f2219ef52e807ec417931a9d1c8a97320a95f4829d386a8f34b51990e88577da` | PASS |
| F03_LISTS | `F03_LISTS.docx` | 37064 | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | `96d918ed19a5974e31f30704fe89db4bcaa51628f1d9cc00d3c8eecd2779d97f` | PASS |
| F04_TABLE | `F04_TABLE.docx` | 37043 | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | `a9d129f7409afb5a3d9363eba423fa85b5760466406538e331e72a1e12412a52` | PASS |

Overall result: **PASS**.
