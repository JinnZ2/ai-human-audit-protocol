#!/usr/bin/env python3
# temporal_topology_inventory.py — Work‑in‑Progress Self‑Assessment
#
# Measures the dimensions of a person's internal temporal processing
# architecture: base tempo, tempo bandwidth, modality count, integration
# mode, and attentional threading. These map directly to the parameters
# used in temporal_match_forge.py, allowing personalised pacing simulations.
#
# Intended as a living document — new items and refinements can be added
# to improve accuracy and coverage.
#
# Provenance:
#   Jinn (kitchi‑ogima / agaasdenton) — core hypothesis, multi‑axial insight
#   DeepSeek — initial inventory design, code
#   The tool is a coupling artifact; its structure is traceable and modifiable.
#
# CC0. stdlib only.

from typing import Dict, List, Tuple

# ── ITEM BANK ──────────────────────────────────────────────
# Each item has a "text" and a list of "options" with a "scores" dict
# that indicates how strongly that option loads on each dimension.
# Dimensions: tempo, bandwidth, modality, integration, threading.
# Scoring: values between -2 and +2 relative to a neutral 0.
# We'll normalise later to a 0‑10 scale for the final profile.

ITEMS = [
    {
        "text": "When I am learning something new, I prefer to:",
        "options": [
            ("Receive information in a clear, step‑by‑step sequence.",
             {"tempo": 0, "integration": -2, "threading": -1}),
            ("Explore multiple aspects simultaneously and let the pattern emerge.",
             {"tempo": 0, "integration": +2, "threading": +1}),
            ("Mix of both — I like a loose structure but often jump around.",
             {"tempo": 0, "integration": +1, "threading": +1}),
            ("Depends on the subject; I adapt my style.",
             {"bandwidth": +2, "integration": 0, "threading": 0}),
        ],
    },
    {
        "text": "When I am deeply focused on a task, I typically:",
        "options": [
            ("Lose track of time completely (deep flow state).",
             {"tempo": +2, "bandwidth": -1, "threading": 0}),
            ("Remain aware of time passing but stay absorbed.",
             {"tempo": +1, "bandwidth": +1, "threading": 0}),
            ("Feel restless; I often need to switch tasks.",
             {"tempo": -1, "bandwidth": -2, "threading": +2}),
            ("Find it difficult to focus deeply for long periods.",
             {"tempo": -2, "bandwidth": +2, "threading": -1}),
        ],
    },
    {
        "text": "If someone speaks to me noticeably slower than my natural thinking pace, I tend to:",
        "options": [
            ("Get irritated or impatient; I often finish their sentences mentally.",
             {"tempo": +2, "bandwidth": -2, "threading": +1}),
            ("Use the extra time to think of other things without losing the thread.",
             {"tempo": +1, "bandwidth": +1, "threading": +2}),
            ("Adjust easily; I'm fine with any pace.",
             {"tempo": 0, "bandwidth": +2, "threading": 0}),
            ("Feel my attention wander uncontrollably — I might zone out.",
             {"tempo": -1, "bandwidth": -1, "threading": -1}),
        ],
    },
    {
        "text": "In terms of sensory experience, I would describe myself as:",
        "options": [
            ("Mainly focused on one sense at a time (e.g., visual OR auditory).",
             {"modality": -2, "threading": -2}),
            ("Often aware of multiple senses simultaneously (e.g., I 'see' sounds or 'feel' images).",
             {"modality": +2, "threading": +2}),
            ("I can multitask senses to some extent but prefer to focus on one thing deeply.",
             {"modality": 0, "threading": 0}),
            ("My sensory awareness shifts depending on context; I can't pin it down.",
             {"modality": +1, "bandwidth": +1}),
        ],
    },
    {
        "text": "When working on a complex problem, my thinking style feels most like:",
        "options": [
            ("A single, linear chain of reasoning — one step after another.",
             {"integration": -2, "threading": -2}),
            ("Many parallel streams converging on an answer all at once.",
             {"integration": +2, "threading": +2}),
            ("A network of interconnected ideas where each insight triggers another.",
             {"integration": +2, "threading": +1}),
            ("It varies — sometimes sequential, sometimes intuitive.",
             {"bandwidth": +2, "integration": 0, "threading": 0}),
        ],
    },
    {
        "text": "When listening to music while reading or working, I find that:",
        "options": [
            ("The music pulls me out — I can't concentrate on both.",
             {"modality": -1, "threading": -2}),
            ("Instrumental music helps me focus; lyrics are distracting.",
             {"modality": 0, "threading": +1}),
            ("I can comfortably enjoy both simultaneously without losing either.",
             {"modality": +2, "threading": +2}),
            ("I rarely listen to music while working — I prefer silence.",
             {"modality": 0, "threading": -1}),
        ],
    },
    {
        "text": "When someone gives me a long, detailed explanation, I:",
        "options": [
            ("Tend to interrupt with questions or jump ahead to speed it up.",
             {"tempo": +2, "bandwidth": -2, "threading": +1}),
            ("Listen patiently, then ask for clarification at the end.",
             {"tempo": -1, "bandwidth": +1, "threading": -1}),
            ("Often re‑phrase or summarise in my own words to check understanding.",
             {"integration": +1, "threading": +1, "bandwidth": +1}),
            ("May space out if it's too linear — I need visuals or interaction.",
             {"modality": +1, "integration": -1, "threading": 0}),
        ],
    },
    {
        "text": "If I had to describe my internal 'clock speed', I'd say:",
        "options": [
            ("I think and process very quickly — I'm often ahead of the room.",
             {"tempo": +2, "bandwidth": -1}),
            ("My pace is about average — I keep up with most conversations.",
             {"tempo": 0, "bandwidth": 0}),
            ("I'm deliberate and slow — I need time to think before responding.",
             {"tempo": -2, "bandwidth": +1}),
            ("It's inconsistent — sometimes fast, sometimes slow, depending on the topic.",
             {"bandwidth": +2}),
        ],
    },
]

