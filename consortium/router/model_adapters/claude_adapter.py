# ============================================================
# CLAUDE ADAPTER — STUB. Real wiring to the Anthropic API requires
# credentials and is intentionally not committed. Run the consortium
# offline with MockAdapter or instantiate this class with real
# credentials by overriding `available()` and `query()` in a private
# subclass, OR by editing this file once secret-handling is decided.
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


class ClaudeAdapter(BaseModelAdapter):
    """
    Stub adapter for the Anthropic Claude API.

    `query()` raises `NotImplementedError` until credentials are
    wired. The audit-symmetric way to wire it:
      1. Decide where credentials live (env var? config file? per-run?)
      2. Override `available()` to return False with a helpful reason
         when the credential is missing.
      3. Override `query()` to construct the prompt, call the API,
         and parse the response into a FrameReading whose
         `assumptions_required` records the model version, the
         input bounds disclosed, and any system prompt that shaped
         the read.
      4. Override `cost_estimate()` to return tokens/USD per query.

    Default `frame_id` is `narrative_structured` because Claude's
    typical analytic mode is narrative/structured reasoning. Callers
    that want a different framing (`thermodynamic_geometry`,
    `pattern_spatial`, etc.) should construct multiple adapter
    instances or a subclass.
    """

    frame_id = "narrative_structured"
    operator_type = "ai"

    def available(self) -> Tuple[bool, str]:
        return (
            False,
            "ClaudeAdapter is a stub; real wiring requires API "
            "credentials. See class docstring."
        )

    def cost_estimate(self, problem: Problem) -> CostEstimate:
        return CostEstimate(
            unit="USD_estimate",
            amount=0.0,
            notes="ClaudeAdapter stub: cost not estimated until wired",
        )

    def query(self, problem: Problem, **options: Any) -> FrameReading:
        raise NotImplementedError(
            "ClaudeAdapter is a stub. Wire credentials and implement "
            "query() per class docstring before invoking. The "
            "consortium runs end-to-end offline using MockAdapter."
        )
