# Blockchain Alternatives — three implementation paths

The `ledger/` folder presents one abstract interface (`LedgerBackend`) and four concrete backends:

1. **`local_filesystem`** — reference implementation, no external deps. Always works.
2. **`ipfs_stub`** — content-addressed storage + timestamping. Lightweight, decentralized.
3. **`ethereum_stub`** — public blockchain. Maximum decentralization.
4. **`hyperledger_stub`** — private/consortium blockchain. Permissioned immutability.

Stubs raise `NotImplementedError` until wired with credentials or infrastructure. The local filesystem backend is the test surface and the offline default. This document is the decision matrix for which backend fits which deployment.

---

## Quick comparison

| Property | local_filesystem | ipfs+timestamp | public chain | private chain |
|---|---|---|---|---|
| External dependencies | none | IPFS daemon or gateway | RPC endpoint + wallet | Fabric SDK + consortium |
| Cost per entry | $0 | $0 (free pinning) | $0.01 – $1.00 | $0 |
| Confirmation latency | ms | seconds | 10s – 2min | 1 – 2 sec |
| Anyone-in-the-world verifiable | no (need the file) | yes (CID + timestamp) | yes (chain + tx) | no (need consortium read) |
| Censorship-resistant | no | partial | yes | no |
| Decentralized | no | yes | yes | no (consortium-controlled) |
| Setup complexity | none | low | medium | high |
| Storage privacy (payload off-chain) | n/a | depends on pinning | yes (just hash on-chain) | configurable |
| Best for | tests, dry-runs, single-machine | most deployments | maximum trust-minimization | controlled consortium |

---

## When to use which

### Local filesystem
**When:** development, tests, dry-runs, single-machine deployments, offline use.

**Why:** zero dependencies, instant, well-understood. The reference implementation. Every test in `tests/test_ledger.py` runs against this backend, so its correctness is the most thoroughly exercised.

**Limitations:** the file lives on one machine. If that machine is compromised, the chain can be tampered with. Verification still detects the tampering — but the *availability* of the chain depends on one node.

### IPFS + timestamping (recommended for most deployments)
**When:** the consortium needs decentralized storage + timestamp proof but does not need every audit entry to incur gas. Most audit-protocol deployments fit here.

**Why:** IPFS gives content-addressed integrity (the CID *is* the hash; retrieving by CID guarantees the bytes match). Pairing with OpenTimestamps or RFC 3161 adds timestamp proof at near-zero cost. Anyone with the CID and the timestamp blob can verify integrity + when-it-was-anchored without trusting any single party.

**Trade-off:** each backing service (IPFS pinning, timestamp authority) is itself a third-party until the consortium runs them themselves. Pinning services can drop content if the bill isn't paid; timestamp authorities can disappear. Mitigations: pin to multiple services; archive timestamp blobs locally.

**Recommended for the audit protocol** because: low operational cost, decentralized by default, no per-entry gas, easy for "the seven knowledge holders" or any auditor to verify offline.

### Public blockchain (Ethereum / Polygon)
**When:** maximum trust-minimization. The consortium wants any party in the world, in any future, to be able to verify entries existed at the recorded time without trusting the consortium itself.

**Why:** public chains are the strongest immutability guarantee available. Tampering with a confirmed transaction requires reorganizing the entire chain — possible in theory, infeasible in practice for a chain with significant economic security.

**Trade-off:** gas cost per entry (Polygon is ~$0.01, Ethereum mainnet has ranged $0.50–$50 over recent years). Confirmation latency 10s to several minutes. Wallet management. The pattern is to anchor only the `entry_hash` on-chain (a tiny event-emitting contract); the actual envelope payload lives off-chain in IPFS or local storage. This keeps gas costs minimal and avoids leaking payload contents on-chain.

**When this fits the audit protocol:** when one or more of these is true:
- the audit covers a domain with adversarial parties (regulatory, legal, contested resource use)
- the consortium wants seven-generation verifiability without committing to keep its own infrastructure running for 175 years
- the audit might one day be reviewed by parties who do not exist yet

