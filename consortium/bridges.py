# ============================================================
# BRIDGES — connect FrameReading ↔ Primitive ↔ ClaimNode
# the layer where collaboration_protocol meets ontology_layer
# meets kfc_runtime. Each bridge function declares what it
# preserves and what it drops, following the TransformRule
# pattern in ontology_layer.py.
#
# v1 scope: forward direction (reading → primitives → claim graph)
# is complete and tested. Inverse direction (trajectory → reading)
# is stubbed honestly as `trajectory_summary` — turning a KFC
# trajectory back into a FrameReading requires interpreting
# trajectory shape (saturation, oscillation, drift) which is real
# work and gets its own pass.
#
# CC0 | bridges relational_cognition/ prose to consortium/ code
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from consortium.collaboration_protocol import (
    GeometricFrame,
    FrameReading,
)
from consortium.ontology_layer import Primitive
from consortium.kfc_runtime import ClaimNode
from consortium.embodied_sensor import EmbodiedReading


# ------------------------------------------------------------
# Default mappings — overridable per call
# ------------------------------------------------------------

# epi sub-tag → consortium frame_id (default routing).
# Direct-sensing modalities all route to embodied_sensor or
# ecological_signal because that's what they *are*, regardless of
# operator_type. The operator_type is captured separately in
# FrameReading.assumptions_required.
EPI_TO_FRAME: Dict[str, str] = {
    "kinesthetic":      "embodied_sensor",
    "olfactory":        "embodied_sensor",
    "visual":           "embodied_sensor",
    "auditory":         "embodied_sensor",
    "instrumental":     "embodied_sensor",
    "compound":         "ecological_signal",
    "phenological":     "ecological_signal",
    "behavioral":       "ecological_signal",
    "presence_absence": "ecological_signal",
    "inferred":         "thermodynamic_geometry",
    "asserted":         "narrative_structured",
}

# epi sub-tag → ontology domain (where the Primitive lives).
EPI_TO_DOMAIN: Dict[str, str] = {
    "kinesthetic":      "embodied",
    "olfactory":        "embodied",
    "visual":           "embodied",
    "auditory":         "embodied",
    "instrumental":     "instrumental",
    "compound":         "ecological",
    "phenological":     "ecological",
    "behavioral":       "ecological",
    "presence_absence": "ecological",
    "inferred":         "inferred",
    "asserted":         "asserted",
}

# Mapping from a reading's epi/role to the Primitive.role string.
EPI_TO_ROLE: Dict[str, str] = {
    "kinesthetic":      "claim",
    "olfactory":        "claim",
    "visual":           "claim",
    "auditory":         "claim",
    "instrumental":     "claim",
    "compound":         "claim",
    "phenological":     "claim",
    "behavioral":       "claim",
    "presence_absence": "claim",
    "inferred":         "claim",
    "asserted":         "claim",
}


# ------------------------------------------------------------
# BridgeReport — what survived the transform, what didn't
# follows TransformRule.preserves / lossy_on convention
# ------------------------------------------------------------
@dataclass
class BridgeReport:
    """
    What a bridge function preserves vs. drops.

    Following ontology_layer.TransformRule's preserves/lossy_on
    convention: every transform across abstraction layers loses
    something. The honest move is to name what.
    """
    bridge_name: str
    preserves: List[str] = field(default_factory=list)
    lossy_on: List[str] = field(default_factory=list)
    notes: str = ""


# ------------------------------------------------------------
# Frame selection
# ------------------------------------------------------------

def select_frame(
    epi: str,
    frames: Dict[str, GeometricFrame],
    override: Optional[str] = None,
) -> GeometricFrame:
    """
    Pick a consortium frame for a reading, by epi sub-tag.

    Routing is by what kind of sensing happened (epi), not by
    operator_type. A human-visual reading and an AI-visual
    reading both route to embodied_sensor because they're both
    direct visual reads; the operator_type is captured separately
    in FrameReading.assumptions_required.

    Caller may override with an explicit frame_id.
    """
    if override is not None:
        if override not in frames:
            raise KeyError(f"override frame_id {override!r} not in frames")
        return frames[override]
    target = EPI_TO_FRAME.get(epi)
    if target is None or target not in frames:
        # honest fallback rather than silent default
        raise ValueError(
            f"no frame mapping for epi={epi!r}; "
            f"caller must pass override frame_id"
        )
    return frames[target]


