"""Unit tests for physics/interface_layer.py.

The module models substrate access as temperature-controlled by comfort (1-stress):
high stress collapses the agent onto its default mode; low stress spreads access
across substrates. Tests verify the access/band/kappa chain, the stress feedback
loop, the two strategies (naive_target vs translator), and the full interact
pipeline including the ENABLING/COERCIVE guardrail.

Demo affinity setup used throughout: affinity=[2.0, 1.0, 0.0], target=2
  substrate 0 = native/emotional (high affinity), substrate 2 = geometric (target)
"""

import math

import pytest

from physics.interface_layer import (
    access,
    band_eff,
    interact,
    kappa_estimate,
    naive_target,
    receive,
    translator,
)

# canonical demo setup
AFF = [2.0, 1.0, 0.0]
STRESS_HIGH = 0.85    # flooded
STRESS_LOW  = 0.10    # comfortable
TARGET = 2


# -----------------------------------------------------------------------
# access() — softmax temperature-controlled by stress
# -----------------------------------------------------------------------

class TestAccess:
    def test_sums_to_one(self):
        for stress in [0.0, 0.3, 0.7, 1.0]:
            acc = access(AFF, stress)
            assert abs(sum(acc) - 1.0) < 1e-12

    def test_returns_same_length_as_affinity(self):
        acc = access(AFF, 0.5)
        assert len(acc) == len(AFF)

    def test_all_positive(self):
        for stress in [0.0, 0.5, 1.0]:
            acc = access(AFF, stress)
            assert all(x > 0.0 for x in acc)

    def test_high_affinity_always_highest_access(self):
        # argmax(affinity) = 0; should always have highest access
        for stress in [0.0, 0.5, 0.9, 1.0]:
            acc = access(AFF, stress)
            assert acc[0] == max(acc)

    def test_high_stress_concentrates_on_default(self):
        acc_hi = access(AFF, 0.99)
        acc_lo = access(AFF, 0.01)
        # high stress → more concentrated on substrate 0
        assert acc_hi[0] > acc_lo[0]

    def test_low_stress_spreads_to_far_substrates(self):
        acc_hi = access(AFF, 0.99)
        acc_lo = access(AFF, 0.01)
        # low stress → more access to far substrate
        assert acc_lo[2] > acc_hi[2]

    def test_temperature_at_max_stress_uses_t_floor(self):
        # T = t_floor + t_span*(1-1) = t_floor; still positive
        acc = access(AFF, 1.0, t_floor=0.15)
        assert all(x > 0.0 for x in acc)

    def test_custom_t_floor_and_t_span(self):
        # very high temperature (t_floor=5, t_span=0) → nearly uniform
        acc = access([1.0, 0.0], 0.5, t_floor=50.0, t_span=0.0)
        assert abs(acc[0] - acc[1]) < 0.01


# -----------------------------------------------------------------------
# band_eff() — effective number of reachable substrates (Hill q=1)
# -----------------------------------------------------------------------

class TestBandEff:
    def test_uniform_access_equals_n(self):
        acc = [1/3, 1/3, 1/3]
        assert abs(band_eff(acc) - 3.0) < 1e-9

    def test_fully_collapsed_near_one(self):
        # nearly all weight on one substrate
        acc = [0.9999, 0.00005, 0.00005]
        assert band_eff(acc) < 1.01

    def test_spread_greater_than_collapsed(self):
        spread    = [0.4, 0.35, 0.25]
        collapsed = [0.98, 0.01, 0.01]
        assert band_eff(spread) > band_eff(collapsed)

    def test_positive_for_any_distribution(self):
        for acc in [[1.0], [0.5, 0.5], [0.25, 0.25, 0.25, 0.25]]:
            assert band_eff(acc) > 0.0

    def test_matches_exp_shannon(self):
        acc = [0.5, 0.3, 0.2]
        H = -sum(x * math.log(x) for x in acc)
        assert abs(band_eff(acc) - math.exp(H)) < 1e-12


# -----------------------------------------------------------------------
# kappa_estimate() — continuity-dependence from band width
# -----------------------------------------------------------------------

