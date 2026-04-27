"""Unit tests for consortium/kfc_runtime.py.

KFC is differential relation compute: bounded claims, bounds-overlap
coupling, cyc-stratified integration, FELT coherence sensor. These
tests cover the public surface plus the soil-graph demo as a smoke
test.
"""

import math

import pytest

from consortium.kfc_runtime import (
    ClaimNode,
    CYC_DT,
    bounds_overlap,
    _scope_overlap,
    should_activate,
    _within,
    step,
    felt_sensor,
    query,
    build_soil_graph,
)


def _node(id="n", rate_fn=None, bounds=None, cond=None, rel=None,
          fail=None, meas=None, cyc=1, state=0.0, active=False):
    return ClaimNode(
        id=id,
        rate_fn=rate_fn or (lambda s, rel, ctx: 0.0),
        bounds=bounds or ("S", "T", "Z"),
        cond=cond or [],
        rel=rel or [],
        fail=fail or [],
        meas=meas or [],
        cyc=cyc,
        state=state,
        active=active,
    )


# ------------------------------------------------------------
# CYC_DT — timescale stratification
# ------------------------------------------------------------

class TestCycDt:
    def test_three_timescales_present(self):
        assert set(CYC_DT.keys()) == {0, 1, 2}

    def test_transient_smaller_than_seasonal(self):
        assert CYC_DT[0] < CYC_DT[1]

    def test_seasonal_smaller_than_generational(self):
        assert CYC_DT[1] < CYC_DT[2]


# ------------------------------------------------------------
# _scope_overlap and bounds_overlap
# ------------------------------------------------------------

class TestScopeOverlap:
    def test_returns_one_when_query_is_none(self):
        assert _scope_overlap("ABC", "DEF", None) == 1.0

    def test_returns_one_when_query_in_both(self):
        assert _scope_overlap("ABC", "ABCD", "B") == 1.0

    def test_returns_zero_when_query_in_one_only(self):
        assert _scope_overlap("ABC", "DEF", "A") == 0.0

    def test_returns_zero_when_query_in_neither(self):
        assert _scope_overlap("ABC", "DEF", "Z") == 0.0


class TestBoundsOverlap:
    def test_full_overlap_when_no_query_dims(self):
        a = ("X", "Y", "Z")
        b = ("X", "Y", "Z")
        assert bounds_overlap(a, b, {}) == 1.0

    def test_zero_when_any_dim_misses(self):
        a = ("X", "Y", "Z")
        b = ("X", "Y", "W")
        ctx = {"space": "X", "time": "Y", "scale": "Z"}
        # scale "Z" not in "W" → 0
        assert bounds_overlap(a, b, ctx) == 0.0

    def test_full_when_all_dims_overlap(self):
        a = ("ABC", "DEF", "GHI")
        b = ("AB", "DE", "GH")
        ctx = {"space": "A", "time": "D", "scale": "G"}
        assert bounds_overlap(a, b, ctx) == 1.0


# ------------------------------------------------------------
# _within and should_activate
# ------------------------------------------------------------

class TestWithin:
    def test_activates_when_all_dims_match(self):
        bounds = ("ABC", "DEF", "GHI")
        ctx = {"space": "A", "time": "D", "scale": "G"}
        assert _within(ctx, bounds)

    def test_skips_dims_with_none_in_ctx(self):
        bounds = ("ABC", "DEF", "GHI")
        ctx = {"space": "A"}  # only space provided
        assert _within(ctx, bounds)

    def test_fails_when_dim_missed(self):
        bounds = ("ABC", "DEF", "GHI")
        ctx = {"space": "Z"}
        assert not _within(ctx, bounds)


class TestShouldActivate:
    def test_activates_when_within_no_fail_all_cond(self):
        n = _node(bounds=("X", "Y", "Z"))
        ctx = {"space": "X"}
        assert should_activate(n, ctx)

    def test_does_not_activate_outside_bounds(self):
        n = _node(bounds=("X", "Y", "Z"))
        ctx = {"space": "OUTSIDE"}
        assert not should_activate(n, ctx)

    def test_fail_blocks_activation(self):
        n = _node(fail=[lambda ctx: True])
        assert not should_activate(n, {})

    def test_unmet_cond_blocks_activation(self):
        n = _node(cond=[lambda ctx: False])
        assert not should_activate(n, {})

    def test_all_conds_must_pass(self):
        n = _node(cond=[lambda ctx: True, lambda ctx: False])
        assert not should_activate(n, {})


# ------------------------------------------------------------
# step
# ------------------------------------------------------------

