import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v3_classify_core", ROOT / "scripts" / "v3_classify_core.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_measurement_error_precedes_loss():
    assert module.classify({
        "measurement_valid": False,
        "insufficient_evidence": True,
        "source_verified": True,
        "destination_representable": True,
        "required_representation_absent": True,
        "independent_absence_corroborated": True,
    }) == "MEASUREMENT_ERROR"


def test_loss_precedes_unresolved():
    assert module.classify({
        "measurement_valid": True,
        "source_verified": True,
        "destination_representable": True,
        "required_representation_absent": True,
        "independent_absence_corroborated": True,
        "evidence_sufficient": False,
    }) == "CONFIRMED_LOST"


def test_partial_requires_measured_component():
    assert module.classify({
        "measurement_valid": True,
        "source_verified": True,
        "destination_representable": True,
        "contract_has_multiple_components": True,
        "required_component_present": True,
        "required_component_directly_differs_or_absent": True,
        "missing_component_is_measured": True,
    }) == "OBSERVED_PARTIAL"


def test_unresolved_is_conservative_fallback():
    assert module.classify({
        "measurement_valid": True,
        "evidence_sufficient": False,
    }) == "UNRESOLVED_EQUIVALENCE"

