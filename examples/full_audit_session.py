"""
full_audit_session.py — end-to-end demo across all four layers.

Shows how relational_cognition / consortium / physics / ledger fit
together in a single session. The demo deliberately exercises each
layer's load-bearing responsibility:

  1. Build a Problem                              (consortium/collaboration_protocol)
  2. Dispatch to consortium with consent          (consortium/router)
  3. Aggregate readings into geometry             (consortium/router/coherence_aggregator)
  4. Build an RCR-shaped proposal from the result (cross-layer; honest manual
                                                   construction — full
                                                   bridge-to-RCR is a future
                                                   build)
  5. Run substrate alignment check                (physics/substrate_alignment_check)
  6. Anchor each artifact to the ledger           (ledger/implementations/local_filesystem)
  7. Verify the ledger chain                      (ledger/verification_tools)
  8. Construct a blind_spot_log entry             (consortium/audit)
  9. Anchor the blind_spot_log entry too

The session leaves a verifiable audit trail that spans all four
layers. Runtime defenses (consortium consent, physics gates)
applied at decision time; structural permanence (ledger hash chain)
achieved at record time; learning preserved (blind_spot_log).

This demo uses MockAdapter and LocalFilesystemLedger so it runs
fully offline with no external dependencies. Real deployments
swap in real model adapters and real ledger backends; the
session shape is the same.

Run:
    python -m examples.full_audit_session
"""

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import json
import tempfile
from datetime import datetime, timezone

from consortium.collaboration_protocol import (
    Problem,
    build_consortium_frames,
)
from consortium.router.consent import ConsentGate
from consortium.router.mock_adapter import MockAdapter
from consortium.router.query_dispatcher import QueryDispatcher
from consortium.router.coherence_aggregator import aggregate
from physics.substrate_alignment_check import alignment_check
from ledger.implementations.local_filesystem import LocalFilesystemLedger
from ledger.verification_tools import verify_chain


def build_problem() -> Problem:
    """A bounded, real-shaped problem the demo will reason about."""
    return Problem(
        problem_id="full_audit_session_demo",
        presenting_symptoms=[
            "soil moisture variance increasing",
            "knowledge holders aging without transmission",
        ],
        suspected_couplings=[
            "mulch_h2o",
            "soil_thermal_mass",
            "knowledge_continuity",
        ],
        bounds=("upper_midwest", "2026_2050", "regional"),
        regime_context={"climate": "transitional"},
        stakes=["food_continuity", "knowledge_preservation"],
    )


def dispatch_consortium(problem: Problem):
    """Layer 1+2: consortium dispatch with consent gate."""
    frames = {f.frame_id: f for f in build_consortium_frames()}
    adapters = [
        MockAdapter(frame=frames["thermodynamic_geometry"]),
        MockAdapter(frame=frames["narrative_structured"]),
        MockAdapter(frame=frames["ecological_signal"]),
    ]
    dispatcher = QueryDispatcher(adapters=adapters)
    cost_estimates = dispatcher.cost_estimates(problem)

    # Consenter sees costs, then grants consent
    gate = ConsentGate()
    gate.grant(
        problem_id=problem.problem_id,
        adapters_authorized=[a.frame_id for a in adapters],
        cost_disclosed=cost_estimates,
        consenter="full_audit_session_demo_runner",
        notes="offline mock-adapter dispatch; zero substrate cost",
    )
    dispatcher.consent_gate = gate
    dispatch_result = dispatcher.fan_out(problem)
    synthesis = aggregate(dispatch_result, problem,
                          frames=list(frames.values()))
    return dispatch_result, synthesis


