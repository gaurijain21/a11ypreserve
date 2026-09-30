# Reviewer Attack

## Strong objections and answers

1. **“This is Roig and Ribera again.”** Correct in the broad problem statement. The response is to cite them, narrow the claim, and contribute a reproducible manifest/comparator plus explicit states for mutation, regeneration, unsupported representation and measurement failure.

2. **“This is an accessibility checker in disguise.”** The comparator must require a source manifest and report the relation between source and output. An output-only check is deliberately out of scope.

3. **“PDF parsers cannot see enough structure.”** Correct. The method must report `MEASUREMENT_ERROR`, use a PDF structure-aware adapter where available, and independently verify selected cases with object inspection or assistive-technology review. It must not infer loss from an empty extractor field.

4. **“Your source fixture may already be inaccessible or malformed.”** Generate fixtures with a standard library, validate the package in a real editor, maintain an author-supplied manifest, and use a second extractor as a negative/control check. The first handcrafted OOXML fixture failed Word open; the repaired python-docx fixture opened, demonstrating why this control is necessary.

5. **“The scope is too broad.”** Limit the main study to two source families, three target representations, and two independently implemented conversion paths. Do not promise every office format, PDF flavor, or assistive technology.

6. **“AI-generated alt text is preservation.”** It is not. If source and output differ but output contains a plausible alternative, classify `REGENERATED` only when provenance shows the converter created it; otherwise `MUTATED` or `MEASUREMENT_ERROR`.

7. **“Visual similarity is semantic equivalence.”** Maintain separate visual, textual, and structural feature channels. A PDF can look perfect while losing headings or table relationships.

8. **“Benchmarks already exist.”** Acknowledge DAISY and DocAccessible explicitly. The narrower gap is a controlled authored-source experiment with declared source intent and representation-aware outcomes, not a claim that no benchmark exists.

## Killer weakness

Without at least two independent conversion engines and one manual/AT confirmation path, this remains a useful prototype rather than a convincing empirical study. That is a continuation gate, not evidence for killing the research question.

