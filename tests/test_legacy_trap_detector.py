"""Unit tests for physics/legacy_trap_detector.py.

Claim: a system splitting energy between maintain (fixed config) and adapt
(track gradient) diverges from its environment when maintenance stays locked
while the environment drifts. Higher maintain_frac → larger steady-state
deficit. The optics() layer is separable from the structural trace.

Tests verify: step() mechanics (full/zero adaptation, custom params), run()
shape and env-drift logic, the maintain_frac → deficit monotonicity, and
optics() output shape and correctness.
"""

import pytest

from physics.legacy_trap_detector import optics, run, step


# ---------------------------------------------------------------------------
# step()
# ---------------------------------------------------------------------------

class TestStep:
    def test_full_adaptation_zeroes_deficit(self):
        # maintain_frac=0 → adapt_budget=1, pull = env - config → config_next = env
        config_next, deficit = step(config=0.0, env=1.0, maintain_frac=0.0)
        assert config_next == pytest.approx(1.0)
        assert deficit == pytest.approx(0.0)

    def test_zero_adaptation_config_unchanged(self):
        # maintain_frac=1 → adapt_budget=0, pull=0 → config unchanged
        config_next, deficit = step(config=0.0, env=1.0, maintain_frac=1.0)
        assert config_next == pytest.approx(0.0)
        assert deficit == pytest.approx(1.0)

    def test_partial_adaptation(self):
        # maintain_frac=0.5, energy=1, k=1:
        # adapt_budget=0.5, pull=0.5*(env-config)=0.5, config_next=0.5
        config_next, deficit = step(config=0.0, env=1.0, maintain_frac=0.5)
        assert config_next == pytest.approx(0.5)
        assert deficit == pytest.approx(0.5)

    def test_deficit_is_nonnegative(self):
        for mf in (0.0, 0.3, 0.7, 1.0):
            _, deficit = step(0.0, 1.0, mf)
            assert deficit >= 0.0

    def test_custom_energy(self):
        # energy=2.0, maintain_frac=0.5 → adapt_budget=1.0 → pull=1.0*(1.0-0.0)=1.0
        config_next, deficit = step(config=0.0, env=1.0, maintain_frac=0.5, energy=2.0)
        assert config_next == pytest.approx(1.0)
        assert deficit == pytest.approx(0.0)

    def test_custom_k_adapt(self):
        # k_adapt=0.5, maintain_frac=0 → pull=0.5*1*(1-0)=0.5
        config_next, deficit = step(config=0.0, env=1.0, maintain_frac=0.0, k_adapt=0.5)
        assert config_next == pytest.approx(0.5)
        assert deficit == pytest.approx(0.5)

    def test_no_gap_gives_zero_deficit(self):
        # env == config: no pull needed
        config_next, deficit = step(config=5.0, env=5.0, maintain_frac=0.5)
        assert deficit == pytest.approx(0.0)

    def test_returns_tuple_of_two(self):
        result = step(0.0, 1.0, 0.5)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# run()
# ---------------------------------------------------------------------------

class TestRun:
    def test_returns_list_of_length_T(self):
        trace = run(maintain_frac=0.5, T=10)
        assert len(trace) == 10

    def test_default_T(self):
        trace = run(maintain_frac=0.5)
        assert len(trace) == 40

    def test_each_row_has_five_elements(self):
        trace = run(maintain_frac=0.5, T=5)
        for row in trace:
            assert len(row) == 5

    def test_step_indices_zero_based(self):
        trace = run(maintain_frac=0.5, T=5)
        for i, row in enumerate(trace):
            assert row[0] == i

    def test_env_increases_by_drift_rate(self):
        drift = 0.05
        trace = run(maintain_frac=0.5, env_drift_rate=drift, T=5)
        for i, row in enumerate(trace):
            expected_env = (i + 1) * drift
            assert row[1] == pytest.approx(expected_env, abs=1e-4)

    def test_maintain_frac_stored_in_trace(self):
        trace = run(maintain_frac=0.7, T=3)
        for row in trace:
            assert row[3] == pytest.approx(0.7, abs=1e-3)

    def test_full_adaptation_config_tracks_env(self):
        # maintain_frac=0 → config_next = env at every step
        trace = run(maintain_frac=0.0, env_drift_rate=0.1, T=5)
        for _, env, config, _, deficit in trace:
            assert deficit == pytest.approx(0.0, abs=1e-4)
            assert config == pytest.approx(env, abs=1e-4)

    def test_custom_config0(self):
        trace = run(maintain_frac=0.5, T=1, config0=10.0, env_drift_rate=0.0)
        # env stays at 0.0 (drift=0), config starts at 10 → adapts toward 0
        _, env, config, _, deficit = trace[0]
        assert env == pytest.approx(0.0, abs=1e-4)
        assert config < 10.0   # moved toward env


