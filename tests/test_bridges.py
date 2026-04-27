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
    BridgeReport,
    select_frame,
    select_frame_for_reading,
    reading_to_primitives,
    frame_reading_to_primitives,
    primitives_to_claim_graph,
    trajectory_summary,
    all_bridge_reports,
    _zero_rate,
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
        assert "_warning" in s

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

    def test_warning_is_present(self):
        # the v1 stub MUST carry a warning so callers don't mistake
        # its output for a real FrameReading lift
        s = trajectory_summary({"a": [1.0]})
        assert "stub" in s["_warning"].lower()


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
            "trajectory_summary",
        }

    def test_every_report_declares_preserves_and_lossy(self):
        for r in all_bridge_reports():
            assert isinstance(r, BridgeReport)
            assert r.preserves, f"{r.bridge_name} declares no preserves"
            assert r.lossy_on, f"{r.bridge_name} declares no lossy_on"

    def test_trajectory_summary_report_flags_v1_stub(self):
        from consortium.bridges import trajectory_summary_report
        r = trajectory_summary_report()
        assert "stub" in r.notes.lower() or "stub" in (r.notes or "").lower()


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
