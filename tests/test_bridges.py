"""Unit tests for consortium/bridges.py.

The bridge layer connects FrameReading ↔ Primitive ↔ ClaimNode.
Each function declares what it preserves and what it drops; these
tests enforce the preservation claims and verify the structural
contracts of the forward pipeline.
"""

from datetime import datetime, timezone

import pytest

from consortium.bridges import (
    EPI_TO_FRAME,
    EPI_TO_DOMAIN,
    TRAJECTORY_SHAPES,
    BridgeReport,
    select_frame,
    select_frame_for_reading,
    reading_to_primitives,
    frame_reading_to_primitives,
    primitives_to_claim_graph,
    trajectory_summary,
    classify_trajectory,
    trajectory_to_frame_reading,
    all_bridge_reports,
    _zero_rate,
    _compute_load_bearing,
    _synthesize_diagnosis,
    _derive_confidence,
)
from consortium.collaboration_protocol import (
    GeometricFrame,
    FrameReading,
    build_consortium_frames,
)
from consortium.ontology_layer import Primitive
from consortium.kfc_runtime import ClaimNode
from consortium.embodied_sensor import (
    EmbodiedReading,
    CoatingProbeResult,
    EPI_SUBTAGS,
)


NOW = datetime(2026, 4, 27, 14, 0, tzinfo=timezone.utc)


def _probe():
    return CoatingProbeResult(probe_name="not_run", result="not_run")


def _reading(**overrides):
    base = dict(
        sensor_id="test:sensor:1",
        operator_type="human",
        location=(0.0, 0.0),
        timestamp=NOW,
        observation="test observation",
        claim_refs=["claim_a", "claim_b"],
        epi="kinesthetic",
        confidence=0.9,
        conditions={},
        coating_probe=_probe(),
    )
    base.update(overrides)
    return EmbodiedReading(**base)


def _frame_reading(frame, **overrides):
    base = dict(
        frame=frame,
        problem_id="prob_test",
        visible_couplings=["coupling_x", "coupling_y"],
        load_bearing_elements=["element_z"],
        invisible_aspects=[],
        proposed_diagnosis="test diagnosis",
        proposed_actions=[("act_1", "high_reversibility")],
        confidence=0.8,
        assumptions_required=[],
        where_this_frame_breaks=[],
    )
    base.update(overrides)
    return FrameReading(**base)


# ------------------------------------------------------------
# Default mappings
# ------------------------------------------------------------

class TestMappings:
    def test_epi_to_frame_covers_all_epi_subtags(self):
        # every epi sub-tag should have a default frame mapping
        assert set(EPI_TO_FRAME.keys()) == EPI_SUBTAGS

    def test_epi_to_domain_covers_all_epi_subtags(self):
        assert set(EPI_TO_DOMAIN.keys()) == EPI_SUBTAGS

    def test_direct_sensing_routes_to_embodied_or_ecological(self):
        # the operator-agnostic claim: visual reading routes the same
        # way regardless of who/what produced it
        assert EPI_TO_FRAME["visual"] in {"embodied_sensor",
                                           "ecological_signal"}
        assert EPI_TO_FRAME["instrumental"] == "embodied_sensor"
        assert EPI_TO_FRAME["phenological"] == "ecological_signal"


# ------------------------------------------------------------
# select_frame
# ------------------------------------------------------------

class TestSelectFrame:
    def setup_method(self):
        self.frames = {f.frame_id: f for f in build_consortium_frames()}

    def test_default_routing_by_epi(self):
        f = select_frame("kinesthetic", self.frames)
        assert f.frame_id == "embodied_sensor"

    def test_override_takes_precedence(self):
        f = select_frame("kinesthetic", self.frames,
                         override="thermodynamic_geometry")
        assert f.frame_id == "thermodynamic_geometry"

    def test_invalid_override_raises(self):
        with pytest.raises(KeyError):
            select_frame("kinesthetic", self.frames, override="nonexistent")

    def test_unknown_epi_raises_without_override(self):
        with pytest.raises(ValueError, match="no frame mapping"):
            select_frame("imaginary_epi", self.frames)

    def test_select_frame_for_reading(self):
        r = _reading(epi="phenological")
        f = select_frame_for_reading(r, self.frames)
        assert f.frame_id == "ecological_signal"


