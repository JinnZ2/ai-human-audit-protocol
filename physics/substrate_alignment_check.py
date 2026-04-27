# ============================================================
# SUBSTRATE ALIGNMENT CHECK
#
# Promotes LOGIC-ETHICS-SAFETY.md §9.2 coherence_gate() pseudocode
# into runnable Python. Returns structured data, not judgment.
#
# Conservation law operates whether anyone believes in it. This
# check makes the operation visible: which axioms are upheld, which
# are violated, with what evidence. The consenter decides what to
# do with the data — the function does not decide for them.
#
# Six checks run; each returns a CheckResult. The aggregate
# AlignmentReport reports all six and a recommended decision, but
# the recommendation is informational. The ledger entry's `decision`
# field is set by the consenter, not by this code.
#
# C1: Conservation
# C2: Keystone integrity
# C3: Temporal stability (any horizon decreasing → not aligned)
# C4: Plural logic (no zero score)
# C5: Reciprocity contract present
# C6: Visibility (Reciprocal Recognition) — every labor entry visible
# ============================================================

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ------------------------------------------------------------
# Result types
# ------------------------------------------------------------

@dataclass
class CheckResult:
    """
    One coherence check's result.

    `passed` may be None when the input is missing the field needed
    to compute the check. None is not the same as False — None means
    "the proposal is incomplete on this axis," False means "complete
    enough to evaluate, and the answer is no."
    """
    name: str
    passed: Optional[bool]
    score: Optional[float] = None
    reason: str = ""
    detail: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlignmentReport:
    """
    Aggregate over all six checks.

    `recommendation` is informational: "aligned" / "revise" / "reject"
    / "incomplete". The consenter writes the final `decision` into
    the ledger entry; this function does not write it for them.
    """
    proposal_id: str
    checks: List[CheckResult]
    recommendation: str
    notes: str = ""

    def passed(self) -> List[str]:
        return [c.name for c in self.checks if c.passed is True]

    def failed(self) -> List[str]:
        return [c.name for c in self.checks if c.passed is False]

    def incomplete(self) -> List[str]:
        return [c.name for c in self.checks if c.passed is None]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "recommendation": self.recommendation,
            "notes": self.notes,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "score": c.score,
                    "reason": c.reason,
                    "detail": c.detail,
                }
                for c in self.checks
            ],
            "summary": {
                "passed": self.passed(),
                "failed": self.failed(),
                "incomplete": self.incomplete(),
            },
        }


# ------------------------------------------------------------
# Individual checks
# ------------------------------------------------------------

def conservation_check(proposal: Dict[str, Any]) -> CheckResult:
    """C1: Are conservation laws upheld?"""
    checks = (proposal.get("checks") or {})
    if "conservation" not in checks:
        return CheckResult(
            name="C1_conservation",
            passed=None,
            reason="checks.conservation not declared",
        )
    val = bool(checks["conservation"])
    return CheckResult(
        name="C1_conservation",
        passed=val,
        reason="conservation declared upheld" if val
               else "conservation declared breached",
    )


def keystone_check(proposal: Dict[str, Any]) -> CheckResult:
    """C2: Keystone intact or replaced?"""
    checks = (proposal.get("checks") or {})
    if "keystone_intact_or_replaced" not in checks:
        return CheckResult(
            name="C2_keystone",
            passed=None,
            reason="checks.keystone_intact_or_replaced not declared",
        )
    val = bool(checks["keystone_intact_or_replaced"])
    keystones = (proposal.get("baselines") or {}).get("keystones") or []
    return CheckResult(
        name="C2_keystone",
        passed=val,
        reason=("all keystones intact or replaced" if val
                else "at least one keystone removed without compensator"),
        detail={"keystones_named": keystones},
    )


