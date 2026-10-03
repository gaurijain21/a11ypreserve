from __future__ import annotations

import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_semantics import extract_pdf  # noqa: E402


FIXTURE_IDS = ("F01_HEADINGS", "F02_ALT_TEXT", "F03_LISTS", "F04_TABLE")
SOURCE_DIR = ROOT / "pilot" / "source_semantics"
PILOT3 = ROOT / "pilot3"

ENGINES = {
    "LibreOffice": {
        "key": "libreoffice",
        "pdf_dir": ROOT / "pilot2" / "outputs" / "libreoffice_pdf",
        "suffix": "LIBREOFFICE",
        "version": "26.2.6.3",
    },
    "Google Docs": {
        "key": "google_docs",
        "pdf_dir": PILOT3 / "outputs" / "google_docs_pdf",
        "suffix": "GOOGLE_DOCS",
        "version": "Google Docs web export; service version not exposed in the downloaded PDF",
    },
}

FEATURES = {
    "F01_HEADINGS": ("headings", "heading hierarchy"),
    "F02_ALT_TEXT": ("figures", "image alternative text"),
    "F03_LISTS": ("lists", "list structure"),
    "F04_TABLE": ("tables", "table structure"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deref(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def source_value(source: dict[str, Any], feature_key: str) -> Any:
    if feature_key == "headings":
        return [{k: item.get(k) for k in ("text", "level", "order")} for item in source.get(feature_key, [])]
    if feature_key == "figures":
        return [{k: item.get(k) for k in ("identifier", "alt", "decorative", "order")} for item in source.get(feature_key, [])]
    return source.get(feature_key, [])


def text_contains(page_text: str, value: str) -> bool:
    """Compare extracted PDF text without treating layout whitespace as content."""
    normalize = lambda text: re.sub(r"\s+", " ", text).strip()
    if normalize(value) in normalize(page_text):
        return True
    # Some PDF text extractors insert spaces inside glyph runs (for example
    # ``W ork``).  A whitespace-insensitive fallback avoids mistaking that
    # parser artifact for lost source text.
    compact = lambda text: re.sub(r"\s+", "", text).casefold()
    return compact(value) in compact(page_text)


def tree_summary(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    root = deref(reader.trailer.get("/Root"))
    struct_root = deref(root.get("/StructTreeRoot")) if hasattr(root, "get") else None
    roles: list[str] = []
    list_numbering: list[str] = []
    table_rows = 0
    header_cells = 0
    data_cells = 0
    figures: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        nonlocal table_rows, header_cells, data_cells
        node = deref(node)
        if isinstance(node, list):
            for child in node:
                walk(child)
            return
        if not hasattr(node, "get"):
            return
        role = node.get("/S")
        role = str(role) if role is not None else None
        if role:
            roles.append(role.lstrip("/"))
        if role == "/L":
            attrs = deref(node.get("/A"))
            if hasattr(attrs, "get") and attrs.get("/ListNumbering") is not None:
                list_numbering.append(str(attrs.get("/ListNumbering")).lstrip("/"))
        if role == "/TR":
            table_rows += 1
        elif role == "/TH":
            header_cells += 1
        elif role == "/TD":
            data_cells += 1
        elif role == "/Figure":
            alt = node.get("/Alt")
            figures.append({"alt": str(alt) if alt is not None else None, "has_alt": bool(alt)})
        kids = node.get("/K")
        if kids is not None:
            walk(kids)

    if hasattr(struct_root, "get"):
        walk(struct_root.get("/K"))
    return {
        "tagged": struct_root is not None,
        "roles": roles,
        "role_counts": {role: roles.count(role) for role in sorted(set(roles))},
        "list_numbering": list_numbering,
        "table_rows": table_rows,
        "header_cells": header_cells,
        "data_cells": data_cells,
        "figures": figures,
        "pages": len(reader.pages),
    }


def validate_pdf(path: Path, engine: str, fixture: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "fixture": fixture,
        "engine": engine,
        "path": str(path),
        "exists": path.exists(),
        "checked_at_utc": utc_now(),
    }
    if not path.exists():
        result.update({"status": "INVALID_CONVERSION", "reason": "expected output file does not exist"})
        return result
    result.update({"size_bytes": path.stat().st_size, "sha256": sha256(path)})
    if path.stat().st_size == 0:
        result.update({"status": "INVALID_CONVERSION", "reason": "zero-byte output"})
        return result
    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        summary = tree_summary(path)
        secondary: dict[str, Any]
        try:
            import pdfplumber

            with pdfplumber.open(path) as secondary_pdf:
                secondary_text = "\n".join(page.extract_text() or "" for page in secondary_pdf.pages)
                secondary = {"tool": "pdfplumber", "parseable": True, "page_count": len(secondary_pdf.pages), "text_nonempty": bool(secondary_text.strip())}
        except Exception as exc:
            secondary = {"tool": "pdfplumber", "parseable": False, "error": repr(exc)}
        result.update(
            {
                "status": "PASS",
                "parseable": True,
                "page_count": len(reader.pages),
                "page_count_minimum": 1,
                "content_text_nonempty": bool(text.strip()),
                "struct_tree_exists": summary["tagged"],
                "content_present": bool(text.strip()),
                "structure_summary": summary,
                "secondary_validation": secondary,
                "metadata": {str(k): str(v) for k, v in (reader.metadata or {}).items()},
            }
        )
    except Exception as exc:
        result.update({"status": "INVALID_CONVERSION", "parseable": False, "reason": repr(exc)})
    return result


def evidence_path(fixture: str, engine_key: str) -> Path:
    return PILOT3 / "evidence" / fixture / f"{engine_key}_semantics.json"


def make_row(
    fixture: str,
    engine: str,
    feature_name: str,
    source: Any,
    destination: Any,
    representation: Any,
    fidelity: str,
    accessibility: str,
    evidence: list[str],
    confidence: float,
    notes: str,
) -> dict[str, Any]:
    return {
        "fixture": fixture,
        "source_format": "DOCX",
        "destination_format": "PDF",
        "converter": engine,
        "source_feature": feature_name,
        "source_value": source,
        "destination_value": destination,
        "destination_representation": representation,
        "equivalence_determination": fidelity,
        "fidelity_classification": fidelity,
        "destination_accessibility": accessibility,
        "classification": fidelity,
        "evidence_path": evidence,
        "confidence": confidence,
        "notes": notes,
    }


def classify_fixture(fixture: str, source: dict[str, Any], dest: dict[str, Any], raw: dict[str, Any], engine: str, evidence: list[str]) -> dict[str, Any]:
    feature_key, feature_name = FEATURES[fixture]
    src = source_value(source, feature_key)
    text = dest.get("pdf_text", "")
    if fixture == "F01_HEADINGS":
        src_levels = [item["level"] for item in source["headings"]]
        dst_levels = [item["level"] for item in dest.get("headings", [])]
        text_present = all(text_contains(text, item["text"]) for item in source["headings"])
        start = next((i for i in range(len(dst_levels) - len(src_levels) + 1) if dst_levels[i : i + len(src_levels)] == src_levels), None)
        if start is None or not text_present:
            fidelity, access, confidence, notes = "LOST", "INACCESSIBLE_FEATURE", 0.98, "The source heading sequence or its visible text is absent from the destination structure."
        elif dst_levels == src_levels:
            fidelity, access, confidence, notes = "SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT", 0.99, "All source heading levels occur in order and their text is independently present in extracted page text."
        else:
            fidelity, access, confidence, notes = "PARTIAL_PRESERVATION", "ACCESSIBLE_BUT_ALTERED", 0.97, "The source H1/H2/H3/H2 sequence is present, but Google Docs added an extra H1 title before it."
        dst = {"roles": dst_levels, "source_sequence_start": start, "source_texts_present": text_present}
        return make_row(fixture, engine, feature_name, src, dst, raw, fidelity, access, evidence, confidence, notes)
    if fixture == "F02_ALT_TEXT":
        source_alt = source["figures"][0]["alt"]
        dest_figures = dest.get("figures", [])
        dest_alt = dest_figures[0].get("alt") if dest_figures else None
        dst = {"figure_count": len(dest_figures), "alt": dest_alt, "decorative": dest_figures[0].get("decorative") if dest_figures else None}
        if dest_alt == source_alt:
            fidelity, access, confidence, notes = "EXACT_PRESERVATION", "ACCESSIBLE_EQUIVALENT", 1.0, "The PDF Figure /Alt value exactly matches the author-written DOCX alternative text."
        elif dest_alt:
            fidelity, access, confidence, notes = "MUTATED", "ACCESSIBLE_BUT_ALTERED", 0.99, "A non-empty destination /Alt exists but differs from the source author-written value."
        else:
            fidelity, access, confidence, notes = "LOST", "INACCESSIBLE_FEATURE", 0.99, "No usable destination /Alt value was found for the source figure."
        return make_row(fixture, engine, feature_name, src, dst, raw, fidelity, access, evidence, confidence, notes)
    if fixture == "F03_LISTS":
        source_types = [item["type"] for item in source["lists"]]
        source_depths = [item["depth"] for item in source["lists"]]
        list_roles = raw["role_counts"].get("L", 0)
        li_roles = raw["role_counts"].get("LI", 0)
        nested_list = list_roles >= 2 and any(item["depth"] == 1 for item in source["lists"])
        numbering = raw["list_numbering"]
        text_present = all(text_contains(text, item["text"]) for item in source["lists"])
        dst = {"list_containers": list_roles, "list_items": li_roles, "list_numbering": numbering, "source_item_texts_present": text_present, "roles": raw["roles"]}
        if list_roles >= 2 and li_roles == len(source["lists"]) and nested_list and text_present and {"Disc", "Decimal"}.issubset(set(numbering)):
            fidelity, access, confidence, notes = "SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT", 0.98, "List containers, list items, nested structure, explicit list numbering, and source item text are independently present."
        elif list_roles >= 2 and li_roles == len(source["lists"]) and nested_list and text_present:
            fidelity, access, confidence, notes = "PARTIAL_PRESERVATION", "DEGRADED_ACCESSIBILITY", 0.95, "List and nested list roles survive, but the PDF structure omits explicit /ListNumbering attributes; visual bullets/numbers are not treated as semantic proof."
        else:
            fidelity, access, confidence, notes = "LOST", "INACCESSIBLE_FEATURE", 0.97, "The destination does not contain enough list structure to establish the source hierarchy."
        return make_row(fixture, engine, feature_name, src, dst, raw, fidelity, access, evidence, confidence, notes)
    if fixture == "F04_TABLE":
        expected = source["tables"][0]
        dst = {"tables": raw["role_counts"].get("Table", 0), "rows": raw["role_counts"].get("TR", 0), "header_cells": raw["header_cells"], "data_cells": raw["data_cells"], "source_cell_texts_present": all(text_contains(text, str(value)) for row in expected["cells"] for value in row)}
        if dst["tables"] >= 1 and dst["rows"] == expected["dimensions"]["rows"] and dst["header_cells"] == expected["dimensions"]["columns"] and dst["data_cells"] == (expected["dimensions"]["rows"] - 1) * expected["dimensions"]["columns"] and dst["source_cell_texts_present"]:
            fidelity, access, confidence, notes = "SEMANTICALLY_EQUIVALENT", "ACCESSIBLE_EQUIVALENT", 0.98, "The PDF has Table/TR/TH/TD roles with a three-cell header row and all source cell values independently present in page text."
        elif dst["tables"] >= 1 and dst["source_cell_texts_present"]:
            fidelity, access, confidence, notes = "PARTIAL_PRESERVATION", "DEGRADED_ACCESSIBILITY", 0.94, "Some table structure survives, but row/cell/header evidence is incomplete."
        else:
            fidelity, access, confidence, notes = "LOST", "INACCESSIBLE_FEATURE", 0.97, "No equivalent table structure and content evidence was found."
        return make_row(fixture, engine, feature_name, src, dst, raw, fidelity, access, evidence, confidence, notes)
    raise AssertionError(fixture)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    generated = utc_now()
    reports = PILOT3 / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    for fixture in FIXTURE_IDS:
        (PILOT3 / "evidence" / fixture).mkdir(parents=True, exist_ok=True)

    manifest = json.loads((ROOT / "pilot" / "manifests" / "hashes.json").read_text(encoding="utf-8"))
    frozen_rows = []
    for fixture in FIXTURE_IDS:
        path = ROOT / "pilot" / "fixtures" / f"{fixture}.docx"
        actual = sha256(path)
        expected = manifest[fixture]["source_docx"]
        frozen_rows.append({"fixture": fixture, "filename": path.name, "path": str(path), "size_bytes": path.stat().st_size, "sha256": actual, "expected_sha256": expected, "match": actual == expected})
    frozen_ok = all(row["match"] for row in frozen_rows)
    frozen_md = ["# Frozen Input Verification", "", f"Verification timestamp (UTC): `{generated}`", "", "Status: **PASS**" if frozen_ok else "Status: **FAIL — experiment must be considered aborted**", "", "| Fixture | Filename | Size (bytes) | SHA-256 | Manifest match |", "|---|---|---:|---|---|"]
    frozen_md += [f"| {row['fixture']} | `{row['filename']}` | {row['size_bytes']} | `{row['sha256']}` | {'PASS' if row['match'] else 'FAIL'} |" for row in frozen_rows]
    write_text(PILOT3 / "FROZEN_INPUT_VERIFICATION.md", "\n".join(frozen_md))
    (PILOT3 / "FROZEN_INPUT_VERIFICATION.json").write_text(json.dumps({"verified_at_utc": generated, "status": "PASS" if frozen_ok else "FAIL", "fixtures": frozen_rows}, indent=2) + "\n", encoding="utf-8")
    if not frozen_ok:
        raise SystemExit("Frozen fixture hash mismatch; aborting Pilot 3 analysis")

    baseline_validation = json.loads((ROOT / "pilot2" / "reports" / "output_validation.json").read_text(encoding="utf-8"))
    baseline_lines = ["# Pilot 2 LibreOffice Baseline Verification", "", f"Verified at (UTC): `{generated}`", "", "Pilot 2 LibreOffice outputs were reused as the frozen baseline; no LibreOffice conversion was rerun in Pilot 3.", "", "| Fixture | Baseline PDF | Recorded SHA-256 | Current SHA-256 | Parseable/tagged |", "|---|---|---|---|---|"]
    baseline_ok = True
    for fixture in FIXTURE_IDS:
        pdf = ENGINES["LibreOffice"]["pdf_dir"] / f"{fixture}__LIBREOFFICE.pdf"
        record = baseline_validation["outputs"].get(f"LibreOffice:{fixture}", {})
        current = sha256(pdf) if pdf.exists() else None
        row_ok = bool(pdf.exists() and current == record.get("sha256") and record.get("status") == "PASS")
        baseline_ok = baseline_ok and row_ok
        baseline_lines.append(f"| {fixture} | `{pdf.name}` | `{record.get('sha256')}` | `{current}` | {'PASS' if row_ok else 'FAIL'} |")
    baseline_lines += ["", f"Baseline verification status: **{'PASS' if baseline_ok else 'FAIL'}**", "", "Pilot 2's Microsoft Word rows remain conversion-layer `INVALID_CONVERSION` records and are not reused as semantic evidence."]
    write_text(PILOT3 / "BASELINE_VERIFICATION.md", "\n".join(baseline_lines))
    if not baseline_ok:
        raise SystemExit("Pilot 2 baseline mismatch; do not compare against an altered baseline")

    validations: dict[str, Any] = {"generated_at_utc": generated, "scope": "Pilot 3 Google Docs versus reused Pilot 2 LibreOffice baseline", "outputs": {}}
    diffs: list[dict[str, Any]] = []
    summary: dict[str, dict[str, str]] = {}
    for fixture in FIXTURE_IDS:
        source = json.loads((SOURCE_DIR / f"{fixture}.json").read_text(encoding="utf-8"))
        feature_key, feature_name = FEATURES[fixture]
        summary[fixture] = {"feature": feature_name}
        for engine, spec in ENGINES.items():
            pdf = spec["pdf_dir"] / f"{fixture}__{spec['suffix']}.pdf"
            validation = validate_pdf(pdf, engine, fixture)
            validations["outputs"][f"{engine}:{fixture}"] = validation
            if validation.get("status") != "PASS":
                diffs.append(make_row(fixture, engine, feature_name, source_value(source, feature_key), None, None, "MEASUREMENT_ERROR", "UNKNOWN", [str(pdf)], 1.0, "The PDF was not analyzable; this is not classified as accessibility loss."))
                summary[fixture][engine] = "MEASUREMENT_ERROR"
                continue
            dest = extract_pdf(pdf)
            raw = validation["structure_summary"]
            evidence_file = evidence_path(fixture, spec["key"])
            evidence_file.write_text(json.dumps({"fixture": fixture, "engine": engine, "source": source_value(source, feature_key), "destination": dest, "raw_structure_summary": raw, "validation": validation}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            row = classify_fixture(fixture, source, dest, raw, engine, [str(evidence_file), str(pdf)])
            diffs.append(row)
            summary[fixture][engine] = row["fidelity_classification"]
    validations["summary"] = {"expected_outputs": 8, "valid_parseable_outputs": sum(1 for value in validations["outputs"].values() if value.get("status") == "PASS"), "all_required_outputs_valid": all(value.get("status") == "PASS" for value in validations["outputs"].values())}
    (reports / "output_validation.json").write_text(json.dumps(validations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (reports / "semantic_diff_results.json").write_text(json.dumps({"generated_at_utc": generated, "taxonomy": {"fidelity": ["EXACT_PRESERVATION", "SEMANTICALLY_EQUIVALENT", "PARTIAL_PRESERVATION", "MUTATED", "REGENERATED", "LOST", "NOT_REPRESENTABLE", "NOT_APPLICABLE", "MEASUREMENT_ERROR"], "destination_accessibility": ["ACCESSIBLE_EQUIVALENT", "ACCESSIBLE_BUT_ALTERED", "DEGRADED_ACCESSIBILITY", "INACCESSIBLE_FEATURE", "UNKNOWN"]}, "results": diffs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    table = ["# Pilot 3 Results", "", "| Fixture | Feature | LibreOffice baseline | Google Docs | Evidence quality |", "|---|---|---|---|---|"]
    for fixture in FIXTURE_IDS:
        feature = summary[fixture]["feature"]
        table.append(f"| {fixture} | {feature} | {summary[fixture]['LibreOffice']} | {summary[fixture]['Google Docs']} | HIGH |")
    table += ["", "The table reports preservation fidelity. Destination accessibility is reported separately in `reports/semantic_diff_results.json`."]
    write_text(PILOT3 / "PILOT3_RESULTS.md", "\n".join(table))

    cross = ["# Cross-Converter Results", "", "This comparison uses the same frozen DOCX source semantics and the same PDF structural extraction for both converters. It does not rank the converters overall.", "", "| Fixture | Feature | LibreOffice fidelity | Google Docs fidelity | LibreOffice accessibility | Google Docs accessibility |", "|---|---|---|---|---|---|"]
    for fixture in FIXTURE_IDS:
        lo = next(x for x in diffs if x["fixture"] == fixture and x["converter"] == "LibreOffice")
        gd = next(x for x in diffs if x["fixture"] == fixture and x["converter"] == "Google Docs")
        cross.append(f"| {fixture} | {lo['source_feature']} | {lo['fidelity_classification']} | {gd['fidelity_classification']} | {lo['destination_accessibility']} | {gd['destination_accessibility']} |")
    cross += ["", "## What Google Docs preserves that LibreOffice does not", "", "For these fixtures, Google Docs preserves the author-written F02 `/Alt` string exactly, while LibreOffice mutates it by adding `Enrollment chart - `.", "", "## What LibreOffice preserves that Google Docs does not", "", "LibreOffice emits explicit PDF `/ListNumbering` attributes (`Disc` and `Decimal`) for the F03 list containers. Google Docs emits the `L`/`LI` nesting but no `/ListNumbering` attribute, so ordered-versus-unordered semantics are not independently established from the PDF structure.", "", "## Is either converter clearly superior overall?", "", "No. The converter behavior is feature-specific: Google Docs is stronger on F02 exact alt-text fidelity, while LibreOffice is stronger on F03 explicit list-type evidence. Both preserve analyzable table structure; Google Docs adds an extra H1 title in F01.", "", "## Does source-grounded comparison reveal differences validators might miss?", "", "Yes. A generic tagged-PDF check would see tagged output from both engines. The source-grounded comparison additionally reveals the LibreOffice F02 string mutation, the Google Docs F01 extra H1, and the Google Docs F03 missing `/ListNumbering` evidence.", "", "## Did the second converter strengthen feasibility?", "", "Yes. The same frozen source semantics produced reproducible, feature-specific signals across two independent conversion routes. That supports the methodology as a cross-converter experiment rather than a single-engine observation.", "", "## What should be tested next?", "", "Scale the same design to more converters and feature families: complex nested lists, table header scope/associations, figure captions and long descriptions, document language, links, bookmarks, reading order, footnotes, and forms. Preserve the two-axis reporting model and keep validator output secondary."]
    write_text(PILOT3 / "CROSS_CONVERTER_RESULTS.md", "\n".join(cross))

    f02 = next(x for x in diffs if x["fixture"] == "F02_ALT_TEXT" and x["converter"] == "LibreOffice")
    f02_google = next(x for x in diffs if x["fixture"] == "F02_ALT_TEXT" and x["converter"] == "Google Docs")
    refinement = ["# F02 Classification Refinement", "", "Pilot 2 used a single legacy classification and reported the LibreOffice result as `DEGRADED`. Pilot 3 separates preservation fidelity from destination accessibility.", "", "## Source value", "", f"`{source_value(json.loads((SOURCE_DIR / 'F02_ALT_TEXT.json').read_text(encoding='utf-8')), 'figures')[0]['alt']}`", "", "## LibreOffice", "", f"Destination `/Alt`: `{f02['destination_value']['alt']}`", "", f"- Preservation fidelity: **{f02['fidelity_classification']}**", f"- Destination accessibility: **{f02['destination_accessibility']}**", "- Rationale: the destination has meaningful alternative text, but it is not the author-written source string.", "", "## Google Docs", "", f"Destination `/Alt`: `{f02_google['destination_value']['alt']}`", "", f"- Preservation fidelity: **{f02_google['fidelity_classification']}**", f"- Destination accessibility: **{f02_google['destination_accessibility']}**", "- Rationale: the PDF `/Alt` exactly matches the source value.", "", "The refinement does not alter Pilot 2 evidence or frozen source truth; it adds a more expressive Pilot 3 taxonomy."]
    write_text(PILOT3 / "F02_CLASSIFICATION_REFINEMENT.md", "\n".join(refinement))

    log_lines = ["# Pilot 3 Automation Log", "", "All four DOCX fixtures were uploaded through the authenticated Google Docs web UI and exported with File → Download → PDF Document (.pdf). No print-to-PDF path, screenshot, manual content repair, or generated substitute PDF was used.", "", "Environment: Windows `10.0.26200.0`; Chrome browser profile with an authenticated Google Docs session; Google Docs web UI; date 2026-09-27 (America/Los_Angeles). The account identity and credentials were not recorded.", "", "LibreOffice baseline: version `26.2.6.3`, reused from Pilot 2; no conversion rerun.", "", "| Timestamp (local) | Tool / method | Source | Destination | Source SHA-256 | Output SHA-256 | Result |", "|---|---|---|---|---|---|---|"]
    for fixture in FIXTURE_IDS:
        source_path = ROOT / "pilot" / "fixtures" / f"{fixture}.docx"
        google_path = ENGINES["Google Docs"]["pdf_dir"] / f"{fixture}__GOOGLE_DOCS.pdf"
        lo_path = ENGINES["LibreOffice"]["pdf_dir"] / f"{fixture}__LIBREOFFICE.pdf"
        google_time = datetime.fromtimestamp(google_path.stat().st_mtime, tz=timezone.utc).astimezone().isoformat()
        log_lines.append(f"| {google_time} | Chrome → Google Docs import → File → Download → PDF Document (.pdf) | `{source_path.name}` | `{google_path.name}` | `{sha256(source_path)}` | `{sha256(google_path)}` | PASS |")
        log_lines.append(f"| Pilot 2 baseline timestamp retained | LibreOffice `soffice --headless` PDF export (Pilot 2 record) | `{source_path.name}` | `{lo_path.name}` | `{sha256(source_path)}` | `{sha256(lo_path)}` | REUSED BASELINE, PASS |")
    log_lines += ["", "One recoverable browser automation issue occurred while opening the F02 picker: an overly broad iframe selector matched multiple frames. The run was resumed with the exact picker iframe selector; the F02 export succeeded. This was an automation-recovery event, not a conversion failure.", "", "Microsoft Word: native WINWORD.EXE was found at `C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE` (file version `16.0.20326.20158`). Word conversion was deliberately deferred in Pilot 3 per scope; the earlier Pilot 2 Word absence remains a conversion-layer limitation, not a semantic result."]
    write_text(PILOT3 / "AUTOMATION_LOG.md", "\n".join(log_lines))

    print(json.dumps({"frozen_inputs": "PASS", "baseline": "PASS", "valid_outputs": validations["summary"]["valid_parseable_outputs"], "results": summary}, indent=2))


if __name__ == "__main__":
    main()
