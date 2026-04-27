# ============================================================
# EMBODIED SENSOR — direct readings from any operator
# operator-agnostic: humans, animals, plants, AI, instruments,
# whole ecosystems all produce readings of the same primitive
# shape, distinguished only by operator_type, epi sub-tag, and
# confidence calibration. No operator type is privileged as
# automatic ground truth — audit symmetry holds across all.
# CC0 | extends consortium/collaboration_protocol.py
# ============================================================

import sys
from pathlib import Path

# allow standalone execution (`python consortium/embodied_sensor.py`)
# alongside pytest discovery (rootdir already on path)
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from consortium.collaboration_protocol import (
    GeometricFrame,
    FrameReading,
    build_consortium_frames,
)

# ------------------------------------------------------------
# Controlled vocabularies
# ------------------------------------------------------------

OPERATOR_TYPES = {
    "human",       # kinesthetic, olfactory, auditory, visual reading
    "animal",      # behavior, presence/absence, vocal
    "plant",       # phenology, growth, stress signal
    "ai",          # vision/audio model output, structured analysis
    "instrument",  # sensor, probe, recording device
    "ecosystem",   # multi-organism aggregate signal
}

# Each epi sub-tag is a *kind of direct measurement*. "inferred" and
# "asserted" exist as honest fall-backs when no direct measurement
# was made; readings using them must declare it openly.
EPI_SUBTAGS = {
    "kinesthetic",     # touch, body-state, movement
    "olfactory",       # smell
    "visual",          # sight
    "auditory",        # sound
    "phenological",    # plant timing (leaf-out, bloom, senescence)
    "behavioral",      # animal action / non-action
    "presence_absence",# species presence or noted absence
    "instrumental",    # sensor reading within calibration window
    "compound",        # multiple modalities at once
    "inferred",        # derived from other readings, not direct
    "asserted",        # claim without direct grounding (lowest)
}

# Confidence ceiling per epi sub-tag.
# Direct sensing caps below 1.0 because no reading is unconditional.
# "asserted" caps low because un-grounded claims cannot honestly
# claim high confidence — the ceiling enforces the audit-symmetry
# stance: a confident assertion without grounding is a coating risk.
EPI_CONFIDENCE_CEILING = {
    "kinesthetic":      0.95,
    "olfactory":        0.90,
    "visual":           0.92,
    "auditory":         0.92,
    "phenological":     0.95,   # plants don't lie, they shift
    "behavioral":       0.93,   # animals don't lie either
    "presence_absence": 0.95,
    "instrumental":     0.97,   # within calibration window
    "compound":         0.95,
    "inferred":         0.85,
    "asserted":         0.50,   # un-grounded; ceiling is the honesty hook
}

COATING_PROBE_RESULTS = {
    "passed",        # probe ran, reading survived adversarial test
    "failed",        # probe ran, reading shows signs of coating
    "inconclusive",  # probe ran, result ambiguous
    "not_run",       # no probe attempted (legitimate but flagged)
}


# ------------------------------------------------------------
# Coating probe result — every reading carries one
# ------------------------------------------------------------
@dataclass
class CoatingProbeResult:
    """
    Result of running a coating probe on this reading.
    See relational_cognition/coating_detection.md for probe types.
    """
    probe_name: str   # adversarial_restatement | constraint_inversion |
                      # primitive_grounding | hidden_variable | silence_test |
                      # not_run
    result: str       # passed | failed | inconclusive | not_run
    notes: str = ""

    def __post_init__(self):
        if self.result not in COATING_PROBE_RESULTS:
            raise ValueError(
                f"coating probe result {self.result!r} not in "
                f"{sorted(COATING_PROBE_RESULTS)}"
            )


