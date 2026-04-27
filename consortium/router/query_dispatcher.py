# ============================================================
# QUERY DISPATCHER — fan out a Problem to multiple adapters,
# collect FrameReadings, record failures and consent refusals.
#
# The dispatcher does NOT short-circuit on disagreement, missing
# readings, or low overall coherence. It collects what is
# available and lets the aggregator surface the geometry of what
# came back — including absences. No single adapter's silence
# stops the consortium.
# CC0 | consortium/router/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from consortium.collaboration_protocol import (
    FrameReading,
    Problem,
)
from consortium.router.base import BaseModelAdapter
from consortium.router.consent import ConsentGate, ConsentDenied


@dataclass
class DispatchResult:
    """
    The result of a fan-out query.

    `readings` are the FrameReadings that came back from adapters
    that were available, authorized, and successful. `failures` and
    `refused` capture absences explicitly: every adapter that was
    invoked appears in exactly one of these three lists.

    `consent_records_consulted` is the consent history surveyed
    during this dispatch — included for audit transparency.
    """
    problem_id: str
    readings: List[FrameReading] = field(default_factory=list)
    failures: List[Dict[str, Any]] = field(default_factory=list)
    refused: List[Dict[str, Any]] = field(default_factory=list)
    unavailable: List[Dict[str, Any]] = field(default_factory=list)
    cost_estimates: Dict[str, Any] = field(default_factory=dict)

    def adapters_attempted(self) -> List[str]:
        ids = [r.frame.frame_id for r in self.readings]
        ids += [f["adapter_id"] for f in self.failures]
        ids += [f["adapter_id"] for f in self.refused]
        ids += [f["adapter_id"] for f in self.unavailable]
        return ids


class QueryDispatcher:
    """
    Fan out a Problem to a list of adapters.

    For each adapter:
      1. Check `available()`. If not available → record `unavailable`.
      2. Check consent. If not authorized → record `refused`.
      3. Call `query()`. On success → record reading. On exception
         → record `failure`.

    No adapter's silence prevents the others from running. The
    dispatcher is fail-soft per adapter, fail-loud per dispatcher
    misuse (e.g., calling without a consent gate when adapters
    require one).
    """

    def __init__(
        self,
        adapters: List[BaseModelAdapter],
        consent_gate: Optional[ConsentGate] = None,
    ):
        self.adapters = list(adapters)
        # if no gate provided, create a default fail-closed gate.
        # Caller must explicitly grant() before queries succeed.
        self.consent_gate = consent_gate or ConsentGate()

    def cost_estimates(self, problem: Problem) -> Dict[str, Any]:
        """Collect cost estimates for all adapters. Useful to disclose
        to a consenter before granting authorization."""
        out: Dict[str, Any] = {}
        for a in self.adapters:
            est = a.cost_estimate(problem)
            out[a.frame_id] = {
                "unit": est.unit,
                "amount": est.amount,
                "notes": est.notes,
                "operator_type": a.operator_type,
            }
        return out

    def fan_out(
        self,
        problem: Problem,
        **options: Any,
    ) -> DispatchResult:
        """Run all adapters against the problem in sequence."""
        result = DispatchResult(problem_id=problem.problem_id)
        result.cost_estimates = self.cost_estimates(problem)

        for adapter in self.adapters:
            ok, reason = adapter.available()
            if not ok:
                result.unavailable.append({
                    "adapter_id": adapter.frame_id,
                    "operator_type": adapter.operator_type,
                    "reason": reason or "unavailable",
                })
                continue

            authorized, ra_reason = self.consent_gate.is_authorized(
                problem.problem_id, adapter.frame_id,
            )
            if not authorized:
                result.refused.append({
                    "adapter_id": adapter.frame_id,
                    "operator_type": adapter.operator_type,
                    "reason": ra_reason,
                })
                continue

            try:
                reading = adapter.query(problem, **options)
            except ConsentDenied as e:
                # adapter itself raised consent denial (defense in depth)
                result.refused.append({
                    "adapter_id": adapter.frame_id,
                    "operator_type": adapter.operator_type,
                    "reason": f"adapter raised ConsentDenied: {e}",
                })
            except Exception as e:
                result.failures.append({
                    "adapter_id": adapter.frame_id,
                    "operator_type": adapter.operator_type,
                    "exception_type": type(e).__name__,
                    "reason": str(e),
                })
            else:
                result.readings.append(reading)

        return result
