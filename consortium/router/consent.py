# ============================================================
# CONSENT GATE — fail-closed authorization for fan-out queries.
# A consortium query that hits external model adapters costs money
# and discloses the problem text to third parties. Every external
# query needs an explicit consent record. Missing consent = refused.
# CC0 | consortium/router/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ConsentRecord:
    """
    A consent grant for a (problem_id, adapter) pair.

    The record names what was disclosed (the cost), who consented,
    and which adapters were authorized. It is immutable once created;
    revocation is recorded as a new record with `revoked=True`.
    """
    timestamp: datetime
    problem_id: str
    adapters_authorized: List[str]   # adapter frame_ids
    cost_disclosed: Dict[str, Any]   # per-adapter cost estimates
    consenter: str                   # who granted consent
    notes: str = ""
    revoked: bool = False


class ConsentDenied(Exception):
    """Raised when a query is attempted without consent."""


class ConsentGate:
    """
    Fail-closed consent authority for consortium queries.

    Default: no adapter is authorized for any problem. Authorization
    is granted explicitly via `grant()` and may name a subset of
    adapters. A query for an adapter not in that subset is refused.

    The gate keeps an immutable history of every consent decision
    (grants, refusals, revocations) for audit. The dispatcher
    consults the gate via `is_authorized()` before calling
    `adapter.query()`.

    Out of scope (open): persistent storage; cross-session consent;
    revocation propagation to in-flight queries; granular per-call
    cost ceilings. v1 is in-memory and per-session.
    """

    def __init__(self):
        self._records: List[ConsentRecord] = []

    # ---- granting ----

    def grant(
        self,
        problem_id: str,
        adapters_authorized: List[str],
        cost_disclosed: Dict[str, Any],
        consenter: str,
        notes: str = "",
    ) -> ConsentRecord:
        """
        Grant consent for the named adapters on the given problem.
        Returns the recorded `ConsentRecord`.
        """
        record = ConsentRecord(
            timestamp=datetime.now(timezone.utc),
            problem_id=problem_id,
            adapters_authorized=list(adapters_authorized),
            cost_disclosed=dict(cost_disclosed),
            consenter=consenter,
            notes=notes,
            revoked=False,
        )
        self._records.append(record)
        return record

    def revoke(
        self,
        problem_id: str,
        adapters: Optional[List[str]] = None,
        consenter: str = "",
        notes: str = "",
    ) -> ConsentRecord:
        """
        Revoke consent for the named adapters on a problem. Recorded
        as a new immutable entry; does not delete prior grants.
        """
        record = ConsentRecord(
            timestamp=datetime.now(timezone.utc),
            problem_id=problem_id,
            adapters_authorized=list(adapters) if adapters is not None
                                 else [],
            cost_disclosed={},
            consenter=consenter,
            notes=notes,
            revoked=True,
        )
        self._records.append(record)
        return record

    # ---- checking ----

    def is_authorized(
        self,
        problem_id: str,
        adapter_id: str,
    ) -> Tuple[bool, str]:
        """
        Check whether `adapter_id` is currently authorized for
        `problem_id`. Returns (True, "") when authorized,
        (False, reason) otherwise. Fails closed.
        """
        # walk records in order; later records can revoke earlier
        # grants for the same (problem_id, adapter_id)
        latest_decision: Optional[bool] = None
        latest_note = ""
        for r in self._records:
            if r.problem_id != problem_id:
                continue
            if adapter_id not in r.adapters_authorized:
                continue
            latest_decision = not r.revoked
            latest_note = r.notes if r.revoked else ""

        if latest_decision is True:
            return (True, "")
        if latest_decision is False:
            return (False, f"consent revoked: {latest_note}".strip(": "))
        return (False, "no consent record for this (problem, adapter)")

    def assert_authorized(
        self,
        problem_id: str,
        adapter_id: str,
    ) -> None:
        """Raise `ConsentDenied` if the (problem, adapter) pair is
        not authorized."""
        ok, reason = self.is_authorized(problem_id, adapter_id)
        if not ok:
            raise ConsentDenied(
                f"adapter={adapter_id!r} not authorized for "
                f"problem={problem_id!r}: {reason}"
            )

    # ---- audit ----

    def records(
        self,
        problem_id: Optional[str] = None,
    ) -> List[ConsentRecord]:
        """Return all consent records, optionally filtered by problem_id.
        Records are returned in insertion order."""
        if problem_id is None:
            return list(self._records)
        return [r for r in self._records if r.problem_id == problem_id]


