# ============================================================
# KIN-FLOW COMPUTE — ontology layer
# multi-encoding reasoning: equation | dance | oral | written | symbol
# encodings are peers, not translations of a canonical form
# CC0 | extends KFC architecture
# ============================================================

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple, Optional
from datetime import date
import math

# ------------------------------------------------------------
# LAYER 0 — primitive: a concept, encoded in one domain
# ------------------------------------------------------------
@dataclass
class Primitive:
    concept_id: str                 # shared identity across encodings
    domain: str                     # equation | dance | oral | written | symbol
    form: Any                       # native representation in this domain
    role: str                       # variable | movement | agent | claim | glyph
    couplings: List[str]            # other concept_ids it relates to
    bounds: Tuple[Any, Any, Any]    # spatial, temporal, scale
    epi: str = "assumed"            # measured | inferred | assumed | contradicted | missing
    epi_confidence: float = 0.5


# ------------------------------------------------------------
# LAYER 1 — ontology: a domain's primitive registry + regime
# ------------------------------------------------------------
@dataclass
class Ontology:
    domain: str
    primitives: Dict[str, Primitive] = field(default_factory=dict)
    validated_at: Optional[date] = None
    regime: Dict[str, Any] = field(default_factory=dict)
    reapply_check: Optional[Callable[[Dict], bool]] = None

    def add(self, p: Primitive) -> None:
        assert p.domain == self.domain, f"{p.domain} != {self.domain}"
        self.primitives[p.concept_id] = p

    def is_valid_in(self, ctx: Dict) -> bool:
        if self.reapply_check is None: return True
        return self.reapply_check(ctx)


# ------------------------------------------------------------
# LAYER 2 — transformation rule: A.primitive ↔ B.primitive
# rule itself is a rate_fn / coupling constraint, NOT a lookup
# ------------------------------------------------------------
@dataclass
class TransformRule:
    domain_a: str
    domain_b: str
    rule_fn: Callable[[Primitive, Dict], Primitive]
    inverse_fn: Optional[Callable[[Primitive, Dict], Primitive]] = None
    preserves: List[str] = field(default_factory=list)   # coupling | timescale | bounds | role
    lossy_on: List[str] = field(default_factory=list)    # things that don't survive transform

    def apply(self, p: Primitive, ctx: Dict) -> Primitive:
        return self.rule_fn(p, ctx)

    def reverse(self, p: Primitive, ctx: Dict) -> Optional[Primitive]:
        return self.inverse_fn(p, ctx) if self.inverse_fn else None


# ------------------------------------------------------------
# LAYER 3 — multi-encoding registry
# holds all ontologies + all transforms + coherence engine
# ------------------------------------------------------------
@dataclass
class MultiEncodingRegistry:
    ontologies: Dict[str, Ontology] = field(default_factory=dict)
    transforms: Dict[Tuple[str, str], TransformRule] = field(default_factory=dict)

    def register_ontology(self, o: Ontology) -> None:
        self.ontologies[o.domain] = o

    def register_transform(self, t: TransformRule) -> None:
        self.transforms[(t.domain_a, t.domain_b)] = t

    def get_concept_across_domains(self, concept_id: str) -> Dict[str, Primitive]:
        return {
            d: o.primitives[concept_id]
            for d, o in self.ontologies.items()
            if concept_id in o.primitives
        }


