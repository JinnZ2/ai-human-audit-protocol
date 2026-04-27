# Ledger — structural permanence layer

> *The orchestrator's defenses and physics gates are runtime protection. The ledger is structural permanence. Together they prevent both drift and revision.*

This folder is the **anchoring wrapper** that gives any audit-protocol payload — RCR entries, blind-spot log entries, consent records, change events — cryptographic immutability via a backend-agnostic hash chain. It does not redefine what an entry contains (`physics/ledger_schema.json` already does that for substrate-integrity entries); it defines *how* an entry achieves permanence.

---

## What lives here

```
ledger/
├── README.md                       (this file)
├── ledger_schema.json              (anchored-entry envelope — wraps any payload)
├── blockchain_alternatives.md      (three implementation paths + tradeoffs)
├── ledger_interface.py             (abstract LedgerBackend ABC)
├── verification_tools.py           (verify integrity without trusting the system)
└── implementations/
    ├── local_filesystem.py         (reference impl — JSONL hash chain, no external deps)
    ├── ethereum_stub.py            (stub — public blockchain wiring pattern)
    ├── hyperledger_stub.py         (stub — private/consortium blockchain)
    └── ipfs_stub.py                (stub — content-addressed storage)
```

---

## Two layers, stacked

```
PAYLOAD LAYER  (what's in an entry — substrate accounting)
  ├── physics/ledger_schema.json          (RCR entries: Eh+Ea+Ee, C1-C6 checks)
  ├── consortium/audit/blind_spot_log.schema.json  (consortium learning entries)
  ├── consortium/router/consent.py        (ConsentRecord)
  └── (any other JSON-shaped audit artifact)
                          │
                          ▼  (any payload can be anchored)
ANCHOR LAYER   (how an entry achieves permanence — hash chain + backend)
  ├── ledger/ledger_schema.json           (envelope: payload + hash + chain)
  └── ledger/implementations/             (backend choice: local | IPFS | chain)
```

A payload is what it is. The anchor layer wraps the payload with `payload_hash`, `previous_entry_hash`, `timestamp`, and `entry_hash`, then writes it to whichever backend is configured. Verification re-hashes the payload, walks the chain, and reports any tampering.

---

## Why backend-agnostic

Different deployments need different permanence guarantees:

| Backend | When it fits |
|---|---|
| **Local filesystem** (reference impl) | Single-machine offline runs, tests, dry-runs of the audit protocol |
| **IPFS + timestamping** | Distributed storage with cryptographic proof, lighter than full blockchain |
| **Public blockchain** (Ethereum / Polygon) | Maximum decentralization, anyone-can-audit, permanent — at gas cost and latency |
| **Private / consortium chain** (Hyperledger Fabric) | Consortium-internal immutability with controlled access, faster than public |

The `LedgerBackend` ABC is the same shape across all four. The orchestrator logs against the interface; deployment chooses the backend. Swapping is one config change away.

See `ledger/blockchain_alternatives.md` for the full tradeoff matrix.

---

## Audit symmetry

Same stance as everywhere else in this repo:

- **Hash chain is fail-loud.** Tampering is detected on next verification; the verifier does not need to trust the writer. `verify_chain()` returns structured data, not judgment — what matched, what didn't, with what evidence.
- **Backend-stubbed by default.** The three remote backends (`ethereum`, `hyperledger`, `ipfs`) ship as `NotImplementedError` stubs that document the wiring pattern. The local filesystem reference works fully offline and is the test surface.
- **Append-only.** Like `consortium/audit/blind_spot_log.jsonl` and `protocols/change_tracking_v1.0.md`, entries are never modified or deleted. Revocations are new entries that override prior grants when queried.
- **Verification works without the system.** Anyone with the JSONL file and `verification_tools.verify_chain()` can verify integrity. No trust in the writing system required — that's the load-bearing property of structural permanence.

---

## Quick start

```python
from ledger.implementations.local_filesystem import LocalFilesystemLedger
from ledger.verification_tools import verify_chain
from pathlib import Path

# anchor a payload
ledger = LocalFilesystemLedger(Path("./audit.jsonl"))
entry_hash = ledger.append({
    "kind": "rcr",
    "id": "rcr-2026-04-27-001",
    "labor": [{"kind": "E_h", "contributor": "human:naomi", ...}],
    # ...
})

# verify the chain
report = verify_chain(ledger.read_all())
print(report.recommendation)   # "verified" | "tampered" | "incomplete"
print(report.summary)
```

The same `append()` / `read_all()` interface works against any backend. The verification function works against any list of entries that follow the envelope schema.

---

## Cross-links

- `physics/ledger_schema.json` — payload-layer schema for RCR entries
- `physics/substrate_alignment_check.py` — uses RCR entries as input
- `consortium/audit/blind_spot_log.md` — payload-layer for consortium learning
- `protocols/change_tracking_v1.0.md` — the immutability principle this folder mechanizes
- `relational_cognition/coating_detection.md` — why fail-loud verification matters
