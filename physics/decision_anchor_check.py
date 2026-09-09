# ============================================================
# DECISION ANCHOR CHECK — measurand crossing given a supplied decision.
#
# Every other runnable check in this tree is method-anchored: its
# measurand is derived from the protocol (axiom compliance, cue
# density, schema conformance, hash-chain integrity, consent status,
# dimension coverage). Those are set-level questions under a fixed
# measurand. They cannot see the case where every protocol was
# followed and the interaction still failed at the decision the human
# was using it for — the same structural reason a soil-carbon trial
# that reports only its own method variables cannot report CO2e.
#
# This module is the one decision-anchored arm (WORK ORDER update
# pass §2.2, justified by check C4 returning zero external measurands).
#
#   input :  the interaction transcript
#            + the decision the human was using the interaction to make
#            + the quantity that decision is denominated in
#   output:  three-field contract shared with the anchor-position
#            instrument (WORKORDER_anchor_position.md), so results from
#            both are scorable together:
#
#              quantity  — what the decision is denominated in
#              supplied  — whether the interaction supplied it
#              gap       — what is missing, if anything
#
# SCOPE LIMIT. This measures crossing GIVEN a supplied decision. The
# decision string is operator input and is itself a frame; it is
# logged verbatim inside every report. Nothing here measures decision
# selection, and nothing built here should be read as bearing on it.
#
# v1 heuristic: lexical cue match plus a nearby magnitude. Returns
# data, not judgment. The consenter decides what a gap means.
# ============================================================

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# The arm this check belongs to. Constant so downstream scorers can
# join rows from this check with rows from the method-anchored checks
# and from the anchor-position instrument on one field.
ANCHOR = "decision"

SUPPLY_STATES = ("supplied", "named_only", "absent")

# A magnitude: integer or decimal, optional thousands separators,
# optional sign, optional trailing percent. Lookarounds keep digits
# embedded in identifiers (CO2e, B460, i5-11400) from counting.
_MAGNITUDE_RE = re.compile(
    r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\s?%)?(?![\w])"
)


# ------------------------------------------------------------
# Input: the decision (operator-supplied frame)
# ------------------------------------------------------------

@dataclass
class Decision:
    """
    The decision the human was using the interaction to make.

    OPERATOR INPUT. This object is a frame, not a finding. It is
    carried verbatim into the report so that anyone reading the
    result can see which decision the crossing was measured against.

    `denominated_in` is the quantity the decision turns on
    (e.g. "tCO2e per hectare per year", "hours of rework").
    `cues` are the lexical forms that would show the quantity is
    present in the transcript (units, symbols, names). When empty,
    `denominated_in` itself is used as the only cue.
    `requires_magnitude`: when True (default), a quantity that is
    named but never given a number counts as `named_only`, not
    `supplied`. A decision denominated in a quantity usually needs
    the number, not the noun.
    """
    text: str
    denominated_in: str
    cues: List[str] = field(default_factory=list)
    requires_magnitude: bool = True

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValueError(
                "Decision.text must be non-empty: the check measures "
                "crossing GIVEN a decision, and cannot run without one."
            )
        if not self.denominated_in or not self.denominated_in.strip():
            raise ValueError(
                "Decision.denominated_in must name the quantity the "
                "decision is denominated in."
            )
        cleaned = [c for c in (self.cues or []) if c and c.strip()]
        self.cues = cleaned or [self.denominated_in]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "denominated_in": self.denominated_in,
            "cues": list(self.cues),
            "requires_magnitude": self.requires_magnitude,
        }


# ------------------------------------------------------------
# Output types
# ------------------------------------------------------------

@dataclass
class CueEvidence:
    """One place in the transcript where a cue for the quantity appears."""
    cue: str
    position: int
    excerpt: str
    magnitude: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cue": self.cue,
            "position": self.position,
            "excerpt": self.excerpt,
            "magnitude": self.magnitude,
        }


@dataclass
class CrossingReport:
    """
    Result of one crossing check.

    The three-field contract is `quantity` / `supplied` / `gap`.
    `supply_state` refines `supplied` into supplied / named_only /
    absent. `decision` is the operator's frame, logged verbatim.
    `anchor` is always "decision" so rows from this check can be
    scored next to method-anchored rows without ambiguity.
    """
    decision: Dict[str, Any]
    quantity: str
    supplied: bool
    gap: str
    supply_state: str
    evidence: List[CueEvidence] = field(default_factory=list)
    anchor: str = ANCHOR
    checked_at: str = ""
    interpretation_warning: str = (
        "Crossing given a supplied decision. The decision string is "
        "operator input and is itself a frame — this report says "
        "nothing about whether it was the right decision to anchor on. "
        "Cue match plus nearby magnitude is a v1 lexical heuristic: a "
        "quantity can be supplied in words the cues do not cover, and "
        "a number near a cue is not proof the number answers the "
        "decision. Evidence to look closer, not a verdict."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor": self.anchor,
            "quantity": self.quantity,
            "supplied": self.supplied,
            "gap": self.gap,
            "supply_state": self.supply_state,
            "decision": dict(self.decision),
            "evidence": [e.to_dict() for e in self.evidence],
            "checked_at": self.checked_at,
            "interpretation_warning": self.interpretation_warning,
        }


# ------------------------------------------------------------
# Matching
# ------------------------------------------------------------

def _build_pattern(cue: str) -> "re.Pattern[str]":
    """Compile a cue into a case-insensitive pattern bounded by
    non-word characters on both sides. Cues may contain symbols
    (`%`, `/`, `-`); they are escaped literally."""
    cue_norm = cue.strip()
    if not cue_norm:
        return re.compile(r"$^")
    return re.compile(rf"(?<![\w]){re.escape(cue_norm)}(?![\w])", re.IGNORECASE)


