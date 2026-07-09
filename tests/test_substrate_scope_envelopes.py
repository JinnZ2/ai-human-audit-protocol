"""Unit tests for physics/substrate_scope_envelopes.py.

Three pluggable competence-envelope sources for substrate_scope_validator:
  fixed — vendor sheet pass-through ("ASSUMED not OBSERVED")
  failures — bounding box of OK field observations, optionally shrunk by margin
  intersect — spec AND observed (spec/field must both agree)

Tests verify: return types and mode strings, bounding-box formula, margin
shrinkage, no-ok edge case, intersection logic (overlap / no-overlap / contained),
the dispatcher routing, and demo scenario quantitative predictions.
"""

import pytest

from physics.substrate_scope_envelopes import (
    envelope,
    envelope_fixed,
    envelope_from_failures,
    envelope_intersect,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _logs():
    return [
        {"heat": 30, "load": 20, "ok": True},
        {"heat": 55, "load": 40, "ok": True},
        {"heat": 68, "load": 55, "ok": False},
        {"heat": 40, "load": 10, "ok": True},
        {"heat": 62, "load": 50, "ok": False},
    ]

def _spec():
    return {"heat": (10, 70), "load": (0, 60)}

def _axes():
    return ["heat", "load"]


# ---------------------------------------------------------------------------
# envelope_fixed()
# ---------------------------------------------------------------------------

class TestEnvelopeFixed:
    def test_returns_tuple_of_two(self):
        result = envelope_fixed({"x": (0.0, 1.0)})
        assert len(result) == 2

    def test_mode_string_is_fixed_spec(self):
        _, src = envelope_fixed({"x": (0.0, 1.0)})
        assert src == "fixed_spec"

    def test_single_axis_preserved(self):
        env, _ = envelope_fixed({"x": (5.0, 15.0)})
        assert env["x"] == (5.0, 15.0)

    def test_multi_axis_all_preserved(self):
        spec = {"heat": (10, 70), "load": (0, 60)}
        env, _ = envelope_fixed(spec)
        assert env["heat"] == (10, 70)
        assert env["load"] == (0, 60)

    def test_returns_copy_not_same_object(self):
        spec = {"x": (0.0, 1.0)}
        env, _ = envelope_fixed(spec)
        assert env is not spec

    def test_empty_spec_returns_empty_dict(self):
        env, src = envelope_fixed({})
        assert env == {}
        assert src == "fixed_spec"

    def test_envelope_values_unchanged(self):
        spec = {"a": (3.0, 7.0), "b": (1.0, 99.0)}
        env, _ = envelope_fixed(spec)
        for ax in spec:
            assert env[ax] == spec[ax]


# ---------------------------------------------------------------------------
# envelope_from_failures()
# ---------------------------------------------------------------------------

class TestEnvelopeFromFailures:
    def test_returns_tuple_of_two(self):
        result = envelope_from_failures([], ["x"], margin=0.0)
        assert len(result) == 2

    def test_mode_string_is_observed_failures(self):
        _, src = envelope_from_failures([], ["x"])
        assert src == "observed_failures"

    def test_no_ok_entries_gives_zero_zero(self):
        logs = [{"x": 5.0, "ok": False}, {"x": 8.0, "ok": False}]
        env, _ = envelope_from_failures(logs, ["x"])
        assert env["x"] == (0.0, 0.0)

    def test_missing_ok_key_treated_as_not_ok(self):
        logs = [{"x": 5.0}]  # no "ok" key → r.get("ok") is None → falsy
        env, _ = envelope_from_failures(logs, ["x"])
        assert env["x"] == (0.0, 0.0)

    def test_single_ok_entry_lo_equals_hi(self):
        logs = [{"x": 42.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"])
        lo, hi = env["x"]
        assert lo == pytest.approx(42.0)
        assert hi == pytest.approx(42.0)

    def test_two_ok_entries_bounding_box(self):
        logs = [{"x": 10.0, "ok": True}, {"x": 30.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"])
        assert env["x"] == pytest.approx((10.0, 30.0))

    def test_failed_entries_excluded(self):
        logs = [
            {"x": 5.0, "ok": True},
            {"x": 100.0, "ok": False},   # extreme failure excluded
            {"x": 20.0, "ok": True},
        ]
        env, _ = envelope_from_failures(logs, ["x"])
        lo, hi = env["x"]
        assert hi == pytest.approx(20.0)   # not 100

    def test_zero_margin_exact_bounding_box(self):
        logs = [{"x": 30.0, "ok": True}, {"x": 55.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"], margin=0.0)
        assert env["x"] == pytest.approx((30.0, 55.0))

    def test_positive_margin_shrinks_bounds(self):
        # lo=30, hi=55, span=25, margin=0.2: lo_new=32.5, hi_new=52.5
        logs = [{"x": 30.0, "ok": True}, {"x": 55.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"], margin=0.2)
        lo, hi = env["x"]
        assert lo == pytest.approx(32.5, abs=1e-6)
        assert hi == pytest.approx(52.5, abs=1e-6)

    def test_margin_lo_increases_hi_decreases(self):
        logs = [{"x": 10.0, "ok": True}, {"x": 90.0, "ok": True}]
        env0, _ = envelope_from_failures(logs, ["x"], margin=0.0)
        envm, _ = envelope_from_failures(logs, ["x"], margin=0.5)
        lo0, hi0 = env0["x"]
        lom, him = envm["x"]
        assert lom > lo0
        assert him < hi0

    def test_multi_axis_independent(self):
        logs = _logs()
        env, _ = envelope_from_failures(logs, _axes())
        # heat ok: [30, 55, 40] → (30, 55)
        assert env["heat"] == pytest.approx((30.0, 55.0))
        # load ok: [20, 40, 10] → (10, 40)
        assert env["load"] == pytest.approx((10.0, 40.0))

    def test_all_ok_uses_all_observations(self):
        logs = [{"x": v, "ok": True} for v in (1, 5, 3, 9, 2)]
        env, _ = envelope_from_failures(logs, ["x"])
        assert env["x"] == pytest.approx((1.0, 9.0))

    def test_large_margin_gives_zero_zero(self):
        # margin=2.0: lo_new=30+25=55, hi_new=55-25=30 → lo_new>hi_new → (0.0,0.0)
        logs = [{"x": 30.0, "ok": True}, {"x": 55.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"], margin=2.0)
        assert env["x"] == (0.0, 0.0)

    def test_margin_just_over_one_gives_zero_zero(self):
        # margin=1.0+ε causes inversion
        logs = [{"x": 10.0, "ok": True}, {"x": 20.0, "ok": True}]
        env, _ = envelope_from_failures(logs, ["x"], margin=1.01)
        assert env["x"] == (0.0, 0.0)


# ---------------------------------------------------------------------------
# envelope_intersect()
# ---------------------------------------------------------------------------

class TestEnvelopeIntersect:
    def test_returns_tuple_of_two(self):
        result = envelope_intersect({"x": (0, 10)}, [], ["x"])
        assert len(result) == 2

    def test_mode_string_is_spec_AND_observed(self):
        _, src = envelope_intersect({"x": (0, 10)}, [], ["x"])
        assert src == "spec_AND_observed"

    def test_no_ok_logs_gives_zero_zero(self):
        # observed = (0.0,0.0); spec=(0,10); lo=max(0,0)=0, hi=min(10,0)=0 → (0,0)
        env, _ = envelope_intersect({"x": (0.0, 10.0)}, [], ["x"])
        assert env["x"] == (0.0, 0.0)

    def test_obs_contained_in_spec_gives_obs(self):
        # obs=(30,55) ⊂ spec=(10,70) → intersect=(30,55)
        logs = [{"x": 30.0, "ok": True}, {"x": 55.0, "ok": True}]
        env, _ = envelope_intersect({"x": (10.0, 70.0)}, logs, ["x"])
        assert env["x"] == pytest.approx((30.0, 55.0))

    def test_spec_contained_in_obs_gives_spec(self):
        # spec=(30,55) ⊂ obs=(10,80) → intersect=(30,55)
        logs = [{"x": 10.0, "ok": True}, {"x": 80.0, "ok": True}]
        env, _ = envelope_intersect({"x": (30.0, 55.0)}, logs, ["x"])
        assert env["x"] == pytest.approx((30.0, 55.0))

    def test_no_overlap_gives_zero_zero(self):
        # spec=(0,10); obs=(20,30) → lo=max(0,20)=20, hi=min(10,30)=10 → lo>hi → (0,0)
        logs = [{"x": 20.0, "ok": True}, {"x": 30.0, "ok": True}]
        env, _ = envelope_intersect({"x": (0.0, 10.0)}, logs, ["x"])
        assert env["x"] == (0.0, 0.0)

    def test_partial_overlap_gives_intersection(self):
        # spec=(0,20); obs=(15,35) → intersect=(15,20)
        logs = [{"x": 15.0, "ok": True}, {"x": 35.0, "ok": True}]
        env, _ = envelope_intersect({"x": (0.0, 20.0)}, logs, ["x"])
        assert env["x"] == pytest.approx((15.0, 20.0))

    def test_exact_match_gives_same(self):
        logs = [{"x": 10.0, "ok": True}, {"x": 50.0, "ok": True}]
        env, _ = envelope_intersect({"x": (10.0, 50.0)}, logs, ["x"])
        assert env["x"] == pytest.approx((10.0, 50.0))

    def test_multi_axis_demo_data(self):
        # intersect = observed since obs ⊂ spec for both axes
        env, _ = envelope_intersect(_spec(), _logs(), _axes())
        assert env["heat"] == pytest.approx((30.0, 55.0))
        assert env["load"] == pytest.approx((10.0, 40.0))

    def test_narrower_than_fixed(self):
        env_fixed, _ = envelope_fixed(_spec())
        env_intersect, _ = envelope_intersect(_spec(), _logs(), _axes())
        for ax in _axes():
            lo_f, hi_f = env_fixed[ax]
            lo_i, hi_i = env_intersect[ax]
            assert lo_i >= lo_f
            assert hi_i <= hi_f

    def test_margin_propagates_to_observed_bounds(self):
        # margin shrinks the observed bounding box before intersection
        logs = [{"x": 10.0, "ok": True}, {"x": 50.0, "ok": True}]
        env0, _ = envelope_intersect({"x": (0.0, 100.0)}, logs, ["x"], margin=0.0)
        envm, _ = envelope_intersect({"x": (0.0, 100.0)}, logs, ["x"], margin=0.5)
        lo0, hi0 = env0["x"]
        lom, him = envm["x"]
        assert lom > lo0
        assert him < hi0


# ---------------------------------------------------------------------------
# envelope() dispatcher
# ---------------------------------------------------------------------------

class TestEnvelopeDispatcher:
    def test_fixed_mode_returns_fixed_spec_src(self):
        _, src = envelope("fixed", spec=_spec())
        assert src == "fixed_spec"

    def test_fixed_mode_passthrough(self):
        env, _ = envelope("fixed", spec={"x": (1.0, 9.0)})
        assert env["x"] == (1.0, 9.0)

    def test_failures_mode_returns_observed_failures_src(self):
        _, src = envelope("failures", field_logs=_logs(), axes=_axes())
        assert src == "observed_failures"

    def test_failures_mode_bounding_box(self):
        env, _ = envelope("failures", field_logs=_logs(), axes=_axes())
        assert env["heat"] == pytest.approx((30.0, 55.0))

    def test_intersect_mode_returns_spec_AND_observed_src(self):
        _, src = envelope("intersect", spec=_spec(), field_logs=_logs(), axes=_axes())
        assert src == "spec_AND_observed"

    def test_intersect_mode_result(self):
        env, _ = envelope("intersect", spec=_spec(), field_logs=_logs(), axes=_axes())
        assert env["heat"] == pytest.approx((30.0, 55.0))

    def test_failures_margin_kwarg(self):
        env0, _ = envelope("failures", field_logs=_logs(), axes=_axes(), margin=0.0)
        envm, _ = envelope("failures", field_logs=_logs(), axes=_axes(), margin=0.5)
        lo0, hi0 = env0["heat"]
        lom, him = envm["heat"]
        assert lom > lo0 and him < hi0

    def test_intersect_margin_kwarg(self):
        env0, _ = envelope("intersect", spec=_spec(), field_logs=_logs(),
                           axes=_axes(), margin=0.0)
        envm, _ = envelope("intersect", spec=_spec(), field_logs=_logs(),
                           axes=_axes(), margin=0.5)
        lo0, hi0 = env0["heat"]
        lom, him = envm["heat"]
        assert lom >= lo0 and him <= hi0

    def test_invalid_mode_raises_value_error(self):
        with pytest.raises(ValueError):
            envelope("unknown", spec=_spec())

    def test_invalid_mode_message_contains_valid_options(self):
        with pytest.raises(ValueError, match="fixed|failures|intersect"):
            envelope("bad")


# ---------------------------------------------------------------------------
# Demo scenario — quantitative predictions
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def test_fixed_envelope_matches_spec(self):
        env, src = envelope_fixed(_spec())
        assert env == _spec()
        assert src == "fixed_spec"

    def test_failures_envelope_heat_range(self):
        env, _ = envelope_from_failures(_logs(), _axes())
        assert env["heat"] == pytest.approx((30.0, 55.0))

    def test_failures_envelope_load_range(self):
        env, _ = envelope_from_failures(_logs(), _axes())
        assert env["load"] == pytest.approx((10.0, 40.0))

    def test_intersect_matches_failures_when_obs_subset_of_spec(self):
        env_f, _ = envelope_from_failures(_logs(), _axes())
        env_i, _ = envelope_intersect(_spec(), _logs(), _axes())
        for ax in _axes():
            assert env_i[ax] == pytest.approx(env_f[ax])

    def test_failures_narrower_than_fixed_for_demo(self):
        env_fixed, _ = envelope_fixed(_spec())
        env_fail, _ = envelope_from_failures(_logs(), _axes())
        for ax in _axes():
            lo_fixed, hi_fixed = env_fixed[ax]
            lo_fail, hi_fail = env_fail[ax]
            assert (hi_fail - lo_fail) < (hi_fixed - lo_fixed)

    def test_three_modes_coverage_ordering(self):
        # fixed covers more than failures/intersect in the demo scenario
        from physics.substrate_scope_validator import validate
        axes_grid = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}

        env_fixed, _ = envelope_fixed(_spec())
        env_fail, _ = envelope_from_failures(_logs(), _axes())
        env_int, _ = envelope_intersect(_spec(), _logs(), _axes())

        cov_fixed = validate(task, env_fixed, axes_grid)["coverage_frac"]
        cov_fail = validate(task, env_fail, axes_grid)["coverage_frac"]
        cov_int = validate(task, env_int, axes_grid)["coverage_frac"]

        assert cov_fixed > cov_fail   # spec wider than observed
        assert cov_int == pytest.approx(cov_fail)  # obs ⊂ spec → same

    def test_fixed_coverage_approx(self):
        from physics.substrate_scope_validator import validate
        axes_grid = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env, _ = envelope_fixed(_spec())
        out = validate(task, env, axes_grid)
        assert out["coverage_frac"] == pytest.approx(0.480, abs=0.01)

    def test_failures_coverage_approx(self):
        from physics.substrate_scope_validator import validate
        axes_grid = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env, _ = envelope_from_failures(_logs(), _axes())
        out = validate(task, env, axes_grid)
        assert out["coverage_frac"] == pytest.approx(0.160, abs=0.01)
