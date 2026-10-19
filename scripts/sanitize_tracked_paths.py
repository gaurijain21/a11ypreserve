"""Replace workstation-specific path metadata in tracked text artifacts.

This preserves scientific values and hashes while making historical reports and
machine-generated records portable. It intentionally does not rewrite binary
evidence or source/output bytes.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    "", ".bib", ".cff", ".csv", ".json", ".md", ".py", ".ps1", ".tex",
    ".toml", ".txt", ".vbs", ".yaml", ".yml",
}


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / item for item in output.decode("utf-8").split("\0") if item]


def sanitize(text: str) -> str:
    root = str(ROOT)
    for value in {root, root.replace("\\", "/"), root.replace("\\", "\\\\")}:
        text = text.replace(value, "<REPOSITORY_ROOT>")
    text = text.replace("https://d.docs.live.net/", "<CLOUD_PATH>/")
    text = re.sub(r"(?i)C:\\A11yWordTest", "<LOCAL_WORD_WORKSPACE>", text)
    text = re.sub(r"(?i)C:\\\\A11yWordTest", "<LOCAL_WORD_WORKSPACE>", text)
    text = re.sub(r"(?i)[A-Za-z]:(?:[\\/]{1,4})Users(?:[\\/]{1,4})[^\"'\r\n;,]+", "<LOCAL_WINDOWS_PATH>", text)
    text = re.sub(r"(?i)[A-Za-z]:(?:[\\/]{1,4})Program Files(?: \(x86\))?(?:[\\/]{1,4})[^\"'\r\n;,]+", "<INSTALLED_APPLICATION>", text)
    text = re.sub(r"(?i)[A-Za-z]:[\\/]Program Files(?: \(x86\))?[\\/][^\"'\r\n;,]+", "<INSTALLED_APPLICATION>", text)
    text = re.sub(r"(?i)/Users/[^\"'\r\n;,]+", "<LOCAL_UNIX_PATH>", text)
    text = re.sub(r"(?i)/home/[^\"'\r\n;,]+", "<LOCAL_UNIX_PATH>", text)
    return text


def main() -> None:
    changed: list[str] = []
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
        clean = sanitize(text)
        if clean != text:
            path.write_text(clean, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    print(f"sanitized {len(changed)} tracked text files")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
