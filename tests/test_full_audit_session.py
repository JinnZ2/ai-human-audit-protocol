"""Smoke tests for examples/full_audit_session.py.

The full-session demo is the cross-layer integration test: it
proves all four architecture layers (relational_cognition, consortium,
physics, ledger) interoperate. These tests verify the end-to-end
contract: every step produces the expected shape, and the artifacts
are all schema-valid + verifiable.
"""

import json
from pathlib import Path

import pytest


# ============================================================
# End-to-end contract
# ============================================================

class TestFullAuditSession:
    def test_runs_without_error(self, tmp_path):
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert result["problem"].problem_id == "full_audit_session_demo"

    def test_consortium_synthesis_has_three_frames(self, tmp_path):
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert len(result["synthesis"]["adapters_fired"]) == 3

    def test_alignment_check_recommends_aligned(self, tmp_path):
        # the demo's RCR is constructed to pass C1-C6
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert result["alignment_report"].recommendation == "aligned"

    def test_ledger_holds_five_entries(self, tmp_path):
        # problem + synthesis + rcr + alignment_report + blind_spot_log
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert len(result["ledger_entries"]) == 5

    def test_chain_verifies_clean(self, tmp_path):
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert result["final_verification"].recommendation == "verified"

    def test_each_anchored_payload_has_distinct_kind(self, tmp_path):
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        kinds = [e["payload_kind"] for e in result["ledger_entries"]]
        # five distinct payload kinds, in this order
        assert kinds == [
            "problem",
            "consortium_synthesis",
            "rcr",
            "alignment_report",
            "blind_spot_log",
        ]

    def test_blind_spot_log_entry_is_run_kind(self, tmp_path):
        from examples.full_audit_session import run
        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        assert result["blind_spot_log_entry"]["entry_kind"] == "run"


# ============================================================
# Cross-layer schema validation
# ============================================================

class TestCrossLayerSchemaValidation:
    def setup_method(self):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")

    def test_anchored_rcr_passes_physics_ledger_schema(self, tmp_path):
        """The RCR payload anchored in the chain should validate
        against physics/ledger_schema.json (the substrate-integrity
        schema, not the envelope schema)."""
        from examples.full_audit_session import run
        import jsonschema

        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        rcr_envelope = next(e for e in result["ledger_entries"]
                            if e["payload_kind"] == "rcr")
        rcr_payload = rcr_envelope["payload"]

        schema_path = (Path(__file__).parent.parent / "physics"
                       / "ledger_schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(rcr_payload, schema)

    def test_envelopes_pass_ledger_schema(self, tmp_path):
        """All five envelopes should validate against
        ledger/ledger_schema.json (the envelope schema)."""
        from examples.full_audit_session import run
        import jsonschema

        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        schema_path = (Path(__file__).parent.parent / "ledger"
                       / "ledger_schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        for envelope in result["ledger_entries"]:
            jsonschema.validate(envelope, schema)

    def test_blind_spot_log_entry_passes_consortium_schema(self, tmp_path):
        """The blind_spot_log entry payload should validate against
        consortium/audit/blind_spot_log.schema.json."""
        from examples.full_audit_session import run
        import jsonschema

        result = run(verbose=False, ledger_path=tmp_path / "session.jsonl")
        log_entry = result["blind_spot_log_entry"]

        schema_path = (Path(__file__).parent.parent / "consortium"
                       / "audit" / "blind_spot_log.schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(log_entry, schema)


# ============================================================
# Tampering detection: the load-bearing claim
# ============================================================

class TestSessionTamperingDetection:
    def test_tampering_with_anchored_rcr_breaks_chain(self, tmp_path):
        # Run a clean session, tamper with an anchored payload, then
        # verify that re-verification flags the tampering. This is the
        # cross-layer smoke test of the load-bearing claim:
        # "structural permanence prevents revision."
        from examples.full_audit_session import run
        from ledger.verification_tools import verify_chain

        ledger_path = tmp_path / "session.jsonl"
        result = run(verbose=False, ledger_path=ledger_path)
        assert result["final_verification"].recommendation == "verified"

        # Tamper with the anchored RCR's payload directly in the file
        with open(ledger_path) as f:
            lines = f.readlines()
        # find the rcr line (third entry: 0=problem, 1=synthesis, 2=rcr)
        rcr_envelope = json.loads(lines[2])
        # mutate something inside the payload
        rcr_envelope["payload"]["proposal"] = "TAMPERED proposal"
        lines[2] = json.dumps(rcr_envelope, sort_keys=True,
                              separators=(",", ":")) + "\n"
        with open(ledger_path, "w") as f:
            f.writelines(lines)

        # Re-read + verify
        with open(ledger_path) as f:
            entries = [json.loads(line) for line in f if line.strip()]
        report = verify_chain(entries)
        assert report.recommendation == "tampered"
