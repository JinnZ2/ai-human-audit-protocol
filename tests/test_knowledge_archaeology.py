"""Unit tests for knowledge_archaeology/knowledge_archaeology.py.

The module is constraint-provenance for knowledge: regime, validation
depth, transmission mode, lineage, attribution. These tests verify
the contract per area and the cross-area integration via deploy_check.
"""

import json
from pathlib import Path

import pytest

from knowledge_archaeology.knowledge_archaeology import (
    KnowledgeNode,
    KnowledgeTree,
    Regime,
    TransmissionMode,
    ValidationDepth,
    applicability,
    load_tree_from_directory,
    load_tree_from_json,
    node_from_dict,
    regime_distance,
    regime_from_dict,
)


_NODES_DIR = (Path(__file__).parent.parent
              / "knowledge_archaeology" / "nodes")


def _node(node_id="n1", regime=None, transmission=None,
          validation=None, **kwargs):
    return KnowledgeNode(
        id=node_id,
        name=kwargs.pop("name", node_id),
        description=kwargs.pop("description", "test"),
        regime=regime or Regime(geography="X"),
        transmission=transmission or TransmissionMode.ORAL_GENERATIONAL,
        validation=validation or ValidationDepth.MULTI_CYCLE,
        **kwargs,
    )


# ============================================================
# Regime
# ============================================================

class TestRegime:
    def test_default_construction(self):
        r = Regime()
        assert r.geography == ""
        assert r.elevation_m is None

    def test_fingerprint_strips_empty(self):
        r = Regime(
            geography="X",
            elevation_m=None,
            resource_scarcity=[],
            avg_temp_C=10.0,
        )
        fp = r.fingerprint()
        assert "geography" in fp
        assert "avg_temp_C" in fp
        assert "elevation_m" not in fp        # None stripped
        assert "resource_scarcity" not in fp  # [] stripped


# ============================================================
# regime_distance
# ============================================================

class TestRegimeDistance:
    def test_identical_regime_distance_zero(self):
        r = Regime(
            geography="X", climate_zone="Dfb",
            avg_temp_C=10.0, population_density="dense",
        )
        assert regime_distance(r, r) == 0.0

    def test_different_geography_increases_distance(self):
        a = Regime(geography="X", climate_zone="Dfb")
        b = Regime(geography="Y", climate_zone="Dfb")
        assert regime_distance(a, b) > 0

    def test_numeric_features_scale_appropriately(self):
        a = Regime(avg_temp_C=10.0)
        close = Regime(avg_temp_C=12.0)   # +2C, well within scale 15
        far = Regime(avg_temp_C=40.0)     # +30C, exceeds scale
        assert regime_distance(a, close) < regime_distance(a, far)

    def test_resource_scarcity_jaccard(self):
        a = Regime(resource_scarcity=["water", "fuel"])
        b = Regime(resource_scarcity=["water", "fuel"])
        c = Regime(resource_scarcity=["chips"])
        assert regime_distance(a, b) < regime_distance(a, c)

    def test_empty_regimes_return_zero(self):
        # no comparable features => default 0/1 = 0
        assert regime_distance(Regime(), Regime()) == 0.0


# ============================================================
# applicability
# ============================================================

class TestApplicability:
    def test_applicable_when_distance_low(self):
        r = Regime(geography="X")
        node = _node(regime=r,
                     validation=ValidationDepth.DEEP_GENERATIONAL)
        result = applicability(node, r, threshold=0.5)
        assert result["verdict"] == "applicable"

    def test_review_required_when_distance_moderate(self):
        a = Regime(geography="X", climate_zone="Dfb",
                   population_density="dense")
        b = Regime(geography="Y", climate_zone="BSh",
                   population_density="dense")  # 2 of 3 differ
        node = _node(regime=a,
                     validation=ValidationDepth.DEEP_GENERATIONAL)
        result = applicability(node, b, threshold=0.5)
        assert result["verdict"] in {"review_required", "regime_mismatch"}

    def test_regime_mismatch_when_distance_high(self):
        a = Regime(geography="X", climate_zone="Dfb",
                   avg_temp_C=4.0, population_density="sparse",
                   technology_level="preindustrial",
                   institutional_context="tribal")
        b = Regime(geography="Y", climate_zone="BSh",
                   avg_temp_C=30.0, population_density="dense",
                   technology_level="industrial",
                   institutional_context="corporate")
        node = _node(regime=a,
                     validation=ValidationDepth.DEEP_GENERATIONAL)
        result = applicability(node, b, threshold=0.5)
        assert result["verdict"] == "regime_mismatch"

    def test_explicit_failure_condition_overrides_to_mismatch(self):
        # even with low regime distance, an explicit fails_under match
        # overrides verdict
        r = Regime(geography="post-grid", population_density="sparse")
        node = _node(regime=r,
                     fails_under=["post-grid"])
        result = applicability(node, r, threshold=0.5)
        assert result["verdict"] == "regime_mismatch"
        assert any("FAIL" in f for f in result["flags"])

    def test_shallow_validation_flagged(self):
        r = Regime(geography="X")
        node = _node(regime=r, validation=ValidationDepth.SINGLE_CYCLE)
        result = applicability(node, r)
        assert any("WARN" in f for f in result["flags"])

    def test_contested_consent_flagged(self):
        node = _node(carrier_consent="contested")
        result = applicability(node, node.regime)
        assert any("ETHICS" in f for f in result["flags"])

    def test_no_consent_flagged(self):
        node = _node(carrier_consent="none")
        result = applicability(node, node.regime)
        assert any("ETHICS" in f for f in result["flags"])

    def test_implicit_consent_not_flagged_for_ethics(self):
        node = _node(carrier_consent="implicit")
        result = applicability(node, node.regime)
        assert not any("ETHICS" in f for f in result["flags"])

    def test_assumptions_returned(self):
        node = _node(assumptions=["A", "B"])
        result = applicability(node, node.regime)
        assert result["assumptions_to_verify"] == ["A", "B"]

    def test_extraction_risks_returned(self):
        node = _node(extraction_risks=["risk_a"])
        result = applicability(node, node.regime)
        assert result["extraction_risks_if_misapplied"] == ["risk_a"]


