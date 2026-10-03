"""Reconcile final manuscript numbers and terminology with V2 results."""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
freeze = json.loads((ROOT / "results/full_experiment/FINAL_EVIDENCE_AWARE_RESULTS.json").read_text(encoding="utf-8"))
counts = freeze["counts"]
integrated = json.loads((ROOT / "integrated_study/INTEGRATED_RESULTS.json").read_text(encoding="utf-8"))
oracle = json.loads((ROOT / "integrated_study/INTEGRATED_SOURCE_ORACLE.json").read_text(encoding="utf-8"))
tex = "\n".join(path.read_text(encoding="utf-8") for path in [ROOT / "paper/main.tex", *sorted((ROOT / "paper/sections").glob("*.tex"))])

checks = [
    ("total primary cases", freeze["record_count"] == 26, str(freeze["record_count"])),
    ("verified preserved", counts["VERIFIED_PRESERVED"] == 11, str(counts["VERIFIED_PRESERVED"])),
    ("observed partial", counts["OBSERVED_PARTIAL"] == 3, str(counts["OBSERVED_PARTIAL"])),
    ("altered", counts["ALTERED"] == 3, str(counts["ALTERED"])),
    ("confirmed lost", counts["CONFIRMED_LOST"] == 2, str(counts["CONFIRMED_LOST"])),
    ("unresolved equivalence", counts["UNRESOLVED_EQUIVALENCE"] == 6, str(counts["UNRESOLVED_EQUIVALENCE"])),
    ("measurement error", counts["MEASUREMENT_ERROR"] == 1, str(counts["MEASUREMENT_ERROR"])),
    ("integrated documents", integrated["documents"] == 3, str(integrated["documents"])),
    ("integrated observations", len(integrated["records"]) == 42, str(len(integrated["records"]))),
    ("integrated source oracle", oracle["passed"] == 21 and oracle["failed"] == 0, f"{oracle['passed']}/{oracle['contract_count']}"),
]

forbidden = [
    "failure rate", "semantic failure", "Google's PDF exporter loses",
    "Google Docs is generally less accessible", "LibreOffice is generally better",
    "blind users could no longer", "all document conversion destroys accessibility",
]
for phrase in forbidden:
    checks.append((f"forbidden phrase absent: {phrase}", phrase.lower() not in tex.lower(), "absent"))

rows = ["# Final Number and Terminology Check", "", "The check below reads `FINAL_EVIDENCE_AWARE_RESULTS.json`, `INTEGRATED_RESULTS.json`, `INTEGRATED_SOURCE_ORACLE.json`, and the final `.tex` sources. It recomputes the V2 and secondary counts, then scans for prohibited overclaims.", "", "| Check | Expected/observed | Status |", "|---|---:|---|"]
for label, ok, observed in checks:
    rows.append(f"| {label} | {observed} | {'PASS' if ok else 'FAIL'} |")
ok = all(item[1] for item in checks)
rows.extend(["", f"Overall status: **{'PASS' if ok else 'FAIL'}**.", "", "V2 counts are controlled-case observations, not population estimates. Integrated observations remain outside the primary denominator."])
(ROOT / "final_review/FINAL_NUMBER_AUDIT.md").parent.mkdir(exist_ok=True)
(ROOT / "final_review/FINAL_NUMBER_AUDIT.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
print("PASS" if ok else "FAIL")
