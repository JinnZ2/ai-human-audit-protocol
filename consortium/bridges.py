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
from typing import Any, Callable, Dict, List, Optional

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
                  "epi / epi_confidence (provenance lives one layer up)"],
        notes="Forward bridge from ontology to dynamical layer. "
              "Caller MUST supply rate_fns to get non-zero integration; "
              "default _zero_rate produces nodes that hold state but "
              "do not move.",
    )


# ------------------------------------------------------------
# Trajectory → summary (v1 stub; not yet a full FrameReading)
# ------------------------------------------------------------

def trajectory_summary(
    trajectory: Dict[str, List[float]],
) -> Dict[str, Any]:
    """
    Honest stub for the inverse direction.

    Turning a KFC trajectory into a FrameReading requires interpreting
    trajectory shape — saturation, oscillation, regime drift, FELT
    events — and that interpretation is real work that gets its own
    pass. This function is the smallest useful thing: per-claim
    final state and a coarse direction tag.

    This is NOT a FrameReading. Do not pass its output to
    MultiGeometryCollaboration without a real lift.

    Preserves: per-claim final state, count, basic direction.
    Lossy on:  EVERYTHING ELSE (frame attribution, blind spots,
               confidence semantics, action proposals, regime drift
               flags, FELT events). v1 stub by design.
    """
    summary: Dict[str, Any] = {
        "claim_count": 0,
        "claims": {},
        "felt_events": [],
        "_warning": (
            "trajectory_summary is a v1 stub — interpreting trajectory "
            "shape into a FrameReading is real work and is open. "
            "Do not pass this output to MultiGeometryCollaboration."
        ),
    }
    for k, v in trajectory.items():
        if k.startswith("_"):
            # FELT events and other meta channels
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
        preserves=["per-claim final state", "claim count", "coarse direction"],
        lossy_on=["frame attribution", "blind spot information",
                  "confidence semantics", "regime drift flags",
                  "load-bearing structure", "action proposals",
                  "FELT event interpretation"],
        notes="V1 STUB. The honest inverse bridge (trajectory → "
              "FrameReading) requires interpreting trajectory shape "
              "(saturation, oscillation, drift, FELT events) and "
              "is open work.",
    )


# ============================================================
# All bridge reports — for inspection / audit
# ============================================================
def all_bridge_reports() -> List[BridgeReport]:
    return [
        reading_to_primitives_report(),
        frame_reading_to_primitives_report(),
        primitives_to_claim_graph_report(),
        trajectory_summary_report(),
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
    print(f"  warning: {summary['_warning'][:80]}...")

    # 5. show what each bridge preserves / drops
    print("\n" + "=" * 70)
    print("BRIDGE REPORTS — what survives, what's lossy")
    print("=" * 70)
    for rep in all_bridge_reports():
        print(f"\n[{rep.bridge_name}]")
        print(f"  preserves: {rep.preserves}")
        print(f"  lossy_on:  {rep.lossy_on}")
        print(f"  notes: {rep.notes}")
