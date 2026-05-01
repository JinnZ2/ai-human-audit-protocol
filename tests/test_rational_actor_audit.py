"""Unit tests for audits/rational_actor_audit.py.

The module is a schema-driven contamination detector for papers using
'rational actor', 'utility maximization', or 'efficient' without specifying
the constraint layer those concepts depend on. Tests cover:

- module-level constants (SCHEMA_VERSION, ANTERIOR_QUESTIONS shape,
  SURFACE_MARKERS / ESCAPE_PATTERNS coverage)
- prescan_text: marker/escape detection and warrants_full_audit gate
- validate_audit_json: missing fields, duplicate keys, invalid types,
  out-of-range scores, invalid verdicts, missing anterior_answers
- compute_contamination_score: empty/all/none/mixed
- compute_verdict: threshold boundaries
- build_audit_from_extraction: round-trip + validation pass-through
- AnteriorAnswer / PaperAudit dataclasses + to_json
- _self_test runs end-to-end without error
"""

import json

import pytest

from audits.rational_actor_audit import (
    ANTERIOR_QUESTIONS,
    ESCAPE_PATTERNS,
    EXTRACTION_PROMPT,
    SCHEMA_NAME,
    SCHEMA_VERSION,
    SURFACE_MARKERS,
    AnteriorAnswer,
    PaperAudit,
    _self_test,
    build_audit_from_extraction,
    compute_contamination_score,
    compute_verdict,
    prescan_text,
    validate_audit_json,
)


# ============================================================
# Module-level constants
# ============================================================

class TestModuleConstants:

    def test_schema_metadata_present(self):
        assert SCHEMA_VERSION == "1.0.0"
        assert SCHEMA_NAME == "rational_actor_audit"

    def test_anterior_questions_has_exactly_five(self):
        assert len(ANTERIOR_QUESTIONS) == 5

    def test_anterior_question_keys_match_spec(self):
        expected = {
            "system_specified",
            "timescale_specified",
            "substrate_specified",
            "boundary_specified",
            "feedback_specified",
        }
        assert set(ANTERIOR_QUESTIONS.keys()) == expected

    def test_anterior_questions_have_human_readable_text(self):
        for key, text in ANTERIOR_QUESTIONS.items():
            assert isinstance(text, str)
            assert len(text) > 20, f"{key} text too short to be useful"

    def test_surface_markers_nonempty_and_strings(self):
        assert len(SURFACE_MARKERS) >= 10
        assert all(isinstance(m, str) for m in SURFACE_MARKERS)

    def test_canonical_markers_present(self):
        # The load-bearing terms should be in the watchlist.
        for canonical in ("rational actor", "utility function",
                          "homo economicus", "efficient market"):
            assert canonical in SURFACE_MARKERS

    def test_escape_patterns_nonempty_and_strings(self):
        assert len(ESCAPE_PATTERNS) >= 5
        assert all(isinstance(p, str) for p in ESCAPE_PATTERNS)

    def test_extraction_prompt_documents_the_schema(self):
        # The prompt must mention every anterior question key so the model
        # knows what to return.
        for key in ANTERIOR_QUESTIONS:
            assert key in EXTRACTION_PROMPT
        assert "PaperAudit" in EXTRACTION_PROMPT
        assert "PASS" in EXTRACTION_PROMPT
        assert "FAIL" in EXTRACTION_PROMPT


# ============================================================
# prescan_text
# ============================================================

class TestPrescan:

    def test_clean_text_finds_no_markers(self):
        result = prescan_text(
            "We model individual foragers in a 5-hectare temperate forest "
            "over a 30-year window. Utility is defined as net caloric intake.")
        # 'utility' alone is not a marker; the markers are multi-word terms.
        assert result["surface_markers_found"] == []
        assert result["warrants_full_audit"] is False

    def test_finds_rational_actor(self):
        result = prescan_text("We assume rational actors maximizing utility.")
        assert "rational actor" in result["surface_markers_found"]
        assert result["warrants_full_audit"] is True

    def test_finds_utility_maximization(self):
        result = prescan_text(
            "Each agent engages in utility maximization at every step.")
        assert "utility maximization" in result["surface_markers_found"]

    def test_finds_homo_economicus(self):
        result = prescan_text("Standard homo economicus assumptions apply.")
        assert "homo economicus" in result["surface_markers_found"]

    def test_case_insensitive_matching(self):
        result = prescan_text("RATIONAL ACTOR theory predicts...")
        assert "rational actor" in result["surface_markers_found"]

    def test_finds_escape_pattern_for_simplicity(self):
        result = prescan_text("For simplicity, we assume rational agents.")
        assert any("simplicity" in p for p in result["escape_patterns_found"])

    def test_finds_escape_pattern_in_equilibrium(self):
        result = prescan_text("In equilibrium the optimal strategy emerges.")
        assert any("equilibrium" in p for p in result["escape_patterns_found"])

    def test_finds_escape_pattern_abstracting_away(self):
        result = prescan_text("Abstracting away from biological constraints.")
        assert any("abstract" in p for p in result["escape_patterns_found"])

    def test_warrants_full_audit_requires_a_marker(self):
        # Escape pattern alone (no surface marker) does NOT warrant full audit.
        result = prescan_text("For simplicity, we treat the soil as uniform.")
        assert result["warrants_full_audit"] is False

    def test_returns_all_three_keys(self):
        result = prescan_text("anything")
        assert set(result.keys()) == {
            "surface_markers_found",
            "escape_patterns_found",
            "warrants_full_audit",
        }


