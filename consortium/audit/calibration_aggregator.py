"""
calibration_aggregator.py

Reads blind_spot_log.jsonl over time and proposes per-frame
confidence calibration updates.

Phase 3 substrate: the consortium learns about itself. A frame
that systematically appears in `blind_spots_per_frame`, OR whose
coating probes systematically fail, OR whose recommendations
systematically disagree with retrospective outcomes — is over-
confident in that domain and should have its calibration adjusted
downward. The opposite case (frame whose readings consistently
hold up under retrospect) suggests under-confidence.

This module is data-not-judgment. It computes statistics over the
log and proposes a `calibration_update` entry. It does NOT modify
the log itself; the proposal is a new entry the consenter chooses
to append (or not).

Returns a fully-shaped `calibration_update` entry that validates
against consortium/audit/blind_spot_log.schema.json.

CC0. No external dependencies.
"""

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# allow standalone execution alongside `python -m consortium.audit.calibration_aggregator`
_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))


# Default thresholds. Caller may override.
DEFAULT_BLIND_SPOT_RATE_FLOOR = 0.7    # 70%+ of consultations → flag
DEFAULT_PROBE_FAIL_RATE_FLOOR = 0.5    # 50%+ probe failures → flag
DEFAULT_MIN_CONSULTATIONS = 3          # need at least N runs to evaluate
DEFAULT_CALIBRATION_DELTA = 0.05       # how much to adjust per flag


@dataclass
class FrameStats:
    """Aggregate statistics for one frame across the log."""
    frame_id: str
    consulted_count: int = 0
    blind_spot_count: int = 0
    probe_passed: int = 0
    probe_failed: int = 0
    probe_inconclusive: int = 0
    probe_not_run: int = 0
    retrospective_outcomes: List[str] = field(default_factory=list)

    @property
    def total_probes(self) -> int:
        return (self.probe_passed + self.probe_failed
                + self.probe_inconclusive + self.probe_not_run)

    @property
    def evaluable_probes(self) -> int:
        return self.probe_passed + self.probe_failed

    @property
    def blind_spot_rate(self) -> float:
        if self.consulted_count == 0:
            return 0.0
        return self.blind_spot_count / self.consulted_count

    @property
    def probe_fail_rate(self) -> float:
        if self.evaluable_probes == 0:
            return 0.0
        return self.probe_failed / self.evaluable_probes


def aggregate_log(
    entries: List[Dict[str, Any]],
) -> Dict[str, FrameStats]:
    """
    Walk a list of blind_spot_log entries and compute per-frame
    statistics. Considers `run` and `retrospective` entries; ignores
    `calibration_update` entries (those are output, not input).
    """
    stats: Dict[str, FrameStats] = {}

    def get(frame_id: str) -> FrameStats:
        if frame_id not in stats:
            stats[frame_id] = FrameStats(frame_id=frame_id)
        return stats[frame_id]

    for entry in entries:
        kind = entry.get("entry_kind")
        if kind not in ("run", "retrospective"):
            continue

        for frame_id in entry.get("frames_consulted", []):
            get(frame_id).consulted_count += 1

        for frame_id in (entry.get("blind_spots_per_frame") or {}).keys():
            get(frame_id).blind_spot_count += 1

        for probe in entry.get("coating_probes_run") or []:
            reading_id = probe.get("reading_id", "")
            result = probe.get("result", "")
            if not reading_id:
                continue
            s = get(reading_id)
            if result == "passed":
                s.probe_passed += 1
            elif result == "failed":
                s.probe_failed += 1
            elif result == "inconclusive":
                s.probe_inconclusive += 1
            else:
                s.probe_not_run += 1

        if kind == "retrospective":
            outcome = entry.get("actual_outcome", "")
            if outcome:
                for frame_id in entry.get("frames_consulted", []):
                    get(frame_id).retrospective_outcomes.append(outcome)

    return stats