def temporal_check(proposal: Dict[str, Any]) -> CheckResult:
    """
    C3: Temporal stability.

    Any horizon labeled 'negative' fails the check. 'unknown' is
    treated as incomplete (None at the horizon level), but if all
    horizons are unknown the check returns None overall. If some are
    'positive' or 'neutral' and none are 'negative', the check passes
    even with some unknowns — but the unknowns are recorded in detail.
    """
    checks = (proposal.get("checks") or {})
    temporal = checks.get("temporal_stability")
    if not isinstance(temporal, dict) or not temporal:
        return CheckResult(
            name="C3_temporal",
            passed=None,
            reason="checks.temporal_stability missing or empty",
        )

    negatives = [h for h, v in temporal.items() if v == "negative"]
    unknowns = [h for h, v in temporal.items() if v == "unknown"]

    if negatives:
        return CheckResult(
            name="C3_temporal",
            passed=False,
            reason=f"horizons declining: {negatives}",
            detail={"negatives": negatives, "unknowns": unknowns,
                    "all_horizons": temporal},
        )

    if unknowns and len(unknowns) == len(temporal):
        return CheckResult(
            name="C3_temporal",
            passed=None,
            reason="all horizons unknown; cannot evaluate",
            detail={"unknowns": unknowns, "all_horizons": temporal},
        )

    return CheckResult(
        name="C3_temporal",
        passed=True,
        reason=("all horizons non-decreasing"
                + (f" (with unknowns: {unknowns})" if unknowns else "")),
        detail={"unknowns": unknowns, "all_horizons": temporal},
    )


def plural_logic_check(
    proposal: Dict[str, Any],
    floor: float = 0.65,
) -> CheckResult:
    """
    C4: Plural logic — no single frame dominance, no zero score.

    Default floor 0.65 matches LOGIC-ETHICS-SAFETY.md §9.2 pseudocode.
    Caller may pass a different floor.
    """
    checks = (proposal.get("checks") or {})
    pls = checks.get("plural_logic_score")
    if not isinstance(pls, dict) or not pls:
        return CheckResult(
            name="C4_plural_logic",
            passed=None,
            reason="checks.plural_logic_score missing or empty",
        )
    minimum = min(pls.values())
    failures = {k: v for k, v in pls.items() if v < floor}
    if failures:
        return CheckResult(
            name="C4_plural_logic",
            passed=False,
            score=minimum,
            reason=f"frames below floor={floor}: {sorted(failures.keys())}",
            detail={"scores": pls, "floor": floor, "below_floor": failures},
        )
    return CheckResult(
        name="C4_plural_logic",
        passed=True,
        score=minimum,
        reason=f"all frames at or above floor={floor}",
        detail={"scores": pls, "floor": floor},
    )


def reciprocity_check(proposal: Dict[str, Any]) -> CheckResult:
    """C5: Reciprocity contract present?"""
    checks = (proposal.get("checks") or {})
    rec = checks.get("reciprocity_contract")
    if not isinstance(rec, dict):
        return CheckResult(
            name="C5_reciprocity",
            passed=None,
            reason="checks.reciprocity_contract missing or malformed",
        )
    present = bool(rec.get("present"))
    obligations = rec.get("obligations") or []
    if not present:
        return CheckResult(
            name="C5_reciprocity",
            passed=False,
            reason="reciprocity_contract.present is False",
        )
    if not obligations:
        return CheckResult(
            name="C5_reciprocity",
            passed=False,
            reason="contract claimed present but no obligations listed",
            detail={"contract": rec},
        )
    return CheckResult(
        name="C5_reciprocity",
        passed=True,
        reason=f"reciprocity present with {len(obligations)} obligations",
        detail={"obligations": obligations},
    )


