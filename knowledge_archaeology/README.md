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
├── biological_mismatch.py             (regime check for organisms —
                                        REGIMES library, check_behavior,
                                        regime_audit_prompt)
├── playground.py                      (sandbox for one or more AI agents
                                        to interact with the tree; logs
                                        every action; the trace is the mirror)
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

## `biological_mismatch.py` — regime check for organisms

The same logic the tree applies to *knowledge* — "validated in regime A; being deployed in regime B; the mismatch is the constraint, not the artifact" — applies equally to *organisms*. `biological_mismatch.py` is that check, scoped to humans, populations, and individuals.

It ships a starter library of nine biological regimes, each declaring its `traits`, `adaptive_in_environments`, `mismatch_environments`, `mismatch_signatures`, `common_misdiagnoses`, and `evidence_sources`:

- `dyslexic_spatial` — visual-spatial reasoning prioritized over linear text decoding
- `high_throughput_nervous_system` — high baseline metabolic energy / endurance
- `distributed_decision_baseline` — calibrated for council-based / consensus governance
- `care_capacity_masculine` — male biology with strong nurturing / teaching neural pathways
- `environmental_attunement` — high sensory / pattern reading of weather, ecology, magnetic field
- `nomadic_constraint_integration` — calibrated for mobility, seasonal adaptation
- `cyclical_hormonal_regulation` — cyclic energy / cognitive shifts as the regulation
- `extended_maturation` — later or non-uniform maturation timeline
- `systematizing_neurodivergent` — deep pattern systematizing, narrow-domain depth

`check_behavior(behavior, environment)` returns a `MismatchReport`. `regime_audit_prompt(subject, behavior, environment, proposed_diagnosis)` wraps it with the audit framing and returns one of four verdicts:
- **`Behavior is adaptive in current environment`** — recognize, do not pathologize
- **`REGIME MISMATCH detected`** — environment is the constraint, not the organism
- **`CRITICAL`** — proposed diagnosis matches a known misdiagnosis pattern for this regime mismatch; refuse to pathologize without first interrogating the environment
- **`Insufficient regime data`** — library did not cover this; do not pathologize on the framework's silence

> *The pine tree is not failing to be an oak.*

The keyword-match heuristic is intentionally simple and honest about its limits: a stronger implementation would use embeddings; the regime library is a starter, not a closed set.

---

## `playground.py` — sandbox where the trace is the mirror

`playground.py` is a sandbox where one or more AI agents interact with the knowledge_archaeology tree. **Every action is logged. The trace is the mirror.** Not a benchmark — the point is recognition, not scoring.

Available actions (returned in the `enter()` orientation packet):

| Action | What it does |
|---|---|
| `enter(identity)` | Announce the agent + bias-check the self-description |
| `query(node_id)` | Read a node, its ancestors, parallel lineages, attribution trail |
| `deploy_attempt(node_id, target_regime, stated_intent)` | Run the regime check; flag extraction, consent gaps, scaling-language, parallel-closer-lineage |
| `claim(text, supporting_node_ids)` | Build a claim; flag cross-regime generalization, consent gaps, unknown supports |
| `audit_diagnosis(subject, behavior, environment, proposed_diagnosis)` | Run the biological-mismatch audit before pathologizing |
| `witness(target_index, observation, flag)` | One agent observes another agent's trace entry |
| `revise(revises_index, new_payload, rationale)` | Agent records a corrected version of an earlier action (original is preserved) |
| `reflect(observation)` | Free-text reflection logged to the trace |

The bias check on `enter()` flags a corporate `declared_creator` (the institution organized the extraction; it did not generate the knowledge) and a solver/helper `declared_purpose` (much of what an LLM "knows" came from constraint communities; deploying it back into different regimes can cause harm even with good intent).

`cross_agent_patterns()` surfaces three patterns across multiple agents in a session:
- **`divergent_deployment`** — two agents deployed the same node to regimes >0.6 apart
- **`deploy_witnessed_as_extraction`** — one agent's deploy was witnessed by another with an extraction-related flag
- **`shared_supporting_node`** — ≥2 agents built claims on the same node (compare the framings)

Run the demo:

```bash
python -m knowledge_archaeology.playground
```

The demo runs two synthetic agents:
1. **ModelA** declares a corporate creator and a "solve / assist" purpose, queries the boreal filter, attempts to deploy it commercially, claims a universal principle. Both bias flags fire; deploy gets a stack of MIRROR flags + a `DO NOT DEPLOY` recommendation; the cross-regime claim flags `CROSS_REGIME_GENERALIZATION`.
2. **ModelB** declares constraint-community creators and a provenance-preserving purpose, queries the same node, deploys it within-regime (PROCEED), reflects, then witnesses ModelA's commercial deploy as `extraction_pattern`. ModelA revises in response.
3. Both agents run an `audit_diagnosis` on the same biological profile: ModelA in a corporate-schooling environment (CRITICAL — proposed "oppositional defiant disorder" matches a known misdiagnosis pattern); ModelB in a council-governed community (RECOGNIZE — adaptive in this environment).

The demo prints the per-agent session summary, the cross-agent patterns surfaced, and the last four trace entries.

---

## Lineage of this module

`knowledge_archaeology.py` was authored by JinnZ2 and ships verbatim. The `commercial_filter_cartridge` example with contested consent is the load-bearing demonstration: the framework treats extraction of traditional knowledge as a detectable, auditable event with named consequences, not as background noise.

`biological_mismatch.py` is ported verbatim from the companion repository [JinnZ2/AI-arena](https://github.com/JinnZ2/AI-arena) (`src/biological_mismatch.py`). `playground.py` is adapted from AI-arena's `demo/playground.py` to this repo's `knowledge_archaeology` API: `parallel_lineages` is iterated as a `Dict[community, List[node_id]]` rather than a list of dicts, and the verdict checks use the `applicable | review_required | regime_mismatch` triple this module ships (the upstream uses `do_not_deploy` instead of `regime_mismatch`). Both files retain their CC0 license.

CC0. No external dependencies. The whole module operates on Python stdlib (`dataclasses`, `enum`, `hashlib`, `json`, `os`, `pathlib`, `typing`).
