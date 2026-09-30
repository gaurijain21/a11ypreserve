# Threats to Validity

## Construct

“Accessibility” is multidimensional. Mitigate by measuring explicit features—language, headings, list nesting, image alternatives, table headers, reading order and links—in separate channels, not by one score.

## Internal

Malformed sources, unstable converters, hidden defaults and stale output files can mimic semantic loss. Mitigate with package validation, source/output hashes, clean output directories, version capture and invalid-conversion classification.

## Measurement

PDF libraries often expose text and metadata but not tag-tree semantics. Missing fields are not losses. Use route-specific adapters, object-level inspection, independent tools and manual/AT checks; otherwise report `MEASUREMENT_ERROR`.

## External

One fixture and one browser do not generalize. Use multiple authoring source families, content complexity levels and at least two engines before making comparative claims.

## Provenance

A converter may regenerate alt text or infer headings. Record engine, version, configuration and evidence of generated content; classify regeneration separately from preservation.

## Platform

This pilot is Windows-specific and encountered Word COM/session and Acrobat-export-path limitations. Re-run on a clean, documented environment and include a second platform where practical.

## Human validation

Automated checks cannot establish usability. A publication-grade study needs blind/low-vision review or qualified accessibility review for a stratified subset, with the protocol and disagreements reported.
# Phase 4 threats and mitigations

This document supplements the earlier pilot discussion. The benchmark measures
source-grounded semantic preservation; it does not claim to measure every
dimension of accessibility or user experience.

| Threat | Why it matters | Mitigation |
|---|---|---|
| Synthetic fixtures | Small atomic documents may not represent real authoring practice. | Use explicit contracts and causal isolation first, then add a small integrated-document set and optionally licensed real documents for external validity. |
| Limited converter versions | Results can be version-specific. | Record exact application/build/version and treat each version as a separate experimental condition. |
| Google Docs cloud updates | A cloud service may change without notice. | Record export date, account/workflow, downloaded output hash, and rerun a small sentinel set when the service changes. |
| Windows dependence | Word COM and some office workflows are platform-specific. | Keep LibreOffice and Google Docs as primary engines; report Windows as an environment constraint and do not make Word a blocker. |
| Semantic-equivalence judgment | Some source concepts have more than one defensible PDF representation. | Freeze contracts, distinguish exact from semantic equivalence, retain raw evidence, and mark unresolved cases `MEASUREMENT_ERROR` or `UNKNOWN`. |
| Parser correctness | A parser can miss a valid representation or invent an association. | Inspect raw PDF objects, use independent parser checks where available, add extractor regression tests, and never infer loss from an unsupported parser. |
| PDF representation differences | Tagged PDFs can encode equivalent content using different structure paths or role maps. | Resolve role maps, inspect marked content/parent relationships, and document representation-specific limits. |
| Feature weighting | A single aggregate rate can hide important feature failures. | Report feature-level matrices first; use only descriptive unweighted counts unless a weighting scheme is independently justified. |
| Missing human-user evaluation | Structural preservation is not the same as assistive-technology usability. | Treat human/AT evaluation as a later complementary study, not as evidence silently substituted into this benchmark. |
| Converter settings | Defaults and export options can change semantics. | Freeze and log all settings; use native tagged export; prohibit print-to-PDF substitutes. |
| Proprietary software | Word and Acrobat/PAC may be unavailable or non-reproducible. | Make open/accessible routes primary where possible, record tool absence, and treat validators as secondary evidence. |
| Fixture asset quality | A poor visual asset could confound an alt-text test. | Render and inspect every page; retain the source image and inspect the OOXML description independently. |
| Integrated-feature interactions | A converter may behave differently when features co-occur. | Keep atomic fixtures for attribution, then evaluate integrated documents as a separate ecological-validity layer. |
| Statistical underpowering | One instance per feature cannot estimate population rates. | Label Phase 4 as benchmark construction/readiness; add justified variants before making population-level claims. |
| Reproducibility and drift | Locale, fonts, cloud state, and parser versions affect output. | Record environment metadata, hashes, versions, dates, and all evidence; never overwrite frozen artifacts. |

The benchmark therefore supports bounded claims such as: “under converter
version V and settings S, fixture F preserved or changed semantic feature Z.”
It does not support global claims that a converter is accessible or
inaccessible overall.
