"""Unit tests for consortium/ontology_layer.py.

The ontology layer is multi-encoding reasoning: equation, dance, oral,
written, symbol all live as peer encodings of the same concept. These
tests cover Primitive/Ontology/TransformRule/MultiEncodingRegistry,
coherence_check, drift_check, and multi_query.
"""

from datetime import date

import pytest

from consortium.ontology_layer import (
    Primitive,
    Ontology,
    TransformRule,
    MultiEncodingRegistry,
    coherence_check,
    drift_check,
    multi_query,
    build_demo,
)


def _prim(concept_id="c", domain="d", couplings=None, bounds=None,
          epi="measured", confidence=0.8, role="claim"):
    return Primitive(
        concept_id=concept_id,
        domain=domain,
        form="form_text",
        role=role,
        couplings=couplings or [],
        bounds=bounds or ("S", "T", "Z"),
        epi=epi,
        epi_confidence=confidence,
    )


# ------------------------------------------------------------
# Primitive
# ------------------------------------------------------------

class TestPrimitive:
    def test_construction(self):
        p = _prim(concept_id="x")
        assert p.concept_id == "x"

    def test_default_epi_assumed(self):
        p = Primitive(
            concept_id="x", domain="d", form="f", role="r",
            couplings=[], bounds=("a", "b", "c"),
        )
        assert p.epi == "assumed"

    def test_default_confidence(self):
        p = Primitive(
            concept_id="x", domain="d", form="f", role="r",
            couplings=[], bounds=("a", "b", "c"),
        )
        assert p.epi_confidence == 0.5


# ------------------------------------------------------------
# Ontology
# ------------------------------------------------------------

class TestOntology:
    def test_add_primitive(self):
        o = Ontology(domain="equation")
        p = _prim(domain="equation")
        o.add(p)
        assert "c" in o.primitives

    def test_add_rejects_domain_mismatch(self):
        o = Ontology(domain="equation")
        p = _prim(domain="oral")
        with pytest.raises(AssertionError):
            o.add(p)

    def test_is_valid_in_default_true(self):
        # no reapply_check → always valid
        o = Ontology(domain="d")
        assert o.is_valid_in({})

    def test_is_valid_in_uses_check(self):
        o = Ontology(
            domain="d",
            reapply_check=lambda ctx: ctx.get("regime") == "current",
        )
        assert o.is_valid_in({"regime": "current"})
        assert not o.is_valid_in({"regime": "stale"})


# ------------------------------------------------------------
# TransformRule
# ------------------------------------------------------------

class TestTransformRule:
    def test_apply_runs_rule_fn(self):
        rule = TransformRule(
            domain_a="a", domain_b="b",
            rule_fn=lambda p, ctx: _prim(concept_id=p.concept_id, domain="b"),
        )
        p = _prim(concept_id="x", domain="a")
        result = rule.apply(p, {})
        assert result.domain == "b"

    def test_reverse_returns_none_without_inverse(self):
        rule = TransformRule(
            domain_a="a", domain_b="b",
            rule_fn=lambda p, ctx: p,
        )
        p = _prim(domain="a")
        assert rule.reverse(p, {}) is None

    def test_reverse_uses_inverse_fn(self):
        rule = TransformRule(
            domain_a="a", domain_b="b",
            rule_fn=lambda p, ctx: p,
            inverse_fn=lambda p, ctx: _prim(concept_id=p.concept_id, domain="a"),
        )
        p = _prim(domain="b")
        result = rule.reverse(p, {})
        assert result is not None
        assert result.domain == "a"

    def test_preserves_and_lossy_lists_default_empty(self):
        rule = TransformRule(
            domain_a="a", domain_b="b",
            rule_fn=lambda p, ctx: p,
        )
        assert rule.preserves == []
        assert rule.lossy_on == []


# ------------------------------------------------------------
# MultiEncodingRegistry
# ------------------------------------------------------------

class TestMultiEncodingRegistry:
    def test_register_ontology(self):
        reg = MultiEncodingRegistry()
        reg.register_ontology(Ontology(domain="x"))
        assert "x" in reg.ontologies

    def test_register_transform(self):
        reg = MultiEncodingRegistry()
        rule = TransformRule(
            domain_a="a", domain_b="b",
            rule_fn=lambda p, ctx: p,
        )
        reg.register_transform(rule)
        assert ("a", "b") in reg.transforms

    def test_get_concept_across_domains(self):
        reg = MultiEncodingRegistry()
        o1 = Ontology(domain="equation")
        o1.add(_prim(concept_id="water", domain="equation"))
        o2 = Ontology(domain="oral")
        o2.add(_prim(concept_id="water", domain="oral"))
        o3 = Ontology(domain="dance")
        # water not in dance ontology
        reg.register_ontology(o1)
        reg.register_ontology(o2)
        reg.register_ontology(o3)
        result = reg.get_concept_across_domains("water")
        assert set(result.keys()) == {"equation", "oral"}


# ------------------------------------------------------------
# coherence_check
# ------------------------------------------------------------

