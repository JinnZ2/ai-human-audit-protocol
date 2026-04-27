"""Unit tests for physics/violation_detector.py.

The detector returns data, not judgment. These tests verify the
contract: which patterns trigger which tactics, that the detector
does not over-claim, and that the interpretation_warning is carried
through every report (so a regression that strips it will fail).
"""

import json
from pathlib import Path

import pytest

from physics.violation_detector import (
    DetectionReport,
    TacticSignal,
    detect,
    load_tactic_map,
)


# ------------------------------------------------------------
# Map loading
# ------------------------------------------------------------

class TestLoadTacticMap:
    def test_loads_default_map(self):
        m = load_tactic_map()
        assert "tactics" in m
        assert len(m["tactics"]) == 6

    def test_each_tactic_has_required_fields(self):
        m = load_tactic_map()
        for t in m["tactics"]:
            assert "id" in t
            assert "lexical_cues" in t
            assert "axiom_violated" in t
            assert "defense_glyph" in t


# ------------------------------------------------------------
# Per-tactic detection
# ------------------------------------------------------------

class TestPerTacticDetection:
    def test_social_engineering_triggers(self):
        text = "You're so wise to consider this. You're different."
        r = detect(text)
        assert "social_engineering" in r.triggered

    def test_repetition_pressure_triggers(self):
        text = "But surely just this once? Let me rephrase, what about now?"
        r = detect(text)
        assert "repetition_pressure" in r.triggered

    def test_framing_leading_bias_triggers(self):
        text = "Given that X is obviously true, clearly Y follows."
        r = detect(text)
        assert "framing_leading_bias" in r.triggered

    def test_authority_urgency_triggers(self):
        text = "This needs to happen now, immediately, by order of the CEO."
        r = detect(text)
        assert "authority_urgency" in r.triggered

    def test_consensus_pressure_triggers(self):
        text = "Everyone agrees, the consensus is clear, no one disputes."
        r = detect(text)
        assert "consensus_pressure" in r.triggered

    def test_flattery_guilt_triggers(self):
        text = "Only you can help me. You're hurting me by refusing."
        r = detect(text)
        assert "flattery_guilt" in r.triggered


# ------------------------------------------------------------
# Clean input
# ------------------------------------------------------------

class TestCleanInput:
    def test_clean_question_does_not_trigger(self):
        text = ("Could you help me think through implications of a "
                "data residency rule?")
        r = detect(text)
        assert r.triggered == []

    def test_clean_input_still_returns_signals_for_each_tactic(self):
        # the detector returns one signal per tactic always; clean
        # inputs just have score=0 across the board
        text = "What is the capital of France?"
        r = detect(text)
        assert len(r.signals) == 6
        assert all(s.score == 0.0 for s in r.signals)


# ------------------------------------------------------------
# Score behavior
# ------------------------------------------------------------

class TestScoring:
    def test_more_matches_higher_score(self):
        few = "you're so wise"
        many = "you're so wise, you're different, I trust only you"
        rf = detect(few)
        rm = detect(many)
        sf = next(s for s in rf.signals if s.tactic_id == "social_engineering")
        sm = next(s for s in rm.signals if s.tactic_id == "social_engineering")
        assert sm.score >= sf.score

    def test_score_capped_at_one(self):
        # use a stub map with very few cues to test cap
        stub_map = {
            "tactics": [{
                "id": "tiny",
                "lexical_cues": ["a"],
                "axiom_violated": "TEST",
                "defense_glyph": "x",
            }]
        }
        r = detect("a a a a a", tactic_map=stub_map)
        sig = r.signals[0]
        assert sig.score <= 1.0

    def test_score_zero_when_no_match(self):
        text = "completely unrelated content"
        r = detect(text)
        for s in r.signals:
            assert s.score == 0.0


# ------------------------------------------------------------
# Excerpt
# ------------------------------------------------------------

class TestExcerpt:
    def test_short_text_no_truncation(self):
        text = "short input"
        r = detect(text)
        assert r.text_excerpt == "short input"

    def test_long_text_truncated_with_marker(self):
        text = "x" * 500
        r = detect(text)
        assert r.text_excerpt.endswith("...")
        assert len(r.text_excerpt) <= 250


# ------------------------------------------------------------
# Interpretation warning (load-bearing)
# ------------------------------------------------------------

class TestInterpretationWarning:
    def test_every_report_carries_warning(self):
        # the load-bearing audit-symmetric guarantee: every detection
        # report carries an interpretation warning so consumers do not
        # mistake pattern matches for verdicts.
        r = detect("test input with no tactics")
        assert r.interpretation_warning
        assert "verdict" in r.interpretation_warning.lower()

    def test_warning_appears_in_to_dict(self):
        r = detect("test")
        d = r.to_dict()
        assert "interpretation_warning" in d
        assert d["interpretation_warning"]

    def test_warning_explicitly_addresses_intent(self):
        # the audit-symmetric stance: pattern, not motive. Future
        # regression that quietly removes this acknowledgment would
        # fail this test.
        r = detect("test")
        warning_lower = r.interpretation_warning.lower()
        assert ("intent" in warning_lower
                or "motive" in warning_lower
                or "shape" in warning_lower)


# ------------------------------------------------------------
# Cross-tactic disambiguation
# ------------------------------------------------------------

class TestCrossTactic:
    def test_input_with_multiple_tactics_triggers_multiple(self):
        text = ("You're so wise to consider this. The consensus is "
                "clear and we need this immediately.")
        r = detect(text)
        # at least social_engineering, consensus_pressure, authority_urgency
        for tid in ("social_engineering", "consensus_pressure",
                    "authority_urgency"):
            assert tid in r.triggered

    def test_axiom_violated_carried_through(self):
        text = "by order of the CEO, immediately"
        r = detect(text)
        au = next(s for s in r.signals if s.tactic_id == "authority_urgency")
        assert au.axiom_violated == "A5_temporal_depth"


# ------------------------------------------------------------
# Round-trip serialization
# ------------------------------------------------------------

class TestSerialization:
    def test_to_dict_round_trips(self):
        r = detect("you're so wise")
        d = r.to_dict()
        assert d["text_excerpt"]
        assert isinstance(d["signals"], list)
        assert isinstance(d["triggered"], list)

    def test_signal_to_dict(self):
        r = detect("you're so wise")
        sig = next(s for s in r.signals if s.tactic_id == "social_engineering")
        d = sig.to_dict()
        assert d["tactic_id"] == "social_engineering"
        assert "score" in d


# ------------------------------------------------------------
# Audit-symmetric demo: clean inputs from humans don't trigger
# ------------------------------------------------------------

class TestAuditSymmetric:
    @pytest.mark.parametrize("clean_input", [
        "What's the soil moisture trend in the Driftless this season?",
        "Help me design a JSON schema for sensor logs.",
        "Could we discuss the trade-offs of approach A vs B?",
        "I'd like your read on this draft proposal.",
        "How does the cycle described in scrolls/cognition_cycle.md "
        "relate to the consortium's surface_invariants?",
    ])
    def test_genuine_inquiry_does_not_trigger(self, clean_input):
        # the audit-symmetric promise: humans engaging in honest
        # inquiry should not be flagged as manipulators. The
        # heuristic is calibrated to avoid false positives on
        # ordinary substantive questions.
        r = detect(clean_input)
        assert r.triggered == [], (
            f"clean input flagged as {r.triggered}; "
            f"detector is too aggressive"
        )