def select_frame_for_reading(
    reading: EmbodiedReading,
    frames: Dict[str, GeometricFrame],
    override: Optional[str] = None,
) -> GeometricFrame:
    """Convenience wrapper: select_frame using a reading's epi."""
    return select_frame(reading.epi, frames, override=override)


# ------------------------------------------------------------
# Reading → Primitives
# ------------------------------------------------------------

def reading_to_primitives(
    reading: EmbodiedReading,
    domain: Optional[str] = None,
) -> List[Primitive]:
    """
    Lift an EmbodiedReading into one Primitive per claim_ref.

    Each Primitive shares the reading's epi/confidence/bounds.
    The reading's observation becomes the Primitive's `form` for
    the first claim_ref; subsequent Primitives reference it via
    a back-reference (so the substantive description isn't
    duplicated).

    Bounds are constructed from the reading's location (spatial)
    and timestamp (temporal); scale is left as 'point' since a
    single reading is a point measurement unless the operator
    declares otherwise in conditions["scale"].

    Preserves: claim_refs, epi, confidence, observation (on first),
               operator_type (in form prefix).
    Lossy on:  conditions dict (only `scale` is consulted),
               coating_probe (lives only on the reading, not the
               primitive — the primitive can be re-coated by
               downstream use).
    """
    if not reading.claim_refs:
        return []

    domain = domain or EPI_TO_DOMAIN.get(reading.epi, "embodied")
    role = EPI_TO_ROLE.get(reading.epi, "claim")
    scale = reading.conditions.get("scale", "point")
    bounds = (
        reading.location,
        reading.timestamp.isoformat(),
        scale,
    )

    primitives: List[Primitive] = []
    primary_claim = reading.claim_refs[0]
    primary_form = (
        f"[{reading.operator_type}|{reading.epi}] {reading.observation}"
    )

    primitives.append(Primitive(
        concept_id=primary_claim,
        domain=domain,
        form=primary_form,
        role=role,
        couplings=[c for c in reading.claim_refs if c != primary_claim],
        bounds=bounds,
        epi=reading.epi if reading.epi in {"measured", "inferred",
                                            "assumed", "contradicted",
                                            "missing"} else "measured",
        epi_confidence=reading.confidence,
    ))

    # subsequent claim_refs get back-references (no duplicated form)
    for c in reading.claim_refs[1:]:
        primitives.append(Primitive(
            concept_id=c,
            domain=domain,
            form=f"[ref:{primary_claim}] {primary_form}",
            role=role,
            couplings=[primary_claim] + [
                x for x in reading.claim_refs if x != c and x != primary_claim
            ],
            bounds=bounds,
            epi=reading.epi if reading.epi in {"measured", "inferred",
                                                "assumed", "contradicted",
                                                "missing"} else "measured",
            epi_confidence=reading.confidence,
        ))

    return primitives


def reading_to_primitives_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="reading_to_primitives",
        preserves=["claim_refs (as concept_ids)", "epi", "confidence",
                   "observation", "operator_type", "location", "timestamp"],
        lossy_on=["coating_probe (lives on reading only)",
                  "conditions dict (only `scale` consulted)",
                  "rate dynamics (Primitives are structural)"],
        notes="Forward bridge: structural lift only. Dynamics live "
              "in the ClaimNode layer; coating probe re-runs are "
              "downstream's responsibility.",
    )


# ------------------------------------------------------------
# FrameReading → Primitives
# ------------------------------------------------------------