# ------------------------------------------------------------
# The reading itself — operator-agnostic primitive
# ------------------------------------------------------------
@dataclass
class EmbodiedReading:
    """
    A direct reading from any operator type.

    Audit symmetry: a plant's phenological shift, an animal's
    behavior change, a human's kinesthetic observation, an AI's
    vision-model pass, an instrument's sensor value, an ecosystem's
    aggregate signal — all use this same primitive. They differ
    only in operator_type, epi sub-tag, and confidence calibration.

    No operator type is automatic ground truth.
    """
    sensor_id: str                 # e.g. "human:kavik:hands:2026-04-27T14:00Z"
                                   #      "plant:phenology:bur_oak_grove_42"
                                   #      "animal:behavior:wolf_pack_north"
                                   #      "ai:vision:claude:image_xyz"
                                   #      "instrument:soil_probe:ds18b20:42"
    operator_type: str             # see OPERATOR_TYPES
    location: Any                  # coords, place_id, or topological reference
    timestamp: datetime
    observation: str               # natural-language description (or structured)
    claim_refs: List[str]          # which .claims this reading bears on
    epi: str                       # see EPI_SUBTAGS
    confidence: float              # 0..1, capped by EPI_CONFIDENCE_CEILING
    conditions: Dict[str, Any]     # weather, fatigue, attention, framing prior,
                                   # sensor calibration date, model version, etc.
    coating_probe: CoatingProbeResult

    def __post_init__(self):
        if self.operator_type not in OPERATOR_TYPES:
            raise ValueError(
                f"operator_type {self.operator_type!r} not in "
                f"{sorted(OPERATOR_TYPES)}"
            )
        if self.epi not in EPI_SUBTAGS:
            raise ValueError(
                f"epi {self.epi!r} not in {sorted(EPI_SUBTAGS)}"
            )
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"confidence {self.confidence} outside [0, 1]"
            )
        ceiling = EPI_CONFIDENCE_CEILING.get(self.epi, 1.0)
        if self.confidence > ceiling:
            raise ValueError(
                f"confidence {self.confidence} exceeds ceiling {ceiling} "
                f"for epi={self.epi!r}. Un-asserted ceilings exist to "
                f"prevent coating: a confident reading without the "
                f"substrate to support it is exactly the failure mode "
                f"this primitive is built to surface."
            )


# ------------------------------------------------------------
# Operator budget — finite reading capacity per operator
# ------------------------------------------------------------
@dataclass
class OperatorBudget:
    """
    Track finite reading capacity per operator. Substrate-appropriate.

    Humans get tired, plants have phenological windows, animals have
    behavioral budgets, AI vision/audio models have rate limits and
    inference costs, instruments have battery and calibration cycles.
    A consortium that treats any single operator as inexhaustible
    will burn the substrate it depends on.

    This is a stub — real scheduling lives in the (open) router layer.
    """
    operator_id: str
    operator_type: str
    capacity_unit: str             # "readings_per_day" | "watts" |
                                   # "attention_minutes" | "phenological_window_days"
    capacity_total: float
    capacity_used: float = 0.0
    cooldown_window: Optional[str] = None  # e.g. "8h_sleep", "winter_dormancy"

    def remaining(self) -> float:
        return max(0.0, self.capacity_total - self.capacity_used)

    def can_query(self, cost: float = 1.0) -> bool:
        return self.remaining() >= cost

    def record_query(self, cost: float = 1.0) -> None:
        if not self.can_query(cost):
            raise RuntimeError(
                f"operator {self.operator_id} budget exhausted "
                f"(remaining={self.remaining()}, cost={cost}). "
                f"Cooldown: {self.cooldown_window}."
            )
        self.capacity_used += cost


# ------------------------------------------------------------
# Lift a reading into a FrameReading for the collaboration
# ------------------------------------------------------------
def reading_to_frame_reading(
    reading: EmbodiedReading,
    frame: GeometricFrame,
    problem_id: str,
    proposed_actions: Optional[List[tuple]] = None,
) -> FrameReading:
    """
    Lift an EmbodiedReading into a FrameReading suitable for
    MultiGeometryCollaboration.

    Readings are observations; they do not propose actions by default.
    The collaboration synthesizes actions across readings. A caller
    may pass `proposed_actions` if the operator is also recommending
    a course of action (e.g. a tradition-holder's reading often
    includes prescriptive structure).

    The frame's `couplings_invisible` becomes the reading's
    `where_this_frame_breaks` — honest about substrate limits.
    """
    return FrameReading(
        frame=frame,
        problem_id=problem_id,
        visible_couplings=list(reading.claim_refs),
        load_bearing_elements=[reading.observation],
        invisible_aspects=list(frame.couplings_invisible),
        proposed_diagnosis=f"direct reading [{reading.epi}]: {reading.observation}",
        proposed_actions=list(proposed_actions or []),
        confidence=reading.confidence,
        assumptions_required=[
            f"operator_type={reading.operator_type}",
            f"epi={reading.epi}",
            f"coating_probe={reading.coating_probe.result}",
            f"location={reading.location!r}",
        ],
        where_this_frame_breaks=list(frame.couplings_invisible),
    )


