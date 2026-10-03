"""Build the V3 secondary/atomic reports from frozen rules and evidence.

The Core rows are copied from the frozen evidence-aware V2 result file without
changing it.  Variant B rows use the explicitly recorded V3 evidence decisions
below; unresolved rows are conservative abstentions, not failures.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from extract_semantics import extract  # noqa: E402

V2 = ROOT / "results" / "full_experiment" / "FINAL_EVIDENCE_AWARE_RESULTS.json"
VARIANT_BASE = ROOT / "v3" / "variant_set_b"
GOOGLE_BASE = ROOT / "v3" / "variant_set_b" / "google"

VARIANT_DECISIONS = {
    ("B01", "LibreOffice"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "four source heading levels and four destination heading levels agree"),
    ("B01", "Google Docs"): ("OBSERVED_PARTIAL", "OBSERVED_PARTIAL", "the destination has the expected hierarchy plus an additional generated H1; levels are directly observed but exact source mapping is not exact"),
    ("B02", "LibreOffice"): ("ALTERED", "OBSERVED_DIFFERENCE", "two Figure nodes survive but both author-supplied alt values acquire exporter-added prefixes"),
    ("B02", "Google Docs"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "two Figure nodes retain the exact source alt values"),
    ("B03", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "list roles and nesting are observed, but the extracted destination evidence does not recover the source item text/type contract"),
    ("B03", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "list roles and nesting are observed, but item text/type equivalence is not established"),
    ("B04", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "table and header-cell structure are observed, but complete source-cell correspondence is not established by the destination extractor"),
    ("B04", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "table and header-cell structure are observed, but complete source-cell correspondence is not established by the destination extractor"),
    ("B05", "LibreOffice"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "document language fr-FR is directly observed"),
    ("B05", "Google Docs"): ("ALTERED", "OBSERVED_DIFFERENCE", "document language is present with reduced specificity (fr-FR -> fr)"),
    ("B06", "LibreOffice"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "both non-default inline language spans are directly observed as fr-FR and es-ES"),
    ("B06", "Google Docs"): ("CONFIRMED_LOST", "INDEPENDENTLY_CONFIRMED_ABSENCE", "required inline language representations are absent from the traversed structure tree and serialized-object scans; visible text remains"),
    ("B07", "LibreOffice"): ("ALTERED", "OBSERVED_DIFFERENCE", "three Figure nodes survive but the source decorative empty state becomes a non-decorative figure with alt text"),
    ("B07", "Google Docs"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "three Figure nodes retain the two informative alt values and the empty decorative state"),
    ("B08", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "two link annotations survive, but destination evidence does not establish source visible-text association"),
    ("B08", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "two link annotations survive, but destination evidence does not establish source visible-text association"),
    ("B09", "LibreOffice"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "document title metadata matches the source contract"),
    ("B09", "Google Docs"): ("ALTERED", "OBSERVED_DIFFERENCE", "visible title text remains, but exported core title metadata is reduced to the generated document title"),
    ("B10", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "complex table/header structure is observed, but complete multi-level association equivalence is not established"),
    ("B10", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "complex table/header structure is observed, but complete multi-level association equivalence is not established"),
    ("B11", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "Note structure is observed, but the extracted evidence does not establish exact note text/reference mapping"),
    ("B11", "Google Docs"): ("CONFIRMED_LOST", "INDEPENDENTLY_CONFIRMED_ABSENCE", "required Note/Reference association is absent from the traversed structure tree and serialized-object scans; visible note text remains"),
    ("B12", "LibreOffice"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "two Formula nodes are observed, but their machine-readable expression equivalence is not established"),
    ("B12", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "visible equations are present in page text, but the required machine-readable formula representation is not established"),
    ("B13", "LibreOffice"): ("VERIFIED_PRESERVED", "VERIFIED_EQUIVALENCE", "two Caption structures and ordered caption text match the source contract"),
    ("B13", "Google Docs"): ("UNRESOLVED_EQUIVALENCE", "UNRESOLVED_EQUIVALENCE", "caption text is present by ordered page-text evidence, but a destination Caption association is not established"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def extract_to(path: Path, output: Path) -> dict:
    value = extract(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return value


def main() -> None:
    frozen = json.loads(V2.read_text(encoding="utf-8"))
    core_rows = []
    for item in frozen["records"]:
        row = dict(item)
        row["study_arm"] = "Core"
        row["frozen_source"] = True
        core_rows.append(row)

    variant_rows = []
    for manifest_path in sorted((VARIANT_BASE / "../.." / "corpus" / "v3_variant_set_b" / "manifests").glob("B*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        variant = manifest["variant_id"]
        feature = manifest["feature_family"]
        source = ROOT / manifest["fixture_path"]
        for pipeline in ("LibreOffice", "Google Docs"):
            if pipeline == "LibreOffice":
                output = VARIANT_BASE / "libreoffice" / "outputs" / f"{variant}__LIBREOFFICE.pdf"
            else:
                output = GOOGLE_BASE / "outputs" / f"{variant}__GOOGLE_DOCS.pdf"
            classification, status, note = VARIANT_DECISIONS[(variant, pipeline)]
            extraction_dir = VARIANT_BASE / ("libreoffice" if pipeline == "LibreOffice" else "google") / "extracted"
            observed = extract_to(output, extraction_dir / f"{variant}.json")
            variant_rows.append({
                "fixture": variant,
                "feature_family": feature,
                "pipeline": pipeline,
                "study_arm": "Variant B",
                "historical_v1_outcome": None,
                "final_evidence_aware_result": classification,
                "evidence_status": status,
                "source_sha256": sha256(source),
                "destination_sha256": sha256(output),
                "source_manifest": rel(manifest_path),
                "destination_extraction": rel(extraction_dir / f"{variant}.json"),
                "supporting_artifact": rel(ROOT / "v3" / "variant_set_b" / "google" / "DIFFICULT_CASE_AUDIT.json") if variant in {"B06", "B11"} and pipeline == "Google Docs" else rel(ROOT / "v3" / "variant_set_b" / ("libreoffice" if pipeline == "LibreOffice" else "google") / "VARIANT_OBSERVATIONS.json") if pipeline == "LibreOffice" else rel(ROOT / "v3" / "variant_set_b" / "google" / "CONVERSION_REPORT.json"),
                "note": note,
                "observed_summary": {"tagged": observed.get("tagged"), "pages": observed.get("pdf", {}).get("pages"), "headings": len(observed.get("headings", [])), "figures": len(observed.get("figures", [])), "lists": len(observed.get("lists", [])), "tables": len(observed.get("tables", [])), "links": len(observed.get("hyperlinks", [])), "footnotes": len(observed.get("footnotes", [])), "equations": len(observed.get("equations", [])), "captions": len(observed.get("captions", [])), "inline_languages": len(observed.get("inline_languages", []))},
            })

    all_rows = core_rows + variant_rows
    payload = {
        "result_model": "V3_ATOMIC_BENCHMARK",
        "scope": "26 controlled fixtures (13 Core + 13 Variant B) x 2 named pipelines",
        "record_count": len(all_rows),
        "core_denominator": 26,
        "variant_b_denominator": 26,
        "classification_spec": rel(ROOT / "contracts" / "v3" / "CLASSIFICATION_DECISION_SPEC.md"),
        "frozen_core_source": rel(V2),
        "records": all_rows,
        "counts": dict(Counter(row["final_evidence_aware_result"] for row in all_rows)),
        "pipeline_counts": {pipeline: dict(Counter(row["final_evidence_aware_result"] for row in all_rows if row["pipeline"] == pipeline)) for pipeline in ("LibreOffice", "Google Docs")},
        "boundary": ["Controlled probes, not a representative sample or prevalence estimate.", "Variant B rows are secondary robustness observations and do not rewrite Core V2 rows.", "Unresolved equivalence is a conservative abstention, not a loss finding."],
    }
    (ROOT / "results" / "V3_PRIMARY_RESULTS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    variant_payload = {"result_model": "V3_VARIANT_SET_B", "variant_count": 13, "case_count": 26, "records": variant_rows, "counts": dict(Counter(row["final_evidence_aware_result"] for row in variant_rows))}
    (VARIANT_BASE / "V3_VARIANT_SET_B_FINAL_RESULTS.json").write_text(json.dumps(variant_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    feature_order = ["headings", "alt_text", "lists", "table", "document_language", "inline_language", "decorative_image", "links", "document_title", "complex_table", "footnotes", "equation", "captions"]
    labels = {"headings": "Headings", "alt_text": "Alt text", "lists": "Lists", "table": "Table", "document_language": "Document language", "inline_language": "Inline language", "decorative_image": "Decorative image", "links": "Links", "document_title": "Document title", "complex_table": "Complex table", "footnotes": "Footnotes", "equation": "Equation", "captions": "Captions"}
    lines = ["# V3 Variant Set B final results", "", "This is a secondary 13-fixture x 2-pipeline robustness arm. It is not merged with the frozen Core denominator.", "", "| Variant | Feature | LibreOffice | Google Docs |", "|---|---|---|---|"]
    for feature in feature_order:
        row = next(r for r in variant_rows if r["feature_family"] == feature and r["pipeline"] == "LibreOffice")
        rowg = next(r for r in variant_rows if r["feature_family"] == feature and r["pipeline"] == "Google Docs")
        lines.append(f"| {row['fixture']} | {labels[feature]} | {row['final_evidence_aware_result']} | {rowg['final_evidence_aware_result']} |")
    lines += ["", "## Interpretation", "", "The decisions use the frozen V3 precedence and treat unresolved cross-format equivalence conservatively. They are not prevalence estimates, converter rankings, or evidence of disabled-user impact. B06 and B11 Google are the only Variant B rows classified as confirmed loss, based on the dedicated two-path serialized-structure audit.", ""]
    (VARIANT_BASE / "V3_VARIANT_SET_B_FINAL_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")

    consistency = {
        "headings": "EXACTLY CONSISTENT: both LibreOffice rows are preserved; both Google rows are partial.",
        "alt_text": "EXACTLY CONSISTENT: LibreOffice alters the author value; Google preserves it.",
        "lists": "UNRESOLVED: Core and Variant B Google are unresolved; the Variant B LibreOffice extraction does not establish full text/type equivalence.",
        "table": "UNRESOLVED: Variant B destination structure is observed in both pipelines, but full source-cell equivalence is not established.",
        "document_language": "EXACTLY CONSISTENT: LibreOffice preserves the tested value; Google reduces specificity.",
        "inline_language": "EXACTLY CONSISTENT: LibreOffice preserves the tested inline languages; Google loses the required inline representations.",
        "decorative_image": "FIXTURE-SENSITIVE: both Google rows retain the tested decorative state, while the Core Google row is partial and the Variant B LibreOffice row alters it.",
        "links": "EXACTLY CONSISTENT AT EVIDENCE LEVEL: all Core and Variant B rows remain unresolved because visible-text association is not established.",
        "document_title": "EXACTLY CONSISTENT: LibreOffice preserves the tested metadata contract; Google alters/reduces it.",
        "complex_table": "UNRESOLVED: both Variant B rows remain unresolved on multi-level association equivalence; Core Google is also unresolved.",
        "footnotes": "PIPELINE-CONSISTENT BUT LO-UNCERTAIN: Google Core and Variant B are confirmed lost; LibreOffice Core is measurement error and Variant B is unresolved.",
        "equation": "UNRESOLVED: the Core and Variant B Google rows remain unresolved; Variant B LibreOffice formula structure is observed without expression equivalence.",
        "captions": "FIXTURE-SENSITIVE AT EVIDENCE LEVEL: Variant B LibreOffice preserves Caption structure while Variant B Google remains unresolved on association.",
    }
    c_lines = ["# V3 within-feature consistency", "", "Comparisons are feature-family observations across Core and Variant B. The two arms have separate denominators; this table does not estimate prevalence.", "", "| Feature | Interpretation |", "|---|---|"]
    for feature in feature_order:
        c_lines.append(f"| {labels[feature]} | {consistency[feature]} |")
    c_lines += ["", "Unresolved means the available destination evidence did not establish equivalence or non-equivalence under the feature-specific contract. It is not treated as degradation.", ""]
    (ROOT / "results" / "V3_WITHIN_FEATURE_CONSISTENCY.md").write_text("\n".join(c_lines), encoding="utf-8")
    print(json.dumps({"atomic_cases": len(all_rows), "variant_cases": len(variant_rows), "counts": payload["counts"]}, indent=2))


if __name__ == "__main__":
    main()
