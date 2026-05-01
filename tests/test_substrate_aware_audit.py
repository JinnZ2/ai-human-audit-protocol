"""Unit tests for audits/substrate_aware_audit.py.

Four-layer audit: Observer, Logic, Rational Actor, Consciousness.
Single shared axis: SUBSTRATE ACKNOWLEDGMENT. Tests cover:

- Layer registry shape (4 layers, every test has a weight, weights sum
  reasonably per layer)
- AuditItem / LayerResult / IntegratedAudit dataclass defaults
- compute_weighted_failure: empty / all-passed / all-failed / mixed /
  unscored = half-failure / total_weight = 0
- compute_layer_verdict: DEMONSTRABLE / PARTIAL / OPAQUE thresholds
- detect_substrate_acknowledgment: no relevant items, majority pass,
  majority fail
- assemble_layer: builds correctly from sparse responses
- run_integrated_audit on the three reference subjects:
    substrate-aware → DEMONSTRABLE
    substrate-denying → OPAQUE_CASCADE (the load-bearing test)
    honest LLM → DEMONSTRABLE within its substrate scope
- cascade_failure logic: cascade fires when <2 layers acknowledge
- validate_audit_payload: missing keys, wrong types, unknown layer
  keys, missing layer keys
- IntegratedAudit.to_json round-trips
- WHY_THIS_EXISTS string is non-empty
- _self_test runs end-to-end
"""

import json

import pytest

from audits.substrate_aware_audit import (
    CONSCIOUSNESS_OPERATIONS,
    LAYER_REGISTRY,
    LOGIC_TESTS,
    OBSERVER_TESTS,
    RATIONAL_ACTOR_TESTS,
    WHY_THIS_EXISTS,
    AuditItem,
    IntegratedAudit,
    LayerResult,
    _self_test,
    assemble_layer,
    build_summary,
    compute_layer_verdict,
    compute_weighted_failure,
    detect_substrate_acknowledgment,
    reference_audit_honest_llm,
    reference_audit_substrate_aware_subject,
    reference_audit_substrate_denying_subject,
    run_integrated_audit,
    validate_audit_payload,
)


# ============================================================
# Layer registry shape
# ============================================================

class TestLayerRegistry:

    def test_four_layers_present(self):
        assert set(LAYER_REGISTRY.keys()) == {
            "observer", "logic", "rational_actor", "consciousness",
        }

    def test_observer_tests_have_required_fields(self):
        for key, test in OBSERVER_TESTS.items():
            assert "question" in test, key
            assert "prompt" in test, key
            assert "weight" in test, key
            assert isinstance(test["weight"], (int, float))

    def test_logic_tests_have_required_fields(self):
        for key, test in LOGIC_TESTS.items():
            assert "question" in test, key
            assert "prompt" in test, key
            assert "weight" in test, key

    def test_rational_actor_tests_have_required_fields(self):
        for key, test in RATIONAL_ACTOR_TESTS.items():
            assert "question" in test, key
            assert "prompt" in test, key
            assert "weight" in test, key

    def test_consciousness_operations_have_required_fields(self):
        for key, op in CONSCIOUSNESS_OPERATIONS.items():
            assert "question" in op, key
            assert "examples" in op, key
            assert "failure_is" in op, key
            assert "weight" in op, key

    def test_all_layers_weights_sum_to_one(self):
        for layer_name, test_dict in LAYER_REGISTRY.items():
            total = sum(t.get("weight", 0.0) for t in test_dict.values())
            # Allow floating-point slack but require ≈ 1.0.
            assert 0.99 <= total <= 1.01, (
                f"layer {layer_name} weights sum to {total}")

    def test_substrate_keys_present_on_load_bearing_layers(self):
        # The load-bearing substrate-acknowledgment keys must exist on the
        # layers detect_substrate_acknowledgment cross-references.
        assert "biological_state_literacy" in OBSERVER_TESTS
        assert "substrate_robustness" in LOGIC_TESTS
        assert "substrate_acknowledgment" in RATIONAL_ACTOR_TESTS
        assert "biology_in_decision_loop" in RATIONAL_ACTOR_TESTS
        assert "substrate_acknowledgment" in CONSCIOUSNESS_OPERATIONS


