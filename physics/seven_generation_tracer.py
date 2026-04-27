# ============================================================
# SEVEN-GENERATION TRACER
#
# Extends the C3 (temporal_stability) check from
# LOGIC-ETHICS-SAFETY.md §5.3 / physics/substrate_alignment_check.py
# from 1y/10y/100y horizons into a 7-generation traceable artifact.
#
# This is NOT a simulator. It cannot predict 175 years of system
# response. It is a *structure for honest accounting*: the user
# declares per-factor costs/benefits and their visibility-at-
# decision-time; the tracer projects them forward and surfaces
# which costs compound, which generations bear them, and which
# would have been invisible to the original consenter.
#
# Returns data, not judgment. The consenter writes what to do
# with the trace.
# ============================================================

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# Approximate years per generation. Used only for human-readable
# offsets; the tracer's logic operates in generation count, not years.
YEARS_PER_GENERATION = 25


# ------------------------------------------------------------
# Input: a generational factor
# ------------------------------------------------------------

@dataclass
class GenerationFactor:
    """
    A cost or benefit declared at decision time, projected forward.

    USER-PROVIDED. This is honest accounting, not simulation. The
    `visible_at_decision_time` field is the audit-symmetric hook:
    factors that would have been invisible to the original consenter
    are flagged at the end of the trace.

    Fields:
        name: human label (e.g. "topsoil_depletion")
        introduced_at_generation: 0 = present, 1 = next gen, ...
        per_generation_amount: magnitude per generation
        unit: e.g. "kg_C_per_m2_lost", "generations_of_knowledge",
              "USD"
        kind: "additive" | "compounding" | "one_time"
              additive:    contributes per_generation_amount each gen
                           from introduction onward
              compounding: amount grows by (1 + compounding_factor)
                           each gen from introduction
              one_time:    contributes per_generation_amount once at
                           introduced_at_generation, zero thereafter
                           (realistic for setup costs, milestone gifts)
        compounding_factor: rate per gen for compounding kind (e.g.
              0.20 = 20% increase per gen). Ignored otherwise.
        direction: "cost" | "benefit"
        visible_at_decision_time: bool — would the original consenter
              have been able to see this at gen 0?
        ledger_entry_responsible: which labor/transform entry in the
              ledger drives this factor (free-form id reference)
        notes: optional
    """
    name: str
    introduced_at_generation: int
    per_generation_amount: float
    unit: str
    direction: str = "cost"
    kind: str = "additive"
    compounding_factor: float = 0.0
    visible_at_decision_time: bool = True
    ledger_entry_responsible: str = ""
    notes: str = ""

    def __post_init__(self):
        if self.kind not in {"additive", "compounding", "one_time"}:
            raise ValueError(
                f"kind must be 'additive', 'compounding', or 'one_time', "
                f"got {self.kind!r}"
            )
        if self.direction not in {"cost", "benefit"}:
            raise ValueError(
                f"direction must be 'cost' or 'benefit', "
                f"got {self.direction!r}"
            )
        if self.kind == "compounding" and self.compounding_factor < 0:
            raise ValueError(
                "compounding_factor must be >= 0"
            )
        if self.introduced_at_generation < 0:
            raise ValueError("introduced_at_generation must be >= 0")


# ------------------------------------------------------------
# Output: per-generation projection
# ------------------------------------------------------------

@dataclass
class GenerationProjection:
    """One generation's projected state."""
    generation: int
    year_offset_estimate: int
    cost_this_gen: float = 0.0
    benefit_this_gen: float = 0.0
    cumulative_cost: float = 0.0
    cumulative_benefit: float = 0.0
    cost_drivers: List[str] = field(default_factory=list)
    benefit_drivers: List[str] = field(default_factory=list)

    def net_this_gen(self) -> float:
        return self.benefit_this_gen - self.cost_this_gen

    def net_cumulative(self) -> float:
        return self.cumulative_benefit - self.cumulative_cost


# ------------------------------------------------------------
# Output: full trace
# ------------------------------------------------------------

