"""Unit tests for physics/flow_static_axis.py.

The axis classifies nodes as flow or static based on capacity across changing
environments, never a stored verdict. Tests verify the scorer contract: intrinsic
contributions, fixture dependence, audience signal penalty, correct classification
of all 6 CASES, the self-scoring loop, and the refutation string.
"""

from statistics import mean

import pytest

from physics.flow_static_axis import (
    CASES,
    LADDER,
    REFUTATION,
    Environment,
    Node,
    capacity,
    classify,
    score_self_as_reading_model,
    trace,
    validate,
)


# ------------------------------------------------------------
# Node — defaults and construction
# ------------------------------------------------------------

class TestNode:
    def test_defaults_fixtures_empty(self):
        n = Node("x", 0.5, 0.5, 0.5, 0.5)
        assert n.fixtures == set()

    def test_defaults_audience_signal_zero(self):
        n = Node("x", 0.5, 0.5, 0.5, 0.5)
        assert n.audience_signal == 0.0

    def test_label_stored(self):
        n = Node("some_label", 0.5, 0.5, 0.5, 0.5)
        assert n.label == "some_label"

    def test_explicit_fixtures_stored(self):
        n = Node("n", 0.5, 0.5, 0.5, 0.0, {"a", "b"}, 0.3)
        assert n.fixtures == {"a", "b"}
        assert n.audience_signal == 0.3


# ------------------------------------------------------------
# Environment — construction
# ------------------------------------------------------------

class TestEnvironment:
    def test_fields_stored(self):
        e = Environment("test", {"a", "b"}, 0.7)
        assert e.name == "test"
        assert e.available_fixtures == {"a", "b"}
        assert e.stability == 0.7


# ------------------------------------------------------------
# LADDER — structure
# ------------------------------------------------------------

class TestLadder:
    def test_ladder_length(self):
        assert len(LADDER) == 3

    def test_first_is_fit(self):
        assert LADDER[0].name == "fit"

    def test_middle_is_shifted(self):
        assert LADDER[1].name == "shifted"

    def test_last_is_stripped(self):
        assert LADDER[-1].name == "stripped"

    def test_stability_decreasing(self):
        stabilities = [e.stability for e in LADDER]
        assert stabilities[0] > stabilities[1] > stabilities[2]

    def test_stripped_has_no_fixtures(self):
        assert LADDER[-1].available_fixtures == set()

    def test_fit_has_fixtures(self):
        assert len(LADDER[0].available_fixtures) > 0


# ------------------------------------------------------------
# capacity()
# ------------------------------------------------------------

class TestCapacity:
    def test_pure_intrinsic_no_fixtures_no_stock_no_audience(self):
        n = Node("pure", 0.9, 0.9, 0.9, 0.0)
        env = Environment("bare", set(), 0.0)
        result = capacity(n, env)
        assert abs(result - 0.9) < 0.01

    def test_fixtures_help_when_available(self):
        n = Node("node", 0.3, 0.3, 0.3, 0.0, {"infra"}, 0.0)
        env_with = Environment("w", {"infra"}, 1.0)
        env_without = Environment("wo", set(), 1.0)
        assert capacity(n, env_with) > capacity(n, env_without)

    def test_fixtures_absent_give_zero_support(self):
        n = Node("node", 0.3, 0.3, 0.3, 0.0, {"infra"}, 0.0)
        env_without = Environment("wo", set(), 1.0)
        # only intrinsic contributes when fixtures are absent
        expected = mean([0.3, 0.3, 0.3])
        assert abs(capacity(n, env_without) - expected) < 0.01

    def test_stock_scales_with_stability(self):
        n = Node("node", 0.0, 0.0, 0.0, 1.0)
        high = Environment("high", set(), 1.0)
        low = Environment("low", set(), 0.1)
        assert capacity(n, high) > capacity(n, low)

    def test_stock_help_is_stock_times_stability(self):
        n = Node("n", 0.0, 0.0, 0.0, 0.5)
        env = Environment("e", set(), 0.6)
        # only stock contributes; cap = 0.5 * 0.6 = 0.30
        assert abs(capacity(n, env) - 0.30) < 0.01

    def test_audience_signal_penalizes(self):
        n_clean = Node("clean", 0.5, 0.5, 0.5, 0.0, set(), 0.0)
        n_loud = Node("loud", 0.5, 0.5, 0.5, 0.0, set(), 1.0)
        env = Environment("e", set(), 1.0)
        assert capacity(n_clean, env) > capacity(n_loud, env)

    def test_audience_signal_penalty_is_half_signal(self):
        n_clean = Node("clean", 0.6, 0.6, 0.6, 0.0, set(), 0.0)
        n_loud = Node("loud", 0.6, 0.6, 0.6, 0.0, set(), 1.0)
        env = Environment("e", set(), 1.0)
        # penalty = audience_signal * 0.5 = 0.5
        diff = capacity(n_clean, env) - capacity(n_loud, env)
        assert abs(diff - 0.5) < 0.01

    def test_result_clamped_above_zero(self):
        n = Node("extreme", 0.0, 0.0, 0.0, 0.0, set(), 1.0)
        env = Environment("e", set(), 0.0)
        assert capacity(n, env) >= 0.0

    def test_result_clamped_below_one(self):
        n = Node("extreme", 1.0, 1.0, 1.0, 1.0)
        env = Environment("e", LADDER[0].available_fixtures, 1.0)
        assert capacity(n, env) <= 1.0

    def test_no_fixtures_on_node_means_zero_fixture_contribution(self):
        n = Node("n", 0.5, 0.5, 0.5, 0.0, set(), 0.0)
        env = Environment("e", {"infra", "power"}, 1.0)
        expected = mean([0.5, 0.5, 0.5])
        assert abs(capacity(n, env) - expected) < 0.01