class TestKappaEstimate:
    def test_single_substrate_returns_one(self):
        assert kappa_estimate([1.0]) == 1.0

    def test_uniform_gives_zero_kappa(self):
        # uniform over n substrates → band_eff = n → kappa = 1-(n-1)/(n-1) = 0
        acc = [1/3, 1/3, 1/3]
        assert abs(kappa_estimate(acc) - 0.0) < 1e-9

    def test_collapsed_gives_kappa_near_one(self):
        acc = [0.9999, 0.00005, 0.00005]
        assert kappa_estimate(acc) > 0.99

    def test_result_in_range_0_to_1(self):
        for acc in [[0.5, 0.5], [0.4, 0.35, 0.25], [0.25, 0.25, 0.25, 0.25]]:
            k = kappa_estimate(acc)
            assert 0.0 <= k <= 1.0

    def test_formula(self):
        acc = [0.5, 0.3, 0.2]
        expected = 1.0 - (band_eff(acc) - 1.0) / (len(acc) - 1.0)
        assert abs(kappa_estimate(acc) - expected) < 1e-12

    def test_higher_stress_yields_higher_kappa(self):
        # more stress → narrower band → higher kappa
        lo = kappa_estimate(access(AFF, STRESS_LOW))
        hi = kappa_estimate(access(AFF, STRESS_HIGH))
        assert hi > lo


# -----------------------------------------------------------------------
# receive() — stress feedback from signal encoding
# -----------------------------------------------------------------------

class TestReceive:
    def test_returns_two_values(self):
        result = receive(AFF, 0.5, 0)
        assert len(result) == 2

    def test_friction_is_complement_of_access(self):
        stress = 0.5
        encoding = 0
        acc = access(AFF, stress)
        _, friction = receive(AFF, stress, encoding)
        assert abs(friction - (1.0 - acc[encoding])) < 1e-12

    def test_native_substrate_low_friction(self):
        # encoding native substrate (0) → high access → low friction
        _, friction = receive(AFF, STRESS_HIGH, 0)
        assert friction < 0.2

    def test_far_substrate_high_friction_when_flooded(self):
        # encoding far substrate (2) when flooded → very low access → high friction
        _, friction = receive(AFF, STRESS_HIGH, 2)
        assert friction > 0.9

    def test_high_friction_raises_stress(self):
        # encoding target (2) when flooded raises stress
        stress = 0.5
        new_stress, friction = receive(AFF, stress, 2)
        assert friction > 0.55        # friction > friction_safe
        assert new_stress > stress

    def test_low_friction_lowers_stress(self):
        # encoding native substrate (0) at moderate stress lowers stress
        stress = 0.5
        new_stress, friction = receive(AFF, stress, 0)
        assert friction < 0.55        # friction < friction_safe
        assert new_stress < stress

    def test_stress_clamped_below_one(self):
        # extreme encoding when already near max stress
        new_stress, _ = receive(AFF, 0.999, 2)
        assert new_stress <= 1.0

    def test_stress_clamped_above_zero(self):
        # very comfortable encoding when already near zero stress
        new_stress, _ = receive(AFF, 0.001, 0)
        assert new_stress >= 0.0

    def test_update_formula(self):
        stress = 0.5
        encoding = 1
        alpha = 0.18
        friction_safe = 0.55
        acc = access(AFF, stress)
        friction = 1.0 - acc[encoding]
        expected = min(1.0, max(0.0, stress + alpha * (friction - friction_safe)))
        new_stress, returned_friction = receive(AFF, stress, encoding)
        assert abs(new_stress - expected) < 1e-12
        assert abs(returned_friction - friction) < 1e-12


# -----------------------------------------------------------------------
# naive_target() — always encodes at target
# -----------------------------------------------------------------------

class TestNaiveTarget:
    def test_always_returns_target(self):
        for stress in [0.0, 0.5, 0.85, 1.0]:
            assert naive_target(AFF, stress, TARGET) == TARGET

    def test_target_value_is_respected(self):
        for t in [0, 1, 2]:
            assert naive_target(AFF, 0.5, t) == t


# -----------------------------------------------------------------------
# translator() — meet-then-lead
# -----------------------------------------------------------------------