### Private / consortium blockchain (Hyperledger Fabric)
**When:** the consortium wants chain-strength immutability *internal to the consortium* without paying gas costs and without making entries public.

**Why:** Fabric is purpose-built for permissioned multi-party ledgers. Consortium members issue each other certificates, share a channel, and write to a chaincode that records anchors. Faster than public chain, no gas, controlled access.

**Trade-off:** outside parties cannot verify without being granted read access. Setting up a Fabric network is a real infrastructure project (orderer + peers + CAs + chaincode + identity management). The consortium owns its own immutability — including the responsibility for keeping the network running.

**When this fits the audit protocol:** when the consortium has the operational capacity to run shared infrastructure AND wants immutability that does not depend on any external service AND does not need outside-world verifiability. Research consortia, cooperatives, and tribal/regional governance bodies often fit.

---

## How to choose

Honest decision tree:

```
Are you running tests / dev / a single machine?
  → local_filesystem

Do you need outside-world verifiability without trusting anyone?
  Yes:
    Can you afford gas + latency per entry?
      Yes → public chain (Polygon for cost; Ethereum for legitimacy)
      No  → ipfs + timestamp
  No (consortium-internal verifiability is sufficient):
    Will the consortium operate shared infrastructure long-term?
      Yes → private chain (Hyperledger Fabric)
      No  → ipfs + timestamp (also works for internal audits;
            the CID is still verifiable internally)
```

**Default recommendation: ipfs + timestamp.** It's the lightest weight option that gives genuine cryptographic permanence with broad verifiability. Move to public chain when adversarial conditions demand it; move to private chain when the consortium has the operational capacity.

---

## Swapping backends

The `LedgerBackend` interface is the same shape across all four. Switching is one line:

```python
# from
ledger = LocalFilesystemLedger(Path("./audit.jsonl"))

# to (when wired)
ledger = IPFSLedger(gateway_url="...", timestamp_authority="...")
# or
ledger = EthereumLedger(rpc_url="...", contract_address="...", wallet=...)
# or
ledger = HyperledgerLedger(channel="...", chaincode="...", identity=...)

# everything downstream is identical
ledger.append(entry_id="...", payload={...}, payload_kind="rcr")
```

`verification_tools.verify_chain()` is backend-agnostic by construction: it operates on the list of envelopes returned by `read_all()`, regardless of where they were stored.

---

## Wiring a real backend

When you decide to wire one of the stubs:

1. **Read the class docstring.** Each stub documents the wiring pattern step-by-step.
2. **Open a separate change event.** Wiring a real backend introduces dependencies, credentials, and per-deployment configuration. Per `protocols/change_tracking_v1.0.md` it gets its own consent record.
3. **Add tests against a fake / sandbox.** Real backend tests need either a hosted sandbox (Polygon Mumbai, Goerli, IPFS local node) or recorded fixtures. Don't make CI hit live mainnet.
4. **Verify the contract.** Before going live, run `verify_chain()` against a few test anchors. The cryptographic guarantees this layer offers are only as strong as the backend's actual immutability.

---

## What this layer does NOT do

- It does NOT validate payload semantics. A perfectly-anchored RCR entry that violates conservation law is still a violation; the ledger just makes the record permanent. Substantive audit (`physics/substrate_alignment_check.py`) is separate.
- It does NOT prevent adversaries from publishing FALSE payloads with VALID hashes. The chain proves the payload was anchored at time T; it does not prove the payload's claims are true.
- It does NOT replace consent (`consortium/router/consent.py`). Anchoring a record does not authorize the action it records; consent does that, and consent records can themselves be anchored.

The layer's load-bearing claim is narrow and exact: **once an entry is anchored, modifying it without breaking the chain is computationally infeasible**. That's the structural permanence the orchestrator's runtime defenses cannot give on their own.
