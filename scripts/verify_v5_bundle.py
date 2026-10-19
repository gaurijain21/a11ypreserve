"""Verify the tracked anonymous V5 upload bundle and its hashes."""
from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "submission" / "ICST2027_V5" / "ICST2027_V5_anonymous_upload.zip"
PAPER = ROOT / "submission" / "ICST2027_V5" / "main.pdf"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def unsafe(text: str) -> str | None:
    checks = [
        ("windows absolute path", re.compile(r"(?i)(?<![A-Za-z0-9])[A-Za-z]:[\\/]{1,4}")),
        ("unix user path", re.compile(r"(?i)/(?:Users|home)/")),
        ("private cloud path", re.compile(r"(?i)d[.]docs[.]live[.]net")),
        ("private key", re.compile(r"-----BEGIN(?: [A-Z]+)? PRIVATE KEY-----")),
        ("GitHub token", re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]+")),
        ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{20,}")),
        ("OpenAI-style key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ]
    for label, pattern in checks:
        if pattern.search(text):
            return label
    return None


def main() -> None:
    if not BUNDLE.exists() or not PAPER.exists():
        raise SystemExit("tracked V5 paper or upload bundle is missing")
    paper_bytes = PAPER.read_bytes()
    with pymupdf.open(stream=paper_bytes, filetype="pdf") as document:
        pages = len(document)
    with zipfile.ZipFile(BUNDLE) as outer:
        names = set(outer.namelist())
        required = {"paper.pdf", "replication_package.zip", "UPLOAD_README.md", "BUNDLE_MANIFEST.json"}
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"bundle missing entries: {missing}")
        manifest = json.loads(outer.read("BUNDLE_MANIFEST.json"))
        bundled_paper = outer.read("paper.pdf")
        bundled_package = outer.read("replication_package.zip")
        if sha256_bytes(bundled_paper) != manifest["paper"]["sha256"]:
            raise SystemExit("bundle paper hash does not match BUNDLE_MANIFEST.json")
        if sha256_bytes(bundled_package) != manifest["replication_package"]["sha256"]:
            raise SystemExit("bundle package hash does not match BUNDLE_MANIFEST.json")
        if bundled_paper != paper_bytes:
            raise SystemExit("bundle paper.pdf differs from tracked main.pdf")
        with zipfile.ZipFile(io.BytesIO(bundled_package)) as package:
            package_names = set(package.namelist())
            if "replication_package/PACKAGE_MANIFEST.json" not in package_names:
                raise SystemExit("replication package manifest is missing")
            text_suffixes = (".md", ".json", ".py", ".ps1", ".tex", ".bib", ".txt", ".csv", ".toml", ".yaml", ".yml", ".cff")
            for name in package_names:
                if not name.endswith(text_suffixes):
                    continue
                issue = unsafe(package.read(name).decode("utf-8", errors="replace"))
                if issue:
                    raise SystemExit(f"{issue} found in bundled text: {name}")
    result = {"status": "PASS", "pages": pages, "bundle_entries": len(names), "replication_package_files": manifest["replication_package"]["files"], "generated_from_commit": manifest.get("generated_from_commit")}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