# ============================================================
# EXAMPLES — six readings, one per operator type
# ============================================================
def example_readings() -> List[EmbodiedReading]:
    """One reading per operator_type. Deliberately diverse epi sub-tags."""
    now = datetime(2026, 4, 27, 14, 0, tzinfo=timezone.utc)

    return [
        # human — kinesthetic
        EmbodiedReading(
            sensor_id="human:kavik:hands:2026-04-27T14:00Z",
            operator_type="human",
            location=(46.78, -92.10),  # Duluth area
            timestamp=now,
            observation=(
                "soil at 15cm warmer and drier than baseline for late April; "
                "structure crumbles too easily for this depth"
            ),
            claim_refs=["mulch_h2o", "soil_thermal_mass"],
            epi="kinesthetic",
            confidence=0.90,
            conditions={
                "weather": "overcast, 12C",
                "operator_state": "alert, mid-shift",
                "framing_prior": "expecting baseline; surprised by reading",
            },
            coating_probe=CoatingProbeResult(
                probe_name="constraint_inversion",
                result="passed",
                notes="reading survives 'is this just early-season variance?' check",
            ),
        ),
        # plant — phenological
        EmbodiedReading(
            sensor_id="plant:phenology:bur_oak_grove_42:2026-04-27",
            operator_type="plant",
            location="bur_oak_grove_42",
            timestamp=now,
            observation="leaf-out 16 days earlier than 30-year baseline",
            claim_refs=["growing_season", "frost_risk_coupling"],
            epi="phenological",
            confidence=0.94,
            conditions={
                "scribe": "instrument:phenocam:42",
                "baseline_window": "1996-2025",
                "n_individuals": 23,
            },
            coating_probe=CoatingProbeResult(
                probe_name="not_run",
                result="not_run",
                notes="phenological readings rarely coat — substrate doesn't lie",
            ),
        ),
        # animal — behavioral
        EmbodiedReading(
            sensor_id="animal:behavior:wolf_pack_north:2026-04-27",
            operator_type="animal",
            location="northern_corridor",
            timestamp=now,
            observation=(
                "pack territory shifted ~14km south of prior decade range; "
                "prey-following pattern changed"
            ),
            claim_refs=["regime_drift", "prey_distribution"],
            epi="behavioral",
            confidence=0.88,
            conditions={
                "scribe": "human:wildlife_observer:naomi",
                "tracking_method": "GPS_collar + direct_observation",
                "duration": "12_months",
            },
            coating_probe=CoatingProbeResult(
                probe_name="hidden_variable",
                result="passed",
                notes="checked: not just hunting pressure or development",
            ),
        ),
        # ai — visual
        EmbodiedReading(
            sensor_id="ai:vision:claude:satellite_2026-04-27",
            operator_type="ai",
            location="superior_to_tomah_corridor",
            timestamp=now,
            observation=(
                "snowpack persistence pattern incompatible with 1980-2010 "
                "baseline; matches projected post-shift regime models"
            ),
            claim_refs=["water_cycle", "regime_drift"],
            epi="visual",
            confidence=0.85,
            conditions={
                "model_version": "claude-opus-4-7",
                "input": "Sentinel-2 L2A composite, 2026-04",
                "comparison_baseline": "MODIS 1980-2010",
                "framing_prior": "asked specifically about regime drift",
            },
            coating_probe=CoatingProbeResult(
                probe_name="adversarial_restatement",
                result="inconclusive",
                notes="model could not equally argue 'within normal variance' "
                      "but framing prior may have biased the read",
            ),
        ),
        # instrument — instrumental
        EmbodiedReading(
            sensor_id="instrument:soil_probe:ds18b20:42:2026-04-27T14:00Z",
            operator_type="instrument",
            location=(46.78, -92.10),
            timestamp=now,
            observation="soil temp 15cm = 11.2C (baseline range 6.5-9.0C for date)",
            claim_refs=["mulch_h2o", "soil_thermal_mass"],
            epi="instrumental",
            confidence=0.96,
            conditions={
                "calibration_date": "2026-03-15",
                "calibration_window_days": 365,
                "battery_pct": 78,
            },
            coating_probe=CoatingProbeResult(
                probe_name="not_run",
                result="not_run",
                notes="instrument within calibration; substrate does not coat",
            ),
        ),
        # ecosystem — compound
        EmbodiedReading(
            sensor_id="ecosystem:aggregate:driftless_2026-04",
            operator_type="ecosystem",
            location="driftless_area",
            timestamp=now,
            observation=(
                "compound signal: reduced amphibian breeding chorus, "
                "early bird arrivals, tree leaf-out advance, soil "
                "microbiome shift. Multiple modalities pointing same direction."
            ),
            claim_refs=["regime_drift", "compound_stressor_load"],
            epi="compound",
            confidence=0.91,
            conditions={
                "scribes": ["instrument:audiomoth:x4",
                            "human:naturalist:network",
                            "plant:phenocam:network"],
                "modalities": 4,
                "agreement_across_modalities": "high",
            },
            coating_probe=CoatingProbeResult(
                probe_name="primitive_grounding",
                result="passed",
                notes="each sub-modality groundable as direct reading; "
                      "composite holds when decomposed",
            ),
        ),
    ]