# ------------------------------------------------------------
# Persistent variant — JSONL append-only on disk
# ------------------------------------------------------------

class PersistentConsentGate(ConsentGate):
    """
    `ConsentGate` that survives process restarts.

    Records are persisted to a JSONL file (one record per line,
    append-only). On construction the file is read and any prior
    records are loaded into memory. On every grant / revoke, the
    new record is appended to the file immediately — there is no
    "save now" call.

    Append-only is the audit-symmetric default: revocations are
    recorded as new entries that override prior grants when queried,
    but the prior grants are not deleted from the file. The full
    history is recoverable.

    Concurrency: this v1 uses simple flock-free append. Two writers
    may interleave a partial write under high concurrency. For
    production use, future versions can wrap appends in `fcntl.flock`
    (POSIX) or move to sqlite. v1 is fine for single-process /
    single-session use, which is what the consortium currently
    requires.

    File format: one JSON object per line.
        {"timestamp": "...", "problem_id": "...", "adapters_authorized":
         [...], "cost_disclosed": {...}, "consenter": "...",
         "notes": "...", "revoked": false}
    """

    def __init__(self, log_path: "Path"):
        super().__init__()
        from pathlib import Path as _Path
        self.log_path = _Path(log_path)
        self._load()

    def _load(self) -> None:
        """Read prior records from disk into memory. Tolerant of
        missing file (treated as empty); strict on malformed lines
        (raises so the caller knows the log is corrupted)."""
        import json
        from datetime import datetime
        if not self.log_path.exists():
            return
        with open(self.log_path) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"corrupted consent log at "
                        f"{self.log_path}:{line_num}: {e}"
                    ) from e
                self._records.append(ConsentRecord(
                    timestamp=datetime.fromisoformat(
                        data["timestamp"].replace("Z", "+00:00")
                    ),
                    problem_id=data["problem_id"],
                    adapters_authorized=list(data["adapters_authorized"]),
                    cost_disclosed=dict(data["cost_disclosed"]),
                    consenter=data["consenter"],
                    notes=data.get("notes", ""),
                    revoked=bool(data.get("revoked", False)),
                ))

    def _append(self, record: ConsentRecord) -> None:
        """Append one record to the JSONL file. Atomic per-line."""
        import json
        # ensure parent directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": record.timestamp.isoformat(),
            "problem_id": record.problem_id,
            "adapters_authorized": list(record.adapters_authorized),
            "cost_disclosed": dict(record.cost_disclosed),
            "consenter": record.consenter,
            "notes": record.notes,
            "revoked": record.revoked,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(payload) + "\n")

    def grant(
        self,
        problem_id: str,
        adapters_authorized: List[str],
        cost_disclosed: Dict[str, Any],
        consenter: str,
        notes: str = "",
    ) -> ConsentRecord:
        record = super().grant(
            problem_id=problem_id,
            adapters_authorized=adapters_authorized,
            cost_disclosed=cost_disclosed,
            consenter=consenter,
            notes=notes,
        )
        self._append(record)
        return record

    def revoke(
        self,
        problem_id: str,
        adapters: Optional[List[str]] = None,
        consenter: str = "",
        notes: str = "",
    ) -> ConsentRecord:
        record = super().revoke(
            problem_id=problem_id,
            adapters=adapters,
            consenter=consenter,
            notes=notes,
        )
        self._append(record)
        return record
