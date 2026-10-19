from __future__ import annotations

import sys
from pathlib import Path

SKILL_SCRIPTS = Path("C:/Users/iamga/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents")
sys.path.insert(0, str(SKILL_SCRIPTS))
import render_docx  # noqa: E402


LO = Path("C:/Users/iamga/OneDrive/Documents/ChatGPT/a11ypreserve/pilot2/libreoffice_runtime/program/soffice.com")
ROOT = Path(__file__).resolve().parents[1]


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
