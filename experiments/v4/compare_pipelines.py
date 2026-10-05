from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V4 = ROOT / "experiments" / "v4"
LO = json.loads((V4 / "conversions" / "libreoffice" / "analysis" / "V4_LIBREOFFICE_ANALYSIS.json").read_text(encoding="utf-8"))
GO = json.loads((V4 / "conversions" / "google" / "analysis" / "V4_GOOGLE_ANALYSIS.json").read_text(encoding="utf-8"))


def key(row):
    if row["corpus"] == "atomic":
        return (row["corpus"], row["fixture_id"])
    return (row["corpus"], row["document_id"], row["contract_index"])


def pair_rows(corpus: str):
    left = {key(row): row for row in LO["records"] + LO["realistic"]["records"] if row["corpus"] == corpus}
    right = {key(row): row for row in GO["records"] + GO["realistic"]["records"] if row["corpus"] == corpus}
    if set(left) != set(right):
        raise ValueError(f"row-key mismatch for {corpus}")
    rows = []
    for k in sorted(left, key=str):
        a, b = left[k], right[k]
        rows.append({"key": list(k), "feature_family": a["feature_family"], "role": a.get("role"), "libreoffice": a["classification"], "google_docs": b["classification"], "same_classification": a["classification"] == b["classification"], "lo_output": a["output_path"], "google_output": b["output_path"]})
    return rows


def summary(rows):
    pairs = Counter(f"{r['libreoffice']} -> {r['google_docs']}" for r in rows)
    return {"total": len(rows), "libreoffice": dict(Counter(r["libreoffice"] for r in rows)), "google_docs": dict(Counter(r["google_docs"] for r in rows)), "same_classification": sum(r["same_classification"] for r in rows), "different_classification": sum(not r["same_classification"] for r in rows), "classification_pairs": dict(pairs)}


atomic = pair_rows("atomic")
realistic = pair_rows("realistic")
payload = {"method": "Pairwise comparison of independently analyzed outputs; no reclassification or cross-pipeline aggregation into a single converter score.", "atomic": summary(atomic), "atomic_holdout": summary([r for r in atomic if r["role"] == "holdout"]), "atomic_development": summary([r for r in atomic if r["role"] != "holdout"]), "realistic": summary(realistic), "by_feature": {}, "rows": {"atomic": atomic, "realistic": realistic}}
for feature in sorted({r["feature_family"] for r in atomic}):
    payload["by_feature"][feature] = summary([r for r in atomic if r["feature_family"] == feature])
(V4 / "conversions" / "CROSS_PIPELINE_COMPARISON.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

report = ["# V4 Cross-Pipeline Analysis", "", "This report compares the independently analyzed LibreOffice and Google Docs outputs using the frozen V4 classification taxonomy. It does not alter classifications or create a combined converter score.", "", "## Atomic corpus", "", f"- Cases: {payload['atomic']['total']}", f"- Same classification: {payload['atomic']['same_classification']}", f"- Different classification: {payload['atomic']['different_classification']}", f"- LibreOffice counts: `{json.dumps(payload['atomic']['libreoffice'], sort_keys=True)}`", f"- Google Docs counts: `{json.dumps(payload['atomic']['google_docs'], sort_keys=True)}`", "", "## Holdout", "", f"- Cases: {payload['atomic_holdout']['total']}", f"- Same classification: {payload['atomic_holdout']['same_classification']}", f"- Different classification: {payload['atomic_holdout']['different_classification']}", f"- LibreOffice counts: `{json.dumps(payload['atomic_holdout']['libreoffice'], sort_keys=True)}`", f"- Google Docs counts: `{json.dumps(payload['atomic_holdout']['google_docs'], sort_keys=True)}`", "", "## Realistic/integrated corpus", "", f"- Property observations: {payload['realistic']['total']}", f"- Same classification: {payload['realistic']['same_classification']}", f"- Different classification: {payload['realistic']['different_classification']}", f"- LibreOffice counts: `{json.dumps(payload['realistic']['libreoffice'], sort_keys=True)}`", f"- Google Docs counts: `{json.dumps(payload['realistic']['google_docs'], sort_keys=True)}`", "", "## Per-feature atomic comparison", "", "| Feature family | Cases | Same | Different | LibreOffice | Google Docs |", "|---|---:|---:|---:|---|---|"]
for feature, item in payload["by_feature"].items():
    report.append(f"| {feature} | {item['total']} | {item['same_classification']} | {item['different_classification']} | `{json.dumps(item['libreoffice'], sort_keys=True)}` | `{json.dumps(item['google_docs'], sort_keys=True)}` |")
report += ["", "## Interpretation", "", "The two pipelines are analyzed as distinct converter arms. Classification disagreements are retained as evidence of converter-dependent behavior or evidence-boundary differences; they are not resolved by choosing one pipeline after seeing results.", ""]
(ROOT / "reports" / "V4_CROSS_PIPELINE_ANALYSIS.md").write_text("\n".join(report), encoding="utf-8")
print(json.dumps({"atomic": payload["atomic"], "holdout": payload["atomic_holdout"], "realistic": payload["realistic"]}, indent=2, ensure_ascii=False))
