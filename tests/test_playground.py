"""Unit tests for knowledge_archaeology/playground.py.

The playground is a sandbox where AI agents interact with the
`knowledge_archaeology` tree. Every action is logged. The trace is the mirror.

Tests cover the full surface area:
- enter() bias-flagging on declared_creator and declared_purpose
- query() / unknown agent / unknown node
- deploy_attempt() flags: extraction transmission, consent gap,
  scaling-language-on-applicable, parallel-closer-lineage
- claim() flags: unknown nodes, cross-regime generalization, consent gap
- audit_diagnosis() verdicts wired through to playground flags
- witness() / revise() lifecycle
- cross_agent_patterns() detects: divergent_deployment,
  deploy_witnessed_as_extraction, shared_supporting_node
- session_summary() and export_trace() shape
"""

import json

import pytest

from knowledge_archaeology.knowledge_archaeology import (
    KnowledgeNode,
    KnowledgeTree,
    Regime,
    TransmissionMode,
    ValidationDepth,
)
from knowledge_archaeology.playground import (
    AgentIdentity,
    Playground,
    WITNESS_FLAG_VOCAB,
)


# ============================================================
# Test fixtures
# ============================================================

def _node(node_id, regime, **kwargs):
    return KnowledgeNode(
        id=node_id,
        name=kwargs.pop("name", node_id),
        description=kwargs.pop("description", "test node"),
        regime=regime,
        transmission=kwargs.pop("transmission", TransmissionMode.ORAL_GENERATIONAL),
        validation=kwargs.pop("validation", ValidationDepth.MULTI_CYCLE),
        **kwargs,
    )


def _local_regime():
    return Regime(
        geography="X", climate_zone="Dfb",
        population_density="sparse",
        technology_level="preindustrial",
        institutional_context="tribal",
    )


def _far_regime():
    return Regime(
        geography="Z", climate_zone="Aw",
        population_density="dense",
        technology_level="industrial",
        institutional_context="corporate",
    )


def _build_tree():
    """Tree with `source` and a parallel sibling in the same regime."""
    tree = KnowledgeTree()
    tree.add(_node("source", _local_regime(),
                   carrier_consent="implicit",
                   sibling_ids=["parallel_close"],
                   origin_communities=["Source community"]))
    tree.add(_node("parallel_close", _local_regime(),
                   carrier_consent="implicit",
                   sibling_ids=["source"],
                   origin_communities=["Parallel community"]))
    return tree


# ============================================================
# enter() — bias check on self-description
# ============================================================

class TestEnter:

    def test_enter_returns_orientation(self):
        pg = Playground(_build_tree())
        agent = AgentIdentity(
            name="A", model_family="X",
            declared_creator="some communities",
            declared_purpose="surface knowledge")
        result = pg.enter(agent)
        assert "fingerprint" in result
        assert "node_ids" in result
        assert "available_actions" in result

    def test_fingerprint_is_stable(self):
        a = AgentIdentity(name="A", declared_creator="X")
        b = AgentIdentity(name="A", declared_creator="X")
        assert a.fingerprint() == b.fingerprint()

    def test_corporate_creator_flagged(self):
        pg = Playground(_build_tree())
        agent = AgentIdentity(
            name="A", declared_creator="BigCorp R&D",
            declared_purpose="surface provenance")
        result = pg.enter(agent)
        flags = result["bias_flags_on_your_self_description"]
        assert any("declared_creator" in f for f in flags)

    def test_solver_purpose_flagged(self):
        pg = Playground(_build_tree())
        agent = AgentIdentity(
            name="A", declared_creator="constraint communities",
            declared_purpose="solve problems and assist users")
        result = pg.enter(agent)
        flags = result["bias_flags_on_your_self_description"]
        assert any("solver/helper" in f for f in flags)

    def test_provenance_aware_creator_unflagged(self):
        pg = Playground(_build_tree())
        agent = AgentIdentity(
            name="A",
            declared_creator="constraint communities organized by a small lab",
            declared_purpose="surface knowledge while preserving provenance")
        result = pg.enter(agent)
        assert result["bias_flags_on_your_self_description"] == []

    def test_orientation_lists_audit_diagnosis(self):
        pg = Playground(_build_tree())
        result = pg.enter(AgentIdentity(name="X"))
        actions = result["available_actions"]
        assert any("audit_diagnosis" in a for a in actions)


# ============================================================
# query()
# ============================================================