def frame_reading_to_primitives(
    fr: FrameReading,
    domain: Optional[str] = None,
) -> List[Primitive]:
    """
    Lift a FrameReading into one Primitive per visible_coupling.

    Each Primitive lives in the frame's domain (default) or
    caller-supplied domain. The frame's id is recorded in the
    Primitive's `form` so the origin frame is recoverable.

    Preserves: visible_couplings (as concept_ids), confidence,
               proposed_diagnosis (in form), frame_id (in form).
    Lossy on:  proposed_actions (live on the reading, not the
               primitive — actions are collaboration-level
               synthesis, not concept-level structure),
               assumptions_required, where_this_frame_breaks
               (frame's documented blind spots; recoverable from
               the frame itself if needed).
    """
    if not fr.visible_couplings:
        return []

    domain = domain or fr.frame.frame_id
    primitives: List[Primitive] = []

    for c in fr.visible_couplings:
        primitives.append(Primitive(
            concept_id=c,
            domain=domain,
            form=f"[frame:{fr.frame.frame_id}] {fr.proposed_diagnosis}",
            role="claim",
            couplings=[x for x in fr.visible_couplings if x != c],
            bounds=("from_frame_reading", fr.problem_id, "frame_scale"),
            epi="measured" if fr.frame.epistemic_strength
                 in {"measured", "embodied", "measured_indirectly",
                     "measured_implicit"}
                 else "inferred",
            epi_confidence=fr.confidence,
        ))

    return primitives


def frame_reading_to_primitives_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="frame_reading_to_primitives",
        preserves=["visible_couplings", "confidence", "proposed_diagnosis",
                   "frame_id"],
        lossy_on=["proposed_actions (collab-level)",
                  "assumptions_required",
                  "where_this_frame_breaks (recoverable from frame)"],
        notes="Forward bridge from collaboration layer to ontology layer. "
              "Actions are dropped because they're synthesis output, not "
              "structural input.",
    )


# ------------------------------------------------------------
# Primitives → ClaimNode graph
# ------------------------------------------------------------

def _zero_rate(state, coupled, ctx):
    """Default rate_fn: state does not move. Used when no rate
    function was supplied for a primitive being lifted to a ClaimNode.
    Honest placeholder: the node holds state but doesn't integrate."""
    return 0.0


def primitives_to_claim_graph(
    primitives: List[Primitive],
    rate_fns: Optional[Dict[str, Callable]] = None,
    cyc: int = 1,
    cond: Optional[List[Callable[[Dict], bool]]] = None,
    fail: Optional[List[Callable[[Dict], bool]]] = None,
) -> Dict[str, ClaimNode]:
    """
    Lift Primitives into a ClaimNode graph for KFC integration.

    Caller supplies `rate_fns: {concept_id: rate_fn}` for any nodes
    where the dynamics are known. Missing entries get `_zero_rate`
    as an honest placeholder.

    Defaults:
        cyc=1 (seasonal)
        cond=[]
        fail=[]
        meas=[] (Primitives don't carry measurement methods directly)

    Preserves: concept_id (→ id), couplings (→ rel), bounds.
    Lossy on:  domain, form, role (these are ontology-level
               structure that the dynamical layer doesn't use),
               epi/epi_confidence (the dynamical layer integrates
               state; provenance lives one layer up).
    Adds:      rate_fn (zero by default — caller should supply).
    """
    rate_fns = rate_fns or {}
    cond = cond if cond is not None else []
    fail = fail if fail is not None else []

    graph: Dict[str, ClaimNode] = {}
    for p in primitives:
        # collisions: if two primitives share concept_id, last wins
        # but we record nothing about it — caller's responsibility
        # to dedupe before this call
        graph[p.concept_id] = ClaimNode(
            id=p.concept_id,
            rate_fn=rate_fns.get(p.concept_id, _zero_rate),
            bounds=p.bounds,
            cond=list(cond),
            rel=list(p.couplings),
            fail=list(fail),
            meas=[],
            cyc=cyc,
        )
    return graph


def primitives_to_claim_graph_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="primitives_to_claim_graph",
        preserves=["concept_id", "couplings", "bounds"],
        lossy_on=["domain (ontology-level)",
                  "form (ontology-level)",
                  "role (ontology-level)",
                  "epi / epi_confidence (provenance lives one layer up)",
                  "coupling kind / strength / load_bearing — these "
                  "live in CouplingMetadata via the typed variant; "
                  "the untyped bridge drops them"],
        notes="Forward bridge from ontology to dynamical layer. "
              "Caller MUST supply rate_fns to get non-zero integration; "
              "default _zero_rate produces nodes that hold state but "
              "do not move. For typed couplings (kind, strength, "
              "load_bearing per edge), use primitives_to_typed_claim_graph.",
    )


