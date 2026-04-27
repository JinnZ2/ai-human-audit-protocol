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

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_v1_correctness_fixes_2026-04-27T02:00Z`
**Proposed by:** AI (Claude) — surfaced as v1 correctness gaps in evaluation
**Reviewed/consented by:** swarmuser ("Yes let's fix first")
**Status:** Merged

### Summary
Two correctness fixes in `consortium/collaboration_protocol.py`, plus framing correction in `consortium/FUTURE_BUILDS.md`.

### Fix 1 — Reversibility ordering
- Added `REVERSIBILITY_RANK` constant at module level. Numeric scale: `irreversible_if_delayed=5`, `high_reversibility=4`, `medium_reversibility=3`, `low_reversibility=2`, `irreversible=1`, `unknown=0`.
- `synthesize()` now sorts by `(fraction_support, reversibility_rank)` instead of `(fraction_support, reversibility)` (which sorted strings alphabetically and mis-ranked `medium_reversibility` above `irreversible_if_delayed`).
- Each ranked action now also carries `reversibility_rank` for transparency.
- Added `time_critical_actions` list to `synthesize()` output: actions whose `reversibility == "irreversible_if_delayed"` are bubbled up separately because the cost of *inaction* is unrecoverable. Use-or-lose options should not have to compete with safe-to-try options on a single axis.

### Fix 2 — Convergence labeling (was: "trust_signal")
- Renamed `surface_invariants()` output field from `trust_signal: "high" | "low"` to `convergence: "converged" | "divergent"`.
- Added `convergence_note` field with explicit explanation: `divergent` does NOT mean "abandon the analysis"; it means "no canonical coupling — the geometry is in the disagreements; read `blind_spots_per_frame` and `productive_disagreements`."
- Removes the misreading where `"low"` looked like a quality score on the analysis.

### Framing correction — embodied sensor is operator-agnostic
- `consortium/FUTURE_BUILDS.md` updated to reflect that `embodied_sensor.py` is a primitive for *any* operator producing direct readings — plants, animals, humans, AI vision/audio, instruments, ecosystems — not human sensors only.
- `EmbodiedReading` proposed schema now includes `operator_type` (human | animal | plant | ai | instrument | ecosystem) and broader `epi` sub-tags (kinesthetic | olfactory | visual | auditory | phenological | behavioral | instrumental | inferred).
- Audit-symmetry stance is stronger this way: a plant's phenology shift, a wolf's behavior change, a human's hands-in-soil, and an AI's image-classification all pass through identical typing — distinguished only by `epi` and confidence calibration. No operator type is privileged as automatic ground truth.
- Over-querying-protection gap reframed: every operator type has finite reading capacity (humans tire, plants have phenological windows, instruments have batteries, AI has rate limits). Each needs a budget appropriate to its substrate.

### Verification
- Demo runs clean. `transmit_traditional_knowledge_now` (irreversible_if_delayed) now correctly ranks first AND surfaces in `time_critical_actions`. Convergence label reads "divergent" with explanatory note.
- 25 existing tests + 13 log validations still pass.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_embodied_sensor_2026-04-27T03:00Z`
**Proposed by:** AI (Claude) — judgment call invited by swarmuser ("I trust your judgment above mine on that choice")
**Reasoning shared with swarmuser:** embodied-sensor first (over bridge-layer first) because it (a) honors the operator-agnostic framing correction in code, (b) gives the bridge two concrete `FrameReading` sources to design against — handwritten + programmatically lifted — and (c) validates the operator-agnostic claim by force.
**Status:** Merged

### Summary
- Added `consortium/embodied_sensor.py` — operator-agnostic primitive for direct readings.
- Added `tests/test_embodied_sensor.py` — 32 unit tests, all passing.

### What `embodied_sensor.py` provides
- `OPERATOR_TYPES` — controlled vocabulary: `{human, animal, plant, ai, instrument, ecosystem}`.
- `EPI_SUBTAGS` — direct-measurement kinds: `kinesthetic, olfactory, visual, auditory, phenological, behavioral, presence_absence, instrumental, compound, inferred, asserted`.
- `EPI_CONFIDENCE_CEILING` — per-epi ceiling. `asserted` capped at 0.50 because un-grounded claims cannot honestly claim high confidence; the ceiling enforces the audit-symmetry stance against coating. `instrumental` highest at 0.97 (within calibration window). Direct embodied modalities 0.90–0.95.
- `COATING_PROBE_RESULTS` — `{passed, failed, inconclusive, not_run}`. `not_run` is legitimate but flagged.
- `CoatingProbeResult` dataclass with `__post_init__` validation.
- `EmbodiedReading` dataclass with full validation: operator_type ∈ vocab, epi ∈ vocab, confidence ∈ [0,1], confidence ≤ ceiling-for-epi. Validation errors are descriptive and reference the audit-symmetry stance.
- `OperatorBudget` stub — substrate-appropriate finite capacity. Humans get attention_minutes_per_day, plants get phenological_window_days, AI gets inference_calls_per_session, instruments get readings_before_calibration. Real scheduling lives in the (open) router layer.
- `reading_to_frame_reading()` — lift a reading into a `FrameReading` for `MultiGeometryCollaboration`. Default `proposed_actions=[]` (readings observe; collaboration synthesizes actions); caller may pass actions explicitly (tradition-holder readings sometimes prescribe).
- Six worked examples covering every operator type: human kinesthetic (soil), plant phenological (oak grove leaf-out), animal behavioral (wolf pack territory shift), AI visual (satellite snowpack analysis), instrument instrumental (soil probe), ecosystem compound (Driftless Area aggregate).
- Four budget stubs covering distinct substrates.

