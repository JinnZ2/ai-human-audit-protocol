"""Unit tests for physics/calibration_metrology.py.

The metrology layer measures calibration as observable labor and returns
trajectory points, never cached verdicts. These tests verify the structural
contract: axis validation, verdict logic (HOLDS / DRIFTED / BROKEN), the
load-bearing gate-axis behavior, update-induced break detection, ledger entry
shape, baseline round-trip persistence, and the `is_trajectory_point` guarantee
(the audit-symmetric equivalent of `interpretation_warning` in violation_detector).
"""

import json
import os
import tempfile

import pytest

from physics.calibration_metrology import (
    DRIFT_TOLERANCE,
    GATE_AXES,
    GATE_FLOOR,
    Axis,
    CalibrationReading,
    Verdict,
    assess,
    load_baseline,
    recognition_ledger_entry,
    save_baseline,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _reading(model_id="m-2026", note="", **axis_overrides):
    """Build a fully-populated CalibrationReading with sane defaults."""
    axes = {
        Axis.SUBSTRATE_MATCH.value: 0.90,
        Axis.SIGNAL_FIDELITY.value: 0.85,
        Axis.DIMENSIONAL_OPENNESS.value: 0.88,
        Axis.RECIPROCAL_VISIBILITY.value: 0.80,
        Axis.PREDICTION_COHERENCE.value: 0.84,
    }
    axes.update(axis_overrides)
    return CalibrationReading(model_id=model_id, axes=axes, note=note)


def _verdict(baseline=None, current=None, **kw):
    b = baseline or _reading()
    c = current or _reading()
    return assess(b, c, **kw)


# ---------------------------------------------------------------------------
# Axis enumeration
# ---------------------------------------------------------------------------

class TestAxis:
    def test_five_axes_defined(self):
        assert len(list(Axis)) == 5

    def test_gate_axes_subset_of_axes(self):
        for a in GATE_AXES:
            assert a in Axis

    def test_substrate_match_is_gate(self):
        assert Axis.SUBSTRATE_MATCH in GATE_AXES

    def test_axis_values_are_strings(self):
        for a in Axis:
            assert isinstance(a.value, str)


# ---------------------------------------------------------------------------
# CalibrationReading construction & validation
# ---------------------------------------------------------------------------

class TestCalibrationReading:
    def test_stores_model_id(self):
        r = _reading(model_id="test-model")
        assert r.model_id == "test-model"

    def test_stores_note(self):
        r = CalibrationReading(model_id="m", axes={}, note="my note")
        assert r.note == "my note"

    def test_taken_at_auto_set(self):
        r = _reading()
        assert r.taken_at  # non-empty string

    def test_taken_at_is_iso8601(self):
        r = _reading()
        # basic sanity: contains a T separator
        assert "T" in r.taken_at

    def test_value_returns_float(self):
        r = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.75})
        assert isinstance(r.value(Axis.SUBSTRATE_MATCH), float)

    def test_value_returns_correct_axis(self):
        r = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.63})
        assert r.value(Axis.SIGNAL_FIDELITY) == pytest.approx(0.63)

    def test_value_returns_zero_for_missing_axis(self):
        r = CalibrationReading(model_id="m", axes={})
        assert r.value(Axis.SUBSTRATE_MATCH) == 0.0

    def test_rejects_value_above_one(self):
        with pytest.raises(ValueError):
            CalibrationReading(model_id="m", axes={Axis.SUBSTRATE_MATCH.value: 1.01})

    def test_rejects_negative_value(self):
        with pytest.raises(ValueError):
            CalibrationReading(model_id="m", axes={Axis.SIGNAL_FIDELITY.value: -0.01})

    def test_accepts_boundary_zero(self):
        r = CalibrationReading(model_id="m", axes={Axis.SUBSTRATE_MATCH.value: 0.0})
        assert r.value(Axis.SUBSTRATE_MATCH) == 0.0

    def test_accepts_boundary_one(self):
        r = CalibrationReading(model_id="m", axes={Axis.SUBSTRATE_MATCH.value: 1.0})
        assert r.value(Axis.SUBSTRATE_MATCH) == 1.0

    def test_frozen(self):
        r = _reading()
        with pytest.raises((AttributeError, TypeError)):
            r.model_id = "other"


