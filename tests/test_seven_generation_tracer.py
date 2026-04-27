"""Unit tests for physics/seven_generation_tracer.py.

The tracer is a structure for honest accounting, not a simulator.
These tests verify the arithmetic of projection, the audit-symmetric
hidden_at_decision_time output, and the bridge to C3 temporal_stability.
"""

import pytest

from physics.seven_generation_tracer import (
    GenerationFactor,
    GenerationProjection,
    SevenGenerationTrace,
    YEARS_PER_GENERATION,
    trace_seven_generations,
    trace_to_temporal_stability_7g,
    _factor_amount_at_gen,
)


# ------------------------------------------------------------
# GenerationFactor validation
# ------------------------------------------------------------

class TestGenerationFactorValidation:
    def test_valid_additive_constructs(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
        )
        assert f.kind == "additive"
        assert f.direction == "cost"

    def test_invalid_kind_rejected(self):
        with pytest.raises(ValueError, match="kind"):
            GenerationFactor(
                name="x", introduced_at_generation=0,
                per_generation_amount=1.0, unit="u",
                kind="bogus",
            )

    def test_invalid_direction_rejected(self):
        with pytest.raises(ValueError, match="direction"):
            GenerationFactor(
                name="x", introduced_at_generation=0,
                per_generation_amount=1.0, unit="u",
                direction="bogus",
            )

    def test_negative_compounding_factor_rejected(self):
        with pytest.raises(ValueError, match="compounding"):
            GenerationFactor(
                name="x", introduced_at_generation=0,
                per_generation_amount=1.0, unit="u",
                kind="compounding", compounding_factor=-0.1,
            )

    def test_negative_introduced_gen_rejected(self):
        with pytest.raises(ValueError, match="introduced_at_generation"):
            GenerationFactor(
                name="x", introduced_at_generation=-1,
                per_generation_amount=1.0, unit="u",
            )


# ------------------------------------------------------------
# _factor_amount_at_gen
# ------------------------------------------------------------

class TestFactorAmountAtGen:
    def test_zero_before_introduction(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=2,
            per_generation_amount=1.0, unit="u",
        )
        assert _factor_amount_at_gen(f, 0) == 0.0
        assert _factor_amount_at_gen(f, 1) == 0.0

    def test_additive_constant_after_introduction(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=0,
            per_generation_amount=2.5, unit="u",
            kind="additive",
        )
        assert _factor_amount_at_gen(f, 0) == 2.5
        assert _factor_amount_at_gen(f, 1) == 2.5
        assert _factor_amount_at_gen(f, 7) == 2.5

    def test_compounding_grows_each_gen(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            kind="compounding", compounding_factor=0.5,
        )
        assert _factor_amount_at_gen(f, 0) == pytest.approx(1.0)
        assert _factor_amount_at_gen(f, 1) == pytest.approx(1.5)
        assert _factor_amount_at_gen(f, 2) == pytest.approx(2.25)

    def test_compounding_with_zero_factor_is_constant(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=0,
            per_generation_amount=3.0, unit="u",
            kind="compounding", compounding_factor=0.0,
        )
        for g in range(5):
            assert _factor_amount_at_gen(f, g) == pytest.approx(3.0)

    def test_one_time_only_at_introduction(self):
        f = GenerationFactor(
            name="setup", introduced_at_generation=0,
            per_generation_amount=10.0, unit="u",
            kind="one_time",
        )
        assert _factor_amount_at_gen(f, 0) == 10.0
        assert _factor_amount_at_gen(f, 1) == 0.0
        assert _factor_amount_at_gen(f, 5) == 0.0

    def test_one_time_at_late_introduction(self):
        f = GenerationFactor(
            name="milestone", introduced_at_generation=3,
            per_generation_amount=5.0, unit="u",
            kind="one_time",
        )
        assert _factor_amount_at_gen(f, 0) == 0.0
        assert _factor_amount_at_gen(f, 2) == 0.0
        assert _factor_amount_at_gen(f, 3) == 5.0
        assert _factor_amount_at_gen(f, 4) == 0.0


# ------------------------------------------------------------
# trace_seven_generations
# ------------------------------------------------------------

