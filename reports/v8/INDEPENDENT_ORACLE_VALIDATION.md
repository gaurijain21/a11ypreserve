# Independent reference-oracle validation

Status: COMPLETED WITH LIMITATIONS.

The reference procedure is a separately implemented mechanical oracle for
direct mutation transitions. It compares source-contract manifests with raw
destination object changes and checks the resulting PDF with two independent
parsers. It is independent of the frozen extraction/comparison implementation
in the sense that it does not import that code or read its derived evidence;
it is not independent human adjudication and it shares PDF standards and
library assumptions with the artifact under test.

All 59 applied Tier-A mutants satisfied their pre-specified transition rule,
with zero unresolved Tier-A cases and zero false semantic-fault alerts under
that rule. The six unsupported attempts remain unsupported rather than being
promoted by parseability. The reference procedure therefore provides a
defensible answer to “did this named injected fault occur?” but not to the
broader question “is this PDF accessible to a person using assistive
technology?”

Evidence: `experiments/v8/V8_MUTATION_GROUND_TRUTH.json` and the case files;
implementation: `scripts/v8_mutation_ground_truth_audit.py`.
