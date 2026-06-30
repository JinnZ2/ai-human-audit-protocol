"""Unit tests for physics/breadcrumb_preservation.py.

Claim: redundant multi-carrier encoding raises information survival under
carrier-loss shocks vs single-carrier.

Tests verify: item_survival() formula (P(at least one survives)), edge cases
(empty, single, full carrier set), consolidation_sweep() trajectory shape and
ordering, loss_under_consolidation() loss calculation, and the demo scenario
cliff prediction.
"""

import pytest

from physics.breadcrumb_preservation import (
    CARRIERS,
    consolidation_sweep,
    item_survival,
    loss_under_consolidation,
)


# ---------------------------------------------------------------------------
# item_survival()
# ---------------------------------------------------------------------------

class TestItemSurvival:
    def test_empty_carriers_zero_survival(self):
        # no carriers → fail = 1.0 → survival = 0.0
        assert item_survival([]) == pytest.approx(0.0)

    def test_single_carrier_narrative(self):
        assert item_survival(["narrative"]) == pytest.approx(CARRIERS["narrative"])

    def test_single_carrier_material(self):
        assert item_survival(["material"]) == pytest.approx(CARRIERS["material"])

    def test_two_carriers_higher_than_each_alone(self):
        s1 = item_survival(["narrative"])
        s2 = item_survival(["material"])
        s12 = item_survival(["narrative", "material"])
        assert s12 > s1
        assert s12 > s2

    def test_all_carriers_near_one(self):
        # with all five carriers, very few shocks kill everything
        s = item_survival(list(CARRIERS.keys()))
        assert s > 0.95

    def test_formula_correctness_two_carriers(self):
        # P(survive) = 1 - (1-0.55)*(1-0.70)
        expected = 1.0 - (1.0 - 0.55) * (1.0 - 0.70)
        assert item_survival(["narrative", "material"]) == pytest.approx(expected, abs=1e-6)

    def test_formula_correctness_three_carriers(self):
        p = 1.0 - (1.0 - CARRIERS["narrative"]) * (1.0 - CARRIERS["practice"]) * (1.0 - CARRIERS["material"])
        assert item_survival(["narrative", "practice", "material"]) == pytest.approx(p, abs=1e-6)

    def test_adding_carrier_never_decreases_survival(self):
        base = item_survival(["narrative"])
        for name in CARRIERS:
            s = item_survival(["narrative", name])
            assert s >= base

    def test_carrier_order_does_not_matter(self):
        a = item_survival(["narrative", "material"])
        b = item_survival(["material", "narrative"])
        assert a == pytest.approx(b)

    def test_result_in_unit_interval(self):
        for name in CARRIERS:
            s = item_survival([name])
            assert 0.0 <= s <= 1.0


# ---------------------------------------------------------------------------
# CARRIERS constant
# ---------------------------------------------------------------------------

class TestCarriersConstant:
    def test_all_five_carriers_present(self):
        for name in ("narrative", "practice", "material", "ritual", "calendrical"):
            assert name in CARRIERS

    def test_all_priors_in_unit_interval(self):
        for name, p in CARRIERS.items():
            assert 0.0 < p < 1.0, f"{name} prior out of range"

    def test_practice_lowest(self):
        assert CARRIERS["practice"] == min(CARRIERS.values())

    def test_material_highest(self):
        assert CARRIERS["material"] == max(CARRIERS.values())


# ---------------------------------------------------------------------------
# consolidation_sweep()
# ---------------------------------------------------------------------------

