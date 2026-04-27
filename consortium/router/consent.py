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