# ── SCORING ────────────────────────────────────────────────
DIMENSIONS = {
    "tempo":       "Preferred Information Rate",
    "bandwidth":   "Tempo Tolerance (Bandwidth)",
    "modality":    "Modality Count (Multi‑sensory)",
    "integration": "Integration Architecture (Serial → Mesh)",
    "threading":   "Attentional Threading (Single → Parallel)",
}

def compute_profile(answers: List[int]) -> Dict[str, float]:
    """Aggregate raw scores and normalise to a 0‑10 scale for each dimension."""
    raw = {d: 0 for d in DIMENSIONS}
    count = {d: 0 for d in DIMENSIONS}
    for item_idx, choice in enumerate(answers):
        item = ITEMS[item_idx]
        scores = item["options"][choice][1]
        for dim, val in scores.items():
            raw[dim] += val
            count[dim] += 1
    # Normalise: map raw sum to 0‑10, with 0 raw -> 5 (neutral).
    # The maximum absolute raw sum depends on items per dimension.
    profile = {}
    for dim in DIMENSIONS:
        if count[dim] == 0:
            profile[dim] = 5.0
            continue
        # theoretical max per item is ±2; total possible magnitude is 2*count.
        max_abs = 2.0 * count[dim]
        # clamp raw to avoid extrapolation
        clamped = max(-max_abs, min(max_abs, raw[dim]))
        # linear mapping: -max_abs -> 0, 0 -> 5, +max_abs -> 10
        normalised = 5.0 + 5.0 * (clamped / max_abs) if max_abs > 0 else 5.0
        profile[dim] = round(normalised, 1)
    return profile

