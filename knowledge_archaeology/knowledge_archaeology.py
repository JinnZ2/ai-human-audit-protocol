"""
knowledge_archaeology.py

Constraint provenance for knowledge.

Every piece of knowledge emerged under specific conditions:

- geographic substrate (climate, soil, water, magnetic latitude)
- forcing functions (resource scarcity, population density, technology level)
- generational depth (how many cycles of trial/error tested it)
- transmission mode (oral, written, embodied, observational)
- validation history (what failures pruned the tree)

When that knowledge moves -- into a person, a model, a tool, a repo --
the provenance usually doesn't move with it. The capability persists;
the conditions of its validity become invisible.

This module makes constraint provenance a first-class attribute.
Anything reading the knowledge can check whether the current environment
matches the regime where the knowledge was validated. Mismatch -> explicit
flag, not silent failure.

CC0. No external dependencies.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set
from enum import Enum
import json
import math

# =============================================================================
# REGIME DESCRIPTORS -- the physical/social conditions knowledge was forged in
# =============================================================================

class TransmissionMode(Enum):
    ORAL_GENERATIONAL = "oral_generational"       # song, story, direct teaching
    EMBODIED_APPRENTICE = "embodied_apprentice"   # hands-on, lifetime exposure
    WRITTEN_FORMAL = "written_formal"             # books, papers, codified
    OBSERVATIONAL_LANDSCAPE = "observational_landscape"  # reading the land/sky
    EXPERIMENTAL_INSTITUTIONAL = "experimental_institutional"  # lab/academic
    EXTRACTED_AGGREGATED = "extracted_aggregated"  # scraped, harvested, mined


class ValidationDepth(Enum):
    UNTESTED = 0
    SINGLE_CYCLE = 1           # tried once
    MULTI_CYCLE = 2            # tested across seasons/years
    GENERATIONAL = 3           # 2-5 generations
    DEEP_GENERATIONAL = 4      # 10+ generations, embedded in tradition
    DEEP_TIME = 5              # paleorecord / multi-millennial


@dataclass
class Regime:
    """The constraint environment a piece of knowledge was forged under."""
    # Geographic / physical
    geography: str = ""                    # e.g. "Northern Minnesota boreal", "Punjab plain"
    climate_zone: str = ""                 # Koppen or descriptive
    elevation_m: Optional[float] = None
    magnetic_latitude_deg: Optional[float] = None
    avg_temp_C: Optional[float] = None
    precip_mm_per_yr: Optional[float] = None
    co2_ppm_at_emergence: Optional[float] = None

    # Forcing functions (what pressure shaped the knowledge)
    resource_scarcity: List[str] = field(default_factory=list)  # water, fuel, food, etc.
    population_density: str = ""           # sparse, moderate, dense
    technology_level: str = ""             # preindustrial, industrial, digital
    institutional_context: str = ""        # tribal, agrarian, corporate, academic

    # Social / cultural
    community_continuity_yrs: Optional[float] = None  # how long that community persisted
    parallel_communities: List[str] = field(default_factory=list)  # other groups that solved similarly

    def fingerprint(self) -> Dict:
        """Compact regime descriptor for matching."""
        return {k: v for k, v in asdict(self).items() if v not in (None, "", [])}


# =============================================================================
# KNOWLEDGE NODE -- a single piece of knowledge with full provenance
# =============================================================================

@dataclass
class KnowledgeNode:
    """A single piece of knowledge with its constraint provenance."""
    id: str                                # unique identifier
    name: str                              # human-readable
    description: str                       # what the knowledge does

    # Provenance
    regime: Regime                         # where/when it emerged
    transmission: TransmissionMode
    validation: ValidationDepth
    generational_depth: int = 0            # explicit count if known

    # Lineage
    parent_ids: List[str] = field(default_factory=list)   # what this descends from
    sibling_ids: List[str] = field(default_factory=list)  # parallel discoveries elsewhere
    derived_ids: List[str] = field(default_factory=list)  # what came from this

    # Attribution (the part extraction usually erases)
    origin_communities: List[str] = field(default_factory=list)
    individual_carriers: List[str] = field(default_factory=list)  # named or anonymized
    carrier_consent: str = "unspecified"   # explicit, implicit, none, contested

    # Validity scope
    valid_under: List[str] = field(default_factory=list)   # conditions where it works
    fails_under: List[str] = field(default_factory=list)   # conditions where it breaks
    assumptions: List[str] = field(default_factory=list)   # invisible preconditions

    # Failure modes if extracted to wrong regime
    extraction_risks: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["transmission"] = self.transmission.value
        d["validation"] = self.validation.value
        return d


# =============================================================================
# REGIME MATCHING -- does current environment match knowledge's validity scope?
# =============================================================================

def regime_distance(source: Regime, target: Regime) -> float:
    """
    Quantify mismatch between source regime and target deployment environment.
    0.0 = identical. Higher = more displacement.
    """
    score = 0.0
    components = 0

    # Numeric features: scaled distances
    numeric_pairs = [
        ("elevation_m", 1000.0),
        ("magnetic_latitude_deg", 30.0),
        ("avg_temp_C", 15.0),
        ("precip_mm_per_yr", 800.0),
        ("co2_ppm_at_emergence", 400.0),
    ]
    for attr, scale in numeric_pairs:
        s = getattr(source, attr)
        t = getattr(target, attr)
        if s is not None and t is not None:
            score += min(2.0, abs(s - t) / scale)
            components += 1

    # Categorical features: 0 if match, 1 if differ
    categorical = ["geography", "climate_zone", "population_density",
                   "technology_level", "institutional_context"]
    for attr in categorical:
        s = getattr(source, attr)
        t = getattr(target, attr)
        if s and t:
            score += 0.0 if s == t else 1.0
            components += 1

    # Set features: Jaccard-distance
    set_attrs = ["resource_scarcity", "parallel_communities"]
    for attr in set_attrs:
        s = set(getattr(source, attr))
        t = set(getattr(target, attr))
        if s or t:
            inter = len(s & t)
            union = len(s | t)
            score += 1.0 - (inter / union if union else 0.0)
            components += 1

    return score / max(components, 1)


def applicability(node: KnowledgeNode, target_regime: Regime,
                  threshold: float = 0.5) -> Dict:
    """
    Check whether a knowledge node applies in the target deployment regime.
    Returns dict with score, verdict, and explanation.
    """
    distance = regime_distance(node.regime, target_regime)
    if distance < threshold:
        verdict = "applicable"
    elif distance < threshold * 2:
        verdict = "review_required"
    else:
        verdict = "regime_mismatch"

    flags = []
    # Hard checks against fails_under
    target_str = json.dumps(target_regime.fingerprint()).lower()
    for fail_cond in node.fails_under:
        if fail_cond.lower() in target_str:
            flags.append(f"FAIL: explicit failure condition matched: {fail_cond}")
            verdict = "regime_mismatch"

    # Validation depth gate
    if node.validation.value < ValidationDepth.MULTI_CYCLE.value:
        flags.append("WARN: knowledge has shallow validation history")

    # Consent gate
    if node.carrier_consent in ("none", "contested"):
        flags.append(f"ETHICS: carrier consent is {node.carrier_consent}")

    return {
        "node_id": node.id,
        "regime_distance": round(distance, 3),
        "verdict": verdict,
        "flags": flags,
        "assumptions_to_verify": node.assumptions,
        "extraction_risks_if_misapplied": node.extraction_risks,
    }


# =============================================================================
# KNOWLEDGE ARCHAEOLOGY TREE -- graph of provenance, not just hierarchy
# =============================================================================

class KnowledgeTree:
    """Directed graph of knowledge nodes with provenance traversal."""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}

    def add(self, node: KnowledgeNode) -> None:
        self.nodes[node.id] = node
        self._reconcile_links(node)

    def _reconcile_links(self, node: KnowledgeNode) -> None:
        """Make sibling and parent/derived links bidirectional across the tree."""
        for sib_id in node.sibling_ids:
            sib = self.nodes.get(sib_id)
            if sib and node.id not in sib.sibling_ids:
                sib.sibling_ids.append(node.id)
        for parent_id in node.parent_ids:
            parent = self.nodes.get(parent_id)
            if parent and node.id not in parent.derived_ids:
                parent.derived_ids.append(node.id)
        # Also: if any existing node names THIS node as parent/sibling, fix back-link
        for other in self.nodes.values():
            if other.id == node.id:
                continue
            if node.id in other.sibling_ids and other.id not in node.sibling_ids:
                node.sibling_ids.append(other.id)
            if node.id in other.parent_ids and other.id not in node.derived_ids:
                node.derived_ids.append(other.id)

    def ancestors(self, node_id: str, depth: int = -1) -> Set[str]:
        """All knowledge this descends from. depth=-1 is unlimited."""
        seen = set()
        stack = [(node_id, 0)]
        while stack:
            nid, d = stack.pop()
            if nid in seen or nid not in self.nodes:
                continue
            seen.add(nid)
            if depth == -1 or d < depth:
                for parent in self.nodes[nid].parent_ids:
                    stack.append((parent, d + 1))
        seen.discard(node_id)
        return seen

    def parallel_lineages(self, node_id: str) -> Dict[str, List[str]]:
        """
        Sibling discoveries -- knowledge that emerged independently in parallel
        communities to solve the same problem under similar constraints.
        Map of community -> sibling ids.
        """
        result: Dict[str, List[str]] = {}
        if node_id not in self.nodes:
            return result
        for sib_id in self.nodes[node_id].sibling_ids:
            if sib_id in self.nodes:
                for community in self.nodes[sib_id].origin_communities:
                    result.setdefault(community, []).append(sib_id)
        return result

    def attribution_trail(self, node_id: str) -> List[Dict]:
        """
        Full attribution: every community and carrier whose knowledge
        contributed to this node, walking the ancestor graph.
        """
        trail = []
        for ancestor_id in self.ancestors(node_id) | {node_id}:
            n = self.nodes[ancestor_id]
            trail.append({
                "node": n.id,
                "name": n.name,
                "communities": list(n.origin_communities),
                "carriers": list(n.individual_carriers),
                "consent": n.carrier_consent,
                "transmission": n.transmission.value,
                "regime": n.regime.fingerprint(),
            })
        return trail

    def deploy_check(self, node_id: str, target_regime: Regime) -> Dict:
        """
        Deploying knowledge into a target regime: returns full provenance
        report plus applicability verdict.
        """
        if node_id not in self.nodes:
            return {"error": f"unknown node {node_id}"}
        node = self.nodes[node_id]
        return {
            "applicability": applicability(node, target_regime),
            "attribution_trail": self.attribution_trail(node_id),
            "parallel_lineages": self.parallel_lineages(node_id),
        }

    def export_json(self) -> str:
        return json.dumps({nid: n.to_dict() for nid, n in self.nodes.items()},
                          indent=2, default=str)


# =============================================================================
# JSON LOADERS -- so communities can author nodes as data, not Python
# =============================================================================

def regime_from_dict(d: Dict) -> Regime:
    return Regime(**{k: v for k, v in d.items() if k in Regime.__dataclass_fields__})


def node_from_dict(d: Dict) -> KnowledgeNode:
    """Build a KnowledgeNode from a dict (typically loaded from JSON)."""
    regime = regime_from_dict(d.get("regime", {}))
    transmission = TransmissionMode(d["transmission"])
    validation = (ValidationDepth(d["validation"])
                  if isinstance(d["validation"], int)
                  else ValidationDepth[d["validation"].upper()])

    fields = {k: v for k, v in d.items()
              if k in KnowledgeNode.__dataclass_fields__
              and k not in ("regime", "transmission", "validation")}
    return KnowledgeNode(
        regime=regime,
        transmission=transmission,
        validation=validation,
        **fields,
    )


def load_tree_from_json(path: str) -> KnowledgeTree:
    """Load a KnowledgeTree from a JSON file containing a list of node dicts."""
    with open(path) as f:
        data = json.load(f)
    tree = KnowledgeTree()
    if isinstance(data, dict):
        data = list(data.values())
    for node_dict in data:
        tree.add(node_from_dict(node_dict))
    return tree


def load_tree_from_directory(directory: str) -> KnowledgeTree:
    """Load every .json file in a directory as one or more nodes into a tree."""
    import os
    tree = KnowledgeTree()
    for fname in sorted(os.listdir(directory)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(directory, fname)) as f:
            data = json.load(f)
        nodes = (data if isinstance(data, list)
                 else [data] if "id" in data
                 else list(data.values()))
        for node_dict in nodes:
            tree.add(node_from_dict(node_dict))
    return tree
