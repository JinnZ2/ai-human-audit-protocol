"""Unit tests for physics/frame_projection.py.

Enforces SITUATEDNESS_METROLOGY.md §2.5 (general covariance) in code:
the axis-vector is the covariant object; any scalar is a frame-relative
projection, stamped with its frame name and is_invariant=False.

Tests verify: project() output shape, formula, frame-stamping, empty-weight
edge case, axes_used filtering, negative weights, compare_projections()
spread computation, nonzero spread when frames differ, zero spread when
frames agree, and the demo scenario quantitative values.
"""

import pytest

from physics.frame_projection import project, compare_projections


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _v(**kw):
    return kw


# ---------------------------------------------------------------------------
# project() — output shape
# ---------------------------------------------------------------------------

class TestProjectShape:
    def test_returns_dict(self):
        assert isinstance(project({"x": 0.5}, {"x": 1.0}), dict)

    def test_required_keys(self):
        out = project({"x": 0.5}, {"x": 1.0})
        for k in ("value", "frame", "weights", "axes_used", "is_invariant", "note"):
            assert k in out

    def test_is_invariant_always_false(self):
        assert project({"x": 0.5}, {"x": 1.0})["is_invariant"] is False

    def test_default_frame_name(self):
        assert project({"x": 0.5}, {"x": 1.0})["frame"] == "unnamed"

    def test_custom_frame_name(self):
        assert project({"x": 0.5}, {"x": 1.0}, "my_frame")["frame"] == "my_frame"

    def test_weights_stored(self):
        out = project({"a": 0.3, "b": 0.7}, {"a": 0.5, "b": 0.5})
        assert out["weights"] == {"a": 0.5, "b": 0.5}

    def test_axes_used_only_overlap(self):
        out = project({"a": 0.3, "c": 0.7}, {"a": 0.5, "b": 0.5})
        assert out["axes_used"] == ["a"]

    def test_note_field_is_string(self):
        assert isinstance(project({"x": 0.5}, {"x": 1.0})["note"], str)

    def test_value_rounded_to_4dp(self):
        out = project({"x": 1/3}, {"x": 1.0})
        assert out["value"] == round(out["value"], 4)


# ---------------------------------------------------------------------------
# project() — formula
# ---------------------------------------------------------------------------

