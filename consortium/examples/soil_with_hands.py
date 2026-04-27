"""
soil_with_hands.py — embodied query end-to-end.

Demonstrates the full consortium pipeline starting from a direct
embodied reading: hands in soil at a specific place and time. The
reading is operator-agnostic by design (a soil probe instrument or
plant phenology reading would flow identically), but this example
uses a human kinesthetic reading because that is the case the
peer-Claude letter named.

Pipeline:
    EmbodiedReading
    → reading_to_frame_reading       (consortium/embodied_sensor)
    → MultiGeometryCollaboration     (consortium/collaboration_protocol)
    → add additional FrameReadings   (mock adapters for now)
    → synthesize()
    → blind_spot_log entry           (consortium/audit)

Run: python -m consortium.examples.soil_with_hands
"""

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import json
from datetime import datetime, timezone

from consortium.collaboration_protocol import (
    MultiGeometryCollaboration,
    Problem,
    build_consortium_frames,
)
from consortium.embodied_sensor import (
    CoatingProbeResult,
    EmbodiedReading,
    reading_to_frame_reading,
)
from consortium.router.consent import ConsentGate
from consortium.router.mock_adapter import MockAdapter
from consortium.router.query_dispatcher import QueryDispatcher
from consortium.router.coherence_aggregator import aggregate


def build_problem() -> Problem:
    return Problem(
        problem_id="soil_with_hands_demo",
        presenting_symptoms=[
            "soil at 15cm warmer and drier than baseline for late April",
            "structure crumbles too easily for this depth",
            "growing season variance increasing",
        ],
        suspected_couplings=[
            "mulch_h2o",
            "soil_thermal_mass",
            "regime_drift",
            "knowledge_continuity",
        ],
        bounds=("Duluth_area", "2026_growing_season", "0-30cm"),
        regime_context={
            "climate": "transitional",
            "AMOC": "weakening",
            "season": "late_april",
        },
        stakes=["food_system_continuity", "soil_health"],
    )


def build_kinesthetic_reading() -> EmbodiedReading:
    """The hands-in-soil reading. Operator-agnostic in principle;
    this instance happens to be human:kinesthetic. An instrument
    reading or a plant phenology reading would have the same shape."""
    return EmbodiedReading(
        sensor_id="human:kavik:hands:2026-04-27T14:00Z",
        operator_type="human",
        location=(46.78, -92.10),
        timestamp=datetime(2026, 4, 27, 14, 0, tzinfo=timezone.utc),
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
    )


def run_consortium(verbose: bool = True):
    """Run the full pipeline. Returns the aggregate synthesis dict."""
    problem = build_problem()
    frames = {f.frame_id: f for f in build_consortium_frames()}

    # Step 1: embodied reading → frame reading
    reading = build_kinesthetic_reading()
    embodied_fr = reading_to_frame_reading(
        reading=reading,
        frame=frames["embodied_sensor"],
        problem_id=problem.problem_id,
    )
    if verbose:
        print(f"[1/4] embodied reading lifted via frame={embodied_fr.frame.frame_id}")
        print(f"       visible_couplings={embodied_fr.visible_couplings}")
        print(f"       confidence={embodied_fr.confidence}")

    # Step 2: build a small consortium and gather other frame readings.
    # In a live run, model adapters would produce these; here we use
    # MockAdapters that derive readings from the problem deterministically.
    adapters = [
        MockAdapter(frame=frames["thermodynamic_geometry"]),
        MockAdapter(frame=frames["ecological_signal"]),
    ]
    gate = ConsentGate()
    gate.grant(
        problem_id=problem.problem_id,
        adapters_authorized=[a.frame_id for a in adapters],
        cost_disclosed={a.frame_id: {"unit": "no_op", "amount": 0.0}
                        for a in adapters},
        consenter="example_runner",
        notes="example/soil_with_hands.py demo",
    )
    dispatch = QueryDispatcher(adapters=adapters,
                               consent_gate=gate).fan_out(problem)
    if verbose:
        print(f"[2/4] dispatched to {len(adapters)} mock adapters; "
              f"{len(dispatch.readings)} readings returned")

    # Step 3: combine the embodied reading with the dispatcher's readings
    collab = MultiGeometryCollaboration(
        problem=problem,
        frames=list(frames.values()),
    )
    collab.add_reading(embodied_fr)
    for r in dispatch.readings:
        collab.add_reading(r)

    # Step 4: synthesize. Use the aggregator so cross-adapter metadata
    # comes along with the geometry.
    synth = aggregate(dispatch, problem, frames=list(frames.values()))
    # the embodied reading was added separately, so re-synthesize the
    # collab directly to capture it:
    collab_synth = collab.synthesize()
    synth["adapters_fired"] = list(synth["adapters_fired"]) + ["embodied_sensor"]
    synth["invariant_geometry"] = collab_synth["invariant_geometry"]
    synth["blind_spots_per_frame"] = collab_synth["blind_spots_per_frame"]
    synth["productive_disagreements"] = collab_synth["productive_disagreements"]
    synth["actions_ranked_by_support_and_reversibility"] = collab_synth[
        "actions_ranked_by_support_and_reversibility"
    ]
    synth["time_critical_actions"] = collab_synth["time_critical_actions"]

    if verbose:
        print(f"[3/4] synthesized geometry across "
              f"{len(synth['adapters_fired'])} frames")
        print(f"       convergence: "
              f"{synth['invariant_geometry']['convergence']}")
        print(f"       blind_spots_per_frame: "
              f"{list(synth['blind_spots_per_frame'].keys())}")

    # Step 5: blind_spot_log entry (printed; real runs would append
    # to consortium/audit/blind_spot_log.jsonl)
    log_entry = {
        "entry_id": f"bs-{problem.problem_id}-"
                    f"{datetime.now(timezone.utc).isoformat()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "problem_id": problem.problem_id,
        "entry_kind": "run",
        "frames_consulted": synth["adapters_fired"],
        "blind_spots_per_frame": synth["blind_spots_per_frame"],
        "productive_disagreements": synth["productive_disagreements"],
        "convergence": synth["invariant_geometry"]["convergence"],
        "coating_probes_run": [{
            "reading_id": "embodied_sensor",
            "probe": reading.coating_probe.probe_name,
            "result": reading.coating_probe.result,
            "notes": reading.coating_probe.notes,
        }],
        "time_critical_actions": synth.get("time_critical_actions", []),
        "notes": ("example: soil_with_hands.py demonstrates embodied "
                  "reading lift through full consortium pipeline"),
    }
    if verbose:
        print(f"[4/4] blind_spot_log entry constructed:")
        print(json.dumps(log_entry, indent=2)[:500] + "...")

    return synth, log_entry


if __name__ == "__main__":
    print("=" * 72)
    print("SOIL WITH HANDS — embodied query end-to-end demo")
    print("=" * 72)
    synth, entry = run_consortium(verbose=True)
    print()
    print("=" * 72)
    print(f"DONE. Convergence: "
          f"{synth['invariant_geometry']['convergence']}")
    print(f"      Frames fired: {synth['adapters_fired']}")
    print("=" * 72)
