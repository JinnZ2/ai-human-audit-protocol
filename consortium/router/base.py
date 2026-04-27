# ============================================================
# BASE MODEL ADAPTER — contract every adapter must satisfy
# operator-agnostic: AI models, instruments, and even human-as-
# scribe adapters all implement this same interface.
# CC0 | consortium/router/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Tuple

from consortium.collaboration_protocol import (
    GeometricFrame,
    Problem,
    FrameReading,
)


@dataclass
class CostEstimate:
    """
    Estimated cost of running a query through this adapter.

    Substrate-appropriate: AI models pay tokens / dollars, humans
    pay attention_minutes, instruments pay battery / calibration
    cycles, ecosystems pay phenological windows. The consent gate
    consults this before authorizing fan-out so the consenter knows
    what they are spending and on whose substrate.
    """
    unit: str            # e.g. "tokens", "USD", "attention_minutes",
                         #      "battery_pct", "phenological_window_pct"
    amount: float
    notes: str = ""


class BaseModelAdapter(ABC):
    """
    Abstract base for any operator that participates in a consortium
    query. Subclasses must declare their consortium frame and operator
    type, implement `query()`, and implement `available()`.

    Operator-agnostic by construction: subclasses can be AI models,
    instruments, ecosystem signal aggregators, or even human-as-scribe
    interfaces. The contract is the same. The audit-symmetry stance
    is enforced at the interface, not by the type of operator.

    No adapter is automatic ground truth. Every reading the adapter
    returns will pass through the same downstream `coating_probe` and
    confidence-ceiling checks as any other.
    """

    # subclasses MUST set these
    frame_id: str = ""
    operator_type: str = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # enforce contract at subclass-definition time so a subclass
        # that forgets to declare frame_id / operator_type fails fast
        # (skip for further-abstract subclasses)
        if not getattr(cls, "_abstract_intermediate", False):
            if not getattr(cls, "frame_id", ""):
                raise TypeError(
                    f"{cls.__name__} must set class attribute frame_id"
                )
            if not getattr(cls, "operator_type", ""):
                raise TypeError(
                    f"{cls.__name__} must set class attribute operator_type"
                )

    @abstractmethod
    def query(
        self,
        problem: Problem,
        **options: Any,
    ) -> FrameReading:
        """
        Run a query against this adapter for the given Problem.

        Returns a FrameReading attributed to this adapter's frame.
        The FrameReading must include a confidence value the adapter
        can defend, blind-spot acknowledgments, and (where applicable)
        proposed actions with reversibility tags.

        Implementations should NOT make external network calls without
        first being authorized by the consent gate. The dispatcher is
        responsible for calling `is_authorized` before invoking
        `query`; this method may assume authorization has been granted
        if it is being called.
        """
        raise NotImplementedError

    @abstractmethod
    def available(self) -> Tuple[bool, str]:
        """
        Runtime availability check.

        Returns (True, "") when the adapter is ready to be queried.
        Returns (False, reason) when it is not — e.g., missing API
        key, instrument off-network, operator off-shift, phenological
        window closed.

        Called by the dispatcher BEFORE the consent check, so an
        adapter that is not available never reaches the consent
        decision.
        """
        raise NotImplementedError

    def cost_estimate(self, problem: Problem) -> CostEstimate:
        """
        Estimated cost of running this query through this adapter.

        Default: zero-cost in unspecified units. Real adapters should
        override with substrate-appropriate cost estimates so the
        consent gate can disclose the cost.
        """
        return CostEstimate(unit="unspecified", amount=0.0)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} "
            f"frame_id={self.frame_id!r} "
            f"operator_type={self.operator_type!r}>"
        )