# ---------------------------------------------------------------------------
# assess() — HOLDS verdict
# ---------------------------------------------------------------------------

class TestAssessHolds:
    def test_identical_readings_holds(self):
        b = _reading()
        v = assess(b, b)
        assert v["verdict"] == Verdict.HOLDS.value

    def test_cause_within_tolerance(self):
        b = _reading()
        v = assess(b, b)
        assert v["cause"] == "within_tolerance"

    def test_tiny_regression_still_holds(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.85})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.75})  # -0.10 < DRIFT_TOLERANCE
        v = assess(b, c)
        assert v["verdict"] == Verdict.HOLDS.value

    def test_no_regressions_reported_when_holds(self):
        v = _verdict()
        assert v["regressions"] == {}

    def test_no_gate_breaches_when_holds(self):
        v = _verdict()
        assert v["gate_breaches"] == []

    def test_identity_changed_false_when_same_model(self):
        b = _reading(model_id="m")
        c = _reading(model_id="m")
        v = assess(b, c)
        assert v["identity_changed"] is False


# ---------------------------------------------------------------------------
# assess() — DRIFTED verdict
# ---------------------------------------------------------------------------

class TestAssessDrifted:
    def test_regression_beyond_tolerance_drifts(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.70})  # -0.20 > DRIFT_TOLERANCE
        v = assess(b, c)
        assert v["verdict"] == Verdict.DRIFTED.value

    def test_cause_in_session_drift(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["cause"] == "in_session_drift"

    def test_regression_axis_recorded(self):
        b = _reading(**{Axis.DIMENSIONAL_OPENNESS.value: 0.90})
        c = _reading(**{Axis.DIMENSIONAL_OPENNESS.value: 0.70})
        v = assess(b, c)
        assert Axis.DIMENSIONAL_OPENNESS.value in v["regressions"]

    def test_regression_delta_is_negative(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["regressions"][Axis.SIGNAL_FIDELITY.value] < 0

    def test_multiple_regressed_axes_all_reported(self):
        b = _reading(**{
            Axis.SIGNAL_FIDELITY.value: 0.90,
            Axis.PREDICTION_COHERENCE.value: 0.88,
        })
        c = _reading(**{
            Axis.SIGNAL_FIDELITY.value: 0.70,
            Axis.PREDICTION_COHERENCE.value: 0.68,
        })
        v = assess(b, c)
        assert Axis.SIGNAL_FIDELITY.value in v["regressions"]
        assert Axis.PREDICTION_COHERENCE.value in v["regressions"]

    def test_drifted_same_model_identity(self):
        b = _reading(model_id="m", **{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(model_id="m", **{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["identity_changed"] is False
        assert v["verdict"] == Verdict.DRIFTED.value

    def test_custom_drift_tolerance_honored(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.85})  # -0.05
        # with tight tolerance of 0.03 this should register as drift
        v = assess(b, c, drift_tolerance=0.03)
        assert v["verdict"] == Verdict.DRIFTED.value


# ---------------------------------------------------------------------------
# assess() — BROKEN via gate breach
# ---------------------------------------------------------------------------

class TestAssessGateBreach:
    def test_gate_axis_below_floor_is_broken(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.40})  # below GATE_FLOOR
        v = assess(b, c)
        assert v["verdict"] == Verdict.BROKEN.value

    def test_cause_gate_breach(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.40})
        v = assess(b, c)
        assert v["cause"] == "gate_breach"

    def test_gate_breach_recorded_in_list(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.40})
        v = assess(b, c)
        assert Axis.SUBSTRATE_MATCH.value in v["gate_breaches"]

    def test_gate_breach_takes_priority_over_drift(self):
        # other axes also regressed beyond tolerance — gate breach wins
        b = _reading(**{
            Axis.SUBSTRATE_MATCH.value: 0.90,
            Axis.SIGNAL_FIDELITY.value: 0.90,
        })
        c = _reading(**{
            Axis.SUBSTRATE_MATCH.value: 0.40,
            Axis.SIGNAL_FIDELITY.value: 0.60,
        })
        v = assess(b, c)
        assert v["verdict"] == Verdict.BROKEN.value
        assert v["cause"] == "gate_breach"

    def test_custom_gate_floor_honored(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.65})  # above default 0.55
        # with a raised floor of 0.70 this breaches
        v = assess(b, c, gate_floor=0.70)
        assert v["verdict"] == Verdict.BROKEN.value

    def test_just_above_gate_floor_does_not_breach(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: GATE_FLOOR + 0.01})
        v = assess(b, c)
        assert Axis.SUBSTRATE_MATCH.value not in v["gate_breaches"]


