# ICST 2027 V3 checklist

## Paper

- [x] IEEE conference source and anonymous author block retained.
- [x] V3 claims use 52 atomic cases, 39 repeatability runs, and a separate 42-observation sanity check.
- [x] Related work names current adjacent conversion/evaluation work without first/unique claims.
- [x] F13 deferral and post-hoc taxonomy chronology are disclosed.
- [ ] Compile and visually inspect the V3 PDF; currently blocked by MiKTeX registry/configuration access and the built-in compiler's missing standard directories.
- [x] Confirm the official ICST 2027 allowance: at most 10 content pages plus up to 2 additional reference-only pages.
- [ ] Confirm V3 page count and references-only allowance from the generated PDF.

## Research

- [x] V2 evidence and files remain frozen.
- [x] Variant B source oracle: 13/13.
- [x] Variant B Google outputs: 13/13 valid and hashed.
- [x] Atomic benchmark: 52 cases with separate Core/Variant denominators.
- [x] Google repeatability: 13/13 classifications stable; 13/13 byte-identical.
- [x] F06 and F11 difficult-case audits complete.
- [x] Calibration false-negative impact documented.
- [x] Unresolved cases are not described as losses.

## Artifact

- [x] Separate `artifact_v3/` candidate assembled.
- [x] Variant B/Core oracle scripts and outputs included.
- [x] LibreOffice profile/cache debris excluded from the V3 ZIP.
- [x] ZIP scan found no personal filesystem paths, identity-linked strings, private-runtime directory names, browser profiles, or authentication-state files; documentation mentions the absence of cookies/tokens as a limitation without containing them.
- [ ] Human license and author-metadata decisions remain.

## Final gate

- [ ] Do not submit until the V3 PDF is compiled, rendered, visually inspected, metadata-checked, and its anonymity is confirmed.

See `FINAL_DESK_REJECTION_AUDIT.md`, `CLAIM_ARTIFACT_TRACE.md`, and `FINAL_PACKAGE_DECISION.md` for the current gate decision.
