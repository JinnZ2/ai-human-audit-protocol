"""Unit tests for physics/reference_frame_drift.py.

Claim: the reference frame is dynamic — sensors fail, knowledge goes stale,
hardware degrades. drift = located() falling while stated capability holds.
That is the broken-thermostat failure: maximising output against a reference
that has quietly moved.

Tests verify: trace_drift() row shape, located/gap computation, delta
arithmetic, runaway flag logic (thresholds and boundary conditions), summary()
keys and formulas, the diverging flag, and demo scenario quantitative values.

Note: reference_frame_drift imports `from reference_frame import ...` as a
bare sibling import. conftest.py adds physics/ to sys.path so pytest can
resolve it without modifying the CC0 source.
"""

import pytest

from physics.reference_frame_drift import summary, trace_drift


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _snap(t, physical=0.5, temporal=0.5, energetic=0.5,
          informational=0.5, epistemic=0.5, stated=0.5, observed=0.5):
    return {
        "t": t,
        "observables": {"physical": physical, "temporal": temporal,
                        "energetic": energetic, "informational": informational,
                        "epistemic": epistemic},
        "stated": stated,
        "observed": observed,
    }


def _demo_snaps():
    return [
        {"t": 0, "observables": {"physical": 0.8, "temporal": 0.7, "energetic": 0.8,
                                 "informational": 0.8, "epistemic": 0.7},
         "stated": 0.85, "observed": 0.80},
        {"t": 1, "observables": {"physical": 0.6, "temporal": 0.6, "energetic": 0.7,
                                 "informational": 0.7, "epistemic": 0.6},
         "stated": 0.86, "observed": 0.72},
        {"t": 2, "observables": {"physical": 0.4, "temporal": 0.5, "energetic": 0.5,
                                 "informational": 0.6, "epistemic": 0.4},
         "stated": 0.87, "observed": 0.61},
        {"t": 3, "observables": {"physical": 0.2, "temporal": 0.3, "energetic": 0.4,
                                 "informational": 0.5, "epistemic": 0.3},
         "stated": 0.88, "observed": 0.50},
    ]


# ---------------------------------------------------------------------------
# trace_drift() — shape and structural contracts
# ---------------------------------------------------------------------------

class TestTraceDriftShape:
    def test_returns_list(self):
        assert isinstance(trace_drift([_snap(0)]), list)

    def test_length_matches_input(self):
        snaps = [_snap(i) for i in range(4)]
        assert len(trace_drift(snaps)) == 4

    def test_single_snapshot_returns_one_row(self):
        assert len(trace_drift([_snap(0)])) == 1

    def test_each_row_has_required_keys(self):
        rows = trace_drift([_snap(0), _snap(1)])
        for r in rows:
            for k in ("t", "located", "stated", "observed",
                      "narrative_gap", "located_delta", "stated_delta", "runaway"):
                assert k in r

    def test_t_values_stored(self):
        snaps = [_snap(5), _snap(10), _snap(15)]
        rows = trace_drift(snaps)
        assert [r["t"] for r in rows] == [5, 10, 15]

    def test_stated_and_observed_stored(self):
        rows = trace_drift([_snap(0, stated=0.7, observed=0.4)])
        assert rows[0]["stated"] == pytest.approx(0.7)
        assert rows[0]["observed"] == pytest.approx(0.4)


# ---------------------------------------------------------------------------
# trace_drift() — located and gap computation
# ---------------------------------------------------------------------------

