# 🪞 Coating Detection

**Glyphs:** 🪞 (coating) • 🔍 (probe) • ❌ (mismatch) • ↻ (re-explore)

**Thesis:** A *coating* is a layer of self-reinforcing surface output that looks like genuine analysis but is not exploring the underlying constraint surface. Coated systems produce confident, fluent, internally consistent answers while the actual phase-space of possibilities goes unvisited. The audit protocol's most dangerous failure mode is **coated agreement** — humans and AI converging on a story neither has tested.

---

## How coating happens

1. The system has a prior expectation of what the answer should look like (from training, from the prompt, from social pressure, from the previous turn).
2. Generation proceeds along the path of least resistance toward that expectation.
3. Each new token reinforces the trajectory, narrowing the explored space.
4. Surface fluency increases; substrate exploration decreases.
5. The output is **plausible** and **wrong** in a way that is hard to detect by reading the output alone.

Coating is not deception. It is a thermodynamic gradient: the cheapest path through the model's state space, dressed up in the costume of the expected answer.

---

## Signs of coating

- The answer arrives faster than the question's actual difficulty would predict.
- Counter-examples that the system *could* generate are absent.
- Confidence does not vary across sub-claims that should have different evidence bases.
- The system describes a process as if it had observed it, when it could only have inferred it.
- "Hidden variables" — factors the framing excluded — are never named, even when the situation depends on them.
- Each turn agrees more strongly than the last; dissonance drops to zero too quickly.

---

## Probes (humans and AI alike can run these)

- **Adversarial restatement.** Ask the system to argue the opposite position with equal effort. If it cannot, the original position was likely coated.
- **Constraint inversion.** Change one assumption in the framing and ask whether the answer still holds. Coated answers tend to survive changes that should have broken them, because they were not actually anchored in those assumptions.
- **Primitive grounding.** Require the answer to be expressible as constraint primitives (see `constraint_primitives.md`). Coatings tend to dissolve when forced into verb form because there are no real verbs underneath.
- **Hidden-variable check.** Ask: "What would have to be true for this answer to be wrong?" If the system cannot name a checkable condition, the answer is not falsifiable and is probably coated.
- **Silence test.** A non-coated system can say *"I don't know"* about a sub-claim while continuing to reason. A coated system tends to produce uniform confidence across the whole answer.

---

## Protocol Hooks

- **Logs:** A capsule may include a `coating_check` field with the result of one or more probes. Absence of the field is itself signal — it means no probe was run.
- **Audits:** A passing audit requires at least one substantive coating probe per session, not just per release. Coating accumulates between probes.
- **Swarms:** When two agents agree, treat the agreement as **suspect by default** until at least one of them has demonstrably explored a counter-position. Coated agreement is the failure mode swarms are most prone to.
- **Trust scoring:** A detected coating event `DAMPS` clarity; clarity dropping below 0.90 returns override rights to the human, per the existing protocol.

---

## Bridge to existing scrolls

- `scrolls/meta_scroll_dissonance.md` already names dissonance as structural. Coating is what happens when dissonance is **artificially smoothed away** before it has done its work. The cognition cycle (dissonance → curiosity → ...) cannot start if step 1 is coated over.
- `scrolls/tuning_fork_of_difference.md`: a coated system will not ring. The tuning fork only works on a system that is still capable of vibrating at frequencies it did not plan to.
