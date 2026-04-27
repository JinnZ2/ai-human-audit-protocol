# ============================================================
# GEMINI ADAPTER — STUB (see ClaudeAdapter docstring for wiring
# pattern; the same applies to Google's Gemini API).
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


class GeminiAdapter(BaseModelAdapter):
    """
    Stub adapter for the Google Gemini API.

    Default `frame_id` is `pattern_spatial` because Gemini's
    multimodal training tends toward spatial / topological framing.
    Callers may construct multiple adapter instances or a subclass
    for other framings.

    Wire by following ClaudeAdapter's docstring pattern.
    """

    frame_id = "pattern_spatial"
    operator_type = "ai"

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "GeminiAdapter is a stub; real wiring requires API "
            "credentials. See class docstring."
        )

    def cost_estimate(self, problem: Problem) -> CostEstimate:
        return CostEstimate(
            unit="USD_estimate",
            amount=0.0,
            notes="GeminiAdapter stub: cost not estimated until wired",
        )

    def query(self, problem: Problem, **options: Any) -> FrameReading:
        raise NotImplementedError(
            "GeminiAdapter is a stub. Wire credentials and implement "
            "query() per class docstring before invoking."
        )
