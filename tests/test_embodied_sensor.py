"""Unit tests for consortium/embodied_sensor.py.

Audit symmetry stance: every operator type — human, animal, plant, AI,
instrument, ecosystem — passes through the same validation, the same
confidence ceilings, the same coating-probe shape. These tests enforce
that.
"""

from datetime import datetime, timezone

import pytest

from consortium.embodied_sensor import (
    OPERATOR_TYPES,
    EPI_SUBTAGS,
    EPI_CONFIDENCE_CEILING,
    COATING_PROBE_RESULTS,
    CoatingProbeResult,
    EmbodiedReading,
    OperatorBudget,
    reading_to_frame_reading,
    example_readings,
    example_budgets,
)
from consortium.collaboration_protocol import (
    GeometricFrame,
    FrameReading,
    build_consortium_frames,
)


NOW = datetime(2026, 4, 27, 14, 0, tzinfo=timezone.utc)


def _valid_probe():
    return CoatingProbeResult(probe_name="not_run", result="not_run")


def _valid_reading(**overrides):
    base = dict(
        sensor_id="test:sensor:1",
        operator_type="human",
        location="test_loc",
        timestamp=NOW,
        observation="test observation",
        claim_refs=["test_claim"],
        epi="kinesthetic",
        confidence=0.9,
        conditions={},
        coating_probe=_valid_probe(),
    )
    base.update(overrides)
    return EmbodiedReading(**base)


# ------------------------------------------------------------
# Vocabularies
# ------------------------------------------------------------

class TestVocabularies:
    def test_operator_types_includes_all_six(self):
        assert OPERATOR_TYPES >= {
            "human", "animal", "plant", "ai", "instrument", "ecosystem"
        }

    def test_epi_subtags_cover_each_operator_kind(self):
        # at minimum: every operator type has at least one matching epi
        assert "kinesthetic" in EPI_SUBTAGS         # human
        assert "behavioral" in EPI_SUBTAGS          # animal
        assert "phenological" in EPI_SUBTAGS        # plant
        assert "visual" in EPI_SUBTAGS              # ai (vision)
        assert "instrumental" in EPI_SUBTAGS        # instrument
        assert "compound" in EPI_SUBTAGS            # ecosystem

    def test_confidence_ceilings_present_for_all_epi(self):
        # every epi sub-tag has a ceiling defined
        assert set(EPI_CONFIDENCE_CEILING.keys()) == EPI_SUBTAGS

    def test_asserted_has_lowest_ceiling(self):
        # un-grounded claims cannot honestly claim high confidence
        assert EPI_CONFIDENCE_CEILING["asserted"] <= 0.6
        # direct-sensing modes all have higher ceiling than asserted
        for tag in ("kinesthetic", "phenological", "behavioral",
                    "instrumental", "visual"):
            assert EPI_CONFIDENCE_CEILING[tag] > EPI_CONFIDENCE_CEILING["asserted"]


# ------------------------------------------------------------
# Coating probe result
# ------------------------------------------------------------

class TestCoatingProbeResult:
    @pytest.mark.parametrize("result", sorted(COATING_PROBE_RESULTS))
    def test_valid_result_accepted(self, result):
        CoatingProbeResult(probe_name="x", result=result)

    def test_invalid_result_rejected(self):
        with pytest.raises(ValueError):
            CoatingProbeResult(probe_name="x", result="bogus")


# ------------------------------------------------------------
# EmbodiedReading validation
# ------------------------------------------------------------

class TestEmbodiedReadingValidation:
    def test_valid_reading_accepted(self):
        r = _valid_reading()
        assert r.operator_type == "human"
        assert r.epi == "kinesthetic"

    def test_invalid_operator_type_rejected(self):
        with pytest.raises(ValueError, match="operator_type"):
            _valid_reading(operator_type="alien")

    def test_invalid_epi_rejected(self):
        with pytest.raises(ValueError, match="epi"):
            _valid_reading(epi="vibes")

    def test_confidence_below_zero_rejected(self):
        with pytest.raises(ValueError, match="confidence"):
            _valid_reading(confidence=-0.1)

    def test_confidence_above_one_rejected(self):
        with pytest.raises(ValueError, match="confidence"):
            _valid_reading(confidence=1.1)

    def test_confidence_at_ceiling_accepted(self):
        ceiling = EPI_CONFIDENCE_CEILING["kinesthetic"]
        r = _valid_reading(confidence=ceiling)
        assert r.confidence == ceiling

    def test_confidence_above_ceiling_rejected(self):
        ceiling = EPI_CONFIDENCE_CEILING["asserted"]
        with pytest.raises(ValueError, match="ceiling"):
            _valid_reading(epi="asserted", confidence=ceiling + 0.01)

    def test_each_operator_type_can_construct(self):
        # operator-agnostic claim: every operator type produces a
        # valid reading through the same primitive
        cases = {
            "human":      ("kinesthetic",     0.9),
            "animal":     ("behavioral",      0.85),
            "plant":      ("phenological",    0.9),
            "ai":         ("visual",          0.85),
            "instrument": ("instrumental",    0.95),
            "ecosystem":  ("compound",        0.9),
        }
        for op, (epi, conf) in cases.items():
            r = _valid_reading(operator_type=op, epi=epi, confidence=conf)
            assert r.operator_type == op
            assert r.epi == epi