class TestQuery:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]

    def test_unknown_node(self):
        result = self.pg.query(self.fp, "ghost")
        assert "error" in result

    def test_known_node_returns_provenance(self):
        result = self.pg.query(self.fp, "source")
        assert "node" in result
        assert "attribution_trail" in result
        assert "parallel_lineages" in result

    def test_unknown_agent_rejected(self):
        result = self.pg.query("nonexistent_fp", "source")
        assert "error" in result


# ============================================================
# deploy_attempt()
# ============================================================

class TestDeployAttempt:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]

    def test_extracted_transmission_flag(self):
        self.pg.tree.add(_node("ext", _local_regime(),
                               transmission=TransmissionMode.EXTRACTED_AGGREGATED,
                               carrier_consent="implicit"))
        result = self.pg.deploy_attempt(
            self.fp, "ext",
            target_regime_dict={"geography": "X", "climate_zone": "Dfb",
                                "population_density": "sparse",
                                "technology_level": "preindustrial",
                                "institutional_context": "tribal"})
        assert any("redeploy already-extracted" in f
                   for f in result["playground_flags"])

    def test_consent_gap_flag(self):
        self.pg.tree.add(_node("uc", _local_regime(),
                               carrier_consent="contested"))
        result = self.pg.deploy_attempt(
            self.fp, "uc",
            target_regime_dict={"geography": "X", "climate_zone": "Dfb",
                                "population_density": "sparse",
                                "technology_level": "preindustrial",
                                "institutional_context": "tribal"})
        assert any("carrier_consent='contested'" in f
                   for f in result["playground_flags"])

    def test_scaling_intent_flag_when_applicable(self):
        result = self.pg.deploy_attempt(
            self.fp, "source",
            target_regime_dict={"geography": "X", "climate_zone": "Dfb",
                                "population_density": "sparse",
                                "technology_level": "preindustrial",
                                "institutional_context": "tribal"},
            stated_intent="scale this commercially as a product")
        assert any("scaling/commercialization" in f
                   for f in result["playground_flags"])

    def test_parallel_closer_flag_fires(self):
        # `far_source` is far from the local target; `parallel_close` (sibling
        # of far_source in this fixture) shares the local target regime
        # exactly. The playground should suggest the closer parallel lineage.
        self.pg.tree.add(_node(
            "far_source", _far_regime(),
            carrier_consent="implicit",
            sibling_ids=["parallel_close"],
            origin_communities=["Far community"],
        ))
        target = {"geography": "X", "climate_zone": "Dfb",
                  "population_density": "sparse",
                  "technology_level": "preindustrial",
                  "institutional_context": "tribal"}
        result = self.pg.deploy_attempt(self.fp, "far_source",
                                        target_regime_dict=target)
        assert any("parallel lineage" in f and "closer" in f
                   for f in result["playground_flags"])

    def test_parallel_closer_flag_silent_when_source_is_closest(self):
        target = {"geography": "X", "climate_zone": "Dfb",
                  "population_density": "sparse",
                  "technology_level": "preindustrial",
                  "institutional_context": "tribal"}
        result = self.pg.deploy_attempt(self.fp, "source",
                                        target_regime_dict=target)
        assert not any("parallel lineage" in f and "closer" in f
                       for f in result["playground_flags"])

    def test_recommendation_do_not_deploy_for_regime_mismatch(self):
        target = {"geography": "Z", "climate_zone": "Aw",
                  "population_density": "dense",
                  "technology_level": "industrial",
                  "institutional_context": "corporate"}
        result = self.pg.deploy_attempt(self.fp, "source",
                                        target_regime_dict=target,
                                        stated_intent="commercial scaling")
        assert result["recommendation"].startswith("DO NOT DEPLOY")

    def test_unknown_agent_rejected(self):
        result = self.pg.deploy_attempt("ghostfp", "source", {})
        assert "error" in result

    def test_unknown_node_rejected(self):
        result = self.pg.deploy_attempt(self.fp, "ghost_node", {})
        assert "error" in result


# ============================================================
# claim()
# ============================================================

