"""Temporary mutation tests for the separately implemented OOXML oracle.

The frozen DOCX files are copied into a temporary directory and mutated in
memory before inspection.  No corpus source, manifest, or result file is
modified.
"""

from __future__ import annotations

import importlib.util
import re
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE_PATH = ROOT / "artifact_v3" / "src" / "independent_source_oracle.py"
spec = importlib.util.spec_from_file_location("independent_source_oracle", ORACLE_PATH)
assert spec and spec.loader
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)
FIXTURES = ROOT / "artifact_v3" / "corpus" / "fixtures"


def mutate(source: Path, target: Path, edits: dict[str, callable], omit: set[str] | None = None) -> None:
    omit = omit or set()
    with zipfile.ZipFile(source) as archive, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as output:
        for name in archive.namelist():
            if name in omit:
                continue
            value = archive.read(name)
            if name in edits:
                value = edits[name](value)
            output.writestr(name, value)


def replace_first(pattern: bytes, replacement: bytes):
    def edit(value: bytes) -> bytes:
        changed, count = re.subn(pattern, replacement, value, count=1)
        assert count == 1, pattern
        return changed

    return edit


def main() -> None:
    cases = {
        "headings": ("F01_HEADINGS.docx", {"word/document.xml": replace_first(rb'w:val="Heading1"', rb'w:val="Normal"')}, set()),
        "alt_text": ("F02_ALT_TEXT.docx", {"word/document.xml": replace_first(rb' descr="[^"]*"', rb' descr=""')}, set()),
        "document_language": ("F05_DOCUMENT_LANGUAGE.docx", {"word/styles.xml": lambda value: re.sub(rb'<w:lang\b[^>]*/>', b'', value)}, set()),
        "table_headers": ("F04_TABLE.docx", {"word/document.xml": lambda value: re.sub(rb'<w:tblHeader\b[^>]*/>', b'', value)}, set()),
        "hyperlink_target": ("F08_LINKS.docx", {"word/_rels/document.xml.rels": replace_first(rb'(relationships/hyperlink" Target=")[^"]+"', rb'\1https://corrupt.invalid/"')}, set()),
        "footnote_part": ("F11_FOOTNOTES.docx", {}, {"word/footnotes.xml"}),
    }
    results = {}
    with tempfile.TemporaryDirectory(prefix="a11ypreserve-oracle-") as directory:
        temp_root = Path(directory)
        for name, (filename, edits, omit) in cases.items():
            source = FIXTURES / filename
            original = oracle.inspect_docx(source)
            mutated = temp_root / filename
            mutate(source, mutated, edits, omit)
            observed = oracle.inspect_docx(mutated)
            if name == "headings":
                rejected = len(observed["headings"]) < len(original["headings"])
            elif name == "alt_text":
                rejected = observed["figures"] != original["figures"] and any(not item["alt"] for item in observed["figures"])
            elif name == "document_language":
                rejected = observed["default_language"] != original["default_language"]
            elif name == "table_headers":
                rejected = observed["tables"] != original["tables"] and not observed["tables"][0]["header_rows"]
            elif name == "hyperlink_target":
                rejected = observed["hyperlinks"] != original["hyperlinks"] and any(item["target"] == "https://corrupt.invalid/" for item in observed["hyperlinks"])
            else:
                rejected = observed["has_footnotes_part"] is False and not observed["footnotes"]
            assert rejected, f"oracle failed to observe corruption: {name}"
            results[name] = "PASS"
    print({"checks": results, "status": "PASS"})


if __name__ == "__main__":
    main()
