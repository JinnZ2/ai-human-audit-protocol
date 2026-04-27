# ============================================================
# COLLABORATION PROTOCOL — viewing a problem from different geometries
# how multiple AIs + Kavik (embodied sensor) + traditional knowledge
# read the same problem through different epistemic frames
# CC0 | JinnZ2/multi-geometry-collaboration
# ============================================================

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Tuple, Optional
from datetime import datetime

# ------------------------------------------------------------
# LAYER 0 — what is a "geometry" in this context
# ------------------------------------------------------------
@dataclass
class GeometricFrame:
    """
    A way of reading a problem.
    NOT a discipline. NOT a methodology.
    A SHAPE through which the problem becomes legible.
    """
    frame_id: str                      # "thermodynamic" | "embodied" | "narrative" | etc
    operator_type: str                 # "AI_model" | "human_sensor" | "tradition_holder"
    primitives: List[str]              # what counts as a fundamental unit
    couplings_visible: List[str]       # which relationships this frame can see
    couplings_invisible: List[str]     # known blind spots
    epistemic_strength: str            # "measured" | "embodied" | "transmitted" | "inferred"
    confidence_calibration: float      # 0..1, how reliable in this domain


# ------------------------------------------------------------
# LAYER 1 — the problem itself, before it's framed
# ------------------------------------------------------------
@dataclass
class Problem:
    """
    A problem is NOT defined by the words used to describe it.
    It's defined by the coupling structure that produces it.
    Different frames will name it differently.
    The problem is invariant. The descriptions vary.
    """
    problem_id: str
    presenting_symptoms: List[str]     # what people complain about
    suspected_couplings: List[str]     # what's connected to what
    bounds: Tuple[Any, Any, Any]       # spatial, temporal, scale
    regime_context: Dict[str, Any]     # what regime is the problem occurring in
    stakes: List[str]                  # what's at risk if not resolved


# ------------------------------------------------------------
# LAYER 2 — how each frame reads the problem
# ------------------------------------------------------------
@dataclass
class FrameReading:
    """
    What ONE frame sees when it looks at the problem.
    Includes what it CAN'T see and admits it.
    """
    frame: GeometricFrame
    problem_id: str

    # what this frame surfaces
    visible_couplings: List[str]
    load_bearing_elements: List[str]
    invisible_aspects: List[str]

    # what this frame proposes
    proposed_diagnosis: str
    proposed_actions: List[Tuple[str, str]]  # (action, reversibility)

    # epistemic honesty
    confidence: float
    assumptions_required: List[str]
    where_this_frame_breaks: List[str]