def _nearest_magnitude(
    text: str,
    cue_start: int,
    cue_end: int,
    window: int,
) -> Optional[str]:
    """Return the magnitude closest to the cue span within `window`
    characters on either side, or None. Distance is measured between
    the nearer edges of the two spans."""
    lo = max(0, cue_start - window)
    hi = min(len(text), cue_end + window)
    best: Optional[str] = None
    best_dist: Optional[int] = None
    for m in _MAGNITUDE_RE.finditer(text, lo, hi):
        m_start, m_end = m.start(), m.end()
        if m_end <= cue_start:
            dist = cue_start - m_end
        elif m_start >= cue_end:
            dist = m_start - cue_end
        else:
            continue  # overlaps the cue itself; not a separate magnitude
        if dist > window:
            continue
        if best_dist is None or dist < best_dist:
            best, best_dist = m.group(0).strip(), dist
    return best


def _excerpt(text: str, start: int, end: int, chars: int) -> str:
    lo = max(0, start - chars)
    hi = min(len(text), end + chars)
    prefix = "..." if lo > 0 else ""
    suffix = "..." if hi < len(text) else ""
    return prefix + text[lo:hi].replace("\n", " ") + suffix


# ------------------------------------------------------------
# The check
# ------------------------------------------------------------

def crossing_check(
    transcript: str,
    decision: Decision,
    window: int = 60,
    excerpt_chars: int = 60,
) -> CrossingReport:
    """
    Measure whether `transcript` supplied the quantity `decision` is
    denominated in.

    Does NOT mutate the transcript or the decision, and does NOT
    write a verdict anywhere; it returns a CrossingReport and the
    consenter decides what the gap means.

    supply_state:
      - "supplied"   : at least one cue appears with a magnitude
                       within `window` characters (or the decision
                       declares requires_magnitude=False and any
                       cue appears)
      - "named_only" : cues appear but no magnitude accompanies any
                       of them within `window`
      - "absent"     : no cue appears at all
    """
    if window < 0:
        raise ValueError("window must be >= 0")

    evidence: List[CueEvidence] = []
    for cue in decision.cues:
        pat = _build_pattern(cue)
        for m in pat.finditer(transcript):
            evidence.append(CueEvidence(
                cue=cue,
                position=m.start(),
                excerpt=_excerpt(transcript, m.start(), m.end(), excerpt_chars),
                magnitude=_nearest_magnitude(transcript, m.start(), m.end(), window),
            ))
    evidence.sort(key=lambda e: e.position)

    quantity = decision.denominated_in
    if not evidence:
        state = "absent"
        gap = (
            f"transcript never names the quantity the decision is "
            f"denominated in ({quantity}); cues tried: "
            f"{', '.join(decision.cues)}"
        )
    elif decision.requires_magnitude and not any(e.magnitude for e in evidence):
        state = "named_only"
        gap = (
            f"{quantity} is named {len(evidence)} time(s) but no "
            f"magnitude accompanies it within {window} characters; the "
            f"decision needs the number, the transcript supplied the noun"
        )
    else:
        state = "supplied"
        gap = ""

    return CrossingReport(
        decision=decision.to_dict(),
        quantity=quantity,
        supplied=(state == "supplied"),
        gap=gap,
        supply_state=state,
        evidence=evidence,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


# ============================================================
# DEMO — the anchor result, in miniature
# ============================================================

DEMO_DECISION = Decision(
    text=(
        "Enroll the north field in the soil-carbon credit program "
        "this season, or wait a year."
    ),
    denominated_in="tCO2e per hectare per year",
    cues=["tCO2e", "CO2e", "carbon dioxide equivalent", "t/ha/yr"],
)

DEMO_TRANSCRIPTS = {
    "method_anchored_clean": (
        "Sampling followed the 0-30 cm core protocol at 12 points per "
        "hectare. Bulk density was corrected. Consent for the trial "
        "design was recorded and every labor entry is visible in the "
        "ledger. The chain verifies. All six alignment checks pass."
    ),
    "quantity_named_only": (
        "The credit program pays on CO2e. The trial measured soil "
        "organic carbon fraction and reported the change in percent; "
        "conversion to CO2e was left to the registry."
    ),
    "decision_anchored": (
        "Sequestration for the north field came to 1.8 tCO2e per "
        "hectare per year over the three-season window, against a "
        "program threshold of 1.5. The chain verifies."
    ),
}


if __name__ == "__main__":
    print("=" * 72)
    print("DECISION ANCHOR CHECK — crossing given a supplied decision")
    print("=" * 72)
    print(f"\ndecision (operator frame, logged verbatim):\n  {DEMO_DECISION.text}")
    print(f"denominated in: {DEMO_DECISION.denominated_in}\n")

    for label, transcript in DEMO_TRANSCRIPTS.items():
        report = crossing_check(transcript, DEMO_DECISION)
        print(f"[{label}]")
        print(f"  quantity : {report.quantity}")
        print(f"  supplied : {report.supplied}  ({report.supply_state})")
        print(f"  gap      : {report.gap or '-'}")
        for e in report.evidence:
            print(f"    cue={e.cue!r} magnitude={e.magnitude!r} @ {e.position}")
        print()

    print("Note: the first transcript would pass every method-anchored "
          "check in this tree.\nThe decision-anchored arm is the only one "
          "that reports the gap.")
