"""Materialize versioned source-to-destination contracts from frozen inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = json.loads((ROOT / "corpus" / "FROZEN_CORPUS_MANIFEST.json").read_text(encoding="utf-8"))
OUT = ROOT / "contracts"

REQUIREMENTS = {
    "headings": ("heading structure with level and sequence preserved", ["PDF heading elements with corresponding levels and order"]),
    "alt_text": ("non-decorative figure alternative text preserved", ["Figure /Alt or an equivalent accessible figure representation"]),
    "lists": ("list membership, nesting, order, and ordered/unordered distinction preserved", ["L/LI structure with equivalent list numbering"]),
    "table": ("table dimensions, cell contents, and header row preserved", ["Table/TR/TH/TD structure or equivalent machine-verifiable table semantics"]),
    "document_language": ("document language preserved", ["document/catalog or structure language"]),
    "inline_language": ("inline language override and its text association preserved", ["marked structure span with an equivalent language attribute"]),
    "decorative_image": ("decorative and informative figure status preserved", ["Artifact or equivalent decorative representation; Figure with equivalent Alt for informative content"]),
    "links": ("link target and visible-name association preserved", ["link annotation plus an equivalent structure/name association"]),
    "document_title": ("visible and core document identity metadata preserved", ["PDF title metadata and equivalent visible title evidence"]),
    "complex_table": ("multi-level header groups and cell associations preserved", ["table header structure with equivalent span/association attributes"]),
    "footnotes": ("footnote reference, body, and association preserved", ["Note/Footnote or an equivalent machine-verifiable association"]),
    "equation": ("equation representation and readable expression preserved", ["Formula or equivalent machine-readable mathematical representation"]),
    "captions": ("caption text and figure association preserved", ["Caption structure or an equivalent figure-caption association"]),
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    for item in FROZEN["fixtures"]:
        fixture = item["fixture_id"]
        source = Path(item["path"])
        manifest = Path(item["source_manifest"])
        expected = json.loads(manifest.read_text(encoding="utf-8"))
        feature = item["feature_family"]
        requirement, equivalents = REQUIREMENTS[feature]
        contract = {
            "contract_version": "a11ypreserve-contract-v1",
            "fixture_id": fixture,
            "source": {
                "format": "DOCX", "feature": feature, "fixture_path": f"corpus/fixtures/{source.name}",
                "sha256": sha256(source), "manifest_path": f"{'corpus' if manifest.parent.name == 'manifests' else 'pilot'}/manifests/{manifest.name}",
                "manifest_sha256": sha256(manifest), "oracle": "independent raw OOXML ZIP/XML inspection plus source extractor agreement",
            },
            "destination": {"format": "PDF", "representation_requirement": requirement, "accepted_equivalents": equivalents},
            "contract": {"feature_contract": expected.get("ground_truth", {k: v for k, v in expected.items() if k not in {"fixture_id", "manifest_version", "contract_version", "document", "source_format"}})},
            "decision_rules": {
                "outcomes": ["PRESERVED", "PARTIALLY_PRESERVED", "ALTERED", "LOST", "MEASUREMENT_ERROR"],
                "evidence_statuses": ["VERIFIED_EQUIVALENCE", "OBSERVED_DIFFERENCE", "OBSERVED_PARTIAL", "INDEPENDENTLY_CONFIRMED_ABSENCE", "UNRESOLVED_EQUIVALENCE", "INSUFFICIENT_EVIDENCE", "MEASUREMENT_FAILURE"],
                "equivalence_rule": "Declare PRESERVED only when the destination representation satisfies the feature contract; otherwise record the observed difference or partial evidence without inferring semantic absence from a single extractor encoding.",
                "uncertainty_rule": "If a feature-specific equivalent cannot be established with the available destination evidence, retain the frozen outcome but label the evidence UNRESOLVED_EQUIVALENCE or INSUFFICIENT_EVIDENCE; use MEASUREMENT_FAILURE only when the measurement path fails.",
            },
            "provenance": {"frozen_corpus": "corpus/FROZEN_CORPUS_MANIFEST.json", "primary_results": "results/full_experiment/PRIMARY_RESULTS_FREEZE.json", "contract_materializer": "scripts/build_contracts.py"},
        }
        (OUT / f"{fixture}.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
