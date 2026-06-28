"""Unit tests for physics/substrate_scope_validator.py.

Claim: a substrate's outputs are licensed only inside its competence envelope.
Scope exceedance = task conditions landing in zero-competence cells.

Tests verify: grid() cell-center placement and count, competence() formula
(soft edges, boundary exclusion, multi-axis product), validate() output shape
and correct coverage_frac / blindspot logic, and the demo scenario quantitative
predictions.
"""

import pytest

from physics.substrate_scope_validator import competence, grid, validate


# ---------------------------------------------------------------------------
# grid()
# ---------------------------------------------------------------------------

class TestGrid:
    def test_single_axis_cell_count(self):
        cells = grid({"x": (0, 10, 5)})
        assert len(cells) == 5

    def test_two_axis_cell_count(self):
        cells = grid({"x": (0, 10, 3), "y": (0, 10, 4)})
        assert len(cells) == 12

    def test_three_axis_cell_count(self):
        cells = grid({"a": (0, 1, 2), "b": (0, 1, 3), "c": (0, 1, 4)})
        assert len(cells) == 24

    def test_single_bin_is_midpoint(self):
        cells = grid({"x": (0, 10, 1)})
        assert len(cells) == 1
        assert cells[0]["x"] == pytest.approx(5.0, abs=1e-3)

    def test_two_bins_centers(self):
        cells = grid({"x": (0.0, 10.0, 2)})
        xs = sorted(c["x"] for c in cells)
        assert xs[0] == pytest.approx(2.5, abs=1e-3)
        assert xs[1] == pytest.approx(7.5, abs=1e-3)

    def test_cells_are_dicts(self):
        cells = grid({"x": (0, 1, 3)})
        for c in cells:
            assert isinstance(c, dict)
            assert "x" in c

    def test_all_cells_have_all_axes(self):
        cells = grid({"a": (0, 1, 2), "b": (0, 1, 2)})
        for c in cells:
            assert "a" in c and "b" in c

    def test_values_rounded_to_4dp(self):
        cells = grid({"x": (0, 1, 3)})
        for c in cells:
            # round-tripping at 4dp should leave value unchanged
            assert c["x"] == round(c["x"], 4)

    def test_centers_within_bounds(self):
        cells = grid({"x": (10, 20, 5)})
        for c in cells:
            assert 10 <= c["x"] <= 20

    def test_no_axis_yields_single_empty_dict(self):
        cells = grid({})
        assert cells == [{}]


# ---------------------------------------------------------------------------
# competence()
# ---------------------------------------------------------------------------

class TestCompetence:
    def _env(self):
        return {"x": (0.0, 10.0)}

    def test_outside_low_returns_zero(self):
        assert competence({"x": -1.0}, self._env()) == 0.0

    def test_outside_high_returns_zero(self):
        assert competence({"x": 11.0}, self._env()) == 0.0

    def test_center_near_max(self):
        # center of [0,10] is 5; d=1 → 0.5+0.49=0.99
        val = competence({"x": 5.0}, self._env())
        assert val == pytest.approx(0.99, abs=1e-3)

    def test_at_boundary_low(self):
        # x=0: d=0 → 0.5+0=0.5
        val = competence({"x": 0.0}, self._env())
        assert val == pytest.approx(0.5, abs=1e-3)

    def test_at_boundary_high(self):
        # x=10: d=0 → 0.5
        val = competence({"x": 10.0}, self._env())
        assert val == pytest.approx(0.5, abs=1e-3)

    def test_two_axis_center(self):
        env = {"x": (0.0, 10.0), "y": (0.0, 10.0)}
        # both at center → 0.99 * 0.99 = 0.9801
        val = competence({"x": 5.0, "y": 5.0}, env)
        assert val == pytest.approx(0.9801, abs=1e-3)

    def test_two_axis_one_outside(self):
        env = {"x": (0.0, 10.0), "y": (0.0, 10.0)}
        # y=11 → outside → returns 0
        assert competence({"x": 5.0, "y": 11.0}, env) == 0.0

    def test_returns_float_rounded_to_4dp(self):
        val = competence({"x": 5.0}, self._env())
        assert val == round(val, 4)

    def test_nonnegative(self):
        for x in (-1, 0, 5, 10, 11):
            val = competence({"x": float(x)}, self._env())
            assert val >= 0.0

    def test_never_exceeds_one(self):
        for x in (0.0, 2.5, 5.0, 7.5, 10.0):
            val = competence({"x": x}, self._env())
            assert val <= 1.0

    def test_monotone_from_boundary_to_center(self):
        env = {"x": (0.0, 10.0)}
        v0 = competence({"x": 0.0}, env)
        v2 = competence({"x": 2.0}, env)
        v5 = competence({"x": 5.0}, env)
        assert v0 < v2 < v5

    def test_single_axis_quarter_point(self):
        # x=2.5, span=10, half_span=5, d=min(2.5,7.5)/5=0.5 → 0.5+0.245=0.745
        val = competence({"x": 2.5}, self._env())
        assert val == pytest.approx(0.745, abs=1e-3)

    def test_empty_envelope_returns_one(self):
        # no axes to check → fit stays 1.0
        val = competence({"x": 5.0}, {})
        assert val == pytest.approx(1.0, abs=1e-3)


