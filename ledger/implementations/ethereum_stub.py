# ============================================================
# ETHEREUM ADAPTER — STUB.
#
# Real wiring requires:
#   - an RPC endpoint (Infura, Alchemy, self-hosted node, ...)
#   - a wallet / private key for signing transactions
#   - gas-price strategy
#   - a smart-contract address that accepts entry_hash anchors
#     (the contract's job is to emit an event with the hash;
#     the actual envelope payload lives off-chain)
#
# The standard pattern: anchor only the `entry_hash` on-chain via
# a tiny event-emitting contract. The full envelope (with payload,
# previous_entry_hash, timestamp, etc.) lives in IPFS or local
# storage. Anchoring just the hash on a public chain costs cents
# per anchor; anchoring full payloads would be wasteful and
# privacy-leaky.
#
# Until credentials and contract address are configured, this
# adapter is a stub that records the wiring pattern and refuses
# to operate.
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Dict, List, Optional, Tuple

from ledger.ledger_interface import AppendResult, LedgerBackend


class EthereumLedger(LedgerBackend):
    """
    Stub adapter for Ethereum / Polygon / EVM-compatible chain
    anchoring.

    Wiring pattern (docstring; not implemented):
        1. Configure RPC endpoint URL
        2. Configure wallet / private key (env var, vault, hardware)
        3. Deploy or reference an anchor contract:
            event AnchorEmitted(bytes32 entryHash, uint256 timestamp);
            function anchor(bytes32 entryHash) public {
                emit AnchorEmitted(entryHash, block.timestamp);
            }
        4. Override `append()` to:
            a. Build the envelope locally via build_envelope()
            b. Write the envelope to a separate storage layer
               (IPFS, local file, S3) — anchor_metadata records
               the storage location
            c. Call anchor(entry_hash) on the contract; the tx_hash
               and block_number go into anchor_metadata
            d. Return AppendResult
        5. Override `read_all()` to:
            a. Read envelopes from the storage layer
            b. Optionally cross-check anchor_metadata.tx_hash exists
               on-chain via the RPC endpoint
        6. Override `available()` to check: RPC reachable, wallet
           has gas, anchor contract exists at expected address.

    Trade-off: real public anchoring costs gas per entry
    (~$0.01-$1.00 depending on chain + congestion), takes 10s-2min
    for confirmation, but produces a verification trail anyone in
    the world can confirm without trusting any party.
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
            "EthereumLedger is a stub. See class docstring for wiring "
            "pattern. The audit protocol runs end-to-end offline using "
            "LocalFilesystemLedger."
        )

    def read_all(self) -> List[Dict[str, Any]]:
        raise NotImplementedError(
            "EthereumLedger is a stub. See class docstring."
        )

    def head(self) -> Optional[str]:
        raise NotImplementedError(
            "EthereumLedger is a stub. See class docstring."
        )

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "EthereumLedger is a stub; real wiring requires RPC "
            "endpoint, wallet, and anchor contract. See class "
            "docstring."
        )
