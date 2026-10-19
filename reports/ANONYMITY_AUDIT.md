# Anonymity audit

The anonymous manuscript and `artifact_v3/` are separate from the working repository. Existing package checks scan text-like release files for user paths, names, and identity-bearing metadata; the artifact self-check passes. `.git` is excluded from the review artifact.

The final upload still requires a human check of the actual archive and portal metadata because generated PDFs, archive metadata, and venue fields can change at packaging time. No scientific evidence should be sanitized in place; only submission copies may receive metadata/path sanitization.