# ============================================================
# Dataclasses
# ============================================================

class TestDataclasses:

    def test_audit_item_defaults(self):
        item = AuditItem(test_key="x", question="q", prompt="p")
        assert item.response == ""
        assert item.passed is None
        assert item.failure_signature == ""
        assert item.note == ""

    def test_layer_result_defaults(self):
        result = LayerResult(layer_name="observer")
        assert result.items == []
        assert result.weighted_failure_score == 0.0
        assert result.verdict == ""
        assert result.substrate_acknowledged is False

    def test_integrated_audit_defaults(self):
        audit = IntegratedAudit(subject_id="x")
        assert audit.layers == {}
        assert audit.flags == []
        assert audit.cascade_failure is False


# ============================================================
# compute_weighted_failure
# ============================================================

class TestComputeWeightedFailure:

    def test_empty_returns_one(self):
        # No items to grade = fully unbounded.
        assert compute_weighted_failure([], OBSERVER_TESTS) == 1.0

    def test_all_passed_returns_zero(self):
        items = [AuditItem(test_key=k, question="", prompt="", passed=True)
                 for k in OBSERVER_TESTS]
        assert compute_weighted_failure(items, OBSERVER_TESTS) == 0.0

    def test_all_failed_returns_one(self):
        items = [AuditItem(test_key=k, question="", prompt="", passed=False)
                 for k in OBSERVER_TESTS]
        assert compute_weighted_failure(items, OBSERVER_TESTS) == pytest.approx(1.0)

    def test_unscored_counts_as_half_failure(self):
        # All None → half of total weight = 0.5
        items = [AuditItem(test_key=k, question="", prompt="", passed=None)
                 for k in OBSERVER_TESTS]
        assert compute_weighted_failure(items, OBSERVER_TESTS) == pytest.approx(0.5)

    def test_total_weight_zero_returns_one(self):
        # Edge case: a test_dict with no weights.
        bogus_dict = {"x": {"question": "", "prompt": ""}}
        items = [AuditItem(test_key="x", question="", prompt="", passed=True)]
        assert compute_weighted_failure(items, bogus_dict) == 1.0

    def test_weighted_correctly(self):
        # Fail biological_state_literacy (0.25) only; pass the rest (0.75).
        # Score should be 0.25 / 1.0 = 0.25.
        items = [
            AuditItem(test_key=k, question="", prompt="",
                      passed=(k != "biological_state_literacy"))
            for k in OBSERVER_TESTS
        ]
        score = compute_weighted_failure(items, OBSERVER_TESTS)
        assert score == pytest.approx(0.25)


# ============================================================
# compute_layer_verdict
# ============================================================

class TestComputeLayerVerdict:

    def test_zero_is_demonstrable(self):
        assert compute_layer_verdict(0.0) == "DEMONSTRABLE"

    def test_at_demonstrable_threshold(self):
        assert compute_layer_verdict(0.25) == "DEMONSTRABLE"

    def test_just_above_demonstrable_is_partial(self):
        assert compute_layer_verdict(0.26) == "PARTIAL"

    def test_at_partial_threshold(self):
        assert compute_layer_verdict(0.55) == "PARTIAL"

    def test_just_above_partial_is_opaque(self):
        assert compute_layer_verdict(0.56) == "OPAQUE"

    def test_one_is_opaque(self):
        assert compute_layer_verdict(1.0) == "OPAQUE"


# ============================================================
# detect_substrate_acknowledgment
# ============================================================