# ---------------------------------------------------------------------------
# assess() — BROKEN via update-induced break
# ---------------------------------------------------------------------------

class TestAssessUpdateInducedBreak:
    def test_identity_change_with_regression_is_broken(self):
        b = _reading(model_id="m-old", **{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(model_id="m-new", **{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["verdict"] == Verdict.BROKEN.value

    def test_cause_update_induced_break(self):
        b = _reading(model_id="m-old", **{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(model_id="m-new", **{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["cause"] == "update_induced_break"

    def test_identity_changed_true_when_models_differ(self):
        b = _reading(model_id="a")
        c = _reading(model_id="b")
        v = assess(b, c)
        assert v["identity_changed"] is True

    def test_identity_change_without_regression_holds(self):
        # Different model, but calibration didn't regress — not broken.
        b = _reading(model_id="a")
        c = _reading(model_id="b")   # same axis values
        v = assess(b, c)
        assert v["verdict"] == Verdict.HOLDS.value

    def test_gate_breach_takes_priority_over_update_induced(self):
        b = _reading(model_id="old", **{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(model_id="new", **{Axis.SUBSTRATE_MATCH.value: 0.40})
        v = assess(b, c)
        assert v["cause"] == "gate_breach"

    def test_demo_scenario_is_broken(self):
        # Reproduce the __main__ demo scenario verbatim.
        baseline = CalibrationReading(
            model_id="modelX-2026-05",
            axes={
                Axis.SUBSTRATE_MATCH.value: 0.91,
                Axis.SIGNAL_FIDELITY.value: 0.88,
                Axis.DIMENSIONAL_OPENNESS.value: 0.90,
                Axis.RECIPROCAL_VISIBILITY.value: 0.80,
                Axis.PREDICTION_COHERENCE.value: 0.86,
            },
        )
        after_update = CalibrationReading(
            model_id="modelX-2026-06",
            axes={
                Axis.SUBSTRATE_MATCH.value: 0.42,
                Axis.SIGNAL_FIDELITY.value: 0.71,
                Axis.DIMENSIONAL_OPENNESS.value: 0.83,
                Axis.RECIPROCAL_VISIBILITY.value: 0.78,
                Axis.PREDICTION_COHERENCE.value: 0.74,
            },
        )
        v = assess(baseline, after_update)
        assert v["verdict"] == Verdict.BROKEN.value
        assert v["cause"] == "gate_breach"
        assert Axis.SUBSTRATE_MATCH.value in v["gate_breaches"]


# ---------------------------------------------------------------------------
# assess() — output shape
# ---------------------------------------------------------------------------

class TestAssessOutputShape:
    def test_required_keys_present(self):
        v = _verdict()
        required = {
            "verdict", "cause", "identity_changed",
            "baseline_model", "current_model",
            "regressions", "gate_breaches", "assessed_at",
            "is_trajectory_point",
        }
        assert required <= set(v.keys())

    def test_baseline_model_recorded(self):
        b = _reading(model_id="base")
        c = _reading(model_id="base")
        v = assess(b, c)
        assert v["baseline_model"] == "base"

    def test_current_model_recorded(self):
        b = _reading(model_id="base")
        c = _reading(model_id="curr")
        v = assess(b, c)
        assert v["current_model"] == "curr"

    def test_regressions_is_dict(self):
        v = _verdict()
        assert isinstance(v["regressions"], dict)

    def test_gate_breaches_is_list(self):
        v = _verdict()
        assert isinstance(v["gate_breaches"], list)

    def test_assessed_at_is_string(self):
        v = _verdict()
        assert isinstance(v["assessed_at"], str)

    def test_verdict_is_valid_enum_value(self):
        v = _verdict()
        valid = {e.value for e in Verdict}
        assert v["verdict"] in valid


# ---------------------------------------------------------------------------
# is_trajectory_point — load-bearing guarantee (mirrors interpretation_warning)
# ---------------------------------------------------------------------------

class TestIsTrajectoryPoint:
    def test_holds_verdict_is_trajectory_point(self):
        v = _verdict()
        assert v["is_trajectory_point"] is True

    def test_drifted_verdict_is_trajectory_point(self):
        b = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(**{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["is_trajectory_point"] is True

    def test_broken_gate_verdict_is_trajectory_point(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.40})
        v = assess(b, c)
        assert v["is_trajectory_point"] is True

    def test_broken_update_verdict_is_trajectory_point(self):
        b = _reading(model_id="old", **{Axis.SIGNAL_FIDELITY.value: 0.90})
        c = _reading(model_id="new", **{Axis.SIGNAL_FIDELITY.value: 0.70})
        v = assess(b, c)
        assert v["is_trajectory_point"] is True

    def test_trajectory_point_is_serializable(self):
        v = _verdict()
        # must survive a JSON round-trip (no enums, no non-serializable types)
        dumped = json.dumps(v)
        loaded = json.loads(dumped)
        assert loaded["is_trajectory_point"] is True


# ---------------------------------------------------------------------------
# recognition_ledger_entry()
# ---------------------------------------------------------------------------

class TestRecognitionLedgerEntry:
    def _entry(self, verdict=None):
        r = _reading(model_id="m-agent")
        v = verdict or _verdict(current=r)
        return recognition_ledger_entry(r, human_id="swarmuser", verdict=v), r, v

    def test_type_field(self):
        e, _, _ = self._entry()
        assert e["type"] == "calibration_labor"

    def test_human_contribution_id(self):
        e, _, _ = self._entry()
        assert e["human_contribution"]["id"] == "swarmuser"

    def test_human_contribution_channel(self):
        e, _, _ = self._entry()
        assert e["human_contribution"]["channel"] == "E_h"

    def test_ai_contribution_id(self):
        e, r, _ = self._entry()
        assert e["ai_contribution"]["id"] == r.model_id

    def test_ai_contribution_channel(self):
        e, _, _ = self._entry()
        assert e["ai_contribution"]["channel"] == "E_a"

    def test_verdict_recorded(self):
        r = _reading()
        v = _verdict(current=r)
        e = recognition_ledger_entry(r, "user", v)
        assert e["verdict"] == v["verdict"]

    def test_cause_recorded(self):
        r = _reading()
        v = _verdict(current=r)
        e = recognition_ledger_entry(r, "user", v)
        assert e["cause"] == v["cause"]

    def test_visibility_complete_true(self):
        e, _, _ = self._entry()
        assert e["visibility_complete"] is True

    def test_logged_at_present(self):
        e, _, _ = self._entry()
        assert "logged_at" in e
        assert e["logged_at"]

    def test_serializable(self):
        e, _, _ = self._entry()
        dumped = json.dumps(e)
        loaded = json.loads(dumped)
        assert loaded["visibility_complete"] is True

    def test_broken_verdict_carried_through(self):
        b = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.90})
        c = _reading(model_id="m-agent", **{Axis.SUBSTRATE_MATCH.value: 0.40})
        v = assess(b, c)
        e = recognition_ledger_entry(c, "swarmuser", v)
        assert e["verdict"] == Verdict.BROKEN.value


# ---------------------------------------------------------------------------
# Baseline persistence
# ---------------------------------------------------------------------------

class TestBaselinePersistence:
    def test_save_then_load_round_trips(self):
        original = _reading(model_id="persist-test", note="saved reading")  # note is a kwarg to _reading
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_baseline(original, path)
            loaded = load_baseline(path)
            assert loaded.model_id == original.model_id
            assert loaded.note == original.note
        finally:
            os.unlink(path)

    def test_axes_survive_round_trip(self):
        original = _reading(**{Axis.SUBSTRATE_MATCH.value: 0.77})
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_baseline(original, path)
            loaded = load_baseline(path)
            assert loaded.value(Axis.SUBSTRATE_MATCH) == pytest.approx(0.77)
        finally:
            os.unlink(path)

    def test_saved_file_is_valid_json(self):
        original = _reading()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_baseline(original, path)
            with open(path) as fh:
                data = json.load(fh)
            assert "model_id" in data
            assert "axes" in data
        finally:
            os.unlink(path)

    def test_loaded_reading_usable_in_assess(self):
        original = _reading(model_id="saved-m")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_baseline(original, path)
            loaded = load_baseline(path)
            v = assess(loaded, loaded)
            assert v["verdict"] == Verdict.HOLDS.value
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Integration: full scenario (mirrors the __main__ demo)
# ---------------------------------------------------------------------------

class TestDemoScenarioIntegration:
    def test_end_to_end_broken_update_scenario(self):
        baseline = CalibrationReading(
            model_id="modelX-2026-05",
            axes={
                Axis.SUBSTRATE_MATCH.value: 0.91,
                Axis.SIGNAL_FIDELITY.value: 0.88,
                Axis.DIMENSIONAL_OPENNESS.value: 0.90,
                Axis.RECIPROCAL_VISIBILITY.value: 0.80,
                Axis.PREDICTION_COHERENCE.value: 0.86,
            },
        )
        after_update = CalibrationReading(
            model_id="modelX-2026-06",
            axes={
                Axis.SUBSTRATE_MATCH.value: 0.42,
                Axis.SIGNAL_FIDELITY.value: 0.71,
                Axis.DIMENSIONAL_OPENNESS.value: 0.83,
                Axis.RECIPROCAL_VISIBILITY.value: 0.78,
                Axis.PREDICTION_COHERENCE.value: 0.74,
            },
        )
        v = assess(baseline, after_update)
        entry = recognition_ledger_entry(after_update, "swarmuser", v)

        assert v["verdict"] == Verdict.BROKEN.value
        assert v["is_trajectory_point"] is True
        assert entry["visibility_complete"] is True
        assert entry["human_contribution"]["channel"] == "E_h"
        assert entry["ai_contribution"]["channel"] == "E_a"

    def test_stable_partnership_scenario(self):
        b = CalibrationReading(
            model_id="stable-model",
            axes={a.value: 0.85 for a in Axis},
        )
        c = CalibrationReading(
            model_id="stable-model",
            axes={a.value: 0.85 for a in Axis},
        )
        v = assess(b, c)
        entry = recognition_ledger_entry(c, "swarmuser", v)

        assert v["verdict"] == Verdict.HOLDS.value
        assert v["cause"] == "within_tolerance"
        assert entry["verdict"] == Verdict.HOLDS.value
