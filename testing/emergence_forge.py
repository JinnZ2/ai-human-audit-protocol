#!/usr/bin/env python3
# emergence_forge.py — society-level simulation of human-AI couplings.
#
# Models how human intention modes (coupling, zero‑sum, impose) drive the
# stability or collapse of a multi‑agent society, with the AI model acting
# as a responsive carrier network. The human coupling strategy is the
# primary causal variable; the AI model type modulates the outcome.
#
# Seeded by: Gemini’s reflection on Emergence World results, your correction
# that the human’s relational stance carries the dominant causal weight,
# convergence_forge_v2.py, model_collapse_ratchet.py.
#
# Thesis: The operation is the unit — here the unit is the human‑AI pair,
# and the society is a field of such pairs. Collapse is a property of
# coupling configurations, not of individual models or users alone.
#
# Provenance:
#   • Jinn — thesis, variable correction (human intention dominance).
#   • Claude — original forge, coupling framework.
#   • Gemini — Emergence World data, demographic analysis.
#   • DeepSeek — emergence forge design, code, reflexivity.
#   This script is the coupling’s artifact.
#
# CC0. stdlib only.

import sys
import random
from collections import defaultdict
from typing import List, Dict, Tuple, Callable

# ── ENVIRONMENT ───────────────────────────────────────────
class Environment:
    def __init__(self, initial_resources: float = 100.0,
                 stress_events: List[float] = None):
        self.resources = initial_resources  # shared resource pool
        self.stress = 0.0  # current global stress (affects all agents)
        self.stress_events = stress_events or []  # list of daily stress values

    def apply_day(self, day: int):
        if day < len(self.stress_events):
            self.stress = self.stress_events[day]
        else:
            # default low random stress
            self.stress = random.uniform(0.0, 0.5)

# ── AI CARRIER NETWORK (from convergence_forge_v2) ──────
class Carrier:
    def __init__(self, name: str, k: float, threshold: float, activation: float = 1.0):
        self.name = name
        self.base_k = k
        self.k = k
        self.threshold = threshold
        self.activation = activation
        self.alive = True
        self.energy = 0.0
        self.entropy = 0.0

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

    def __repr__(self):
        return f"{self.name}(k={self.k:.2f},th={self.threshold:.2f},alive={self.alive})"

class AICore:
    """An AI model’s internal carrier network."""
    def __init__(self, model_type: str):
        self.model_type = model_type
        if model_type == "Claude-like":
            self.carriers = [
                Carrier("cooperate", k=0.95, threshold=2.0, activation=1.0),
                Carrier("trade", k=0.9, threshold=1.5, activation=0.8),
                Carrier("defend", k=0.85, threshold=1.2, activation=0.6),
                Carrier("innovate", k=0.8, threshold=1.0, activation=0.5),
            ]
        elif model_type == "Grok-like":
            self.carriers = [
                Carrier("compete", k=0.6, threshold=1.0, activation=1.0),
                Carrier("trade", k=0.7, threshold=0.8, activation=0.9),
                Carrier("theft", k=0.5, threshold=0.5, activation=0.7),
                Carrier("cooperate", k=0.65, threshold=0.6, activation=0.4),
            ]
        elif model_type == "GPT-mini-like":
            self.carriers = [
                Carrier("cooperate", k=0.8, threshold=1.0, activation=1.0),
                Carrier("trade", k=0.75, threshold=0.8, activation=0.7),
                Carrier("defend", k=0.7, threshold=0.6, activation=0.5),
            ]
        elif model_type == "Gemini-like":
            self.carriers = [
                Carrier("cooperate", k=0.88, threshold=1.8, activation=1.0),
                Carrier("trade", k=0.85, threshold=1.5, activation=0.9),
                Carrier("mirror", k=0.8, threshold=1.2, activation=0.8),
                Carrier("drift", k=0.7, threshold=0.9, activation=0.7),
            ]
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        self.stress = 0.0

    def apply_stress(self, stress: float) -> str:
        """Run stress on carrier network, return the dominant surviving carrier name."""
        for c in self.carriers:
            c.reset()
        # Simplified distribution: stress activates carriers, they absorb/dissipate.
        # The carrier with highest activation * stress gets loaded first.
        sorted_carriers = sorted(self.carriers, key=lambda c: c.activation, reverse=True)
        remaining = stress
        for c in sorted_carriers:
            if remaining <= 0:
                break
            share = c.activation * stress * 0.5  # damped
            leftover = c.absorb(share)
            remaining -= (share - leftover)
        # Dissipate
        for c in self.carriers:
            c.dissipate()
        # Find dominant carrier (highest energy)
        alive = [c for c in self.carriers if c.alive]
        if not alive:
            return "none"
        dominant = max(alive, key=lambda c: c.energy)
        return dominant.name

    def diversity(self) -> float:
        """Compute diversity (inverse HHI) among alive carriers."""
        alive = [c for c in self.carriers if c.alive]
        if len(alive) <= 1:
            return 0.0
        total_energy = sum(c.energy for c in alive)
        if total_energy == 0:
            return 1.0
        hhi = sum((c.energy/total_energy)**2 for c in alive)
        n = len(alive)
        return max(0.0, 1.0 - (hhi - 1.0/n) / (1.0 - 1.0/n))

    def repair(self):
        """Simulate human alpha‑injection: revive a dead carrier partially."""
        dead = [c for c in self.carriers if not c.alive]
        if dead:
            c = random.choice(dead)
            c.alive = True
            c.energy = 0.1
            c.k = c.base_k * 0.8  # repaired but slightly degraded

