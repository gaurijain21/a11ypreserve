# V5 adversarial review

| Reviewer attack | Severity | Status | Evidence / remaining concern |
|---|---|---|---|
| Software testing: contribution is only a PDF checker | HIGH | MITIGATED | Source-contract framing, holdout, differential routes, mutation tests, and abstention make the testing boundary explicit. |
| Software testing: source mutation does not validate destination chain | HIGH | RESOLVED for tested mutants | 59 valid destination mutants were attempted across all 65 atomic variants; 46 changed classification, 13 survived, six attempts were unsupported, and two produced measurement errors. Sixty-five no-op controls produced zero false positives. Mutation model is not exhaustive. |
| Software testing: holdout arithmetic leaks calibration/development | HIGH | RESOLVED | Machine audit derives 130 total, 52 holdout, 78 non-holdout from manifests. |
| Accessibility: tag presence is treated as semantics | HIGH | MITIGATED | V5 feature contracts require values, relations, and association evidence; unresolved cases abstain. |
| Accessibility: footnotes are overclaimed | HIGH | MITIGATED | `/Note` alone is insufficient; reference/body identity is required and uncertainty remains. |
| Accessibility: reading order is omitted | MEDIUM | RESOLVED as scope decision | Feasibility study records NO-GO rather than adding an arbitrary oracle. |
| Accessibility: exact fidelity is confused with usability | HIGH | RESOLVED in terminology | Reports distinguish source-value fidelity, machine-observable semantics, and user validity. |
| Empirical: profile mismatch changes LibreOffice result interpretation | HIGH | MITIGATED / V5 comparison | V4 is explicitly PDF/A-1b + tagged/PDF-UA; V5 normal-profile condition is separate. Final effect category is in the machine analysis. |
| Empirical: cloud backend cannot be pinned | MEDIUM | OPEN | Google temporal sessions and import/export localization remain deferred. |
| Empirical: project-created realistic documents are not external evidence | MEDIUM | OPEN but explicit | Natural arm is not fabricated; V4 realistic arm is labeled applicability only. |
| Empirical: independent oracle disagreement is high | HIGH | MITIGATED | Second implementation agrees on 8/26; disagreements are exposed and explained as a deliberately lighter oracle, not hidden. External adjudication is not claimed. |
| Novelty: “first benchmark” claim is unsupported | HIGH | RESOLVED | Prior-art report uses combination-based positioning and cites close benchmarks/standards. |
| Reproducibility: GUI/cloud routes cannot be replayed offline | MEDIUM | MITIGATED | Routes, versions, hashes, timestamps, producers, and failure boundaries are recorded; credentials/browser state are not distributed. |

The strongest remaining rejection arguments are limited natural-document and
temporal cloud evidence, incomplete generality of destination mutation models,
and the lack of external human adjudication. None changes the central
source-grounded testing question, but they bound the verdict.
