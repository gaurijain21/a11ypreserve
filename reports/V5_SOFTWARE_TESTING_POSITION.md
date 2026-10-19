# V5 software-testing contribution position

| Testing concept | A11yPreserve mapping |
|---|---|
| Controlled test input | DOCX fixture with a verified source contract |
| Specification oracle | Feature-specific source accessibility contract |
| System under test | Named DOCX→PDF converter workflow |
| Observation mechanism | PDF structure, objects, annotations, marked content, metadata, and corroborating parsers |
| Decision procedure | Cross-format comparator with explicit abstention |
| Source mutation testing | 39/39 deliberate source-oracle mutations detected in V4 |
| Destination mutation testing | V5 controlled PDF-structure mutants test end-to-end fault sensitivity |
| Differential testing | Same frozen DOCX contracts are exercised through distinct real pipelines |
| Regression testing | Frozen hashes, manifests, contracts, reports, and repeatability checks detect drift |
| Holdout | D/E fixture-level prospective evaluation against rule tuning |
| Applicability testing | Project-created realistic arm; natural-document arm deferred for lack of rights-cleared evidence |

The methodology is specification-based testing of a transformation boundary.
It uses differential testing across converters and mutation testing to probe
oracle sensitivity. It is not a repair tool, a global converter ranking, or a
complete PDF accessibility checker. Metamorphic testing is only a possible
future extension; the current evidence does not claim a metamorphic oracle.
