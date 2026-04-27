# ============================================================
# MOCK ADAPTER — deterministic, offline, no external calls.
# Used for tests, dry runs, and as an honest baseline that doesn't
# depend on any model provider. The consortium runs end-to-end
# without a single external API call when populated with mocks.
# CC0 | consortium/router/
# ============================================================

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from typing import Any, Callable, Dict, List, Optional, Tuple

from consortium.collaboration_protocol import (
    FrameReading,
    GeometricFrame,
    Problem,
)
from consortium.router.base import BaseModelAdapter, CostEstimate


# subclass of BaseModelAdapter is concrete (not abstract), so
# __init_subclass__ enforces frame_id + operator_type are set
class MockAdapter(BaseModelAdapter):
    """
    Deterministic offline adapter.

    Configured per-instance with a frame and operator_type. By
    default produces a `FrameReading` that:
      - sets `visible_couplings` = problem.suspected_couplings
      - sets `load_bearing_elements` = first three of those
      - reports a fixed proposed_diagnosis derived from frame_id
      - proposes no actions
      - reports `confidence` = the frame's `confidence_calibration`
      - inherits `where_this_frame_breaks` from the frame

    Callers may pass a `response_factory(problem) -> Dict[str, Any]`
    to override any of the above per-call. The factory returns a dict
    with any subset of FrameReading fields; defaults fill in the rest.
    Useful for tests that need to simulate specific consortium
    scenarios.

    No network calls. `available()` always returns True. `cost_estimate()`
    reports zero cost in "no_op" units, since running a mock has no
    substrate impact.
    """

    # set on instances; class-level placeholders required by base
    frame_id = "_mock_placeholder"
    operator_type = "_mock_placeholder"

    def __init__(
        self,
        frame: GeometricFrame,
        operator_type: Optional[str] = None,
        response_factory: Optional[Callable[[Problem], Dict[str, Any]]] = None,
    ):
        # instance attributes override class attributes
        self.frame_id = frame.frame_id
        self.operator_type = operator_type or frame.operator_type
        self.frame = frame
        self.response_factory = response_factory

    def available(self) -> Tuple[bool, str]:
        return (True, "")

    def cost_estimate(self, problem: Problem) -> CostEstimate:
        return CostEstimate(
            unit="no_op",
            amount=0.0,
            notes="MockAdapter: offline; no substrate cost.",
        )

    def query(self, problem: Problem, **options: Any) -> FrameReading:
        defaults = self._default_response(problem)
        if self.response_factory is not None:
            override = self.response_factory(problem)
            defaults.update(override)
        return FrameReading(
            frame=self.frame,
            problem_id=problem.problem_id,
            visible_couplings=defaults["visible_couplings"],
            load_bearing_elements=defaults["load_bearing_elements"],
            invisible_aspects=defaults["invisible_aspects"],
            proposed_diagnosis=defaults["proposed_diagnosis"],
            proposed_actions=defaults["proposed_actions"],
            confidence=defaults["confidence"],
            assumptions_required=defaults["assumptions_required"],
            where_this_frame_breaks=defaults["where_this_frame_breaks"],
        )

    def _default_response(self, problem: Problem) -> Dict[str, Any]:
        couplings = list(problem.suspected_couplings)
        return {
            "visible_couplings": couplings,
            "load_bearing_elements": couplings[:3],
            "invisible_aspects": list(self.frame.couplings_invisible),
            "proposed_diagnosis": (
                f"[mock:{self.frame.frame_id}] reading of "
                f"{problem.problem_id}"
            ),
            "proposed_actions": [],
            "confidence": self.frame.confidence_calibration,
            "assumptions_required": [
                f"adapter=MockAdapter",
                f"frame_id={self.frame.frame_id}",
                f"operator_type={self.operator_type}",
                "deterministic_no_external_call=True",
            ],
            "where_this_frame_breaks": list(self.frame.couplings_invisible),
        }
