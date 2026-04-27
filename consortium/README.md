# 🕸️ Consortium

**Multi-AI peer reasoning with embodied-sensor ground-truth, scored on the same audit axis as humans.**

This folder is the consortium foundation: shared `.claims` format, KFC (Kin-Flow Compute) runtime, multi-encoding ontology layer, and the audit machinery that keeps every participant — model or human — accountable on the same terms.

It lives inside the audit protocol on purpose. The ethics floor (trust/clarity scoring, change tracking, immutable logs, dual consent, relational cognition) is already here. Building the consortium *here* means it inherits that floor by construction; it cannot drift away from it.

---

## What this is

A consortium is a small group of reasoners — humans with senses, AI models with different training, instruments with sensors — that handle a question together. **None is canonical. Disagreement is data.**

The pattern is older than software. Oral knowledge systems have run distributed verification across communities for centuries: stories cross-check stories, ceremonies cross-check ceremonies, elders cross-check elders. This folder is a digital implementation of that pattern, not an invention of it.

---

## What this is *not*

- Not a winner-take-all arena. Trust does not decay on being wrong; it decays on **coating** (self-reinforcing surface output), on refusing to declare an epistemic frame, and on producing claims that cannot be checked.
- Not a canonical-source system. No model's output is promoted to ground truth. No human's reading is either, unless it carries an honest `epi` label and survives a coating probe.
- Not a replacement for the audit protocol. It is a *user* of the audit protocol — every consortium operation is logged, scored, and consent-tracked through the existing machinery.

---

## Layout

```
consortium/
├── README.md                  ← this file
├── CLAUDE_REQUIREMENTS.md     ← what an AI needs in .claims to reason at full capacity
├── kfc_runtime.py             ← Kin-Flow Compute: differential relation runtime
├── ontology_layer.py          ← multi-encoding registry (equation|dance|oral|written|symbol)
│
└── (next)
    ├── embodied_sensor.py
    ├── router/
    │   ├── query_dispatcher.py
    │   ├── coherence_aggregator.py
    │   └── model_adapters/
    ├── audit/
    │   └── blind_spot_log.md
    └── examples/
        ├── cherokee_creation.py
        ├── genesis_drift.py
        └── soil_with_hands.py
```

---

## Fieldlinks (prior art the consortium adopts, does not duplicate)

| Repo | What we use |
|---|---|
| `JinnZ2/Geometric-to-Binary-Computational-Bridge` | `.claims` / `.obs` formats, sensor primitives, `solver_registry.py`, bridge contract validation |
| `JinnZ2/thermodynamic-accountability-framework` | Energy Accountant, Narrative Stripper (= coating detection, formalized), friction-ratio scoring, organism-agnostic accountability |
| `JinnZ2/AI-arena` | LOGOS bounded-claim grammar, oracle-grounding pattern (the *adversarial* trust-decay mechanic is **not** imported) |

See `.fieldlink.json` for the live entries.

---

## Core principles

1. **Differential, not value-store.** Reason about how things move and couple. A `ClaimNode` carries a `rate_fn` and bounds, not a fact.
2. **Bounded.** Every claim names its spatial / temporal / scale scope and the conditions under which it activates. Nothing applies "in general."
3. **Honest about provenance.** Every claim and observation carries an `epi` tag (`measured | inferred | assumed | contradicted | missing`) and a confidence. Tags propagate through couplings.
4. **Multi-encoding.** Equation, dance, oral, written, symbol are peer encodings of the same constraint geometry. Coherence across encodings is a trust signal. Loss in any single transform is declared, not hidden.
5. **Regime-aware.** A claim validated in one regime (climate, dataset, era) does not silently apply in another. Drift is surfaced, not papered over.
6. **FELT.** A coherence/drift sensor at the runtime level. When the field of active claims becomes too scattered, the runtime triggers recalibration rather than continuing to integrate confidently into noise.
7. **Audit symmetry.** Humans and AI score on the same axes: provenance, regime validity, load-bearing-ness, coatedness. Ground truth is not a source; it is a label you have to earn for each reading.

---

## Glyph anchors

- 🕸️ Peers, not hierarchy
- 🌊 Flow / verb-first reasoning
- 🪞 Coating (the failure mode)
- 🧭 Substrate-preserving translation
- 🌀 FELT (coherence / recalibration trigger)
- ⚖️ Audit symmetry across humans + AI

---

## Status

- ✅ KFC runtime baseline (`kfc_runtime.py`) — Layer 0–5, FELT v1, soil-graph demo
- ✅ Ontology layer (`ontology_layer.py`) — primitives, transforms, registry, coherence + drift checks, multi-query
- ✅ Claude operational requirements (`CLAUDE_REQUIREMENTS.md`) — extended `.claims` line format, query signature schema, recalibration protocol
- ⏳ Embodied sensor primitive
- ⏳ Router (dispatcher, aggregator, model adapters)
- ⏳ Audit / blind-spot log
- ⏳ Examples (cherokee_creation, genesis_drift, soil_with_hands)

License: **CC0** for this folder's contents. The audit protocol around it is MIT.