class TestCoherenceCheck:
    def _build_reg(self, primitives_per_domain):
        reg = MultiEncodingRegistry()
        for domain, prims in primitives_per_domain.items():
            o = Ontology(domain=domain)
            for p in prims:
                o.add(p)
            reg.register_ontology(o)
        return reg

    def test_insufficient_encodings_flagged(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation")],
        })
        result = coherence_check(reg, "x")
        assert result.get("insufficient_encodings") is True

    def test_universal_couplings_intersection(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                couplings=["a", "b", "c"])],
            "oral":     [_prim(concept_id="x", domain="oral",
                                couplings=["a", "b"])],
        })
        result = coherence_check(reg, "x")
        assert set(result["universal_couplings"]) == {"a", "b"}

    def test_domain_specific_couplings(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                couplings=["a", "b"])],
            "oral":     [_prim(concept_id="x", domain="oral",
                                couplings=["a", "z"])],
        })
        result = coherence_check(reg, "x")
        assert "b" in result["domain_specific_couplings"]["equation"]
        assert "z" in result["domain_specific_couplings"]["oral"]

    def test_bounds_agreement(self):
        same_bounds = ("X", "Y", "Z")
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                bounds=same_bounds)],
            "oral":     [_prim(concept_id="x", domain="oral",
                                bounds=same_bounds)],
        })
        result = coherence_check(reg, "x")
        assert result["bounds_agree"] is True

    def test_bounds_disagreement(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                bounds=("X", "Y", "Z"))],
            "oral":     [_prim(concept_id="x", domain="oral",
                                bounds=("A", "B", "C"))],
        })
        result = coherence_check(reg, "x")
        assert result["bounds_agree"] is False

    def test_coherence_score_full_agreement(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                couplings=["a"])],
            "oral":     [_prim(concept_id="x", domain="oral",
                                couplings=["a"])],
        })
        result = coherence_check(reg, "x")
        assert result["coherence_score"] == 1.0
        assert result["load_bearing_check"] is True

    def test_coherence_score_no_overlap(self):
        reg = self._build_reg({
            "equation": [_prim(concept_id="x", domain="equation",
                                couplings=["a"])],
            "oral":     [_prim(concept_id="x", domain="oral",
                                couplings=["b"])],
        })
        result = coherence_check(reg, "x")
        assert result["coherence_score"] == 0.0
        assert result["load_bearing_check"] is False


# ------------------------------------------------------------
# drift_check
# ------------------------------------------------------------

class TestDriftCheck:
    def test_no_drift_when_all_valid(self):
        reg = MultiEncodingRegistry()
        reg.register_ontology(Ontology(
            domain="x",
            reapply_check=lambda ctx: True,
        ))
        assert drift_check(reg, {}) == []

    def test_drift_detected_for_invalid_ontology(self):
        reg = MultiEncodingRegistry()
        reg.register_ontology(Ontology(
            domain="x",
            validated_at=date(1850, 1, 1),
            regime={"climate": "holocene"},
            reapply_check=lambda ctx: ctx.get("climate") == "holocene",
        ))
        drifts = drift_check(reg, {"climate": "post-shift"})
        assert len(drifts) == 1
        assert drifts[0]["domain"] == "x"
        assert drifts[0]["action"] == "do_not_silently_apply"


# ------------------------------------------------------------
# multi_query
# ------------------------------------------------------------

class TestMultiQuery:
    def test_returns_views_per_domain(self):
        reg = MultiEncodingRegistry()
        for d in ("equation", "oral"):
            o = Ontology(domain=d)
            o.add(_prim(concept_id="x", domain=d, couplings=["a"]))
            reg.register_ontology(o)
        result = multi_query(reg, "x", {})
        assert set(result["views"].keys()) == {"equation", "oral"}

    def test_missing_encodings_listed(self):
        reg = MultiEncodingRegistry()
        eq = Ontology(domain="equation")
        eq.add(_prim(concept_id="x", domain="equation"))
        oral = Ontology(domain="oral")
        # x not in oral
        reg.register_ontology(eq)
        reg.register_ontology(oral)
        result = multi_query(reg, "x", {})
        assert "oral" in result["missing_encodings"]

    def test_trust_signal_high_when_coherent_and_no_drift(self):
        reg = MultiEncodingRegistry()
        for d in ("equation", "oral"):
            o = Ontology(domain=d, reapply_check=lambda ctx: True)
            o.add(_prim(concept_id="x", domain=d,
                        couplings=["a", "b", "c"]))
            reg.register_ontology(o)
        result = multi_query(reg, "x", {})
        assert result["trust_signal"] == "high"

    def test_trust_signal_investigate_when_low_coherence(self):
        reg = MultiEncodingRegistry()
        eq = Ontology(domain="equation", reapply_check=lambda ctx: True)
        eq.add(_prim(concept_id="x", domain="equation", couplings=["a"]))
        oral = Ontology(domain="oral", reapply_check=lambda ctx: True)
        oral.add(_prim(concept_id="x", domain="oral", couplings=["b"]))
        reg.register_ontology(eq)
        reg.register_ontology(oral)
        result = multi_query(reg, "x", {})
        # zero coherence score → investigate
        assert result["trust_signal"] == "investigate"

    def test_trust_signal_investigate_when_drift(self):
        reg = MultiEncodingRegistry()
        for d in ("equation", "oral"):
            o = Ontology(
                domain=d,
                reapply_check=lambda ctx: ctx.get("ok", False),
            )
            o.add(_prim(concept_id="x", domain=d, couplings=["a"]))
            reg.register_ontology(o)
        # coherence is high but drift is also high → investigate
        result = multi_query(reg, "x", {"ok": False})
        assert result["regime_drifts"]
        assert result["trust_signal"] == "investigate"


# ------------------------------------------------------------
# build_demo smoke test
# ------------------------------------------------------------

class TestBuildDemo:
    def test_demo_constructs(self):
        reg = build_demo()
        assert {"equation", "oral", "dance", "written"} <= set(reg.ontologies.keys())

    def test_demo_water_cycle_present_in_all_four(self):
        reg = build_demo()
        result = reg.get_concept_across_domains("water_cycle")
        assert set(result.keys()) >= {"equation", "oral", "dance", "written"}

    def test_demo_runs_multi_query(self):
        reg = build_demo()
        result = multi_query(reg, "water_cycle",
                             {"climate": "post-shift", "year": 2026})
        assert result["concept_id"] == "water_cycle"
        assert "views" in result