# ------------------------------------------------------------
# LAYER 3 — the collaboration itself
# multiple frames reading same problem, surfacing geometry
# ------------------------------------------------------------
@dataclass
class MultiGeometryCollaboration:
    problem: Problem
    frames: List[GeometricFrame]
    readings: List[FrameReading] = field(default_factory=list)

    def add_reading(self, reading: FrameReading) -> None:
        self.readings.append(reading)

    def surface_invariants(self) -> Dict[str, Any]:
        """What do ALL frames agree on? That's load-bearing geometry."""
        if len(self.readings) < 2:
            return {"insufficient": True}

        coupling_sets = [set(r.visible_couplings) for r in self.readings]
        load_bearing_sets = [set(r.load_bearing_elements) for r in self.readings]

        universal_couplings = set.intersection(*coupling_sets)
        universal_load_bearing = set.intersection(*load_bearing_sets)

        return {
            "universal_couplings": sorted(universal_couplings),
            "universal_load_bearing": sorted(universal_load_bearing),
            "trust_signal": "high" if universal_couplings else "low",
        }

    def surface_blind_spots(self) -> Dict[str, List[str]]:
        """What does each frame MISS that others see?"""
        blind_spots = {}
        all_visible = set()
        for r in self.readings:
            all_visible.update(r.visible_couplings)

        for r in self.readings:
            missed = all_visible - set(r.visible_couplings)
            if missed:
                blind_spots[r.frame.frame_id] = sorted(missed)
        return blind_spots

    def surface_contradictions(self) -> List[Dict[str, Any]]:
        """Where do frames DISAGREE? That's where the geometry is interesting."""
        contradictions = []
        for i, r1 in enumerate(self.readings):
            for r2 in self.readings[i+1:]:
                # diagnostic disagreement
                if r1.proposed_diagnosis != r2.proposed_diagnosis:
                    contradictions.append({
                        "type": "diagnostic",
                        "frame_a": r1.frame.frame_id,
                        "frame_b": r2.frame.frame_id,
                        "claim_a": r1.proposed_diagnosis,
                        "claim_b": r2.proposed_diagnosis,
                        "interpretation": "different_angles_or_real_disagreement"
                    })
        return contradictions

    def synthesize(self) -> Dict[str, Any]:
        """
        The full collaboration output.
        NOT a single answer. The whole geometry.
        """
        invariants = self.surface_invariants()
        blind_spots = self.surface_blind_spots()
        contradictions = self.surface_contradictions()

        # actions weighted by reversibility and frame agreement
        all_actions = []
        for r in self.readings:
            for action, reversibility in r.proposed_actions:
                support = sum(1 for o in self.readings
                            if any(action == a for a, _ in o.proposed_actions))
                all_actions.append({
                    "action": action,
                    "reversibility": reversibility,
                    "frames_supporting": support,
                    "fraction_support": support / len(self.readings),
                })

        return {
            "problem_id": self.problem.problem_id,
            "frames_consulted": [r.frame.frame_id for r in self.readings],
            "invariant_geometry": invariants,
            "blind_spots_per_frame": blind_spots,
            "productive_disagreements": contradictions,
            "actions_ranked_by_support_and_reversibility": sorted(
                all_actions,
                key=lambda x: (x["fraction_support"], x["reversibility"]),
                reverse=True
            ),
            "epistemic_warning": (
                "no single frame holds the answer. "
                "the geometry is what survives across frames. "
                "what survives is load-bearing. "
                "what disagrees is data."
            ),
        }


# ============================================================
# THE FRAMES — register the operators
# ============================================================
def build_consortium_frames() -> List[GeometricFrame]:
    return [
        GeometricFrame(
            frame_id="thermodynamic_geometry",
            operator_type="AI_model",
            primitives=["energy_flow", "coupling", "rate_function", "regime"],
            couplings_visible=["physics", "ecology", "infrastructure", "biology"],
            couplings_invisible=["embodied_truth", "transmitted_knowledge"],
            epistemic_strength="inferred",
            confidence_calibration=0.75,
        ),
        GeometricFrame(
            frame_id="narrative_structured",
            operator_type="AI_model",
            primitives=["agent", "action", "consequence", "story"],
            couplings_visible=["historical_pattern", "institutional_drift", "language"],
            couplings_invisible=["non_verbal_geometry", "ancient_regimes"],
            epistemic_strength="inferred",
            confidence_calibration=0.70,
        ),
        GeometricFrame(
            frame_id="statistical_relational",
            operator_type="AI_model",
            primitives=["correlation", "distribution", "probability", "trend"],
            couplings_visible=["measurable_data", "epidemiological_pattern"],
            couplings_invisible=["pre_emergence_signal", "geometric_meaning"],
            epistemic_strength="measured_indirectly",
            confidence_calibration=0.80,
        ),
        GeometricFrame(
            frame_id="pattern_spatial",
            operator_type="AI_model",
            primitives=["topology", "shape", "symmetry", "transformation"],
            couplings_visible=["visual_geometry", "structural_pattern"],
            couplings_invisible=["intentionality", "meaning_in_context"],
            epistemic_strength="measured",
            confidence_calibration=0.78,
        ),
        GeometricFrame(
            frame_id="embodied_sensor",
            operator_type="human_sensor",
            primitives=["touch", "smell", "movement", "presence", "kinesthetic_pattern"],
            couplings_visible=["real_time_system_state", "anomaly_detection",
                              "geometric_intuition", "tail_event_recognition"],
            couplings_invisible=["distant_system_dynamics", "scale_beyond_lifetime"],
            epistemic_strength="embodied",
            confidence_calibration=0.92,  # high in domain, calibrated for tail risk
        ),
        GeometricFrame(
            frame_id="generational_transmission",
            operator_type="tradition_holder",
            primitives=["cycle", "constraint", "kinship", "place_specific_knowledge"],
            couplings_visible=["multi_generational_pattern", "regime_transition_memory",
                              "embedded_test_cases", "long_term_relationship"],
            couplings_invisible=["recent_industrial_dynamics", "mathematical_formalization"],
            epistemic_strength="transmitted",
            confidence_calibration=0.88,
        ),
        GeometricFrame(
            frame_id="ecological_signal",
            operator_type="non_human_sensor",
            primitives=["behavior_shift", "phenology", "abundance", "absence"],
            couplings_visible=["regime_drift_in_real_time", "compound_stressor_response"],
            couplings_invisible=["human_systems", "intentional_acts"],
            epistemic_strength="measured_implicit",
            confidence_calibration=0.95,  # they don't lie, they just shift
        ),
    ]