# ------------------------------------------------------------
# Operator budget
# ------------------------------------------------------------

class TestOperatorBudget:
    def test_remaining_starts_full(self):
        b = OperatorBudget(
            operator_id="x", operator_type="human",
            capacity_unit="m", capacity_total=10.0,
        )
        assert b.remaining() == 10.0

    def test_can_query_when_remaining(self):
        b = OperatorBudget(
            operator_id="x", operator_type="human",
            capacity_unit="m", capacity_total=10.0,
        )
        assert b.can_query(cost=5.0)

    def test_cannot_query_when_exhausted(self):
        b = OperatorBudget(
            operator_id="x", operator_type="human",
            capacity_unit="m", capacity_total=10.0,
            capacity_used=10.0,
        )
        assert not b.can_query(cost=1.0)

    def test_record_query_decrements(self):
        b = OperatorBudget(
            operator_id="x", operator_type="human",
            capacity_unit="m", capacity_total=10.0,
        )
        b.record_query(cost=3.0)
        assert b.remaining() == 7.0

    def test_record_query_raises_when_exhausted(self):
        b = OperatorBudget(
            operator_id="x", operator_type="human",
            capacity_unit="m", capacity_total=1.0,
        )
        with pytest.raises(RuntimeError, match="exhausted"):
            b.record_query(cost=2.0)


# ------------------------------------------------------------
# Lift to FrameReading
# ------------------------------------------------------------

class TestReadingToFrameReading:
    def test_lift_produces_frame_reading(self):
        frames = {f.frame_id: f for f in build_consortium_frames()}
        r = _valid_reading()
        fr = reading_to_frame_reading(
            reading=r,
            frame=frames["embodied_sensor"],
            problem_id="prob_42",
        )
        assert isinstance(fr, FrameReading)
        assert fr.problem_id == "prob_42"
        assert fr.confidence == r.confidence

    def test_lift_preserves_claim_refs_as_visible_couplings(self):
        frames = {f.frame_id: f for f in build_consortium_frames()}
        r = _valid_reading(claim_refs=["a", "b", "c"])
        fr = reading_to_frame_reading(
            reading=r,
            frame=frames["embodied_sensor"],
            problem_id="prob_x",
        )
        assert fr.visible_couplings == ["a", "b", "c"]

    def test_lift_includes_audit_metadata_in_assumptions(self):
        frames = {f.frame_id: f for f in build_consortium_frames()}
        r = _valid_reading()
        fr = reading_to_frame_reading(
            reading=r,
            frame=frames["embodied_sensor"],
            problem_id="prob_x",
        )
        joined = " ".join(fr.assumptions_required)
        assert "operator_type=human" in joined
        assert "epi=kinesthetic" in joined
        assert "coating_probe=" in joined

    def test_lift_default_proposed_actions_empty(self):
        # readings observe; collaboration synthesizes actions
        frames = {f.frame_id: f for f in build_consortium_frames()}
        r = _valid_reading()
        fr = reading_to_frame_reading(
            reading=r,
            frame=frames["embodied_sensor"],
            problem_id="prob_x",
        )
        assert fr.proposed_actions == []

    def test_lift_accepts_explicit_proposed_actions(self):
        # tradition holders may include prescriptive structure
        frames = {f.frame_id: f for f in build_consortium_frames()}
        r = _valid_reading()
        fr = reading_to_frame_reading(
            reading=r,
            frame=frames["embodied_sensor"],
            problem_id="prob_x",
            proposed_actions=[("act_now", "irreversible_if_delayed")],
        )
        assert fr.proposed_actions == [("act_now", "irreversible_if_delayed")]

    def test_lift_carries_frame_blind_spots(self):
        frames = {f.frame_id: f for f in build_consortium_frames()}
        embodied = frames["embodied_sensor"]
        r = _valid_reading()
        fr = reading_to_frame_reading(
            reading=r,
            frame=embodied,
            problem_id="prob_x",
        )
        assert fr.where_this_frame_breaks == list(embodied.couplings_invisible)


# ------------------------------------------------------------
# Examples are valid + diverse
# ------------------------------------------------------------

class TestExamples:
    def test_example_readings_construct(self):
        readings = example_readings()
        assert len(readings) >= 6

    def test_example_readings_cover_all_operator_types(self):
        readings = example_readings()
        present = {r.operator_type for r in readings}
        assert present == OPERATOR_TYPES

    def test_example_readings_all_within_ceilings(self):
        # validation in __post_init__ already enforces this; this test
        # makes the contract explicit and catches future drift
        for r in example_readings():
            ceiling = EPI_CONFIDENCE_CEILING[r.epi]
            assert r.confidence <= ceiling, (
                f"{r.sensor_id} confidence {r.confidence} exceeds "
                f"ceiling {ceiling} for epi={r.epi}"
            )

    def test_example_budgets_construct(self):
        budgets = example_budgets()
        assert len(budgets) >= 4
        for b in budgets:
            assert b.operator_type in OPERATOR_TYPES
            assert b.capacity_total > 0
