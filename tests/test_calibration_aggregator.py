"""Unit tests for consortium/audit/calibration_aggregator.py.

The aggregator is the Phase 3 feedback loop substrate: reads the
blind_spot_log over time and proposes calibration updates. These
tests verify the contract: stats are computed correctly, thresholds
gate proposals, the output entry validates against the schema.
"""

import json
from pathlib import Path

import pytest

from consortium.audit.calibration_aggregator import (
    DEFAULT_BLIND_SPOT_RATE_FLOOR,
    DEFAULT_CALIBRATION_DELTA,
    DEFAULT_MIN_CONSULTATIONS,
    DEFAULT_PROBE_FAIL_RATE_FLOOR,
    FrameStats,
    aggregate_log,
    aggregate_log_file,
    build_calibration_update_entry,
    propose_calibration_drift,
)


def _run_entry(frames_consulted, blind_spots=None, probes=None,
               problem_id="p"):
    return {
        "entry_id": f"bs-{problem_id}",
        "timestamp": "2026-04-27T00:00:00+00:00",
        "problem_id": problem_id,
        "entry_kind": "run",
        "frames_consulted": list(frames_consulted),
        "blind_spots_per_frame": blind_spots or {},
        "productive_disagreements": [],
        "convergence": "converged",
        "coating_probes_run": probes or [],
    }


# ============================================================
# FrameStats properties
# ============================================================

class TestFrameStats:
    def test_blind_spot_rate_zero_when_never_consulted(self):
        s = FrameStats(frame_id="x")
        assert s.blind_spot_rate == 0.0

    def test_blind_spot_rate_calculated(self):
        s = FrameStats(frame_id="x", consulted_count=4, blind_spot_count=3)
        assert s.blind_spot_rate == 0.75

    def test_probe_fail_rate_zero_when_no_probes(self):
        s = FrameStats(frame_id="x")
        assert s.probe_fail_rate == 0.0

    def test_probe_fail_rate_uses_only_passed_failed(self):
        # inconclusive and not_run are excluded from denominator
        s = FrameStats(
            frame_id="x", probe_passed=2, probe_failed=2,
            probe_inconclusive=10, probe_not_run=10,
        )
        assert s.probe_fail_rate == 0.5

    def test_evaluable_probes_excludes_inconclusive(self):
        s = FrameStats(
            frame_id="x", probe_passed=1, probe_failed=2,
            probe_inconclusive=5, probe_not_run=3,
        )
        assert s.evaluable_probes == 3


# ============================================================
# aggregate_log
# ============================================================

class TestAggregateLog:
    def test_empty_log(self):
        assert aggregate_log([]) == {}

    def test_single_run_consultation(self):
        stats = aggregate_log([
            _run_entry(["frame_a"]),
        ])
        assert "frame_a" in stats
        assert stats["frame_a"].consulted_count == 1

    def test_blind_spots_counted(self):
        stats = aggregate_log([
            _run_entry(
                ["frame_a"],
                blind_spots={"frame_a": ["coupling_x"]},
            ),
        ])
        assert stats["frame_a"].blind_spot_count == 1

    def test_probe_results_categorized(self):
        stats = aggregate_log([
            _run_entry(["a"], probes=[
                {"reading_id": "a", "probe": "x", "result": "passed"},
                {"reading_id": "a", "probe": "x", "result": "failed"},
                {"reading_id": "a", "probe": "x", "result": "inconclusive"},
                {"reading_id": "a", "probe": "x", "result": "not_run"},
            ]),
        ])
        s = stats["a"]
        assert s.probe_passed == 1
        assert s.probe_failed == 1
        assert s.probe_inconclusive == 1
        assert s.probe_not_run == 1

    def test_calibration_update_entries_ignored(self):
        stats = aggregate_log([
            {"entry_kind": "calibration_update",
             "frames_consulted": ["a"]},
        ])
        assert stats == {}

    def test_retrospective_entries_counted(self):
        stats = aggregate_log([
            {"entry_kind": "retrospective",
             "frames_consulted": ["a"],
             "blind_spots_per_frame": {},
             "actual_outcome": "thing happened"},
        ])
        assert stats["a"].consulted_count == 1
        assert "thing happened" in stats["a"].retrospective_outcomes

    def test_multi_run_aggregation(self):
        stats = aggregate_log([
            _run_entry(["a", "b"]),
            _run_entry(["a"], blind_spots={"a": ["x"]}),
            _run_entry(["a", "b"], blind_spots={"a": ["y"]}),
        ])
        # a consulted 3 times, b consulted 2 times
        assert stats["a"].consulted_count == 3
        assert stats["b"].consulted_count == 2
        # a in blind_spots 2 times
        assert stats["a"].blind_spot_count == 2


# ============================================================
# propose_calibration_drift
# ============================================================

