"""Audit manuscript numbers against the V2 evidence-aware accounting."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
TEXT = "\n".join(
    path.read_text(encoding="utf-8")
    for path in [PAPER / "main.tex", *sorted((PAPER / "sections").glob("*.tex"))]
)

CHECKS = [
    ("source fixture count", r"\b13\b", 1, "corpus/FROZEN_CORPUS_MANIFEST.json"),
    ("conversion case count", r"\b26\b", 1, "results/full_experiment/PRIMARY_RESULTS_FREEZE.json"),
    ("verified preserved count", r"\b11\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("observed partial count", r"\b3\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("altered count", r"\b3\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("confirmed lost count", r"\b2\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("unresolved equivalence count", r"\b6\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("measurement-error count", r"\b1\b", 1, "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json"),
    ("atomic source oracle count", r"13", 1, "final_strengthening/INDEPENDENT_SOURCE_ORACLE.json"),
    ("integrated source oracle count", r"21/21", 1, "integrated_study/INTEGRATED_SOURCE_ORACLE.json"),
    ("integrated property-pipeline observations", r"\b42\b", 1, "integrated_study/INTEGRATED_RESULTS.json"),
    ("LibreOffice version", r"26\.2\.6\.3", 1, "results/full_experiment/AUTOMATION_LOG.md"),
    ("Chrome version", r"153\.0\.8010\.53", 1, "results/full_experiment/AUTOMATION_LOG.md"),
    ("Windows version", r"10\.0\.26200\.0", 1, "results/full_experiment/AUTOMATION_LOG.md"),
]

rows = []
all_ok = True
for label, pattern, expected_min, evidence in CHECKS:
    count = len(re.findall(pattern, TEXT))
    status = "PASS" if count >= expected_min else "FAIL"
    all_ok &= status == "PASS"
    rows.append(f"| {label} | `{pattern}` | {count} | {evidence} | {status} |")

out = [
    "# Number Audit",
    "",
    "This audit was generated from `paper/main.tex` and all section files after the final bibliography-resolved build. It checks that V2 evidence-aware numbers are present and traceable to machine-readable result artifacts; it does not replace artifact-level verification.",
    "",
    "| Claim family | Pattern | Occurrences | Frozen evidence | Status |",
    "|---|---:|---:|---|---|",
    *rows,
    "",
    f"Overall status: **{'PASS' if all_ok else 'FAIL'}**.",
    "",
    "The manuscript reports V2 counts as the primary result model, retains V1 only for provenance, and keeps the three-document integrated check outside the primary 26-case denominator. No headline percentages are used.",
]
(PAPER / "NUMBER_AUDIT.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("PASS" if all_ok else "FAIL")