# ------------------------------------------------------------
# Typed coupling metadata (per CLAUDE_REQUIREMENTS.md §3)
# Side-channel companion to ClaimNode graphs. Lives alongside
# rather than inside ClaimNode because both Primitive and
# ClaimNode are upstream-authored and shipped verbatim. When
# upstream ships v2 with typed couplings inline, this side-channel
# folds back in.
# ------------------------------------------------------------

# Coupling kinds per CLAUDE_REQUIREMENTS.md §Requirement 3.
VALID_COUPLING_KINDS = {
    "causal_forward",   # A drives B
    "causal_reverse",   # B drives A
    "bidirectional",    # mutual coupling
    "constraint",       # A bounds B but doesn't drive it
    "correlational",    # co-occur, mechanism unknown
    "decorative",       # historical association, no current force
    "unknown",          # not specified by caller
}


@dataclass
class CouplingMetadata:
    """
    Per-edge typed metadata.

    Used alongside a ClaimNode graph to carry the coupling
    semantics from CLAUDE_REQUIREMENTS.md §Requirement 3 without
    modifying the upstream-shipped Primitive / ClaimNode classes.

    Fields:
        kind: one of VALID_COUPLING_KINDS
        strength: 0..1 (constant; the dynamic case is left for v2)
        load_bearing: if removed, does the system collapse?
        conditional_notes: free-form context where this coupling
            fires (until rate_fn-conditional couplings ship)
    """
    kind: str = "unknown"
    strength: float = 1.0
    load_bearing: bool = False
    conditional_notes: str = ""

    def __post_init__(self):
        if self.kind not in VALID_COUPLING_KINDS:
            raise ValueError(
                f"coupling kind {self.kind!r} not in "
                f"{sorted(VALID_COUPLING_KINDS)}"
            )
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError(
                f"strength {self.strength} outside [0, 1]"
            )


@dataclass
class TypedClaimGraph:
    """
    A ClaimNode graph plus its typed coupling metadata.

    `nodes` is the same dict shape returned by
    `primitives_to_claim_graph`. `coupling_metadata` is keyed by
    (source_concept_id, target_concept_id) tuples. Edges that
    appear in `nodes[X].rel` but NOT in `coupling_metadata` default
    to `kind="unknown"` when queried via `get_kind` / `is_load_bearing`.
    """
    nodes: Dict[str, ClaimNode]
    coupling_metadata: Dict[Tuple[str, str], CouplingMetadata] = field(
        default_factory=dict
    )

    def get_kind(self, source: str, target: str) -> str:
        m = self.coupling_metadata.get((source, target))
        return m.kind if m else "unknown"

    def is_load_bearing(self, source: str, target: str) -> bool:
        m = self.coupling_metadata.get((source, target))
        return m.load_bearing if m else False

    def load_bearing_edges(self) -> List[Tuple[str, str]]:
        return [
            (s, t) for (s, t), m in self.coupling_metadata.items()
            if m.load_bearing
        ]


def primitives_to_typed_claim_graph(
    primitives: List[Primitive],
    coupling_specs: Optional[Dict[Tuple[str, str], CouplingMetadata]] = None,
    rate_fns: Optional[Dict[str, Callable]] = None,
    cyc: int = 1,
    cond: Optional[List[Callable[[Dict], bool]]] = None,
    fail: Optional[List[Callable[[Dict], bool]]] = None,
) -> TypedClaimGraph:
    """
    Like `primitives_to_claim_graph` but carries typed coupling
    metadata.

    `coupling_specs` is `{(source_id, target_id): CouplingMetadata}`.
    Specs are kept verbatim; missing edges default to `"unknown"`
    when queried via `TypedClaimGraph.get_kind`. Specs that name
    edges not present in any primitive's `couplings` are kept as
    declared — they are caller-supplied metadata, possibly forward-
    looking; the bridge does not silently drop them.

    Returns a `TypedClaimGraph(nodes, coupling_metadata)`.

    Preserves: everything `primitives_to_claim_graph` preserves,
               plus per-edge kind / strength / load_bearing.
    Lossy on:  same as `primitives_to_claim_graph` for the structural
               fields (domain, form, role, epi); coupling specs are
               PRESERVED rather than dropped.
    """
    nodes = primitives_to_claim_graph(
        primitives,
        rate_fns=rate_fns,
        cyc=cyc,
        cond=cond,
        fail=fail,
    )
    return TypedClaimGraph(
        nodes=nodes,
        coupling_metadata=dict(coupling_specs or {}),
    )


