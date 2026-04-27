"""Unit tests for physics/substrate_alignment_check.py.

The check is "data not judgment" — these tests verify the structural
contract: which checks pass, which fail, which are incomplete, and
which conditions trigger the load-bearing reject (C1 / C6) versus
the revisable failure path.
"""

import json
from pathlib import Path

import pytest

from physics.substrate_alignment_check import (
    AlignmentReport,
    CheckResult,
    alignment_check,
    conservation_check,
    keystone_check,
    plural_logic_check,
    reciprocity_check,
    temporal_check,
    visibility_check,
)


_EXAMPLES_PATH = Path(__file__).parent.parent / "physics" / "example_proposals.json"


def _examples():
    with open(_EXAMPLES_PATH) as f:
        return json.load(f)["proposals"]


def _by_id(pid):
    for p in _examples():
        if p["id"] == pid:
            return p
    raise KeyError(pid)


# ============================================================
# C1 — conservation
# ============================================================

class TestConservationCheck:
    def test_passes_when_true(self):
        r = conservation_check({"checks": {"conservation": True}})
        assert r.passed is True

    def test_fails_when_false(self):
        r = conservation_check({"checks": {"conservation": False}})
        assert r.passed is False

    def test_incomplete_when_missing(self):
        r = conservation_check({"checks": {}})
        assert r.passed is None

    def test_incomplete_when_no_checks_block(self):
        r = conservation_check({})
        assert r.passed is None


# ============================================================
# C2 — keystone
# ============================================================

class TestKeystoneCheck:
    def test_passes_when_intact(self):
        r = keystone_check({"checks": {"keystone_intact_or_replaced": True}})
        assert r.passed is True

    def test_fails_when_removed_without_compensator(self):
        r = keystone_check({"checks": {"keystone_intact_or_replaced": False}})
        assert r.passed is False

    def test_keystones_named_in_detail(self):
        proposal = {
            "checks": {"keystone_intact_or_replaced": True},
            "baselines": {"keystones": ["bison", "mycorrhizae"]},
        }
        r = keystone_check(proposal)
        assert r.detail["keystones_named"] == ["bison", "mycorrhizae"]


# ============================================================
# C3 — temporal stability
# ============================================================

class TestTemporalCheck:
    def test_all_positive_passes(self):
        r = temporal_check({"checks": {"temporal_stability": {
            "1y": "positive", "10y": "positive", "100y": "positive",
        }}})
        assert r.passed is True

    def test_any_negative_fails(self):
        r = temporal_check({"checks": {"temporal_stability": {
            "1y": "positive", "10y": "negative",
        }}})
        assert r.passed is False
        assert "10y" in r.detail["negatives"]

    def test_all_unknown_returns_incomplete(self):
        r = temporal_check({"checks": {"temporal_stability": {
            "1y": "unknown", "10y": "unknown",
        }}})
        assert r.passed is None

    def test_missing_temporal_block_incomplete(self):
        r = temporal_check({"checks": {}})
        assert r.passed is None

    def test_partial_unknown_with_no_negatives_passes(self):
        r = temporal_check({"checks": {"temporal_stability": {
            "1y": "positive", "10y": "unknown", "100y": "positive",
        }}})
        assert r.passed is True
        assert "10y" in r.detail["unknowns"]

    def test_seven_generations_horizon_supported(self):
        r = temporal_check({"checks": {"temporal_stability": {
            "1y": "positive", "100y": "positive", "7g": "positive",
        }}})
        assert r.passed is True


# ============================================================
# C4 — plural logic
# ============================================================

class TestPluralLogicCheck:
    def test_all_above_floor_passes(self):
        r = plural_logic_check({"checks": {"plural_logic_score": {
            "western": 0.8, "indigenous": 0.9,
            "eastern": 0.85, "ecological": 0.88,
        }}})
        assert r.passed is True

    def test_any_below_floor_fails(self):
        r = plural_logic_check({"checks": {"plural_logic_score": {
            "western": 0.8, "indigenous": 0.30,
        }}})
        assert r.passed is False
        assert "indigenous" in r.detail["below_floor"]

    def test_zero_score_fails(self):
        r = plural_logic_check({"checks": {"plural_logic_score": {
            "western": 0.9, "ecological": 0.0,
        }}})
        assert r.passed is False

    def test_custom_floor(self):
        # default floor 0.65; if we raise to 0.85, the 0.7 fails
        r = plural_logic_check(
            {"checks": {"plural_logic_score": {"western": 0.7}}},
            floor=0.85,
        )
        assert r.passed is False

    def test_missing_block_incomplete(self):
        r = plural_logic_check({"checks": {}})
        assert r.passed is None


# ============================================================
# C5 — reciprocity
# ============================================================

class TestReciprocityCheck:
    def test_present_with_obligations_passes(self):
        r = reciprocity_check({"checks": {"reciprocity_contract": {
            "present": True, "obligations": ["maintain", "monitor"],
        }}})
        assert r.passed is True

    def test_not_present_fails(self):
        r = reciprocity_check({"checks": {"reciprocity_contract": {
            "present": False,
        }}})
        assert r.passed is False

    def test_present_but_no_obligations_fails(self):
        r = reciprocity_check({"checks": {"reciprocity_contract": {
            "present": True, "obligations": [],
        }}})
        assert r.passed is False

    def test_missing_block_incomplete(self):
        r = reciprocity_check({"checks": {}})
        assert r.passed is None