# ------------------------------------------------------------
# reading_to_primitives
# ------------------------------------------------------------

class TestReadingToPrimitives:
    def test_one_primitive_per_claim_ref(self):
        r = _reading(claim_refs=["a", "b", "c"])
        prims = reading_to_primitives(r)
        assert len(prims) == 3
        assert {p.concept_id for p in prims} == {"a", "b", "c"}

    def test_empty_claim_refs_returns_empty(self):
        r = _reading(claim_refs=[])
        assert reading_to_primitives(r) == []

    def test_preserves_confidence(self):
        r = _reading(confidence=0.87)
        prims = reading_to_primitives(r)
        assert all(p.epi_confidence == 0.87 for p in prims)

    def test_default_domain_from_epi(self):
        r = _reading(epi="phenological")
        prims = reading_to_primitives(r)
        assert all(p.domain == "ecological" for p in prims)

    def test_explicit_domain_override(self):
        r = _reading()
        prims = reading_to_primitives(r, domain="custom_domain")
        assert all(p.domain == "custom_domain" for p in prims)

    def test_first_primitive_carries_full_observation(self):
        r = _reading(claim_refs=["a", "b"], observation="the actual obs")
        prims = reading_to_primitives(r)
        first = next(p for p in prims if p.concept_id == "a")
        assert "the actual obs" in first.form

    def test_subsequent_primitives_back_reference(self):
        r = _reading(claim_refs=["a", "b", "c"], observation="x")
        prims = reading_to_primitives(r)
        non_first = [p for p in prims if p.concept_id != "a"]
        assert all("[ref:a]" in p.form for p in non_first)

    def test_couplings_exclude_self(self):
        r = _reading(claim_refs=["a", "b", "c"])
        prims = reading_to_primitives(r)
        for p in prims:
            assert p.concept_id not in p.couplings

    def test_bounds_include_location_and_timestamp(self):
        loc = (47.0, -92.0)
        r = _reading(location=loc, claim_refs=["a"])
        prims = reading_to_primitives(r)
        spatial, temporal, scale = prims[0].bounds
        assert spatial == loc
        assert temporal == NOW.isoformat()


# ------------------------------------------------------------
# frame_reading_to_primitives
# ------------------------------------------------------------

class TestFrameReadingToPrimitives:
    def setup_method(self):
        self.frames = {f.frame_id: f for f in build_consortium_frames()}

    def test_one_primitive_per_visible_coupling(self):
        fr = _frame_reading(self.frames["embodied_sensor"],
                            visible_couplings=["x", "y", "z"])
        prims = frame_reading_to_primitives(fr)
        assert len(prims) == 3
        assert {p.concept_id for p in prims} == {"x", "y", "z"}

    def test_empty_visible_couplings_returns_empty(self):
        fr = _frame_reading(self.frames["embodied_sensor"],
                            visible_couplings=[])
        assert frame_reading_to_primitives(fr) == []

    def test_preserves_confidence(self):
        fr = _frame_reading(self.frames["embodied_sensor"],
                            confidence=0.55)
        prims = frame_reading_to_primitives(fr)
        assert all(p.epi_confidence == 0.55 for p in prims)

    def test_default_domain_is_frame_id(self):
        fr = _frame_reading(self.frames["pattern_spatial"])
        prims = frame_reading_to_primitives(fr)
        assert all(p.domain == "pattern_spatial" for p in prims)

    def test_form_records_origin_frame(self):
        fr = _frame_reading(self.frames["embodied_sensor"])
        prims = frame_reading_to_primitives(fr)
        assert all("[frame:embodied_sensor]" in p.form for p in prims)

    def test_couplings_exclude_self(self):
        fr = _frame_reading(self.frames["embodied_sensor"],
                            visible_couplings=["x", "y", "z"])
        prims = frame_reading_to_primitives(fr)
        for p in prims:
            assert p.concept_id not in p.couplings


# ------------------------------------------------------------
# primitives_to_claim_graph
# ------------------------------------------------------------

