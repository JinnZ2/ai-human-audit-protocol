# Blind Spot Log — append-only consortium learning

*Where the consortium learns about itself over time.*

The collaboration protocol surfaces blind spots **per run** (`MultiGeometryCollaboration.surface_blind_spots`). This log records those surfaces across runs, append-only, so the consortium can detect:

- **Frames that systematically miss the same coupling.** If `narrative_structured` blind-spots on `regime_drift` in 80% of runs touching climate, that frame's calibration is over-confident in that domain.
- **Costs revealed in retrospect.** `seven_generation_tracer.py` named which factors were `hidden_at_decision_time`; this log is where, generations later, those hidden factors get matched against observed outcomes.
- **Coating recurrences.** When the same kind of coated agreement keeps appearing — and which probes caught it.
- **Operator over-querying.** When budgets in `embodied_sensor.OperatorBudget` keep getting hit, which operators bear the load.

The log is the start of Phase 3 — the "alive part" of the original consortium plan: drift detection across consortium output over time, model-specific blind-spot tracking, Kavik-as-sensor scheduling.

---

## Format

| File | Role |
|---|---|
| `blind_spot_log.md` | This file. Format spec + how-to-write-an-entry. |
| `blind_spot_log.schema.json` | JSON Schema for entries. |
| `blind_spot_log.jsonl` | The actual log. **Append-only.** One JSON object per line. |
| `example_blind_spot_log.jsonl` | Worked examples that validate against the schema. |

JSON Lines (`.jsonl`) was chosen over a single JSON array because:
1. Append-only writes do not require parsing the existing file.
2. Concurrent writers can append without coordinating on file structure.
3. Each line is independently parseable; corruption in one entry does not invalidate others.

---

## Required fields

Every entry MUST include:

- `entry_id` — stable, unique. Suggested: `bs-YYYY-MM-DD-NNN` or `bs-<problem_id>-<timestamp>`.
- `timestamp` — ISO 8601 UTC.
- `problem_id` — references the problem the consortium ran on.
- `frames_consulted` — array of frame_ids that participated.
- `blind_spots_per_frame` — object keyed by frame_id, value is array of coupling strings the frame missed.
- `productive_disagreements` — array of `{frame_a, frame_b, type, claim_a, claim_b}` entries from `MultiGeometryCollaboration.surface_contradictions`.
- `convergence` — `"converged" | "divergent"` from `surface_invariants`.
- `coating_probes_run` — array of probe results per reading (probe_name + result).
- `entry_kind` — `"run" | "retrospective" | "calibration_update"`. (See below.)

Optional fields:

- `time_critical_actions` — bubbled from `synthesize().time_critical_actions`.
- `recommended_action` — what the consenter decided.
- `actual_outcome` — only populated retrospectively (months/years later); compares the recommendation against what happened.
- `frames_calibration_drift` — for `calibration_update` entries; per-frame confidence adjustment proposed.
- `notes` — free-form.

---

## Entry kinds

### `run`
A consortium run completed. Records the synthesized geometry. **Most entries will be this kind.** Written immediately after `aggregate()` returns.

### `retrospective`
Written N generations / months / years after a `run` entry. References the original `entry_id`. Records what actually happened: which `time_critical_actions` were taken, which `hidden_at_decision_time` factors materialized, whether the recommendation panned out. **This is the load-bearing kind for Phase 3** — the consortium can only learn from retrospect.

### `calibration_update`
A periodic entry (suggested: monthly, or after every 50 `run` entries) that aggregates over recent runs and proposes per-frame calibration adjustments: which frames were systematically over-confident, which under-, which were silent on coupling X. Does not modify other entries (immutability); it proposes new calibration values for future runs.

---

## How to write an entry

```python
import json
from datetime import datetime, timezone
from pathlib import Path

entry = {
    "entry_id": f"bs-{problem.problem_id}-{datetime.now(timezone.utc).isoformat()}",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "problem_id": problem.problem_id,
    "entry_kind": "run",
    "frames_consulted": synth["adapters_fired"],
    "blind_spots_per_frame": synth["blind_spots_per_frame"],
    "productive_disagreements": synth["productive_disagreements"],
    "convergence": synth["invariant_geometry"]["convergence"],
    "coating_probes_run": [
        {"reading_id": r.frame.frame_id, "probe": "...", "result": "..."}
        for r in dispatch_result.readings
    ],
    "time_critical_actions": synth.get("time_critical_actions", []),
    "notes": "",
}

log_path = Path("consortium/audit/blind_spot_log.jsonl")
with open(log_path, "a") as f:
    f.write(json.dumps(entry) + "\n")
```

A small helper in `consortium/audit/` may be added later to standardize this; for now the format is the contract.

---

## Audit-symmetric guarantees

The log itself follows the conservation rules it audits.

- **Append-only.** Past entries are never modified or deleted. Calibration updates propose new values without touching prior entries. Per `protocols/change_tracking_v1.0.md`, the immutable changelog principle applies.
- **Operator-agnostic.** A blind spot reported by `ecological_signal` (a non-human frame) gets the same line shape as one reported by `narrative_structured` (an AI frame).
- **Visibility-by-construction.** Hidden labor in the consortium's own runs (which adapter wasn't queried because of consent withholding, which one was unavailable, which probe wasn't run) is recorded in `coating_probes_run` and the parent `aggregate()` fields. The log does not let the consortium hide its own gaps.
- **Plural logic.** When frames disagree, both readings are recorded. The log does not pick a winner. This is the same `convergence: divergent` stance from `collaboration_protocol.py` — geometry is in the disagreements.

---

## How Phase 3 reads this log

The log is the substrate for the eventual `drift_detector` / `calibration_tracker` that does NOT exist yet. When that machinery is built, it will read this log to:

- Compute per-frame blind-spot frequency tables across runs
- Compare `recommended_action` to `actual_outcome` on retrospective entries to identify systematic over/under-confidence per frame
- Detect when a coupling appears as "blind spot" in many frames but is consistently named by one — that one frame becomes load-bearing for that coupling
- Surface unfilled retrospectives: runs where decisions were made and the outcome has not been logged after a horizon-appropriate interval

For now, the log is the seed. Each entry written is a pebble in what will eventually be a calibration substrate. **The pebble must be honest even when the calibration machinery does not yet exist to use it.**

---

## Cross-links

- `consortium/collaboration_protocol.py:MultiGeometryCollaboration.surface_blind_spots` — the per-run source
- `consortium/collaboration_protocol.py:synthesize` — the per-run output the log preserves
- `physics/seven_generation_tracer.py:SevenGenerationTrace.hidden_at_decision_time` — what a future retrospective entry will reconcile against
- `relational_cognition/coating_detection.md` — the probe vocabulary used in `coating_probes_run`
- `protocols/change_tracking_v1.0.md` — the immutability principle this log inherits