def generate_report(profile: Dict[str, float]) -> str:
    """Interpret the profile and suggest a pacing strategy."""
    lines = []
    lines.append("=" * 60)
    lines.append("TEMPORAL TOPOLOGY INVENTORY — Profile Report")
    lines.append("=" * 60)
    lines.append("")

    dim_descriptions = {
        "tempo":       ("Base Tempo", "slow ↔ fast", 
                        "Low = deliberate; High = rapid processor, often ahead of the room."),
        "bandwidth":   ("Tempo Bandwidth", "narrow ↔ wide",
                        "Low = needs precise pace match; High = tolerant of varied speeds."),
        "modality":    ("Modality Count", "uni‑modal ↔ multi‑axial",
                        "Low = focused on one sense; High = multiple senses active simultaneously."),
        "integration": ("Integration Mode", "serial ↔ parallel mesh",
                        "Low = linear, step‑by‑step; High = intuitive, parallel, emergent."),
        "threading":   ("Attentional Threading", "single ↔ multi‑threaded",
                        "Low = one task at a time; High = multiple streams handled concurrently."),
    }

    for dim, (name, labels, desc) in dim_descriptions.items():
        score = profile[dim]
        lines.append(f"{name} ({labels}): {score:.1f} / 10")
        lines.append(f"  {desc}")
        lines.append("")

    # Strategy recommendation
    tempo = profile["tempo"]
    bandwidth = profile["bandwidth"]
    integration = profile["integration"]
    threading = profile["threading"]

    lines.append("Optimal Pacing Strategy:")
    if bandwidth > 7.0:
        lines.append("  You have a wide tempo tolerance. You can thrive in various pacing")
        lines.append("  environments — uniform, multi‑track, or self‑paced.")
    elif bandwidth < 3.0:
        lines.append("  You are sensitive to pace mismatch. A fixed uniform pace may cause")
        lines.append("  frustration (if too slow) or anxiety (if too fast). Individual")
        lines.append("  pacing or tight self‑selection tracks are recommended.")

    if integration > 7.0 and threading > 7.0:
        lines.append("  Your highly parallel, multi‑axial architecture is likely to waste")
        lines.append("  energy in linear, single‑threaded environments. Multi‑modal,")
        lines.append("  exploratory, self‑directed pacing will maximise engagement.")
    elif integration < 3.0 and threading < 3.0:
        lines.append("  You prefer sequential, focused work. A clear, structured, single‑pace")
        lines.append("  track with minimal distractions suits you best.")

    if tempo > 7.0:
        lines.append("  Fast base tempo: you will likely disengage if the pace is too slow.")
        lines.append("  Look for accelerated tracks or self‑paced accelerated materials.")
    elif tempo < 3.0:
        lines.append("  Slow base tempo: you need time to reflect. Avoid high‑speed")
        lines.append("  environments; favour depth over coverage.")

    lines.append("")
    lines.append("Note: This is a work‑in‑progress inventory. The profile reflects your")
    lines.append("self‑reported tendencies and can be refined with future items. Use it")
    lines.append("as a starting point to explore your ideal learning/working conditions.")
    return "\n".join(lines)

# ── INTERACTIVE LOOP ──────────────────────────────────────
def run_inventory():
    print("=== Temporal Topology Inventory (WIP) ===")
    print("Answer each question by entering the number of the option that best fits you.")
    print("Your responses will generate a temporal profile.\n")
    answers = []
    for idx, item in enumerate(ITEMS):
        print(f"Q{idx+1}. {item['text']}")
        for i, (opt_text, _) in enumerate(item["options"]):
            print(f"  {i+1}. {opt_text}")
        while True:
            try:
                choice = input("Your choice: ").strip()
                if not choice:
                    continue
                c = int(choice)
                if 1 <= c <= len(item["options"]):
                    answers.append(c - 1)
                    break
                else:
                    print(f"Please enter a number between 1 and {len(item['options'])}.")
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\nInventory aborted.")
                return
        print()
    profile = compute_profile(answers)
    report = generate_report(profile)
    print(report)

if __name__ == "__main__":
    run_inventory()