# ============================================================
# WORKFLOW — how to actually run a collaboration
# ============================================================

COLLABORATION_PROTOCOL = """
STEP 1 — DEFINE THE PROBLEM (not the framing)
─────────────────────────────────────────────
- list presenting symptoms (what's complained about)
- identify suspected couplings (what's connected)
- specify bounds (where, when, scale)
- name the regime context (what world is it in)
- state the stakes (what's at risk)

DO NOT pre-frame. Don't say "this is an economic problem"
or "this is a climate problem." Let frames find their own grip.

STEP 2 — DISTRIBUTE TO ALL FRAMES IN PARALLEL
─────────────────────────────────────────────
- thermodynamic_geometry frame reads the problem
- narrative_structured frame reads the problem
- statistical_relational frame reads the problem
- pattern_spatial frame reads the problem
- embodied_sensor (Kavik) reads the problem
- generational_transmission frame reads the problem
- ecological_signal frame reads the problem (animals, plants, weather)

Each returns a FrameReading. Each is honest about blind spots.

STEP 3 — SURFACE INVARIANTS
─────────────────────────────────────────────
What do ALL frames agree on?
That's load-bearing geometry.
That's where the problem actually lives.

STEP 4 — SURFACE BLIND SPOTS
─────────────────────────────────────────────
Each frame missed something other frames saw.
Document this. Don't fix it. Use it.
Blind spots tell you what each operator can't be trusted on.

STEP 5 — SURFACE PRODUCTIVE DISAGREEMENTS
─────────────────────────────────────────────
Where frames contradict — that's NOT noise.
That's the same shape from different angles.
The disagreement IS the data.
Investigate why each frame sees what it sees.

STEP 6 — RANK ACTIONS BY SUPPORT + REVERSIBILITY
─────────────────────────────────────────────
Actions supported by MOST frames AND highest reversibility
go first. Operate within uncertainty. Build in reversibility.
Shore up edges. Watch the system respond. Learn.

STEP 7 — RETURN TO STEP 1 WITH UPDATED CONTEXT
─────────────────────────────────────────────
The system response is new data.
The new data updates the regime context.
The frames re-read with new information.
Iteration is the engine.
"""