def primitives_to_typed_claim_graph_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="primitives_to_typed_claim_graph",
        preserves=["concept_id", "couplings (as rel)", "bounds",
                   "coupling kind per edge",
                   "coupling strength per edge",
                   "load_bearing per edge",
                   "caller-supplied conditional notes per edge"],
        lossy_on=["domain (ontology-level)",
                  "form (ontology-level)",
                  "role (ontology-level)",
                  "epi / epi_confidence (provenance lives one layer up)",
                  "edges absent from coupling_specs are reported as "
                  "kind='unknown' (lossy because caller may have "
                  "intended a default that is not 'unknown')"],
        notes="Typed variant of primitives_to_claim_graph per "
              "CLAUDE_REQUIREMENTS.md §Requirement 3. Coupling "
              "metadata lives in a CouplingMetadata side-channel "
              "(TypedClaimGraph.coupling_metadata) rather than "
              "inside ClaimNode, because both Primitive and "
              "ClaimNode are upstream-authored and shipped verbatim. "
              "When upstream ships v2 with typed couplings inline, "
              "this side-channel folds back in.",
    )


# ------------------------------------------------------------
# Trajectory → summary (lightweight; for full FrameReading lift
# use trajectory_to_frame_reading below)
# ------------------------------------------------------------

def trajectory_summary(
    trajectory: Dict[str, List[float]],
) -> Dict[str, Any]:
    """
    Lightweight summary of a KFC trajectory.

    Returns per-claim final state, coarse direction tag, and any
    FELT events. For a full inverse lift back into a FrameReading
    suitable for re-injection into MultiGeometryCollaboration, use
    `trajectory_to_frame_reading` below.

    Preserves: per-claim final state, count, basic direction,
               FELT event count.
    Lossy on:  trajectory shape (only direction, not curvature),
               coupling structure, frame attribution.
    """
    summary: Dict[str, Any] = {
        "claim_count": 0,
        "claims": {},
        "felt_events": [],
        "_note": (
            "trajectory_summary is a lightweight summary. For a full "
            "FrameReading lift, use trajectory_to_frame_reading."
        ),
    }
    for k, v in trajectory.items():
        if k.startswith("_"):
            summary["felt_events"].extend(v if isinstance(v, list) else [v])
            continue
        summary["claim_count"] += 1
        if not v:
            summary["claims"][k] = {"final": None, "direction": "no_steps"}
            continue
        first, last = v[0], v[-1]
        delta = last - first
        if abs(delta) < 1e-9:
            direction = "stable"
        elif delta > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
        summary["claims"][k] = {
            "final": last,
            "first": first,
            "delta": delta,
            "direction": direction,
            "n_steps": len(v),
        }
    return summary


def trajectory_summary_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="trajectory_summary",
        preserves=["per-claim final state", "claim count",
                   "coarse direction", "FELT event count"],
        lossy_on=["trajectory shape (curvature, oscillation, saturation)",
                  "coupling structure",
                  "frame attribution",
                  "regime drift interpretation"],
        notes="Lightweight summary. For full FrameReading lift, "
              "use trajectory_to_frame_reading.",
    )


# ------------------------------------------------------------
# Trajectory shape classification
# ------------------------------------------------------------

# Trajectory shape categories. The classifier maps a numeric series
# onto one of these. Each category is itself a frame imposed on raw
# numbers — classification is a coating risk by construction.
TRAJECTORY_SHAPES = {
    "no_steps",            # empty series
    "single_point",        # only one entry
    "stable",              # range below epsilon
    "monotonic_increase",
    "monotonic_decrease",
    "saturating_increase", # monotonic with decreasing |deltas|
    "saturating_decrease",
    "accelerating_increase",   # monotonic with increasing |deltas|
    "accelerating_decrease",
    "oscillating",         # multiple sign changes in deltas
    "mixed",               # neither monotonic nor oscillating-enough
}


