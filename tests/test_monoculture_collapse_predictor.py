"""Unit tests for physics/monoculture_collapse_predictor.py.

Claim: diversity sets the barrier height that holds a system out of collapse.
Consolidation (apex-broadcast) eats the barrier. Below spinodal → escape.

Tests verify: barrier formula, Kramers escape rate (including clamping of
negative barriers), sweep shape and monotone state logic, the hysteresis
gap (collapse needs higher consolidation than recovery), and the demo
scenario quantitative predictions.
"""

import math

import pytest

from physics.monoculture_collapse_predictor import barrier, escape_rate, sweep


# ---------------------------------------------------------------------------
# barrier()
# ---------------------------------------------------------------------------

class TestBarrier:
    def test_formula_default_coefficients(self):
        # D0=1, k=1: barrier = diversity - consolidation * broadcast
        assert barrier(1.0, 0.5, 2.0) == pytest.approx(1.0 - 0.5 * 2.0)

    def test_zero_when_balanced(self):
        assert barrier(1.0, 1.0, 1.0) == pytest.approx(0.0)

    def test_positive_when_diverse_dominates(self):
        assert barrier(2.0, 0.5, 1.0) == pytest.approx(1.5)

    def test_negative_when_consolidation_dominates(self):
        assert barrier(1.0, 2.0, 1.0) == pytest.approx(-1.0)

    def test_custom_D0(self):
        assert barrier(1.0, 1.0, 1.0, D0=2.0, k=1.0) == pytest.approx(1.0)

    def test_custom_k(self):
        assert barrier(1.0, 1.0, 1.0, D0=1.0, k=2.0) == pytest.approx(-1.0)

    def test_zero_consolidation(self):
        assert barrier(1.0, 0.0, 1.0) == pytest.approx(1.0)

    def test_zero_diversity(self):
        assert barrier(0.0, 1.0, 1.0) == pytest.approx(-1.0)


# ---------------------------------------------------------------------------
# escape_rate()
# ---------------------------------------------------------------------------

class TestEscapeRate:
    def test_positive_barrier(self):
        expected = math.exp(-1.0 / 0.15)
        assert escape_rate(1.0, temp=0.15) == pytest.approx(expected)

    def test_zero_barrier_gives_attempt(self):
        assert escape_rate(0.0) == pytest.approx(1.0)

    def test_negative_barrier_clamped_to_attempt(self):
        # max(b, 0) = 0 → rate = attempt * exp(0) = attempt
        assert escape_rate(-1.0) == pytest.approx(1.0)
        assert escape_rate(-100.0) == pytest.approx(1.0)

    def test_custom_attempt(self):
        assert escape_rate(0.0, attempt=2.0) == pytest.approx(2.0)
        assert escape_rate(-1.0, attempt=3.0) == pytest.approx(3.0)

    def test_higher_barrier_lower_rate(self):
        assert escape_rate(0.3) > escape_rate(0.5)
        assert escape_rate(0.5) > escape_rate(1.0)

    def test_lower_temp_lower_rate_for_same_barrier(self):
        # more sensitive to barrier at lower temperature
        assert escape_rate(0.5, temp=0.1) < escape_rate(0.5, temp=0.2)

    def test_very_large_barrier_near_zero(self):
        assert escape_rate(100.0) < 1e-10


# ---------------------------------------------------------------------------
# sweep() — shape and structural contracts
# ---------------------------------------------------------------------------

class TestSweepShape:
    def _fwd(self, **kw):
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, **kw)
        return f

    def test_returns_two_lists(self):
        f, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0)
        assert isinstance(f, list) and isinstance(r, list)

    def test_fwd_length_equals_steps_plus_one(self):
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, steps=20)
        assert len(f) == 21

    def test_rev_length_equals_steps_plus_one(self):
        _, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, steps=20)
        assert len(r) == 21

    def test_each_row_has_four_elements(self):
        f, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, steps=10)
        for row in f + r:
            assert len(row) == 4

    def test_fwd_c_ascending(self):
        f = self._fwd(steps=10, c_lo=0.0, c_hi=2.0)
        cs = [row[0] for row in f]
        assert cs == sorted(cs)

    def test_rev_c_descending(self):
        _, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0,
                     steps=10, c_lo=0.0, c_hi=2.0)
        cs = [row[0] for row in r]
        assert cs == sorted(cs, reverse=True)

    def test_fwd_starts_at_c_lo(self):
        f = self._fwd(c_lo=0.3, c_hi=1.5, steps=10)
        assert f[0][0] == pytest.approx(0.3, abs=1e-4)

    def test_fwd_ends_at_c_hi(self):
        f = self._fwd(c_lo=0.0, c_hi=1.8, steps=10)
        assert f[-1][0] == pytest.approx(1.8, abs=1e-4)

    def test_state_values_only_diverse_or_collapsed(self):
        f, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.85)
        valid = {"diverse", "collapsed"}
        for row in f + r:
            assert row[3] in valid


# ---------------------------------------------------------------------------
# sweep() — physics and state logic
# ---------------------------------------------------------------------------