class TestConsolidationSweep:
    def test_returns_list(self):
        assert isinstance(consolidation_sweep(), list)

    def test_length_equals_carrier_count(self):
        # one row per N from len(CARRIERS) down to 1
        assert len(consolidation_sweep()) == len(CARRIERS)

    def test_first_row_uses_all_carriers(self):
        rows = consolidation_sweep()
        n, used, surv = rows[0]
        assert n == len(CARRIERS)
        assert len(used) == len(CARRIERS)

    def test_last_row_uses_one_carrier(self):
        rows = consolidation_sweep()
        n, used, surv = rows[-1]
        assert n == 1
        assert len(used) == 1

    def test_n_values_descending(self):
        rows = consolidation_sweep()
        ns = [r[0] for r in rows]
        assert ns == sorted(ns, reverse=True)

    def test_survival_descending(self):
        # more carriers → higher survival → rows sorted from high to low
        rows = consolidation_sweep()
        survs = [r[2] for r in rows]
        assert survs == sorted(survs, reverse=True)

    def test_survival_values_rounded_to_4dp(self):
        rows = consolidation_sweep()
        for _, _, surv in rows:
            assert surv == round(surv, 4)

    def test_custom_subset_two_carriers(self):
        # pass a two-element subset of real carrier names
        rows = consolidation_sweep(["narrative", "material"])
        assert len(rows) == 2

    def test_each_row_has_three_elements(self):
        for row in consolidation_sweep():
            assert len(row) == 3

    def test_survival_matches_item_survival(self):
        rows = consolidation_sweep()
        for n, used, surv in rows:
            assert surv == pytest.approx(item_survival(used), abs=1e-4)


# ---------------------------------------------------------------------------
# loss_under_consolidation()
# ---------------------------------------------------------------------------

class TestLossUnderConsolidation:
    def _rows(self):
        return loss_under_consolidation(consolidation_sweep())

    def test_returns_list(self):
        assert isinstance(self._rows(), list)

    def test_same_length_as_sweep(self):
        assert len(self._rows()) == len(consolidation_sweep())

    def test_each_row_has_four_elements(self):
        for row in self._rows():
            assert len(row) == 4

    def test_first_loss_is_zero(self):
        # full carrier set → loss vs full = 0
        rows = self._rows()
        n, used, surv, loss = rows[0]
        assert loss == pytest.approx(0.0, abs=1e-4)

    def test_loss_increases_as_carriers_removed(self):
        rows = self._rows()
        losses = [r[3] for r in rows]
        assert losses == sorted(losses)

    def test_last_loss_largest(self):
        rows = self._rows()
        losses = [r[3] for r in rows]
        assert losses[-1] == max(losses)

    def test_loss_nonnegative(self):
        for _, _, _, loss in self._rows():
            assert loss >= 0.0

    def test_loss_equals_full_minus_surv(self):
        rows = loss_under_consolidation(consolidation_sweep())
        full_surv = rows[0][2]
        for n, used, surv, loss in rows:
            assert loss == pytest.approx(full_surv - surv, abs=1e-4)

    def test_survival_values_preserved(self):
        sweep_rows = consolidation_sweep()
        loss_rows = loss_under_consolidation(sweep_rows)
        for (_, _, s_sweep), (_, _, s_loss, _) in zip(sweep_rows, loss_rows):
            assert s_sweep == s_loss


# ---------------------------------------------------------------------------
# Demo scenario — cliff prediction
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _loss_rows(self):
        return loss_under_consolidation(consolidation_sweep())

    def test_full_survival_near_1(self):
        rows = self._loss_rows()
        assert rows[0][2] > 0.95

    def test_single_carrier_survival_equals_narrative_prior(self):
        # last row uses first carrier in CARRIERS (narrative=0.55)
        rows = self._loss_rows()
        n, used, surv, loss = rows[-1]
        assert surv == pytest.approx(CARRIERS[used[0]], abs=1e-4)

    def test_cliff_at_single_carrier_transition(self):
        # biggest drop should be at the 2→1 transition
        rows = self._loss_rows()
        drops = [(rows[i-1][2] - rows[i][2], rows[i][0]) for i in range(1, len(rows))]
        cliff_drop, cliff_n = max(drops)
        assert cliff_n == 1  # cliff is dropping to 1 carrier

    def test_cliff_drop_above_threshold(self):
        rows = self._loss_rows()
        drops = [(rows[i-1][2] - rows[i][2], rows[i][0]) for i in range(1, len(rows))]
        cliff_drop, _ = max(drops)
        assert cliff_drop > 0.10  # non-trivial cliff

    def test_monotone_survival(self):
        rows = self._loss_rows()
        survs = [r[2] for r in rows]
        assert survs == sorted(survs, reverse=True)