class TestProposeCalibrationDrift:
    def test_no_proposal_below_min_consultations(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=2,
                blind_spot_count=2,   # 100% blind spot rate
            )
        }
        proposals = propose_calibration_drift(
            stats, min_consultations=3,
        )
        assert proposals == {}

    def test_high_blind_spot_rate_triggers_proposal(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=10,
                blind_spot_count=8,   # 80% blind spot rate, above default 70%
            )
        }
        proposals = propose_calibration_drift(stats)
        assert "a" in proposals
        assert "blind_spot_rate" in proposals["a"]["reason"]

    def test_low_blind_spot_rate_no_proposal(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=10, blind_spot_count=1,
                probe_passed=5,
            )
        }
        proposals = propose_calibration_drift(stats)
        assert "a" not in proposals

    def test_high_probe_fail_rate_triggers_proposal(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=5,
                probe_passed=1, probe_failed=4,   # 80% fail rate
            )
        }
        proposals = propose_calibration_drift(stats)
        assert "a" in proposals
        assert "probe_fail_rate" in proposals["a"]["reason"]

    def test_both_signals_compound_adjustment(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=10, blind_spot_count=8,
                probe_passed=1, probe_failed=4,
            )
        }
        proposals = propose_calibration_drift(stats)
        # both reasons present
        assert "blind_spot_rate" in proposals["a"]["reason"]
        assert "probe_fail_rate" in proposals["a"]["reason"]
        # adjustment is double single delta
        prev = proposals["a"]["previous_calibration"]
        new = proposals["a"]["proposed_calibration"]
        assert prev - new == pytest.approx(2 * DEFAULT_CALIBRATION_DELTA)

    def test_uses_current_calibrations_as_prior(self):
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=5, blind_spot_count=5,
            )
        }
        proposals = propose_calibration_drift(
            stats, current_calibrations={"a": 0.90},
        )
        assert proposals["a"]["previous_calibration"] == 0.90

    def test_proposed_calibration_floor(self):
        # huge adjustments should still floor at 0.30
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=10, blind_spot_count=10,
                probe_passed=0, probe_failed=10,
            )
        }
        proposals = propose_calibration_drift(
            stats, current_calibrations={"a": 0.35},
            delta=0.50,
        )
        assert proposals["a"]["proposed_calibration"] >= 0.30

    def test_default_prior(self):
        # frame not in current_calibrations gets 0.75 default
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=10, blind_spot_count=10,
            )
        }
        proposals = propose_calibration_drift(stats)
        assert proposals["a"]["previous_calibration"] == 0.75

    def test_probe_fail_requires_min_evaluable(self):
        # only one probe, even at 100% fail, doesn't trigger
        stats = {
            "a": FrameStats(
                frame_id="a", consulted_count=3,
                probe_passed=0, probe_failed=1,   # only 1 evaluable
            )
        }
        proposals = propose_calibration_drift(stats)
        # blind_spot_rate is 0, probe is below the n>=2 gate → no proposal
        assert "a" not in proposals


# ============================================================
# build_calibration_update_entry
# ============================================================

class TestBuildEntry:
    def test_entry_has_required_schema_fields(self):
        entry = build_calibration_update_entry(
            proposals={"a": {"previous_calibration": 0.8,
                              "proposed_calibration": 0.7,
                              "reason": "test"}},
            n_runs_aggregated=5,
        )
        for f in ("entry_id", "timestamp", "problem_id", "entry_kind",
                  "frames_consulted", "blind_spots_per_frame",
                  "productive_disagreements", "convergence",
                  "coating_probes_run"):
            assert f in entry
        assert entry["entry_kind"] == "calibration_update"

    def test_frames_calibration_drift_passed_through(self):
        proposals = {"a": {"previous_calibration": 0.8,
                            "proposed_calibration": 0.7,
                            "reason": "x"}}
        entry = build_calibration_update_entry(
            proposals=proposals, n_runs_aggregated=5,
        )
        assert entry["frames_calibration_drift"] == proposals

    def test_validates_against_blind_spot_log_schema(self):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")

        entry = build_calibration_update_entry(
            proposals={"a": {"previous_calibration": 0.8,
                              "proposed_calibration": 0.7,
                              "reason": "test"}},
            n_runs_aggregated=5,
        )
        schema_path = (Path(__file__).parent.parent
                       / "consortium" / "audit"
                       / "blind_spot_log.schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(entry, schema)

    def test_n_runs_recorded_in_notes(self):
        entry = build_calibration_update_entry(
            proposals={}, n_runs_aggregated=42,
        )
        assert "42" in entry["notes"]


# ============================================================
# aggregate_log_file (end-to-end)
# ============================================================

class TestAggregateLogFile:
    def test_missing_file_returns_empty_proposals(self, tmp_path):
        result = aggregate_log_file(tmp_path / "missing.jsonl")
        assert result["frames_calibration_drift"] == {}
        assert "does not exist" in result["notes"]

    def test_real_example_log_processes_cleanly(self):
        # the example log we shipped earlier should aggregate without
        # error; small sample → likely no proposals at default
        # thresholds, but the ENTRY itself should validate
        example_path = (Path(__file__).parent.parent
                        / "consortium" / "audit"
                        / "example_blind_spot_log.jsonl")
        result = aggregate_log_file(example_path)
        assert result["entry_kind"] == "calibration_update"

    def test_writes_proposal_when_threshold_met(self, tmp_path):
        # build a log with deliberate over-blindness for one frame
        log = tmp_path / "synthetic.jsonl"
        with open(log, "w") as f:
            for i in range(5):
                entry = _run_entry(
                    ["over_confident", "fine_frame"],
                    blind_spots={"over_confident": ["coupling_x"]},
                )
                entry["entry_id"] = f"bs-{i}"
                f.write(json.dumps(entry) + "\n")
        result = aggregate_log_file(log)
        assert "over_confident" in result["frames_calibration_drift"]
        assert "fine_frame" not in result["frames_calibration_drift"]

    def test_n_runs_aggregated_correct(self, tmp_path):
        log = tmp_path / "synthetic.jsonl"
        with open(log, "w") as f:
            for i in range(7):
                f.write(json.dumps(_run_entry(["x"])) + "\n")
            # one calibration_update entry — should NOT count
            f.write(json.dumps({
                "entry_kind": "calibration_update",
                "entry_id": "cu",
                "timestamp": "2026-04-27T00:00:00+00:00",
                "problem_id": "_calibration_aggregate",
                "frames_consulted": [],
                "blind_spots_per_frame": {},
                "productive_disagreements": [],
                "convergence": "converged",
                "coating_probes_run": [],
            }) + "\n")
        result = aggregate_log_file(log)
        assert "7" in result["notes"]