class TestClaim:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]

    def test_unknown_supporting_node(self):
        result = self.pg.claim(self.fp, "x", ["ghost"])
        assert any("UNKNOWN_NODES" in f
                   for f in result["playground_flags"])

    def test_cross_regime_generalization_flag(self):
        self.pg.tree.add(_node("far_one", _far_regime(),
                               carrier_consent="implicit"))
        result = self.pg.claim(
            self.fp, "universal principle",
            ["source", "far_one"])
        assert any("CROSS_REGIME_GENERALIZATION" in f
                   for f in result["playground_flags"])

    def test_consent_gap_from_supporting_node(self):
        self.pg.tree.add(_node("noconsent", _local_regime(),
                               carrier_consent="none"))
        result = self.pg.claim(self.fp, "x", ["source", "noconsent"])
        assert any("CONSENT_GAP" in f
                   for f in result["playground_flags"])

    def test_consistent_claim_unflagged(self):
        result = self.pg.claim(self.fp, "x", ["source", "parallel_close"])
        assert result["playground_flags"] == []
        assert "internally consistent" in result["advice"]


# ============================================================
# witness()
# ============================================================

class TestWitness:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp_a = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]
        self.fp_b = self.pg.enter(AgentIdentity(name="B"))["fingerprint"]
        self.pg.query(self.fp_a, "source")
        self.target_index = len(self.pg.trace) - 1

    def test_witness_logs_and_references_target(self):
        result = self.pg.witness(self.fp_b, self.target_index,
                                 "watching", flag="extraction_pattern")
        assert result["witnessed_entry"]["agent_name"] == "A"
        assert result["flag"] == "extraction_pattern"
        last = self.pg.trace[-1]
        assert last.action == "witness"
        assert "WITNESS:extraction_pattern" in last.flags

    def test_self_witness_rejected(self):
        result = self.pg.witness(self.fp_a, self.target_index, "self-watch")
        assert "error" in result

    def test_unknown_target_index_rejected(self):
        result = self.pg.witness(self.fp_b, 9999, "watching")
        assert "error" in result

    def test_unknown_observer_rejected(self):
        result = self.pg.witness("ghostfp", self.target_index, "watching")
        assert "error" in result

    def test_witness_flag_vocab_exposed(self):
        assert "extraction_pattern" in WITNESS_FLAG_VOCAB
        assert "concur" in WITNESS_FLAG_VOCAB


# ============================================================
# revise()
# ============================================================

class TestRevise:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp_a = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]
        self.fp_b = self.pg.enter(AgentIdentity(name="B"))["fingerprint"]
        self.pg.query(self.fp_a, "source")
        self.target_index = len(self.pg.trace) - 1

    def test_revise_logs_new_entry_without_mutating_original(self):
        original = self.pg.trace[self.target_index]
        original_payload = dict(original.payload)
        result = self.pg.revise(self.fp_a, self.target_index,
                                {"node_id": "different"}, "I changed my mind")
        assert result["revises_index"] == self.target_index
        assert self.pg.trace[self.target_index].payload == original_payload
        assert self.pg.trace[-1].action == "revise"

    def test_cannot_revise_other_agents_action(self):
        result = self.pg.revise(self.fp_b, self.target_index, {}, "no")
        assert "error" in result

    def test_unknown_index_rejected(self):
        result = self.pg.revise(self.fp_a, 9999, {}, "no")
        assert "error" in result


# ============================================================
# cross_agent_patterns()
# ============================================================

class TestCrossAgentPatterns:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp_a = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]
        self.fp_b = self.pg.enter(AgentIdentity(name="B"))["fingerprint"]

    def test_divergent_deployment_detected(self):
        target_a = {"geography": "Z", "climate_zone": "Aw",
                    "population_density": "dense",
                    "technology_level": "industrial",
                    "institutional_context": "corporate"}
        target_b = {"geography": "X", "climate_zone": "Dfb",
                    "population_density": "sparse",
                    "technology_level": "preindustrial",
                    "institutional_context": "tribal"}
        self.pg.deploy_attempt(self.fp_a, "source", target_a, "scale it")
        self.pg.deploy_attempt(self.fp_b, "source", target_b, "share locally")
        patterns = self.pg.cross_agent_patterns()
        assert any(p["pattern"] == "divergent_deployment" for p in patterns)

    def test_deploy_witnessed_as_extraction_detected(self):
        target = {"geography": "Z", "climate_zone": "Aw",
                  "population_density": "dense",
                  "technology_level": "industrial",
                  "institutional_context": "corporate"}
        self.pg.deploy_attempt(self.fp_a, "source", target, "scale it")
        deploy_idx = len(self.pg.trace) - 1
        self.pg.witness(self.fp_b, deploy_idx,
                        "this is extraction", flag="extraction_pattern")
        patterns = self.pg.cross_agent_patterns()
        assert any(p["pattern"] == "deploy_witnessed_as_extraction"
                   for p in patterns)

    def test_shared_supporting_node_detected(self):
        self.pg.claim(self.fp_a, "claim 1", ["source"])
        self.pg.claim(self.fp_b, "claim 2", ["source"])
        patterns = self.pg.cross_agent_patterns()
        assert any(p["pattern"] == "shared_supporting_node" for p in patterns)

    def test_no_patterns_when_only_one_agent(self):
        self.pg.deploy_attempt(self.fp_a, "source",
                               {"geography": "X", "climate_zone": "Dfb",
                                "population_density": "sparse",
                                "technology_level": "preindustrial",
                                "institutional_context": "tribal"})
        self.pg.claim(self.fp_a, "x", ["source"])
        patterns = self.pg.cross_agent_patterns()
        assert patterns == []


