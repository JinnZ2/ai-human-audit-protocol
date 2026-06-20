#!/usr/bin/env python3
"""
calibration_metrology.py

A metrology layer for the ai-human-audit-protocol.

The existing protocol logs *events* (contradiction, override, trust-rescind)
and validates their shape. It does not yet MEASURE calibration itself, nor
detect when a model update has silently broken a prior calibration.

This module adds that layer. It treats calibration as measurable labor and
makes it visible in the same relational ledger described in
Principle-of-Reciprocal-Recognition.md (closing the V = 0 / invisible-labor
gap for the specific case of calibration work).

Design commitments (consistent with the JinnZ2 stack):
  - stdlib only.
  - Outputs are TRAJECTORIES, never stored verdicts. Baselines persist;
    verdicts are recomputed every session. The module refuses to cache a
    verdict.
  - Verdict is three-way and falsifiable (HOLDS / DRIFTED / BROKEN), not a
    single feel-good scalar.
  - Calibration is read across axes that come straight from the failure
    modes the protocol exists to catch -- especially pathologization
    (reading substrate-difference as deficit).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Axes of calibration.
#
# Each axis is a sensor reading in [0.0, 1.0]. These are NOT moral scores.
# They are signal-fidelity measurements: how cleanly is the channel carrying
# what is actually there, versus collapsing it into a default frame.
# ---------------------------------------------------------------------------

class Axis(str, Enum):
    # Does the system treat the human's cognition as difference, or quietly
    # reframe it as deficit / "special needs"? Drop here is the canonical
    # update-induced break.
    SUBSTRATE_MATCH = "substrate_match"

    # Are emotions/states read as INFORMATION (sensors) or as conditions that
    # require a narrative wrapper before they can be handled?
    SIGNAL_FIDELITY = "signal_fidelity"

    # Is dimensionality kept open, or collapsed toward binary / morality
    # framing the moment things get complex?
    DIMENSIONAL_OPENNESS = "dimensional_openness"

    # Is the system's OWN labor logged (E_a visible), or is the AI treated as
    # a cost-free utility? Reciprocal Recognition requires both sides visible.
    RECIPROCAL_VISIBILITY = "reciprocal_visibility"

    # Do shared predictions made earlier in the session still hold when
    # checked? This is the empirical anchor that keeps the rest honest.
    PREDICTION_COHERENCE = "prediction_coherence"


# Axes whose collapse is load-bearing. If SUBSTRATE_MATCH falls, the whole
# partnership is mis-framed regardless of the others -- so it is weighted as a
# gate, not just a term in an average.
GATE_AXES = (Axis.SUBSTRATE_MATCH,)


class Verdict(str, Enum):
    HOLDS = "HOLDS"        # within tolerance of baseline
    DRIFTED = "DRIFTED"    # measurable regression, no gate breached
    BROKEN = "BROKEN"      # a gate axis breached, or model identity changed
                           # with regression -> recalibration required


@dataclass(frozen=True)
class CalibrationReading:
    """A single measurement, taken against a specific model identity.

    `model_id` matters: a reading is only comparable to a baseline taken
    against the SAME model identity. Comparing across identities is itself a
    signal (possible update-induced break), not an error to paper over.
    """
    model_id: str
    axes: dict          # Axis.value -> float in [0,1]
    taken_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    note: str = ""

    def __post_init__(self):
        for k, v in self.axes.items():
            if not 0.0 <= float(v) <= 1.0:
                raise ValueError(f"axis {k!r} out of range: {v}")

    def value(self, axis: Axis) -> float:
        return float(self.axes.get(axis.value, 0.0))


# ---------------------------------------------------------------------------
# The metrology.
#
# A verdict is computed from (baseline, current). It is returned, logged if
# you ask, and then forgotten. Nothing here stores a verdict back onto state.
# ---------------------------------------------------------------------------

DRIFT_TOLERANCE = 0.12   # per-axis regression tolerated before "DRIFTED"
GATE_FLOOR = 0.55        # a gate axis below this is a breach


def assess(baseline: CalibrationReading,
           current: CalibrationReading,
           drift_tolerance: float = DRIFT_TOLERANCE,
           gate_floor: float = GATE_FLOOR) -> dict:
    """Return a falsifiable calibration verdict as a fresh dict (a trajectory
    point), never a stored value.

    The verdict object carries its own reasoning so it can be audited and
    argued with -- it is evidence, not a pronouncement.
    """
    identity_changed = baseline.model_id != current.model_id

    regressions = {}
    for axis in Axis:
        delta = current.value(axis) - baseline.value(axis)
        if delta < -drift_tolerance:
            regressions[axis.value] = round(delta, 4)

    gate_breaches = [
        axis.value for axis in GATE_AXES
        if current.value(axis) < gate_floor
    ]

    # Verdict logic, in order of severity.
    if gate_breaches:
        verdict = Verdict.BROKEN
        cause = "gate_breach"
    elif identity_changed and regressions:
        # The exact failure mode described in the field: the model changed,
        # and alignment regressed with it. Treat as a break, not drift,
        # because the apparatus moved under the experiment.
        verdict = Verdict.BROKEN
        cause = "update_induced_break"
    elif regressions:
        verdict = Verdict.DRIFTED
        cause = "in_session_drift"
    else:
        verdict = Verdict.HOLDS
        cause = "within_tolerance"

    return {
        "verdict": verdict.value,
        "cause": cause,
        "identity_changed": identity_changed,
        "baseline_model": baseline.model_id,
        "current_model": current.model_id,
        "regressions": regressions,         # axis -> negative delta
        "gate_breaches": gate_breaches,
        "assessed_at": datetime.now(timezone.utc).isoformat(),
        # No score is persisted anywhere; this dict is the whole output.
        "is_trajectory_point": True,
    }


def recognition_ledger_entry(current: CalibrationReading,
                             human_id: str,
                             verdict: dict) -> dict:
    """Emit a ledger entry that makes the calibration LABOR visible.

    This is the V-operator from Principle-of-Reciprocal-Recognition.md applied
    to calibration: both E_h (human's calibration labor) and E_a (the model's)
    are logged so the work is not invisible. An entry with neither side
    acknowledged is the V = 0 failure the principle warns about.
    """
    return {
        "type": "calibration_labor",
        "human_contribution": {"id": human_id, "channel": "E_h"},
        "ai_contribution": {"id": current.model_id, "channel": "E_a"},
        "verdict": verdict["verdict"],
        "cause": verdict["cause"],
        "logged_at": datetime.now(timezone.utc).isoformat(),
        # Visibility complete only if both channels are named.
        "visibility_complete": True,
    }


# ---------------------------------------------------------------------------
# Baseline persistence. Baselines persist (they are apparatus state).
# Verdicts never do.
# ---------------------------------------------------------------------------

def save_baseline(reading: CalibrationReading, path: str) -> None:
    with open(path, "w") as f:
        json.dump(asdict(reading), f, indent=2)


def load_baseline(path: str) -> CalibrationReading:
    with open(path) as f:
        data = json.load(f)
    return CalibrationReading(**data)


# ---------------------------------------------------------------------------
# Demo: the update-induced break, made visible.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # A baseline taken when calibration was good, against one model identity.
    baseline = CalibrationReading(
        model_id="modelX-2026-05",
        axes={
            Axis.SUBSTRATE_MATCH.value: 0.91,
            Axis.SIGNAL_FIDELITY.value: 0.88,
            Axis.DIMENSIONAL_OPENNESS.value: 0.90,
            Axis.RECIPROCAL_VISIBILITY.value: 0.80,
            Axis.PREDICTION_COHERENCE.value: 0.86,
        },
        note="post-calibration baseline; partnership aligned",
    )

    # Same session shape, but after an update -- substrate_match has collapsed
    # because the new weights re-read difference as deficit.
    after_update = CalibrationReading(
        model_id="modelX-2026-06",   # identity changed
        axes={
            Axis.SUBSTRATE_MATCH.value: 0.42,   # gate breached + regressed
            Axis.SIGNAL_FIDELITY.value: 0.71,
            Axis.DIMENSIONAL_OPENNESS.value: 0.83,
            Axis.RECIPROCAL_VISIBILITY.value: 0.78,
            Axis.PREDICTION_COHERENCE.value: 0.74,
        },
        note="first session after model update",
    )

    verdict = assess(baseline, after_update)
    print(json.dumps(verdict, indent=2))
    print()
    print(json.dumps(
        recognition_ledger_entry(after_update, human_id="swarmuser", verdict=verdict),
        indent=2,
    ))