class TestPrimitivesToClaimGraph:
    def _prim(self, cid, couplings=None):
        return Primitive(
            concept_id=cid,
            domain="test",
            form="test_form",
            role="claim",
            couplings=couplings or [],
            bounds=("space", "time", "scale"),
            epi="measured",
            epi_confidence=0.8,
        )

    def test_one_node_per_primitive(self):
        prims = [self._prim("a"), self._prim("b"), self._prim("c")]
        g = primitives_to_claim_graph(prims)
        assert set(g.keys()) == {"a", "b", "c"}

    def test_zero_rate_default(self):
        prims = [self._prim("a")]
        g = primitives_to_claim_graph(prims)
        # default is _zero_rate
        assert g["a"].rate_fn(0.0, {}, {}) == 0.0

    def test_supplied_rate_fn_used(self):
        prims = [self._prim("a")]
        custom = lambda s, rel, ctx: s + 1
        g = primitives_to_claim_graph(prims, rate_fns={"a": custom})
        assert g["a"].rate_fn(5.0, {}, {}) == 6.0

    def test_preserves_couplings_as_rel(self):
        prims = [self._prim("a", couplings=["b", "c"])]
        g = primitives_to_claim_graph(prims)
        assert g["a"].rel == ["b", "c"]

    def test_preserves_bounds(self):
        prims = [self._prim("a")]
        g = primitives_to_claim_graph(prims)
        assert g["a"].bounds == ("space", "time", "scale")

    def test_default_cyc(self):
        prims = [self._prim("a")]
        g = primitives_to_claim_graph(prims)
        assert g["a"].cyc == 1

    def test_explicit_cyc(self):
        prims = [self._prim("a")]
        g = primitives_to_claim_graph(prims, cyc=2)
        assert g["a"].cyc == 2

    def test_collision_last_wins(self):
        # documented behavior: caller dedupes; if not, last wins
        prims = [self._prim("a", couplings=["x"]),
                 self._prim("a", couplings=["y"])]
        g = primitives_to_claim_graph(prims)
        assert g["a"].rel == ["y"]


# ------------------------------------------------------------
# trajectory_summary (v1 stub)
# ------------------------------------------------------------

class TestTrajectorySummary:
    def test_empty_trajectory(self):
        s = trajectory_summary({})
        assert s["claim_count"] == 0
        assert s["claims"] == {}
        assert s["felt_events"] == []
        assert "_note" in s

    def test_increasing_direction(self):
        s = trajectory_summary({"a": [1.0, 2.0, 3.0]})
        assert s["claims"]["a"]["direction"] == "increasing"
        assert s["claims"]["a"]["delta"] == pytest.approx(2.0)

    def test_decreasing_direction(self):
        s = trajectory_summary({"a": [3.0, 2.0, 1.0]})
        assert s["claims"]["a"]["direction"] == "decreasing"

    def test_stable_direction(self):
        s = trajectory_summary({"a": [1.0, 1.0, 1.0]})
        assert s["claims"]["a"]["direction"] == "stable"

    def test_no_steps(self):
        s = trajectory_summary({"a": []})
        assert s["claims"]["a"]["direction"] == "no_steps"

    def test_underscore_keys_are_felt_events(self):
        s = trajectory_summary({
            "a": [1.0, 2.0],
            "_felt": ["FELT_TRIGGER coherence=0.30"],
        })
        assert s["claim_count"] == 1
        assert s["felt_events"] == ["FELT_TRIGGER coherence=0.30"]

    def test_note_points_to_full_lift(self):
        # the lightweight summary must direct callers to the full
        # inverse lift so they don't mistake the summary for a
        # FrameReading
        s = trajectory_summary({"a": [1.0]})
        assert "trajectory_to_frame_reading" in s["_note"]


# ------------------------------------------------------------
# Bridge reports
# ------------------------------------------------------------

class TestBridgeReports:
    def test_all_reports_returned(self):
        reports = all_bridge_reports()
        names = {r.bridge_name for r in reports}
        assert names == {
            "reading_to_primitives",
            "frame_reading_to_primitives",
            "primitives_to_claim_graph",
            "primitives_to_typed_claim_graph",
            "trajectory_summary",
            "trajectory_to_frame_reading",
        }

    def test_every_report_declares_preserves_and_lossy(self):
        for r in all_bridge_reports():
            assert isinstance(r, BridgeReport)
            assert r.preserves, f"{r.bridge_name} declares no preserves"
            assert r.lossy_on, f"{r.bridge_name} declares no lossy_on"

    def test_trajectory_to_frame_reading_report_flags_coating_risk(self):
        from consortium.bridges import trajectory_to_frame_reading_report
        r = trajectory_to_frame_reading_report()
        # the inverse bridge MUST flag itself as a coating risk because
        # classification is a frame imposed on numbers
        assert ("coating" in r.notes.lower()
                or "heuristic" in r.notes.lower())

    def test_all_reports_include_inverse_bridge(self):
        names = {r.bridge_name for r in all_bridge_reports()}
        assert "trajectory_to_frame_reading" in names