def visibility_check(proposal: Dict[str, Any]) -> CheckResult:
    """
    C6: Visibility (Principle of Reciprocal Recognition).

    Every labor entry must carry visible=True, OR carry visible=False
    with a justification in `notes`. Unrecognized labor is unaccounted
    entropy. A ledger entry with hidden labor and no justification is
    a Law of Full Accounting violation.
    """
    labor = proposal.get("labor")
    if labor is None:
        return CheckResult(
            name="C6_visibility",
            passed=None,
            reason="labor field not declared",
        )
    if not isinstance(labor, list):
        return CheckResult(
            name="C6_visibility",
            passed=None,
            reason="labor field malformed (expected array)",
        )
    if not labor:
        return CheckResult(
            name="C6_visibility",
            passed=None,
            reason="labor array empty; nothing to evaluate",
        )

    invisible_unjustified: List[Dict[str, Any]] = []
    invisible_justified: List[Dict[str, Any]] = []
    visible: List[Dict[str, Any]] = []

    for entry in labor:
        if not isinstance(entry, dict):
            continue
        if entry.get("visible") is True:
            visible.append(entry)
        else:
            if (entry.get("notes") or "").strip():
                invisible_justified.append(entry)
            else:
                invisible_unjustified.append(entry)

    if invisible_unjustified:
        return CheckResult(
            name="C6_visibility",
            passed=False,
            reason=(f"{len(invisible_unjustified)} labor entries "
                    f"invisible without justification (entropy debt)"),
            detail={
                "invisible_unjustified_count": len(invisible_unjustified),
                "invisible_justified_count": len(invisible_justified),
                "visible_count": len(visible),
                "examples_unjustified": invisible_unjustified[:3],
            },
        )

    return CheckResult(
        name="C6_visibility",
        passed=True,
        reason=("all labor visible"
                if not invisible_justified
                else f"all labor visible or justified "
                     f"({len(invisible_justified)} justified-invisible)"),
        detail={
            "visible_count": len(visible),
            "invisible_justified_count": len(invisible_justified),
        },
    )


# ------------------------------------------------------------
# Aggregate
# ------------------------------------------------------------

def alignment_check(
    proposal: Dict[str, Any],
    plural_logic_floor: float = 0.65,
) -> AlignmentReport:
    """
    Run all six checks against a proposal. Return a structured
    AlignmentReport. Does NOT mutate the proposal and does NOT write
    a `decision` field — that is the consenter's responsibility.

    Recommendation:
      - "aligned"    : all checks passed
      - "revise"     : some checks failed but none on conservation
                       or visibility (the load-bearing axes)
      - "reject"     : conservation OR visibility failed
                       (these are the floor; failure here is not
                       a revision opportunity)
      - "incomplete" : at least one check is None and no checks
                       have failed
    """
    checks = [
        conservation_check(proposal),
        keystone_check(proposal),
        temporal_check(proposal),
        plural_logic_check(proposal, floor=plural_logic_floor),
        reciprocity_check(proposal),
        visibility_check(proposal),
    ]

    failed = [c for c in checks if c.passed is False]
    incomplete = [c for c in checks if c.passed is None]

    if any(c.name in {"C1_conservation", "C6_visibility"}
           and c.passed is False for c in checks):
        recommendation = "reject"
        notes = (
            "C1 (conservation) or C6 (visibility) is the load-bearing "
            "floor. Failure here is not a revision opportunity — the "
            "proposal violates the conservation framing the entire "
            "ledger rests on."
        )
    elif failed:
        recommendation = "revise"
        notes = (
            f"{len(failed)} check(s) failed but conservation and "
            f"visibility hold. Revision is open."
        )
    elif incomplete:
        recommendation = "incomplete"
        notes = (
            f"{len(incomplete)} check(s) lack data; cannot evaluate. "
            f"Add the missing fields and re-run."
        )
    else:
        recommendation = "aligned"
        notes = "all six checks passed"

    return AlignmentReport(
        proposal_id=proposal.get("id", "unknown"),
        checks=checks,
        recommendation=recommendation,
        notes=notes,
    )


# ============================================================
# DEMO — run the check against the example proposals
# ============================================================
if __name__ == "__main__":
    import json
    from pathlib import Path

    examples_path = Path(__file__).parent / "example_proposals.json"
    with open(examples_path) as f:
        examples = json.load(f)

    print("=" * 72)
    print("SUBSTRATE ALIGNMENT CHECK — example proposals")
    print("=" * 72)

    for ex in examples["proposals"]:
        report = alignment_check(ex)
        print(f"\n[{report.proposal_id}]")
        print(f"  recommendation: {report.recommendation}")
        print(f"  notes: {report.notes}")
        for c in report.checks:
            mark = "✓" if c.passed is True else (
                "✗" if c.passed is False else "?")
            print(f"  {mark} {c.name:25s} {c.reason}")
