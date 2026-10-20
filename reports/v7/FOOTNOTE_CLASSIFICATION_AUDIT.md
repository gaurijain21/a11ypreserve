# Footnote classification audit

The frozen feature matrix records all five LibreOffice and Word footnote cases
as measurement error and all five Google Docs cases as unresolved equivalence.
The available raw evidence contains note-like structure or visible note text,
but it does not reliably establish the reference/body association for the
contract.

The V7 independent audit observed `/Note` roles in 5 cases and no `/Note` role
in 10 cases across the archived 195-case set, but this observation alone is not
an association oracle. The V7 association attack changed a `/Note` role and was
detected by the frozen comparator on the selected footnote case. This does not
justify converting the historical measurement-error or unresolved rows into
preservation or confirmed loss.

Evidence: `experiments/v7/V7_INDEPENDENT_ORACLE.json`,
`experiments/v7/V7_ASSOCIATION_ATTACKS.json`, and
`submission/ICST2027_V6/sections/results.tex`.
