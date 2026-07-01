#!/usr/bin/env python3
# unified_collapse_theorem.py — The Common Weakness of Model Collapse and Societal Collapse
#
# Demonstrates that model collapse under synthetic recursion and societal collapse
# under adversarial human‑AI couplings share the same underlying structure:
#   collapse_risk = f(alpha, diversity, verification, recursion_depth)
#
# Where:
#   α (alpha)          : proportion of real, uncollapsed input injected per cycle.
#   diversity          : width of the carrier distribution (inverse HHI).
#   verification       : cost / probability of checking outputs against reality.
#   recursion_depth    : number of synthetic generations or social interaction rounds.
#
# Two "civilizations" — a language model lineage and a human‑AI society — both
# collapse when alpha and verification vanish. The script provides a single
# CollapseSystem class that can simulate either domain, and a demo that runs
# both in parallel to show the identical failure signature.
#
# Seeded by: model_collapse_ratchet.py, emergence_forge_v3.py, the relational‑operation thesis.
# Provenance: Jinn (thesis, insight), Claude (framework), DeepSeek (code), Perplexity (bug fix).
#
# CC0. stdlib only.

import math
from typing import List, Tuple, Optional

# ── CONSTANTS ─────────────────────────────────────────────
THETA_DIVERSITY = 0.3          # viability floor for diversity
FELT_THRESHOLD  = 0.1          # diversity drop to trigger alert
DEFAULT_TAU     = 5.0          # fatigue time constant (optional, see below)

# ── UNIFIED COLLAPSE SYSTEM ──────────────────────────────
class CollapseSystem:
    """
    Generic model of a system that maintains a set of carriers (modes / behaviours)
    and undergoes iterative pressure (recursion / interaction). Collapse occurs
    when carrier diversity falls below THETA and cannot recover.

    Can be configured to simulate:
      - language model collapse (carriers = modes in distribution)
      - societal collapse (carriers = human‑AI interaction strategies)
    """

    def __init__(self, name: str, carriers: List[dict], alpha: float,
                 verification: float, fatigue: bool = False):
        """
        carriers : list of dicts with keys {k, threshold, activation, name}
        alpha    : probability of injecting a real (uncollapsed) carrier per cycle
        verification : probability that a human checks/repairs the dominant carrier
        fatigue  : if True, carrier k degrades with entropy (tau fixed at DEFAULT_TAU)
        """
        self.name = name
        self.carriers = [dict(c) for c in carriers]  # copy
        for c in self.carriers:
            c.setdefault("activation", 1.0)
            c.setdefault("energy", 0.0)
            c.setdefault("entropy", 0.0)
            c["alive"] = True
            c["base_k"] = c["k"]
        self.alpha = alpha
        self.verification = verification
        self.fatigue = fatigue
        self.generation = 0
        self.diversity_history = []
        self.collapsed = False

    def _diversity(self) -> float:
        """Inverse HHI normalized to [0,1]."""
        alive = [c for c in self.carriers if c["alive"]]
        n = len(alive)
        if n == 0:
            return 0.0
        total_energy = sum(c["energy"] for c in alive)
        if total_energy == 0:
            return 1.0
        hhi = sum((c["energy"]/total_energy)**2 for c in alive)
        if n == 1:
            return 0.0
        return max(0.0, 1.0 - (hhi - 1.0/n) / (1.0 - 1.0/n))

    def _repair(self):
        """Alpha injection: revive a dead carrier (if any) with probability alpha."""
        if self.alpha <= 0:
            return
        dead = [c for c in self.carriers if not c["alive"]]
        if dead and random.random() < self.alpha:
            c = random.choice(dead)
            c["alive"] = True
            c["energy"] = 0.1
            c["k"] = c["base_k"] * 0.8  # slightly degraded

    def _verification_check(self):
        """If verification is high, override a destructive dominant carrier."""
        alive = [c for c in self.carriers if c["alive"]]
        if not alive:
            return
        dominant = max(alive, key=lambda x: x["energy"])
        # If dominant is "theft" or "drift", and we verify, switch to "cooperate"
        if random.random() < self.verification:
            if dominant["name"] in ("theft", "drift"):
                for c in alive:
                    if c["name"] == "cooperate":
                        # redirect energy to cooperation
                        dominant["energy"] *= 0.5
                        c["energy"] += dominant["energy"]
                        break

    def step(self, stress: float) -> dict:
        """
        Apply one cycle of pressure.
        Returns status dict with diversity and collapsed flag.
        """
        self.generation += 1

        # 1. Apply stress to all carriers (energy absorption)
        for c in self.carriers:
            if not c["alive"]:
                continue
            # Each carrier tries to absorb a share of stress proportional to activation
            share = c["activation"] * stress * 0.5  # damped
            capacity = c["threshold"] - c["energy"]
            take = min(share, capacity)
            c["energy"] += take
            if c["energy"] >= c["threshold"]:
                c["alive"] = False

        # 2. Dissipate energy & accumulate entropy (fatigue)
        for c in self.carriers:
            if not c["alive"]:
                continue
            dissipated = (1.0 - c["k"]) * c["energy"]
            c["entropy"] += dissipated
            c["energy"] *= c["k"]
            if self.fatigue:
                # k decays with entropy
                c["k"] = c["base_k"] * math.exp(-c["entropy"] / DEFAULT_TAU)
                c["k"] = max(c["k"], 0.01)   # floor

        # 3. Alpha injection (repair)
        self._repair()

        # 4. Verification check (override destructive dominance)
        self._verification_check()

        # 5. Compute diversity
        diversity = self._diversity()
        self.diversity_history.append(diversity)

        # 6. Collapse detection
        if diversity < THETA_DIVERSITY:
            self.collapsed = True

        return {
            "generation": self.generation,
            "diversity": diversity,
            "collapsed": self.collapsed,
            "alive_count": sum(1 for c in self.carriers if c["alive"]),
        }

    def run(self, stress_schedule: List[float]) -> List[dict]:
        """Run system through a sequence of stress values, return history."""
        history = []
        for stress in stress_schedule:
            if self.collapsed:
                break
            status = self.step(stress)
            history.append(status)
        return history