# ------------------------------------------------------------
# Trajectory shape classification
# ------------------------------------------------------------

class TestClassifyTrajectory:
    def test_empty(self):
        assert classify_trajectory([]) == "no_steps"

    def test_single_point(self):
        assert classify_trajectory([1.0]) == "single_point"

    def test_stable(self):
        assert classify_trajectory([1.0, 1.0, 1.0, 1.0]) == "stable"

    def test_stable_within_epsilon(self):
        assert classify_trajectory([1.0, 1.0 + 1e-9, 1.0]) == "stable"

    def test_monotonic_increase(self):
        # roughly linear increase
        s = [0.0, 1.0, 2.0, 3.0, 4.0]
        assert classify_trajectory(s) == "monotonic_increase"

    def test_monotonic_decrease(self):
        s = [4.0, 3.0, 2.0, 1.0, 0.0]
        assert classify_trajectory(s) == "monotonic_decrease"

    def test_saturating_increase(self):
        # large jumps early, small jumps late
        s = [0.0, 5.0, 9.0, 9.5, 9.6, 9.65, 9.66]
        assert classify_trajectory(s) == "saturating_increase"

    def test_saturating_decrease(self):
        s = [10.0, 5.0, 1.0, 0.5, 0.4, 0.35, 0.34]
        assert classify_trajectory(s) == "saturating_decrease"

    def test_accelerating_increase(self):
        # small jumps early, large jumps late (think exponential)
        s = [0.0, 0.1, 0.2, 0.3, 1.0, 3.0, 9.0]
        assert classify_trajectory(s) == "accelerating_increase"

    def test_oscillating(self):
        # multiple sign changes
        s = [0.0, 1.0, -1.0, 1.0, -1.0, 1.0]
        assert classify_trajectory(s) == "oscillating"

    def test_mixed_when_not_oscillating_enough(self):
        # one sign change → not oscillating, not strictly monotonic
        s = [0.0, 1.0, 2.0, 1.0]   # only one sign change in deltas
        assert classify_trajectory(s) == "mixed"

    def test_known_shapes_set(self):
        # every output of classify_trajectory must be in TRAJECTORY_SHAPES
        cases = [
            [], [1.0], [1.0, 1.0],
            [0.0, 1.0, 2.0, 3.0], [3.0, 2.0, 1.0, 0.0],
            [0.0, 5.0, 9.0, 9.5], [10.0, 5.0, 1.0, 0.5],
            [0.0, 0.1, 0.2, 1.0, 3.0],
            [0.0, 1.0, -1.0, 1.0, -1.0],
            [0.0, 1.0, 2.0, 1.0],
        ]
        for s in cases:
            assert classify_trajectory(s) in TRAJECTORY_SHAPES


# ------------------------------------------------------------
# Load-bearing detection
# ------------------------------------------------------------

class TestComputeLoadBearing:
    def test_excludes_underscore_keys(self):
        traj = {
            "a": [0.0, 5.0],
            "_felt": ["FELT_TRIGGER"],
        }
        assert "_felt" not in _compute_load_bearing(traj)

    def test_orders_by_total_delta(self):
        traj = {
            "small_move": [0.0, 0.1],
            "big_move":   [0.0, 10.0],
            "no_move":    [1.0, 1.0],
        }
        result = _compute_load_bearing(traj, top_n=3)
        assert result[0] == "big_move"

    def test_skips_empty_series(self):
        traj = {"a": [], "b": [0.0, 5.0]}
        result = _compute_load_bearing(traj)
        assert "a" not in result
        assert "b" in result

    def test_top_n_caps_output(self):
        traj = {f"c{i}": [0.0, float(i)] for i in range(10)}
        result = _compute_load_bearing(traj, top_n=3)
        assert len(result) == 3


# ------------------------------------------------------------
# Diagnosis synthesis
# ------------------------------------------------------------

