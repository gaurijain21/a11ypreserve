from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pilot_semantics import extract_docx  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    pilot = ROOT / "pilot"
    fixtures = pilot / "fixtures"
    manifests = pilot / "manifests"
    output_dir = pilot / "source_semantics"
    output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    report: dict[str, object] = {}
    for source in sorted(fixtures.glob("F*.docx")):
        fixture_id = source.stem
        manifest = json.loads((manifests / f"{fixture_id}.json").read_text(encoding="utf-8"))
        asir = extract_docx(source)
        (output_dir / f"{fixture_id}.json").write_text(json.dumps(asir, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if asir["document"]["title"] != manifest["document"]["title"]:
            errors.append(f"{fixture_id}: title mismatch")
        if asir["document"]["language"] != manifest["document"]["language"]:
            errors.append(f"{fixture_id}: language mismatch")
        if fixture_id == "F01_HEADINGS":
            observed = [{"text": x["text"], "level": x["level"]} for x in asir["headings"]]
            if observed != manifest["headings"]:
                errors.append(f"{fixture_id}: headings mismatch: {observed}")
        if fixture_id == "F02_ALT_TEXT":
            observed = [{k: x[k] for k in ("identifier", "alt", "decorative", "order")} for x in asir["figures"]]
            if observed != manifest["figures"]:
                errors.append(f"{fixture_id}: figure mismatch: {observed}")
        if fixture_id == "F03_LISTS":
            observed = [{k: x[k] for k in ("type", "depth", "text", "parent")} for x in asir["lists"]]
            expected = manifest["lists"]
            if observed != expected:
                errors.append(f"{fixture_id}: list mismatch: {observed}")
        if fixture_id == "F04_TABLE":
            table = asir["tables"][0]
            expected = manifest["table"]
            if table["dimensions"] != expected["dimensions"] or table["cells"] != expected["cells"] or table["headers"] != expected["headers"] or table["header_row"] != expected["header_row"]:
                errors.append(f"{fixture_id}: table mismatch: {table}")
        report[fixture_id] = {"source_sha256": sha256(source), "manifest_sha256": sha256(manifests / f"{fixture_id}.json"), "verified": not any(fixture_id in e for e in errors)}
    (pilot / "reports" / "source_verification.json").write_text(json.dumps({"verified": not errors, "errors": errors, "fixtures": report}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verified": not errors, "errors": errors, "fixtures": report}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
