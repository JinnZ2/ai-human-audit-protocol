# ============================================================
# HYPERLEDGER FABRIC ADAPTER — STUB.
#
# Hyperledger Fabric is a permissioned, consortium-internal chain.
# Trades public verifiability for: faster confirmation (1-2 sec),
# zero per-tx cost, controlled access (only consortium members
# can write), and standard enterprise features (TLS, KMS, etc.).
#
# Use case: a research consortium, a cooperative, or any group
# that wants immutability + fast writes + access control, but
# does not need anyone-in-the-world verifiability. The seven
# knowledge holders mentioned in the project framing fit this
# shape exactly.
#
# Wiring requires:
#   - Fabric SDK (fabric-sdk-py or hyperledger-fabric-sdk-py)
#   - Channel + chaincode deployed
#   - Member identity / certificate issued by the consortium CA
#   - Endorsement policy configured
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Dict, List, Optional, Tuple

from ledger.ledger_interface import AppendResult, LedgerBackend


class HyperledgerLedger(LedgerBackend):
    """
    Stub adapter for Hyperledger Fabric (private/consortium chain).

    Wiring pattern (docstring; not implemented):
        1. Install Fabric SDK (`pip install fabric-sdk-py` or
           preferred binding)
        2. Stand up Fabric network: orderer + peer nodes + CA,
           OR connect to existing consortium network
        3. Deploy chaincode (smart contract) that implements:
            function anchor(entryHash, payloadKind, timestamp)
                writes hash + metadata to the chaincode's state DB
            function getEntry(entryHash)
                returns the recorded anchor
        4. Issue member identity (certificate from consortium CA)
        5. Override `append()` to:
            a. Build envelope locally
            b. Write envelope to a storage layer (or store payload
               itself on-chain if size permits and privacy allows)
            c. Submit anchor() chaincode invocation; collect tx_id
            d. Return AppendResult with anchor_metadata = {
                   'kind': 'hyperledger',
                   'channel': '...',
                   'tx_id': '...',
                   'block_number': ...,
               }
        6. Override `read_all()` and `head()` to query chaincode
           via the SDK
        7. Override `available()` to verify: SDK installed, member
           certificate present + valid, channel reachable

    Trade-off: faster than public chain (1-2 sec confirmation), no
    gas cost, controlled access — but verifiability is bounded by
    who can join the consortium. Outsiders cannot verify without
    being granted read access, unlike public chain.
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
            "HyperledgerLedger is a stub. See class docstring for "
            "wiring pattern."
        )

    def read_all(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("stub")

    def head(self) -> Optional[str]:
        raise NotImplementedError("stub")

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "HyperledgerLedger is a stub; real wiring requires Fabric "
            "SDK + consortium membership. See class docstring."
        )