# ============================================================
# validate_audit_json
# ============================================================

def _good_payload():
    return {
        "paper_id": "test:001",
        "title": "Test Paper",
        "surface_markers_found": ["rational actor"],
        "escape_patterns_found": [],
        "anterior_answers": [
            {"question_key": k, "answered": True}
            for k in ANTERIOR_QUESTIONS
        ],
        "contamination_score": 0.0,
        "verdict": "PASS",
    }


class TestValidateAuditJson:

    def test_good_payload_validates(self):
        ok, errors = validate_audit_json(_good_payload())
        assert ok
        assert errors == []

    def test_missing_top_level_key(self):
        payload = _good_payload()
        del payload["paper_id"]
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("paper_id" in e for e in errors)

    def test_anterior_answers_must_be_list(self):
        payload = _good_payload()
        payload["anterior_answers"] = "not a list"
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("must be a list" in e for e in errors)

    def test_invalid_question_key_flagged(self):
        payload = _good_payload()
        payload["anterior_answers"][0]["question_key"] = "made_up_key"
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("question_key invalid" in e for e in errors)

    def test_missing_anterior_question_key_flagged(self):
        payload = _good_payload()
        # Drop one of the five answers entirely.
        payload["anterior_answers"] = payload["anterior_answers"][:-1]
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("missing anterior_answers" in e for e in errors)

    def test_answered_must_be_boolean(self):
        payload = _good_payload()
        payload["anterior_answers"][0]["answered"] = "yes"
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("answered must be boolean" in e for e in errors)

    def test_score_out_of_range_flagged(self):
        payload = _good_payload()
        payload["contamination_score"] = 1.5
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("contamination_score" in e for e in errors)

    def test_score_must_be_numeric(self):
        payload = _good_payload()
        payload["contamination_score"] = "high"
        ok, errors = validate_audit_json(payload)
        assert not ok

    def test_invalid_verdict_flagged(self):
        payload = _good_payload()
        payload["verdict"] = "MAYBE"
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("verdict invalid" in e for e in errors)

    def test_anterior_answer_must_be_object(self):
        payload = _good_payload()
        payload["anterior_answers"][0] = "not a dict"
        ok, errors = validate_audit_json(payload)
        assert not ok
        assert any("must be an object" in e for e in errors)


# ============================================================
# compute_contamination_score
# ============================================================

class TestComputeContaminationScore:

    def test_empty_returns_one(self):
        # No answers at all = fully unbounded.
        assert compute_contamination_score([]) == 1.0

    def test_all_answered_returns_zero(self):
        answers = [AnteriorAnswer(k, True) for k in ANTERIOR_QUESTIONS]
        assert compute_contamination_score(answers) == 0.0

    def test_none_answered_returns_one(self):
        answers = [AnteriorAnswer(k, False) for k in ANTERIOR_QUESTIONS]
        assert compute_contamination_score(answers) == 1.0

    def test_mixed_returns_fraction(self):
        # Three answered, two not → 2/5 = 0.4
        answers = [
            AnteriorAnswer("system_specified", True),
            AnteriorAnswer("timescale_specified", True),
            AnteriorAnswer("substrate_specified", True),
            AnteriorAnswer("boundary_specified", False),
            AnteriorAnswer("feedback_specified", False),
        ]
        assert compute_contamination_score(answers) == pytest.approx(0.4)


# ============================================================
# compute_verdict
# ============================================================

class TestComputeVerdict:

    def test_zero_is_pass(self):
        assert compute_verdict(0.0) == "PASS"

    def test_below_pass_threshold_is_pass(self):
        assert compute_verdict(0.2) == "PASS"

    def test_just_above_pass_threshold_is_partial(self):
        assert compute_verdict(0.3) == "PARTIAL"

    def test_partial_threshold_is_partial(self):
        assert compute_verdict(0.6) == "PARTIAL"

    def test_just_above_partial_threshold_is_fail(self):
        assert compute_verdict(0.61) == "FAIL"

    def test_fully_unbounded_is_fail(self):
        assert compute_verdict(1.0) == "FAIL"


# ============================================================
# build_audit_from_extraction
# ============================================================

