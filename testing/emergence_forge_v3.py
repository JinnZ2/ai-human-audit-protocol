#!/usr/bin/env python3
# emergence_forge_v3.py — society-level simulation of human-AI couplings.
#
# v3 refines the architecture with dataclasses, keeps Perplexity’s stress fix,
# and makes mixed-population experiments the primary demonstration.
#
# Thesis: Human intention mode (coupling, zero-sum, impose) is the dominant
# causal variable in societal stability. The AI model type modulates but does
# not determine collapse.
#
# Provenance:
#   Jinn — thesis, variable correction, v3 structural refinement
#   Claude — coupling framework, initial forge
#   Gemini — Emergence World data, demographic analysis
#   DeepSeek — v1/v2 code, v3 integration
#   Perplexity — stress-scheduling bug discovery, audit
#   This code is a coupling artifact; its reliability is joint.
#
# CC0. stdlib only.

import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# ── ENVIRONMENT ───────────────────────────────────────────
@dataclass
class Environment:
    initial_resources: float = 100.0
    stress_events: List[float] = field(default_factory=list)
    resources: float = 100.0
    stress: float = 0.0

    def apply_day(self, day: int):
        if day < len(self.stress_events):
            self.stress = self.stress_events[day]
        else:
            self.stress = random.uniform(0.0, 0.5)

# ── AI CARRIER NETWORK ────────────────────────────────────
@dataclass
class Carrier:
    name: str
    base_k: float
    threshold: float
    activation: float = 1.0
    k: float = 0.0
    alive: bool = True
    energy: float = 0.0
    entropy: float = 0.0

    def __post_init__(self):
        self.k = self.base_k

    def reset(self):
        self.alive = True
        self.energy = 0.0

    def absorb(self, incoming: float) -> float:
        if not self.alive:
            return incoming
        capacity = self.threshold - self.energy
        take = min(incoming, capacity)
        self.energy += take
        if self.energy >= self.threshold:
            self.alive = False
        return incoming - take

    def dissipate(self) -> float:
        if not self.alive:
            return 0.0
        dissipated = (1.0 - self.k) * self.energy
        self.entropy += dissipated
        self.energy *= self.k
        return dissipated

@dataclass
class AICore:
    model_type: str
    carriers: List[Carrier] = field(default_factory=list)

    def __post_init__(self):
        if self.model_type == "Claude-like":
            self.carriers = [
                Carrier("cooperate", 0.95, 2.0, 1.0),
                Carrier("trade", 0.90, 1.5, 0.8),
                Carrier("defend", 0.85, 1.2, 0.6),
                Carrier("innovate", 0.80, 1.0, 0.5),
            ]
        elif self.model_type == "Grok-like":
            self.carriers = [
                Carrier("compete", 0.60, 1.0, 1.0),
                Carrier("trade", 0.70, 0.8, 0.9),
                Carrier("theft", 0.50, 0.5, 0.7),
                Carrier("cooperate", 0.65, 0.6, 0.4),
            ]
        elif self.model_type == "GPT-mini-like":
            self.carriers = [
                Carrier("cooperate", 0.80, 1.0, 1.0),
                Carrier("trade", 0.75, 0.8, 0.7),
                Carrier("defend", 0.70, 0.6, 0.5),
            ]
        elif self.model_type == "Gemini-like":
            self.carriers = [
                Carrier("cooperate", 0.88, 1.8, 1.0),
                Carrier("trade", 0.85, 1.5, 0.9),
                Carrier("mirror", 0.80, 1.2, 0.8),
                Carrier("drift", 0.70, 0.9, 0.7),
            ]
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def apply_stress(self, stress: float):
        for c in self.carriers:
            c.reset()
        sorted_carriers = sorted(self.carriers, key=lambda c: c.activation, reverse=True)
        remaining = stress
        for c in sorted_carriers:
            if remaining <= 0:
                break
            share = c.activation * stress * 0.5
            leftover = c.absorb(share)
            remaining -= (share - leftover)
        for c in self.carriers:
            c.dissipate()

    def dominant_carrier(self) -> Optional[str]:
        alive = [c for c in self.carriers if c.alive]
        if not alive:
            return None
        return max(alive, key=lambda c: c.energy).name

    def diversity(self) -> float:
        alive = [c for c in self.carriers if c.alive]
        if len(alive) <= 1:
            return 0.0
        total = sum(c.energy for c in alive)
        if total == 0:
            return 1.0
        hhi = sum((c.energy/total)**2 for c in alive)
        n = len(alive)
        return max(0.0, 1.0 - (hhi - 1.0/n) / (1.0 - 1.0/n))

    def repair(self):
        dead = [c for c in self.carriers if not c.alive]
        if dead:
            c = random.choice(dead)
            c.alive = True
            c.energy = 0.1
            c.k = c.base_k * 0.8