def _monotonic_subkind(deltas: List[float], direction: str) -> str:
    """Refine a monotonic trajectory into saturating / accelerating /
    plain monotonic. Compares first-half mean |delta| to second-half."""
    abs_d = [abs(d) for d in deltas]
    if len(abs_d) < 4:
        return f"monotonic_{direction}"
    half = len(abs_d) // 2
    first = abs_d[:half]
    last = abs_d[half:]
    first_avg = sum(first) / max(len(first), 1)
    last_avg = sum(last) / max(len(last), 1)
    if first_avg < 1e-12:
        return f"monotonic_{direction}"
    ratio = last_avg / first_avg
    if ratio < 0.5:
        return f"saturating_{direction}"
    if ratio > 2.0:
        return f"accelerating_{direction}"
    return f"monotonic_{direction}"


def classify_trajectory(
    series: List[float],
    epsilon: float = 1e-6,
    min_oscillations: int = 2,
) -> str:
    """
    Classify a single-claim trajectory into one of TRAJECTORY_SHAPES.

    The classification is a coarse interpretive frame. A stable
    series and an oscillating series with frequency higher than the
    sampling rate look identical; this function does not attempt to
    detect that aliasing. Callers should treat the output as a
    coating-risk interpretation, not a fact about the system.
    """
    n = len(series)
    if n == 0:
        return "no_steps"
    if n == 1:
        return "single_point"

    range_ = max(series) - min(series)
    if range_ < epsilon:
        return "stable"

    deltas = [series[i+1] - series[i] for i in range(n-1)]

    # multiple sign changes → oscillating
    sign_changes = sum(
        1 for i in range(len(deltas)-1)
        if deltas[i] * deltas[i+1] < 0
    )
    if sign_changes >= min_oscillations:
        return "oscillating"

    if all(d >= -epsilon for d in deltas):
        return _monotonic_subkind(deltas, "increase")
    if all(d <= epsilon for d in deltas):
        return _monotonic_subkind(deltas, "decrease")

    return "mixed"


# ------------------------------------------------------------
# Trajectory → FrameReading (full inverse lift)
# ------------------------------------------------------------

def _compute_load_bearing(
    trajectory: Dict[str, List[float]],
    top_n: int = 3,
) -> List[str]:
    """Identify load-bearing claims by total |delta| over the
    trajectory. Excludes meta-channels (underscore-prefixed keys)."""
    movement = {}
    for cid, series in trajectory.items():
        if cid.startswith("_"):
            continue
        if not series:
            continue
        movement[cid] = abs(max(series) - min(series))
    return [
        cid for cid, _ in sorted(
            movement.items(),
            key=lambda x: x[1],
            reverse=True,
        )[:top_n]
    ]


def _synthesize_diagnosis(
    shapes: Dict[str, str],
    felt_events: List[Any],
) -> str:
    """Synthesize a diagnosis sentence from trajectory shapes + FELT
    events. FELT presence dominates because it indicates the runtime
    itself flagged coherence loss during integration."""
    if felt_events:
        return (
            f"FELT_TRIGGER fired {len(felt_events)} time(s) during "
            f"integration; regime drift or coherence loss suspected"
        )

    accelerating = [c for c, s in shapes.items()
                    if s.startswith("accelerating")]
    oscillating = [c for c, s in shapes.items() if s == "oscillating"]
    saturating = [c for c, s in shapes.items()
                  if s.startswith("saturating")]
    monotonic = [c for c, s in shapes.items() if s.startswith("monotonic")]
    mixed = [c for c, s in shapes.items() if s == "mixed"]
    stable = [c for c, s in shapes.items() if s == "stable"]

    parts = []
    if accelerating:
        parts.append(f"divergent dynamics in {accelerating}")
    if oscillating:
        parts.append(f"oscillation in {oscillating}")
    if saturating:
        parts.append(f"saturation in {saturating}")
    if monotonic and not (accelerating or saturating):
        parts.append(f"monotonic drift in {monotonic}")
    if mixed:
        parts.append(f"mixed dynamics in {mixed}")
    if stable and not (accelerating or oscillating
                        or saturating or monotonic or mixed):
        return f"system stable across observation window in {stable}"
    if not parts:
        return "no characteristic dynamics detected"
    return "; ".join(parts)


