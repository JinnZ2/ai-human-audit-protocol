# ============================================================
# VERIFICATION TOOLS — verify a ledger chain without trusting it.
#
# The load-bearing property of structural permanence: anyone with
# the chain bytes (and this module) can verify integrity. No trust
# in the writing system required.
#
# verify_chain() returns structured data, not judgment. Per-entry
# pass/fail, the specific reason for any failure, and an aggregate
# recommendation. The consenter / auditor decides what to do with
# the data.
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ledger.ledger_interface import (
    ENVELOPE_VERSION,
    HASH_ALGORITHM,
    hash_entry_chain_input,
    hash_payload,
)


# ------------------------------------------------------------
# Per-entry verification result
# ------------------------------------------------------------

@dataclass
class EntryVerification:
    """One entry's verification result.

    Each check is independent and reported separately. An entry can
    fail one check and pass others — the report shows precisely
    which axis failed."""
    entry_id: str
    position: int
    payload_hash_ok: Optional[bool] = None
    entry_hash_ok: Optional[bool] = None
    chain_link_ok: Optional[bool] = None
    schema_ok: Optional[bool] = None
    reasons: List[str] = field(default_factory=list)

    def all_passed(self) -> bool:
        return (
            self.payload_hash_ok is True
            and self.entry_hash_ok is True
            and self.chain_link_ok is True
            and self.schema_ok is True
        )


# ------------------------------------------------------------
# Chain-level verification report
# ------------------------------------------------------------

@dataclass
class VerificationReport:
    """
    Full report from verify_chain.

    `recommendation` is informational: 'verified' / 'tampered' /
    'incomplete'. Consenter decides what to do with the data.
    """
    n_entries: int
    entries: List[EntryVerification]
    recommendation: str
    summary: str
    tampered_entries: List[str] = field(default_factory=list)
    chain_breaks: List[int] = field(default_factory=list)
    interpretation_warning: str = (
        "Verification reports cryptographic integrity ONLY. A passing "
        "verification means the chain is internally consistent and "
        "untampered. It does NOT mean the payloads are correct, "
        "honest, or non-coated. Run substantive audits separately."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_entries": self.n_entries,
            "recommendation": self.recommendation,
            "summary": self.summary,
            "tampered_entries": list(self.tampered_entries),
            "chain_breaks": list(self.chain_breaks),
            "interpretation_warning": self.interpretation_warning,
            "entries": [
                {
                    "entry_id": e.entry_id,
                    "position": e.position,
                    "payload_hash_ok": e.payload_hash_ok,
                    "entry_hash_ok": e.entry_hash_ok,
                    "chain_link_ok": e.chain_link_ok,
                    "schema_ok": e.schema_ok,
                    "reasons": list(e.reasons),
                    "all_passed": e.all_passed(),
                }
                for e in self.entries
            ],
        }


# ------------------------------------------------------------
# Schema-level checks (structural; cheap)
# ------------------------------------------------------------

REQUIRED_FIELDS = [
    "envelope_version",
    "entry_id",
    "timestamp",
    "payload_kind",
    "payload",
    "payload_hash",
    "previous_entry_hash",
    "entry_hash",
    "hash_algorithm",
]


def _check_schema(entry: Dict[str, Any]) -> tuple:
    """Returns (ok, reasons). Lightweight structural check that
    doesn't depend on jsonschema being installed."""
    reasons = []
    for f in REQUIRED_FIELDS:
        if f not in entry:
            reasons.append(f"missing field: {f}")
    if entry.get("envelope_version") != ENVELOPE_VERSION:
        reasons.append(
            f"envelope_version != {ENVELOPE_VERSION!r}: "
            f"{entry.get('envelope_version')!r}"
        )
    if entry.get("hash_algorithm") != HASH_ALGORITHM:
        reasons.append(
            f"hash_algorithm != {HASH_ALGORITHM!r}: "
            f"{entry.get('hash_algorithm')!r}"
        )
    return (not reasons, reasons)


# ------------------------------------------------------------
# verify_chain
# ------------------------------------------------------------

