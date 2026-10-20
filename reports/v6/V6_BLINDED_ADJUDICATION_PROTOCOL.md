# V6 blinded adjudication protocol

## Purpose

This protocol is prepared to reduce the remaining independent-ground-truth objection without fabricating an adjudication. It is a future human-review arm and is not an executed V6 result.

## Packet population

The packet index covers the 26 cases in `experiments/v5/independent_oracle_validation.json`. Each packet has a stable opaque ID, the PDF hash, and a pointer to the preserved evidence record. The expected comparator and diagnostic labels are omitted from the packet index. A coordinator must create a separate key before review and must not give reviewers the historical labels.

## Reviewer task

For each packet, the reviewer receives the source contract, source OOXML excerpts needed for the feature, the destination PDF, and extracted evidence from the independent paths. The reviewer records one of: `PRESERVED`, `ALTERED`, `LOST`, `PARTIAL`, `UNRESOLVED`, or `MEASUREMENT_ERROR`, plus an evidence citation and confidence. If the evidence cannot establish the relation, the reviewer must abstain rather than infer from tags, visible text, or the expected result.

## Blinding and adjudication

Reviewers must not see fixture IDs, pipeline labels, historical classifications, or mutation outcomes. Two qualified reviewers should work independently. Disagreements should be resolved by a third adjudicator or a documented consensus procedure. Report agreement, abstention, disagreement reasons, and the final rubric version. Do not pool reviewer labels with V4/V5 classifications without a separately versioned analysis.

## Current status

`PENDING_HUMAN_REVIEW`. No reviewer, adjudication, agreement statistic, or independent ground-truth claim is asserted by this repository state.