# ============================================================
# KnowledgeTree
# ============================================================

class TestKnowledgeTree:
    def test_add_stores_node(self):
        tree = KnowledgeTree()
        n = _node()
        tree.add(n)
        assert "n1" in tree.nodes

    def test_sibling_links_become_bidirectional(self):
        tree = KnowledgeTree()
        a = _node("a")
        b = _node("b", sibling_ids=["a"])
        tree.add(a)
        tree.add(b)
        # both directions should now hold
        assert "b" in tree.nodes["a"].sibling_ids
        assert "a" in tree.nodes["b"].sibling_ids

    def test_parent_links_create_derived_back_link(self):
        tree = KnowledgeTree()
        parent = _node("parent")
        child = _node("child", parent_ids=["parent"])
        tree.add(parent)
        tree.add(child)
        assert "child" in tree.nodes["parent"].derived_ids

    def test_ancestors_walks_graph(self):
        tree = KnowledgeTree()
        tree.add(_node("a"))
        tree.add(_node("b", parent_ids=["a"]))
        tree.add(_node("c", parent_ids=["b"]))
        assert tree.ancestors("c") == {"a", "b"}

    def test_ancestors_handles_diamond(self):
        # a → b, a → c, both b and c point at d
        tree = KnowledgeTree()
        tree.add(_node("a"))
        tree.add(_node("b", parent_ids=["a"]))
        tree.add(_node("c", parent_ids=["a"]))
        tree.add(_node("d", parent_ids=["b", "c"]))
        assert tree.ancestors("d") == {"a", "b", "c"}

    def test_ancestors_excludes_self(self):
        tree = KnowledgeTree()
        tree.add(_node("a"))
        assert "a" not in tree.ancestors("a")

    def test_ancestors_depth_limit(self):
        tree = KnowledgeTree()
        tree.add(_node("a"))
        tree.add(_node("b", parent_ids=["a"]))
        tree.add(_node("c", parent_ids=["b"]))
        # depth=1 from c only walks one level back → just b
        assert tree.ancestors("c", depth=1) == {"b"}

    def test_parallel_lineages_groups_by_community(self):
        tree = KnowledgeTree()
        a = _node("a", origin_communities=["A_comm"])
        b = _node("b", origin_communities=["B_comm"], sibling_ids=["a"])
        tree.add(a)
        tree.add(b)
        # from a's perspective, b is the sibling, originating in B_comm
        result = tree.parallel_lineages("a")
        assert "B_comm" in result
        assert "b" in result["B_comm"]

    def test_attribution_trail_includes_self_and_ancestors(self):
        tree = KnowledgeTree()
        tree.add(_node("a", origin_communities=["A"]))
        tree.add(_node("b", origin_communities=["B"], parent_ids=["a"]))
        trail = tree.attribution_trail("b")
        nodes_in_trail = {entry["node"] for entry in trail}
        assert nodes_in_trail == {"a", "b"}

    def test_deploy_check_returns_three_blocks(self):
        tree = KnowledgeTree()
        r = Regime(geography="X")
        tree.add(_node("a", regime=r))
        result = tree.deploy_check("a", Regime(geography="Y"))
        assert "applicability" in result
        assert "attribution_trail" in result
        assert "parallel_lineages" in result

    def test_deploy_check_unknown_node_returns_error(self):
        tree = KnowledgeTree()
        result = tree.deploy_check("missing", Regime())
        assert "error" in result

    def test_export_json_serializes(self):
        tree = KnowledgeTree()
        tree.add(_node("a"))
        s = tree.export_json()
        # round-trip
        data = json.loads(s)
        assert "a" in data