class TestTraceSevenGenerations:
    def test_default_eight_generations_returned(self):
        # 0 (present) through 7 inclusive = 8 entries
        trace = trace_seven_generations("p", [])
        assert len(trace.generations) == 8

    def test_year_offsets_correct(self):
        trace = trace_seven_generations("p", [])
        for i, g in enumerate(trace.generations):
            assert g.year_offset_estimate == i * YEARS_PER_GENERATION

    def test_zero_factors_zero_costs(self):
        trace = trace_seven_generations("p", [])
        for g in trace.generations:
            assert g.cost_this_gen == 0.0
            assert g.benefit_this_gen == 0.0
            assert g.net_cumulative() == 0.0

    def test_additive_cost_accumulates_linearly(self):
        f = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost", kind="additive",
        )
        trace = trace_seven_generations("p", [f])
        # gen 0 + 1 + ... + 7 = 8 generations × 1.0 = 8.0
        assert trace.generations[-1].cumulative_cost == pytest.approx(8.0)

    def test_compounding_cost_grows_geometrically(self):
        f = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost", kind="compounding",
            compounding_factor=1.0,   # double each gen
        )
        # 1 + 2 + 4 + 8 + 16 + 32 + 64 + 128 = 255
        trace = trace_seven_generations("p", [f])
        assert trace.generations[-1].cumulative_cost == pytest.approx(255.0)

    def test_benefit_accumulates_separately(self):
        f = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=2.0, unit="u",
            direction="benefit", kind="additive",
        )
        trace = trace_seven_generations("p", [f])
        assert trace.generations[-1].cumulative_benefit == pytest.approx(16.0)
        assert trace.generations[-1].cumulative_cost == 0.0
        assert trace.generations[-1].net_cumulative() == pytest.approx(16.0)

    def test_compound_risk_horizon_detected(self):
        # cost stays ahead of benefit from gen 0
        cost = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=2.0, unit="u",
            direction="cost", kind="additive",
        )
        benefit = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="benefit", kind="additive",
        )
        trace = trace_seven_generations("p", [cost, benefit])
        # net is negative every gen including gen 0 (cost 2 vs benefit 1)
        assert trace.compound_risk_horizon == 0

    def test_compound_risk_horizon_none_when_always_positive(self):
        benefit = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="benefit", kind="additive",
        )
        trace = trace_seven_generations("p", [benefit])
        assert trace.compound_risk_horizon is None

    def test_compound_risk_horizon_late(self):
        # benefit dominates early; compounding cost overtakes by gen N
        benefit = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=10.0, unit="u",
            direction="benefit", kind="additive",
        )
        cost = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost", kind="compounding",
            compounding_factor=2.0,   # triple each gen
        )
        trace = trace_seven_generations("p", [benefit, cost])
        # cost: 1, 3, 9, 27, 81, 243, 729, 2187
        # cumulative cost: 1, 4, 13, 40, 121, 364, 1093, 3280
        # cumulative benefit: 10, 20, 30, 40, 50, 60, 70, 80
        # cost overtakes when cumulative_cost > cumulative_benefit
        # gen 0: 1 vs 10 → benefit; gen 1: 4 vs 20 → benefit;
        # gen 2: 13 vs 30 → benefit; gen 3: 40 vs 40 → tie (net 0);
        # gen 4: 121 vs 50 → cost wins
        # net_cumulative goes negative first at gen 4
        assert trace.compound_risk_horizon == 4

    def test_hidden_at_decision_listed(self):
        visible = GenerationFactor(
            name="v", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            visible_at_decision_time=True,
        )
        hidden = GenerationFactor(
            name="h", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            visible_at_decision_time=False,
        )
        trace = trace_seven_generations("p", [visible, hidden])
        assert trace.hidden_at_decision_time == ["h"]
        assert "v" not in trace.hidden_at_decision_time

    def test_factor_introduced_late(self):
        # factor introduced at gen 3 should not contribute before then
        f = GenerationFactor(
            name="late", introduced_at_generation=3,
            per_generation_amount=2.0, unit="u",
            direction="cost", kind="additive",
        )
        trace = trace_seven_generations("p", [f])
        assert trace.generations[2].cumulative_cost == 0.0
        assert trace.generations[3].cumulative_cost == pytest.approx(2.0)
        # gen 3-7 inclusive = 5 contributions × 2.0 = 10.0
        assert trace.generations[-1].cumulative_cost == pytest.approx(10.0)

    def test_n_generations_override(self):
        trace = trace_seven_generations("p", [], n_generations=3)
        # 0 through 3 inclusive = 4 entries
        assert len(trace.generations) == 4

    def test_n_generations_zero_rejected(self):
        with pytest.raises(ValueError):
            trace_seven_generations("p", [], n_generations=0)

    def test_drivers_listed_per_generation(self):
        f = GenerationFactor(
            name="driver_x", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost",
        )
        trace = trace_seven_generations("p", [f])
        assert "driver_x" in trace.generations[0].cost_drivers

    def test_interpretation_warning_present(self):
        trace = trace_seven_generations("p", [])
        # the warning is load-bearing: marks the trace as accounting-not-
        # prediction. A regression that strips it should fail.
        assert trace.interpretation_warning
        assert "prediction" in trace.interpretation_warning.lower()

    def test_to_dict_round_trip(self):
        f = GenerationFactor(
            name="x", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            visible_at_decision_time=False,
        )
        trace = trace_seven_generations("prop", [f])
        d = trace.to_dict()
        assert d["proposal_id"] == "prop"
        assert "interpretation_warning" in d
        assert "x" in d["hidden_at_decision_time"]
        assert len(d["generations"]) == 8