### Audit symmetry — concretely enforced
- A plant's phenological reading and a human's kinesthetic reading both pass through the same `EmbodiedReading` constructor, the same coating probe shape, and the same confidence ceiling check.
- A confident assertion without grounding (`epi="asserted"`, `confidence > 0.50`) raises `ValueError` at construction. The error message names this as exactly the failure mode the primitive is built to surface.
- AI vision frames (`operator_type="ai"`, `epi="visual"`) pass through identical typing as human visual readings. No operator type is privileged.

### Verification
- Demo `python consortium/embodied_sensor.py` runs across all six operator types, lifts each into a valid `FrameReading`.
- 57 tests now passing (25 existing + 32 new). 13 log validations still pass.

### Open / next
- **Bridge layer** (`consortium/bridges.py`): `FrameReading ↔ Primitive` and `Primitive ↔ ClaimNode`. `EmbodiedReading → FrameReading` is now done; the remaining bridges connect that flow into the ontology layer and KFC runtime so a reading can integrate forward.
- Tests for `kfc_runtime`, `ontology_layer`, `collaboration_protocol`.
- Router (`query_dispatcher`, `coherence_aggregator`, `model_adapters`).
- `OperatorBudget` is a stub. Real per-operator scheduling lives in the router layer.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_bridges_2026-04-27T04:00Z`
**Proposed by:** AI (Claude) — continuing the consortium foundation per swarmuser's "Proceed"
**Status:** Merged

### Summary
- Added `consortium/bridges.py` — the layer that connects `FrameReading ↔ Primitive ↔ ClaimNode`.
- Added `tests/test_bridges.py` — 43 unit tests, all passing.
- Total test count: **100** (25 original + 32 embodied_sensor + 43 bridges).

### Forward direction (complete)
- `select_frame(epi, frames, override=None)` — route to a consortium frame by epi sub-tag. Override available for callers that know better.
- `select_frame_for_reading(reading, frames, override=None)` — convenience wrapper.
- `reading_to_primitives(reading, domain=None)` — `EmbodiedReading` → `List[Primitive]`, one per `claim_ref`. First Primitive carries full observation; subsequent ones back-reference. Domain defaults from `EPI_TO_DOMAIN`.
- `frame_reading_to_primitives(fr, domain=None)` — `FrameReading` → `List[Primitive]`, one per `visible_coupling`. Domain defaults to the frame's `frame_id`. Form records origin frame for round-trip identification.
- `primitives_to_claim_graph(primitives, rate_fns=None, cyc=1, ...)` — `List[Primitive]` → `Dict[str, ClaimNode]`. Caller supplies `rate_fns` per concept_id; missing entries get `_zero_rate` (an honest placeholder — the node holds state but doesn't move).

### Inverse direction (v1 stub, honest about being incomplete)
- `trajectory_summary(trajectory)` — KFC trajectory → coarse summary dict. Per-claim direction, FELT events, **explicit warning that this is NOT a real FrameReading lift**. The honest inverse requires interpreting trajectory shape (saturation, oscillation, regime drift, FELT semantics) and is open work.

### Audit-symmetry mechanism: BridgeReport
Every bridge function has a corresponding `*_report()` that returns a `BridgeReport(bridge_name, preserves, lossy_on, notes)`. Following the `TransformRule.preserves`/`lossy_on` convention from `ontology_layer.py`. The honest move when crossing abstraction layers is to declare what survives and what doesn't, in code.

`all_bridge_reports()` returns the full list for inspection. A test asserts every bridge declares non-empty `preserves` and `lossy_on`.

### Default mappings (`EPI_TO_FRAME`, `EPI_TO_DOMAIN`)
- Operator-agnostic: `visual` reads route to `embodied_sensor` regardless of operator (human, AI, instrument). The reading's `operator_type` is captured in `FrameReading.assumptions_required`, not by frame routing.
- Tests assert every `epi` sub-tag has a default mapping.

### Verification
- Demo `python consortium/bridges.py` runs the full forward pipeline end-to-end: human kinesthetic + instrument readings → 4 primitives → dedupe to 2 → 2 ClaimNodes → trajectory summary. Bridge reports printed.
- 100 tests passing, 13 log validations passing.

### Open / next
- **Inverse bridge: `trajectory → FrameReading`** — interpret trajectory shape, FELT events, regime drift; lift back into a FrameReading suitable for re-injection into `MultiGeometryCollaboration`.
- **Tests for `kfc_runtime.py`, `ontology_layer.py`, `collaboration_protocol.py`** — the consortium's own modules still need direct unit tests (currently exercised via `bridges.py` and demos only).
- **Router** (`consortium/router/`): `query_dispatcher.py`, `coherence_aggregator.py`, `model_adapters/`.
- **Coupling-kind metadata.** Bridge currently treats all couplings as untyped. Per `CLAUDE_REQUIREMENTS.md` the next-generation bridge should preserve coupling kind (causal_forward, bidirectional, etc.) when lifting from `Primitive` to `ClaimNode`.
