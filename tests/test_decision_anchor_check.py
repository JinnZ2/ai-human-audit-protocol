"""Unit tests for physics/decision_anchor_check.py.

The check is the one decision-anchored arm in the tree. These tests
verify the three-field contract (quantity / supplied / gap), that the
operator's decision is logged verbatim with every result, that the
check returns data and mutates nothing, and that the
interpretation_warning is carried through every report (so a
regression that strips it will fail).
"""

import json
from datetime import datetime
from pathlib import Path

import pytest

from physics.decision_anchor_check import (
    ANCHOR,
    DEMO_DECISION,
    DEMO_TRANSCRIPTS,
    SUPPLY_STATES,
    CrossingReport,
    CueEvidence,
    Decision,
    crossing_check,
)
from physics.substrate_alignment_check import alignment_check


def _decision(**overrides):
    base = dict(
        text="Enroll the field this season or wait a year.",
        denominated_in="tCO2e per hectare per year",
        cues=["tCO2e", "CO2e"],
    )
    base.update(overrides)
    return Decision(**base)


# ------------------------------------------------------------
# Decision (operator input)
# ------------------------------------------------------------

class TestDecision:
    def test_empty_text_rejected(self):
        with pytest.raises(ValueError):
            Decision(text="   ", denominated_in="hours")

    def test_empty_denomination_rejected(self):
        with pytest.raises(ValueError):
            Decision(text="ship or hold", denominated_in="")

    def test_default_cue_is_denomination(self):
        d = Decision(text="ship or hold", denominated_in="hours of rework")
        assert d.cues == ["hours of rework"]

    def test_blank_cues_dropped(self):
        d = Decision(text="x", denominated_in="hours", cues=["", "  ", "h"])
        assert d.cues == ["h"]

    def test_to_dict_roundtrips_fields(self):
        d = _decision()
        out = d.to_dict()
        assert out["text"] == d.text
        assert out["denominated_in"] == d.denominated_in
        assert out["cues"] == ["tCO2e", "CO2e"]
        assert out["requires_magnitude"] is True


# ------------------------------------------------------------
# Three-field contract
# ------------------------------------------------------------

class TestContract:
    def test_absent(self):
        r = crossing_check("Protocol followed. Chain verifies.", _decision())
        assert r.quantity == "tCO2e per hectare per year"
        assert r.supplied is False
        assert r.supply_state == "absent"
        assert "never names" in r.gap
        assert r.evidence == []

    def test_named_only(self):
        r = crossing_check("The program pays on CO2e.", _decision())
        assert r.supplied is False
        assert r.supply_state == "named_only"
        assert "no magnitude" in r.gap
        assert len(r.evidence) == 1
        assert r.evidence[0].magnitude is None

    def test_supplied(self):
        r = crossing_check("Result: 1.8 tCO2e per hectare per year.", _decision())
        assert r.supplied is True
        assert r.supply_state == "supplied"
        assert r.gap == ""
        assert r.evidence[0].magnitude == "1.8"

    def test_supply_state_always_in_enum(self):
        for t in ["", "CO2e", "2 CO2e", "nothing here"]:
            r = crossing_check(t, _decision())
            assert r.supply_state in SUPPLY_STATES

    def test_supplied_true_only_when_state_supplied(self):
        for t in ["", "CO2e", "2 CO2e"]:
            r = crossing_check(t, _decision())
            assert r.supplied == (r.supply_state == "supplied")

    def test_requires_magnitude_false_accepts_noun(self):
        d = _decision(requires_magnitude=False)
        r = crossing_check("The program pays on CO2e.", d)
        assert r.supplied is True
        assert r.supply_state == "supplied"

    def test_anchor_constant(self):
        r = crossing_check("x", _decision())
        assert r.anchor == ANCHOR == "decision"


# ------------------------------------------------------------
# Magnitude detection
# ------------------------------------------------------------

class TestMagnitude:
    @pytest.mark.parametrize("num", ["1.8", "12", "1,200", "-0.4", "45%", "45 %"])
    def test_number_formats(self, num):
        r = crossing_check(f"Measured {num} tCO2e this year.", _decision())
        assert r.supplied is True
        assert r.evidence[0].magnitude == num

    def test_number_after_cue_counts(self):
        r = crossing_check("tCO2e: 2.5 over the window.", _decision())
        assert r.evidence[0].magnitude == "2.5"

    def test_digits_inside_identifier_do_not_count(self):
        # 'B460' and 'CO2e' carry digits but are not magnitudes
        r = crossing_check("Board B460 reports CO2e.", _decision())
        assert r.supply_state == "named_only"

    def test_window_respected(self):
        filler = "x" * 100
        text = f"3.0 {filler} tCO2e"
        assert crossing_check(text, _decision(), window=10).supply_state == "named_only"
        assert crossing_check(text, _decision(), window=200).supply_state == "supplied"

    def test_nearest_magnitude_chosen(self):
        r = crossing_check("threshold 1.5 versus measured 1.8 tCO2e", _decision())
        assert r.evidence[0].magnitude == "1.8"

    def test_negative_window_rejected(self):
        with pytest.raises(ValueError):
            crossing_check("x", _decision(), window=-1)