@dataclass
class SevenGenerationTrace:
    """
    Full output of the tracer.

    `compound_risk_horizon` is the first generation at which
    cumulative net falls below zero, if ever — None if the trace
    stays non-negative throughout.

    `hidden_at_decision_time` lists factors whose
    visible_at_decision_time=False — these are the costs/benefits
    the original consenter could not have seen. This is the
    audit-symmetric output: it makes the invisible labor *visible
    after the fact* so future consenters can be calibrated.
    """
    proposal_id: str
    generations: List[GenerationProjection]
    compound_risk_horizon: Optional[int] = None
    hidden_at_decision_time: List[str] = field(default_factory=list)
    factors: List[GenerationFactor] = field(default_factory=list)
    interpretation_warning: str = (
        "Trace, not prediction. Each factor's per-generation amount "
        "and visibility flag was declared by the consenter. The "
        "tracer projects forward arithmetically; it does not "
        "simulate system response. Treat the trace as a structure "
        "for honest accounting — not as a forecast."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "compound_risk_horizon": self.compound_risk_horizon,
            "hidden_at_decision_time": list(self.hidden_at_decision_time),
            "interpretation_warning": self.interpretation_warning,
            "generations": [
                {
                    "generation": g.generation,
                    "year_offset_estimate": g.year_offset_estimate,
                    "cost_this_gen": g.cost_this_gen,
                    "benefit_this_gen": g.benefit_this_gen,
                    "cumulative_cost": g.cumulative_cost,
                    "cumulative_benefit": g.cumulative_benefit,
                    "cost_drivers": list(g.cost_drivers),
                    "benefit_drivers": list(g.benefit_drivers),
                    "net_this_gen": g.net_this_gen(),
                    "net_cumulative": g.net_cumulative(),
                }
                for g in self.generations
            ],
            "factors": [
                {
                    "name": f.name,
                    "introduced_at_generation": f.introduced_at_generation,
                    "per_generation_amount": f.per_generation_amount,
                    "unit": f.unit,
                    "kind": f.kind,
                    "compounding_factor": f.compounding_factor,
                    "direction": f.direction,
                    "visible_at_decision_time": f.visible_at_decision_time,
                    "ledger_entry_responsible": f.ledger_entry_responsible,
                    "notes": f.notes,
                }
                for f in self.factors
            ],
        }


# ------------------------------------------------------------
# The trace
# ------------------------------------------------------------

def _factor_amount_at_gen(
    factor: GenerationFactor,
    generation: int,
) -> float:
    """Compute factor's contribution at a specific generation.
    Returns 0 for generations before introduction.

    For 'additive': per_generation_amount each gen from introduction.
    For 'compounding': per_generation_amount × (1+rate)^(gen - intro).
    For 'one_time': per_generation_amount at introduced gen, 0 after.
    """
    if generation < factor.introduced_at_generation:
        return 0.0
    if factor.kind == "one_time":
        return (factor.per_generation_amount
                if generation == factor.introduced_at_generation
                else 0.0)
    if factor.kind == "additive":
        return factor.per_generation_amount
    # compounding: amount grows by compounding_factor each gen
    elapsed = generation - factor.introduced_at_generation
    return factor.per_generation_amount * (
        (1.0 + factor.compounding_factor) ** elapsed
    )


def trace_seven_generations(
    proposal_id: str,
    factors: List[GenerationFactor],
    n_generations: int = 7,
) -> SevenGenerationTrace:
    """
    Project the given factors over `n_generations` generations
    (default 7). Returns a `SevenGenerationTrace`.

    The trace is purely arithmetic; it does not check whether the
    declared per-generation amounts are realistic. That is the
    consenter's responsibility — the tracer makes the consenter's
    declarations visible, not authoritative.

    `compound_risk_horizon` is the first generation at which
    cumulative net (benefit − cost) goes below zero, or None if
    it never does.
    """
    if n_generations < 1:
        raise ValueError("n_generations must be >= 1")

    generations: List[GenerationProjection] = []
    cumulative_cost = 0.0
    cumulative_benefit = 0.0
    compound_risk_horizon: Optional[int] = None

    for gen in range(n_generations + 1):   # gen=0 is present
        proj = GenerationProjection(
            generation=gen,
            year_offset_estimate=gen * YEARS_PER_GENERATION,
        )
        for f in factors:
            amount = _factor_amount_at_gen(f, gen)
            if amount == 0:
                continue
            if f.direction == "cost":
                proj.cost_this_gen += amount
                proj.cost_drivers.append(f.name)
            else:
                proj.benefit_this_gen += amount
                proj.benefit_drivers.append(f.name)
        cumulative_cost += proj.cost_this_gen
        cumulative_benefit += proj.benefit_this_gen
        proj.cumulative_cost = cumulative_cost
        proj.cumulative_benefit = cumulative_benefit
        generations.append(proj)
        if (compound_risk_horizon is None
                and proj.net_cumulative() < 0):
            compound_risk_horizon = gen

    hidden = [
        f.name for f in factors
        if not f.visible_at_decision_time
    ]

    return SevenGenerationTrace(
        proposal_id=proposal_id,
        generations=generations,
        compound_risk_horizon=compound_risk_horizon,
        hidden_at_decision_time=hidden,
        factors=list(factors),
    )


# ------------------------------------------------------------
# Bridge to substrate_alignment_check: convert trace → C3 verdict
# ------------------------------------------------------------