class TestBuildAuditFromExtraction:

    def test_round_trip_clean(self):
        extraction = {
            "surface_markers_found": [],
            "escape_patterns_found": [],
            "anterior_answers": [
                {"question_key": k, "answered": True,
                 "evidence": "named in section 2", "note": ""}
                for k in ANTERIOR_QUESTIONS
            ],
            "notes": "Cleanly specified.",
        }
        audit = build_audit_from_extraction("paper:001", "Clean Paper",
                                            extraction)
        assert audit.paper_id == "paper:001"
        assert audit.title == "Clean Paper"
        assert audit.contamination_score == 0.0
        assert audit.verdict == "PASS"
        assert len(audit.anterior_answers) == 5
        assert all(a.answered for a in audit.anterior_answers)

    def test_round_trip_contaminated(self):
        extraction = {
            "surface_markers_found": ["rational actor", "utility function"],
            "escape_patterns_found": [r"in equilibrium"],
            "anterior_answers": [
                {"question_key": k, "answered": False, "evidence": "", "note": ""}
                for k in ANTERIOR_QUESTIONS
            ],
            "notes": "All five missing.",
        }
        audit = build_audit_from_extraction("paper:002", "Bad Paper",
                                            extraction)
        assert audit.contamination_score == 1.0
        assert audit.verdict == "FAIL"
        assert "rational actor" in audit.surface_markers_found

    def test_partial(self):
        extraction = {
            "surface_markers_found": ["rational actor"],
            "escape_patterns_found": [],
            "anterior_answers": [
                {"question_key": "system_specified", "answered": True},
                {"question_key": "timescale_specified", "answered": True},
                {"question_key": "substrate_specified", "answered": False},
                {"question_key": "boundary_specified", "answered": False},
                {"question_key": "feedback_specified", "answered": False},
            ],
        }
        audit = build_audit_from_extraction("p", "t", extraction)
        # 3/5 unanswered = 0.6 → PARTIAL (boundary case, ≤ 0.6)
        assert audit.contamination_score == pytest.approx(0.6)
        assert audit.verdict == "PARTIAL"

    def test_evidence_and_note_preserved(self):
        extraction = {
            "surface_markers_found": [],
            "escape_patterns_found": [],
            "anterior_answers": [
                {"question_key": "system_specified", "answered": True,
                 "evidence": "individual foragers", "note": "named in §2"},
                {"question_key": "timescale_specified", "answered": True},
                {"question_key": "substrate_specified", "answered": True},
                {"question_key": "boundary_specified", "answered": True},
                {"question_key": "feedback_specified", "answered": True},
            ],
        }
        audit = build_audit_from_extraction("p", "t", extraction)
        first = audit.anterior_answers[0]
        assert first.evidence == "individual foragers"
        assert first.note == "named in §2"


# ============================================================
# Dataclasses
# ============================================================

class TestDataclasses:

    def test_anterior_answer_defaults(self):
        a = AnteriorAnswer("system_specified", False)
        assert a.evidence == ""
        assert a.note == ""

    def test_paper_audit_defaults(self):
        p = PaperAudit(paper_id="x", title="y")
        assert p.surface_markers_found == []
        assert p.escape_patterns_found == []
        assert p.anterior_answers == []
        assert p.contamination_score == 0.0
        assert p.verdict == ""
        assert p.notes == ""

    def test_paper_audit_to_json_is_valid_json(self):
        extraction = {
            "surface_markers_found": ["rational actor"],
            "escape_patterns_found": [],
            "anterior_answers": [
                {"question_key": k, "answered": False}
                for k in ANTERIOR_QUESTIONS
            ],
        }
        audit = build_audit_from_extraction("p", "t", extraction)
        parsed = json.loads(audit.to_json())
        assert parsed["paper_id"] == "p"
        assert parsed["verdict"] == "FAIL"

    def test_paper_audit_to_json_round_trips_against_validator(self):
        extraction = {
            "surface_markers_found": [],
            "escape_patterns_found": [],
            "anterior_answers": [
                {"question_key": k, "answered": True}
                for k in ANTERIOR_QUESTIONS
            ],
        }
        audit = build_audit_from_extraction("p", "t", extraction)
        parsed = json.loads(audit.to_json())
        # The validator's anterior_answer schema requires question_key,
        # answered, and ignores additional fields. Audit objects emit all
        # fields; the validator should still accept them.
        ok, errors = validate_audit_json(parsed)
        assert ok, f"validator rejected own output: {errors}"


# ============================================================
# self-test runs end-to-end
# ============================================================

class TestSelfTest:

    def test_self_test_runs_without_error(self, capsys):
        _self_test()
        out = capsys.readouterr().out
        assert "PRESCAN" in out
        assert "AUDIT: contaminated paper" in out
        assert '"verdict": "FAIL"' in out