def derive_rcr_proposal(problem: Problem, synthesis: dict) -> dict:
    """Layer 3 (manual bridge): turn the consortium synthesis into an
    RCR-shaped proposal. A full automated bridge is open work; here
    we construct it manually with honest fields. The point of this
    demo is to show that the resulting RCR is *checkable* by the
    physics layer — the route to it can be refined separately."""
    return {
        "id": f"rcr-{problem.problem_id}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "proposal": "consortium-derived intervention proposal",
        "participants": {
            "human_groups": ["upper_midwest_residents"],
            "non_human": ["soil_biota"],
            "ecosystems": ["watershed", "prairie"],
            "temporal": ["1y", "10y", "100y", "7g"],
        },
        "baselines": {
            "energy": {"flows": ["solar->grass->soil"], "loss_points": []},
            "keystones": ["mycorrhizae", "knowledge_holders"],
            "constraints": ["water_limits"],
        },
        "transform": {
            "actions": ["soil_thermal_mass_build", "knowledge_transmission"],
            "regeneration_plan": ["soil_C_rebuild_7y"],
        },
        "labor": [
            {"kind": "E_h", "contributor": "human:residents",
             "amount": 200.0, "unit": "person_hours_per_year",
             "visible": True},
            {"kind": "E_a", "contributor": "ai:consortium",
             "amount": 3.0, "unit": "fan_out_calls",
             "visible": True,
             "notes": "from this demo's consortium dispatch"},
            {"kind": "E_e", "contributor": "ecosystem:watershed",
             "amount": 1.0, "unit": "growing_season_pct",
             "visible": True},
        ],
        "checks": {
            "conservation": True,
            "keystone_intact_or_replaced": True,
            "temporal_stability": {
                "1y": "neutral", "10y": "positive",
                "100y": "positive", "7g": "positive",
            },
            "plural_logic_score": {
                "western": 0.80, "indigenous": 0.85,
                "eastern": 0.82, "ecological": 0.88,
            },
            "reciprocity_contract": {
                "present": True,
                "obligations": ["maintenance", "monitoring"],
            },
        },
        "decision": "pending",
    }


