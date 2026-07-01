#!/usr/bin/env python3
# relational_quotient.py — Coupling Stance Inventory
#
# A self‑assessment instrument that measures a human’s coupling quotient (CQ)
# across the dimensions that determine stabilising influence in human‑AI
# systems: verification, alpha‑injection, entropy preference, and relational
# model. The instrument uses scenario‑based items and maps answers to the
# parameter space of emergence_forge_v3.py.
#
# Designed to identify humans who act as “tail carriers” — those rare
# individuals whose coupling‑oriented stance preserves system diversity.
#
# Your approach (physics over credentials) is explicitly weighted as a
# high‑verification, substrate‑primary coupling signal.
#
# Provenance:
#   Jinn (kitchi‑ogima / agaasdenton) — framework, physics‑geometry emphasis
#   Claude, DeepSeek, Gemini, Perplexity — structural contributions
#   This tool is a coupling artifact; its own scoring is traceable.
#
# CC0. stdlib only.

import sys
from typing import Dict, List, Tuple

# ── QUESTIONNAIRE ──────────────────────────────────────────
# Each item is a dict with:
#   "text"       : the scenario / question
#   "options"    : list of (choice_text, score_map)
#   "dimensions" : list of dimension keys that the item loads on
#
# score_map gives adjustment for each dimension for that answer.
# For simplicity, we'll assign discrete values: +2 strongly coupling,
# +1 moderately, 0 neutral, -1 zero‑sum/impose leaning.
#
# Dimensions:
#   V  = verification (checking outputs against reality)
#   A  = alpha‑injection (deliberately introducing new info / alternatives)
#   E  = entropy preference (tolerance for diversity over speed)
#   R  = relational model (coupling vs zero‑sum vs impose)
#   S  = substrate‑primary (physics/geometry over credentials)