# ============================================================
# JSON loaders
# ============================================================

class TestJsonLoaders:
    def test_regime_from_dict(self):
        r = regime_from_dict({"geography": "X", "avg_temp_C": 10.0,
                              "extra_unknown_field": "ignored"})
        assert r.geography == "X"
        assert r.avg_temp_C == 10.0

    def test_node_from_dict_int_validation(self):
        d = {
            "id": "n", "name": "n", "description": "d",
            "regime": {"geography": "X"},
            "transmission": "oral_generational",
            "validation": 3,
        }
        n = node_from_dict(d)
        assert n.validation == ValidationDepth.GENERATIONAL

    def test_node_from_dict_string_validation(self):
        d = {
            "id": "n", "name": "n", "description": "d",
            "regime": {"geography": "X"},
            "transmission": "oral_generational",
            "validation": "DEEP_GENERATIONAL",
        }
        n = node_from_dict(d)
        assert n.validation == ValidationDepth.DEEP_GENERATIONAL

    def test_load_tree_from_directory(self):
        # the three real example node files should load and link
        tree = load_tree_from_directory(str(_NODES_DIR))
        assert "anishinaabe_gravity_filtration_v1" in tree.nodes
        assert "punjab_baoli_filtration_v1" in tree.nodes
        assert "commercial_filter_cartridge_v3" in tree.nodes

    def test_loaded_tree_has_bidirectional_sibling_link(self):
        tree = load_tree_from_directory(str(_NODES_DIR))
        a = tree.nodes["anishinaabe_gravity_filtration_v1"]
        b = tree.nodes["punjab_baoli_filtration_v1"]
        # the file declares anishinaabe → punjab as sibling; reconcile
        # should make the reverse link too
        assert "punjab_baoli_filtration_v1" in a.sibling_ids
        assert "anishinaabe_gravity_filtration_v1" in b.sibling_ids

    def test_loaded_tree_has_derived_back_link(self):
        # commercial_filter_cartridge_v3 lists anishinaabe + punjab as parents;
        # both parents should now have commercial in derived_ids
        tree = load_tree_from_directory(str(_NODES_DIR))
        a = tree.nodes["anishinaabe_gravity_filtration_v1"]
        p = tree.nodes["punjab_baoli_filtration_v1"]
        assert "commercial_filter_cartridge_v3" in a.derived_ids
        assert "commercial_filter_cartridge_v3" in p.derived_ids


# ============================================================
# Example demo: end-to-end semantics
# ============================================================

class TestExampleDemo:
    def test_demo_runs_without_error(self):
        from knowledge_archaeology.examples.example_deploy_check import main
        # captures no return; should not raise
        main()

    def test_commercial_attribution_trail_includes_traditional_sources(self):
        # this is the load-bearing assertion of the extraction-audit demo:
        # the commercial cartridge's attribution must walk back to the
        # traditional lineages that were absorbed
        tree = load_tree_from_directory(str(_NODES_DIR))
        trail = tree.attribution_trail("commercial_filter_cartridge_v3")
        nodes_in_trail = {entry["node"] for entry in trail}
        assert "anishinaabe_gravity_filtration_v1" in nodes_in_trail
        assert "punjab_baoli_filtration_v1" in nodes_in_trail

    def test_commercial_post_grid_deployment_flagged(self):
        # the post-grid deployment must surface as regime_mismatch
        tree = load_tree_from_directory(str(_NODES_DIR))
        target_postgrid = Regime(
            geography="post-grid rural",
            climate_zone="Dfb",
            population_density="sparse",
            technology_level="preindustrial",
            institutional_context="tribal",
            resource_scarcity=["fuel", "supply_chain"],
        )
        result = tree.deploy_check("commercial_filter_cartridge_v3",
                                    target_postgrid)
        assert result["applicability"]["verdict"] == "regime_mismatch"

    def test_boreal_to_punjab_finds_parallel_lineage(self):
        # the parallel-lineage demo: applying the boreal filter to a
        # Punjab regime should surface punjab_baoli as a sibling that
        # already fits
        tree = load_tree_from_directory(str(_NODES_DIR))
        target_punjab = Regime(
            geography="Punjab plain", climate_zone="BSh",
            avg_temp_C=24.0, precip_mm_per_yr=600,
            resource_scarcity=["fuel", "potable_groundwater"],
            population_density="dense",
            technology_level="preindustrial",
            institutional_context="agrarian",
        )
        result = tree.deploy_check("anishinaabe_gravity_filtration_v1",
                                    target_punjab)
        # parallel_lineages keys are community names from the sibling
        # node's origin_communities
        assert any("Punjabi" in community
                   for community in result["parallel_lineages"])