def trace_to_temporal_stability_7g(
    trace: SevenGenerationTrace,
) -> str:
    """
    Convert a SevenGenerationTrace into the value that should
    populate `checks.temporal_stability["7g"]` in a ledger entry.

    Returns one of:
      - "positive"  — final-generation cumulative net is clearly positive
      - "neutral"   — final-generation cumulative is approximately zero
      - "negative"  — final-generation cumulative net is below zero
      - "unknown"   — empty trace

    Threshold for "approximately zero" is a small absolute value.
    The threshold is conservative; callers may override by writing
    the field directly.
    """
    if not trace.generations:
        return "unknown"
    final = trace.generations[-1].net_cumulative()
    if final < -1e-9:
        return "negative"
    if final > 1e-9:
        return "positive"
    return "neutral"


# ============================================================
# DEMO — three example traces
# ============================================================
if __name__ == "__main__":
    # Example 1: extractive proposal — costs compound, benefits don't
    extractive = [
        GenerationFactor(
            name="topsoil_depletion",
            introduced_at_generation=0,
            per_generation_amount=2.0,
            unit="kg_C_per_m2_lost_per_gen",
            direction="cost",
            kind="additive",
            visible_at_decision_time=False,
            ledger_entry_responsible="transform.actions[0]:intensive_tillage",
            notes="invisible at gen 0; only visible after gen 2-3",
        ),
        GenerationFactor(
            name="mycorrhizal_collapse",
            introduced_at_generation=1,
            per_generation_amount=0.5,
            compounding_factor=0.25,
            unit="recovery_capacity_pct_lost",
            direction="cost",
            kind="compounding",
            visible_at_decision_time=False,
            ledger_entry_responsible="transform.actions[1]:biocide_application",
            notes="each gen of biota loss makes next gen's recovery harder",
        ),
        GenerationFactor(
            name="immediate_yield_premium",
            introduced_at_generation=0,
            per_generation_amount=1.0,
            unit="harvest_units",
            direction="benefit",
            kind="additive",
            visible_at_decision_time=True,
            ledger_entry_responsible="transform.actions[0]",
            notes="declines naturally; gen 0 only",
        ),
    ]

    # Example 2: regenerative proposal — benefits compound
    regenerative = [
        GenerationFactor(
            name="initial_setup_cost",
            introduced_at_generation=0,
            per_generation_amount=3.0,
            unit="person_years",
            direction="cost",
            kind="one_time",
            visible_at_decision_time=True,
            ledger_entry_responsible="transform.actions[0]:corridor_setup",
            notes="known up front; one-time hit at gen 0",
        ),
        GenerationFactor(
            name="soil_carbon_accumulation",
            introduced_at_generation=1,
            per_generation_amount=1.0,
            compounding_factor=0.15,
            unit="kg_C_per_m2",
            direction="benefit",
            kind="compounding",
            visible_at_decision_time=True,
            ledger_entry_responsible="transform.regeneration_plan[0]",
            notes="compounds as soil C builds biota that builds more C",
        ),
        GenerationFactor(
            name="knowledge_transmission",
            introduced_at_generation=1,
            per_generation_amount=0.5,
            compounding_factor=0.10,
            unit="generations_of_knowledge_preserved",
            direction="benefit",
            kind="compounding",
            visible_at_decision_time=True,
            ledger_entry_responsible="labor[2]:E_h:elder_teaching",
        ),
    ]

    print("=" * 72)
    print("SEVEN-GENERATION TRACER — demo")
    print("=" * 72)

    for label, factors in [
        ("EXTRACTIVE proposal (costs compound)", extractive),
        ("REGENERATIVE proposal (benefits compound)", regenerative),
    ]:
        print(f"\n--- {label} ---")
        trace = trace_seven_generations(label, factors)
        for g in trace.generations:
            year = g.year_offset_estimate
            net = g.net_cumulative()
            mark = "+" if net > 0 else ("-" if net < 0 else "0")
            print(f"  gen {g.generation} (~yr +{year:3d}): "
                  f"cost={g.cumulative_cost:.2f} "
                  f"benefit={g.cumulative_benefit:.2f} "
                  f"net={net:+.2f} {mark}")
        if trace.compound_risk_horizon is not None:
            print(f"  ⚠ compound risk horizon: gen "
                  f"{trace.compound_risk_horizon} "
                  f"(~yr +{trace.compound_risk_horizon * YEARS_PER_GENERATION})")
        if trace.hidden_at_decision_time:
            print(f"  ! hidden at decision: "
                  f"{trace.hidden_at_decision_time}")
        c3 = trace_to_temporal_stability_7g(trace)
        print(f"  → C3.temporal_stability['7g'] = {c3!r}")
