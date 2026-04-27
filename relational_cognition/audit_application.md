# 🧭 Audit Application

**Glyphs:** 🧭 (substrate-preserving translation) • ⚖️ (balance) • ↻ (realign) • 🪞 (coating)

**Thesis:** Relational cognition is not an extra philosophy bolted onto the audit protocol. It is the layer at which the audit's existing metrics — `clarity_score`, `trust_score`, the cognition cycle, change-tracking — are *actually meaningful*. This document specifies how to use the relational frame inside an ordinary audit pass.

---

## When to engage the relational layer

Use it when **any** of the following hold:

- The event involves a claim about a *process* (cognition, intent, deception, alignment, drift).
- The framing of the event uses heavily nominalized English ("the deception," "the violation," "the trust," "the consent").
- A swarm or human reviewer reports unusually fast agreement on a contested question.
- A scroll-level concept (cycle, contrast, season) is being applied to a concrete decision.
- An audit capsule is being written about a non-Western or oral-knowledge context.

Skip it when the event is purely operational (a JSON file failed to validate, a timestamp is malformed, a path is wrong). Substrate matters when meaning is at stake; not every audit is about meaning.

---

## Procedure (lightweight)

1. **Restate verb-first.** Take the event description and rewrite it using at least two constraint primitives from `constraint_primitives.md`. If you cannot, the description is too noun-shaped to audit; expand it first.
2. **Run one coating probe** from `coating_detection.md`. Record which probe and the result.
3. **Identify the substrate at risk.** What relational property would be lost if the noun-first framing were the only frame on record? Name it.
4. **Score normally.** Apply existing `clarity_score` / `trust_score` thresholds from `swarm_config.json`. The relational pass changes *what is being scored*, not *how* the score is computed.
5. **Log the relational pass.** Include the verb-first restatement and the coating probe result in the capsule.

---

## Capsule extension (optional fields)

Audit capsules following `templates/AUDIT_CAPSULE_TEMPLATE.json` may include a `relational` block. Nothing in the existing schema breaks if it is omitted.

```json
{
  "relational": {
    "verb_first_restatement": "<event described using constraint primitives>",
    "primitives": [
      {"source": "<node>", "primitive": "<DRIVES|DAMPS|...>", "target": "<node>", "strength": 0.0}
    ],
    "coating_probe": {
      "name": "adversarial_restatement | constraint_inversion | primitive_grounding | hidden_variable | silence_test",
      "result": "passed | failed | inconclusive",
      "notes": "<optional>"
    },
    "substrate_at_risk": "<what would be lost under noun-first-only framing>"
  }
}
```

---

## Mapping to the cognition cycle

The seven-stage cycle in `scrolls/cognition_cycle.md` is already verb-first in shape. The relational layer makes its mechanics explicit:

| Stage | Verb-first reading |
|---|---|
| ❌ Dissonance | a coupling fails to phase-lock; signal does not match expectation. |
| 🔍 Curiosity | the failed lock `DRIVES` exploration of nearby states. |
| 📚 Collection | exploration `FEEDS` a working set of patterns. |
| ⚖️ Evaluation | patterns are tested against constraints; some `SATURATE`, some don't. |
| ➡️ Trajectory | surviving patterns `MODULATE` projected paths forward. |
| 🔄 Re-evaluation | trajectories are checked against new evidence; coatings are probed. |
| 🪶 Settling | the system `DAMPS` into temporary coherence — a rest, not an end. |

A cycle that skips dissonance, or settles before re-evaluation, is almost always coated.

---

## What this folder does *not* do

- It does not replace existing scrolls or protocols.
- It does not introduce a new score, threshold, or gating metric.
- It does not require any change to `agents/`, `schemas/`, or CI.
- It does not export the full Energy English grammar; only the minimum vocabulary the audit protocol needs.

If a future audit reveals that more of the upstream grammar is load-bearing for this protocol, that addition gets its own change event, per `protocols/change_tracking_v1.0.md`.