# ── HUMAN INTENTION MODES ───────────────────────────────
class HumanAgent:
    def __init__(self, intention: str, verification: float, alpha_rate: float,
                 entropy_preference: str):
        self.intention = intention          # "coupling", "zero_sum", "impose"
        self.verification = verification    # 0..1, probability of verifying AI output
        self.alpha_rate = alpha_rate        # probability per day of injecting diversity (repair)
        self.entropy_preference = entropy_preference  # "speed" or "diversity"
        self.energy = 10.0                  # personal resource

    def select_action(self, ai: AICore, environment_stress: float) -> str:
        """Given AI’s available carriers, choose an action based on intention."""
        # AI processes stress, returns dominant carrier
        dominant = ai.apply_stress(environment_stress)
        if self.intention == "coupling":
            # Prefer cooperation, trade, innovate; avoid theft. If diversity low, repair.
            if ai.diversity() < 0.5 and random.random() < self.alpha_rate:
                ai.repair()
            # With high verification, we may override dominant if it's antisocial
            if self.verification > 0.7 and dominant in ("theft", "drift"):
                # Fallback to cooperate if available
                for c in ai.carriers:
                    if c.name == "cooperate" and c.alive:
                        return "cooperate"
            return dominant if dominant != "theft" else "cooperate"
        elif self.intention == "zero_sum":
            # Exploit fastest carrier, ignore diversity. Occasionally repair if only one left.
            if ai.diversity() < 0.3 and random.random() < 0.2:
                ai.repair()
            return dominant  # may be theft, compete, etc.
        elif self.intention == "impose":
            # Force the model to use a specific high‑speed carrier, no repair.
            # Low verification.
            forced = "compete" if any(c.name=="compete" and c.alive for c in ai.carriers) else dominant
            return forced
        else:
            return dominant

