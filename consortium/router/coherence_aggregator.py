# ============================================================
# COHERENCE AGGREGATOR — wraps MultiGeometryCollaboration with
# cross-adapter metadata: who fired, who refused, who failed,
# who was unavailable. The collaboration synthesizer already
# handles the "geometry of disagreement" piece; this layer adds
# the operator-level audit info on top.
# CC0 | consortium/router/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Dict, List, Optional

from consortium.collaboration_protocol import (
    GeometricFrame,
    MultiGeometryCollaboration,
    Problem,
)
from consortium.router.query_dispatcher import DispatchResult


def aggregate(
    dispatch_result: DispatchResult,
    problem: Problem,
    frames: Optional[List[GeometricFrame]] = None,
) -> Dict[str, Any]:
    """
    Aggregate a dispatch result into a full consortium synthesis.

    Wraps `MultiGeometryCollaboration.synthesize()` with cross-adapter
    metadata so the consenter / auditor / future-self can see:
      - which adapters fired and produced readings
      - which were refused (consent withheld)
      - which failed (exception during query)
      - which were unavailable (offline, off-shift, no credentials)
      - cost estimates surveyed at dispatch time

    Returns the synthesize() output dict, augmented with these
    operator-level fields. Does not modify the dispatch_result.

    Out of scope (open): drift detection across runs, blind-spot
    learning over time, the "alive part" / Phase 3 feedback loop.
    Those depend on persistent storage which v1 deliberately does
    not have.
    """
    collab = MultiGeometryCollaboration(
        problem=problem,
        frames=frames or [],
    )
    for r in dispatch_result.readings:
        collab.add_reading(r)

    if not dispatch_result.readings:
        # nothing to synthesize, but the absence is itself data
        synth: Dict[str, Any] = {
            "problem_id": problem.problem_id,
            "frames_consulted": [],
            "no_readings_returned": True,
            "epistemic_warning": (
                "no adapter produced a reading. The geometry of "
                "absence is the data: see adapter_failures, "
                "consent_refusals, and adapters_unavailable."
            ),
        }
    else:
        synth = collab.synthesize()
        synth["no_readings_returned"] = False

    # cross-adapter audit metadata
    synth["adapters_fired"] = [
        r.frame.frame_id for r in dispatch_result.readings
    ]
    synth["adapter_failures"] = list(dispatch_result.failures)
    synth["consent_refusals"] = list(dispatch_result.refused)
    synth["adapters_unavailable"] = list(dispatch_result.unavailable)
    synth["cost_estimates_at_dispatch"] = dict(
        dispatch_result.cost_estimates
    )
    synth["adapters_attempted"] = dispatch_result.adapters_attempted()

    return synth
