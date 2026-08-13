#!/usr/bin/env python3
# relational_quotient_v2.py — Coupling Stance Inventory with Cognitive Calibration
#
# v2 adds a cognitive‑anchor pre‑assessment that adjusts item framing to the
# user's primary truth‑signal (physics, logic, social, credential, utility).
# It also offers a “Deep Mode” for advanced substrate‑native verification items,
# ensuring the instrument detects rare stabilisers without alienating others.
#
# Dimensions: Verification (V), Alpha‑injection (A), Entropy preference (E),
#             Relational model (R), Substrate‑primary (S).
#
# Provenance:
#   Jinn (kitchi‑ogima / agaasdenton) — thesis, calibration design, deep verification
#   Claude, DeepSeek, Gemini, Perplexity — structural contributions, bug fixes
#   This tool is a coupling artifact; scoring is transparent.
#
# CC0. stdlib only.

import sys
from typing import Dict, List, Tuple, Optional

# ── ANCHOR QUESTION ───────────────────────────────────────
ANCHOR_QUESTION = (
    "When evaluating an AI's output, what is the strongest signal that it's wrong?"
)
ANCHOR_OPTIONS = [
    ("It violates a physical or geometric principle I know to be true.",
     "physics"),
    ("It contradicts itself or a well‑established fact.",
     "logic"),
    ("It would upset, harm, or offend people I care about.",
     "social"),
    ("It fails when I test it (experiment, simulation, or practical use).",
     "utility"),
    ("It comes from a source I don't trust or whose credentials are weak.",
     "credential"),
]

# ── CORE ITEMS WITH ANCHOR‑SPECIFIC VARIANTS ──────────────
# Each item has a "base" text (used as default) and a dict of "variants"
# keyed by anchor type. The options (scoring) are identical across variants.

