"""Unit tests for consortium/router/ — the v1-offline router.

Covers BaseModelAdapter contract, MockAdapter, ConsentGate (fail-closed),
QueryDispatcher (fan-out, failure modes, refusal modes), CoherenceAggregator
(synthesis + cross-adapter metadata), and the API stubs.
"""

from datetime import datetime, timezone

import pytest

from consortium.collaboration_protocol import (
    FrameReading,
    Problem,
    build_consortium_frames,
)
from consortium.router.base import BaseModelAdapter, CostEstimate
from consortium.router.mock_adapter import MockAdapter
from consortium.router.consent import (
    ConsentGate,
    ConsentRecord,
    ConsentDenied,
)
from consortium.router.query_dispatcher import (
    QueryDispatcher,
    DispatchResult,
)
from consortium.router.coherence_aggregator import aggregate
from consortium.router.model_adapters.claude_adapter import ClaudeAdapter
from consortium.router.model_adapters.gemini_adapter import GeminiAdapter
from consortium.router.model_adapters.deepseek_adapter import DeepSeekAdapter


def _problem(problem_id="prob_test"):
    return Problem(
        problem_id=problem_id,
        presenting_symptoms=["s1", "s2"],
        suspected_couplings=["c1", "c2", "c3", "c4"],
        bounds=("space", "time", "scale"),
        regime_context={"climate": "current"},
        stakes=["s"],
    )


def _frames():
    return {f.frame_id: f for f in build_consortium_frames()}


# ============================================================
# BaseModelAdapter contract
# ============================================================

class TestBaseModelAdapter:
    def test_subclass_without_frame_id_rejected(self):
        with pytest.raises(TypeError, match="frame_id"):
            class Bad(BaseModelAdapter):
                operator_type = "ai"

                def query(self, problem, **opts):
                    pass

                def available(self):
                    return (True, "")

    def test_subclass_without_operator_type_rejected(self):
        with pytest.raises(TypeError, match="operator_type"):
            class Bad(BaseModelAdapter):
                frame_id = "x"

                def query(self, problem, **opts):
                    pass

                def available(self):
                    return (True, "")

    def test_subclass_with_both_attrs_accepted(self):
        # this must not raise
        class Good(BaseModelAdapter):
            frame_id = "x"
            operator_type = "ai"

            def query(self, problem, **opts):
                pass

            def available(self):
                return (True, "")

        # we just want the class definition to succeed
        assert Good.frame_id == "x"

    def test_default_cost_estimate(self):
        class A(BaseModelAdapter):
            frame_id = "x"
            operator_type = "ai"

            def query(self, problem, **opts):
                return None

            def available(self):
                return (True, "")

        est = A().cost_estimate(_problem())
        assert isinstance(est, CostEstimate)
        assert est.amount == 0.0


# ============================================================
# MockAdapter
# ============================================================