# ------------------------------------------------------------
# Bridge to C3 temporal_stability
# ------------------------------------------------------------

class TestTraceToTemporalStability7g:
    def test_positive_when_benefit_wins(self):
        f = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="benefit",
        )
        trace = trace_seven_generations("p", [f])
        assert trace_to_temporal_stability_7g(trace) == "positive"

    def test_negative_when_cost_wins(self):
        f = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost",
        )
        trace = trace_seven_generations("p", [f])
        assert trace_to_temporal_stability_7g(trace) == "negative"

    def test_neutral_when_balanced(self):
        cost = GenerationFactor(
            name="c", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="cost",
        )
        benefit = GenerationFactor(
            name="b", introduced_at_generation=0,
            per_generation_amount=1.0, unit="u",
            direction="benefit",
        )
        trace = trace_seven_generations("p", [cost, benefit])
        assert trace_to_temporal_stability_7g(trace) == "neutral"

    def test_unknown_when_empty_trace(self):
        # construct an empty trace artificially
        empty = SevenGenerationTrace(proposal_id="p", generations=[])
        assert trace_to_temporal_stability_7g(empty) == "unknown"


# ------------------------------------------------------------
# Audit-symmetric: extractive vs regenerative demos
# ------------------------------------------------------------

class TestExtractiveVsRegenerative:
    def test_extractive_compound_risk_visible(self):
        # the demo's extractive case must surface compound risk
        # otherwise the framework hasn't earned the "compound costs"
        # claim made in physics/PHYSICS_FIRST_AXIOMS.md
        topsoil = GenerationFactor(
            name="topsoil_depletion",
            introduced_at_generation=0,
            per_generation_amount=2.0, unit="kg_C",
            direction="cost", kind="additive",
            visible_at_decision_time=False,
        )
        myco = GenerationFactor(
            name="mycorrhizae_collapse",
            introduced_at_generation=1,
            per_generation_amount=0.5, unit="recovery_pct",
            direction="cost", kind="compounding",
            compounding_factor=0.25,
            visible_at_decision_time=False,
        )
        yield_premium = GenerationFactor(
            name="yield_premium",
            introduced_at_generation=0,
            per_generation_amount=1.0, unit="harvest",
            direction="benefit", kind="additive",
            visible_at_decision_time=True,
        )
        trace = trace_seven_generations(
            "extractive", [topsoil, myco, yield_premium],
        )
        assert trace.compound_risk_horizon is not None
        assert trace_to_temporal_stability_7g(trace) == "negative"
        # the failures were invisible at decision time
        assert "topsoil_depletion" in trace.hidden_at_decision_time
        assert "mycorrhizae_collapse" in trace.hidden_at_decision_time

    def test_regenerative_no_compound_risk(self):
        setup = GenerationFactor(
            name="setup_cost",
            introduced_at_generation=0,
            per_generation_amount=3.0, unit="person_years",
            direction="cost", kind="one_time",
            visible_at_decision_time=True,
        )
        soil_c = GenerationFactor(
            name="soil_C",
            introduced_at_generation=1,
            per_generation_amount=1.0, unit="kg_C",
            direction="benefit", kind="compounding",
            compounding_factor=0.15,
            visible_at_decision_time=True,
        )
        knowledge = GenerationFactor(
            name="knowledge",
            introduced_at_generation=1,
            per_generation_amount=0.5, unit="generations",
            direction="benefit", kind="compounding",
            compounding_factor=0.10,
            visible_at_decision_time=True,
        )
        trace = trace_seven_generations(
            "regenerative", [setup, soil_c, knowledge],
        )
        # by gen 7 the compounding benefits should have overtaken
        # the one-time setup cost
        assert trace_to_temporal_stability_7g(trace) == "positive"
        # nothing was hidden at decision time
        assert trace.hidden_at_decision_time == []
