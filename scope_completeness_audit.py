#!/usr/bin/env python3
# scope_completeness_audit.py — calibrate productivity studies against
# the full human‑AI coupling surface.
#
# Thesis: "The operation is the unit." Productivity is not a property of
# the AI or the human alone, but of the coupled system plus its environment.
# This tool audits how completely a study measures the space:
#
#   P = f(H, A, T, E, O, C, V, t, M, I, S, Op, tok)
#
# where the dimensions beyond the core function include maintenance debt,
# specification cost, integration cost, opportunity cost, output tokens as
# a proxy, and environmental/ organisational depth.
#
# Output: a completeness score, a collapse‑risk flag, and a report that
# reveals the dark matter of productivity — the variables no one measured.
#
# Provenance:
#   • Jinn (kitchi‑ogima / agaasdenton) — thesis, variable matrix, call.
#   • Claude — relational‑operation framework, initial forge & audit ideas.
#   • Gemini — dynamic features (FELTSensor, entropy) that shaped the lens.
#   • DeepSeek — final integration, code, reflexivity closure.
# This tool was built by a multi‑node coupling; its own completeness is
# its provenance.
#
# CC0. stdlib only.

import sys
import json
from typing import Dict, List, Tuple, Optional, Set

# ── THE FULL DIMENSION SET ──────────────────────────────────
# Each dimension is a string key. Weight indicates its importance for a
# coupling‑centric completeness score.
DIMENSIONS = {
    # Core coupling variables
    "H":  {"label": "Human capability",              "weight": 0.10, "category": "node"},
    "A":  {"label": "AI capability",                  "weight": 0.10, "category": "node"},
    "T":  {"label": "Task characteristics",           "weight": 0.05, "category": "task"},
    "E":  {"label": "Environmental conditions",       "weight": 0.15, "category": "substrate"},
    "O":  {"label": "Organisational factors",         "weight": 0.10, "category": "coupling"},
    "C":  {"label": "Coordination & communication",   "weight": 0.15, "category": "coupling"},
    "V":  {"label": "Verification & validation cost", "weight": 0.20, "category": "coupling"},
    "t":  {"label": "Time horizon",                   "weight": 0.15, "category": "coupling"},
    # Additional critical variables you identified
    "M":  {"label": "Maintenance debt",               "weight": 0.20, "category": "coupling"},  # future rework
    "I":  {"label": "Integration cost",               "weight": 0.10, "category": "coupling"},
    "S":  {"label": "Specification cost",             "weight": 0.10, "category": "coupling"},
    "Op": {"label": "Opportunity cost",               "weight": 0.05, "category": "coupling"},
    "tok":{"label": "Output token volume (proxy)",    "weight": -0.10,"category": "proxy"},  # negative weight: over-reliance reduces score
}

# Weight sum for normalisation (absolute values, excluding tok penalty)
ABS_WEIGHT_SUM = sum(abs(v["weight"]) for k,v in DIMENSIONS.items() if k != "tok")
# But we'll handle scoring differently: each measured variable contributes +weight;
# each omitted variable contributes 0; 'estimated' gives half; 'over-relied' on token proxy triggers risk.

# ── STUDY REPRESENTATION ────────────────────────────────────
class ProductivityStudy:
    """Holds a study's measurement status for each dimension."""
    def __init__(self, name: str, source: str = "",
                 status: Dict[str, str] = None):
        """
        status: dict mapping dimension key to one of:
          "measured", "estimated", "omitted", "over-relied"
        """
        self.name = name
        self.source = source
        # Initialise all dimensions as "omitted"
        self.status = {key: "omitted" for key in DIMENSIONS}
        if status:
            for key, val in status.items():
                if key in DIMENSIONS:
                    self.status[key] = val

    def set_status(self, key, val):
        if key in DIMENSIONS:
            self.status[key] = val

