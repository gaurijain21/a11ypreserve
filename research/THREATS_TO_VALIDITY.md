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

