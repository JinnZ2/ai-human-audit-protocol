"""Unit tests for physics/continuity_audit.py.

The module audits an incentive structure (field g) acting on a diversity field,
propagates the trajectory, and reports whether continuity is supported or degraded.
Tests verify mathematical contracts (Hill numbers, replicator dynamics, resilience)
and the full audit pipeline including self-sabotage scoring and falsifier string.

Two reference distributions are used throughout:
  P0_DEMO — canonical demo distribution; already high evenness (0.817).
            Confirms DEGRADES (g>0) and INDETERMINATE (g=0).
  P0_LOW  — very skewed; evenness ≈ 0.25.
            Confirms SUPPORTS (g<0) because there is room for C to rise.
"""

import math

import pytest

from physics.continuity_audit import (
    Agent,
    audit,
    continuity_support,
    diversity_profile,
    hill,
    normalized_evenness,
    replicator_step,
    resilience,
)

# canonical high-evenness distribution (from the demo)
P0_DEMO = [0.30, 0.22, 0.18, 0.14, 0.10, 0.06]
# low-evenness distribution: room for diversifying force to move C
P0_LOW  = [0.90, 0.04, 0.03, 0.02, 0.01]

AGENTS = [
    Agent("AI_model",    0.95),
    Agent("institution", 0.55),
    Agent("biology",     0.35),
]


# -----------------------------------------------------------------------
# hill() — effective number of types
# -----------------------------------------------------------------------

class TestHill:
    def test_q0_is_richness(self):
        assert hill([0.4, 0.3, 0.2, 0.1], 0.0) == 4.0

    def test_q0_excludes_zeros(self):
        assert hill([0.5, 0.5, 0.0, 0.0], 0.0) == 2.0

    def test_q1_is_exp_shannon(self):
        p = [0.5, 0.5]
        expected = math.exp(-2 * 0.5 * math.log(0.5))
        assert abs(hill(p, 1.0) - expected) < 1e-9

    def test_q2_is_inverse_simpson(self):
        p = [0.6, 0.4]
        expected = 1.0 / (0.6**2 + 0.4**2)
        assert abs(hill(p, 2.0) - expected) < 1e-9

    def test_uniform_all_orders_equal_n(self):
        p = [0.25, 0.25, 0.25, 0.25]
        for q in [0.0, 0.5, 1.0, 2.0]:
            assert abs(hill(p, q) - 4.0) < 1e-9, f"D({q}) should equal 4 for uniform"

    def test_monoculture_is_1_for_all_q(self):
        p = [1.0]
        for q in [0.0, 1.0, 2.0, 4.0]:
            assert abs(hill(p, q) - 1.0) < 1e-9, f"D({q}) should be 1 for monoculture"

    def test_empty_returns_zero(self):
        assert hill([], 1.0) == 0.0

    def test_all_zeros_returns_zero(self):
        assert hill([0.0, 0.0, 0.0], 1.0) == 0.0

    def test_ordering_property_nonuniform(self):
        # D(q) is non-increasing in q for non-uniform distributions
        p = [0.5, 0.3, 0.2]
        d0 = hill(p, 0.0)
        d1 = hill(p, 1.0)
        d2 = hill(p, 2.0)
        d4 = hill(p, 4.0)
        assert d0 >= d1 >= d2 >= d4


# -----------------------------------------------------------------------
# diversity_profile()
# -----------------------------------------------------------------------

class TestDiversityProfile:
    def test_returns_dict_with_default_qs(self):
        profile = diversity_profile([0.5, 0.3, 0.2])
        assert set(profile.keys()) == {0.0, 0.5, 1.0, 2.0, 4.0}

    def test_custom_qs_respected(self):
        profile = diversity_profile([0.5, 0.5], qs=(0.0, 2.0))
        assert set(profile.keys()) == {0.0, 2.0}

    def test_all_values_nonnegative(self):
        profile = diversity_profile([0.4, 0.3, 0.2, 0.1])
        assert all(v >= 0.0 for v in profile.values())

    def test_uniform_all_equal_n(self):
        profile = diversity_profile([0.25, 0.25, 0.25, 0.25])
        assert all(abs(v - 4.0) < 1e-9 for v in profile.values())


# -----------------------------------------------------------------------
# normalized_evenness()
# -----------------------------------------------------------------------

class TestNormalizedEvenness:
    def test_uniform_four_types_is_1(self):
        assert abs(normalized_evenness([0.25, 0.25, 0.25, 0.25]) - 1.0) < 1e-9

    def test_single_nonzero_type_returns_zero(self):
        assert normalized_evenness([1.0]) == 0.0

    def test_all_zeros_returns_zero(self):
        assert normalized_evenness([0.0, 0.0, 0.0]) == 0.0

    def test_result_in_range_0_to_1(self):
        e = normalized_evenness([0.5, 0.3, 0.15, 0.05])
        assert 0.0 <= e <= 1.0

    def test_formula_is_hill2_over_total_len(self):
        p = [0.4, 0.3, 0.2, 0.1]
        assert abs(normalized_evenness(p) - hill(p, 2.0) / len(p)) < 1e-9

    def test_more_even_has_higher_evenness(self):
        skewed = [0.7, 0.2, 0.1]
        even   = [0.4, 0.35, 0.25]
        assert normalized_evenness(even) > normalized_evenness(skewed)

    def test_two_equal_types_with_zero_padding(self):
        # [0.5, 0.5, 0, 0]: D(2)=2, len=4 → 0.5
        assert abs(normalized_evenness([0.5, 0.5, 0.0, 0.0]) - 0.5) < 1e-9