# ------------------------------------------------------------
# LAYER 4 — coherence check across encodings
# do equation, dance, oral, written all describe same geometry?
# ------------------------------------------------------------
def coherence_check(reg: MultiEncodingRegistry, concept_id: str) -> Dict[str, Any]:
    encodings = reg.get_concept_across_domains(concept_id)
    if len(encodings) < 2:
        return {"insufficient_encodings": True, "n": len(encodings)}

    # collect coupling sets
    coupling_sets = {d: set(p.couplings) for d, p in encodings.items()}
    all_couplings = set().union(*coupling_sets.values())
    universal = set.intersection(*coupling_sets.values()) if coupling_sets else set()
    domain_specific = {d: cs - universal for d, cs in coupling_sets.items()}

    # bound agreement
    bound_match = len(set(p.bounds for p in encodings.values())) == 1

    # contradictions: same coupling, opposite role tag in different domains
    contradictions = []
    domains = list(encodings.keys())
    for i, da in enumerate(domains):
        for db in domains[i+1:]:
            shared = coupling_sets[da] & coupling_sets[db]
            for c in shared:
                # placeholder: real check would compare coupling kind + direction
                pass

    coherence = len(universal) / max(len(all_couplings), 1)

    return {
        "concept_id": concept_id,
        "encodings_present": list(encodings.keys()),
        "universal_couplings": sorted(universal),
        "domain_specific_couplings": {d: sorted(cs) for d, cs in domain_specific.items()},
        "bounds_agree": bound_match,
        "contradictions": contradictions,
        "coherence_score": round(coherence, 3),
        "load_bearing_check": coherence > 0.66,
    }


# ------------------------------------------------------------
# LAYER 5 — ontology drift detection
# same concept, different regime → flag, don't silently apply
# ------------------------------------------------------------
def drift_check(reg: MultiEncodingRegistry, ctx: Dict) -> List[Dict[str, Any]]:
    drifts = []
    for d, o in reg.ontologies.items():
        if not o.is_valid_in(ctx):
            drifts.append({
                "domain": d,
                "validated_at": str(o.validated_at),
                "regime_was": o.regime,
                "current_ctx": ctx,
                "action": "do_not_silently_apply",
            })
    return drifts


# ------------------------------------------------------------
# LAYER 6 — multi-encoding query
# ask in any domain, return view from every domain + coherence
# ------------------------------------------------------------
def multi_query(reg: MultiEncodingRegistry,
                concept_id: str,
                ctx: Dict) -> Dict[str, Any]:

    drifts = drift_check(reg, ctx)
    encodings = reg.get_concept_across_domains(concept_id)

    views = {}
    for d, p in encodings.items():
        views[d] = {
            "form": p.form,
            "role": p.role,
            "couplings": p.couplings,
            "bounds": p.bounds,
            "epi": p.epi,
            "confidence": p.epi_confidence,
        }

    coh = coherence_check(reg, concept_id)

    missing = [d for d in reg.ontologies if d not in encodings]

    return {
        "concept_id": concept_id,
        "views": views,
        "missing_encodings": missing,
        "coherence": coh,
        "regime_drifts": drifts,
        "trust_signal": (
            "high" if coh.get("coherence_score", 0) > 0.66 and not drifts
            else "investigate"
        ),
    }