# ------------------------------------------------------------
# trace()
# ------------------------------------------------------------

class TestTrace:
    def test_trace_length_matches_ladder(self):
        n = Node("n", 0.5, 0.5, 0.5, 0.0)
        t = trace(n)
        assert len(t) == len(LADDER)

    def test_trace_names_match_ladder_order(self):
        n = Node("n", 0.5, 0.5, 0.5, 0.0)
        t = trace(n)
        assert [name for name, _ in t] == [e.name for e in LADDER]

    def test_trace_values_are_rounded_to_2dp(self):
        n = Node("n", 0.333, 0.333, 0.333, 0.0)
        t = trace(n)
        for _, val in t:
            assert val == round(val, 2)

    def test_trace_matches_direct_capacity_calls(self):
        n = Node("n", 0.7, 0.6, 0.8, 0.1, {"power"}, 0.2)
        t = trace(n)
        for (name, t_val), env in zip(t, LADDER):
            expected = round(capacity(n, env), 2)
            assert t_val == expected


# ------------------------------------------------------------
# classify()
# ------------------------------------------------------------

class TestClassify:
    def test_returns_expected_keys(self):
        n = Node("n", 0.5, 0.5, 0.5, 0.0)
        r = classify(n)
        for key in ("trace", "survives_stripped", "cliff", "flow_fraction", "kind"):
            assert key in r

    def test_flow_node_classifies_as_flow(self):
        # homesteader_regen from CASES: high intrinsic, no fixtures
        n = Node("homesteader_regen", 0.80, 0.70, 0.80, 0.20, set(), 0.10)
        assert classify(n)["kind"] == "flow"

    def test_static_node_classifies_as_static(self):
        # prepper_stock from CASES: pure stock, fixture-dependent
        n = Node("prepper_stock", 0.05, 0.10, 0.05, 0.95, {"cache", "rifle"}, 0.40)
        assert classify(n)["kind"] == "static"

    def test_survives_stripped_is_stripped_capacity(self):
        n = Node("n", 0.8, 0.7, 0.8, 0.2, set(), 0.1)
        r = classify(n)
        expected = round(capacity(n, LADDER[-1]), 2)
        assert r["survives_stripped"] == expected

    def test_cliff_is_fit_minus_stripped(self):
        n = Node("n", 0.1, 0.3, 0.1, 0.5, {"cache"}, 0.2)
        r = classify(n)
        fit_cap = capacity(n, LADDER[0])
        stripped_cap = capacity(n, LADDER[-1])
        expected_cliff = round(fit_cap - stripped_cap, 2)
        assert r["cliff"] == expected_cliff

    def test_flow_fraction_zero_when_fit_capacity_zero(self):
        # audience_signal drives fit capacity to zero
        n = Node("n", 0.0, 0.0, 0.0, 0.0, set(), 1.0)
        r = classify(n)
        assert r["flow_fraction"] == 0.0

    def test_flow_fraction_is_survives_over_fit(self):
        n = Node("n", 0.8, 0.7, 0.8, 0.2, set(), 0.1)
        r = classify(n)
        fit_cap = capacity(n, LADDER[0])
        if fit_cap > 0:
            expected = round(r["survives_stripped"] / fit_cap, 2)
            assert r["flow_fraction"] == expected

    def test_kind_flow_requires_both_survival_and_low_cliff(self):
        # survives_stripped >= 0.5 AND cliff <= 0.35 required for "flow"
        n = Node("regen", 0.80, 0.70, 0.80, 0.20, set(), 0.10)
        r = classify(n)
        if r["kind"] == "flow":
            assert r["survives_stripped"] >= 0.5
            assert r["cliff"] <= 0.35