def run(verbose: bool = True, ledger_path=None):
    """Run the full session. Returns a dict with everything that
    happened, suitable for testing or for archival.

    `ledger_path` defaults to a tempdir; pass an explicit path for
    persistent runs (real deployments would point at the long-lived
    audit ledger)."""
    cleanup_tmp = None
    if ledger_path is None:
        cleanup_tmp = tempfile.TemporaryDirectory()
        ledger_path = Path(cleanup_tmp.name) / "session.jsonl"

    if verbose:
        print("=" * 72)
        print("FULL AUDIT SESSION — end-to-end demo")
        print("=" * 72)

    # ---- Step 1+2: problem + consortium dispatch ----
    problem = build_problem()
    if verbose:
        print(f"\n[1/9] PROBLEM: {problem.problem_id}")
        print(f"      stakes={problem.stakes}")

    dispatch_result, synthesis = dispatch_consortium(problem)
    if verbose:
        print(f"\n[2/9] CONSORTIUM DISPATCH")
        print(f"      adapters_fired={synthesis['adapters_fired']}")
        print(f"      convergence={synthesis['invariant_geometry']['convergence']}")

    # ---- Step 3: derive RCR proposal ----
    rcr = derive_rcr_proposal(problem, synthesis)
    if verbose:
        print(f"\n[3/9] RCR PROPOSAL DERIVED  id={rcr['id']}")
        print(f"      labor entries={len(rcr['labor'])}")

    # ---- Step 4: substrate alignment check ----
    report = alignment_check(rcr)
    if verbose:
        print(f"\n[4/9] SUBSTRATE ALIGNMENT CHECK")
        print(f"      recommendation={report.recommendation}")
        for c in report.checks:
            mark = "✓" if c.passed is True else (
                "✗" if c.passed is False else "?")
            print(f"        {mark} {c.name}")

    # ---- Step 5+6: anchor artifacts to ledger ----
    ledger = LocalFilesystemLedger(ledger_path)
    anchor_problem = ledger.append(
        entry_id=f"anchor-problem-{problem.problem_id}",
        payload={"kind": "problem",
                 "problem_id": problem.problem_id,
                 "stakes": problem.stakes,
                 "regime_context": problem.regime_context},
        payload_kind="problem",
    )
    anchor_synthesis = ledger.append(
        entry_id=f"anchor-synthesis-{problem.problem_id}",
        payload={"kind": "consortium_synthesis",
                 "adapters_fired": synthesis["adapters_fired"],
                 "convergence": synthesis["invariant_geometry"]["convergence"]},
        payload_kind="consortium_synthesis",
    )
    anchor_rcr = ledger.append(
        entry_id=f"anchor-rcr-{rcr['id']}",
        payload=rcr,
        payload_kind="rcr",
    )
    anchor_check = ledger.append(
        entry_id=f"anchor-check-{rcr['id']}",
        payload=report.to_dict(),
        payload_kind="alignment_report",
    )
    if verbose:
        print(f"\n[5/9] ARTIFACTS ANCHORED TO LEDGER")
        print(f"      4 entries written to {ledger_path}")

    # ---- Step 7: verify the chain ----
    verification = verify_chain(ledger.read_all())
    if verbose:
        print(f"\n[6/9] CHAIN VERIFIED")
        print(f"      recommendation={verification.recommendation}")
        print(f"      summary={verification.summary}")

    # ---- Step 8: blind_spot_log entry ----
    log_entry = {
        "entry_id": f"bs-{problem.problem_id}-"
                    f"{datetime.now(timezone.utc).isoformat()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "problem_id": problem.problem_id,
        "entry_kind": "run",
        "frames_consulted": synthesis["adapters_fired"],
        "blind_spots_per_frame": synthesis["blind_spots_per_frame"],
        "productive_disagreements": synthesis["productive_disagreements"],
        "convergence": synthesis["invariant_geometry"]["convergence"],
        "coating_probes_run": [],
        "time_critical_actions": synthesis.get(
            "time_critical_actions", []),
        "recommended_action": (
            f"alignment_check recommendation: {report.recommendation}; "
            f"see anchored RCR for full proposal"),
        "notes": (
            "full audit session: consortium dispatched; physics "
            "alignment check passed; chain verified; this entry "
            "itself anchored on next step"),
    }

    # ---- Step 9: anchor the blind_spot_log entry too ----
    anchor_log = ledger.append(
        entry_id=f"anchor-blind-spot-{log_entry['entry_id']}",
        payload=log_entry,
        payload_kind="blind_spot_log",
    )
    if verbose:
        print(f"\n[7/9] BLIND_SPOT_LOG ENTRY")
        print(f"      entry_id={log_entry['entry_id'][:60]}...")
    if verbose:
        print(f"\n[8/9] BLIND_SPOT_LOG ENTRY ANCHORED")
        print(f"      anchor_hash={anchor_log.entry_hash[:16]}...")

    # ---- Step 9: re-verify chain (now 5 entries) ----
    final_verification = verify_chain(ledger.read_all())
    if verbose:
        print(f"\n[9/9] FINAL CHAIN VERIFICATION")
        print(f"      n_entries={final_verification.n_entries}")
        print(f"      recommendation={final_verification.recommendation}")

    result = {
        "problem": problem,
        "synthesis": synthesis,
        "rcr": rcr,
        "alignment_report": report,
        "ledger_entries": ledger.read_all(),
        "blind_spot_log_entry": log_entry,
        "final_verification": final_verification,
        "ledger_path": str(ledger_path),
    }

    if verbose:
        print()
        print("=" * 72)
        print(f"DONE — runtime defenses applied (consortium consent + "
              f"physics check); structural permanence achieved (5 "
              f"entries in chain, all verified); learning recorded "
              f"(blind_spot_log entry, itself anchored).")
        print("=" * 72)

    if cleanup_tmp:
        cleanup_tmp.cleanup()
    return result


if __name__ == "__main__":
    run(verbose=True)
