# 🌳 Knowledge Archaeology

*Constraint provenance for knowledge.*

Every piece of knowledge emerged under specific conditions: a geographic substrate, a forcing function, a community continuity, a transmission mode. When the knowledge moves — into a person, a model, a tool, a repository — the provenance usually doesn't move with it. The capability persists; the conditions of its validity become invisible.

This folder makes constraint provenance a **first-class attribute**. A node carries its regime alongside its content. A tree of nodes preserves both ancestry (where it descends from) and parallel lineages (independent discoveries in other communities). Anything reading the knowledge can run a `deploy_check` against the current environment; mismatch surfaces as an explicit flag, not silent failure.

---

## What lives here

```
knowledge_archaeology/
├── README.md                          (this file)
├── knowledge_archaeology.py           (the module — Regime, KnowledgeNode,
                                        KnowledgeTree, JSON loaders)
├── examples/
│   └── example_deploy_check.py        (three worked demos)
└── nodes/
    ├── anishinaabe_gravity_filtration_v1.json
    ├── punjab_baoli_filtration_v1.json
    └── commercial_filter_cartridge_v3.json
```

---

## The three core artifacts

### `Regime`

The constraint environment knowledge was forged under: geography, climate zone, elevation, magnetic latitude, temperature, precipitation, resource scarcity, population density, technology level, institutional context, community continuity, parallel communities. Every field is optional; supply what's known, leave the rest empty.

### `KnowledgeNode`

A piece of knowledge with full provenance:
- **Provenance**: regime, transmission mode, validation depth, generational depth
- **Lineage**: parent_ids (descended from), sibling_ids (parallel discoveries), derived_ids (descendants — populated automatically by the tree)
- **Attribution**: origin communities, individual carriers, **carrier_consent** (the field extraction usually erases)
- **Validity scope**: valid_under, fails_under, assumptions, extraction_risks

### `KnowledgeTree`

A directed graph of nodes. Operations:
- `add(node)` — adds a node and reconciles bidirectional links (siblings, parent↔derived)
- `ancestors(node_id)` — all knowledge this descends from
- `parallel_lineages(node_id)` — sibling discoveries grouped by community
- `attribution_trail(node_id)` — every community and carrier whose knowledge contributed
- `deploy_check(node_id, target_regime)` — applicability + attribution + parallel lineages

---

## The three failure modes this catches

### 1. Regime mismatch

A piece of knowledge validated in one regime gets silently re-applied in another. `regime_distance(source, target)` quantifies the displacement. `applicability()` returns a verdict: `applicable` / `review_required` / `regime_mismatch`. Hard checks against `fails_under` strings can override the distance score.

> Example: applying a boreal-validated water-filter design into Punjab plain regime triggers `review_required` (or worse), and surfaces parallel lineages — Punjab baoli filtration — that were already validated locally.

### 2. Extraction audit

`attribution_trail(node_id)` walks the ancestor graph and returns every community + carrier whose knowledge contributed, with `carrier_consent` for each step. A commercial product whose ancestors include traditional lineages without explicit consent surfaces in the trail.

> Example: a commercial filter cartridge with `parent_ids = [anishinaabe_..., punjab_baoli_...]` and `carrier_consent = "contested"` produces a trail that names the communities the knowledge came from and the consent state at each ancestor.

### 3. Validation-depth gate

A node with `validation = SINGLE_CYCLE` carries a `WARN: knowledge has shallow validation history` flag in `applicability()` regardless of regime distance. Even a perfect regime match doesn't grant credibility to knowledge that hasn't been tested across cycles.

---

## How this connects to the rest of the protocol

| Layer | Connection |
|---|---|
| `physics/MORALITY_ARCHAEOLOGY.md` | Frames the same insight in prose: the framework is excavation, not invention; knowledge has provenance and that provenance shapes its validity. This folder is the operational form. |
| `consortium/ontology_layer.py` | `Ontology.regime` and `reapply_check` are a smaller version of the same idea (drift detection across regimes). Knowledge_archaeology's `Regime` is richer (full geographic + social + temporal context); a future version of `Ontology` could compose it. |
| `physics/seven_generation_tracer.py` | Uses generational time. `KnowledgeNode.generational_depth` and `validation: DEEP_GENERATIONAL` operate on the same scale. |
| `consortium/embodied_sensor.py` | The `epi` sub-tag system (kinesthetic, phenological, etc.) parallels `TransmissionMode`. Both insist on declaring how a piece of information arrived at the system. |

---

## Cultural sourcing

The example node files (`nodes/anishinaabe_gravity_filtration_v1.json`, `nodes/punjab_baoli_filtration_v1.json`) reference real traditional knowledge systems. They are intentionally **structural and respectful**, not full ethnographic accounts:

- Communities are named at the level of identification, not deep description
- Carriers are referenced anonymously by default (`community_holders_unnamed_by_default`)
- `carrier_consent: "implicit"` reflects that the *general existence* of these traditions is widely acknowledged and can be referenced; specific implementation detail belongs to authorized cultural holders
- The example nodes demonstrate the *machinery* of provenance tracking, not the actual depth of the traditional practices

A real consortium application of this module to specific traditional knowledge would source detail from authorized cultural holders, populate the placeholders carefully, and document the consent process in the node itself.

The `commercial_filter_cartridge_v3.json` example deliberately carries `carrier_consent: "contested"` to show what the audit catches when traditional lineages are absorbed into commercial products without acknowledgment.

---

## Run the demo

```bash
python -m knowledge_archaeology.examples.example_deploy_check
```

Output shows:
1. Boreal filter applied to Punjab regime → applicability flags + Punjab parallel lineage surfaces
2. Commercial cartridge attribution trail → walks back to traditional lineages
3. Commercial cartridge applied to post-grid sparse region → regime mismatch flagged

---

## Lineage of this module

This module was authored by JinnZ2 and ships verbatim. The `commercial_filter_cartridge` example with contested consent is the load-bearing demonstration: the framework treats extraction of traditional knowledge as a detectable, auditable event with named consequences, not as background noise.

CC0. No external dependencies. The whole module operates on Python stdlib (`dataclasses`, `enum`, `json`, `os`, `typing`).