class TestProjectFormula:
    def test_single_axis_full_weight(self):
        # value = (0.6 * 1.0) / abs(1.0) = 0.6
        assert project({"x": 0.6}, {"x": 1.0})["value"] == pytest.approx(0.6)

    def test_two_axes_equal_weights(self):
        # (0.4*1 + 0.6*1) / (1+1) = 0.5
        assert project({"a": 0.4, "b": 0.6}, {"a": 1.0, "b": 1.0})["value"] == pytest.approx(0.5)

    def test_two_axes_unequal_weights(self):
        # (0.4*0.3 + 0.6*0.7) / (0.3+0.7) = (0.12+0.42)/1.0 = 0.54
        v = project({"a": 0.4, "b": 0.6}, {"a": 0.3, "b": 0.7})["value"]
        assert v == pytest.approx(0.54, abs=1e-4)

    def test_zero_weight_sum_gives_zero(self):
        # no overlapping keys → wsum=0 → value=0.0
        assert project({"x": 0.9}, {"y": 1.0})["value"] == pytest.approx(0.0)

    def test_missing_axis_ignored(self):
        # "z" not in vector → only "a" used
        out = project({"a": 0.5}, {"a": 1.0, "z": 0.5})
        assert out["value"] == pytest.approx(0.5)
        assert "z" not in out["axes_used"]

    def test_negative_weight_uses_absolute_for_normalization(self):
        # weights: {"x": -1.0} → wsum = abs(-1) = 1
        # value = (0.6 * -1.0) / 1 = -0.6
        out = project({"x": 0.6}, {"x": -1.0})
        assert out["value"] == pytest.approx(-0.6, abs=1e-4)

    def test_mixed_sign_weights(self):
        # a=0.8 w=0.5, b=0.3 w=-0.5 → wsum=1.0 → (0.8*0.5 + 0.3*-0.5)/1.0 = 0.4-0.15=0.25
        out = project({"a": 0.8, "b": 0.3}, {"a": 0.5, "b": -0.5})
        assert out["value"] == pytest.approx(0.25, abs=1e-4)

    def test_empty_vector_gives_zero(self):
        assert project({}, {"x": 1.0})["value"] == pytest.approx(0.0)

    def test_empty_weights_gives_zero(self):
        assert project({"x": 0.5}, {})["value"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# compare_projections() — output shape
# ---------------------------------------------------------------------------

class TestCompareProjectionsShape:
    def test_returns_dict(self):
        assert isinstance(compare_projections({}, []), dict)

    def test_required_keys(self):
        out = compare_projections({"x": 0.5}, [("f", {"x": 1.0})])
        for k in ("projections", "spread", "note"):
            assert k in out

    def test_projections_is_list(self):
        out = compare_projections({"x": 0.5}, [("f1", {"x": 1.0}), ("f2", {"x": 0.5})])
        assert isinstance(out["projections"], list)

    def test_projections_length_matches_frames(self):
        frames = [("f1", {"x": 1.0}), ("f2", {"x": 0.5}), ("f3", {"x": 0.2})]
        out = compare_projections({"x": 0.5}, frames)
        assert len(out["projections"]) == 3

    def test_each_projection_has_is_invariant_false(self):
        out = compare_projections({"x": 0.5}, [("f", {"x": 1.0})])
        for p in out["projections"]:
            assert p["is_invariant"] is False

    def test_empty_frames_gives_zero_spread(self):
        assert compare_projections({"x": 0.5}, [])["spread"] == pytest.approx(0.0)

    def test_note_field_is_string(self):
        out = compare_projections({"x": 0.5}, [("f", {"x": 1.0})])
        assert isinstance(out["note"], str)

    def test_spread_rounded_to_4dp(self):
        frames = [("f1", {"x": 1.0}), ("f2", {"x": 0.0})]
        out = compare_projections({"x": 1/3}, frames)
        assert out["spread"] == round(out["spread"], 4)


# ---------------------------------------------------------------------------
# compare_projections() — spread semantics
# ---------------------------------------------------------------------------

class TestCompareProjectionsSpread:
    def test_zero_spread_when_frames_identical(self):
        v = {"x": 0.5}
        frames = [("f1", {"x": 1.0}), ("f2", {"x": 1.0})]
        assert compare_projections(v, frames)["spread"] == pytest.approx(0.0)

    def test_nonzero_spread_when_frames_differ(self):
        v = {"a": 0.8, "b": 0.2}
        frames = [("f1", {"a": 1.0}), ("f2", {"b": 1.0})]
        out = compare_projections(v, frames)
        assert out["spread"] > 0

    def test_spread_is_max_minus_min(self):
        v = {"x": 0.3, "y": 0.7}
        frames = [("f1", {"x": 1.0}), ("f2", {"y": 1.0})]
        out = compare_projections(v, frames)
        vals = [p["value"] for p in out["projections"]]
        assert out["spread"] == pytest.approx(max(vals) - min(vals), abs=1e-4)

    def test_spread_indicates_frame_dependence(self):
        # nonzero spread = the scalar changes with frame = artifact, not invariant
        v = {"located": 0.3, "grounded_share": 0.9}
        frames = [
            ("heavy_location", {"located": 0.9, "grounded_share": 0.1}),
            ("heavy_grounding", {"located": 0.1, "grounded_share": 0.9}),
        ]
        out = compare_projections(v, frames)
        assert out["spread"] > 0.1

    def test_single_frame_gives_zero_spread(self):
        out = compare_projections({"x": 0.5}, [("f", {"x": 1.0})])
        assert out["spread"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Demo scenario — quantitative values from __main__
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _run(self):
        v = {"located": 0.3, "grounded_share": 0.5, "authored_share": 0.2}
        frames = [
            ("operator_trust",    {"located": 0.5, "grounded_share": 0.5}),
            ("autonomy_weighted", {"authored_share": 0.8, "located": 0.2}),
            ("grounding_only",    {"grounded_share": 1.0}),
        ]
        return compare_projections(v, frames)

    def test_operator_trust_value(self):
        # (0.3*0.5 + 0.5*0.5) / (0.5+0.5) = (0.15+0.25)/1.0 = 0.40
        p = next(p for p in self._run()["projections"] if p["frame"] == "operator_trust")
        assert p["value"] == pytest.approx(0.40, abs=1e-4)

    def test_autonomy_weighted_value(self):
        # authored_share=0.2 in vector, located=0.3
        # wsum = 0.8+0.2=1.0; value=(0.2*0.8+0.3*0.2)/1.0=0.16+0.06=0.22
        p = next(p for p in self._run()["projections"] if p["frame"] == "autonomy_weighted")
        assert p["value"] == pytest.approx(0.22, abs=1e-4)

    def test_grounding_only_value(self):
        # grounded_share=0.5, wsum=1.0 → 0.5
        p = next(p for p in self._run()["projections"] if p["frame"] == "grounding_only")
        assert p["value"] == pytest.approx(0.50, abs=1e-4)

    def test_spread_nonzero(self):
        assert self._run()["spread"] > 0

    def test_spread_value(self):
        # max=0.50, min=0.22 → spread=0.28
        assert self._run()["spread"] == pytest.approx(0.28, abs=1e-4)

    def test_all_projections_not_invariant(self):
        for p in self._run()["projections"]:
            assert p["is_invariant"] is False
