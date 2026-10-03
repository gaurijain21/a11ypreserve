from __future__ import annotations

import json
import sys
from pathlib import Path

from extract_semantics import extract
from phase4_compare import compare_all


def main(source_path: str, output_path: str, feature: str | None = None) -> None:
    source = extract(Path(source_path))
    destination = extract(Path(output_path))
    report = {"source": source_path, "output": output_path, "features": compare_all(source, destination, feature)}
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) not in {3, 4}:
        raise SystemExit("usage: a11ydiff source.docx output.pdf [feature]")
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