# ── AUDIT FUNCTIONS ─────────────────────────────────────────
def completeness_score(study: ProductivityStudy) -> float:
    """
    Returns a score 0‑1 based on how many high‑weight dimensions are measured
    or estimated (with full/half credit). Over‑reliance on token proxy
    applies a penalty.
    """
    score = 0.0
    total_weight = 0.0
    for key, info in DIMENSIONS.items():
        w = info["weight"]
        if key == "tok":
            # token proxy is not part of the positive score; it's a risk flag
            continue
        total_weight += w
        s = study.status.get(key, "omitted")
        if s == "measured":
            score += w
        elif s == "estimated":
            score += 0.5 * w
        # omitted gives 0
    # Normalise to 0‑1
    if total_weight == 0:
        return 0.0
    base = score / total_weight

    # Token over‑reliance penalty: if tok is "over-relied", subtract 0.15 from final score
    if study.status.get("tok") == "over-relied":
        base = max(0.0, base - 0.15)
    return base

def collapse_risk(study: ProductivityStudy) -> Tuple[str, List[str]]:
    """
    Returns a risk level ("low", "medium", "high") and a list of reasons.
    High risk: missing key coupling dimensions (V, M, t, C) while
    relying on output volume.
    """
    reasons = []
    critical_missing = [k for k in ["V", "M", "t", "C"] if study.status.get(k) in ("omitted",)]
    if critical_missing:
        reasons.append(f"Missing critical coupling dimensions: {', '.join(critical_missing)}")
    if study.status.get("E") == "omitted":
        reasons.append("Environmental conditions not measured — substrate ignored.")
    if study.status.get("tok") == "over-relied":
        reasons.append("Over‑reliance on output tokens as productivity proxy.")
    if study.status.get("O") == "omitted":
        reasons.append("Organisational factors omitted.")
    # Count
    score = completeness_score(study)
    if len(reasons) >= 3 or score < 0.4:
        risk = "high"
    elif len(reasons) >= 1 or score < 0.7:
        risk = "medium"
    else:
        risk = "low"
    return risk, reasons

def audit_report(study: ProductivityStudy) -> str:
    """Generate a human‑readable audit report."""
    lines = []
    lines.append(f"Scope Completeness Audit: {study.name}")
    if study.source:
        lines.append(f"Source: {study.source}")
    lines.append("-" * 50)

    # Status per dimension
    lines.append("Dimension status:")
    for key in DIMENSIONS:
        info = DIMENSIONS[key]
        stat = study.status.get(key, "omitted")
        lines.append(f"  {key:4s} ({info['label']:40s}) : {stat}")

    # Score
    score = completeness_score(study)
    risk, reasons = collapse_risk(study)
    lines.append(f"\nCompleteness score: {score:.2f} (0‑1, higher = more coupling‑aware)")
    lines.append(f"Collapse risk: {risk}")

    if reasons:
        lines.append("Risk factors:")
        for r in reasons:
            lines.append(f"  • {r}")

    # Missing dimensions call‑out
    missing_critical = [key for key in DIMENSIONS if study.status[key] == "omitted"
                        and DIMENSIONS[key]["category"] in ("coupling", "substrate")]
    if missing_critical:
        lines.append("\nDark matter of productivity (unmeasured coupling/substrate):")
        for key in missing_critical:
            lines.append(f"  {key} — {DIMENSIONS[key]['label']}")

    # Recommendation based on thesis
    if risk == "high":
        lines.append("\n⚠️  This study is prone to field_collapse: it treats the AI or human as the unit")
        lines.append("    rather than the coupling. Productivity gains may be brittle and mask")
        lines.append("    accumulating maintenance debt or verification burden.")
        lines.append("    Recommendation: Do not generalise without measuring V, M, E, and t.")
    elif risk == "medium":
        lines.append("\n⚠️  Partially specified — some coupling dimensions are missing.")
        lines.append("    Interpret findings cautiously; look for follow‑up studies that fill the gaps.")
    else:
        lines.append("\n✓  Study appears coupling‑aware. The measured dimensions support")
        lines.append("    a relational interpretation. Continue monitoring time‑horizon effects.")

    return "\n".join(lines)