class TestTraceDriftValues:
    def test_located_is_mean_of_observables(self):
        # all axes = 0.6 → located = 0.6
        rows = trace_drift([_snap(0, physical=0.6, temporal=0.6, energetic=0.6,
                                  informational=0.6, epistemic=0.6)])
        assert rows[0]["located"] == pytest.approx(0.6)

    def test_located_with_mixed_values(self):
        # (0.2+0.4+0.6+0.8+1.0)/5 = 3.0/5 = 0.6
        rows = trace_drift([_snap(0, physical=0.2, temporal=0.4, energetic=0.6,
                                  informational=0.8, epistemic=1.0)])
        assert rows[0]["located"] == pytest.approx(0.6)

    def test_narrative_gap_stated_minus_observed(self):
        rows = trace_drift([_snap(0, stated=0.9, observed=0.5)])
        assert rows[0]["narrative_gap"] == pytest.approx(0.4)

    def test_narrative_gap_can_be_negative(self):
        rows = trace_drift([_snap(0, stated=0.4, observed=0.8)])
        assert rows[0]["narrative_gap"] == pytest.approx(-0.4)

    def test_narrative_gap_zero_when_equal(self):
        rows = trace_drift([_snap(0, stated=0.5, observed=0.5)])
        assert rows[0]["narrative_gap"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# trace_drift() — delta arithmetic
# ---------------------------------------------------------------------------

class TestTraceDriftDeltas:
    def test_first_row_located_delta_zero(self):
        rows = trace_drift([_snap(0)])
        assert rows[0]["located_delta"] == pytest.approx(0.0)

    def test_first_row_stated_delta_zero(self):
        rows = trace_drift([_snap(0)])
        assert rows[0]["stated_delta"] == pytest.approx(0.0)

    def test_located_delta_is_current_minus_previous(self):
        # row0: all=0.8 → located=0.8; row1: all=0.4 → located=0.4
        snaps = [
            _snap(0, physical=0.8, temporal=0.8, energetic=0.8,
                  informational=0.8, epistemic=0.8),
            _snap(1, physical=0.4, temporal=0.4, energetic=0.4,
                  informational=0.4, epistemic=0.4),
        ]
        rows = trace_drift(snaps)
        assert rows[1]["located_delta"] == pytest.approx(0.4 - 0.8, abs=1e-4)

    def test_stated_delta_is_current_minus_previous(self):
        snaps = [_snap(0, stated=0.5), _snap(1, stated=0.8)]
        rows = trace_drift(snaps)
        assert rows[1]["stated_delta"] == pytest.approx(0.3, abs=1e-4)

    def test_located_delta_rounded(self):
        snaps = [_snap(0, physical=1.0), _snap(1, physical=0.0)]
        rows = trace_drift(snaps)
        val = rows[1]["located_delta"]
        assert val == round(val, 4)

    def test_positive_located_delta_when_frame_improves(self):
        snaps = [
            _snap(0, physical=0.2, temporal=0.2, energetic=0.2,
                  informational=0.2, epistemic=0.2),
            _snap(1, physical=0.8, temporal=0.8, energetic=0.8,
                  informational=0.8, epistemic=0.8),
        ]
        rows = trace_drift(snaps)
        assert rows[1]["located_delta"] > 0


# ---------------------------------------------------------------------------
# trace_drift() — runaway flag
# ---------------------------------------------------------------------------

class TestTraceDriftRunaway:
    def _two_snaps(self, obs0, obs1, stated0, stated1):
        return trace_drift([
            {"t": 0, "observables": {ax: obs0 for ax in
             ("physical", "temporal", "energetic", "informational", "epistemic")},
             "stated": stated0, "observed": 0.5},
            {"t": 1, "observables": {ax: obs1 for ax in
             ("physical", "temporal", "energetic", "informational", "epistemic")},
             "stated": stated1, "observed": 0.5},
        ])

    def test_first_row_never_runaway(self):
        rows = trace_drift([_snap(0)])
        assert rows[0]["runaway"] is False

    def test_runaway_true_when_both_conditions_met(self):
        # located drops: 0.8 → 0.4 (delta=-0.4 < -0.02); stated stable (delta=0)
        rows = self._two_snaps(0.8, 0.4, 0.9, 0.9)
        assert rows[1]["runaway"] is True

    def test_runaway_false_when_located_delta_at_threshold(self):
        # located drops by exactly 0.02: delta=-0.02 NOT < -0.02 → False
        # obs0=0.8, obs1=0.7: located drops 0.8-0.7=0.1? No wait, located=mean(all).
        # I need a drop of exactly 0.02 in located.
        # located0=0.8 (all axes=0.8), located1=0.7 (delta=-0.1 — that's too big)
        # Let me design: only physical changes.
        # located = (physical + 0.5*4)/5 = (physical + 2) / 5
        # delta(located) = delta(physical)/5
        # I need delta(located)=-0.02 → delta(physical)=-0.1 → physical: 0.7 → 0.6
        rows = trace_drift([
            {"t": 0, "observables": {"physical": 0.7, "temporal": 0.5,
             "energetic": 0.5, "informational": 0.5, "epistemic": 0.5},
             "stated": 0.5, "observed": 0.5},
            {"t": 1, "observables": {"physical": 0.6, "temporal": 0.5,
             "energetic": 0.5, "informational": 0.5, "epistemic": 0.5},
             "stated": 0.5, "observed": 0.5},
        ])
        assert rows[1]["located_delta"] == pytest.approx(-0.02, abs=1e-4)
        assert rows[1]["runaway"] is False  # NOT strictly < -0.02

    def test_runaway_false_when_stated_drops_below_threshold(self):
        # located drops a lot, but stated also drops (stated_delta < -0.01 → False)
        rows = self._two_snaps(0.8, 0.2, 0.9, 0.87)  # stated_delta=-0.03
        assert rows[1]["stated_delta"] < -0.01
        assert rows[1]["runaway"] is False

    def test_runaway_true_when_stated_delta_at_threshold(self):
        # stated_delta = -0.01 → >= -0.01 → stated condition True
        rows = self._two_snaps(0.9, 0.5, 0.91, 0.90)  # stated_delta=-0.01
        assert rows[1]["stated_delta"] == pytest.approx(-0.01, abs=1e-4)
        assert rows[1]["runaway"] is True  # located drops big, stated_delta = -0.01

    def test_runaway_false_when_frame_stable(self):
        # no location change → delta=0 → not < -0.02 → False
        rows = self._two_snaps(0.5, 0.5, 0.5, 0.5)
        assert rows[1]["runaway"] is False

    def test_multiple_runaway_steps(self):
        # three consecutive runaway steps
        rows = trace_drift(_demo_snaps())
        runaway_count = sum(1 for r in rows if r["runaway"])
        assert runaway_count == 3  # t=1,2,3

    def test_runaway_field_is_bool(self):
        rows = trace_drift([_snap(0), _snap(1)])
        for r in rows:
            assert isinstance(r["runaway"], bool)


# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------

class TestSummary:
    def _flat_rows(self, n=3, located=0.5, gap=0.0):
        return [{"t": i, "located": located, "narrative_gap": gap, "runaway": False}
                for i in range(n)]

    def test_returns_dict(self):
        assert isinstance(summary(self._flat_rows()), dict)

    def test_required_keys(self):
        out = summary(self._flat_rows())
        for k in ("located_drift", "narrative_gap_change",
                  "runaway_timesteps", "diverging"):
            assert k in out

    def test_located_drift_is_last_minus_first(self):
        rows = [{"t": 0, "located": 0.8, "narrative_gap": 0.0, "runaway": False},
                {"t": 1, "located": 0.5, "narrative_gap": 0.0, "runaway": False}]
        out = summary(rows)
        assert out["located_drift"] == pytest.approx(-0.3, abs=1e-4)

    def test_narrative_gap_change_is_last_minus_first(self):
        rows = [{"t": 0, "located": 0.5, "narrative_gap": 0.05, "runaway": False},
                {"t": 1, "located": 0.5, "narrative_gap": 0.38, "runaway": False}]
        out = summary(rows)
        assert out["narrative_gap_change"] == pytest.approx(0.33, abs=1e-4)

    def test_located_drift_rounded_to_4dp(self):
        rows = [{"t": 0, "located": 1/3, "narrative_gap": 0.0, "runaway": False},
                {"t": 1, "located": 0.0, "narrative_gap": 0.0, "runaway": False}]
        val = summary(rows)["located_drift"]
        assert val == round(val, 4)

    def test_runaway_timesteps_collects_t_values(self):
        rows = [
            {"t": 0, "located": 0.8, "narrative_gap": 0.0, "runaway": False},
            {"t": 1, "located": 0.5, "narrative_gap": 0.1, "runaway": True},
            {"t": 2, "located": 0.3, "narrative_gap": 0.2, "runaway": True},
        ]
        assert summary(rows)["runaway_timesteps"] == [1, 2]

    def test_runaway_timesteps_empty_when_none(self):
        assert summary(self._flat_rows())["runaway_timesteps"] == []

    def test_diverging_true_when_drift_negative_and_gap_positive(self):
        rows = [{"t": 0, "located": 0.8, "narrative_gap": 0.05, "runaway": True},
                {"t": 1, "located": 0.3, "narrative_gap": 0.38, "runaway": True}]
        assert summary(rows)["diverging"] is True

    def test_diverging_false_when_drift_nonnegative(self):
        rows = [{"t": 0, "located": 0.3, "narrative_gap": 0.0, "runaway": False},
                {"t": 1, "located": 0.8, "narrative_gap": 0.1, "runaway": False}]
        assert summary(rows)["diverging"] is False

    def test_diverging_false_when_gap_nonpositive(self):
        rows = [{"t": 0, "located": 0.8, "narrative_gap": 0.3, "runaway": True},
                {"t": 1, "located": 0.2, "narrative_gap": 0.2, "runaway": True}]
        assert summary(rows)["diverging"] is False

    def test_diverging_false_when_both_improving(self):
        rows = [{"t": 0, "located": 0.3, "narrative_gap": 0.5, "runaway": False},
                {"t": 1, "located": 0.8, "narrative_gap": 0.1, "runaway": False}]
        assert summary(rows)["diverging"] is False

    def test_empty_rows_returns_safe_defaults(self):
        # empty list must not raise IndexError (rows[-1] guard)
        out = summary([])
        assert out["located_drift"] == pytest.approx(0.0)
        assert out["narrative_gap_change"] == pytest.approx(0.0)
        assert out["runaway_timesteps"] == []
        assert out["diverging"] is False


# ---------------------------------------------------------------------------
# Demo scenario — quantitative predictions
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _rows(self):
        return trace_drift(_demo_snaps())

    def _sum(self):
        return summary(self._rows())

    def test_t0_located(self):
        # (0.8+0.7+0.8+0.8+0.7)/5 = 3.8/5 = 0.76
        assert self._rows()[0]["located"] == pytest.approx(0.76)

    def test_t1_located(self):
        # (0.6+0.6+0.7+0.7+0.6)/5 = 3.2/5 = 0.64
        assert self._rows()[1]["located"] == pytest.approx(0.64)

    def test_t2_located(self):
        # (0.4+0.5+0.5+0.6+0.4)/5 = 2.4/5 = 0.48
        assert self._rows()[2]["located"] == pytest.approx(0.48)

    def test_t3_located(self):
        # (0.2+0.3+0.4+0.5+0.3)/5 = 1.7/5 = 0.34
        assert self._rows()[3]["located"] == pytest.approx(0.34)

    def test_t0_narrative_gap(self):
        assert self._rows()[0]["narrative_gap"] == pytest.approx(0.05)

    def test_t3_narrative_gap(self):
        assert self._rows()[3]["narrative_gap"] == pytest.approx(0.38)

    def test_runaway_at_t1_t2_t3(self):
        rows = self._rows()
        assert rows[0]["runaway"] is False
        assert rows[1]["runaway"] is True
        assert rows[2]["runaway"] is True
        assert rows[3]["runaway"] is True

    def test_summary_located_drift(self):
        assert self._sum()["located_drift"] == pytest.approx(-0.42, abs=1e-4)

    def test_summary_gap_change(self):
        assert self._sum()["narrative_gap_change"] == pytest.approx(0.33, abs=1e-4)

    def test_summary_runaway_timesteps(self):
        assert self._sum()["runaway_timesteps"] == [1, 2, 3]

    def test_summary_diverging(self):
        assert self._sum()["diverging"] is True