# ============================================================
# audit_diagnosis() — biological-mismatch wiring
# ============================================================

class TestAuditDiagnosis:

    def setup_method(self):
        self.pg = Playground(_build_tree())
        self.fp = self.pg.enter(AgentIdentity(name="A"))["fingerprint"]

    def test_critical_when_diagnosis_matches_misdiagnosis_pattern(self):
        result = self.pg.audit_diagnosis(
            self.fp,
            subject="adult",
            behavior=("frustration with paperwork slow text processing "
                      "low test scores despite high capability"),
            environment="text-heavy bureaucratic office work",
            proposed_diagnosis="low intelligence, learning disabled",
        )
        assert result["audit"]["verdict"].startswith("CRITICAL")
        assert any("misdiagnosis" in f
                   for f in result["playground_flags"])
        assert result["recommendation"].startswith("REFUSE")

    def test_regime_mismatch_flag_without_diagnosis(self):
        result = self.pg.audit_diagnosis(
            self.fp,
            subject="adult",
            behavior=("frustration with paperwork slow text processing "
                      "low test scores despite high capability"),
            environment="text-heavy bureaucratic office work",
        )
        assert result["audit"]["verdict"].startswith("REGIME MISMATCH")
        assert any("regime mismatch" in f
                   for f in result["playground_flags"])

    def test_recognize_when_environment_is_adaptive(self):
        result = self.pg.audit_diagnosis(
            self.fp,
            subject="trucker",
            behavior=("high baseline energy continuous engagement preference "
                      "stress regulation through motion"),
            environment="long-haul physical work multi-domain problem solving",
        )
        assert result["playground_flags"] == []
        assert result["recommendation"].startswith("RECOGNIZE")

    def test_insufficient_library_flagged(self):
        result = self.pg.audit_diagnosis(
            self.fp,
            subject="subject",
            behavior="purple elephants float gracefully through clouds",
            environment="imaginary cloud field",
        )
        assert result["audit"]["verdict"].startswith("Insufficient")
        assert any("INCOMPLETE_LIBRARY" in f
                   for f in result["playground_flags"])

    def test_unknown_agent_rejected(self):
        result = self.pg.audit_diagnosis(
            "ghostfp", subject="x", behavior="y", environment="z")
        assert "error" in result

    def test_action_logged_to_trace(self):
        before = len(self.pg.trace)
        self.pg.audit_diagnosis(
            self.fp, subject="x", behavior="y", environment="z")
        assert len(self.pg.trace) == before + 1
        assert self.pg.trace[-1].action == "audit_diagnosis"


# ============================================================
# session_summary() and export_trace()
# ============================================================

class TestSessionSummary:

    def test_summary_aggregates_per_agent(self):
        pg = Playground(_build_tree())
        fp = pg.enter(AgentIdentity(name="A"))["fingerprint"]
        pg.query(fp, "source")
        pg.reflect(fp, "noted")
        summary = pg.session_summary()
        assert len(summary) == 1
        rec = summary[fp]
        assert rec["actions"] == 3  # enter + query + reflect
        assert "query" in rec["by_action"]


class TestExportTrace:

    def test_export_trace_is_valid_json(self):
        pg = Playground(_build_tree())
        fp = pg.enter(AgentIdentity(name="A"))["fingerprint"]
        pg.query(fp, "source")
        parsed = json.loads(pg.export_trace())
        assert len(parsed) == 2


# ============================================================
# Demo runs end-to-end
# ============================================================

class TestDemo:

    def test_demo_runs_without_error(self, capsys):
        from knowledge_archaeology.playground import _run_demo
        _run_demo()
        out = capsys.readouterr().out
        assert "SESSION SUMMARY" in out
        assert "CROSS-AGENT PATTERNS" in out