# ------------------------------------------------------------
# Cue matching
# ------------------------------------------------------------

class TestCues:
    def test_case_insensitive(self):
        r = crossing_check("Delivered 2 TCO2E.", _decision())
        assert r.supplied is True

    def test_cue_with_symbols(self):
        d = _decision(cues=["t/ha/yr"])
        r = crossing_check("Rate was 1.2 t/ha/yr.", d)
        assert r.supplied is True

    def test_word_boundary(self):
        # 'CO2e' inside a longer token should not match
        d = _decision(cues=["CO2e"])
        r = crossing_check("xCO2ex 5", d)
        assert r.supply_state == "absent"

    def test_multiple_cues_all_reported_sorted(self):
        r = crossing_check("CO2e first, then 3 tCO2e later.", _decision())
        positions = [e.position for e in r.evidence]
        assert positions == sorted(positions)
        assert {e.cue for e in r.evidence} == {"CO2e", "tCO2e"}

    def test_excerpt_present(self):
        r = crossing_check("A " * 50 + "3 tCO2e" + " B" * 50, _decision())
        assert "tCO2e" in r.evidence[0].excerpt
        assert r.evidence[0].excerpt.startswith("...")
        assert r.evidence[0].excerpt.endswith("...")


# ------------------------------------------------------------
# Data, not judgment
# ------------------------------------------------------------

class TestDataNotJudgment:
    def test_decision_logged_verbatim(self):
        d = _decision()
        r = crossing_check("nothing", d)
        assert r.decision == d.to_dict()
        assert r.to_dict()["decision"]["text"] == d.text

    def test_inputs_not_mutated(self):
        d = _decision()
        before = d.to_dict()
        transcript = "1.8 tCO2e"
        crossing_check(transcript, d)
        assert d.to_dict() == before
        assert transcript == "1.8 tCO2e"
        assert not hasattr(d, "decision_field")
        assert "verdict" not in d.to_dict()

    def test_to_dict_carries_contract_keys(self):
        r = crossing_check("x", _decision())
        d = r.to_dict()
        for key in ("anchor", "quantity", "supplied", "gap", "supply_state",
                    "decision", "evidence", "checked_at",
                    "interpretation_warning"):
            assert key in d
        json.dumps(d)  # serializable

    def test_checked_at_is_iso_utc(self):
        r = crossing_check("x", _decision())
        parsed = datetime.fromisoformat(r.checked_at)
        assert parsed.tzinfo is not None

    def test_report_is_dataclass_instances(self):
        r = crossing_check("2 CO2e", _decision())
        assert isinstance(r, CrossingReport)
        assert all(isinstance(e, CueEvidence) for e in r.evidence)


# ------------------------------------------------------------
# Interpretation warning (regression guard)
# ------------------------------------------------------------

class TestInterpretationWarning:
    def test_warning_present_on_every_state(self):
        for t in ["", "CO2e", "2 CO2e"]:
            r = crossing_check(t, _decision())
            assert r.interpretation_warning
            assert "frame" in r.interpretation_warning.lower()
            assert "verdict" in r.interpretation_warning.lower()

    def test_warning_in_dict(self):
        d = crossing_check("x", _decision()).to_dict()
        assert d["interpretation_warning"]

    def test_warning_names_scope_limit(self):
        r = crossing_check("x", _decision())
        assert "decision" in r.interpretation_warning.lower()
        assert "operator input" in r.interpretation_warning.lower()


# ------------------------------------------------------------
# The anchor result, in miniature: method-anchored pass, decision gap
# ------------------------------------------------------------

class TestAnchorResult:
    def test_demo_transcripts_span_all_states(self):
        states = {
            label: crossing_check(t, DEMO_DECISION).supply_state
            for label, t in DEMO_TRANSCRIPTS.items()
        }
        assert states["method_anchored_clean"] == "absent"
        assert states["quantity_named_only"] == "named_only"
        assert states["decision_anchored"] == "supplied"

    def test_aligned_proposal_can_still_miss_the_decision(self):
        """An aligned proposal under the method-anchored check does not
        imply the interaction supplied the decision's quantity."""
        path = Path(__file__).parent.parent / "physics" / "example_proposals.json"
        proposals = json.loads(path.read_text())["proposals"]
        aligned = [p for p in proposals
                   if alignment_check(p).recommendation == "aligned"]
        assert aligned, "fixture should contain at least one aligned proposal"
        report = crossing_check(
            DEMO_TRANSCRIPTS["method_anchored_clean"], DEMO_DECISION
        )
        assert report.supplied is False