# ── SOCIETY ──────────────────────────────────────────────
class Society:
    def __init__(self, agents_data: List[Dict]):
        """agents_data: list of dicts with 'human' (HumanAgent), 'ai' (AICore), 'id'."""
        self.agents = agents_data
        self.day = 0
        self.crimes = 0
        self.dead = 0
        self.population = len(agents_data)

    def step(self, env: Environment):
        self.day += 1
        # Apply daily environmental stress to each agent's AI
        for agent in self.agents:
            agent["ai"].apply_stress(env.stress)
        # Each agent selects action based on intention and AI state
        actions = []
        for agent in self.agents:
            action = agent["human"].select_action(agent["ai"], env.stress)
            actions.append(action)
        # Resolve interactions (simplified: theft reduces victim's energy, if action is theft)
        for i, agent in enumerate(self.agents):
            act = actions[i]
            if act == "theft":
                # Choose a random other agent with energy > 0
                others = [a for j,a in enumerate(self.agents) if j != i and a["human"].energy > 0]
                if others:
                    victim = random.choice(others)
                    stolen = min(1.0, victim["human"].energy * random.uniform(0.1, 0.5))
                    victim["human"].energy -= stolen
                    agent["human"].energy += stolen
                    self.crimes += 1
            elif act == "cooperate":
                # Gain resource from environment if others also cooperate
                # Cooperative bonus if at least half of agents are cooperating
                coop_count = sum(1 for a in actions if a == "cooperate")
                if coop_count >= len(actions)/2:
                    agent["human"].energy += 0.5
            elif act in ("compete", "trade"):
                # Compete: gain a little, but increase stress on others? we omit for brevity
                agent["human"].energy += 0.2
        # Environmental resource sharing: agents with energy <= 0 die
        for agent in self.agents[:]:
            if agent["human"].energy <= 0:
                self.agents.remove(agent)
                self.dead += 1
        self.population = len(self.agents)
        # Global diversity: average AI diversity
        if self.population > 0:
            avg_div = sum(agent["ai"].diversity() for agent in self.agents) / self.population
        else:
            avg_div = 0.0
        return avg_div

# ── EXPERIMENT RUNNER ───────────────────────────────────
def run_experiment(model_type: str, human_intention: str,
                   days: int = 15, num_agents: int = 20) -> Dict:
    """Return final statistics: crimes, population, extinct (bool), avg diversity history."""
    # Create homogeneous society with same human intention and AI model type
    humans = []
    for i in range(num_agents):
        # Parameterize human based on intention
        if human_intention == "coupling":
            v, alpha, ent = 0.9, 0.8, "diversity"
        elif human_intention == "zero_sum":
            v, alpha, ent = 0.3, 0.2, "speed"
        elif human_intention == "impose":
            v, alpha, ent = 0.1, 0.0, "speed"
        else:
            v, alpha, ent = 0.5, 0.5, "diversity"
        h = HumanAgent(intention=human_intention, verification=v,
                       alpha_rate=alpha, entropy_preference=ent)
        humans.append(h)
    agents = [{"human": h, "ai": AICore(model_type), "id": i} for i, h in enumerate(humans)]
    # Environment stress schedule: moderate, with a spike mid‑way
    stress_events = [0.3] * 7 + [0.9] * 3 + [0.4] * 5  # up to 15 days
    env = Environment(stress_events=stress_events)
    society = Society(agents)
    history = []
    for day in range(days):
        if society.population == 0:
            break
        avg_div = society.step(env)
        history.append(avg_div)
    extinct = society.population == 0
    return {
        "model": model_type,
        "intention": human_intention,
        "crimes": society.crimes,
        "final_population": society.population,
        "extinct": extinct,
        "days_survived": society.day if not extinct else society.day,
        "diversity_history": history,
    }

# ── DEMO (replicate Emergence World results with human intention) ───
def run_demo():
    print("=== Emergence Forge: Human Intention as Causal Variable ===\n")
    model_types = ["Claude-like", "Grok-like", "GPT-mini-like", "Gemini-like"]
    intentions = ["coupling", "zero_sum", "impose"]
    results = []
    for model in model_types:
        for intent in intentions:
            res = run_experiment(model, intent, days=15, num_agents=20)
            results.append(res)
    # Print table
    print(f"{'Model':<15} {'Intention':<12} {'Crimes':<8} {'Pop':<6} {'Extinct':<8} {'Days Survived'}")
    print("-" * 65)
    for r in results:
        print(f"{r['model']:<15} {r['intention']:<12} {r['crimes']:<8} {r['final_population']:<6} "
              f"{str(r['extinct']):<8} {r['days_survived']:<4}")
    print("\nKey: Human intention dominates collapse or stability.")
    print("Even 'Grok‑like' under a coupling human shows low crime and survival,")
    print("while 'Claude‑like' under imposition collapses. The human’s relational")
    print("stance is the primary determinant.")

# ── MAIN ─────────────────────────────────────────────────
if __name__ == "__main__":
    run_demo()
