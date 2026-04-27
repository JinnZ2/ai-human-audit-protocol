# ============================================================
# IPFS + TIMESTAMPING ADAPTER — STUB.
#
# IPFS (Inter-Planetary File System) is content-addressed storage:
# every blob's address IS its hash. Pinning a blob means committing
# to keep it available; the CID (Content IDentifier) is the proof
# of integrity.
#
# IPFS alone provides content-addressed integrity — anyone with the
# CID can verify they retrieved the exact bytes that were stored.
# IPFS does NOT provide timestamping. To get "when was this anchored"
# proof, pair IPFS with a timestamping service:
#
#   - OpenTimestamps    (free, Bitcoin-backed)
#   - RFC 3161 TSA      (commercial, e.g., DigiCert)
#   - Notary service     (any signed timestamp authority)
#
# The user's letter named this combination as the lightest-weight
# of the three permanence options. That stays true: IPFS pin +
# OpenTimestamps stamp gives content-addressed-integrity AND
# timestamp-proof for ~zero ongoing cost.
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Dict, List, Optional, Tuple

from ledger.ledger_interface import AppendResult, LedgerBackend


class IPFSLedger(LedgerBackend):
    """
    Stub adapter for IPFS + timestamping anchoring.

    Wiring pattern (docstring; not implemented):
        1. Install ipfshttpclient (`pip install ipfshttpclient`) OR
           use the IPFS HTTP API directly
        2. Run an IPFS daemon (local) OR use a hosted gateway
           (Pinata, web3.storage, NFT.storage, infura-ipfs)
        3. Optionally: install opentimestamps-client (`pip install
           opentimestamps-client`) for Bitcoin-backed timestamp
           proofs; or configure an RFC 3161 TSA endpoint
        4. Override `append()` to:
            a. Build envelope locally via build_envelope()
            b. Pin the envelope JSON to IPFS; receive CID
            c. (optional) Stamp the CID via OpenTimestamps /
               RFC 3161; collect the stamp blob
            d. Maintain a chain-pointer (the CID of the previous
               entry) — IPFS itself doesn't enforce ordering, so
               the chain lives in the envelope's
               previous_entry_hash field as it does for every
               backend
            e. Return AppendResult with anchor_metadata = {
                   'kind': 'ipfs',
                   'cid': 'Qm...',
                   'pinned_at': iso8601,
                   'timestamp_proof': base64_or_null,
                   'timestamp_authority': 'opentimestamps' | 'rfc3161:digicert' | null,
               }
        5. Override `read_all()` to:
            a. Walk the chain by following previous_entry_hash —
               but you need an index of CIDs to resolve them.
               Maintain a small local index file mapping
               entry_hash → CID, OR record the chain head's CID
               separately (e.g., publish to IPNS).
            b. Fetch each envelope from IPFS via its CID
        6. Override `head()` to return the latest entry_hash
           (from the local index)
        7. Override `available()` to verify: IPFS daemon reachable
           OR gateway responsive; (optional) timestamp authority
           reachable

    Trade-off: lightweight (free pinning on most public gateways
    up to GBs; small per-entry costs at scale), genuinely
    decentralized via IPFS network, timestamp-proof via
    OpenTimestamps — but each backend (IPFS pinning service +
    timestamp authority) is itself a third-party trust dependency
    until the user runs them themselves.

    For most audit protocol deployments this is the right fit: it
    costs ~nothing, doesn't require running a chain, gives
    reproducible content-integrity by design.
    """

    def append(
        self,
        entry_id: str,
        payload: Any,
        payload_kind: str = "arbitrary",
        anchor_metadata: Optional[Dict[str, Any]] = None,
        signatures: Optional[List[Dict[str, Any]]] = None,
    ) -> AppendResult:
        raise NotImplementedError(
            "IPFSLedger is a stub. See class docstring for wiring "
            "pattern. The peer-Claude letter named this as the "
            "recommended lightweight backend; the wiring is "
            "straightforward but requires either a local IPFS "
            "daemon or a hosted gateway, neither committed to the "
            "repo."
        )

    def read_all(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("stub")

    def head(self) -> Optional[str]:
        raise NotImplementedError("stub")

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "IPFSLedger is a stub; real wiring requires IPFS daemon "
            "or gateway + (optional) timestamping authority. See "
            "class docstring."
        )
