# Venue recommendation

Verified against official venue pages on 2026-09-29.

## Primary recommended venue

IEEE ICST 2027 Research Papers.

## Why this paper fits

ICST's official scope explicitly includes empirical studies, replication and case studies, testing tools, and testing of non-functional properties such as accessibility. A11yPreserve is strongest as a controlled source-to-destination conformance protocol: it freezes feature contracts, checks source representations, records provenance, compares cross-format structure, and separates verified preservation from observed change, unresolved equivalence, and measurement error. That is a testing-methodology contribution with a bounded empirical application.

The paper does not present itself as a general PDF validator, a product ranking, or a user study. Its narrow claim boundary is appropriate for a testing venue and is supported by an anonymized replication package.

## Main reviewer risk

Reviewers may argue that 13 controlled fixtures and two pipelines are too small for broad converter conclusions, or that the absence of a disabled-user study limits accessibility significance. The manuscript now addresses this directly: fixtures are atomic and non-representative, counts are descriptive, unresolved equivalence is not degradation, Google Docs is an end-to-end cloud pipeline rather than an isolated exporter, and no claim is made about task completion or user impact. The contribution is the protocol and evidence chain, not a population estimate.

## Required manuscript adaptation

The submission copy uses the IEEE conference two-column format, preserves the frozen evidence-aware counts, retains the DocAccessible/DAISY and other prior-art distinctions, keeps the two confirmed-loss table, explains deferred F13, and uses an anonymous author block. No fixture, PDF, manifest, classification, denominator, research question, or scientific interpretation was changed.

The official ICST page requires a maximum of 10 pages including content, with up to 2 additional pages for references. The current copy is 9 pages total, including references. The exact venue template should be rechecked before upload; the local build uses the current IEEEtran class and bibliography style obtained from CTAN because the official IEEE template endpoint was inaccessible in this environment.

## Required artifact adaptation

The artifact candidate is separated from the canonical project, contains the frozen DOCX/PDF evidence and contracts, includes the core extractor/comparator/oracle code, records reproducibility levels, and removes local paths from publication copies. It contains no browser profile, cookies, authentication state, token, or credential. The package remains anonymous and is not published by this task.

## Current submission timing

The official ICST 2027 page lists the research-paper deadline as Nov 2, 2026, with all deadlines AoE (UTC-12), initial notification Dec 22, major-revision submission Jan 31, 2027, final notification Feb 20, and camera-ready Mar 18, 2027. Submission is through the ICST 2027 HotCRP site linked from the official track page. The same page says anonymized replication material is expected when applicable and that associated artifacts must be anonymized.

## Backup venue

ACM DocEng, next available cycle.

## Why backup differs

DocEng is the strongest topical match because the work is fundamentally about document transformation, document representations, and preservation across conversion pipelines. It is not the current primary only because DocEng 2026 is closed and the DocEng 2027 CFP and deadlines are not yet published. Its 2026 call used a 10-page ACM format and a single-blind review with an auxiliary-material package, so the artifact is being prepared in a form that can be adapted later.

Official sources: [ICST 2027 research track](https://conf.researchr.org/track/icst-2027/icst-2027-research-papers), [DocEng 2026 CFP](https://doceng.org/doceng2026/cfp), and [DocEng submission rules](https://doceng.org/doceng2026/submission).