class TestSynthesizeDiagnosis:
    def test_felt_dominates(self):
        d = _synthesize_diagnosis(
            shapes={"a": "stable"},
            felt_events=["FELT_TRIGGER"],
        )
        assert "FELT_TRIGGER" in d
        assert "regime drift" in d.lower() or "coherence" in d.lower()

    def test_accelerating_called_divergent(self):
        d = _synthesize_diagnosis(
            shapes={"a": "accelerating_increase"},
            felt_events=[],
        )
        assert "divergent" in d.lower()

    def test_oscillating_named(self):
        d = _synthesize_diagnosis(
            shapes={"a": "oscillating"},
            felt_events=[],
        )
        assert "oscillation" in d.lower()

    def test_saturating_named(self):
        d = _synthesize_diagnosis(
            shapes={"a": "saturating_increase"},
            felt_events=[],
        )
        assert "saturation" in d.lower()

    def test_all_stable(self):
        d = _synthesize_diagnosis(
            shapes={"a": "stable", "b": "stable"},
            felt_events=[],
        )
        assert "stable" in d.lower()


# ------------------------------------------------------------
# Confidence derivation
# ------------------------------------------------------------

class TestDeriveConfidence:
    def test_clean_trajectory_above_50pct(self):
        c = _derive_confidence(shapes={"a": "stable"}, felt_events=[])
        assert c > 0.5

    def test_felt_lowers(self):
        clean = _derive_confidence({"a": "stable"}, [])
        with_felt = _derive_confidence({"a": "stable"}, ["FELT_TRIGGER"])
        assert with_felt < clean

    def test_felt_floor(self):
        c = _derive_confidence({"a": "stable"},
                               ["F1", "F2", "F3", "F4", "F5"])
        assert c >= 0.30

    def test_oscillating_lowers(self):
        clean = _derive_confidence({"a": "stable"}, [])
        osc = _derive_confidence({"a": "oscillating"}, [])
        assert osc < clean

    def test_mixed_lowers(self):
        clean = _derive_confidence({"a": "stable"}, [])
        mixed = _derive_confidence({"a": "mixed"}, [])
        assert mixed < clean

    def test_in_unit_interval(self):
        c = _derive_confidence({"a": "stable"}, [])
        assert 0.0 <= c <= 1.0


# ------------------------------------------------------------
# trajectory_to_frame_reading (full inverse lift)
# ------------------------------------------------------------