# -----------------------------------------------------------------------
# replicator_step()
# -----------------------------------------------------------------------

class TestReplicatorStep:
    def test_output_sums_to_one(self):
        new_p = replicator_step([0.4, 0.35, 0.25], 1.0, 0.05)
        assert abs(sum(new_p) - 1.0) < 1e-12

    def test_neutral_g_leaves_distribution_unchanged(self):
        p = [0.4, 0.35, 0.25]
        new_p = replicator_step(p, 0.0, 0.1)
        for a, b in zip(p, new_p):
            assert abs(a - b) < 1e-12

    def test_positive_g_increases_most_common(self):
        p = [0.6, 0.3, 0.1]
        new_p = replicator_step(p, 1.0, 0.1)
        assert new_p[0] > p[0]

    def test_negative_g_increases_rarest(self):
        p = [0.6, 0.3, 0.1]
        new_p = replicator_step(p, -1.0, 0.1)
        assert new_p[2] > p[2]

    def test_all_nonnegative(self):
        new_p = replicator_step([0.5, 0.4, 0.1], 5.0, 0.2)
        assert all(x >= 0.0 for x in new_p)

    def test_length_preserved(self):
        p = [0.3, 0.4, 0.3]
        assert len(replicator_step(p, 1.0, 0.1)) == len(p)


# -----------------------------------------------------------------------
# resilience()
# -----------------------------------------------------------------------

class TestResilience:
    def test_high_evenness_gives_high_resilience(self):
        p = [0.25, 0.25, 0.25, 0.25]   # evenness = 1.0 >> d_crit
        assert resilience(p) > 0.9

    def test_single_type_gives_low_resilience(self):
        p = [1.0]                        # evenness = 0.0; single type
        assert resilience(p, d_crit=0.3) < 0.1

    def test_at_d_crit_gives_half(self):
        # evenness = 1.0; set d_crit = 1.0 → logistic(0) = 0.5
        p = [0.25, 0.25, 0.25, 0.25]
        assert abs(resilience(p, d_crit=1.0) - 0.5) < 1e-9

    def test_result_in_range_0_to_1(self):
        r = resilience([0.4, 0.3, 0.2, 0.1])
        assert 0.0 < r < 1.0

    def test_more_even_more_resilient(self):
        skewed = [0.7, 0.2, 0.1]
        even   = [0.4, 0.35, 0.25]
        assert resilience(even) > resilience(skewed)


# -----------------------------------------------------------------------
# continuity_support()
# -----------------------------------------------------------------------

class TestContinuitySupport:
    def test_uniform_gives_high_support(self):
        assert continuity_support([0.25, 0.25, 0.25, 0.25]) > 0.9

    def test_accepts_d_crit_kwarg(self):
        p = [0.25, 0.25, 0.25, 0.25]
        high = continuity_support(p, d_crit=0.1)
        low  = continuity_support(p, d_crit=0.9)
        assert high > low

    def test_equals_resilience(self):
        p = [0.4, 0.3, 0.2, 0.1]
        assert abs(continuity_support(p) - resilience(p)) < 1e-12


# -----------------------------------------------------------------------
# Agent
# -----------------------------------------------------------------------

class TestAgent:
    def test_name_stored(self):
        assert Agent("x", 0.7).name == "x"

    def test_kappa_stored(self):
        assert Agent("x", 0.7).kappa == 0.7


# -----------------------------------------------------------------------
# audit() — full pipeline
# -----------------------------------------------------------------------

