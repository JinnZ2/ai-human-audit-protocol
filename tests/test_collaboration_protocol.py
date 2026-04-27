"""Unit tests for consortium/collaboration_protocol.py.

The collaboration protocol is the layer where geometric frames
read a problem together. These tests cover GeometricFrame, Problem,
FrameReading, MultiGeometryCollaboration, REVERSIBILITY_RANK
ordering, and the AMOC demo.
"""

import pytest

from consortium.collaboration_protocol import (
    GeometricFrame,
    Problem,
    FrameReading,
    MultiGeometryCollaboration,
    REVERSIBILITY_RANK,
    build_consortium_frames,
    example_problem_amoc_response,
)


def _frame(frame_id="f", operator_type="AI_model"):
    return GeometricFrame(
        frame_id=frame_id,
        operator_type=operator_type,
        primitives=["p1"],
        couplings_visible=["v1", "v2"],
        couplings_invisible=["i1"],
        epistemic_strength="inferred",
        confidence_calibration=0.8,
    )


def _problem(problem_id="prob"):
    return Problem(
        problem_id=problem_id,
        presenting_symptoms=["s1"],
        suspected_couplings=["sc1"],
        bounds=("space", "time", "scale"),
        regime_context={"climate": "current"},
        stakes=["st1"],
    )


def _reading(frame, problem_id="prob",
             visible_couplings=None,
             load_bearing=None,
             diagnosis="diag",
             actions=None,
             confidence=0.8):
    return FrameReading(
        frame=frame,
        problem_id=problem_id,
        visible_couplings=visible_couplings or ["v1"],
        load_bearing_elements=load_bearing or ["lb1"],
        invisible_aspects=[],
        proposed_diagnosis=diagnosis,
        proposed_actions=actions or [],
        confidence=confidence,
        assumptions_required=[],
        where_this_frame_breaks=[],
    )


# ------------------------------------------------------------
# REVERSIBILITY_RANK
# ------------------------------------------------------------

class TestReversibilityRank:
    def test_irreversible_if_delayed_ranks_highest(self):
        # cost-of-inaction is unrecoverable; should bubble up
        assert REVERSIBILITY_RANK["irreversible_if_delayed"] >= max(
            v for k, v in REVERSIBILITY_RANK.items()
            if k != "irreversible_if_delayed"
        )

    def test_high_reversibility_above_medium(self):
        assert (REVERSIBILITY_RANK["high_reversibility"]
                > REVERSIBILITY_RANK["medium_reversibility"])

    def test_medium_above_low(self):
        assert (REVERSIBILITY_RANK["medium_reversibility"]
                > REVERSIBILITY_RANK["low_reversibility"])

    def test_irreversible_ranks_low(self):
        # actions you can't undo should be done last (under uncertainty)
        assert (REVERSIBILITY_RANK["irreversible"]
                < REVERSIBILITY_RANK["high_reversibility"])

    def test_unknown_at_bottom(self):
        assert REVERSIBILITY_RANK["unknown"] == min(REVERSIBILITY_RANK.values())


# ------------------------------------------------------------
# Frame / Problem / Reading construction
# ------------------------------------------------------------

class TestConstruction:
    def test_geometric_frame(self):
        f = _frame()
        assert f.frame_id == "f"
        assert f.confidence_calibration == 0.8

    def test_problem(self):
        p = _problem()
        assert p.problem_id == "prob"

    def test_frame_reading(self):
        f = _frame()
        r = _reading(f)
        assert r.frame is f
        assert r.problem_id == "prob"


# ------------------------------------------------------------
# MultiGeometryCollaboration.add_reading
# ------------------------------------------------------------

class TestAddReading:
    def test_starts_empty(self):
        c = MultiGeometryCollaboration(problem=_problem(), frames=[])
        assert c.readings == []

    def test_appends(self):
        f = _frame()
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f])
        c.add_reading(_reading(f))
        assert len(c.readings) == 1


# ------------------------------------------------------------
# surface_invariants
# ------------------------------------------------------------

class TestSurfaceInvariants:
    def test_insufficient_when_under_two_readings(self):
        c = MultiGeometryCollaboration(problem=_problem(), frames=[])
        result = c.surface_invariants()
        assert result.get("insufficient") is True

    def test_converged_label_when_universal_couplings(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, visible_couplings=["a", "b"]))
        c.add_reading(_reading(f2, visible_couplings=["a", "c"]))
        result = c.surface_invariants()
        assert result["convergence"] == "converged"
        assert "a" in result["universal_couplings"]

    def test_divergent_label_when_no_overlap(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, visible_couplings=["a"]))
        c.add_reading(_reading(f2, visible_couplings=["b"]))
        result = c.surface_invariants()
        assert result["convergence"] == "divergent"
        assert result["universal_couplings"] == []

    def test_convergence_note_explains_divergent(self):
        # divergent should NOT be misread as "abandon analysis"
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, visible_couplings=["a"]))
        c.add_reading(_reading(f2, visible_couplings=["b"]))
        result = c.surface_invariants()
        note = result["convergence_note"]
        assert "disagreement" in note.lower() or "geometry" in note.lower()

    def test_load_bearing_intersection(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, load_bearing=["lb_a", "lb_b"]))
        c.add_reading(_reading(f2, load_bearing=["lb_a", "lb_c"]))
        result = c.surface_invariants()
        assert "lb_a" in result["universal_load_bearing"]