class TestTrajectoryToFrameReading:
    def setup_method(self):
        self.frames = {f.frame_id: f for f in build_consortium_frames()}

    def test_produces_frame_reading(self):
        traj = {"a": [0.0, 1.0, 2.0]}
        fr = trajectory_to_frame_reading(
            traj, self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert isinstance(fr, FrameReading)
        assert fr.problem_id == "prob_x"

    def test_visible_couplings_from_claim_ids(self):
        traj = {"a": [0.0, 1.0], "b": [0.0, 2.0]}
        fr = trajectory_to_frame_reading(
            traj, self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert set(fr.visible_couplings) == {"a", "b"}

    def test_underscore_keys_excluded_from_visible(self):
        traj = {"a": [0.0, 1.0], "_felt": ["FELT_TRIGGER"]}
        fr = trajectory_to_frame_reading(
            traj, self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert "_felt" not in fr.visible_couplings

    def test_load_bearing_populated(self):
        traj = {"big": [0.0, 10.0], "small": [0.0, 0.01]}
        fr = trajectory_to_frame_reading(
            traj, self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert "big" in fr.load_bearing_elements

    def test_assumptions_carry_audit_metadata(self):
        traj = {"a": [0.0, 1.0]}
        fr = trajectory_to_frame_reading(
            traj, self.frames["thermodynamic_geometry"], "prob_x",
        )
        joined = " ".join(fr.assumptions_required)
        assert "trajectory_classification=heuristic_v1" in joined
        assert "shapes=" in joined
        assert "felt_events_count=" in joined

    def test_felt_events_lower_confidence(self):
        clean = trajectory_to_frame_reading(
            {"a": [0.0, 1.0, 2.0]},
            self.frames["thermodynamic_geometry"], "prob_x",
        )
        noisy = trajectory_to_frame_reading(
            {"a": [0.0, 1.0, 2.0], "_felt": ["F1", "F2"]},
            self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert noisy.confidence < clean.confidence

    def test_default_proposed_actions_empty(self):
        fr = trajectory_to_frame_reading(
            {"a": [0.0, 1.0]},
            self.frames["thermodynamic_geometry"], "prob_x",
        )
        assert fr.proposed_actions == []

    def test_explicit_proposed_actions(self):
        fr = trajectory_to_frame_reading(
            {"a": [0.0, 1.0]},
            self.frames["thermodynamic_geometry"], "prob_x",
            proposed_actions=[("respond", "high_reversibility")],
        )
        assert fr.proposed_actions == [("respond", "high_reversibility")]

    def test_where_breaks_carries_frame_blind_spots(self):
        frame = self.frames["thermodynamic_geometry"]
        fr = trajectory_to_frame_reading(
            {"a": [0.0, 1.0]}, frame, "prob_x",
        )
        assert fr.where_this_frame_breaks == list(frame.couplings_invisible)

    def test_round_trip_lift_into_collaboration(self):
        # the FrameReading produced by the inverse lift must be valid
        # input for MultiGeometryCollaboration without raising
        from consortium.collaboration_protocol import (
            MultiGeometryCollaboration,
            Problem,
        )
        problem = Problem(
            problem_id="rt",
            presenting_symptoms=[], suspected_couplings=[],
            bounds=("s", "t", "z"),
            regime_context={}, stakes=[],
        )
        collab = MultiGeometryCollaboration(problem=problem, frames=[])
        fr = trajectory_to_frame_reading(
            {"a": [0.0, 1.0, 2.0]},
            self.frames["thermodynamic_geometry"], "rt",
        )
        collab.add_reading(fr)
        # second reading from a different frame for invariants to compute
        fr2 = trajectory_to_frame_reading(
            {"a": [0.0, 0.5, 1.0]},
            self.frames["pattern_spatial"], "rt",
        )
        collab.add_reading(fr2)
        result = collab.synthesize()
        assert result["problem_id"] == "rt"


# ------------------------------------------------------------
# Typed coupling metadata
# ------------------------------------------------------------

class TestCouplingMetadata:
    def test_default_kind_is_unknown(self):
        from consortium.bridges import CouplingMetadata
        m = CouplingMetadata()
        assert m.kind == "unknown"
        assert m.strength == 1.0
        assert m.load_bearing is False

    def test_invalid_kind_rejected(self):
        from consortium.bridges import CouplingMetadata
        with pytest.raises(ValueError, match="coupling kind"):
            CouplingMetadata(kind="bogus")

    def test_strength_out_of_range_rejected(self):
        from consortium.bridges import CouplingMetadata
        with pytest.raises(ValueError, match="strength"):
            CouplingMetadata(strength=1.5)
        with pytest.raises(ValueError, match="strength"):
            CouplingMetadata(strength=-0.1)

    def test_all_documented_kinds_accepted(self):
        from consortium.bridges import CouplingMetadata, VALID_COUPLING_KINDS
        # every kind from CLAUDE_REQUIREMENTS.md §3 must be accepted
        required = {
            "causal_forward", "causal_reverse", "bidirectional",
            "constraint", "correlational", "decorative", "unknown",
        }
        assert required <= VALID_COUPLING_KINDS
        for k in required:
            CouplingMetadata(kind=k)


class TestTypedClaimGraph:
    def _build(self):
        from consortium.bridges import (
            CouplingMetadata,
            TypedClaimGraph,
            primitives_to_typed_claim_graph,
        )
        prims = [
            Primitive(
                concept_id="a", domain="d", form="f", role="r",
                couplings=["b"], bounds=("s", "t", "z"),
                epi="measured", epi_confidence=0.9,
            ),
            Primitive(
                concept_id="b", domain="d", form="f", role="r",
                couplings=["a"], bounds=("s", "t", "z"),
                epi="measured", epi_confidence=0.9,
            ),
        ]
        specs = {
            ("a", "b"): CouplingMetadata(
                kind="causal_forward",
                strength=0.8,
                load_bearing=True,
            ),
        }
        return primitives_to_typed_claim_graph(prims, coupling_specs=specs)

    def test_returns_typed_claim_graph(self):
        from consortium.bridges import TypedClaimGraph
        g = self._build()
        assert isinstance(g, TypedClaimGraph)

    def test_nodes_match_untyped_bridge(self):
        g = self._build()
        assert set(g.nodes.keys()) == {"a", "b"}

    def test_get_kind_returns_specified_for_known_edge(self):
        g = self._build()
        assert g.get_kind("a", "b") == "causal_forward"

    def test_get_kind_returns_unknown_for_unspecified_edge(self):
        # b → a is in the rel list but no spec was provided
        g = self._build()
        assert g.get_kind("b", "a") == "unknown"

    def test_is_load_bearing(self):
        g = self._build()
        assert g.is_load_bearing("a", "b") is True
        assert g.is_load_bearing("b", "a") is False

    def test_load_bearing_edges_lists_correct_pairs(self):
        g = self._build()
        edges = g.load_bearing_edges()
        assert ("a", "b") in edges
        assert ("b", "a") not in edges

    def test_no_specs_returns_empty_metadata(self):
        from consortium.bridges import primitives_to_typed_claim_graph
        prims = [Primitive(
            concept_id="x", domain="d", form="f", role="r",
            couplings=[], bounds=("s", "t", "z"),
            epi="measured", epi_confidence=0.9,
        )]
        g = primitives_to_typed_claim_graph(prims)
        assert g.coupling_metadata == {}

    def test_caller_supplied_specs_kept_even_for_absent_edges(self):
        # caller may supply forward-looking specs; bridge does not
        # silently drop them. This is the "preserves" half of the
        # BridgeReport contract.
        from consortium.bridges import (
            CouplingMetadata,
            primitives_to_typed_claim_graph,
        )
        prims = [Primitive(
            concept_id="x", domain="d", form="f", role="r",
            couplings=[], bounds=("s", "t", "z"),
            epi="measured", epi_confidence=0.9,
        )]
        specs = {
            ("x", "future_node"): CouplingMetadata(kind="causal_forward"),
        }
        g = primitives_to_typed_claim_graph(prims, coupling_specs=specs)
        assert ("x", "future_node") in g.coupling_metadata

    def test_rate_fns_passed_through(self):
        from consortium.bridges import primitives_to_typed_claim_graph
        prims = [Primitive(
            concept_id="x", domain="d", form="f", role="r",
            couplings=[], bounds=("s", "t", "z"),
            epi="measured", epi_confidence=0.9,
        )]
        custom = lambda s, rel, ctx: s + 1
        g = primitives_to_typed_claim_graph(
            prims, rate_fns={"x": custom},
        )
        assert g.nodes["x"].rate_fn(5.0, {}, {}) == 6.0


# ------------------------------------------------------------
# End-to-end: reading → primitives → claim_graph
# ------------------------------------------------------------

class TestEndToEnd:
    def test_reading_through_full_forward_pipeline(self):
        r = _reading(
            claim_refs=["mulch_h2o", "soil_thermal_mass"],
            confidence=0.92,
        )

        # reading → primitives
        prims = reading_to_primitives(r)
        assert len(prims) == 2
        concept_ids = {p.concept_id for p in prims}
        assert concept_ids == {"mulch_h2o", "soil_thermal_mass"}

        # primitives → claim graph
        g = primitives_to_claim_graph(prims)
        assert set(g.keys()) == {"mulch_h2o", "soil_thermal_mass"}

        # confidence has migrated through both layers
        assert all(p.epi_confidence == 0.92 for p in prims)

    def test_two_readings_dedupe_path(self):
        # human + instrument both report on mulch_h2o
        r_human = _reading(operator_type="human", epi="kinesthetic",
                           claim_refs=["mulch_h2o"], confidence=0.90)
        r_inst = _reading(operator_type="instrument", epi="instrumental",
                          claim_refs=["mulch_h2o"], confidence=0.96,
                          sensor_id="instrument:1")

        prims = (reading_to_primitives(r_human)
                 + reading_to_primitives(r_inst))
        assert len(prims) == 2  # not yet deduped

        # caller dedupes (documented as caller's responsibility)
        seen = {}
        for p in prims:
            if p.concept_id not in seen:
                seen[p.concept_id] = p
        deduped = list(seen.values())
        assert len(deduped) == 1
        # first-seen wins (human in this order)
        assert deduped[0].epi_confidence == 0.90