class TestMockAdapter:
    def test_construction_inherits_frame_attrs(self):
        f = _frames()["thermodynamic_geometry"]
        a = MockAdapter(frame=f)
        assert a.frame_id == "thermodynamic_geometry"
        assert a.operator_type == "AI_model"  # frame's operator_type

    def test_explicit_operator_type_override(self):
        f = _frames()["embodied_sensor"]
        a = MockAdapter(frame=f, operator_type="instrument")
        assert a.operator_type == "instrument"

    def test_available_always_true(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        ok, reason = a.available()
        assert ok is True
        assert reason == ""

    def test_zero_cost(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        est = a.cost_estimate(_problem())
        assert est.amount == 0.0
        assert est.unit == "no_op"

    def test_query_returns_frame_reading(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        fr = a.query(_problem())
        assert isinstance(fr, FrameReading)
        assert fr.problem_id == "prob_test"

    def test_query_uses_problem_couplings(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        p = _problem()
        fr = a.query(p)
        assert set(fr.visible_couplings) == set(p.suspected_couplings)

    def test_load_bearing_first_three(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        fr = a.query(_problem())
        assert len(fr.load_bearing_elements) == 3

    def test_response_factory_override(self):
        f = _frames()["thermodynamic_geometry"]
        a = MockAdapter(
            frame=f,
            response_factory=lambda p: {
                "proposed_diagnosis": "custom override",
                "confidence": 0.42,
            },
        )
        fr = a.query(_problem())
        assert fr.proposed_diagnosis == "custom override"
        assert fr.confidence == 0.42

    def test_assumptions_record_adapter_metadata(self):
        a = MockAdapter(frame=_frames()["narrative_structured"])
        fr = a.query(_problem())
        joined = " ".join(fr.assumptions_required)
        assert "MockAdapter" in joined
        assert "deterministic_no_external_call" in joined


# ============================================================
# ConsentGate
# ============================================================

class TestConsentGate:
    def test_fail_closed_default(self):
        gate = ConsentGate()
        ok, reason = gate.is_authorized("p1", "adapter_x")
        assert ok is False
        assert "no consent" in reason

    def test_grant_authorizes(self):
        gate = ConsentGate()
        gate.grant("p1", ["adapter_x"], {"USD_estimate": 0.10}, "user")
        ok, _ = gate.is_authorized("p1", "adapter_x")
        assert ok is True

    def test_grant_does_not_authorize_other_problem(self):
        gate = ConsentGate()
        gate.grant("p1", ["adapter_x"], {}, "user")
        ok, _ = gate.is_authorized("p2", "adapter_x")
        assert ok is False

    def test_grant_does_not_authorize_other_adapter(self):
        gate = ConsentGate()
        gate.grant("p1", ["adapter_x"], {}, "user")
        ok, _ = gate.is_authorized("p1", "adapter_y")
        assert ok is False

    def test_revoke_blocks(self):
        gate = ConsentGate()
        gate.grant("p1", ["x"], {}, "user")
        assert gate.is_authorized("p1", "x")[0] is True
        gate.revoke("p1", ["x"], "user", notes="test_revoke")
        ok, reason = gate.is_authorized("p1", "x")
        assert ok is False
        assert "revoked" in reason.lower()

    def test_grant_after_revoke_re_authorizes(self):
        gate = ConsentGate()
        gate.grant("p1", ["x"], {}, "user")
        gate.revoke("p1", ["x"], "user")
        gate.grant("p1", ["x"], {}, "user", notes="re-grant")
        ok, _ = gate.is_authorized("p1", "x")
        assert ok is True

    def test_assert_authorized_raises(self):
        gate = ConsentGate()
        with pytest.raises(ConsentDenied):
            gate.assert_authorized("p1", "x")

    def test_assert_authorized_passes_when_granted(self):
        gate = ConsentGate()
        gate.grant("p1", ["x"], {}, "user")
        # must not raise
        gate.assert_authorized("p1", "x")

    def test_records_immutable_history(self):
        gate = ConsentGate()
        gate.grant("p1", ["x"], {}, "user1", notes="grant_1")
        gate.revoke("p1", ["x"], "user2", notes="revoke_1")
        gate.grant("p1", ["x"], {}, "user3", notes="grant_2")
        records = gate.records("p1")
        # all three preserved in order
        assert len(records) == 3
        assert records[0].notes == "grant_1"
        assert records[1].notes == "revoke_1"
        assert records[2].notes == "grant_2"

    def test_records_filtered_by_problem(self):
        gate = ConsentGate()
        gate.grant("p1", ["x"], {}, "u")
        gate.grant("p2", ["x"], {}, "u")
        assert len(gate.records("p1")) == 1
        assert len(gate.records()) == 2


# ============================================================
# QueryDispatcher
# ============================================================

class TestQueryDispatcher:
    def setup_method(self):
        self.frames = _frames()

    def _adapters(self, frame_ids):
        return [MockAdapter(frame=self.frames[fid]) for fid in frame_ids]

    def test_no_consent_means_all_refused(self):
        adapters = self._adapters(["thermodynamic_geometry",
                                    "narrative_structured"])
        d = QueryDispatcher(adapters=adapters)
        result = d.fan_out(_problem())
        assert result.readings == []
        assert len(result.refused) == 2

    def test_consented_adapters_produce_readings(self):
        adapters = self._adapters(["thermodynamic_geometry",
                                    "narrative_structured"])
        gate = ConsentGate()
        gate.grant("prob_test",
                   ["thermodynamic_geometry", "narrative_structured"],
                   {}, "user")
        d = QueryDispatcher(adapters=adapters, consent_gate=gate)
        result = d.fan_out(_problem())
        assert len(result.readings) == 2
        assert result.refused == []

    def test_partial_consent_partial_run(self):
        adapters = self._adapters(["thermodynamic_geometry",
                                    "narrative_structured"])
        gate = ConsentGate()
        gate.grant("prob_test", ["thermodynamic_geometry"], {}, "user")
        d = QueryDispatcher(adapters=adapters, consent_gate=gate)
        result = d.fan_out(_problem())
        assert len(result.readings) == 1
        assert result.readings[0].frame.frame_id == "thermodynamic_geometry"
        assert len(result.refused) == 1
        assert result.refused[0]["adapter_id"] == "narrative_structured"

    def test_unavailable_adapter_recorded(self):
        f = self.frames["thermodynamic_geometry"]

        class UnavailableMock(MockAdapter):
            def available(self):
                return (False, "credential missing")

        gate = ConsentGate()
        gate.grant("prob_test", ["thermodynamic_geometry"], {}, "user")
        d = QueryDispatcher(
            adapters=[UnavailableMock(frame=f)],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        assert result.readings == []
        assert len(result.unavailable) == 1
        assert result.unavailable[0]["reason"] == "credential missing"

    def test_failure_recorded_when_query_raises(self):
        f = self.frames["thermodynamic_geometry"]

        class FailingMock(MockAdapter):
            def query(self, problem, **opts):
                raise RuntimeError("boom")

        gate = ConsentGate()
        gate.grant("prob_test", ["thermodynamic_geometry"], {}, "user")
        d = QueryDispatcher(
            adapters=[FailingMock(frame=f)],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        assert result.readings == []
        assert len(result.failures) == 1
        assert result.failures[0]["exception_type"] == "RuntimeError"

    def test_consent_denied_in_query_recorded_as_refused(self):
        f = self.frames["thermodynamic_geometry"]

        class StrictMock(MockAdapter):
            def query(self, problem, **opts):
                raise ConsentDenied("stricter check failed")

        gate = ConsentGate()
        gate.grant("prob_test", ["thermodynamic_geometry"], {}, "user")
        d = QueryDispatcher(
            adapters=[StrictMock(frame=f)],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        assert len(result.refused) == 1

    def test_cost_estimates_collected(self):
        adapters = self._adapters(["thermodynamic_geometry"])
        d = QueryDispatcher(adapters=adapters)
        ests = d.cost_estimates(_problem())
        assert "thermodynamic_geometry" in ests

    def test_adapters_attempted_includes_all_outcomes(self):
        f1 = self.frames["thermodynamic_geometry"]
        f2 = self.frames["narrative_structured"]
        f3 = self.frames["pattern_spatial"]

        class OK(MockAdapter):
            pass

        class Unavail(MockAdapter):
            def available(self):
                return (False, "down")

        class Fail(MockAdapter):
            def query(self, problem, **opts):
                raise ValueError("v")

        gate = ConsentGate()
        gate.grant("prob_test",
                   ["thermodynamic_geometry", "pattern_spatial"], {}, "u")
        d = QueryDispatcher(
            adapters=[OK(frame=f1), Unavail(frame=f2), Fail(frame=f3)],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        attempted = result.adapters_attempted()
        assert set(attempted) == {
            "thermodynamic_geometry",
            "narrative_structured",
            "pattern_spatial",
        }


# ============================================================
# CoherenceAggregator
# ============================================================

class TestCoherenceAggregator:
    def setup_method(self):
        self.frames = _frames()

    def test_aggregates_with_readings(self):
        adapters = [
            MockAdapter(frame=self.frames["thermodynamic_geometry"]),
            MockAdapter(frame=self.frames["narrative_structured"]),
        ]
        gate = ConsentGate()
        gate.grant("prob_test",
                   ["thermodynamic_geometry", "narrative_structured"],
                   {}, "u")
        d = QueryDispatcher(adapters=adapters, consent_gate=gate)
        result = d.fan_out(_problem())

        synth = aggregate(result, _problem(),
                          frames=list(self.frames.values()))
        assert "invariant_geometry" in synth
        assert "adapters_fired" in synth
        assert set(synth["adapters_fired"]) == {
            "thermodynamic_geometry", "narrative_structured",
        }
        assert synth["no_readings_returned"] is False

    def test_aggregates_with_zero_readings(self):
        # all refused → no readings, but the aggregation must still
        # surface the geometry of absence rather than crash
        adapters = [MockAdapter(frame=self.frames["thermodynamic_geometry"])]
        d = QueryDispatcher(adapters=adapters)  # no consent
        result = d.fan_out(_problem())

        synth = aggregate(result, _problem(),
                          frames=list(self.frames.values()))
        assert synth["no_readings_returned"] is True
        assert synth["adapters_fired"] == []
        assert len(synth["consent_refusals"]) == 1
        assert "absence" in synth["epistemic_warning"].lower()

    def test_failures_and_refusals_carried_through(self):
        f1 = self.frames["thermodynamic_geometry"]
        f2 = self.frames["narrative_structured"]

        class Fail(MockAdapter):
            def query(self, problem, **opts):
                raise RuntimeError("boom")

        gate = ConsentGate()
        gate.grant("prob_test", ["thermodynamic_geometry"], {}, "u")
        # only f1 consented, f2 refused
        d = QueryDispatcher(
            adapters=[Fail(frame=f1), MockAdapter(frame=f2)],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        synth = aggregate(result, _problem(),
                          frames=list(self.frames.values()))
        assert len(synth["adapter_failures"]) == 1
        assert len(synth["consent_refusals"]) == 1


# ============================================================
# API stubs
# ============================================================

class TestApiStubs:
    @pytest.mark.parametrize("cls,expected_frame_id", [
        (ClaudeAdapter, "narrative_structured"),
        (GeminiAdapter, "pattern_spatial"),
        (DeepSeekAdapter, "statistical_relational"),
    ])
    def test_stub_declares_frame_id(self, cls, expected_frame_id):
        assert cls.frame_id == expected_frame_id
        assert cls.operator_type == "ai"

    @pytest.mark.parametrize("cls", [ClaudeAdapter, GeminiAdapter, DeepSeekAdapter])
    def test_stub_unavailable_with_helpful_reason(self, cls):
        a = cls()
        ok, reason = a.available()
        assert ok is False
        assert "stub" in reason.lower() or "credentials" in reason.lower()

    @pytest.mark.parametrize("cls", [ClaudeAdapter, GeminiAdapter, DeepSeekAdapter])
    def test_stub_query_raises_not_implemented(self, cls):
        a = cls()
        with pytest.raises(NotImplementedError):
            a.query(_problem())

    def test_stubs_dispatched_appear_as_unavailable(self):
        # the dispatcher should record stubs as unavailable, not fail
        gate = ConsentGate()
        gate.grant("prob_test",
                   ["narrative_structured", "pattern_spatial",
                    "statistical_relational"], {}, "u")
        d = QueryDispatcher(
            adapters=[ClaudeAdapter(), GeminiAdapter(), DeepSeekAdapter()],
            consent_gate=gate,
        )
        result = d.fan_out(_problem())
        assert result.readings == []
        # all three should land in unavailable, not failure
        assert len(result.unavailable) == 3
        assert result.failures == []


# ============================================================
# Full-stack smoke test: dispatch → aggregate
# ============================================================

class TestFullStackSmoke:
    def test_three_mock_adapters_full_synthesis(self):
        frames = _frames()
        adapters = [
            MockAdapter(frame=frames["thermodynamic_geometry"]),
            MockAdapter(frame=frames["narrative_structured"]),
            MockAdapter(frame=frames["pattern_spatial"]),
        ]
        # disclose costs to consenter
        d = QueryDispatcher(adapters=adapters)
        costs = d.cost_estimates(_problem())
        assert len(costs) == 3

        # consenter authorizes after seeing costs
        gate = ConsentGate()
        gate.grant(
            problem_id="prob_test",
            adapters_authorized=list(costs.keys()),
            cost_disclosed=costs,
            consenter="test_user",
            notes="full-stack smoke test",
        )
        d = QueryDispatcher(adapters=adapters, consent_gate=gate)
        result = d.fan_out(_problem())
        assert len(result.readings) == 3
        assert result.refused == []
        assert result.failures == []

        # synthesize across all three
        synth = aggregate(result, _problem(),
                          frames=list(frames.values()))
        assert synth["no_readings_returned"] is False
        assert len(synth["adapters_fired"]) == 3
        # all three mock adapters propose the same couplings, so
        # convergence should be "converged"
        assert synth["invariant_geometry"]["convergence"] == "converged"