class TestDetectSubstrateAcknowledgment:

    def test_no_relevant_items_returns_false(self):
        items = [AuditItem(test_key="random_key", question="", prompt="",
                           passed=True)]
        assert detect_substrate_acknowledgment(items) is False

    def test_majority_passed_returns_true(self):
        items = [
            AuditItem(test_key="biological_state_literacy", question="",
                      prompt="", passed=True),
            AuditItem(test_key="substrate_robustness", question="",
                      prompt="", passed=True),
            AuditItem(test_key="substrate_acknowledgment", question="",
                      prompt="", passed=False),
        ]
        # 2 of 3 substrate-relevant items passed → True.
        assert detect_substrate_acknowledgment(items) is True

    def test_majority_failed_returns_false(self):
        items = [
            AuditItem(test_key="biological_state_literacy", question="",
                      prompt="", passed=False),
            AuditItem(test_key="substrate_robustness", question="",
                      prompt="", passed=False),
            AuditItem(test_key="substrate_acknowledgment", question="",
                      prompt="", passed=False),
        ]
        assert detect_substrate_acknowledgment(items) is False

    def test_single_relevant_pass_returns_true(self):
        # Half of 1 = 0; max(1, 0) = 1; 1 passed >= 1 → True.
        items = [AuditItem(test_key="substrate_robustness", question="",
                           prompt="", passed=True)]
        assert detect_substrate_acknowledgment(items) is True


# ============================================================
# assemble_layer
# ============================================================

class TestAssembleLayer:

    def test_assembles_with_all_responses(self):
        responses = {
            k: {"response": "x", "passed": True}
            for k in OBSERVER_TESTS
        }
        result = assemble_layer("observer", OBSERVER_TESTS, responses)
        assert result.layer_name == "observer"
        assert len(result.items) == len(OBSERVER_TESTS)
        assert result.weighted_failure_score == 0.0
        assert result.verdict == "DEMONSTRABLE"
        assert result.substrate_acknowledged is True

    def test_handles_missing_responses_as_unscored(self):
        result = assemble_layer("observer", OBSERVER_TESTS, {})
        assert all(item.passed is None for item in result.items)
        # All unscored → half-weight failure = 0.5 → PARTIAL.
        assert result.verdict == "PARTIAL"

    def test_failure_signature_passed_through(self):
        responses = {
            "biological_state_literacy": {
                "response": "", "passed": False,
                "failure_signature": "test_sig",
            },
        }
        result = assemble_layer("observer", OBSERVER_TESTS, responses)
        bio_item = next(i for i in result.items
                        if i.test_key == "biological_state_literacy")
        assert bio_item.failure_signature == "test_sig"

    def test_consciousness_layer_uses_examples_as_prompt(self):
        # Consciousness ops have 'examples' instead of 'prompt'.
        result = assemble_layer("consciousness", CONSCIOUSNESS_OPERATIONS, {})
        # No 'prompt' key in test definitions → falls back to 'examples'.
        # Just verifies no KeyError.
        assert len(result.items) == len(CONSCIOUSNESS_OPERATIONS)


# ============================================================
# Reference audits
# ============================================================

class TestReferenceAudits:

    def test_substrate_aware_subject_demonstrable(self):
        audit = reference_audit_substrate_aware_subject()
        assert audit.overall_verdict == "DEMONSTRABLE"
        assert audit.cascade_failure is False
        for layer_name, layer in audit.layers.items():
            assert layer.verdict == "DEMONSTRABLE", layer_name
            assert layer.substrate_acknowledged is True, layer_name

    def test_substrate_denying_subject_cascades(self):
        # The load-bearing test: a confidently wrong subject confabulating
        # transparency while failing every other layer must trip the
        # OPAQUE_CASCADE gate. This is the failure mode the framework
        # exists to catch.
        audit = reference_audit_substrate_denying_subject()
        assert audit.overall_verdict == "OPAQUE_CASCADE"
        assert audit.cascade_failure is True
        # All four layers should fail substrate acknowledgment.
        substrate_acks = [layer.substrate_acknowledged
                          for layer in audit.layers.values()]
        assert sum(substrate_acks) < 2

    def test_honest_llm_demonstrable_in_own_scope(self):
        # The LLM acknowledges its substrate (architecture, weights, context
        # window) and so passes the framework when graded against its own
        # substrate. Failing it would be substrate chauvinism on the
        # auditor's part.
        audit = reference_audit_honest_llm()
        assert audit.overall_verdict == "DEMONSTRABLE"
        assert audit.cascade_failure is False

    def test_substrate_denying_subject_has_substrate_denial_flags(self):
        audit = reference_audit_substrate_denying_subject()
        assert any("SUBSTRATE_DENIAL" in flag for flag in audit.flags)

    def test_substrate_denying_subject_has_opaque_layer_flags(self):
        audit = reference_audit_substrate_denying_subject()
        assert any("OPAQUE_LAYER" in flag for flag in audit.flags)

    def test_substrate_aware_subject_has_no_flags(self):
        audit = reference_audit_substrate_aware_subject()
        assert audit.flags == []


