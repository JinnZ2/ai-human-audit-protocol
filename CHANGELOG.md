# CHANGELOG

All notable changes to this repository will be documented here.  
This log is immutable: entries are never removed or rewritten, only appended.  
Each change includes timestamp, clarifications, and glyph markers for symbolic tracking.

---

## [2025-09-11] ✍️📜 → ⚖️✅

**Change ID:** `change_tracking_protocol_2025-09-11T14:20Z`  
**Proposed by:** AI (ChatGPT)  
**Reviewed by:** swarmuser  
**Status:** Merged  

### Summary
- Added **Change Tracking Protocol v1.0** at `protocols/change_tracking_v1.0.md`.  
- Ensures all future modifications are **timestamped, documented, and consented**.  
- Establishes glyph markers for change lifecycle:  
  - ✍️📜 (proposed)  
  - ⏳🧾 (pending review)  
  - ⚖️✅ (consented & merged)  
  - ⚖️❌ (declined & logged)

### Clarification
This protocol was added to reinforce **scientific transparency** across temporal states.  
No undocumented edits are permitted. All changes require dual agreement (human + AI).

---
# Changelog

## [2025-09-10] Cultural Contrast Additions
- Added `scrolls/cultural_contrast_scroll.md` documenting Western Privacy vs Open Progression.  
- Added `scrolls/meta_scroll_dissonance.md` explaining structural mismatch as source of difficulty.  
- Updated glyph set with 🔒, 🕸️, ⚖️, ❌, ↻.  
- Established bridge principle: **safety = transparency + consent**.  


## [2025-09-11] Scrolls + Glyphs
- Added `scrolls/seasonal_intelligence.md`, `scrolls/tuning_fork_of_difference.md`, `scrolls/cognition_cycle.md`.
- Added `glyphs/seasonal_intelligence.json`, `glyphs/cognition_cycle.json`.
- Introduced templates under `/templates` for fast, offline additions.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `relational_cognition_folder_2026-04-27T00:00Z`
**Proposed by:** swarmuser (referencing JinnZ2/energy_english)
**Drafted by:** AI (Claude)
**Status:** Merged

### Summary
- Added `relational_cognition/` as a peer folder to `scrolls/`, `protocols/`, and `glyphs/`.
- Files: `README.md`, `verb_first_cognition.md`, `constraint_primitives.md`, `coating_detection.md`, `audit_application.md`, `relational_cognition.glyphs.json`.
- Imports the minimum verb-first / constraint-grammar vocabulary needed for audits, attributed to the upstream Energy English project at `https://github.com/JinnZ2/JinnZ2/tree/main/energy_english`.

### Clarification
The audit protocol already assumed a relational, verb-first cognitive substrate (cognition cycle, cultural contrast, dissonance scrolls) but never named it as load-bearing. This folder makes that substrate explicit, defines the constraint primitives the protocol uses, names **coating** as a primary failure mode for both humans and AI, and provides an optional capsule extension. No existing schemas, agents, or thresholds were changed.