# ---------------------------------------------------------------------------
# Deficit monotonics: higher maintain_frac → higher steady-state deficit
# ---------------------------------------------------------------------------

class TestDeficitMonotonics:
    def _final_deficit(self, mf, T=40):
        return run(maintain_frac=mf, T=T)[-1][4]

    def test_higher_maintain_frac_higher_deficit(self):
        d01 = self._final_deficit(0.1)
        d05 = self._final_deficit(0.5)
        d09 = self._final_deficit(0.9)
        assert d01 < d05 < d09

    def test_zero_maintain_frac_near_zero_deficit(self):
        assert self._final_deficit(0.0) == pytest.approx(0.0, abs=1e-4)

    def test_full_maintain_frac_high_deficit(self):
        # maintain_frac=1 → config never moves → deficit grows with env drift
        d = self._final_deficit(1.0, T=20)
        # env at t=20 is 20*0.05 = 1.0, config=0 → deficit = 1.0
        assert d == pytest.approx(1.0, abs=1e-4)

    def test_deficit_grows_over_time_for_high_maintain(self):
        trace = run(maintain_frac=0.9, T=40)
        early = trace[0][4]
        late = trace[-1][4]
        assert late > early


# ---------------------------------------------------------------------------
# optics()
# ---------------------------------------------------------------------------

class TestOptics:
    def test_required_keys_present(self):
        trace = run(maintain_frac=0.5)
        out = optics(trace)
        for key in ("final_deficit", "deficit_growing", "note"):
            assert key in out

    def test_final_deficit_matches_trace(self):
        trace = run(maintain_frac=0.5)
        out = optics(trace)
        assert out["final_deficit"] == trace[-1][4]

    def test_deficit_growing_true_when_rising(self):
        trace = run(maintain_frac=0.9, T=40)
        out = optics(trace)
        assert out["deficit_growing"] is True

    def test_deficit_growing_false_when_flat(self):
        # full adaptation → deficit = 0 throughout → slope = 0
        trace = run(maintain_frac=0.0, T=10)
        out = optics(trace)
        assert out["deficit_growing"] is False

    def test_note_is_nonempty_string(self):
        trace = run(maintain_frac=0.5)
        out = optics(trace)
        assert isinstance(out["note"], str) and len(out["note"]) > 0

    def test_note_describes_deficit_and_maintenance(self):
        trace = run(maintain_frac=0.5)
        note = optics(trace)["note"].lower()
        assert "deficit" in note or "maintenance" in note or "gradient" in note


# ---------------------------------------------------------------------------
# Demo scenario
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def test_three_maintain_fracs_produce_different_deficits(self):
        results = {mf: run(maintain_frac=mf)[-1][4] for mf in (0.1, 0.5, 0.9)}
        assert results[0.1] < results[0.5] < results[0.9]

    def test_high_maintain_high_final_deficit(self):
        trace = run(maintain_frac=0.9)
        assert trace[-1][4] > 0.3

    def test_low_maintain_low_final_deficit(self):
        trace = run(maintain_frac=0.1)
        assert trace[-1][4] < 0.1

    def test_sample_trace_row_structure(self):
        trace = run(maintain_frac=0.9)
        sample = trace[::8]
        for row in sample:
            t, env, config, mf, deficit = row
            assert isinstance(t, int)
            assert env > 0  # env has been drifting
            assert deficit >= 0