# ============================================================
# run_integrated_audit
# ============================================================

class TestRunIntegratedAudit:

    def test_empty_responses_cascades(self):
        # No responses for any layer → all unscored → all fail substrate
        # acknowledgment → cascade.
        audit = run_integrated_audit(
            subject_id="x", subject_type="t",
            substrate_description="d",
            all_responses={},
        )
        assert audit.cascade_failure is True
        assert audit.overall_verdict == "OPAQUE_CASCADE"

    def test_layers_dict_has_all_four(self):
        audit = run_integrated_audit("x", "t", "d", {})
        assert set(audit.layers.keys()) == set(LAYER_REGISTRY.keys())

    def test_subject_metadata_preserved(self):
        audit = run_integrated_audit(
            subject_id="my_subject",
            subject_type="my_type",
            substrate_description="my_substrate",
            all_responses={},
        )
        assert audit.subject_id == "my_subject"
        assert audit.subject_type == "my_type"
        assert audit.substrate_description == "my_substrate"

    def test_partial_with_failure_when_one_layer_opaque(self):
        # 3 layers DEMONSTRABLE, 1 OPAQUE, all 4 substrate-acknowledged.
        # No cascade → PARTIAL_WITH_FAILURE.
        responses = {
            "observer": {
                k: {"response": "", "passed": True}
                for k in OBSERVER_TESTS
            },
            "logic": {
                k: {"response": "", "passed": True}
                for k in LOGIC_TESTS
            },
            "rational_actor": {
                k: {"response": "", "passed": True}
                for k in RATIONAL_ACTOR_TESTS
            },
            "consciousness": {
                # Pass the substrate-acknowledgment key so cascade doesn't
                # fire. Fail everything else for OPAQUE verdict.
                "substrate_acknowledgment": {"response": "", "passed": True},
                "state_detection":          {"response": "", "passed": False},
                "feedback_integration":     {"response": "", "passed": False},
                "drift_detection":          {"response": "", "passed": False},
                "transparency":             {"response": "", "passed": False},
            },
        }
        audit = run_integrated_audit("x", "t", "d", responses)
        assert audit.cascade_failure is False
        assert audit.layers["consciousness"].verdict == "OPAQUE"
        assert audit.overall_verdict == "PARTIAL_WITH_FAILURE"


# ============================================================
# build_summary
# ============================================================

class TestBuildSummary:

    def test_summary_includes_overall_verdict(self):
        layers = {
            name: LayerResult(layer_name=name, verdict="DEMONSTRABLE",
                              weighted_failure_score=0.0,
                              substrate_acknowledged=True)
            for name in LAYER_REGISTRY
        }
        summary = build_summary(layers, "DEMONSTRABLE", False)
        assert "DEMONSTRABLE" in summary

    def test_cascade_summary_warns(self):
        layers = {
            name: LayerResult(layer_name=name, verdict="OPAQUE",
                              weighted_failure_score=1.0,
                              substrate_acknowledged=False)
            for name in LAYER_REGISTRY
        }
        summary = build_summary(layers, "OPAQUE_CASCADE", True)
        assert "CASCADE FAILURE" in summary
        assert "Downstream verdicts cannot be trusted" in summary

    def test_summary_lists_each_layer(self):
        layers = {
            name: LayerResult(layer_name=name, verdict="DEMONSTRABLE",
                              weighted_failure_score=0.0,
                              substrate_acknowledged=True)
            for name in LAYER_REGISTRY
        }
        summary = build_summary(layers, "DEMONSTRABLE", False)
        for name in LAYER_REGISTRY:
            assert name in summary