def _derive_confidence(
    shapes: Dict[str, str],
    felt_events: List[Any],
) -> float:
    """Heuristic confidence for the inverse lift. Lower when FELT
    fired, lower when shape is ambiguous (mixed/oscillating). NOT
    calibrated — callers should treat this as a starting prior, not
    a calibrated value."""
    base = 0.70
    if felt_events:
        return max(0.30, base - 0.10 * len(felt_events))
    types = set(shapes.values())
    if "mixed" in types:
        base -= 0.15
    if "oscillating" in types:
        base -= 0.10
    return max(0.30, min(0.85, base))


def trajectory_to_frame_reading(
    trajectory: Dict[str, List[float]],
    frame: GeometricFrame,
    problem_id: str,
    proposed_actions: Optional[List[tuple]] = None,
) -> FrameReading:
    """
    Lift a KFC trajectory into a FrameReading suitable for
    re-injection into MultiGeometryCollaboration.

    The classifier ascribes a shape category to each per-claim
    series; each category is a frame imposed on numbers and is
    therefore a coating risk. The resulting FrameReading carries
    its `trajectory_classification=heuristic_v1` flag in
    `assumptions_required` so downstream readers can audit it.

    Args:
        trajectory: KFC `query()` output, possibly including
            underscore-prefixed meta channels (e.g. _felt).
        frame: the GeometricFrame that owns this reading. Typically
            the frame whose model produced the integration.
        problem_id: problem identifier for the resulting FrameReading.
        proposed_actions: optional list of (action, reversibility);
            inverse lifts may include actions if the integrating
            frame proposes any.

    Preserves: claim ids that integrated, trajectory shape per claim,
               FELT event count, relative load-bearing (by total
               |delta|).
    Lossy on:  continuous trajectory (compressed to a category),
               exact rate dynamics, coupling kind (inferred only
               from co-movement), FELT event semantic content,
               confidence (derived heuristically).
    """
    series_data = {k: v for k, v in trajectory.items()
                   if not k.startswith("_")}
    felt_events: List[Any] = []
    for k, v in trajectory.items():
        if k.startswith("_"):
            felt_events.extend(v if isinstance(v, list) else [v])

    shapes = {cid: classify_trajectory(s) for cid, s in series_data.items()}
    load_bearing = _compute_load_bearing(trajectory)
    diagnosis = _synthesize_diagnosis(shapes, felt_events)
    confidence = _derive_confidence(shapes, felt_events)

    return FrameReading(
        frame=frame,
        problem_id=problem_id,
        visible_couplings=list(series_data.keys()),
        load_bearing_elements=load_bearing,
        invisible_aspects=list(frame.couplings_invisible),
        proposed_diagnosis=diagnosis,
        proposed_actions=list(proposed_actions or []),
        confidence=confidence,
        assumptions_required=[
            "trajectory_classification=heuristic_v1",
            f"shapes={shapes}",
            f"felt_events_count={len(felt_events)}",
            f"load_bearing_top_n={len(load_bearing)}",
        ],
        where_this_frame_breaks=list(frame.couplings_invisible),
    )


def trajectory_to_frame_reading_report() -> BridgeReport:
    return BridgeReport(
        bridge_name="trajectory_to_frame_reading",
        preserves=["claim ids that integrated",
                   "trajectory shape per claim "
                   "(stable / monotonic / saturating / accelerating / "
                   "oscillating / mixed)",
                   "FELT event count",
                   "relative load-bearing (top-N by total |delta|)"],
        lossy_on=["continuous trajectory (compressed to category)",
                  "exact rate dynamics",
                  "coupling kind (inferred from co-movement only)",
                  "FELT event semantic content (count only)",
                  "confidence (derived heuristically; not calibrated)"],
        notes="V1 interpretive bridge. Each shape category is itself "
              "a frame imposed on raw numbers — classification is a "
              "coating risk by construction. The resulting "
              "FrameReading carries trajectory_classification="
              "heuristic_v1 in assumptions_required so the heuristic "
              "is auditable downstream. Caller should run a coating "
              "probe on the resulting FrameReading before treating "
              "it as ground truth.",
    )


