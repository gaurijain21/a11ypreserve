"""Audit tracked text artifacts for private paths, secrets, and generated state."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    "", ".bib", ".cff", ".csv", ".gitignore", ".json", ".md", ".py", ".ps1",
    ".tex", ".toml", ".txt", ".vbs", ".yaml", ".yml",
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / item for item in output.decode("utf-8").split("\0") if item]


def patterns() -> list[tuple[str, re.Pattern[str]]]:
    slash = re.escape("/")
    backslash = re.escape(chr(92))
    users = "Users"
    home = "home"
    drive = r"(?<![A-Za-z0-9])[A-Za-z]" + ":" + "[" + backslash + "/]"
    return [
        ("windows absolute path", re.compile(r"(?i)" + drive)),
        ("UNC path", re.compile(r"(?i)(?<![A-Za-z0-9>])" + re.escape(chr(92) * 2) + r"[A-Za-z0-9._-]+" + re.escape(chr(92)))),
        # Do not treat public URLs such as `https://example.org/home/...` as
        # local Unix paths; require the slash not to be part of a host/path.
        ("unix user path", re.compile(r"(?i)(?<![A-Za-z0-9:])" + slash + users + slash + r"|(?<![A-Za-z0-9:])" + slash + home + slash)),
        ("private cloud path", re.compile(r"(?i)d[.]docs[.]live[.]net")),
        ("private key", re.compile(r"-----BEGIN(?: [A-Z]+)? PRIVATE KEY-----")),
        ("GitHub token", re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]+")),
        ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{20,}")),
        ("OpenAI-style key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ]


def main() -> None:
    findings: list[dict[str, str]] = []
    for path in tracked_files():
        if path.suffix.lower() not in TEXT_SUFFIXES or not path.is_file():
            continue
        raw = path.read_bytes()
        if b"\0" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns():
            match = pattern.search(text)
            if match:
                findings.append({"file": str(path.relative_to(ROOT)).replace("\\", "/"), "kind": label, "line": str(text.count("\n", 0, match.start()) + 1)})
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    required_ignores = ["submission/**/upload_v5/", "submission/**/upload/", "**/.codex/", "**/profiles/"]
    missing_ignores = [item for item in required_ignores if item not in ignore]
    result = {"status": "PASS" if not findings and not missing_ignores else "FAIL", "tracked_text_files_checked": sum(1 for path in tracked_files() if path.suffix.lower() in TEXT_SUFFIXES), "findings": findings, "missing_required_ignores": missing_ignores}
    report = ROOT / "reports" / "REPOSITORY_SAFETY_AUDIT.json"
    report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