# ---------------------------------------------------------------------------
# validate() — output shape
# ---------------------------------------------------------------------------

class TestValidateShape:
    def _run(self, n=5):
        axes = {"heat": (0, 100, n), "load": (0, 100, n)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env = {"heat": (10, 70), "load": (0, 60)}
        return validate(task, env, axes)

    def test_returns_dict(self):
        assert isinstance(self._run(), dict)

    def test_required_keys(self):
        out = self._run()
        for key in ("cells", "coverage_frac", "blindspots", "trajectory"):
            assert key in out

    def test_cells_is_int(self):
        assert isinstance(self._run()["cells"], int)

    def test_cells_matches_grid_count(self):
        # 5×5 grid, task=full → all 25 cells in task
        assert self._run(5)["cells"] == 25

    def test_coverage_frac_in_unit_interval(self):
        out = self._run()
        assert 0.0 <= out["coverage_frac"] <= 1.0

    def test_blindspots_is_list(self):
        assert isinstance(self._run()["blindspots"], list)

    def test_blindspots_are_dicts(self):
        out = self._run()
        for b in out["blindspots"]:
            assert isinstance(b, dict)

    def test_trajectory_is_list(self):
        assert isinstance(self._run()["trajectory"], list)

    def test_trajectory_length_matches_cells(self):
        out = self._run()
        assert len(out["trajectory"]) == out["cells"]

    def test_trajectory_sorted_ascending_by_cov(self):
        out = self._run()
        covs = [cov for _, cov in out["trajectory"]]
        assert covs == sorted(covs)

    def test_trajectory_rows_are_cell_cov_pairs(self):
        out = self._run()
        for item in out["trajectory"]:
            cell, cov = item
            assert isinstance(cell, dict)
            assert isinstance(cov, float)


# ---------------------------------------------------------------------------
# validate() — coverage and blindspot correctness
# ---------------------------------------------------------------------------

class TestValidatePhysics:
    def test_full_envelope_no_blindspots(self):
        axes = {"x": (0, 10, 4)}
        task = {"x": (0, 10)}
        env = {"x": (0, 10)}
        out = validate(task, env, axes)
        assert len(out["blindspots"]) == 0
        assert out["coverage_frac"] == pytest.approx(1.0)

    def test_no_overlap_all_blindspots(self):
        # task=[0,10], envelope=[20,30] → zero overlap → all blindspots
        axes = {"x": (0, 10, 4)}
        task = {"x": (0, 10)}
        env = {"x": (20, 30)}
        out = validate(task, env, axes)
        assert out["coverage_frac"] == pytest.approx(0.0)
        assert len(out["blindspots"]) == out["cells"]

    def test_partial_overlap_partial_coverage(self):
        # task covers x=[0,10]; envelope covers x=[5,10] → right half covered
        axes = {"x": (0, 10, 4)}
        task = {"x": (0, 10)}
        env = {"x": (5, 10)}
        out = validate(task, env, axes)
        assert 0.0 < out["coverage_frac"] < 1.0

    def test_blindspot_cells_have_zero_competence(self):
        axes = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env = {"heat": (10, 70), "load": (0, 60)}
        out = validate(task, env, axes)
        for cell in out["blindspots"]:
            assert competence(cell, env) == 0.0

    def test_covered_cells_have_positive_competence(self):
        axes = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env = {"heat": (10, 70), "load": (0, 60)}
        out = validate(task, env, axes)
        covered = [cell for cell, cov in out["trajectory"] if cov > 0.0]
        for cell in covered:
            assert competence(cell, env) > 0.0

    def test_task_subset_fewer_cells(self):
        # task restricted to half the range → fewer cells evaluated
        axes = {"x": (0, 10, 10)}
        full = validate({"x": (0, 10)}, {"x": (0, 10)}, axes)
        half = validate({"x": (0, 5)}, {"x": (0, 10)}, axes)
        assert half["cells"] < full["cells"]

    def test_empty_task_region_zero_cells(self):
        # task range that no grid cell falls within
        axes = {"x": (0, 10, 4)}  # cells at 1.25, 3.75, 6.25, 8.75
        out = validate({"x": (50, 60)}, {"x": (0, 10)}, axes)
        assert out["cells"] == 0
        assert out["coverage_frac"] == pytest.approx(0.0)

    def test_two_axis_blindspot_count(self):
        # any cell outside heat or load envelope → blindspot
        axes = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env = {"heat": (10, 70), "load": (0, 60)}
        out = validate(task, env, axes)
        # manually: blindspots are cells where heat or load outside envelope
        expected_blind = sum(
            1 for cell in grid(axes)
            if all(task[a][0] <= cell[a] <= task[a][1] for a in task)
            and competence(cell, env) == 0.0
        )
        assert len(out["blindspots"]) == expected_blind


# ---------------------------------------------------------------------------
# Demo scenario — quantitative predictions
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _demo(self):
        axes = {"heat": (0, 100, 5), "load": (0, 100, 5)}
        task = {"heat": (0, 100), "load": (0, 100)}
        env = {"heat": (10, 70), "load": (0, 60)}
        return validate(task, env, axes)

    def test_cells_equals_25(self):
        assert self._demo()["cells"] == 25

    def test_coverage_frac_near_expected(self):
        # 5x5 grid, envelope covers 12 of 25 cells fully → approx 0.48
        assert 0.40 <= self._demo()["coverage_frac"] <= 0.60

    def test_blindspots_count_positive(self):
        out = self._demo()
        assert len(out["blindspots"]) > 0

    def test_trajectory_ascending(self):
        out = self._demo()
        covs = [cov for _, cov in out["trajectory"]]
        assert covs == sorted(covs)

    def test_worst_cells_at_envelope_boundary(self):
        # lowest competence cells should be outside or on the edge
        out = self._demo()
        env = {"heat": (10, 70), "load": (0, 60)}
        worst_cov = out["trajectory"][0][1]
        assert worst_cov == pytest.approx(0.0)

    def test_best_cells_near_envelope_center(self):
        out = self._demo()
        best_cov = out["trajectory"][-1][1]
        assert best_cov > 0.5

    def test_blindspot_cells_outside_envelope(self):
        out = self._demo()
        env = {"heat": (10, 70), "load": (0, 60)}
        for cell in out["blindspots"]:
            heat_out = cell["heat"] < 10 or cell["heat"] > 70
            load_out = cell["load"] < 0 or cell["load"] > 60
            assert heat_out or load_out
