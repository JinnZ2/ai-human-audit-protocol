"""Smoke tests for consortium/examples/.

Each example is a worked end-to-end demonstration of a distinct
slice of the framework. These tests verify the demos run without
error AND make a small contract assertion per example so future
regressions in the underlying machinery surface here.
"""

import json
from pathlib import Path

import pytest


# ============================================================
# soil_with_hands.py — embodied query end-to-end
# ============================================================

class TestSoilWithHands:
    def test_runs_end_to_end(self):
        from consortium.examples.soil_with_hands import run_consortium
        synth, entry = run_consortium(verbose=False)
        assert synth["problem_id"] == "soil_with_hands_demo"

    def test_embodied_frame_is_in_consulted_frames(self):
        from consortium.examples.soil_with_hands import run_consortium
        synth, _ = run_consortium(verbose=False)
        assert "embodied_sensor" in synth["adapters_fired"]

    def test_log_entry_passes_schema(self):
        from consortium.examples.soil_with_hands import run_consortium
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")

        _, entry = run_consortium(verbose=False)
        schema_path = (Path(__file__).parent.parent / "consortium"
                       / "audit" / "blind_spot_log.schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(entry, schema)

    def test_log_entry_marked_as_run(self):
        from consortium.examples.soil_with_hands import run_consortium
        _, entry = run_consortium(verbose=False)
        assert entry["entry_kind"] == "run"

    def test_coating_probe_recorded(self):
        from consortium.examples.soil_with_hands import run_consortium
        _, entry = run_consortium(verbose=False)
        # the kinesthetic reading uses constraint_inversion;
        # this test guards against the example dropping the probe
        # by accident
        probes = [c["probe"] for c in entry["coating_probes_run"]]
        assert "constraint_inversion" in probes


# ============================================================
# cherokee_creation.py — multi-encoding ontology
# ============================================================

class TestCherokeeCreation:
    def test_runs_without_error(self):
        from consortium.examples.cherokee_creation import run
        coh, full = run(verbose=False)
        assert coh.get("concept_id") == "origin_emergence"

    def test_four_encodings_present(self):
        from consortium.examples.cherokee_creation import run
        coh, _ = run(verbose=False)
        assert set(coh["encodings_present"]) == {
            "oral", "dance", "written", "equation",
        }

    def test_universal_couplings_nonempty(self):
        # the demo is intentionally constructed to have universal
        # couplings (so the machinery's "load-bearing across
        # encodings" detection is exercised). If the demo loses
        # them, the machinery loses its check.
        from consortium.examples.cherokee_creation import run
        coh, _ = run(verbose=False)
        assert coh["universal_couplings"]

    def test_load_bearing_flag_true(self):
        from consortium.examples.cherokee_creation import run
        coh, _ = run(verbose=False)
        assert coh["load_bearing_check"] is True


# ============================================================
# genesis_drift.py — regime drift detection
# ============================================================

class TestGenesisDrift:
    def test_runs_without_error(self):
        from consortium.examples.genesis_drift import run
        h, t, full = run(verbose=False)
        assert isinstance(h, list)
        assert isinstance(t, list)

    def test_no_drift_in_validating_regime(self):
        # holocene context matches the prescription's validation;
        # drift_check should NOT fire
        from consortium.examples.genesis_drift import run
        h, _, _ = run(verbose=False)
        assert h == []

    def test_drift_detected_in_post_shift_regime(self):
        # transitional context is outside validation; drift_check MUST fire
        from consortium.examples.genesis_drift import run
        _, t, _ = run(verbose=False)
        assert len(t) == 1
        assert t[0]["action"] == "do_not_silently_apply"

    def test_trust_signal_investigates_under_drift(self):
        from consortium.examples.genesis_drift import run
        _, _, full = run(verbose=False)
        # drift present → multi_query should return investigate
        assert full["trust_signal"] == "investigate"


# ============================================================
# Audit log: example file validates against schema
# ============================================================

class TestExampleBlindSpotLog:
    def _entries(self):
        path = (Path(__file__).parent.parent / "consortium"
                / "audit" / "example_blind_spot_log.jsonl")
        with open(path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def test_each_entry_validates(self):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")
        schema_path = (Path(__file__).parent.parent / "consortium"
                       / "audit" / "blind_spot_log.schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        for entry in self._entries():
            jsonschema.validate(entry, schema)

    def test_all_entry_kinds_demonstrated(self):
        # the example log should exercise all three entry_kinds so
        # the format spec is grounded in worked examples
        kinds = {e["entry_kind"] for e in self._entries()}
        assert "run" in kinds
        assert "calibration_update" in kinds
        # retrospective is the last one to add; future commits will
        # populate it. For now, run + calibration_update is enough.

    def test_calibration_update_carries_drift_proposal(self):
        cu = [e for e in self._entries()
              if e["entry_kind"] == "calibration_update"]
        assert cu, "no calibration_update example present"
        assert "frames_calibration_drift" in cu[0]