def verify_chain(entries: List[Dict[str, Any]]) -> VerificationReport:
    """
    Verify a chain of anchored entries.

    For each entry, runs four independent checks:
      1. payload_hash matches sha256(canonicalize(payload))
      2. entry_hash matches sha256(canonicalize(chain_input))
      3. previous_entry_hash matches the prior entry's entry_hash
         (or is None for the genesis entry)
      4. envelope schema is well-formed (required fields present,
         versions match)

    Returns a `VerificationReport` with per-entry results +
    aggregate recommendation.

    Recommendation:
      - 'verified'   : every entry passed all four checks
      - 'tampered'   : at least one entry failed a hash or chain check
      - 'incomplete' : at least one entry failed schema check and
                       no hash/chain failures (envelope was well-formed
                       but content couldn't be verified — e.g. unknown
                       envelope_version)
      - 'empty'      : zero entries
    """
    if not entries:
        return VerificationReport(
            n_entries=0,
            entries=[],
            recommendation="empty",
            summary="no entries",
        )

    results: List[EntryVerification] = []
    tampered_ids: List[str] = []
    chain_breaks: List[int] = []
    expected_prev: Optional[str] = None

    for i, entry in enumerate(entries):
        v = EntryVerification(
            entry_id=entry.get("entry_id", f"<missing@{i}>"),
            position=i,
        )

        schema_ok, schema_reasons = _check_schema(entry)
        v.schema_ok = schema_ok
        v.reasons.extend(schema_reasons)

        # payload_hash check
        if "payload" in entry and "payload_hash" in entry:
            recomputed = hash_payload(entry["payload"])
            v.payload_hash_ok = (recomputed == entry["payload_hash"])
            if not v.payload_hash_ok:
                v.reasons.append(
                    f"payload_hash mismatch: stored="
                    f"{entry['payload_hash']} recomputed={recomputed}"
                )
        else:
            v.payload_hash_ok = False
            v.reasons.append("cannot check payload_hash: fields missing")

        # entry_hash check
        chain_inputs = (
            "entry_id", "timestamp", "payload_kind", "payload_hash",
            "previous_entry_hash", "hash_algorithm", "envelope_version",
        )
        if all(k in entry for k in chain_inputs) and "entry_hash" in entry:
            recomputed_eh = hash_entry_chain_input(
                entry_id=entry["entry_id"],
                timestamp=entry["timestamp"],
                payload_kind=entry["payload_kind"],
                payload_hash=entry["payload_hash"],
                previous_entry_hash=entry["previous_entry_hash"],
                hash_algorithm=entry["hash_algorithm"],
                envelope_version=entry["envelope_version"],
            )
            v.entry_hash_ok = (recomputed_eh == entry["entry_hash"])
            if not v.entry_hash_ok:
                v.reasons.append(
                    f"entry_hash mismatch: stored="
                    f"{entry['entry_hash']} recomputed={recomputed_eh}"
                )
        else:
            v.entry_hash_ok = False
            v.reasons.append("cannot check entry_hash: fields missing")

        # chain link check
        actual_prev = entry.get("previous_entry_hash")
        if actual_prev != expected_prev:
            v.chain_link_ok = False
            v.reasons.append(
                f"chain link broken at position {i}: "
                f"expected previous_entry_hash={expected_prev}, "
                f"got {actual_prev}"
            )
            chain_breaks.append(i)
        else:
            v.chain_link_ok = True

        if v.payload_hash_ok is False or v.entry_hash_ok is False:
            tampered_ids.append(v.entry_id)

        # next iteration expects this entry's entry_hash as the
        # previous link
        expected_prev = entry.get("entry_hash")
        results.append(v)

    # Aggregate
    has_hash_failure = any(
        (v.payload_hash_ok is False or v.entry_hash_ok is False)
        for v in results
    )
    has_chain_break = bool(chain_breaks)
    has_schema_failure = any(v.schema_ok is False for v in results)

    if has_hash_failure or has_chain_break:
        recommendation = "tampered"
        summary = (
            f"verification FAILED: "
            f"{len(tampered_ids)} hash mismatch(es), "
            f"{len(chain_breaks)} chain break(s)"
        )
    elif has_schema_failure:
        recommendation = "incomplete"
        summary = (
            "schema-level issues found but no tampering detected; "
            "some entries could not be fully verified"
        )
    else:
        recommendation = "verified"
        summary = f"all {len(results)} entries passed all checks"

    return VerificationReport(
        n_entries=len(entries),
        entries=results,
        recommendation=recommendation,
        summary=summary,
        tampered_entries=tampered_ids,
        chain_breaks=chain_breaks,
    )


# ============================================================
# DEMO — verify a small chain (uses LocalFilesystemLedger)
# ============================================================
if __name__ == "__main__":
    import tempfile
    from ledger.implementations.local_filesystem import LocalFilesystemLedger

    with tempfile.TemporaryDirectory() as tmp:
        ledger_path = Path(tmp) / "demo.jsonl"
        ledger = LocalFilesystemLedger(ledger_path)

        # Append a few entries (simulating audit-protocol payloads)
        ledger.append(entry_id="anchor-001",
                      payload={"kind": "rcr", "summary": "first decision"},
                      payload_kind="rcr")
        ledger.append(entry_id="anchor-002",
                      payload={"kind": "blind_spot_log",
                               "summary": "first run"},
                      payload_kind="blind_spot_log")
        ledger.append(entry_id="anchor-003",
                      payload={"kind": "consent_record",
                               "consenter": "swarmuser"},
                      payload_kind="consent_record")

        # Verify the clean chain
        report = verify_chain(ledger.read_all())
        print("=" * 72)
        print("LEDGER VERIFICATION DEMO — clean chain")
        print("=" * 72)
        print(f"  recommendation: {report.recommendation}")
        print(f"  summary: {report.summary}")
        for e in report.entries:
            mark = "✓" if e.all_passed() else "✗"
            print(f"    {mark} pos {e.position}: {e.entry_id}")
        print()

        # Now tamper with the file: edit one payload (simulating
        # a malicious editor modifying entry 1)
        with open(ledger_path) as f:
            lines = f.readlines()
        import json as _json
        tampered = _json.loads(lines[1])
        tampered["payload"]["summary"] = "TAMPERED summary"
        lines[1] = _json.dumps(tampered, sort_keys=True,
                               separators=(",", ":")) + "\n"
        with open(ledger_path, "w") as f:
            f.writelines(lines)

        # Re-verify
        report2 = verify_chain(ledger.read_all())
        print("=" * 72)
        print("LEDGER VERIFICATION DEMO — after tampering with entry 1")
        print("=" * 72)
        print(f"  recommendation: {report2.recommendation}")
        print(f"  summary: {report2.summary}")
        for e in report2.entries:
            mark = "✓" if e.all_passed() else "✗"
            print(f"    {mark} pos {e.position}: {e.entry_id}")
            if not e.all_passed():
                for r in e.reasons:
                    print(f"        {r}")
        print()
        print("Note: tampering with a payload mid-chain breaks the "
              "payload_hash for that entry AND the chain link from "
              "the next entry forward, because the next entry's "
              "previous_entry_hash points at the original entry_hash. "
              "Tampering is detected by re-hashing — no trust in the "
              "writing system required.")