class TestAudit:
    # --- return shape ---

    def test_returns_expected_top_level_keys(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        for key in ("incentive_g", "verdict", "dC_dt", "C_start", "C_end",
                    "even_start", "even_end", "agents", "falsifier",
                    "trajectory", "note"):
            assert key in r

    def test_incentive_g_is_stored(self):
        assert audit(P0_DEMO, +0.5, AGENTS)["incentive_g"] == +0.5

    # --- three verdict branches ---

    def test_consolidation_degrades_continuity(self):
        assert audit(P0_DEMO, +1.0, AGENTS)["verdict"] == "DEGRADES_CONTINUITY"

    def test_neutral_is_indeterminate(self):
        assert audit(P0_DEMO, 0.0, AGENTS)["verdict"] == "INDETERMINATE"

    def test_diversifying_on_low_distribution_supports_continuity(self):
        # P0_LOW starts at low evenness (~0.25); g=-1 has room to raise C
        assert audit(P0_LOW, -1.0, AGENTS)["verdict"] == "SUPPORTS_CONTINUITY"

    # --- dC/dt direction ---

    def test_dC_dt_negative_when_degrading(self):
        assert audit(P0_DEMO, +1.0, AGENTS)["dC_dt"] < 0

    def test_dC_dt_zero_when_neutral(self):
        assert abs(audit(P0_DEMO, 0.0, AGENTS)["dC_dt"]) < 1e-3

    def test_dC_dt_positive_when_supporting(self):
        assert audit(P0_LOW, -1.0, AGENTS)["dC_dt"] > 0

    # --- C_start / C_end consistency ---

    def test_C_start_matches_initial_C(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        expected = round(continuity_support(P0_DEMO), 4)
        assert abs(r["C_start"] - expected) < 1e-9

    def test_C_end_less_than_start_when_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        assert r["C_end"] < r["C_start"]

    def test_C_end_greater_than_start_when_supporting(self):
        r = audit(P0_LOW, -1.0, AGENTS)
        assert r["C_end"] > r["C_start"]

    # --- trajectory ---

    def test_trajectory_has_steps_plus_one_entries(self):
        r = audit(P0_DEMO, 0.0, AGENTS, steps=10)
        assert len(r["trajectory"]) == 11

    def test_each_trajectory_entry_has_required_keys(self):
        r = audit(P0_DEMO, 0.0, AGENTS, steps=5)
        for entry in r["trajectory"]:
            for key in ("C", "even", "D"):
                assert key in entry

    def test_trajectory_C_values_in_range(self):
        r = audit(P0_DEMO, +1.0, AGENTS, steps=20)
        for entry in r["trajectory"]:
            assert 0.0 <= entry["C"] <= 1.0

    def test_trajectory_even_values_in_range(self):
        r = audit(P0_LOW, -1.0, AGENTS, steps=20)
        for entry in r["trajectory"]:
            assert 0.0 <= entry["even"] <= 1.0

    # --- agents ---

    def test_agents_dict_contains_all_agents(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        for a in AGENTS:
            assert a.name in r["agents"]

    def test_each_agent_entry_has_expected_fields(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        for name, s in r["agents"].items():
            for key in ("kappa", "self_sabotage", "coherent_with_own_continuity"):
                assert key in s

    # --- coherence (incoherence = kappa >= 0.6 while pursuing degrading field) ---

    def test_high_kappa_agent_incoherent_under_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        # AI_model kappa=0.95 >= 0.6 and DEGRADES → INCOHERENT
        assert r["agents"]["AI_model"]["coherent_with_own_continuity"] is False

    def test_mid_kappa_agent_coherent_under_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        # institution kappa=0.55 < 0.6 → coherent regardless
        assert r["agents"]["institution"]["coherent_with_own_continuity"] is True

    def test_low_kappa_agent_coherent_under_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        # biology kappa=0.35 < 0.6 → coherent regardless
        assert r["agents"]["biology"]["coherent_with_own_continuity"] is True

    def test_all_agents_coherent_when_supporting(self):
        r = audit(P0_LOW, -1.0, AGENTS)
        for name, s in r["agents"].items():
            assert s["coherent_with_own_continuity"] is True

    def test_all_agents_coherent_when_indeterminate(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        for name, s in r["agents"].items():
            assert s["coherent_with_own_continuity"] is True

    # --- self-sabotage ---

    def test_self_sabotage_positive_when_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        assert r["agents"]["AI_model"]["self_sabotage"] > 0

    def test_self_sabotage_zero_when_supporting(self):
        r = audit(P0_LOW, -1.0, AGENTS)
        for name, s in r["agents"].items():
            assert s["self_sabotage"] == 0.0

    def test_self_sabotage_zero_when_neutral(self):
        r = audit(P0_DEMO, 0.0, AGENTS)
        for name, s in r["agents"].items():
            assert s["self_sabotage"] == 0.0

    def test_self_sabotage_scales_with_kappa_when_degrading(self):
        r = audit(P0_DEMO, +1.0, AGENTS)
        ai_s  = r["agents"]["AI_model"]["self_sabotage"]
        bio_s = r["agents"]["biology"]["self_sabotage"]
        assert ai_s > bio_s

    # --- normalization of p0 ---

    def test_unnormalized_p0_gives_same_result(self):
        p_scaled = [x * 3.0 for x in P0_DEMO]
        r_norm   = audit(P0_DEMO, +1.0, AGENTS)
        r_scaled = audit(p_scaled, +1.0, AGENTS)
        assert r_norm["verdict"] == r_scaled["verdict"]
        assert abs(r_norm["C_start"] - r_scaled["C_start"]) < 1e-9

    # --- falsifier and note ---

    def test_falsifier_is_nonempty(self):
        assert bool(audit(P0_DEMO, 0.0, AGENTS)["falsifier"])

    def test_falsifier_mentions_d_crit(self):
        assert "d_crit" in audit(P0_DEMO, 0.0, AGENTS)["falsifier"]

    def test_note_warns_against_storing_verdict(self):
        note = audit(P0_DEMO, 0.0, AGENTS)["note"]
        assert "do not store" in note.lower() or "re-run" in note.lower()