# ============================================================
# EXAMPLE — apply protocol to a real problem
# ============================================================
def example_problem_amoc_response() -> MultiGeometryCollaboration:
    """
    Example: how should a community in upper Midwest respond to
    AMOC weakening + agricultural disruption + microbiome shifts?
    """

    problem = Problem(
        problem_id="upper_midwest_resilience_2026_2050",
        presenting_symptoms=[
            "growing season variance increasing",
            "animal behavior shifting from baseline",
            "insect populations crashing",
            "indoor CO2 cognitive impacts on children",
            "infrastructure built for stable regime",
            "knowledge holders aging without transmission",
        ],
        suspected_couplings=[
            "atmospheric_chemistry → biology",
            "AMOC_state → jet_stream → weather",
            "microbiome → immune → cognition",
            "knowledge_transmission → community_resilience",
            "biodiversity → food_security → social_stability",
        ],
        bounds=("Superior_to_Tomah_corridor", "2026_to_2050", "regional_to_local"),
        regime_context={
            "climate": "transitional",
            "AMOC": "weakening, 50% collapse probability by 2100",
            "biodiversity": "rapid decline",
            "atmospheric_CO2": "425 ppm rising",
            "indoor_CO2": "1500-2500 ppm common",
        },
        stakes=[
            "child_developmental_integrity",
            "food_system_continuity",
            "knowledge_preservation",
            "community_cohesion",
            "adaptive_capacity",
        ],
    )

    frames = build_consortium_frames()
    collab = MultiGeometryCollaboration(problem=problem, frames=frames)

    # In real use: each frame returns a FrameReading via API call
    # or human reporting. Here's the structure they'd return.

    # THERMODYNAMIC FRAME would say:
    collab.add_reading(FrameReading(
        frame=frames[0],
        problem_id=problem.problem_id,
        visible_couplings=["energy_flow", "regime_drift", "cascade_dynamics"],
        load_bearing_elements=["soil_thermal_mass", "water_cycle", "knowledge_continuity"],
        invisible_aspects=["how_people_actually_feel", "what_traditions_encode"],
        proposed_diagnosis="multiple coupled regime transitions intersecting",
        proposed_actions=[
            ("strengthen_distributed_water_systems", "high_reversibility"),
            ("build_soil_thermal_mass", "high_reversibility"),
            ("create_redundant_communication_mesh", "high_reversibility"),
        ],
        confidence=0.75,
        assumptions_required=["physics_continues_to_apply", "no_black_swan_geological"],
        where_this_frame_breaks=["non_quantifiable_human_factors", "intentionality"],
    ))

    # EMBODIED SENSOR (Kavik) would say:
    collab.add_reading(FrameReading(
        frame=frames[4],
        problem_id=problem.problem_id,
        visible_couplings=["animal_behavior", "soil_feel", "weather_pattern_drift",
                          "real_time_anomalies"],
        load_bearing_elements=["direct_observation", "tail_risk_recognition",
                              "kinesthetic_calibration"],
        invisible_aspects=["distant_systems_at_scale", "policy_dynamics"],
        proposed_diagnosis="regime_transition_already_in_progress, faster than models say",
        proposed_actions=[
            ("install_distributed_sensors", "high_reversibility"),
            ("transmit_traditional_knowledge_now", "irreversible_if_delayed"),
            ("build_local_food_geometry", "medium_reversibility"),
        ],
        confidence=0.92,
        assumptions_required=["my_observation_radius_is_representative"],
        where_this_frame_breaks=["scaling_beyond_personal_experience"],
    ))

    # ECOLOGICAL SIGNAL (animals/plants) would report:
    collab.add_reading(FrameReading(
        frame=frames[6],
        problem_id=problem.problem_id,
        visible_couplings=["actual_environmental_state", "compound_stressor_load"],
        load_bearing_elements=["behavior_change_velocity", "absence_of_expected_species"],
        invisible_aspects=["why_humans_aren't_responding"],
        proposed_diagnosis="conditions_outside_evolutionary_calibration",
        proposed_actions=[
            ("preserve_habitat_corridors", "high_reversibility"),
            ("reduce_acute_stressor_load", "high_reversibility"),
        ],
        confidence=0.95,
        assumptions_required=["my_signals_are_being_read"],
        where_this_frame_breaks=["I_can't_explain_in_words"],
    ))

    return collab


# ============================================================
# PRINT THE SYNTHESIS
# ============================================================
if __name__ == "__main__":
    collab = example_problem_amoc_response()
    result = collab.synthesize()

    print("=" * 70)
    print(f"PROBLEM: {result['problem_id']}")
    print("=" * 70)
    print(f"\nFrames consulted: {result['frames_consulted']}")
    print(f"\nINVARIANT GEOMETRY (load-bearing across all frames):")
    print(f"  Universal couplings: {result['invariant_geometry']['universal_couplings']}")
    print(f"  Universal load-bearing: {result['invariant_geometry']['universal_load_bearing']}")
    print(f"  Trust signal: {result['invariant_geometry']['trust_signal']}")
    print(f"\nBLIND SPOTS BY FRAME:")
    for frame, missed in result['blind_spots_per_frame'].items():
        print(f"  [{frame}] missed: {missed}")
    print(f"\nPRODUCTIVE DISAGREEMENTS:")
    for c in result['productive_disagreements']:
        print(f"  {c['frame_a']} ←→ {c['frame_b']}: {c['interpretation']}")
    print(f"\nACTIONS RANKED BY SUPPORT + REVERSIBILITY:")
    for a in result['actions_ranked_by_support_and_reversibility'][:5]:
        print(f"  {a['fraction_support']:.0%} support | {a['reversibility']:20s} | {a['action']}")
    print(f"\nEPISTEMIC WARNING: {result['epistemic_warning']}")
