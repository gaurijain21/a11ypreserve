# Final V4 Adversarial Review

| Attack | Classification | Evidence / remaining issue |
|---|---|---|
| Novelty claims “first accessibility conversion study” | RESOLVED | Prior-art audit rejects that claim and states a combination-based contribution. |
| Too few variants per feature | RESOLVED | 65 fixtures, five meaningful variants per retained family. |
| Source truth is extractor-dependent | SUBSTANTIALLY MITIGATED | Raw-OOXML oracle, primary extractor, 65/65 certificates, and 39/39 mutation detections. |
| Comparator is biased or overconfident | SUBSTANTIALLY MITIGATED | 78 frozen controls, 0 false positives, 0 unsupported confident classifications; 5 false negatives remain. |
| Holdout is post-hoc | RESOLVED | D/E split and inspection rule frozen before converter execution. |
| Synthetic atomic corpus lacks external validity | SUBSTANTIALLY MITIGATED | Ten coherent project-created multi-page documents and 78 property contracts; no external documents. |
| Only two or three converters | ACCEPTED LIMITATION | No V4 converter environment was available; Word failed before conversion and LibreOffice was absent. |
| No actual V4 conversion results | SUBMISSION BLOCKER | Primary denominator is zero. |
| Reading order omitted | ACCEPTED LIMITATION | No defensible calibrated bounded oracle was established. |
| User impact not measured | ACCEPTED LIMITATION | Structural preservation, PDF accessibility, assistive technology, usability, and harm are explicitly separated. |
| Cloud route reproducibility | ACCEPTED LIMITATION | No authenticated Google session was available; no upload was attempted. |
| Artifact reproducibility | SUBSTANTIALLY MITIGATED | Source-only and calibration entry points plus manifests and hashes exist. |

Overall decision: NO-GO until at least one legitimate V4 converter pipeline produces a complete traceable output set and the frozen analysis is rerun.
