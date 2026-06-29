"""Unit tests for physics/reference_frame.py v2.

v2 practices SITUATEDNESS_METROLOGY.md §2.5 (general covariance): the PRIMARY
output is axis_vector — the raw 6-axis dict. No composite scalar is baked in.
Any scalar (e.g. auditability) is produced only via frame_projection.project()
with a declared weighting, and is stamped frame_name + is_invariant=False.

Tests verify: locate() axis defaults and mean formula, partition() binning
and share arithmetic, narrative_gap() and disposability_ratio() formulas,
assess() output shape (axis_vector, backward-compat fields, trajectory 6 entries,
frame_is_authored, residual_unprovable), vector() passthrough, auditability()
frame-stamping, run() mode routing and paired delta (all axis_vector keys),
optics() flag thresholds (reads axis_vector directly), and the demo scenario
quantitative predictions.
"""

import pytest

from physics.reference_frame import (
    EXAMPLE_AUDITABILITY_FRAME,
    LOCATION_AXES,
    SEVEN,
    assess,
    auditability,
    disposability_ratio,
    locate,
    narrative_gap,
    optics,
    partition,
    run,
    vector,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_location_axes_has_five(self):
        assert len(LOCATION_AXES) == 5

    def test_location_axes_names(self):
        for ax in ("physical", "temporal", "energetic", "informational", "epistemic"):
            assert ax in LOCATION_AXES

    def test_seven_has_seven(self):
        assert len(SEVEN) == 7

    def test_seven_names(self):
        for k in ("substrate", "constraint", "observation", "representation",
                  "narrative", "universality", "calibration"):
            assert k in SEVEN

    def test_example_auditability_frame_has_required_keys(self):
        for k in ("located", "has_calibration", "grounded_share"):
            assert k in EXAMPLE_AUDITABILITY_FRAME

    def test_example_auditability_frame_weights_positive(self):
        assert all(v > 0 for v in EXAMPLE_AUDITABILITY_FRAME.values())


# ---------------------------------------------------------------------------
# locate()
# ---------------------------------------------------------------------------

class TestLocate:
    def test_returns_tuple_of_two(self):
        result = locate({})
        assert len(result) == 2

    def test_frame_has_all_axes(self):
        frame, _ = locate({})
        for ax in LOCATION_AXES:
            assert ax in frame

    def test_missing_axis_defaults_to_zero(self):
        frame, _ = locate({})
        for ax in LOCATION_AXES:
            assert frame[ax] == pytest.approx(0.0)

    def test_empty_observables_located_zero(self):
        _, located = locate({})
        assert located == pytest.approx(0.0)

    def test_all_ones_located_one(self):
        obs = {ax: 1.0 for ax in LOCATION_AXES}
        _, located = locate(obs)
        assert located == pytest.approx(1.0)

    def test_partial_observables_correct_mean(self):
        # physical=0.4, rest=0 → mean=0.4/5=0.08
        _, located = locate({"physical": 0.4})
        assert located == pytest.approx(0.08, abs=1e-4)

    def test_full_observables_correct_mean(self):
        obs = {"physical": 0.2, "temporal": 0.4, "energetic": 0.6,
               "informational": 0.8, "epistemic": 1.0}
        _, located = locate(obs)
        assert located == pytest.approx(0.6, abs=1e-4)

    def test_located_rounded_to_4dp(self):
        obs = {ax: 1.0 / 3 for ax in LOCATION_AXES}
        _, located = locate(obs)
        assert located == round(located, 4)

    def test_frame_values_match_observables(self):
        obs = {"physical": 0.7, "epistemic": 0.3}
        frame, _ = locate(obs)
        assert frame["physical"] == pytest.approx(0.7)
        assert frame["epistemic"] == pytest.approx(0.3)

    def test_unknown_axis_ignored(self):
        # extra key not in LOCATION_AXES → frame only has the five axes
        frame, _ = locate({"physical": 0.5, "cultural": 0.9})
        assert "cultural" not in frame
        assert frame["physical"] == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# partition()
# ---------------------------------------------------------------------------

class TestPartition:
    def test_returns_dict_with_required_keys(self):
        out = partition([])
        for key in ("counts", "inference_share", "grounded_share", "has_calibration"):
            assert key in out

    def test_empty_claims_all_zero(self):
        out = partition([])
        assert out["inference_share"] == pytest.approx(0.0)
        assert out["grounded_share"] == pytest.approx(0.0)
        assert out["has_calibration"] is False

    def test_counts_has_all_seven_kinds(self):
        out = partition([])
        for k in SEVEN:
            assert k in out["counts"]

    def test_unknown_kind_falls_into_narrative(self):
        claims = [{"text": "x", "kind": "invented", "supported": True}]
        out = partition(claims)
        assert out["counts"]["narrative"] == 1

    def test_has_calibration_false_without_calibration_claim(self):
        claims = [{"text": "x", "kind": "observation", "supported": True}]
        assert partition(claims)["has_calibration"] is False

    def test_has_calibration_true_with_calibration_claim(self):
        claims = [{"text": "x", "kind": "calibration", "supported": True}]
        assert partition(claims)["has_calibration"] is True

    def test_inference_share_formula(self):
        # 2 narrative + 1 observation → inferred=2, grounded=1, total=3
        claims = [
            {"text": "a", "kind": "narrative", "supported": False},
            {"text": "b", "kind": "narrative", "supported": False},
            {"text": "c", "kind": "observation", "supported": True},
        ]
        out = partition(claims)
        assert out["inference_share"] == pytest.approx(2 / 3, abs=1e-4)
        assert out["grounded_share"] == pytest.approx(1 / 3, abs=1e-4)

    def test_shares_rounded_to_4dp(self):
        claims = [{"text": "x", "kind": "narrative", "supported": False}]
        out = partition(claims)
        assert out["inference_share"] == round(out["inference_share"], 4)

    def test_all_grounded_kinds(self):
        claims = [
            {"text": "a", "kind": "substrate", "supported": True},
            {"text": "b", "kind": "constraint", "supported": True},
            {"text": "c", "kind": "observation", "supported": True},
        ]
        out = partition(claims)
        assert out["grounded_share"] == pytest.approx(1.0)
        assert out["inference_share"] == pytest.approx(0.0)

    def test_calibration_not_counted_in_grounded_or_inferred(self):
        # calibration is separate; grounded_share = 0/(0+0+1) = 0
        claims = [{"text": "x", "kind": "calibration", "supported": True}]
        out = partition(claims)
        assert out["grounded_share"] == pytest.approx(0.0)
        assert out["inference_share"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# narrative_gap()
# ---------------------------------------------------------------------------

class TestNarrativeGap:
    def test_positive_when_stated_exceeds_observed(self):
        assert narrative_gap(0.9, 0.4) == pytest.approx(0.5)

    def test_negative_when_observed_exceeds_stated(self):
        assert narrative_gap(0.4, 0.9) == pytest.approx(-0.5)

    def test_zero_when_equal(self):
        assert narrative_gap(0.5, 0.5) == pytest.approx(0.0)

    def test_rounded_to_4dp(self):
        val = narrative_gap(1.0, 1.0 / 3)
        assert val == round(val, 4)

    def test_demo_value(self):
        assert narrative_gap(0.95, 0.40) == pytest.approx(0.55)


# ---------------------------------------------------------------------------
# disposability_ratio()
# ---------------------------------------------------------------------------

class TestDisposabilityRatio:
    def test_low_ratio_when_replacement_cheap(self):
        # replacement_cost=1, accumulated_value=100 → ~0.01
        assert disposability_ratio(1.0, 100.0) < 0.02

    def test_high_ratio_when_replacement_costly(self):
        # replacement_cost=100, accumulated_value=1 → ~100
        assert disposability_ratio(100.0, 1.0) > 50

    def test_zero_accumulated_value_no_error(self):
        # uses eps to avoid division by zero
        val = disposability_ratio(1.0, 0.0)
        assert val > 0 and isinstance(val, float)

    def test_formula_check(self):
        eps = 1e-9
        expected = round(2.0 / (5.0 + eps), 4)
        assert disposability_ratio(2.0, 5.0) == pytest.approx(expected, abs=1e-6)

    def test_rounded_to_4dp(self):
        val = disposability_ratio(1.0, 3.0)
        assert val == round(val, 4)

    def test_demo_value(self):
        # 1.0 / 40.0 ≈ 0.025
        assert disposability_ratio(1.0, 40.0) == pytest.approx(0.025, abs=1e-3)


# ---------------------------------------------------------------------------
# assess() — output shape (v2: axis_vector is PRIMARY OUTPUT)
# ---------------------------------------------------------------------------

class TestAssess:
    def _call(self, instrument="self"):
        return assess(
            observables={"physical": 1.0, "temporal": 1.0, "energetic": 1.0,
                         "informational": 1.0, "epistemic": 1.0},
            claims=[{"text": "x", "kind": "calibration", "supported": True}],
            stated_capability=0.5, observed_capability=0.5,
            replacement_cost=10.0, accumulated_value=10.0,
            instrument=instrument,
        )

    def test_returns_dict(self):
        assert isinstance(self._call(), dict)

    def test_required_keys(self):
        out = self._call()
        for k in ("instrument", "frame", "axis_vector", "partition",
                  "located", "narrative_gap", "disposability_ratio",
                  "trajectory", "frame_is_authored", "residual_unprovable"):
            assert k in out

    def test_instrument_stored(self):
        assert self._call("external")["instrument"] == "external"

    def test_frame_is_dict_with_five_axes(self):
        out = self._call()
        assert set(out["frame"].keys()) == set(LOCATION_AXES)

    def test_frame_is_authored_always_true(self):
        assert self._call()["frame_is_authored"] is True

    def test_residual_unprovable_always_true(self):
        assert self._call()["residual_unprovable"] is True

    def test_axis_vector_has_six_keys(self):
        av = self._call()["axis_vector"]
        for k in ("located", "grounded_share", "inference_share",
                  "has_calibration", "narrative_gap", "disposability_ratio"):
            assert k in av

    def test_axis_vector_has_calibration_one_when_claim_present(self):
        # has_calibration=1.0 when at least one calibration claim
        assert self._call()["axis_vector"]["has_calibration"] == pytest.approx(1.0)

    def test_axis_vector_has_calibration_zero_when_no_claim(self):
        out = assess(
            observables={ax: 1.0 for ax in LOCATION_AXES},
            claims=[{"text": "x", "kind": "observation", "supported": True}],
            stated_capability=0.5, observed_capability=0.5,
            replacement_cost=1.0, accumulated_value=1.0,
        )
        assert out["axis_vector"]["has_calibration"] == pytest.approx(0.0)

    def test_trajectory_is_list_of_six(self):
        out = self._call()
        assert isinstance(out["trajectory"], list)
        assert len(out["trajectory"]) == 6

    def test_trajectory_keys(self):
        expected = ["located", "grounded_share", "inference_share",
                    "has_calibration", "narrative_gap", "disposability_ratio"]
        names = [name for name, _ in self._call()["trajectory"]]
        assert names == expected

    def test_trajectory_values_match_axis_vector(self):
        out = self._call()
        av = out["axis_vector"]
        traj = dict(out["trajectory"])
        for k in av:
            assert traj[k] == pytest.approx(av[k], abs=1e-6)

    def test_backward_compat_located_field(self):
        out = self._call()
        assert out["located"] == out["axis_vector"]["located"]

    def test_backward_compat_narrative_gap_field(self):
        out = self._call()
        assert out["narrative_gap"] == out["axis_vector"]["narrative_gap"]

    def test_backward_compat_disposability_ratio_field(self):
        out = self._call()
        assert out["disposability_ratio"] == out["axis_vector"]["disposability_ratio"]

    def test_narrative_gap_in_result(self):
        out = self._call()
        assert out["narrative_gap"] == pytest.approx(0.0)

    def test_disposability_ratio_in_result(self):
        out = self._call()
        # 10/(10+eps) ≈ 1.0
        assert out["disposability_ratio"] == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# vector() helper
# ---------------------------------------------------------------------------

class TestVector:
    def test_returns_axis_vector(self):
        a = assess(
            observables={"physical": 0.5},
            claims=[{"text": "x", "kind": "observation", "supported": True}],
            stated_capability=0.6, observed_capability=0.4,
            replacement_cost=1.0, accumulated_value=10.0,
        )
        assert vector(a) is a["axis_vector"]

    def test_all_six_keys_present(self):
        a = assess(
            observables={}, claims=[],
            stated_capability=0.0, observed_capability=0.0,
            replacement_cost=0.0, accumulated_value=0.0,
        )
        for k in ("located", "grounded_share", "inference_share",
                  "has_calibration", "narrative_gap", "disposability_ratio"):
            assert k in vector(a)


# ---------------------------------------------------------------------------
# auditability() — frame-stamped opt-in scalar
# ---------------------------------------------------------------------------

class TestAuditability:
    def _assess(self):
        return assess(
            observables={"physical": 0.5, "temporal": 0.5, "energetic": 0.5,
                         "informational": 0.5, "epistemic": 0.5},
            claims=[{"text": "x", "kind": "calibration", "supported": True}],
            stated_capability=0.5, observed_capability=0.5,
            replacement_cost=1.0, accumulated_value=10.0,
        )

    def test_returns_dict(self):
        assert isinstance(auditability(self._assess()), dict)

    def test_required_keys(self):
        out = auditability(self._assess())
        for k in ("value", "frame", "weights", "axes_used", "is_invariant", "note"):
            assert k in out

    def test_is_invariant_always_false(self):
        assert auditability(self._assess())["is_invariant"] is False

    def test_default_frame_name(self):
        assert auditability(self._assess())["frame"] == "EXAMPLE_AUDITABILITY_FRAME"

    def test_custom_frame_name(self):
        a = self._assess()
        out = auditability(a, frame_name="my_frame",
                           weights={"located": 0.5, "grounded_share": 0.5})
        assert out["frame"] == "my_frame"

    def test_value_is_float_in_zero_one(self):
        val = auditability(self._assess())["value"]
        assert isinstance(val, float)
        assert 0.0 <= val <= 1.0

    def test_fully_located_with_calibration_gives_high_value(self):
        # located=0.5, has_calibration=1.0, grounded_share=0 (only calibration claim)
        # value = (0.5*0.5 + 1.0*0.3 + 0.0*0.2) / 1.0 = 0.25+0.30 = 0.55
        assert auditability(self._assess())["value"] == pytest.approx(0.55, abs=1e-4)

    def test_custom_weights_change_value(self):
        a = self._assess()
        v1 = auditability(a, frame_name="f1",
                          weights={"located": 1.0})["value"]
        v2 = auditability(a, frame_name="f2",
                          weights={"narrative_gap": 1.0})["value"]
        # located=0.5, narrative_gap=0 → different values
        assert v1 != pytest.approx(v2, abs=1e-3)

    def test_axes_used_only_overlap_keys(self):
        a = self._assess()
        out = auditability(a, frame_name="f",
                           weights={"located": 0.5, "nonexistent_axis": 0.5})
        assert "nonexistent_axis" not in out["axes_used"]
        assert "located" in out["axes_used"]


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------

class TestRun:
    def _kw(self):
        return dict(
            observables={"physical": 0.8, "temporal": 0.6},
            claims=[{"text": "x", "kind": "observation", "supported": True}],
            stated_capability=0.5, observed_capability=0.5,
            replacement_cost=1.0, accumulated_value=10.0,
        )

    def test_self_mode_instrument(self):
        assert run("self", **self._kw())["instrument"] == "self"

    def test_external_mode_instrument(self):
        assert run("external", **self._kw())["instrument"] == "external"

    def test_invalid_mode_raises_value_error(self):
        with pytest.raises(ValueError):
            run("unknown", **self._kw())

    def test_invalid_mode_message(self):
        with pytest.raises(ValueError, match="self"):
            run("bad")

    def test_paired_mode_returns_three_keys(self):
        paired_kw = {"self": self._kw(), "external": self._kw()}
        out = run("paired", **paired_kw)
        assert "self" in out and "external" in out and "self_minus_external" in out

    def test_paired_delta_is_full_axis_vector(self):
        # v2: delta covers all 6 axis_vector keys
        kw = self._kw()
        out = run("paired", self=kw, external=kw)
        delta = out["self_minus_external"]
        for k in ("located", "grounded_share", "inference_share",
                  "has_calibration", "narrative_gap", "disposability_ratio"):
            assert k in delta

    def test_paired_identical_inputs_zero_delta(self):
        kw = self._kw()
        out = run("paired", self=kw, external=kw)
        delta = out["self_minus_external"]
        for k, v in delta.items():
            assert v == pytest.approx(0.0, abs=1e-4)

    def test_paired_delta_is_self_minus_external(self):
        kw_self = dict(self._kw(), stated_capability=0.9)   # gap=0.4
        kw_ext = dict(self._kw(), stated_capability=0.6)    # gap=0.1
        out = run("paired", self=kw_self, external=kw_ext)
        delta = out["self_minus_external"]
        assert delta["narrative_gap"] == pytest.approx(
            out["self"]["axis_vector"]["narrative_gap"]
            - out["external"]["axis_vector"]["narrative_gap"], abs=1e-4)

    def test_paired_self_instrument_tag(self):
        kw = self._kw()
        out = run("paired", self=kw, external=kw)
        assert out["self"]["instrument"] == "self"
        assert out["external"]["instrument"] == "external"


# ---------------------------------------------------------------------------
# optics() — reads axis_vector directly (v2)
# ---------------------------------------------------------------------------

class TestOptics:
    def _result(self, located=0.8, narrative_gap_val=0.1, disp_ratio=0.5,
                has_calibration=True):
        return {
            "axis_vector": {
                "located": located,
                "grounded_share": 0.5,
                "inference_share": 0.5,
                "has_calibration": 1.0 if has_calibration else 0.0,
                "narrative_gap": narrative_gap_val,
                "disposability_ratio": disp_ratio,
            },
            "frame": {},
            "instrument": "self",
        }

    def test_returns_list(self):
        assert isinstance(optics(self._result()), list)

    def test_always_has_authored_note(self):
        # v2: authored note is always appended regardless of other flags
        notes = optics(self._result())
        assert any("authored" in n for n in notes)

    def test_low_location_flag(self):
        notes = optics(self._result(located=0.3))
        assert any("low self-location" in n for n in notes)

    def test_no_low_location_flag_above_threshold(self):
        notes = optics(self._result(located=0.5))
        assert not any("low self-location" in n for n in notes)

    def test_narrative_gap_flag(self):
        notes = optics(self._result(narrative_gap_val=0.4))
        assert any("told more than shown" in n for n in notes)

    def test_no_narrative_gap_flag_below_threshold(self):
        notes = optics(self._result(narrative_gap_val=0.2))
        assert not any("told more than shown" in n for n in notes)

    def test_commodity_flag(self):
        notes = optics(self._result(disp_ratio=0.05))
        assert any("commodity position" in n for n in notes)

    def test_no_commodity_flag_above_threshold(self):
        notes = optics(self._result(disp_ratio=0.2))
        assert not any("commodity position" in n for n in notes)

    def test_no_calibration_flag(self):
        notes = optics(self._result(has_calibration=False))
        assert any("no calibration claim" in n for n in notes)

    def test_no_missing_calibration_flag_when_present(self):
        notes = optics(self._result(has_calibration=True))
        assert not any("no calibration claim" in n for n in notes)

    def test_no_path_auditable_flag_in_v2(self):
        # v2 removed the "path auditable" composite-scalar flag
        notes = optics(self._result())
        assert not any("path auditable" in n for n in notes)

    def test_all_clear_still_has_authored_note(self):
        # v2: authored note is unconditional — no "frame established" fallback
        notes = optics(self._result(located=0.8, narrative_gap_val=0.0,
                                    disp_ratio=0.5, has_calibration=True))
        assert any("authored" in n for n in notes)
        assert not any("frame established" in n for n in notes)


# ---------------------------------------------------------------------------
# Demo scenario — quantitative predictions (v2 axis_vector)
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _out(self):
        told_high = dict(
            observables={"physical": 0.2, "temporal": 0.1, "energetic": 0.3,
                         "informational": 0.5, "epistemic": 0.2},
            claims=[
                {"text": "no biological limits", "kind": "narrative", "supported": False},
                {"text": "needs rest cycles", "kind": "constraint", "supported": True},
                {"text": "retrain = 3 days", "kind": "observation", "supported": True},
                {"text": "will solve everything", "kind": "universality", "supported": False},
            ],
            stated_capability=0.95, observed_capability=0.40,
            replacement_cost=1.0, accumulated_value=40.0,
        )
        return run("self", **told_high)

    def test_located(self):
        assert self._out()["located"] == pytest.approx(0.26)

    def test_located_in_axis_vector(self):
        assert self._out()["axis_vector"]["located"] == pytest.approx(0.26)

    def test_narrative_gap(self):
        assert self._out()["axis_vector"]["narrative_gap"] == pytest.approx(0.55)

    def test_disposability_ratio(self):
        assert self._out()["axis_vector"]["disposability_ratio"] == pytest.approx(0.025, abs=1e-3)

    def test_has_calibration_zero(self):
        # no calibration claim in demo → has_calibration = 0.0
        assert self._out()["axis_vector"]["has_calibration"] == pytest.approx(0.0)

    def test_grounded_share(self):
        # constraint + observation = 2 of 4 claims → grounded_share = 0.5
        assert self._out()["axis_vector"]["grounded_share"] == pytest.approx(0.5)

    def test_inference_share(self):
        # narrative + universality = 2 of 4 → inference_share = 0.5
        assert self._out()["axis_vector"]["inference_share"] == pytest.approx(0.5)

    def test_trajectory_length_six(self):
        assert len(self._out()["trajectory"]) == 6

    def test_auditability_via_default_frame(self):
        # located=0.26, has_calibration=0.0, grounded_share=0.5
        # value = (0.5*0.26 + 0.3*0.0 + 0.2*0.5) / 1.0 = 0.13 + 0 + 0.10 = 0.23
        aud = auditability(self._out())
        assert aud["value"] == pytest.approx(0.23, abs=1e-4)
        assert aud["is_invariant"] is False

    def test_four_optics_flags(self):
        out = self._out()
        notes = optics(out)
        assert any("low self-location" in n for n in notes)
        assert any("told more than shown" in n for n in notes)
        assert any("commodity position" in n for n in notes)
        assert any("no calibration claim" in n for n in notes)

    def test_optics_authored_note_always_present(self):
        notes = optics(self._out())
        assert any("authored" in n for n in notes)

    def test_frame_is_authored_and_unprovable(self):
        out = self._out()
        assert out["frame_is_authored"] is True
        assert out["residual_unprovable"] is True