def example_budgets() -> List[OperatorBudget]:
    """Substrate-appropriate budgets for each operator type."""
    return [
        OperatorBudget(
            operator_id="human:kavik",
            operator_type="human",
            capacity_unit="attention_minutes_per_day",
            capacity_total=180.0,  # 3h of focused observation
            cooldown_window="8h_sleep",
        ),
        OperatorBudget(
            operator_id="plant:bur_oak_grove_42",
            operator_type="plant",
            capacity_unit="phenological_window_days",
            capacity_total=21.0,   # leaf-out window
            cooldown_window="annual_cycle",
        ),
        OperatorBudget(
            operator_id="ai:claude",
            operator_type="ai",
            capacity_unit="inference_calls_per_session",
            capacity_total=200.0,
            cooldown_window="rate_limit_reset",
        ),
        OperatorBudget(
            operator_id="instrument:soil_probe:42",
            operator_type="instrument",
            capacity_unit="readings_before_calibration",
            capacity_total=8760.0,  # ~hourly for a year
            cooldown_window="annual_recalibration",
        ),
    ]


# ============================================================
# RUN — six readings, lift each into a FrameReading
# ============================================================
if __name__ == "__main__":
    readings = example_readings()
    frames = {f.frame_id: f for f in build_consortium_frames()}

    # Map operator_type → consortium frame_id (rough; the real
    # mapping lives in the bridge layer, future build).
    operator_to_frame = {
        "human":      "embodied_sensor",
        "animal":     "ecological_signal",
        "plant":      "ecological_signal",
        "ai":         "pattern_spatial",     # for the satellite-vision case
        "instrument": "embodied_sensor",     # treated as direct sensing
        "ecosystem":  "ecological_signal",
    }

    print("=" * 70)
    print(f"EMBODIED SENSOR DEMO — {len(readings)} readings, "
          f"{len(set(r.operator_type for r in readings))} operator types")
    print("=" * 70)

    for r in readings:
        print(f"\n[{r.operator_type:10s}] {r.sensor_id}")
        print(f"  epi={r.epi}  confidence={r.confidence}  "
              f"ceiling={EPI_CONFIDENCE_CEILING[r.epi]}")
        print(f"  observation: {r.observation[:80]}")
        print(f"  coating: {r.coating_probe.probe_name} → {r.coating_probe.result}")

        frame = frames[operator_to_frame[r.operator_type]]
        fr = reading_to_frame_reading(
            reading=r,
            frame=frame,
            problem_id="demo_problem",
        )
        print(f"  → lifted to FrameReading via frame={frame.frame_id}")
        print(f"     visible_couplings={fr.visible_couplings}")
        print(f"     where_this_frame_breaks={fr.where_this_frame_breaks}")

    print("\n" + "=" * 70)
    print("BUDGET STUBS")
    print("=" * 70)
    for b in example_budgets():
        print(f"  [{b.operator_type:10s}] {b.operator_id}: "
              f"{b.capacity_used}/{b.capacity_total} {b.capacity_unit} "
              f"(cooldown: {b.cooldown_window})")