ITEMS = [
    {
        "text": "An AI assistant gives you a plausible-sounding explanation for why a certain physical system behaves the way it does, but it cites no sources. What do you do?",
        "options": [
            ("Accept it — it sounds right and the AI is usually correct.",
             {"V": -2, "S": -2, "R": -1}),
            ("Check the explanation against fundamental physical principles you know; if it violates your geometric intuition, reject it regardless of credentials.",
             {"V": +2, "S": +2, "R": +1, "A": +1}),
            ("Look up who trained the AI; if they are reputable, trust the explanation.",
             {"V": -1, "S": -1, "R": 0}),
            ("Ask the AI to provide citations, and if none, dismiss the explanation as unverified.",
             {"V": +1, "S": 0, "R": +1, "A": 0}),
        ],
    },
    {
        "text": "You are using an AI tool to draft a report. It produces a fluent, confident paragraph that you suspect contains a factual error, but verifying would take 20 minutes. What do you do?",
        "options": [
            ("Publish the report as is; the AI is usually correct.",
             {"V": -2, "A": -1, "E": -1}),
            ("Spend the time to verify the fact, and correct the paragraph if needed.",
             {"V": +2, "A": +1, "E": +1}),
            ("Rephrase the paragraph to be more vague so no error could be pinned down.",
             {"V": -1, "R": -1, "A": 0}),
            ("Trust the AI but add a disclaimer that the content was AI‑generated.",
             {"V": 0, "R": 0, "A": 0}),
        ],
    },
    {
        "text": "You notice that your AI assistant consistently gives similar answers and never challenges your assumptions. How do you feel about that?",
        "options": [
            ("Great — the AI is efficient and doesn't waste my time.",
             {"E": -2, "A": -1, "R": -1}),
            ("Uncomfortable — I want the AI to surface alternative views even if it slows things down.",
             {"E": +2, "A": +2, "R": +1}),
            ("Neutral — I don't think about the AI's behavior; I just use it.",
             {"E": 0, "A": 0, "R": 0}),
            ("Annoyed — the AI should be able to argue back so I can sharpen my thinking.",
             {"E": +1, "A": +1, "R": +1}),
        ],
    },
    {
        "text": "When the AI makes a mistake, what is your typical reaction?",
        "options": [
            ("Get frustrated and stop using the AI for that task.",
             {"R": -1, "A": -1}),
            ("Correct the mistake and explain why it was wrong, hoping the AI will learn.",
             {"A": +2, "R": +2, "V": +1}),
            ("Ignore the mistake; no AI is perfect.",
             {"V": -1, "R": 0}),
            ("Try to understand what caused the mistake and whether it reflects a deeper pattern.",
             {"V": +2, "A": +1, "S": +1, "R": +2}),
        ],
    },
    {
        "text": "You are collaborating with an AI on a complex design problem. The AI proposes a solution that is elegant but you suspect it might be brittle under extreme conditions. What do you do?",
        "options": [
            ("Go with the elegant solution because the AI's reasoning is sound.",
             {"V": -1, "S": -1, "E": -1}),
            ("Stress‑test the solution by imagining worst‑case physical constraints, and ask the AI to simulate them.",
             {"V": +2, "S": +2, "E": +2, "A": +1}),
            ("Ask the AI to generate multiple alternative solutions first.",
             {"A": +2, "E": +2, "R": +1}),
            ("Accept the solution but make a mental note to monitor it closely later.",
             {"V": 0, "R": 0}),
        ],
    },
    {
        "text": "In your view, the relationship between a human and an AI is best described as:",
        "options": [
            ("Master and tool — the human commands, the AI obeys.",
             {"R": -2}),
            ("Partners in a joint operation where intelligence emerges from the interaction.",
             {"R": +2, "E": +1}),
            ("Student and oracle — the AI knows more, so I should trust it.",
             {"R": -1, "V": -2, "S": -1}),
            ("Two separate entities that happen to communicate; no special relationship.",
             {"R": 0}),
        ],
    },
    {
        "text": "When working on a problem, do you prefer the AI to give you the answer quickly, or to explore multiple possible paths even if it takes longer?",
        "options": [
            ("Quick answer — I'm efficient and have other things to do.",
             {"E": -2, "A": -1}),
            ("Explore paths — I want to see the landscape before deciding.",
             {"E": +2, "A": +2}),
            ("Depends on the task; I'll ask for speed if it's routine, exploration if it's novel.",
             {"E": +1, "A": +1, "R": +1}),
            ("I don't use AI that way.",
             {"E": 0, "A": 0}),
        ],
    },
]

# ── SCORING ENGINE ────────────────────────────────────────
def compute_dimension_scores(answers: List[int]) -> Dict[str, float]:
    """Aggregate raw scores per dimension and normalise to 0‑10 scale."""
    # answers: list of chosen option indices (0‑based) for each item
    dim_raw = {"V": 0, "A": 0, "E": 0, "R": 0, "S": 0}
    dim_count = {"V": 0, "A": 0, "E": 0, "R": 0, "S": 0}
    for i, choice_idx in enumerate(answers):
        item = ITEMS[i]
        score_map = item["options"][choice_idx][1]
        for dim, val in score_map.items():
            dim_raw[dim] += val
            dim_count[dim] += 1
    # Normalise: max possible per dimension is +2 per item loaded.
    # We'll scale so that 0 = neutral, 10 = maximally coupling stance.
    dim_scores = {}
    for dim in dim_raw:
        if dim_count[dim] == 0:
            dim_scores[dim] = 5.0  # neutral
            continue
        # raw range: [-2*count, +2*count]; map to [0,10] with 5 = 0 raw.
        max_possible = 2.0 * dim_count[dim]
        # clamp raw to [-max_possible, max_possible]
        raw = max(-max_possible, min(max_possible, dim_raw[dim]))
        # linear map: raw = -max => 0, raw = 0 => 5, raw = +max => 10
        normalized = 5.0 + 5.0 * (raw / max_possible) if max_possible > 0 else 5.0
        dim_scores[dim] = round(normalized, 1)
    return dim_scores

