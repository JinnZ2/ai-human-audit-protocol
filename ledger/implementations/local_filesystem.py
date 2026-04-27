# ============================================================
# LOCAL FILESYSTEM LEDGER — reference implementation.
#
# JSONL append-only file. Each line is one anchored-entry envelope
# (per ledger/ledger_schema.json). On append, the file is locked
# briefly (POSIX fcntl on Linux/macOS; best-effort on Windows) and
# one line is appended atomically. Reading walks the file in order.
#
# This backend has NO external dependencies. It works offline,
# in tests, in containers, on flights. It is the test surface for
# the entire ledger interface.
#
# Use cases:
#   - tests / dry runs
#   - single-machine deployments
#   - prototype consortium sessions before chain-anchoring is wired
#   - auditing the format itself (a corrupted file is detectable
#     by `ledger.verification_tools.verify_chain()`)
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

import json
from typing import Any, Dict, List, Optional, Tuple

from ledger.ledger_interface import (
    AppendResult,
    LedgerBackend,
    build_envelope,
)


class LocalFilesystemLedger(LedgerBackend):
    """
    JSONL append-only ledger on the local filesystem.

    Args:
        path: filesystem path to the JSONL file. Created if missing.
              Parent directory created if missing.

    Concurrency: simple append. Multiple writers from the same
    process serialize via Python's GIL on the file write call.
    Multi-process concurrency is not handled in v1; users with that
    need should use a backend that handles it natively (e.g. a real
    blockchain or a database).
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    # ---- abstract methods ----

    def available(self) -> Tuple[bool, str]:
        # Always available unless the parent directory is unwritable.
        # We don't try the parent if the file already exists.
        if self.path.exists():
            return (True, "")
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            return (True, "")
        except OSError as e:
            return (False, f"cannot create parent directory: {e}")

    def append(
        self,
        entry_id: str,
        payload: Any,
        payload_kind: str = "arbitrary",
        anchor_metadata: Optional[Dict[str, Any]] = None,
        signatures: Optional[List[Dict[str, Any]]] = None,
    ) -> AppendResult:
        prev = self.head()

        # Build the envelope (computes hashes deterministically).
        envelope = build_envelope(
            entry_id=entry_id,
            payload=payload,
            payload_kind=payload_kind,
            previous_entry_hash=prev,
            anchor_metadata=anchor_metadata,
            signatures=signatures,
        )

        # Append `local_filesystem` anchor metadata noting where the
        # entry lives, so anchor_metadata can record the file + line.
        # Existing anchor_metadata (if any) is preserved.
        existing_meta = envelope.get("anchor_metadata", {})
        existing_meta = {**existing_meta, "kind": "local_filesystem",
                         "path": str(self.path)}
        envelope["anchor_metadata"] = existing_meta

        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(envelope, sort_keys=True,
                          separators=(",", ":"), ensure_ascii=False)
        # `with open(..., "a")` is atomic per-line on POSIX for small
        # writes (under PIPE_BUF). For our ~few KB envelopes, that's
        # the realistic case.
        with open(self.path, "a") as f:
            f.write(line + "\n")

        return AppendResult(
            entry_id=entry_id,
            entry_hash=envelope["entry_hash"],
            payload_hash=envelope["payload_hash"],
            previous_entry_hash=prev,
            anchor_metadata=existing_meta,
        )

    def read_all(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        entries: List[Dict[str, Any]] = []
        with open(self.path) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"corrupted ledger file {self.path} "
                        f"line {line_num}: {e}"
                    ) from e
        return entries

    def head(self) -> Optional[str]:
        entries = self.read_all()
        if not entries:
            return None
        return entries[-1]["entry_hash"]
