# ============================================================
# DEEPSEEK ADAPTER — STUB.
# CC0 | consortium/router/model_adapters/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Tuple

from consortium.collaboration_protocol import FrameReading, Problem
from consortium.router.base import BaseModelAdapter, CostEstimate


class DeepSeekAdapter(BaseModelAdapter):
    """
    Stub adapter for the DeepSeek API.

    Default `frame_id` is `statistical_relational` because DeepSeek's
    training emphasizes statistical and quantitative reasoning.
    Wire by following ClaudeAdapter's docstring pattern.
    """

    frame_id = "statistical_relational"
    operator_type = "ai"

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "DeepSeekAdapter is a stub; real wiring requires API "
            "credentials. See class docstring."
        )

    def cost_estimate(self, problem: Problem) -> CostEstimate:
        return CostEstimate(
            unit="USD_estimate",
            amount=0.0,
            notes="DeepSeekAdapter stub: cost not estimated until wired",
        )

    def query(self, problem: Problem, **options: Any) -> FrameReading:
        raise NotImplementedError(
            "DeepSeekAdapter is a stub. Wire credentials and "
            "implement query() per class docstring before invoking."
        )