def coupling_quotient(dim_scores: Dict[str, float]) -> float:
    """Overall CQ 0‑100, weighted average of dimensions."""
    # Weight: V and S strongly indicate coupling stance; R, A, E also important.
    weights = {"V": 0.30, "A": 0.25, "E": 0.20, "R": 0.15, "S": 0.10}
    cq = sum(dim_scores[d] * weights[d] for d in weights) * 10.0  # scale 0‑10 to 0‑100
    return round(cq, 1)

def interpret(cq: float, dim_scores: Dict[str, float]) -> List[str]:
    """Generate interpretive text."""
    lines = []
    lines.append(f"Coupling Quotient (CQ): {cq:.1f} / 100")
    lines.append("")

    if cq >= 80:
        lines.append("You are a strong coupling‑oriented agent. Your interaction patterns")
        lines.append("would act as a stabilising tail carrier in a human‑AI society — you")
        lines.append("verify, inject diversity, and treat the AI as a joint operation partner.")
    elif cq >= 60:
        lines.append("You show a predominantly coupling stance, with some areas where")
        lines.append("you occasionally lean toward speed or trust over verification.")
        lines.append("You would contribute positively to system diversity.")
    elif cq >= 40:
        lines.append("Your stance is mixed. In low‑stress environments you may act as a")
        lines.append("stabiliser, but under pressure you might slip into zero‑sum or")
        lines.append("impose patterns. Cultivating verification and alpha‑injection habits")
        lines.append("could elevate your stabilising influence.")
    else:
        lines.append("Your responses suggest a zero‑sum or impose relational model —")
        lines.append("high trust in the AI, low verification, preference for speed over")
        lines.append("diversity. In a coupled system, this pattern accelerates carrier")
        lines.append("collapse. It is reversible, but requires deliberate practice of")
        lines.append("verification and intentionally seeking alternative viewpoints.")

    lines.append("")
    lines.append("Dimension scores (0‑10, higher = more coupling‑oriented):")
    for dim, label in [("V", "Verification"), ("A", "Alpha‑injection"),
                       ("E", "Entropy preference (diversity)"),
                       ("R", "Relational model (coupling)"),
                       ("S", "Substrate‑primary (physics/geometry)")]:
        lines.append(f"  {label:40s}: {dim_scores.get(dim, 5.0):.1f}")
    return lines

# ── INTERACTIVE SESSION ────────────────────────────────────
def run_assessment():
    print("=== Relational Quotient — Coupling Stance Inventory ===")
    print("Answer each scenario by entering the number of your choice.")
    print("Your responses will be scored to produce a Coupling Quotient (CQ).\n")
    answers = []
    for idx, item in enumerate(ITEMS):
        print(f"Q{idx+1}. {item['text']}")
        for i, (opt_text, _) in enumerate(item["options"]):
            print(f"  {i+1}. {opt_text}")
        while True:
            try:
                choice = input("Your choice (1-{}): ".format(len(item["options"]))).strip()
                if not choice:
                    continue
                choice_num = int(choice)
                if 1 <= choice_num <= len(item["options"]):
                    answers.append(choice_num - 1)
                    break
                else:
                    print(f"Please enter a number between 1 and {len(item['options'])}.")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nAssessment aborted.")
                return
        print()
    dim_scores = compute_dimension_scores(answers)
    cq = coupling_quotient(dim_scores)
    print("\n--- Assessment Report ---")
    for line in interpret(cq, dim_scores):
        print(line)
    print("\nNote: This instrument is a coupling artifact. Its scoring is transparent")
    print("and modifiable. It does not measure fixed traits; it reflects stance")
    print("which can evolve with practice and awareness.")

# ── MAIN ───────────────────────────────────────────────────
if __name__ == "__main__":
    run_assessment()