# ------------------------------------------------------------
# surface_blind_spots
# ------------------------------------------------------------

class TestSurfaceBlindSpots:
    def test_each_frame_blind_to_others_couplings(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, visible_couplings=["a"]))
        c.add_reading(_reading(f2, visible_couplings=["b"]))
        result = c.surface_blind_spots()
        assert "b" in result["f1"]
        assert "a" in result["f2"]

    def test_no_blind_spots_when_all_match(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, visible_couplings=["a"]))
        c.add_reading(_reading(f2, visible_couplings=["a"]))
        result = c.surface_blind_spots()
        # no missed couplings → no entries
        assert result == {}


# ------------------------------------------------------------
# surface_contradictions
# ------------------------------------------------------------

class TestSurfaceContradictions:
    def test_diagnostic_disagreement_flagged(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, diagnosis="A"))
        c.add_reading(_reading(f2, diagnosis="B"))
        result = c.surface_contradictions()
        assert len(result) == 1
        assert result[0]["frame_a"] == "f1"
        assert result[0]["frame_b"] == "f2"

    def test_same_diagnosis_no_contradiction(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, diagnosis="same"))
        c.add_reading(_reading(f2, diagnosis="same"))
        assert c.surface_contradictions() == []


# ------------------------------------------------------------
# synthesize
# ------------------------------------------------------------

class TestSynthesize:
    def _basic(self):
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1,
                               visible_couplings=["a"],
                               actions=[("act_safe", "high_reversibility")]))
        c.add_reading(_reading(f2,
                               visible_couplings=["a"],
                               actions=[("act_urgent", "irreversible_if_delayed")]))
        return c

    def test_keys_present(self):
        result = self._basic().synthesize()
        for k in ("problem_id", "frames_consulted", "invariant_geometry",
                  "blind_spots_per_frame", "productive_disagreements",
                  "time_critical_actions",
                  "actions_ranked_by_support_and_reversibility",
                  "epistemic_warning"):
            assert k in result

    def test_time_critical_surfaces_irreversible_if_delayed(self):
        result = self._basic().synthesize()
        actions = [a["action"] for a in result["time_critical_actions"]]
        assert "act_urgent" in actions

    def test_irreversible_if_delayed_ranks_first(self):
        result = self._basic().synthesize()
        ranked = result["actions_ranked_by_support_and_reversibility"]
        assert ranked[0]["action"] == "act_urgent"

    def test_actions_have_reversibility_rank(self):
        result = self._basic().synthesize()
        for a in result["actions_ranked_by_support_and_reversibility"]:
            assert "reversibility_rank" in a

    def test_fraction_support_reflects_overlap(self):
        # if both frames propose the same action, fraction_support = 1.0
        f1, f2 = _frame("f1"), _frame("f2")
        c = MultiGeometryCollaboration(problem=_problem(), frames=[f1, f2])
        c.add_reading(_reading(f1, actions=[("shared", "high_reversibility")]))
        c.add_reading(_reading(f2, actions=[("shared", "high_reversibility")]))
        result = c.synthesize()
        # both readings list the same action
        ranked = result["actions_ranked_by_support_and_reversibility"]
        shared = [a for a in ranked if a["action"] == "shared"]
        # both list it, support count is 2 / 2 readings
        assert any(a["fraction_support"] == 1.0 for a in shared)

    def test_epistemic_warning_present(self):
        result = self._basic().synthesize()
        assert "geometry" in result["epistemic_warning"].lower()


# ------------------------------------------------------------
# build_consortium_frames
# ------------------------------------------------------------

class TestBuildConsortiumFrames:
    def test_seven_frames(self):
        frames = build_consortium_frames()
        assert len(frames) == 7

    def test_all_distinct_ids(self):
        frames = build_consortium_frames()
        ids = [f.frame_id for f in frames]
        assert len(set(ids)) == len(ids)

    def test_includes_embodied_and_ecological(self):
        frames = build_consortium_frames()
        ids = {f.frame_id for f in frames}
        assert "embodied_sensor" in ids
        assert "ecological_signal" in ids
        assert "generational_transmission" in ids

    def test_each_frame_has_required_attributes(self):
        for f in build_consortium_frames():
            assert f.frame_id
            assert f.operator_type
            assert f.primitives
            assert f.couplings_visible
            assert 0.0 <= f.confidence_calibration <= 1.0


# ------------------------------------------------------------
# AMOC demo smoke test
# ------------------------------------------------------------

class TestAmocDemo:
    def test_demo_constructs(self):
        c = example_problem_amoc_response()
        assert isinstance(c, MultiGeometryCollaboration)
        assert c.problem.problem_id.startswith("upper_midwest")

    def test_demo_synthesizes_without_error(self):
        c = example_problem_amoc_response()
        result = c.synthesize()
        assert result["problem_id"] == c.problem.problem_id

    def test_demo_includes_at_least_three_readings(self):
        c = example_problem_amoc_response()
        assert len(c.readings) >= 3