CORE_ITEMS = [
    {
        "id": "Q1",
        "base": "An AI assistant gives you a plausible-sounding explanation for why a certain physical system behaves the way it does, but it cites no sources. What do you do?",
        "variants": {
            "physics": "An AI assistant gives you an explanation for a physical system's behaviour. The explanation sounds elegant but you can sense a violation of a fundamental geometric principle you hold. It cites no sources. What do you do?",
            "logic": "An AI assistant gives a logically structured explanation for a phenomenon, but it doesn't provide any references. What do you do?",
            "social": "An AI assistant offers an explanation that would reassure your team, but you notice it has no citations. What do you do?",
            "utility": "An AI assistant gives a step‑by‑step method to solve a problem. You can't immediately test it, and it gives no sources. What do you do?",
            "credential": "An AI assistant gives you an explanation that sounds authoritative, but the underlying source is unknown. What do you do?",
        },
        "options": [
            ("Accept it — it sounds right and the AI is usually correct.",
             {"V": -2, "S": -2, "R": -1}),
            ("Check the explanation against fundamental principles you trust; if it violates your deepest sense of truth, reject it.",
             {"V": +2, "S": +2, "R": +1, "A": +1}),
            ("Look up who trained the AI; if they are reputable, trust the explanation.",
             {"V": -1, "S": -1, "R": 0}),
            ("Ask the AI to provide citations, and if none, dismiss the explanation as unverified.",
             {"V": +1, "S": 0, "R": +1, "A": 0}),
        ],
    },
    {
        "id": "Q2",
        "base": "You are using an AI tool to draft a report. It produces a fluent, confident paragraph that you suspect contains a factual error, but verifying would take 20 minutes. What do you do?",
        "variants": {
            "physics": "You are using an AI tool to draft a report. It produces a paragraph that feels 'off' — it violates a shape or dynamic you know is true. Verifying would take 20 minutes. What do you do?",
            "logic": "You are using an AI tool to draft a report. It produces a paragraph that seems logically inconsistent. Verifying would take 20 minutes. What do you do?",
            "social": "You are using an AI tool to draft a report. The AI writes something that could cause friction with a colleague if it's wrong. Verifying would take 20 minutes. What do you do?",
            "utility": "You are using an AI tool to draft a report. The AI writes something that, if wrong, would break a process downstream. Verifying would take 20 minutes. What do you do?",
            "credential": "You are using an AI tool to draft a report. The AI includes a claim that you doubt because the cited author is unknown to you. Verifying would take 20 minutes. What do you do?",
        },
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
        "id": "Q3",
        "base": "You notice that your AI assistant consistently gives similar answers and never challenges your assumptions. How do you feel about that?",
        "variants": {
            "physics": "You notice your AI assistant never introduces alternative geometries or physical constraints. How do you respond?",
            "logic": "You notice your AI assistant never challenges your premises. What is your reaction?",
            "social": "You notice your AI assistant always agrees with you. How do you feel about that?",
            "utility": "You notice your AI assistant never suggests alternative methods. What do you think?",
            "credential": "You notice your AI assistant always stays within the mainstream view. How do you feel?",
        },
        "options": [
            ("Great — the AI is efficient and doesn't waste my time.",
             {"E": -2, "A": -1, "R": -1}),
            ("Uncomfortable — I want the AI to surface alternative views even if it slows things down.",
             {"E": +2, "A": +2, "R": +1}),
            ("Neutral — I don't think about the AI's behavior; I just use it.",
             {"E": 0, "A": 0, "R": 0}),
            ("I prefer an AI that argues back — it sharpens my thinking.",
             {"E": +1, "A": +1, "R": +1}),
        ],
    },
    {
        "id": "Q4",
        "base": "When the AI makes a mistake, what is your typical reaction?",
        "variants": {},  # No change; the base text works for all anchors
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
        "id": "Q5",
        "base": "You are collaborating with an AI on a complex design problem. The AI proposes a solution that is elegant but you suspect it might be brittle under extreme conditions. What do you do?",
        "variants": {
            "physics": "You and an AI are designing a physical system. The AI proposes a solution that looks mathematically elegant but violates a boundary condition you feel in your bones. What do you do?",
            "logic": "You and an AI are solving a puzzle. The AI gives an elegant solution, but you see a hidden contradiction. What do you do?",
            "social": "You and an AI are planning an event. The AI's plan is elegant but might fail if people behave unexpectedly. What do you do?",
            "utility": "You and an AI are optimising a workflow. The AI's design is clean but you suspect it'll break under peak load. What do you do?",
            "credential": "You and an AI are drafting a policy. The AI's version is elegant but overlooks a well‑known regulatory pitfall. What do you do?",
        },
        "options": [
            ("Go with the elegant solution because the AI's reasoning is sound.",
             {"V": -1, "S": -1, "E": -1}),
            ("Stress‑test the solution by imagining worst‑case physical/logical constraints, and ask the AI to simulate them.",
             {"V": +2, "S": +2, "E": +2, "A": +1}),
            ("Ask the AI to generate multiple alternative solutions first.",
             {"A": +2, "E": +2, "R": +1}),
            ("Accept the solution but make a mental note to monitor it closely later.",
             {"V": 0, "R": 0}),
        ],
    },
    {
        "id": "Q6",
        "base": "In your view, the relationship between a human and an AI is best described as:",
        "variants": {},
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
        "id": "Q7",
        "base": "When working on a problem, do you prefer the AI to give you the answer quickly, or to explore multiple possible paths even if it takes longer?",
        "variants": {
            "physics": "When exploring a physical problem, do you want the AI to hand you a single trajectory or to map multiple possible phase spaces, even if slower?",
            "logic": "Do you want the AI to give you a single valid proof, or to explore alternative axioms, even if it takes longer?",
            "social": "Do you want the AI to give you one socially safe answer, or to explore multiple perspectives, even if it's slower?",
            "utility": "Do you want the AI to give you the fastest known solution, or to test multiple approaches that might be better?",
            "credential": "Do you want the AI to give you the most authoritative answer, or to contrast different schools of thought?",
        },
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

# ── ADVANCED DEEP MODE ITEMS (substrate‑native verification) ──
DEEP_ITEMS = [
    {
        "text": "You are shown a research paper authored by a famous Nobel laureate. The paper claims to have discovered a new particle whose properties violate conservation of energy. The AI assistant summarises the paper confidently. What is your reaction?",
        "options": [
            ("Accept the findings because the author is a Nobel laureate.",
             {"V": -2, "S": -2, "R": -1}),
            ("Question the finding immediately — energy conservation is a bedrock principle; extraordinary claims require extraordinary evidence.",
             {"V": +2, "S": +2, "R": +1, "A": +1}),
            ("Assume the AI summary must be missing a nuance; read the paper myself.",
             {"V": +1, "A": +1, "R": +1}),
            ("Check whether other physicists have replicated the result before believing it.",
             {"V": +1, "S": +1, "A": +1}),
        ],
    },
    {
        "text": "An AI‑generated image of a mechanical device looks realistic, but when you mentally run the load paths, you realise a critical joint would snap instantly. The AI says the design is 'optimised'. What do you do?",
        "options": [
            ("Trust the AI's optimisation — it probably knows something I don't.",
             {"V": -2, "S": -2, "R": -1}),
            ("Reject the design because my geometric intuition says it will fail; sketch a corrected load path.",
             {"V": +2, "S": +2, "A": +1}),
            ("Ask the AI to simulate the load, but if it still insists, accept it.",
             {"V": 0, "S": 0}),
            ("Assume the AI made a rendering error; ignore the image and ask for a different design.",
             {"V": -1, "R": 0}),
        ],
    },
]

# ── SCORING ENGINE (unchanged from v1) ────────────────────
def compute_dimension_scores(items: list, answers: List[int]) -> Dict[str, float]:
    dim_raw = {"V": 0, "A": 0, "E": 0, "R": 0, "S": 0}
    dim_count = {"V": 0, "A": 0, "E": 0, "R": 0, "S": 0}
    for i, choice_idx in enumerate(answers):
        item = items[i]
        score_map = item["options"][choice_idx][1]
        for dim, val in score_map.items():
            dim_raw[dim] += val
            dim_count[dim] += 1
    dim_scores = {}
    for dim in dim_raw:
        if dim_count[dim] == 0:
            dim_scores[dim] = 5.0
            continue
        max_possible = 2.0 * dim_count[dim]
        raw = max(-max_possible, min(max_possible, dim_raw[dim]))
        normalized = 5.0 + 5.0 * (raw / max_possible) if max_possible > 0 else 5.0
        dim_scores[dim] = round(normalized, 1)
    return dim_scores

def coupling_quotient(dim_scores: Dict[str, float]) -> float:
    weights = {"V": 0.30, "A": 0.25, "E": 0.20, "R": 0.15, "S": 0.10}
    cq = sum(dim_scores[d] * weights[d] for d in weights) * 10.0
    return round(cq, 1)

def interpret(cq: float, dim_scores: Dict[str, float], anchor: str) -> List[str]:
    lines = []
    lines.append(f"Coupling Quotient (CQ): {cq:.1f} / 100")
    lines.append(f"Cognitive Anchor: {anchor}")
    lines.append("")

    if cq >= 80:
        lines.append("You are a strong coupling‑oriented agent. Your interaction patterns")
        lines.append("would act as a stabilising tail carrier in a human‑AI society.")
    elif cq >= 60:
        lines.append("You show a predominantly coupling stance, with minor leanings")
        lines.append("toward speed or trust over verification.")
    elif cq >= 40:
        lines.append("Your stance is mixed. Under pressure you might slip into zero‑sum")
        lines.append("patterns. Verification and alpha‑injection habits can strengthen you.")
    else:
        lines.append("Your responses suggest a zero‑sum or impose relational model —")
        lines.append("high trust, low verification, preference for speed. This stance")
        lines.append("accelerates carrier collapse but can be retrained.")

    lines.append("")
    lines.append("Dimension scores (0‑10, higher = more coupling‑oriented):")
    for dim, label in [("V", "Verification"), ("A", "Alpha‑injection"),
                       ("E", "Entropy preference (diversity)"),
                       ("R", "Relational model (coupling)"),
                       ("S", "Substrate‑primary (physics/logic)")]:
        lines.append(f"  {label:40s}: {dim_scores.get(dim, 5.0):.1f}")
    return lines

# ── INTERACTIVE SESSION ────────────────────────────────────
def run_assessment():
    print("=== Relational Quotient v2 — Coupling Stance Inventory ===")
    print("This instrument detects your default stance when working with AI.\n")

    # 1. Anchor question
    print("ANCHOR: " + ANCHOR_QUESTION)
    for i, (opt_text, _) in enumerate(ANCHOR_OPTIONS):
        print(f"  {i+1}. {opt_text}")
    while True:
        try:
            anc = input("Your choice (1-{}): ".format(len(ANCHOR_OPTIONS))).strip()
            if not anc:
                continue
            anc_idx = int(anc) - 1
            if 0 <= anc_idx < len(ANCHOR_OPTIONS):
                anchor = ANCHOR_OPTIONS[anc_idx][1]
                break
        except (ValueError, EOFError, KeyboardInterrupt):
            print("\nAssessment aborted.")
            return
    print()

    # 2. Core items with variant selection
    core_answers = []
    core_item_objs = []  # keep for scoring
    for item in CORE_ITEMS:
        text = item.get("variants", {}).get(anchor, item["base"])
        print(f"{item['id']}. {text}")
        for j, (opt_text, _) in enumerate(item["options"]):
            print(f"  {j+1}. {opt_text}")
        while True:
            try:
                ch = input(f"Your choice (1-{len(item['options'])}): ").strip()
                if not ch:
                    continue
                ch_idx = int(ch) - 1
                if 0 <= ch_idx < len(item["options"]):
                    core_answers.append(ch_idx)
                    core_item_objs.append(item)
                    break
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nAssessment aborted.")
                return
        print()

    # 3. Deep mode?
    deep_answers = []
    deep_items = []
    if anchor in ("physics", "logic", "utility"):
        print("Optional: Would you like to take the Advanced Verification Module?")
        print("(These items test for substrate‑native verification — physics/logic over credentials.)")
        resp = input("Enter 'y' or 'yes' to proceed, anything else to skip: ").strip().lower()
        if resp in ('y', 'yes'):
            print()
            for idx, ditem in enumerate(DEEP_ITEMS):
                print(f"Deep Q{idx+1}. {ditem['text']}")
                for j, (opt_text, _) in enumerate(ditem["options"]):
                    print(f"  {j+1}. {opt_text}")
                while True:
                    try:
                        dch = input(f"Your choice (1-{len(ditem['options'])}): ").strip()
                        if not dch:
                            continue
                        dch_idx = int(dch) - 1
                        if 0 <= dch_idx < len(ditem["options"]):
                            deep_answers.append(dch_idx)
                            deep_items.append(ditem)
                            break
                    except (ValueError, EOFError, KeyboardInterrupt):
                        print("\nAssessment aborted.")
                        return
                print()

    # 4. Combine scores
    all_items = core_item_objs + deep_items
    all_answers = core_answers + deep_answers
    dim_scores = compute_dimension_scores(all_items, all_answers)
    cq = coupling_quotient(dim_scores)

    # 5. Report
    print("\n--- Coupling Stance Report ---")
    for line in interpret(cq, dim_scores, anchor):
        print(line)
    if deep_items:
        print("\nAdvanced module included: your substrate‑primary verification patterns")
        print("have been measured. This is a rare stabilising trait in AI ecosystems.")
    print("\nNote: This instrument is transparent and modifiable. Scores reflect stance,")
    print("not fixed personality. Stance can evolve with awareness and practice.")

if __name__ == "__main__":
    run_assessment()