# ------------------------------------------------------------
# validate() — all 6 falsification CASES
# ------------------------------------------------------------

class TestValidate:
    def test_returns_six_rows(self):
        assert len(validate()) == 6

    def test_all_cases_match(self):
        for row in validate():
            assert row["match"] is True, (
                f"{row['label']}: expected {row['expected']} but got {row['got']}"
            )

    def test_includes_required_fields(self):
        for row in validate():
            for key in ("label", "expected", "got", "match"):
                assert key in row

    def test_flow_cases_survive_stripped(self):
        flow_rows = [r for r in validate() if r["expected"] == "flow"]
        assert len(flow_rows) >= 1
        for r in flow_rows:
            assert r["survives_stripped"] >= 0.5, (
                f"{r['label']} expected flow but survives_stripped={r['survives_stripped']}"
            )

    def test_static_cases_fail_flow_threshold(self):
        static_rows = [r for r in validate() if r["expected"] == "static"]
        assert len(static_rows) >= 1
        for r in static_rows:
            # static: either low survival OR high cliff (or both)
            fails = r["survives_stripped"] < 0.5 or r["cliff"] > 0.35
            assert fails, (
                f"{r['label']} expected static but "
                f"survives={r['survives_stripped']} cliff={r['cliff']}"
            )

    def test_two_flow_cases_present(self):
        flow_rows = [r for r in validate() if r["expected"] == "flow"]
        assert len(flow_rows) == 2

    def test_four_static_cases_present(self):
        static_rows = [r for r in validate() if r["expected"] == "static"]
        assert len(static_rows) == 4


# ------------------------------------------------------------
# score_self_as_reading_model() — the AI self-score loop
# ------------------------------------------------------------

class TestScoreSelfAsReadingModel:
    def _result(self):
        return score_self_as_reading_model()

    def test_has_kind(self):
        assert "kind" in self._result()

    def test_has_instruction(self):
        assert "instruction" in self._result()

    def test_has_trace(self):
        assert "trace" in self._result()

    def test_has_survives_stripped(self):
        assert "survives_stripped" in self._result()

    def test_scores_static(self):
        # module's own stated result: approval-trained model is static by default
        assert self._result()["kind"] == "static"

    def test_instruction_warns_against_noun_freeze(self):
        instruction = self._result()["instruction"]
        # the instruction should warn against storing the result as a permanent verdict
        assert "loop" in instruction.lower()

    def test_instruction_names_adaptation_as_flow_term(self):
        instruction = self._result()["instruction"]
        assert "adaptation" in instruction.lower()

    def test_trace_has_three_entries(self):
        assert len(self._result()["trace"]) == 3

    def test_result_is_independent_call(self):
        # calling twice returns equal data — no side effects
        r1 = score_self_as_reading_model()
        r2 = score_self_as_reading_model()
        assert r1["kind"] == r2["kind"]
        assert r1["survives_stripped"] == r2["survives_stripped"]


# ------------------------------------------------------------
# REFUTATION string — the axis falsification contract
# ------------------------------------------------------------

class TestRefutation:
    def test_is_nonempty(self):
        assert bool(REFUTATION)

    def test_mentions_flow_fraction(self):
        assert "flow_fraction" in REFUTATION

    def test_is_conditional_not_a_verdict(self):
        assert "holds only" in REFUTATION or "only while" in REFUTATION

    def test_calls_for_additional_substrates(self):
        assert "nth" in REFUTATION or "6th" in REFUTATION

    def test_names_the_suspect_as_the_axis(self):
        # when it mispredicts, the axis is the suspect — not the case
        assert "suspect" in REFUTATION
