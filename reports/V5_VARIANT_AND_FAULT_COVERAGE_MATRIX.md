# V5 variant and fault coverage matrix

The five variants are the actual frozen V4 A–E fixtures, not a taxonomy
invented after conversion. A–C are development and D–E are holdout. The
machine-readable source manifests and OOXML ground truth remain the source of
truth; this table summarizes the dimensions visible in those contracts.

| Family | A | B | C | D | E | Fault/edge dimensions exercised |
|---|---|---|---|---|---|---|
| Headings | H1→H2 sequence | adds H3 | mixed depth/sequence | holdout level sequence | holdout level sequence | hierarchy depth, extra level, order, unseen variants |
| Alternative text | ordinary sentence | punctuation/length variation | Unicode punctuation | holdout wording | holdout wording | exact fidelity, punctuation, Unicode, unseen values |
| Lists | basic unordered | ordered | nested/mixed | holdout list type/depth | holdout list type/depth | type, nesting, item multiplicity/order |
| Basic tables | small header table | value variation | dimensions/headers variation | holdout table | holdout table | dimensions, header relation, cell values |
| Document language | default language | locale variation | language value variation | holdout locale | holdout locale | exact tag, locale normalization, unseen tag |
| Inline language | one override | alternate override | span/value variation | holdout span | holdout span | run scope, text association, non-default value |
| Decorative images | explicit decorative | meaningful image | state/value variation | holdout state | holdout state | Artifact/Figure distinction, image identity |
| Hyperlinks | one URI/name | two links | target/name variation | holdout link | holdout link | URI, visible name, multiplicity, association |
| Metadata | title | subject/keywords | combined metadata | holdout metadata | holdout metadata | field presence, field value, namespace behavior |
| Complex tables | grouped headers | spans/merges | header association variation | holdout grouped table | holdout grouped table | multi-level headers, gridSpan/vMerge, associations |
| Footnotes | one note | two notes | note text/reference variation | holdout note | holdout note | multiplicity, body text, reference identity |
| Equations | one OMML expression | two expressions | token/value variation | holdout expression | holdout expression | formula structure, token multiplicity, visible fallback risk |
| Captions | one figure/caption | caption text variation | association/order variation | holdout pair | holdout pair | text, figure identity, association versus adjacency |

Each row has a feature-specific comparator rule and abstention boundary in the
V5 equivalence specification. The strongest intentional negative controls are
the source mutation audit (39/39 source mutations) and the new destination
mutation arm; neither is interpreted as exhaustive mutation coverage.
