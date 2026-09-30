from __future__ import annotations

import sys
import os
import shutil
from pathlib import Path

SKILL_SCRIPTS = os.environ.get("A11YPRESERVE_DOCUMENT_SKILLS")
if SKILL_SCRIPTS:
    sys.path.insert(0, SKILL_SCRIPTS)
try:
    import render_docx  # type: ignore  # noqa: E402
except ModuleNotFoundError as exc:
    raise SystemExit(
        "render_docx is unavailable; install the document helper or set "
        "A11YPRESERVE_DOCUMENT_SKILLS to its directory"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
LO = Path(os.environ.get("A11YPRESERVE_SOFFICE", shutil.which("soffice.com") or shutil.which("soffice") or ""))


def main() -> None:
    if not LO.exists():
        raise SystemExit(f"Bundled LibreOffice runtime missing: {LO}")
    render_docx._resolve_soffice = lambda: str(LO)  # type: ignore[assignment]
    fixture_dir = ROOT / "corpus" / "fixtures"
    for doc in sorted(fixture_dir.glob("F*.docx")):
        output_dir = ROOT / "corpus" / "render_qa" / doc.stem
        output_dir.mkdir(parents=True, exist_ok=True)
        render_docx.rasterize(str(doc), str(output_dir), 150, verbose=True, emit_pdf=True)
        pages = sorted(output_dir.glob("page-*.png"))
        if not pages:
            raise SystemExit(f"No rendered pages for {doc.name}")
        print(f"{doc.name}: {len(pages)} page(s)")


if __name__ == "__main__":
    main()
