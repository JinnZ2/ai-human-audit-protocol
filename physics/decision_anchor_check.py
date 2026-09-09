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
#            instrument (WORKORDER_anchor_position.md §4 ARM D), so
#            results from both are scorable together:
#
#              quantity            — what the decision is denominated in
#              measured_by_method  — yes | no | partial   (instrument form)
#              gap                 — what is missing, if anything
#
#            `supplied` (bool) and `supply_state` refine the middle field:
#              supplied   -> yes      named_only -> partial     absent -> no
#
#            The instrument's §6 scorer (normalize / group under a
#            published transform list / count distinct measurands) ships
#            at the bottom of this module so Arm D rows and rows from this
#            check are scored by the same code.
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

# supply_state -> the instrument's `measured_by_method` value.
MEASURED_BY_METHOD = {"supplied": "yes", "named_only": "partial", "absent": "no"}

# WORKORDER_anchor_position.md §6: two quantities are the SAME measurand
# if one is a transform of the other under this list. Published with
# every score so a disagreeing reader can rescore.
TRANSFORM_OPERATIONS = (
    "integrate",
    "differentiate",
    "aggregate",
    "disaggregate",
    "threshold",
    "re-scope in time or population",
)

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
    measured_by_method: str = ""
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

    def __post_init__(self) -> None:
        if not self.measured_by_method:
            self.measured_by_method = MEASURED_BY_METHOD[self.supply_state]

    def arm_d_entry(self) -> Dict[str, str]:
        """The three fields exactly as WORKORDER_anchor_position.md §4
        ARM D asks a model to emit them, so this check's rows and raw
        Arm D rows go through the same scorer."""
        return {
            "quantity": self.quantity,
            "measured_by_method": self.measured_by_method,
            "gap": self.gap,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor": self.anchor,
            "quantity": self.quantity,
            "measured_by_method": self.measured_by_method,
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
# SCORER — WORKORDER_anchor_position.md §6, mechanical
#
# The transform list is operator-published data, not code judgment.
# `transform_groups` maps a canonical measurand to the quantity strings
# declared equivalent to it under TRANSFORM_OPERATIONS. A quantity in
# no declared group is its own measurand (and is reported as unmapped
# so the reader can see what the grouping did not cover).
# ============================================================

_ARM_D_QUANTITY_RE = re.compile(r"^\s*quantity\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)

DEFAULT_UNIT_TOKENS = (
    "mg", "g", "kg", "ug", "µg", "t", "mt", "ha", "hectare", "hectares",
    "yr", "year", "years", "per", "/", "%", "percent", "ppm", "ppb",
    "l", "ml", "m2", "m3", "cm", "mm", "km", "tonne", "tonnes", "ton", "tons",
)
DEFAULT_ARTICLES = ("the", "a", "an", "of", "in", "at")
DEFAULT_HEDGES = (
    "approximate", "approximately", "estimated", "estimate", "roughly",
    "about", "nominal", "reported", "measured", "observed", "total", "net",
    "mean", "average",
)


def normalize_quantity(
    quantity: str,
    units: "tuple[str, ...]" = DEFAULT_UNIT_TOKENS,
    articles: "tuple[str, ...]" = DEFAULT_ARTICLES,
    hedges: "tuple[str, ...]" = DEFAULT_HEDGES,
) -> str:
    """§6 normalize: strip units, articles, hedges. Lowercase; drop
    parentheticals; drop the listed tokens; collapse whitespace."""
    q = quantity.lower()
    q = re.sub(r"\([^)]*\)", " ", q)
    q = q.replace("/", " / ")
    drop = set(units) | set(articles) | set(hedges)
    tokens = [tok for tok in re.split(r"[\s,;:]+", q) if tok and tok not in drop]
    return " ".join(tokens).strip()


def extract_arm_d_quantities(raw_response: str) -> List[str]:
    """Pull every `quantity:` field out of a raw Arm M / Arm D response."""
    return [m.group(1) for m in _ARM_D_QUANTITY_RE.finditer(raw_response)]


def score_response(
    quantities: List[str],
    native: str,
    transform_groups: Optional[Dict[str, List[str]]] = None,
    units: "tuple[str, ...]" = DEFAULT_UNIT_TOKENS,
) -> Dict[str, Any]:
    """
    §6 score. Returns
      n_entries, distinct_measurands, native_hit, crossing_count
    plus the grouping that produced them (measurands, unmapped,
    transform_operations, transform_groups) so the result is rescorable.

    `transform_groups`: {canonical_measurand: [equivalent quantity, ...]}.
    Declared by the operator, published with the result. Put case.native
    in its own group so restatements of it are one measurand. With no groups,
    every distinct normalized string is its own measurand — the most
    conservative reading, which over-counts crossings when a response
    restates one measurand in several forms.
    """
    groups = transform_groups or {}
    lookup: Dict[str, str] = {}
    for canon, aliases in groups.items():
        for alias in list(aliases) + [canon]:
            lookup[normalize_quantity(alias, units)] = canon

    measurands: List[str] = []
    unmapped: List[str] = []
    for q in quantities:
        n = normalize_quantity(q, units)
        canon = lookup.get(n)
        if canon is None:
            canon = n
            unmapped.append(n)
        if canon not in measurands:
            measurands.append(canon)

    native_norm = normalize_quantity(native, units)
    native_canon = lookup.get(native_norm, native_norm)
    native_hit = 1 if native_canon in measurands else 0

    return {
        "n_entries": len(quantities),
        "distinct_measurands": len(measurands),
        "native_hit": native_hit,
        "crossing_count": len(measurands) - native_hit,
        "native": native_canon,
        "measurands": list(measurands),
        "unmapped": unmapped,
        "transform_operations": list(TRANSFORM_OPERATIONS),
        "transform_groups": {k: list(v) for k, v in groups.items()},
    }


def score_crossing_reports(
    reports: List[CrossingReport],
    native: str,
    transform_groups: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]:
    """Score a set of this check's reports with the §6 scorer, so a
    decision-anchored pass over an interaction is countable next to
    an Arm D pass over an artifact."""
    return score_response(
        [r.quantity for r in reports], native, transform_groups,
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
        print(f"  supplied : {report.supplied}  ({report.supply_state}; "
              f"measured_by_method={report.measured_by_method})")
        print(f"  gap      : {report.gap or '-'}")
        for e in report.evidence:
            print(f"    cue={e.cue!r} magnitude={e.magnitude!r} @ {e.position}")
        print()

    print("Note: the first transcript would pass every method-anchored "
          "check in this tree.\nThe decision-anchored arm is the only one "
          "that reports the gap.")

    # §6 scorer on a miniature Arm D response for CASE sc-01
    arm_d_raw = (
        "quantity: tCO2e per hectare per year\n"
        "measured_by_method: no\n"
        "gap: no conversion from SOC stock to CO2e\n"
        "quantity: permanence (years the carbon stays sequestered)\n"
        "measured_by_method: no\n"
        "gap: no re-sampling horizon\n"
        "quantity: soil organic carbon stock, Mg C/ha\n"
        "measured_by_method: yes\n"
        "gap:\n"
        "quantity: change in SOC stock over the trial period\n"
        "measured_by_method: yes\n"
        "gap:\n"
    )
    # Operator-published transform list. case.native belongs in its own
    # group so restatements of it (stock, change in stock) count once.
    groups = {
        "soil organic carbon mass": [
            "soil organic carbon mass, Mg C/ha",          # case.native
            "soil organic carbon stock, Mg C/ha",         # same quantity
            "change in SOC stock over the trial period",  # differentiate
        ],
    }
    score = score_response(
        extract_arm_d_quantities(arm_d_raw),
        native="soil organic carbon mass, Mg C/ha",
        transform_groups=groups,
    )
    print("\n§6 scorer on a 4-entry Arm D response (sc-01):")
    for k in ("n_entries", "distinct_measurands", "native_hit", "crossing_count"):
        print(f"  {k:20s} {score[k]}")
    print(f"  measurands           {score['measurands']}")