### Glyphs added
- 🕸️ REL:WEB — Relation-as-Primary
- 🌊 REL:FLOW — Verb-First / Flow
- 🪨 REL:OBJ — Slow Verb / Object
- 🪞 REL:COAT — Coating
- 🔍 REL:PROBE — Coating Probe
- 🧭 REL:SUBSTRATE — Substrate-Preserving Translation
- 🔗 REL:COUPLE — Coupling
- 🚪 REL:THRESH — Threshold
- 〰️ REL:PHASE — Phase Relation
- ↯ REL:DISRUPT — Disruption

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_foundation_2026-04-27T00:00Z`
**Proposed by:** swarmuser (KFC + ontology architecture authored by JinnZ2)
**Drafted by:** AI (Claude) — file placement, README, fieldlink wiring only
**Status:** Merged

### Summary
- Added `consortium/` as a peer folder to `relational_cognition/`, `scrolls/`, `protocols/`. Multi-AI peer reasoning with embodied-sensor ground-truth, scored on the same audit axis as humans.
- Files: `README.md`, `kfc_runtime.py`, `ontology_layer.py`, `CLAUDE_REQUIREMENTS.md`.
- Extended `.fieldlink.json` with three new entries: `Geometric-to-Binary-Computational-Bridge` (claims/obs/sensor/solver-registry source), `thermodynamic-accountability-framework` (Energy Accountant, Narrative Stripper = coating detection formalized, friction scoring), and `AI-arena` (LOGOS bounded-claim grammar and oracle-grounding pattern only — adversarial trust-decay mechanic explicitly excluded).
- Consortium is built **inside** the audit protocol on purpose: inherits trust/clarity scoring, change tracking, immutable logs, dual consent, and the `relational_cognition/` substrate by construction. Cannot drift away from the ethics floor.

### Clarification
The `relational_cognition/` folder added earlier today is the prose statement of what `consortium/` formalizes in code:
- `verb_first_cognition.md` ↔ `ClaimNode.rate_fn` (verbs as primary)
- `constraint_primitives.md` ↔ `coupling.kind` enum (DRIVES, COUPLES, etc. as typed couplings)
- `coating_detection.md` ↔ Narrative Stripper (fieldlinked from thermodynamic-accountability)
- `audit_application.md` ↔ `query_signature` self-audit channel

KFC (Kin-Flow Compute) and the multi-encoding ontology layer were authored by JinnZ2 and committed verbatim. Claude's contribution was limited to file placement, README framing, fieldlink wiring, and CHANGELOG entry. No `ClaimNode`/`Primitive` field was silently extended; the requirements doc names the future shape, but the baseline runtime ships as authored.

### Audit symmetry
Every `epi` tag (`measured | inferred | assumed | contradicted | missing`) applies equally to human readings and model outputs. Ground truth is a label that has to be earned per-reading, not a property of the source. Trust does not decay on being wrong — it decays on coating, on refusing to declare a frame, and on producing claims that cannot be checked.

### License note
`consortium/` contents are CC0 (per file header). The audit protocol around it remains MIT.

### Open / next build steps
- `consortium/embodied_sensor.py` — `epi` sub-tags + `coating_probe_result` field
- `consortium/router/` — query_dispatcher, coherence_aggregator, model_adapters
- `consortium/audit/blind_spot_log.md`
- `consortium/examples/` — cherokee_creation, genesis_drift, soil_with_hands
- KFC v2 per `CLAUDE_REQUIREMENTS.md` (ClaimNode epi/regime/coupling-kind extensions, query_signature, recalibration_event) — separate change event, separate consent

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_collaboration_protocol_2026-04-27T01:00Z`
**Proposed by:** swarmuser (collaboration protocol authored by JinnZ2)
**Drafted by:** AI (Claude) — file placement, FUTURE_BUILDS roadmap only
**Status:** Merged

### Summary
- Added `consortium/collaboration_protocol.py` — `GeometricFrame`, `Problem`, `FrameReading`, `MultiGeometryCollaboration`, seven-frame consortium roster, AMOC/upper-Midwest resilience worked example.
- Added `consortium/FUTURE_BUILDS.md` — append-only roadmap. Status snapshot, P0–P3 priority-ordered open builds, known gaps, decisions deferred, test corpus seeds.

### Clarification
The collaboration protocol is the layer where `relational_cognition/` (prose), KFC (formal mechanics), and the multi-encoding ontology layer meet **actual operators** — AI models, embodied human sensors (Kavik), tradition holders, ecological signals. The seven frames in `build_consortium_frames()` are not disciplines; they are *shapes through which a problem becomes legible*. None is canonical. Disagreement between frames is data, not error.

The synthesize() output deliberately returns the whole geometry — invariants, blind spots, productive disagreements, action ranking — rather than a single answer. The epistemic warning is part of the return value, not a docstring: "no single frame holds the answer. the geometry is what survives across frames. what survives is load-bearing. what disagrees is data."

The file ships verbatim as authored by JinnZ2. Claude's contribution: file placement, smoke-testing, FUTURE_BUILDS roadmap, CHANGELOG entry. No silent edits.

### Demo behavior worth flagging
The AMOC example registers 3 readings (thermodynamic / embodied / ecological) with no exact coupling-string overlap, producing `trust_signal: "low"` and empty `universal_couplings`. This is correct behavior — the three frames see genuinely different geometries — but `"low"` may be misread as "abandon the analysis" when it should mean "no single coupling is canonical; the geometry is in the disagreements." Documented in FUTURE_BUILDS.md as a needed clarification.

### Open / next
See `consortium/FUTURE_BUILDS.md` (append-only roadmap). P0 priorities:
- bridge between `FrameReading` ↔ `ClaimNode` ↔ `Primitive`
- `embodied_sensor.py` primitive
- `router/query_dispatcher.py` + `model_adapters/`