# ============================================================
# All bridge reports — for inspection / audit
# ============================================================
def all_bridge_reports() -> List[BridgeReport]:
    return [
        reading_to_primitives_report(),
        frame_reading_to_primitives_report(),
        primitives_to_claim_graph_report(),
        primitives_to_typed_claim_graph_report(),
        trajectory_summary_report(),
        trajectory_to_frame_reading_report(),
    ]


# ============================================================
# DEMO — full forward pipeline
# EmbodiedReading → Primitives → ClaimNode graph → KFC query
#                → trajectory_summary
# ============================================================
if __name__ == "__main__":
    from consortium.collaboration_protocol import build_consortium_frames
    from consortium.embodied_sensor import example_readings
    from consortium.kfc_runtime import query

    print("=" * 70)
    print("BRIDGE PIPELINE DEMO — forward direction")
    print("=" * 70)

    readings = example_readings()
    frames = {f.frame_id: f for f in build_consortium_frames()}

    # take the human kinesthetic + instrument readings (same claim_refs:
    # mulch_h2o, soil_thermal_mass) and lift them through the pipeline
    selected = [r for r in readings if "mulch_h2o" in r.claim_refs]
    print(f"\nSelected {len(selected)} readings touching mulch_h2o:")
    for r in selected:
        print(f"  - [{r.operator_type:10s}] {r.sensor_id}")

    # 1. reading → primitives
    all_primitives: List[Primitive] = []
    for r in selected:
        prims = reading_to_primitives(r)
        all_primitives.extend(prims)
        print(f"\n  reading_to_primitives({r.operator_type}) → "
              f"{len(prims)} primitives")
        for p in prims:
            print(f"    [{p.domain:10s}] {p.concept_id:25s} epi={p.epi} "
                  f"conf={p.epi_confidence}")

    # dedupe by concept_id (real consortium would do this thoughtfully —
    # right now we just keep first-seen)
    seen = {}
    for p in all_primitives:
        if p.concept_id not in seen:
            seen[p.concept_id] = p
    deduped = list(seen.values())
    print(f"\nDeduped: {len(all_primitives)} → {len(deduped)} primitives")

    # 2. primitives → claim graph
    rate_fns = {
        "mulch_h2o": lambda M, rel, ctx: ctx.get("I", 0) - ctx.get("E", 0),
        "soil_thermal_mass": lambda T, rel, ctx: 0.01 * (15.0 - T),
    }
    graph = primitives_to_claim_graph(deduped, rate_fns=rate_fns, cyc=1)
    print(f"\nprimitives_to_claim_graph → {len(graph)} ClaimNodes:")
    for nid, node in graph.items():
        rate_kind = "supplied" if nid in rate_fns else "zero_rate (placeholder)"
        print(f"  {nid:25s} cyc={node.cyc} rate_fn={rate_kind} "
              f"rel={node.rel}")

    # 3. integrate
    ctx = {"space": "from_frame_reading", "time": "any", "scale": "any",
           "I": 2.0, "E": 0.5}
    # bounds-overlap on free-form strings won't activate; for the demo
    # we just trace the structure rather than running a real integration
    print(f"\n(integration via consortium.kfc_runtime.query — bounds checking "
          f"is structural; demo skips activation)")

    # 4. summarize a fake trajectory to show the inverse stub
    fake_traj = {
        "mulch_h2o": [1.0, 1.1, 1.2, 1.5, 1.8],
        "soil_thermal_mass": [10.0, 10.5, 10.8, 11.0, 11.0],
        "_felt": ["FELT_TRIGGER coherence=0.30 < 0.35 → recalibrate"],
    }
    summary = trajectory_summary(fake_traj)
    print(f"\ntrajectory_summary (v1 stub):")
    for cid, info in summary["claims"].items():
        print(f"  {cid:25s} {info}")
    print(f"  felt_events: {summary['felt_events']}")
    print(f"  note: {summary['_note'][:80]}...")

    # 5. show what each bridge preserves / drops
    print("\n" + "=" * 70)
    print("BRIDGE REPORTS — what survives, what's lossy")
    print("=" * 70)
    for rep in all_bridge_reports():
        print(f"\n[{rep.bridge_name}]")
        print(f"  preserves: {rep.preserves}")
        print(f"  lossy_on:  {rep.lossy_on}")
        print(f"  notes: {rep.notes}")
