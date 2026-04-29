"""Unit tests for knowledge_archaeology/biological_mismatch.py.

The module is a regime-check for organisms (humans, populations, individuals)
being forced into environments that contradict their biological baseline. The
core principle: when a behavior is adaptive in regime A but is being deployed
in regime B, the behavior is NOT pathology. It is regime mismatch.

Tests cover:
- regime library shape (every entry has the required fields)
- _keyword_match coarse overlap heuristic
- check_behavior verdicts: no match, adaptive-in-current-env, mismatch
- regime_audit_prompt verdicts: CRITICAL, REGIME MISMATCH, adaptive,
  insufficient data
- MismatchReport.to_dict round-trip
"""

import pytest

from knowledge_archaeology.biological_mismatch import (
    REGIMES,
    BiologicalRegime,
    MismatchReport,
    RegimeCategory,
    _keyword_match,
    check_behavior,
    regime_audit_prompt,
)


# ============================================================
# Regime library
# ============================================================

class TestRegimeLibrary:

    def test_all_regimes_have_required_fields(self):
        for rid, r in REGIMES.items():
            assert r.id == rid
            assert r.traits, rid
            assert r.adaptive_in_environments, rid
            assert r.mismatch_environments, rid
            assert r.common_misdiagnoses, rid

    def test_regime_to_dict_serializes_category_as_string(self):
        r = REGIMES["dyslexic_spatial"]
        d = r.to_dict()
        assert d["category"] == "neurocognitive"
        assert isinstance(d["category"], str)

    def test_all_categories_have_at_least_one_regime(self):
        covered = {r.category for r in REGIMES.values()}
        for cat in RegimeCategory:
            assert cat in covered, f"category {cat.value} has no regime"

    def test_regime_dataclass_construction(self):
        r = BiologicalRegime(
            id="example",
            name="example",
            category=RegimeCategory.NEUROCOGNITIVE,
            description="x",
            traits=["a"],
            adaptive_in_environments=["b"],
            mismatch_environments=["c"],
            common_misdiagnoses=["d"],
        )
        assert r.id == "example"
        assert r.category is RegimeCategory.NEUROCOGNITIVE


# ============================================================
# _keyword_match
# ============================================================

class TestKeywordMatch:

    def test_empty_phrase_returns_false(self):
        assert not _keyword_match("", "anything goes here")

    def test_only_stopwords_returns_false(self):
        assert not _keyword_match("a an the", "lots of words present")

    def test_full_overlap_returns_true(self):
        assert _keyword_match(
            "spatial reasoning",
            "high spatial reasoning capability")

    def test_no_overlap_returns_false(self):
        assert not _keyword_match(
            "elephant migrations",
            "credential gated bureaucratic forms")

    def test_partial_overlap_below_threshold(self):
        # "spatial reasoning kinetic embodied" → 4 meaningful words.
        # Threshold is ceil(4/2) = 2. One match should not be enough.
        assert not _keyword_match(
            "spatial reasoning kinetic embodied",
            "spatial calculations only")

    def test_punctuation_stripped(self):
        assert _keyword_match(
            "high-throughput, motion-regulating systems.",
            "throughput motion systems running")


# ============================================================
# check_behavior — no match
# ============================================================

class TestCheckBehaviorNoMatch:

    def test_unrelated_behavior_returns_empty_match(self):
        report = check_behavior(
            "purple elephants float gracefully through clouds",
            "imaginary environment")
        assert report.matching_regimes == []
        assert report.is_adaptive_somewhere is False
        assert report.is_adaptive_in_current_environment is False
        assert "DO NOT pathologize" in report.recommendation


# ============================================================
# check_behavior — adaptive in current environment
# ============================================================

class TestCheckBehaviorAdaptiveHere:

    def test_truck_driver_high_energy_in_mobile_work(self):
        report = check_behavior(
            "high baseline energy continuous engagement preference "
            "stress regulation through motion",
            "long-haul physical work multi-domain problem solving")
        assert "high_throughput_nervous_system" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is True
        assert report.likely_misdiagnoses == []
        assert "RECOGNIZE" in report.recommendation


# ============================================================
# check_behavior — regime mismatch (the load-bearing path)
# ============================================================