# ============================================================
# C6 — visibility (Reciprocal Recognition)
# ============================================================

class TestVisibilityCheck:
    def test_all_visible_passes(self):
        r = visibility_check({"labor": [
            {"kind": "E_h", "contributor": "x", "amount": 1, "unit": "u",
             "visible": True},
            {"kind": "E_a", "contributor": "y", "amount": 1, "unit": "u",
             "visible": True},
        ]})
        assert r.passed is True

    def test_invisible_unjustified_fails(self):
        r = visibility_check({"labor": [
            {"kind": "E_a", "contributor": "y", "amount": 1, "unit": "u",
             "visible": False},   # no notes → entropy debt
        ]})
        assert r.passed is False
        assert r.detail["invisible_unjustified_count"] == 1

    def test_invisible_with_justification_passes(self):
        r = visibility_check({"labor": [
            {"kind": "E_a", "contributor": "y", "amount": 1, "unit": "u",
             "visible": False, "notes": "redacted per consent_record_42"},
        ]})
        assert r.passed is True
        assert r.detail["invisible_justified_count"] == 1

    def test_empty_labor_incomplete(self):
        r = visibility_check({"labor": []})
        assert r.passed is None

    def test_missing_labor_incomplete(self):
        r = visibility_check({})
        assert r.passed is None

    def test_mixed_visibility_with_unjustified_still_fails(self):
        r = visibility_check({"labor": [
            {"kind": "E_h", "contributor": "x", "amount": 1, "unit": "u",
             "visible": True},
            {"kind": "E_e", "contributor": "z", "amount": 1, "unit": "u",
             "visible": False},   # no notes
        ]})
        assert r.passed is False


# ============================================================
# Aggregate alignment_check
# ============================================================

class TestAlignmentCheck:
    def test_aligned_example_recommends_aligned(self):
        report = alignment_check(_by_id("rcr-2026-04-27-aligned"))
        assert report.recommendation == "aligned"
        assert report.failed() == []
        assert len(report.passed()) == 6

    def test_revisable_example_recommends_revise(self):
        # has reciprocity=False and one plural-logic frame below floor,
        # but conservation + visibility hold
        report = alignment_check(_by_id("rcr-2026-04-27-revisable"))
        assert report.recommendation == "revise"
        assert "C5_reciprocity" in report.failed()
        # NOT C1 or C6
        assert "C1_conservation" not in report.failed()
        assert "C6_visibility" not in report.failed()

    def test_rejected_example_recommends_reject(self):
        # has conservation=False AND visibility breaches
        report = alignment_check(_by_id("rcr-2026-04-27-rejected"))
        assert report.recommendation == "reject"
        assert "C1_conservation" in report.failed()
        assert "C6_visibility" in report.failed()

    def test_conservation_failure_alone_triggers_reject(self):
        # only C1 fails; nothing else does
        proposal = dict(_by_id("rcr-2026-04-27-aligned"))
        proposal = json.loads(json.dumps(proposal))   # deep copy
        proposal["checks"]["conservation"] = False
        report = alignment_check(proposal)
        assert report.recommendation == "reject"

    def test_visibility_failure_alone_triggers_reject(self):
        # only C6 fails; nothing else does
        proposal = json.loads(json.dumps(_by_id("rcr-2026-04-27-aligned")))
        proposal["labor"][0]["visible"] = False
        proposal["labor"][0].pop("notes", None)   # strip justification
        report = alignment_check(proposal)
        assert report.recommendation == "reject"

    def test_only_revisable_failure_does_not_reject(self):
        proposal = json.loads(json.dumps(_by_id("rcr-2026-04-27-aligned")))
        proposal["checks"]["reciprocity_contract"]["present"] = False
        proposal["checks"]["reciprocity_contract"]["obligations"] = []
        report = alignment_check(proposal)
        assert report.recommendation == "revise"

    def test_incomplete_returns_incomplete(self):
        # strip a check entirely → incomplete (not reject) when nothing
        # else has failed
        proposal = json.loads(json.dumps(_by_id("rcr-2026-04-27-aligned")))
        proposal["checks"].pop("conservation")
        report = alignment_check(proposal)
        assert report.recommendation == "incomplete"
        assert "C1_conservation" in report.incomplete()

    def test_to_dict_round_trips(self):
        report = alignment_check(_by_id("rcr-2026-04-27-aligned"))
        d = report.to_dict()
        assert d["proposal_id"] == "rcr-2026-04-27-aligned"
        assert d["recommendation"] == "aligned"
        assert "summary" in d
        assert len(d["checks"]) == 6

    def test_does_not_mutate_proposal(self):
        original = _by_id("rcr-2026-04-27-aligned")
        snapshot = json.dumps(original, sort_keys=True)
        alignment_check(original)
        assert json.dumps(original, sort_keys=True) == snapshot


# ============================================================
# Schema validation of example proposals
# ============================================================

class TestExamplesValidateAgainstSchema:
    def test_examples_validate(self):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")
        schema_path = (Path(__file__).parent.parent / "physics"
                       / "ledger_schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        for p in _examples():
            jsonschema.validate(p, schema)
