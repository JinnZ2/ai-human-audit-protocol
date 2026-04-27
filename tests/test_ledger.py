"""Unit tests for the ledger/ folder.

Covers: canonical JSON, hashing primitives, envelope construction,
LedgerBackend ABC contract, LocalFilesystemLedger reference impl,
verify_chain (with tampering scenarios), and stub adapters.
"""

import json
from pathlib import Path

import pytest

from ledger.ledger_interface import (
    AppendResult,
    ENVELOPE_VERSION,
    HASH_ALGORITHM,
    LedgerBackend,
    build_envelope,
    canonicalize,
    hash_entry_chain_input,
    hash_payload,
    sha256_hex,
)
from ledger.implementations.local_filesystem import LocalFilesystemLedger
from ledger.implementations.ethereum_stub import EthereumLedger
from ledger.implementations.hyperledger_stub import HyperledgerLedger
from ledger.implementations.ipfs_stub import IPFSLedger
from ledger.verification_tools import (
    EntryVerification,
    VerificationReport,
    verify_chain,
)


# ============================================================
# Canonical JSON
# ============================================================

class TestCanonicalize:
    def test_sorts_keys(self):
        a = {"b": 1, "a": 2}
        b = {"a": 2, "b": 1}
        assert canonicalize(a) == canonicalize(b)

    def test_no_whitespace(self):
        s = canonicalize({"a": 1, "b": [2, 3]})
        assert " " not in s
        assert "\n" not in s

    def test_unicode_preserved(self):
        s = canonicalize({"glyph": "🕸️"})
        assert "🕸️" in s

    def test_nested_sorting(self):
        a = canonicalize({"outer": {"b": 1, "a": 2}})
        b = canonicalize({"outer": {"a": 2, "b": 1}})
        assert a == b


# ============================================================
# Hashing primitives
# ============================================================

class TestHashing:
    def test_sha256_hex_length(self):
        assert len(sha256_hex("anything")) == 64

    def test_sha256_hex_deterministic(self):
        assert sha256_hex("test") == sha256_hex("test")

    def test_hash_payload_deterministic_across_key_order(self):
        a = {"a": 1, "b": 2}
        b = {"b": 2, "a": 1}
        assert hash_payload(a) == hash_payload(b)

    def test_hash_payload_changes_when_content_changes(self):
        a = {"x": 1}
        b = {"x": 2}
        assert hash_payload(a) != hash_payload(b)

    def test_hash_entry_chain_input_changes_when_any_field_changes(self):
        base = dict(
            entry_id="e1",
            timestamp="2026-04-27T00:00:00+00:00",
            payload_kind="rcr",
            payload_hash="a" * 64,
            previous_entry_hash=None,
        )
        h1 = hash_entry_chain_input(**base)

        # change each field; hash should change
        for field in ("entry_id", "timestamp", "payload_kind",
                      "payload_hash"):
            modified = dict(base)
            modified[field] = "different"
            assert hash_entry_chain_input(**modified) != h1


# ============================================================
# Envelope construction
# ============================================================

class TestBuildEnvelope:
    def test_required_fields_present(self):
        env = build_envelope(
            entry_id="e1",
            payload={"x": 1},
            payload_kind="rcr",
            previous_entry_hash=None,
        )
        for f in ("envelope_version", "entry_id", "timestamp",
                  "payload_kind", "payload", "payload_hash",
                  "previous_entry_hash", "entry_hash",
                  "hash_algorithm"):
            assert f in env

    def test_envelope_version(self):
        env = build_envelope("e1", {}, "rcr", None)
        assert env["envelope_version"] == ENVELOPE_VERSION

    def test_hash_algorithm(self):
        env = build_envelope("e1", {}, "rcr", None)
        assert env["hash_algorithm"] == HASH_ALGORITHM

    def test_genesis_has_null_previous(self):
        env = build_envelope("e1", {}, "rcr", None)
        assert env["previous_entry_hash"] is None

    def test_payload_hash_is_64_hex(self):
        env = build_envelope("e1", {"a": 1}, "rcr", None)
        ph = env["payload_hash"]
        assert len(ph) == 64
        assert all(c in "0123456789abcdef" for c in ph)

    def test_entry_hash_is_64_hex(self):
        env = build_envelope("e1", {}, "rcr", None)
        eh = env["entry_hash"]
        assert len(eh) == 64
        assert all(c in "0123456789abcdef" for c in eh)

    def test_anchor_metadata_optional(self):
        env_without = build_envelope("e1", {}, "rcr", None)
        assert "anchor_metadata" not in env_without
        env_with = build_envelope("e1", {}, "rcr", None,
                                   anchor_metadata={"kind": "test"})
        assert env_with["anchor_metadata"] == {"kind": "test"}

    def test_signatures_optional(self):
        env = build_envelope("e1", {}, "rcr", None,
                              signatures=[{"signer": "x",
                                           "algorithm": "y",
                                           "signature": "z"}])
        assert len(env["signatures"]) == 1