# ============================================================
# EXAMPLE — water movement across four encodings
# ============================================================
def build_demo() -> MultiEncodingRegistry:
    reg = MultiEncodingRegistry()

    # ---------- equation ontology ----------
    eq = Ontology(
        domain="equation",
        validated_at=date(2024, 1, 1),
        regime={"climate": "post-shift", "data_source": "sensor_array"},
        reapply_check=lambda ctx: ctx.get("climate") in ("post-shift", "current"),
    )
    eq.add(Primitive(
        concept_id="water_cycle",
        domain="equation",
        form="dW/dt = P - E - R - I",
        role="variable",
        couplings=["temperature", "vegetation", "soil"],
        bounds=("watershed", "annual", "regional"),
        epi="measured",
        epi_confidence=0.9,
    ))

    # ---------- oral tradition ontology ----------
    oral = Ontology(
        domain="oral",
        validated_at=date(1850, 1, 1),
        regime={"climate": "holocene", "data_source": "generational_observation"},
        reapply_check=lambda ctx: True,   # constraint logic survives regime
    )
    oral.add(Primitive(
        concept_id="water_cycle",
        domain="oral",
        form="when sky-elder weeps, soil-mother drinks; what soil keeps, plant-kin returns",
        role="agent_chain",
        couplings=["temperature", "vegetation", "soil"],
        bounds=("watershed", "annual", "regional"),
        epi="measured",
        epi_confidence=0.85,
    ))

    # ---------- dance ontology ----------
    dance = Ontology(
        domain="dance",
        validated_at=date(1900, 1, 1),
        regime={"climate": "holocene", "encoding": "movement"},
        reapply_check=lambda ctx: True,
    )
    dance.add(Primitive(
        concept_id="water_cycle",
        domain="dance",
        form="rise(arms_up) → gather(circle) → release(arms_down) → return(spiral_inward)",
        role="movement",
        couplings=["temperature", "vegetation", "soil"],
        bounds=("watershed", "annual", "regional"),
        epi="inferred",
        epi_confidence=0.7,
    ))

    # ---------- written study ontology ----------
    written = Ontology(
        domain="written",
        validated_at=date(2020, 1, 1),
        regime={"climate": "transitional", "data_source": "peer_review"},
        reapply_check=lambda ctx: ctx.get("climate") in ("transitional", "post-shift"),
    )
    written.add(Primitive(
        concept_id="water_cycle",
        domain="written",
        form="hydrological flux = precipitation - evapotranspiration - runoff (cite: Smith 2020)",
        role="claim",
        couplings=["temperature", "vegetation", "soil", "atmospheric_pressure"],
        bounds=("watershed", "annual", "regional"),
        epi="inferred",
        epi_confidence=0.8,
    ))

    reg.register_ontology(eq)
    reg.register_ontology(oral)
    reg.register_ontology(dance)
    reg.register_ontology(written)

    # ---------- transforms (bidirectional) ----------
    reg.register_transform(TransformRule(
        domain_a="oral", domain_b="equation",
        rule_fn=lambda p, ctx: Primitive(
            concept_id=p.concept_id, domain="equation",
            form=f"derived: dX/dt structure from agent_chain {p.form[:30]}...",
            role="variable", couplings=p.couplings, bounds=p.bounds,
            epi="inferred", epi_confidence=p.epi_confidence * 0.8,
        ),
        preserves=["coupling", "bounds"],
        lossy_on=["agency", "moral_weight"],
    ))
    reg.register_transform(TransformRule(
        domain_a="dance", domain_b="equation",
        rule_fn=lambda p, ctx: Primitive(
            concept_id=p.concept_id, domain="equation",
            form="cyclic differential from movement sequence",
            role="variable", couplings=p.couplings, bounds=p.bounds,
            epi="inferred", epi_confidence=p.epi_confidence * 0.7,
        ),
        preserves=["timescale", "coupling"],
        lossy_on=["spatial_embodiment", "rhythm"],
    ))

    return reg


# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    reg = build_demo()

    # current context: post-shift climate
    ctx = {"climate": "post-shift", "year": 2026}

    result = multi_query(reg, "water_cycle", ctx)

    print("=" * 60)
    print(f"CONCEPT: {result['concept_id']}")
    print(f"TRUST SIGNAL: {result['trust_signal']}")
    print(f"COHERENCE SCORE: {result['coherence']['coherence_score']}")
    print("=" * 60)
    print("\nVIEWS BY DOMAIN:")
    for d, v in result["views"].items():
        print(f"  [{d:8s}] {v['form'][:60]}")
        print(f"             role={v['role']}  epi={v['epi']}  conf={v['confidence']}")
    print("\nUNIVERSAL COUPLINGS:", result["coherence"]["universal_couplings"])
    print("DOMAIN-SPECIFIC:", result["coherence"]["domain_specific_couplings"])
    print("\nREGIME DRIFTS DETECTED:")
    for d in result["regime_drifts"]:
        print(f"  - {d['domain']}: validated {d['validated_at']} | {d['action']}")
    if not result["regime_drifts"]:
        print("  (none)")