class TestTranslator:
    def test_returns_valid_index(self):
        for stress in [0.0, 0.5, 0.85, 1.0]:
            idx = translator(AFF, stress, TARGET)
            assert 0 <= idx < len(AFF)

    def test_stays_at_native_when_flooded(self):
        # flooded → only substrate 0 reachable with floor=0.25 → picks 0
        result = translator(AFF, 0.99, TARGET)
        assert result == 0

    def test_picks_intermediate_at_low_stress(self):
        # at stress=0.2, substrate 1 becomes reachable (acc[1] ≈ 0.259 > 0.25)
        result = translator(AFF, 0.2, TARGET)
        assert result == 1

    def test_returns_target_when_target_is_native(self):
        # when target has highest affinity, translator reaches it even at low stress
        aff_reversed = [0.0, 1.0, 2.0]
        result = translator(aff_reversed, 0.0, 2)
        assert result == 2

    def test_never_overshoots_target(self):
        for stress in [0.0, 0.2, 0.5, 0.8]:
            result = translator(AFF, stress, 1)   # target=1
            assert result <= 1

    def test_falls_back_to_easiest_when_no_reachable(self):
        # floor=1.0 means nothing is "reachable" → fallback to argmax(acc)
        result = translator(AFF, 0.5, TARGET, floor=1.0)
        acc = access(AFF, 0.5)
        assert result == acc.index(max(acc))


# -----------------------------------------------------------------------
# interact() — full interaction pipeline
# -----------------------------------------------------------------------

class TestInteract:
    def _naive(self, **kw):
        return interact(AFF, STRESS_HIGH, TARGET, naive_target, **kw)

    def _trans(self, **kw):
        return interact(AFF, STRESS_HIGH, TARGET, translator, **kw)

    def test_returns_expected_keys(self):
        r = self._naive()
        for key in ("reached_target", "band_delta", "classification",
                    "kappa_start", "kappa_end", "trajectory",
                    "falsifier", "note"):
            assert key in r

    def test_trajectory_length_equals_steps(self):
        r = interact(AFF, STRESS_HIGH, TARGET, naive_target, steps=7)
        assert len(r["trajectory"]) == 7

    def test_each_trajectory_entry_has_required_keys(self):
        r = self._naive(steps=3)
        for entry in r["trajectory"]:
            for key in ("stress", "encoding", "reach_target", "band", "kappa"):
                assert key in entry

    # --- guardrail: naive is COERCIVE, translator is ENABLING ---

    def test_naive_is_coercive_on_flooded_agent(self):
        assert self._naive()["classification"] == "COERCIVE"

    def test_translator_is_enabling_on_flooded_agent(self):
        assert self._trans()["classification"] == "ENABLING"

    def test_classification_enabling_when_band_delta_positive(self):
        r = self._trans()
        assert r["band_delta"] > 1e-3
        assert r["classification"] == "ENABLING"

    def test_classification_coercive_when_band_delta_negative(self):
        r = self._naive()
        assert r["band_delta"] < -1e-3
        assert r["classification"] == "COERCIVE"

    # --- kappa direction ---

    def test_naive_raises_kappa(self):
        r = self._naive()
        assert r["kappa_end"] > r["kappa_start"]

    def test_translator_lowers_kappa(self):
        r = self._trans()
        assert r["kappa_end"] < r["kappa_start"]

    def test_kappa_start_matches_computed(self):
        r = self._naive()
        expected = round(kappa_estimate(access(AFF, STRESS_HIGH)), 4)
        assert r["kappa_start"] == expected

    # --- trajectory values in range ---

    def test_trajectory_stress_in_range(self):
        for entry in self._trans()["trajectory"]:
            assert 0.0 <= entry["stress"] <= 1.0

    def test_trajectory_band_positive(self):
        for entry in self._naive()["trajectory"]:
            assert entry["band"] > 0.0

    def test_trajectory_kappa_in_range(self):
        for entry in self._trans()["trajectory"]:
            assert 0.0 <= entry["kappa"] <= 1.0

    def test_translator_reduces_stress_over_horizon(self):
        r = self._trans()
        stress_start = r["trajectory"][0]["stress"]
        stress_end   = r["trajectory"][-1]["stress"]
        assert stress_end < stress_start

    def test_naive_raises_stress_to_ceiling(self):
        r = self._naive()
        # naive drives stress to 1.0 quickly
        assert r["trajectory"][-1]["stress"] == 1.0

    # --- falsifier and note ---

    def test_falsifier_nonempty(self):
        assert bool(self._naive()["falsifier"])

    def test_note_warns_against_storing(self):
        note = self._naive()["note"]
        assert "not a stored verdict" in note.lower() or "re-read" in note.lower()
