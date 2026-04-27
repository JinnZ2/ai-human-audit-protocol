# ============================================================
# LEDGER INTERFACE — backend-agnostic anchored ledger
#
# Abstract base class for any structural-permanence backend. The
# orchestrator (consortium, physics gates, change tracking) logs
# against this interface; the deployment configures which backend.
#
# v1 supports four backends (see ledger/implementations/):
#   - local_filesystem      (reference; works offline)
#   - ethereum_stub         (public blockchain — stub)
#   - hyperledger_stub      (private/consortium chain — stub)
#   - ipfs_stub             (content-addressed storage — stub)
#
# All four implement the same `LedgerBackend` ABC. Swapping is a
# config-change away. Verification is backend-agnostic by
# construction (verification_tools.verify_chain consumes envelope
# entries without caring where they were stored).
# ============================================================

import hashlib
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


ENVELOPE_VERSION = "1.0"
HASH_ALGORITHM = "sha256"


# ------------------------------------------------------------
# Canonical JSON
# ------------------------------------------------------------

def canonicalize(obj: Any) -> str:
    """
    Deterministic JSON serialization for hashing.

    Rules:
      - sort_keys=True   (deterministic field order)
      - separators=(',', ':')  (no extra whitespace)
      - ensure_ascii=False (preserve unicode)

    Two callers that canonicalize the same object MUST produce the
    same byte-string. Tests verify this property.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_hex(data: str) -> str:
    """SHA-256 hex digest of a UTF-8 string."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def hash_payload(payload: Any) -> str:
    """SHA-256 hex digest of the canonical JSON of a payload."""
    return sha256_hex(canonicalize(payload))


def hash_entry_chain_input(
    entry_id: str,
    timestamp: str,
    payload_kind: str,
    payload_hash: str,
    previous_entry_hash: Optional[str],
    hash_algorithm: str = HASH_ALGORITHM,
    envelope_version: str = ENVELOPE_VERSION,
) -> str:
    """
    Compute entry_hash from the chain-input fields. The chain-input
    is everything that would let a verifier confirm position in the
    chain — payload_hash + previous_entry_hash + timestamp + entry_id
    + format metadata.
    """
    chain_input = {
        "entry_id": entry_id,
        "envelope_version": envelope_version,
        "hash_algorithm": hash_algorithm,
        "payload_hash": payload_hash,
        "payload_kind": payload_kind,
        "previous_entry_hash": previous_entry_hash,
        "timestamp": timestamp,
    }
    return sha256_hex(canonicalize(chain_input))


# ------------------------------------------------------------
# Envelope construction
# ------------------------------------------------------------

def build_envelope(
    entry_id: str,
    payload: Any,
    payload_kind: str,
    previous_entry_hash: Optional[str],
    timestamp: Optional[str] = None,
    anchor_metadata: Optional[Dict[str, Any]] = None,
    signatures: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Construct an anchored-entry envelope per `ledger/ledger_schema.json`.

    The envelope wraps `payload` with hash-chain metadata. The
    backend's `append()` is responsible for writing this dict to its
    storage; the envelope itself is backend-agnostic.

    `previous_entry_hash` is None for the genesis entry of a chain.
    `timestamp` defaults to UTC now in ISO 8601.
    """
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()
    payload_hash = hash_payload(payload)
    entry_hash = hash_entry_chain_input(
        entry_id=entry_id,
        timestamp=timestamp,
        payload_kind=payload_kind,
        payload_hash=payload_hash,
        previous_entry_hash=previous_entry_hash,
    )
    envelope: Dict[str, Any] = {
        "envelope_version": ENVELOPE_VERSION,
        "entry_id": entry_id,
        "timestamp": timestamp,
        "payload_kind": payload_kind,
        "payload": payload,
        "payload_hash": payload_hash,
        "previous_entry_hash": previous_entry_hash,
        "entry_hash": entry_hash,
        "hash_algorithm": HASH_ALGORITHM,
    }
    if anchor_metadata is not None:
        envelope["anchor_metadata"] = dict(anchor_metadata)
    if signatures:
        envelope["signatures"] = list(signatures)
    return envelope


# ------------------------------------------------------------
# Result type for append
# ------------------------------------------------------------

@dataclass
class AppendResult:
    """Return value of `LedgerBackend.append()`. Carries the new
    entry's hash + position so callers can chain references."""
    entry_id: str
    entry_hash: str
    payload_hash: str
    previous_entry_hash: Optional[str]
    anchor_metadata: Dict[str, Any]


# ------------------------------------------------------------
# Abstract backend
# ------------------------------------------------------------

class LedgerBackend(ABC):
    """
    Abstract base for any structural-permanence backend.

    Every backend supports four operations:
      - `append(entry_id, payload, payload_kind, ...)` — add an entry
      - `read_all()` — return the full chain (newest last)
      - `head()` — return the most recent entry's hash, or None
      - `available()` — runtime check; returns (bool, reason)

    Subclasses implement the actual storage. The hash-chain logic
    lives in `build_envelope()` above; backends write the envelope
    and read it back.
    """

    @abstractmethod
    def append(
        self,
        entry_id: str,
        payload: Any,
        payload_kind: str = "arbitrary",
        anchor_metadata: Optional[Dict[str, Any]] = None,
        signatures: Optional[List[Dict[str, Any]]] = None,
    ) -> AppendResult:
        """Append a new entry to the chain. Computes envelope and
        writes to backend storage. Returns AppendResult with the new
        entry_hash + position."""
        raise NotImplementedError

    @abstractmethod
    def read_all(self) -> List[Dict[str, Any]]:
        """Return all envelope entries, in chain order (oldest first)."""
        raise NotImplementedError

    @abstractmethod
    def head(self) -> Optional[str]:
        """Return the most recent entry's `entry_hash`, or None if
        the chain is empty."""
        raise NotImplementedError

    @abstractmethod
    def available(self) -> "tuple[bool, str]":
        """Runtime availability check. Returns (True, '') when ready;
        (False, reason) when not (missing credentials, network down,
        etc.)."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