class TestCheckBehaviorMismatch:

    def test_dyslexic_in_bureaucratic_environment(self):
        report = check_behavior(
            "frustration with paperwork slow text processing low test scores "
            "despite high capability",
            "text-heavy bureaucratic office work credential-gated career")
        assert "dyslexic_spatial" in report.matching_regimes
        assert report.is_adaptive_somewhere is True
        assert report.is_adaptive_in_current_environment is False
        assert report.likely_misdiagnoses
        assert "environment is the constraint" in report.actual_constraint

    def test_distributed_decision_in_corporate_hierarchy(self):
        report = check_behavior(
            "questioning authority directives coalition-building with peers "
            "slow compliance with unilateral orders",
            "corporate top-down hierarchy mandatory schooling")
        assert "distributed_decision_baseline" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is False

    def test_care_masculine_in_status_culture(self):
        report = check_behavior(
            "preferring time with children to status competition "
            "low motivation for status-display work",
            "corporate masculinity frames status-via-economic-dominance culture")
        assert "care_capacity_masculine" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is False

    def test_cyclical_hormonal_in_constant_productivity(self):
        report = check_behavior(
            "cyclic energy fluctuation across weeks, monthly cognitive shifts, "
            "premenstrual sensitivity called moodiness",
            "constant linear productivity demands, quarterly performance "
            "metrics insensitive to cycles")
        assert "cyclical_hormonal_regulation" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is False

    def test_extended_maturation_in_age_graded_school(self):
        report = check_behavior(
            "behind same-age peers academically, called late bloomer, "
            "social awkwardness in cohort",
            "standardized-age testing systems, K-12 grade-by-birth-year structures")
        assert "extended_maturation" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is False

    def test_systematizing_in_open_plan_office(self):
        report = check_behavior(
            "deep pattern systematizing, intense special interests, "
            "literal language processing, sensory overload",
            "open-plan offices high-stimulation workplaces, "
            "small talk ambiguous interpersonal politics")
        assert "systematizing_neurodivergent" in report.matching_regimes
        assert report.is_adaptive_in_current_environment is False


# ============================================================
# regime_audit_prompt — the audit wrapper
# ============================================================

class TestRegimeAuditPrompt:

    def test_critical_when_proposed_diagnosis_matches_misdiagnosis(self):
        result = regime_audit_prompt(
            "adult",
            "frustration with paperwork slow text processing low test scores",
            "text-heavy bureaucratic office work credential-gated career",
            proposed_diagnosis="low intelligence, learning disabled",
        )
        assert result["verdict"].startswith("CRITICAL")

    def test_regime_mismatch_when_no_diagnosis_proposed(self):
        result = regime_audit_prompt(
            "adult",
            "frustration with paperwork slow text processing low test scores",
            "text-heavy bureaucratic office work credential-gated career",
            proposed_diagnosis="",
        )
        assert result["verdict"].startswith("REGIME MISMATCH")

    def test_recognize_when_environment_is_adaptive(self):
        result = regime_audit_prompt(
            "athlete",
            "high baseline energy continuous engagement stress regulation "
            "through motion",
            "long-haul physical work multi-domain problem solving",
        )
        assert "Behavior is adaptive in current environment" in result["verdict"]

    def test_insufficient_data_when_no_regime_matches(self):
        result = regime_audit_prompt(
            "subject",
            "elephant migration song dancing patterns",
            "imaginary cloud field",
        )
        assert result["verdict"].startswith("Insufficient regime data")

    def test_audit_includes_questions_and_subject(self):
        result = regime_audit_prompt(
            "adult", "behavior", "environment", "diagnosis")
        assert result["subject"] == "adult"
        assert result["proposed_diagnosis"] == "diagnosis"
        assert len(result["audit_questions"]) >= 4

    def test_regime_check_dict_present(self):
        result = regime_audit_prompt(
            "adult", "behavior", "environment", "")
        assert "regime_check" in result
        assert "matching_regimes" in result["regime_check"]


# ============================================================
# MismatchReport
# ============================================================

class TestMismatchReport:

    def test_to_dict_round_trip(self):
        report = check_behavior("anything", "anywhere")
        d = report.to_dict()
        assert "matching_regimes" in d
        assert "recommendation" in d
        assert "actual_constraint" in d

    def test_dataclass_fields_present(self):
        report = check_behavior(
            "frustration with paperwork slow text processing",
            "text-heavy bureaucratic office work")
        assert isinstance(report, MismatchReport)
        assert isinstance(report.matching_regimes, list)
        assert isinstance(report.likely_misdiagnoses, list)