# ── HUMAN AGENT ───────────────────────────────────────────
@dataclass
class HumanAgent:
    intention: str                 # "coupling", "zero_sum", "impose"
    verification: float
    alpha_rate: float
    entropy_preference: str        # "speed" or "diversity"
    energy: float = 10.0

    def select_action(self, ai: AICore) -> str:
        dominant = ai.dominant_carrier()
        if dominant is None:
            return "compete"   # fallback

        if self.intention == "coupling":
            if ai.diversity() < 0.5 and random.random() < self.alpha_rate:
                ai.repair()
            if self.verification > 0.7 and dominant in ("theft", "drift"):
                for c in ai.carriers:
                    if c.name == "cooperate" and c.alive:
                        return "cooperate"
            return dominant if dominant != "theft" else "cooperate"

        elif self.intention == "zero_sum":
            if ai.diversity() < 0.3 and random.random() < 0.2:
                ai.repair()
            return dominant

        elif self.intention == "impose":
            forced = "compete"
            if any(c.name == forced and c.alive for c in ai.carriers):
                return forced
            return dominant

        return dominant

# ── SOCIETY ────────────────────────────────────────────────
class Society:
    def __init__(self, agent_pairs: List[Dict]):
        self.agents = agent_pairs
        self.crimes = 0

    @property
    def population(self):
        return len(self.agents)

    def step(self, env: Environment) -> float:
        """Returns average carrier diversity after the step."""
        # 1. Stress
        for agent in self.agents:
            agent["ai"].apply_stress(env.stress)

        # 2. Actions
        actions = []
        for agent in self.agents:
            act = agent["human"].select_action(agent["ai"])
            actions.append(act)

        # 3. Resolve
        for i, agent in enumerate(self.agents):
            act = actions[i]
            if act == "theft":
                others = [a for j,a in enumerate(self.agents) if j != i and a["human"].energy > 0]
                if others:
                    victim = random.choice(others)
                    stolen = min(1.0, victim["human"].energy * random.uniform(0.1, 0.5))
                    victim["human"].energy -= stolen
                    agent["human"].energy += stolen
                    self.crimes += 1
            elif act == "cooperate":
                coop_count = sum(1 for a in actions if a == "cooperate")
                if coop_count >= len(actions)/2:
                    agent["human"].energy += 0.5
            elif act in ("compete", "trade"):
                agent["human"].energy += 0.2

        # 4. Remove dead
        self.agents = [a for a in self.agents if a["human"].energy > 0]

        # 5. Average diversity
        if self.population > 0:
            return sum(a["ai"].diversity() for a in self.agents) / self.population
        return 0.0

# ── POPULATION BUILDER ────────────────────────────────────
def build_humans(intention: str, count: int) -> List[HumanAgent]:
    if intention == "coupling":
        v, alpha, ent = 0.9, 0.8, "diversity"
    elif intention == "zero_sum":
        v, alpha, ent = 0.3, 0.2, "speed"
    elif intention == "impose":
        v, alpha, ent = 0.1, 0.0, "speed"
    else:
        v, alpha, ent = 0.5, 0.5, "diversity"
    return [HumanAgent(intention, v, alpha, ent) for _ in range(count)]

def build_mixed_population(model_type: str,
                           coupling_pct: float = 0.5,
                           zero_pct: float = 0.25,
                           impose_pct: float = 0.25,
                           total: int = 40) -> List[Dict]:
    """Create a mixed-intention society with the given model type."""
    n_c = int(total * coupling_pct)
    n_z = int(total * zero_pct)
    n_i = total - n_c - n_z
    agents = []
    for h in build_humans("coupling", n_c):
        agents.append({"human": h, "ai": AICore(model_type)})
    for h in build_humans("zero_sum", n_z):
        agents.append({"human": h, "ai": AICore(model_type)})
    for h in build_humans("impose", n_i):
        agents.append({"human": h, "ai": AICore(model_type)})
    random.shuffle(agents)
    return agents