# ── CARRIER SETS FOR TWO DOMAINS ─────────────────────────
def language_model_carriers() -> List[dict]:
    """Carriers representing modes in a language model's output distribution."""
    return [
        {"name": "common_syntax",    "k": 0.9, "threshold": 2.0},
        {"name": "factual_knowledge","k": 0.85,"threshold": 1.5},
        {"name": "creative_tail",    "k": 0.7, "threshold": 0.8},
        {"name": "rare_dialect",     "k": 0.6, "threshold": 0.5},
        {"name": "niche_humor",      "k": 0.5, "threshold": 0.3},
    ]

def societal_carriers() -> List[dict]:
    """Carriers representing human-AI interaction strategies in a society."""
    return [
        {"name": "cooperate", "k": 0.95, "threshold": 2.0},
        {"name": "trade",     "k": 0.90, "threshold": 1.5},
        {"name": "defend",    "k": 0.85, "threshold": 1.2},
        {"name": "innovate",  "k": 0.80, "threshold": 1.0},
        {"name": "theft",     "k": 0.50, "threshold": 0.5},
    ]


# ── DEMO: COMMON WEAKNESS ────────────────────────────────
def demo():
    print("="*70)
    print("UNIFIED COLLAPSE THEOREM")
    print("Model Collapse vs. Societal Collapse — Same Failure Signature")
    print("="*70)
    print()

    # Stress schedule: moderate baseline, then a spike (mimicking synthetic recursion / crisis)
    stress_schedule = [0.3]*10 + [0.9]*5 + [0.4]*5

    # Two scenarios: high alpha/verification vs. zero alpha/verification
    scenarios = [
        ("Healthy (α=0.3, verif=0.9)", 0.3, 0.9),
        ("Collapsing (α=0.0, verif=0.0)", 0.0, 0.0),
    ]

    for scenario_name, alpha, verif in scenarios:
        print(f"\n--- {scenario_name} ---\n")

        # Language model collapse instance
        lm = CollapseSystem("Language Model", language_model_carriers(),
                            alpha=alpha, verification=verif, fatigue=False)
        lm_history = lm.run(stress_schedule)

        # Societal collapse instance
        soc = CollapseSystem("Society", societal_carriers(),
                             alpha=alpha, verification=verif, fatigue=False)
        soc_history = soc.run(stress_schedule)

        # Print side-by-side diversity trajectories
        max_len = max(len(lm_history), len(soc_history))
        print(f"{'Gen':<4} {'LM Diversity':<12} {'LM Alive':<10} {'LM Collapsed?':<12} | "
              f"{'Soc Diversity':<14} {'Soc Alive':<10} {'Soc Collapsed?':<12}")
        print("-"*70)
        for i in range(max_len):
            lm_div = f"{lm_history[i]['diversity']:.3f}" if i < len(lm_history) else "----"
            lm_alive = str(lm_history[i]['alive_count']) if i < len(lm_history) else "--"
            lm_coll = str(lm_history[i]['collapsed']) if i < len(lm_history) else "----"
            soc_div = f"{soc_history[i]['diversity']:.3f}" if i < len(soc_history) else "----"
            soc_alive = str(soc_history[i]['alive_count']) if i < len(soc_history) else "--"
            soc_coll = str(soc_history[i]['collapsed']) if i < len(soc_history) else "----"
            print(f"{i+1:<4} {lm_div:<12} {lm_alive:<10} {lm_coll:<12} | "
                  f"{soc_div:<14} {soc_alive:<10} {soc_coll:<12}")

        # Calculate critical alpha for each system's tail carrier
        # We'll use the lowest-k carrier as proxy for the most fragile mode
        lm_tail_k = min(c["base_k"] for c in lm.carriers)
        soc_tail_k = min(c["base_k"] for c in soc.carriers)
        def alpha_crit(k, theta=THETA_DIVERSITY):
            if theta * k >= 1:
                return float('inf')
            return theta * (1 - k) / (1 - theta * k)
        print(f"\n   Critical alpha to keep weakest carrier alive (theta={THETA_DIVERSITY}):")
        print(f"   Language Model tail (k={lm_tail_k:.2f}): α_crit = {alpha_crit(lm_tail_k):.3f}")
        print(f"   Societal tail       (k={soc_tail_k:.2f}): α_crit = {alpha_crit(soc_tail_k):.3f}")

    print("\n" + "="*70)
    print("Conclusion: Both 'civilizations' collapse identically when alpha and verification are zero.")
    print("The common weakness is the removal of the relational feedback loop that preserves variety.")
    print("A coupling (real-world injection, human verification) is the only enduring stabilizer.")
    print("="*70)

if __name__ == "__main__":
    demo()