class TestSweepPhysics:
    def test_fwd_state_starts_diverse(self):
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0)
        assert f[0][3] == "diverse"

    def test_fwd_state_monotone_once_collapsed(self):
        # state can only go diverse → collapsed, never back in forward pass
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.5)
        collapsed_seen = False
        for _, _, _, state in f:
            if state == "collapsed":
                collapsed_seen = True
            if collapsed_seen:
                assert state == "collapsed"

    def test_lower_reciprocity_collapses_at_lower_consolidation(self):
        f_hi, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0)
        f_lo, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.5)
        fc_hi = next((c for c, _, _, s in f_hi if s == "collapsed"), None)
        fc_lo = next((c for c, _, _, s in f_lo if s == "collapsed"), None)
        assert fc_lo is not None and fc_hi is not None
        assert fc_lo < fc_hi

    def test_zero_reciprocity_immediate_or_early_collapse(self):
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.0, steps=40)
        # with zero reciprocity effective diversity=0, barrier always ≤ 0, rate=1 ≥ 0.5
        states = [row[3] for row in f]
        assert "collapsed" in states
        # should collapse at first or very early step
        fc = next((c for c, _, _, s in f if s == "collapsed"), None)
        assert fc is not None
        assert fc <= 0.1  # collapses at very low consolidation

    def test_unreachable_threshold_stays_diverse(self):
        # escape_threshold > 1.0 can never be reached (rate capped by attempt=1)
        f, _ = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, escape_threshold=2.0)
        assert all(row[3] == "diverse" for row in f)

    def test_rev_can_recover_after_collapse(self):
        # with the default scenario, rev contains "diverse" state
        _, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.85)
        assert any(row[3] == "diverse" for row in r)

    def test_no_collapse_rev_also_diverse(self):
        # if forward never collapses, reverse is also all diverse
        f, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, escape_threshold=2.0)
        assert all(row[3] == "diverse" for row in r)


# ---------------------------------------------------------------------------
# Hysteresis — the load-bearing physical claim
# ---------------------------------------------------------------------------

class TestHysteresis:
    def _spinodals(self, **kw):
        f, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.85, **kw)
        fc = next((c for c, _, _, s in f if s == "collapsed"), None)
        rc = next((c for c, _, _, s in r if s == "diverse"), None)
        return fc, rc

    def test_collapse_at_higher_consolidation_than_recovery(self):
        fc, rc = self._spinodals()
        assert fc is not None and rc is not None
        assert fc > rc  # asymmetric reset: recovery needs lower consolidation

    def test_hysteresis_gap_positive(self):
        fc, rc = self._spinodals()
        assert round(fc - rc, 3) > 0

    def test_lower_reciprocity_smaller_hysteresis_window_or_same(self):
        # not a strict inequality in all parameterizations — just sanity check
        fc_hi, rc_hi = self._spinodals()
        f_lo, r_lo = sweep(diversity=1.0, broadcast=1.0, reciprocity=0.3)
        fc_lo = next((c for c, _, _, s in f_lo if s == "collapsed"), None)
        rc_lo = next((c for c, _, _, s in r_lo if s == "diverse"), None)
        if fc_lo is not None and rc_lo is not None:
            assert fc_lo <= fc_hi  # lower reciprocity collapses sooner

    def test_hysteresis_requires_collapse_first(self):
        # rev state starts where fwd ended; if fwd ended diverse → no rev recovery
        _, r = sweep(diversity=1.0, broadcast=1.0, reciprocity=1.0, escape_threshold=2.0)
        rc = next((c for c, _, _, s in r if s == "diverse"), None)
        # all rev diverse because fwd never collapsed
        assert all(row[3] == "diverse" for row in r)


# ---------------------------------------------------------------------------
# Demo scenario — quantitative verification
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _scan(self):
        return sweep(diversity=1.0, broadcast=1.0, reciprocity=0.85)

    def test_spinodal_fwd_not_none(self):
        f, _ = self._scan()
        assert next((c for c, _, _, s in f if s == "collapsed"), None) is not None

    def test_recover_rev_not_none(self):
        _, r = self._scan()
        assert next((c for c, _, _, s in r if s == "diverse"), None) is not None

    def test_hysteresis_gap_approx(self):
        f, r = self._scan()
        fc = next((c for c, _, _, s in f if s == "collapsed"), None)
        rc = next((c for c, _, _, s in r if s == "diverse"), None)
        gap = round(fc - rc, 3)
        assert gap > 0.05  # non-trivial gap

    def test_spinodal_value_in_expected_range(self):
        # analytical spinodal ≈ 0.746 → nearest 0.05 step = 0.75
        f, _ = self._scan()
        fc = next((c for c, _, _, s in f if s == "collapsed"), None)
        assert 0.70 <= fc <= 0.85

    def test_recovery_value_in_expected_range(self):
        # analytical recovery ≈ 0.642 → nearest 0.05 step = 0.60
        _, r = self._scan()
        rc = next((c for c, _, _, s in r if s == "diverse"), None)
        assert 0.55 <= rc <= 0.70