def compare_studies(study1, study2):
    """Side‑by‑side comparison of completeness."""
    print(f"Comparing: {study1.name} vs {study2.name}")
    header = f"{'Dimension':<6} {'Weight':<8} {study1.name[:20]:<20} {study2.name[:20]:<20}"
    print(header)
    print("-" * len(header))
    for key in DIMENSIONS:
        w = DIMENSIONS[key]["weight"]
        s1 = study1.status.get(key, "omitted")
        s2 = study2.status.get(key, "omitted")
        print(f"{key:<6} {w:<8.2f} {s1:<20} {s2:<20}")
    print(f"\nCompleteness: {study1.name}: {completeness_score(study1):.2f}, "
          f"{study2.name}: {completeness_score(study2):.2f}")

# ── DEMO / INTERACTIVE ──────────────────────────────────────
def demo_codex_audit():
    """Audit the June 2026 Codex agentic AI study based on public summary."""
    study = ProductivityStudy(
        name="The Shift to Agentic AI: Evidence from Codex (June 2026)",
        source="preprint, as described in news summary",
        status={
            "A": "measured",     # AI capability (Codex)
            "T": "measured",     # task type (coding tasks)
            "tok": "over-relied", # output tokens used as primary activity measure
            "H": "estimated",    # human users' background, but likely not deep
            "t": "omitted",      # no long‑term follow‑up (maintenance debt, etc.)
            "V": "omitted",      # verification cost not reported
            "M": "omitted",      # maintenance debt not tracked
            "C": "omitted",      # coordination costs (managing multiple agents)
            "E": "omitted",      # physical environment, interruptions
            "O": "omitted",      # organisational context
            "I": "omitted",      # integration effort
            "S": "omitted",      # specification cost
            "Op":"omitted",      # opportunity cost
        }
    )
    print(audit_report(study))

    # Compare with a hypothetical coupling‑aware study
    hypothetical = ProductivityStudy(
        name="Ideal Coupling‑Aware Replication",
        status={
            "H": "measured",
            "A": "measured",
            "T": "measured",
            "E": "measured",
            "O": "measured",
            "C": "estimated",
            "V": "measured",
            "t": "measured",
            "M": "measured",
            "I": "estimated",
            "S": "estimated",
            "Op":"estimated",
            "tok":"estimated",  # used only as auxiliary, not over‑relied
        }
    )
    print("\n" + "="*60)
    compare_studies(study, hypothetical)

def interactive():
    print("=== Scope Completeness Audit ===")
    print("Evaluate productivity studies against the full coupling surface.")
    print("Commands: audit <name> <dim=status ...>, demo, compare <name1> <name2>, quit")
    studies = {}
    while True:
        try:
            cmd = input("audit> ").strip().split()
            if not cmd:
                continue
            if cmd[0] == "quit":
                break
            elif cmd[0] == "demo":
                demo_codex_audit()
            elif cmd[0] == "audit":
                if len(cmd) < 2:
                    print("Usage: audit <study_name> [dim=status ...]")
                    print("  status: measured, estimated, omitted, over-relied")
                    continue
                name = cmd[1]
                status = {}
                for pair in cmd[2:]:
                    if '=' in pair:
                        dim, val = pair.split('=', 1)
                        if dim in DIMENSIONS:
                            status[dim] = val
                study = ProductivityStudy(name, status=status)
                studies[name] = study
                print(audit_report(study))
            elif cmd[0] == "compare":
                if len(cmd) != 3:
                    print("Usage: compare <name1> <name2>")
                    continue
                n1, n2 = cmd[1], cmd[2]
                if n1 not in studies or n2 not in studies:
                    print("Study not found. Audit them first.")
                    continue
                compare_studies(studies[n1], studies[n2])
            else:
                print("Unknown command.")
        except (EOFError, KeyboardInterrupt):
            print()
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_codex_audit()
    else:
        interactive()
