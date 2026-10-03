# F02 Classification Refinement

Pilot 2 used a single legacy classification and reported the LibreOffice result as `DEGRADED`. Pilot 3 separates preservation fidelity from destination accessibility.

## Source value

`Bar chart showing enrollment increasing from 120 students in 2024 to 180 students in 2026.`

## LibreOffice

Destination `/Alt`: `Enrollment chart - Bar chart showing enrollment increasing from 120 students in 2024 to 180 students in 2026.`

- Preservation fidelity: **MUTATED**
- Destination accessibility: **ACCESSIBLE_BUT_ALTERED**
- Rationale: the destination has meaningful alternative text, but it is not the author-written source string.

## Google Docs

Destination `/Alt`: `Bar chart showing enrollment increasing from 120 students in 2024 to 180 students in 2026.`

- Preservation fidelity: **EXACT_PRESERVATION**
- Destination accessibility: **ACCESSIBLE_EQUIVALENT**
- Rationale: the PDF `/Alt` exactly matches the source value.

The refinement does not alter Pilot 2 evidence or frozen source truth; it adds a more expressive Pilot 3 taxonomy.