class TestStep:
    def test_inactive_node_does_not_change(self):
        n = _node(rate_fn=lambda s, rel, ctx: 1.0, state=5.0, active=False)
        graph = {"n": n}
        step(graph, {})
        assert n.state == 5.0
        assert n.history == []

    def test_active_node_integrates(self):
        # rate = 1.0, cyc=1 (dt=1.0), no rel → weight=1
        n = _node(rate_fn=lambda s, rel, ctx: 1.0, cyc=1,
                  state=0.0, active=True)
        graph = {"n": n}
        step(graph, {})
        assert n.state == pytest.approx(1.0)
        assert n.history == [pytest.approx(1.0)]

    def test_history_accumulates(self):
        n = _node(rate_fn=lambda s, rel, ctx: 1.0, cyc=1, active=True)
        graph = {"n": n}
        for _ in range(3):
            step(graph, {})
        assert len(n.history) == 3

    def test_cyc_dt_scales_step_size(self):
        # transient (cyc=0) integrates in tiny steps
        n = _node(rate_fn=lambda s, rel, ctx: 1.0, cyc=0, active=True)
        graph = {"n": n}
        step(graph, {})
        assert n.state == pytest.approx(CYC_DT[0])


# ------------------------------------------------------------
# felt_sensor
# ------------------------------------------------------------

class TestFeltSensor:
    def test_empty_returns_none(self):
        assert felt_sensor({}) is None

    def test_no_history_returns_none(self):
        # all claims have <= 1 history entry → drift = 0 → coherence = 1
        n = _node()
        n.history = [0.0]
        assert felt_sensor({"n": n}) is None

    def test_low_drift_returns_none(self):
        n = _node()
        n.history = [0.0, 0.01, 0.02]
        result = felt_sensor({"n": n})
        # coherence ≈ exp(-0.02) ≈ 0.98 → above default threshold
        assert result is None

    def test_high_drift_triggers_warning(self):
        n = _node()
        n.history = [0.0, 100.0]   # huge drift → coherence ≈ 0
        result = felt_sensor({"n": n})
        assert result is not None
        assert "FELT_TRIGGER" in result
        assert "recalibrate" in result

    def test_threshold_override(self):
        n = _node()
        n.history = [0.0, 0.5]    # mild drift
        # default threshold 0.35; coherence = exp(-0.5) ≈ 0.61 → above
        assert felt_sensor({"n": n}) is None
        # bump threshold to 0.7 → now 0.61 falls below → trigger
        result = felt_sensor({"n": n}, threshold=0.7)
        assert result is not None


# ------------------------------------------------------------
# query
# ------------------------------------------------------------

class TestQuery:
    def test_returns_observe_keys(self):
        # build a graph that activates and runs
        n = _node(id="a", rate_fn=lambda s, rel, ctx: 1.0,
                  bounds=("X", "Y", "Z"), cyc=1)
        graph = {"a": n}
        ctx = {"space": "X", "time": "Y", "scale": "Z"}
        traj = query(graph, ctx, duration=3.0, observe=["a"])
        assert "a" in traj

    def test_n_steps_proportional_to_duration(self):
        n = _node(id="a", rate_fn=lambda s, rel, ctx: 1.0,
                  bounds=("X", "Y", "Z"), cyc=1)  # dt=1.0
        graph = {"a": n}
        ctx = {"space": "X", "time": "Y", "scale": "Z"}
        traj = query(graph, ctx, duration=5.0, observe=["a"])
        assert len(traj["a"]) == 5

    def test_unobserved_id_returns_zero_default(self):
        # observing an id not in the graph fills with 0.0
        n = _node(id="a", rate_fn=lambda s, rel, ctx: 1.0,
                  bounds=("X", "Y", "Z"), cyc=1)
        graph = {"a": n}
        ctx = {"space": "X", "time": "Y", "scale": "Z"}
        traj = query(graph, ctx, duration=3.0, observe=["nonexistent"])
        assert traj["nonexistent"] == [0.0, 0.0, 0.0]

    def test_history_is_cleared_at_start(self):
        n = _node(id="a", rate_fn=lambda s, rel, ctx: 1.0,
                  bounds=("X", "Y", "Z"), cyc=1)
        n.history = [99.0, 99.0]   # pre-existing junk
        graph = {"a": n}
        ctx = {"space": "X", "time": "Y", "scale": "Z"}
        query(graph, ctx, duration=2.0, observe=["a"])
        # history rebuilt from scratch
        assert n.history[0] != 99.0


# ------------------------------------------------------------
# Soil graph demo as smoke test
# ------------------------------------------------------------

class TestSoilGraphDemo:
    def test_demo_constructs(self):
        g = build_soil_graph()
        assert {"mulch_h2o", "mycorr", "albedo"} <= set(g.keys())

    def test_each_node_has_rate_fn(self):
        g = build_soil_graph()
        for node in g.values():
            assert callable(node.rate_fn)

    def test_each_node_has_bounds(self):
        g = build_soil_graph()
        for node in g.values():
            assert len(node.bounds) == 3