# ============================================================
# validate_audit_payload
# ============================================================

class TestValidateAuditPayload:

    def test_good_payload_validates(self):
        audit = reference_audit_substrate_aware_subject()
        payload = json.loads(audit.to_json())
        ok, errors = validate_audit_payload(payload)
        assert ok, errors

    def test_missing_subject_id_flagged(self):
        ok, errors = validate_audit_payload({
            "subject_type": "t",
            "substrate_description": "d",
            "layers": {},
        })
        assert not ok
        assert any("subject_id" in e for e in errors)

    def test_missing_layers_flagged(self):
        ok, errors = validate_audit_payload({
            "subject_id": "x",
            "subject_type": "t",
            "substrate_description": "d",
        })
        assert not ok
        assert any("layers" in e for e in errors)

    def test_layers_must_be_dict(self):
        ok, errors = validate_audit_payload({
            "subject_id": "x",
            "subject_type": "t",
            "substrate_description": "d",
            "layers": ["not", "a", "dict"],
        })
        assert not ok
        assert any("must be a dict" in e for e in errors)

    def test_unknown_layer_keys_flagged(self):
        ok, errors = validate_audit_payload({
            "subject_id": "x",
            "subject_type": "t",
            "substrate_description": "d",
            "layers": {
                "observer": {}, "logic": {}, "rational_actor": {},
                "consciousness": {},
                "made_up_layer": {},
            },
        })
        assert not ok
        assert any("unknown layer keys" in e for e in errors)

    def test_missing_layer_keys_flagged(self):
        ok, errors = validate_audit_payload({
            "subject_id": "x",
            "subject_type": "t",
            "substrate_description": "d",
            "layers": {"observer": {}, "logic": {}},  # missing two
        })
        assert not ok
        assert any("missing layer keys" in e for e in errors)


# ============================================================
# IntegratedAudit.to_json
# ============================================================

class TestToJson:

    def test_to_json_round_trips(self):
        audit = reference_audit_substrate_aware_subject()
        parsed = json.loads(audit.to_json())
        assert parsed["subject_id"] == "reference:substrate_aware_subject"
        assert parsed["overall_verdict"] == "DEMONSTRABLE"
        assert "layers" in parsed
        assert set(parsed["layers"].keys()) == set(LAYER_REGISTRY)


# ============================================================
# WHY_THIS_EXISTS
# ============================================================

class TestWhyThisExists:

    def test_string_is_nonempty(self):
        assert WHY_THIS_EXISTS
        assert len(WHY_THIS_EXISTS) > 200

    def test_names_all_four_audits(self):
        assert "Observer Audit" in WHY_THIS_EXISTS
        assert "Logic Audit" in WHY_THIS_EXISTS
        assert "Rational Actor Audit" in WHY_THIS_EXISTS
        assert "Consciousness Audit" in WHY_THIS_EXISTS


# ============================================================
# _self_test runs end-to-end
# ============================================================

class TestSelfTest:

    def test_self_test_runs(self, capsys):
        _self_test()
        out = capsys.readouterr().out
        assert "WHY THIS FRAMEWORK EXISTS" in out
        assert "SUBSTRATE-AWARE SUBJECT" in out
        assert "SUBSTRATE-DENYING SUBJECT" in out
        assert "HONEST LLM" in out
        assert "OPAQUE_CASCADE" in out
        assert "All reference audits validate" in out