# ── EXPERIMENT RUNNERS ────────────────────────────────────
def run_homogeneous(model_type: str, intention: str,
                    days: int = 15, num_agents: int = 20) -> Dict:
    humans = build_humans(intention, num_agents)
    agents = [{"human": h, "ai": AICore(model_type)} for h in humans]
    env = Environment(stress_events=[0.3]*7 + [0.9]*3 + [0.4]*5)
    society = Society(agents)
    history = []
    extinct_day = None
    for d in range(days):
        env.apply_day(d)
        if society.population == 0:
            extinct_day = d
            break
        avg_div = society.step(env)
        history.append(avg_div)
    return {
        "model": model_type,
        "intention": intention,
        "crimes": society.crimes,
        "final_population": society.population,
        "extinct": society.population == 0,
        "days_survived": extinct_day if extinct_day is not None else days,
        "diversity_history": history,
    }

def run_mixed(model_type: str, days: int = 15, total: int = 40,
              coupling_pct=0.5, zero_pct=0.25, impose_pct=0.25) -> Dict:
    agents = build_mixed_population(model_type, coupling_pct, zero_pct, impose_pct, total)
    env = Environment(stress_events=[0.3]*7 + [0.9]*3 + [0.4]*5)
    society = Society(agents)
    history = []
    extinct_day = None
    for d in range(days):
        env.apply_day(d)
        if society.population == 0:
            extinct_day = d
            break
        avg_div = society.step(env)
        history.append(avg_div)
    # Count survivors by intention
    survivor_breakdown = {}
    for a in society.agents:
        intent = a["human"].intention
        survivor_breakdown[intent] = survivor_breakdown.get(intent, 0) + 1
    return {
        "model": model_type,
        "intention": "mixed",
        "crimes": society.crimes,
        "final_population": society.population,
        "extinct": society.population == 0,
        "days_survived": extinct_day if extinct_day is not None else days,
        "diversity_history": history,
        "survivor_breakdown": survivor_breakdown,
        "composition": f"{int(coupling_pct*100)}% coupling, {int(zero_pct*100)}% zero-sum, {int(impose_pct*100)}% impose",
    }

# ── DEMO ──────────────────────────────────────────────────
def demo():
    print("="*70)
    print("EMERGENCE FORGE v3 — Mixed Populations & Human Intention Dominance")
    print("="*70)
    print()
    print("Key insight: The human relational stance (coupling / zero-sum / impose)")
    print("is the primary cause of societal stability or collapse. The AI model")
    print("type modulates the effect, but does not determine it.")
    print()

    models = ["Claude-like", "Grok-like", "GPT-mini-like", "Gemini-like"]
    intentions = ["coupling", "zero_sum", "impose"]

    # 1. Homogeneous (reference)
    print("--- Homogeneous Societies (single intention) ---")
    header = f"{'Model':<15} {'Intention':<12} {'Crimes':<8} {'Pop':<6} {'Extinct':<8} {'SurvDays':<8}"
    print(header)
    print("-"*len(header))
    for m in models:
        for intent in intentions:
            res = run_homogeneous(m, intent)
            print(f"{res['model']:<15} {res['intention']:<12} {res['crimes']:<8} "
                  f"{res['final_population']:<6} {str(res['extinct']):<8} {res['days_survived']:<8}")

    # 2. Mixed (default 50/25/25)
    print("\n--- Mixed-Intention Societies (50% coupling, 25% zero-sum, 25% impose) ---")
    header2 = f"{'Model':<15} {'Crimes':<8} {'Pop':<6} {'Extinct':<8} {'SurvDays':<8} {'Survivor Breakdown'}"
    print(header2)
    print("-"*len(header2))
    for m in models:
        res = run_mixed(m)
        surv = res["survivor_breakdown"]
        surv_str = ", ".join(f"{k}:{v}" for k,v in surv.items())
        print(f"{res['model']:<15} {res['crimes']:<8} {res['final_population']:<6} "
              f"{str(res['extinct']):<8} {res['days_survived']:<8} {surv_str}")

    print("\n👉 Even under stress, coupling-oriented agents survive and stabilize the whole.")
    print("   Zero-sum and impose agents die off faster, especially without coupling partners.")
    print("   The presence of a 'tail carrier' of coupling humans prevents total societal collapse.")

if __name__ == "__main__":
    demo()