def propose_calibration_drift(
    stats: Dict[str, FrameStats],
    current_calibrations: Optional[Dict[str, float]] = None,
    blind_spot_rate_floor: float = DEFAULT_BLIND_SPOT_RATE_FLOOR,
    probe_fail_rate_floor: float = DEFAULT_PROBE_FAIL_RATE_FLOOR,
    min_consultations: int = DEFAULT_MIN_CONSULTATIONS,
    delta: float = DEFAULT_CALIBRATION_DELTA,
) -> Dict[str, Dict[str, Any]]:
    """
    Compute per-frame calibration drift proposals.

    Returns a dict keyed by frame_id, value matches the
    `frames_calibration_drift` shape in
    consortium/audit/blind_spot_log.schema.json:
        {previous_calibration, proposed_calibration, reason}

    Frames not meeting any threshold are NOT included in the output.
    The output is ALWAYS only frames where adjustment is proposed.

    `current_calibrations` is the input prior — typically the most
    recent `calibration_update` entry's frames_calibration_drift, or
    the frame's `confidence_calibration` from
    `consortium/collaboration_protocol.build_consortium_frames()`.
    Missing entries default to 0.75 (a generic prior).
    """
    current_calibrations = current_calibrations or {}
    proposals: Dict[str, Dict[str, Any]] = {}

    for frame_id, s in stats.items():
        if s.consulted_count < min_consultations:
            continue

        reasons = []
        adjustment = 0.0

        if s.blind_spot_rate >= blind_spot_rate_floor:
            reasons.append(
                f"blind_spot_rate={s.blind_spot_rate:.2f} "
                f"≥ floor {blind_spot_rate_floor} "
                f"({s.blind_spot_count}/{s.consulted_count} runs); "
                f"systematic blindness suggests over-confidence"
            )
            adjustment += delta

        if (s.evaluable_probes >= 2
                and s.probe_fail_rate >= probe_fail_rate_floor):
            reasons.append(
                f"probe_fail_rate={s.probe_fail_rate:.2f} "
                f"≥ floor {probe_fail_rate_floor} "
                f"({s.probe_failed}/{s.evaluable_probes} probes); "
                f"coating-probe failures suggest the readings do not "
                f"survive adversarial restatement"
            )
            adjustment += delta

        if not reasons:
            continue

        prev = current_calibrations.get(frame_id, 0.75)
        new = max(0.30, min(0.99, prev - adjustment))

        proposals[frame_id] = {
            "previous_calibration": prev,
            "proposed_calibration": round(new, 3),
            "reason": "; ".join(reasons),
        }

    return proposals


def build_calibration_update_entry(
    proposals: Dict[str, Dict[str, Any]],
    n_runs_aggregated: int,
    consenter: str = "calibration_aggregator",
    notes: str = "",
) -> Dict[str, Any]:
    """
    Build a fully-shaped `calibration_update` entry that validates
    against consortium/audit/blind_spot_log.schema.json.

    Returns the entry dict; caller decides whether to append it to
    `blind_spot_log.jsonl`. The aggregator does NOT write to the log.
    """
    now = datetime.now(timezone.utc).isoformat()
    base_notes = (
        f"v1 calibration update; aggregated over {n_runs_aggregated} "
        f"run/retrospective entries"
    )
    full_notes = f"{base_notes}. {notes}".strip(". ").strip()

    return {
        "entry_id": f"bs-cal-{now}",
        "timestamp": now,
        "problem_id": "_calibration_aggregate",
        "entry_kind": "calibration_update",
        "frames_consulted": [],
        "blind_spots_per_frame": {},
        "productive_disagreements": [],
        "convergence": "converged",
        "coating_probes_run": [],
        "frames_calibration_drift": proposals,
        "notes": full_notes,
    }


def aggregate_log_file(
    log_path: Path,
    current_calibrations: Optional[Dict[str, float]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    End-to-end: read a blind_spot_log.jsonl, aggregate, propose,
    and return a calibration_update entry. Caller decides whether
    to append the entry to the same log.
    """
    log_path = Path(log_path)
    if not log_path.exists():
        return build_calibration_update_entry(
            proposals={},
            n_runs_aggregated=0,
            notes="log file does not exist",
        )

    entries: List[Dict[str, Any]] = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))

    n_aggregated = sum(
        1 for e in entries
        if e.get("entry_kind") in ("run", "retrospective")
    )
    stats = aggregate_log(entries)
    proposals = propose_calibration_drift(
        stats,
        current_calibrations=current_calibrations,
        **kwargs,
    )
    return build_calibration_update_entry(
        proposals=proposals,
        n_runs_aggregated=n_aggregated,
    )


# ============================================================
# DEMO — run against the example log
# ============================================================
if __name__ == "__main__":
    example_path = (Path(__file__).parent
                    / "example_blind_spot_log.jsonl")
    print("=" * 72)
    print("CALIBRATION AGGREGATOR — demo against example_blind_spot_log.jsonl")
    print("=" * 72)
    update = aggregate_log_file(example_path)
    print(json.dumps(update, indent=2))
    print()
    if update["frames_calibration_drift"]:
        print(f"Proposed adjustments for {len(update['frames_calibration_drift'])} "
              f"frame(s).")
    else:
        print("No frames met thresholds for adjustment "
              "(small sample; v1 thresholds are conservative).")