# ============================================================
# LedgerBackend ABC contract
# ============================================================

class TestLedgerBackendABC:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            LedgerBackend()


# ============================================================
# LocalFilesystemLedger
# ============================================================

class TestLocalFilesystemLedger:
    def test_genesis_has_no_previous(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        result = ledger.append("e1", {"x": 1})
        assert result.previous_entry_hash is None

    def test_second_entry_links_to_first(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        r1 = ledger.append("e1", {"x": 1})
        r2 = ledger.append("e2", {"x": 2})
        assert r2.previous_entry_hash == r1.entry_hash

    def test_read_all_returns_entries_in_order(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {"i": 1})
        ledger.append("e2", {"i": 2})
        ledger.append("e3", {"i": 3})
        entries = ledger.read_all()
        assert [e["entry_id"] for e in entries] == ["e1", "e2", "e3"]

    def test_head_is_latest_entry_hash(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {})
        r2 = ledger.append("e2", {})
        assert ledger.head() == r2.entry_hash

    def test_head_is_none_when_empty(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        assert ledger.head() is None

    def test_read_all_empty_when_missing_file(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "missing.jsonl")
        assert ledger.read_all() == []

    def test_corrupted_file_raises(self, tmp_path):
        path = tmp_path / "bad.jsonl"
        path.write_text("not valid json\n")
        ledger = LocalFilesystemLedger(path)
        with pytest.raises(ValueError, match="corrupted"):
            ledger.read_all()

    def test_anchor_metadata_includes_filesystem_kind(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {})
        entries = ledger.read_all()
        assert entries[0]["anchor_metadata"]["kind"] == "local_filesystem"

    def test_parent_directory_created(self, tmp_path):
        path = tmp_path / "deep" / "nested" / "l.jsonl"
        ledger = LocalFilesystemLedger(path)
        ledger.append("e1", {})
        assert path.exists()

    def test_payload_kind_recorded(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {}, payload_kind="rcr")
        entries = ledger.read_all()
        assert entries[0]["payload_kind"] == "rcr"

    def test_available_returns_true_when_writable(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ok, reason = ledger.available()
        assert ok is True


# ============================================================
# verify_chain — clean chain
# ============================================================

class TestVerifyCleanChain:
    def test_empty_chain(self):
        report = verify_chain([])
        assert report.recommendation == "empty"
        assert report.n_entries == 0

    def test_single_entry_verifies(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {"x": 1})
        report = verify_chain(ledger.read_all())
        assert report.recommendation == "verified"

    def test_multiple_entries_verify(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        for i in range(5):
            ledger.append(f"e{i}", {"i": i})
        report = verify_chain(ledger.read_all())
        assert report.recommendation == "verified"
        assert report.summary == "all 5 entries passed all checks"

    def test_each_entry_passes_all_checks(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        for i in range(3):
            ledger.append(f"e{i}", {"i": i})
        report = verify_chain(ledger.read_all())
        for e in report.entries:
            assert e.payload_hash_ok is True
            assert e.entry_hash_ok is True
            assert e.chain_link_ok is True
            assert e.schema_ok is True


# ============================================================
# verify_chain — tampering detection
# ============================================================

class TestVerifyDetectsTampering:
    def _build_chain(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        for i in range(4):
            ledger.append(f"e{i}", {"i": i})
        return ledger

    def test_payload_tampering_detected(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        entries = ledger.read_all()
        # mutate entry 1's payload (hash should now mismatch)
        entries[1]["payload"]["i"] = 99
        report = verify_chain(entries)
        assert report.recommendation == "tampered"
        # entry 1's payload_hash check should fail
        e1 = report.entries[1]
        assert e1.payload_hash_ok is False

    def test_entry_hash_tampering_detected(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        entries = ledger.read_all()
        # mutate entry 2's entry_hash
        entries[2]["entry_hash"] = "0" * 64
        report = verify_chain(entries)
        assert report.recommendation == "tampered"

    def test_chain_link_break_detected(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        entries = ledger.read_all()
        # mutate entry 2's previous_entry_hash to break the link
        entries[2]["previous_entry_hash"] = "0" * 64
        report = verify_chain(entries)
        assert report.recommendation == "tampered"
        assert 2 in report.chain_breaks

    def test_entry_deletion_detected(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        entries = ledger.read_all()
        # delete entry 2; entry 3's previous_entry_hash now points
        # at entry 2's hash, but entry 1's hash is what's left in the
        # walked position
        del entries[2]
        report = verify_chain(entries)
        assert report.recommendation == "tampered"

    def test_genesis_replacement_detected(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        entries = ledger.read_all()
        # replace entry 0 with a different one (different entry_id)
        # this changes its entry_hash, breaking the link from entry 1
        entries[0]["entry_id"] = "tampered_genesis"
        report = verify_chain(entries)
        assert report.recommendation == "tampered"

    def test_to_dict_round_trip(self, tmp_path):
        ledger = self._build_chain(tmp_path)
        report = verify_chain(ledger.read_all())
        d = report.to_dict()
        assert d["recommendation"] == "verified"
        assert d["n_entries"] == 4
        assert "interpretation_warning" in d

    def test_interpretation_warning_present(self, tmp_path):
        # the load-bearing audit-symmetric guarantee: the verification
        # report explicitly notes that cryptographic integrity ≠
        # substantive correctness. Future regressions must not strip
        # this acknowledgment.
        report = verify_chain([])
        assert "cryptographic integrity" in report.interpretation_warning.lower()
        assert "honest" in report.interpretation_warning.lower() or \
               "correct" in report.interpretation_warning.lower()


# ============================================================
# Schema-level checks
# ============================================================

class TestSchemaChecks:
    def test_missing_required_field_flagged(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {"x": 1})
        entries = ledger.read_all()
        # remove a required field
        del entries[0]["payload_kind"]
        report = verify_chain(entries)
        # schema_ok should be False; payload_kind missing
        assert report.entries[0].schema_ok is False

    def test_wrong_envelope_version_flagged(self, tmp_path):
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {"x": 1})
        entries = ledger.read_all()
        entries[0]["envelope_version"] = "999.0"
        report = verify_chain(entries)
        assert report.entries[0].schema_ok is False


# ============================================================
# Stubs: must report unavailable + raise on use
# ============================================================

class TestStubBackends:
    @pytest.mark.parametrize("cls", [
        EthereumLedger, HyperledgerLedger, IPFSLedger,
    ])
    def test_stub_unavailable_with_helpful_reason(self, cls):
        backend = cls()
        ok, reason = backend.available()
        assert ok is False
        assert "stub" in reason.lower()

    @pytest.mark.parametrize("cls", [
        EthereumLedger, HyperledgerLedger, IPFSLedger,
    ])
    def test_stub_append_raises(self, cls):
        backend = cls()
        with pytest.raises(NotImplementedError):
            backend.append("e1", {"x": 1})

    @pytest.mark.parametrize("cls", [
        EthereumLedger, HyperledgerLedger, IPFSLedger,
    ])
    def test_stub_read_all_raises(self, cls):
        backend = cls()
        with pytest.raises(NotImplementedError):
            backend.read_all()


# ============================================================
# Schema validation against ledger_schema.json
# ============================================================

class TestEnvelopeAgainstSchema:
    def test_clean_envelope_validates(self, tmp_path):
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")
        schema_path = (Path(__file__).parent.parent / "ledger"
                       / "ledger_schema.json")
        with open(schema_path) as f:
            schema = json.load(f)
        ledger = LocalFilesystemLedger(tmp_path / "l.jsonl")
        ledger.append("e1", {"x": 1}, payload_kind="rcr")
        entries = ledger.read_all()
        for entry in entries:
            jsonschema.validate(entry, schema)


# ============================================================
# End-to-end: tamper + verify
# ============================================================

class TestEndToEnd:
    def test_full_lifecycle(self, tmp_path):
        # Anchor a few entries, verify clean, tamper, verify tampered
        ledger = LocalFilesystemLedger(tmp_path / "audit.jsonl")
        ledger.append("anchor-001", {"kind": "rcr", "summary": "first"})
        ledger.append("anchor-002", {"kind": "blind_spot_log"})
        ledger.append("anchor-003", {"kind": "consent_record"})

        clean = verify_chain(ledger.read_all())
        assert clean.recommendation == "verified"

        # Tamper directly with the file
        path = tmp_path / "audit.jsonl"
        with open(path) as f:
            lines = f.readlines()
        tampered = json.loads(lines[1])
        tampered["payload"]["summary"] = "TAMPERED"
        lines[1] = json.dumps(tampered, sort_keys=True,
                              separators=(",", ":")) + "\n"
        with open(path, "w") as f:
            f.writelines(lines)

        tampered_report = verify_chain(ledger.read_all())
        assert tampered_report.recommendation == "tampered"
        assert "anchor-002" in tampered_report.tampered_entries
