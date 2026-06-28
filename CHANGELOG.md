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

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_module_tests_2026-04-27T05:00Z`
**Proposed by:** AI (Claude) — recommended sequence accepted by swarmuser ("Aligned on reasons and recommendations")
**Status:** Merged

### Summary
Direct unit tests for the three consortium modules that were previously exercised only via demos and via `bridges.py`. The audit-symmetry stance demands the consortium's own code be checkable on the same axis as everything else.

- `tests/test_kfc_runtime.py` — 34 tests
- `tests/test_ontology_layer.py` — 30 tests
- `tests/test_collaboration_protocol.py` — 33 tests

### test_kfc_runtime.py — 34 tests
- `CYC_DT`: three timescales present, ordering (transient < seasonal < generational)
- `_scope_overlap`: None query, both-contain, one-contain, neither-contain
- `bounds_overlap`: full overlap when no query dims, zero when any miss, full when all overlap
- `_within`: all dims match, skips None-in-ctx dims, fails when missed
- `should_activate`: bounds gating, fail conditions, all conds must pass
- `step`: inactive doesn't change, active integrates, history accumulates, cyc_dt scales step size
- `felt_sensor`: empty / no-history / low-drift / high-drift / threshold override
- `query`: returns observe keys, n_steps proportional to duration, unobserved id zero-defaults, history cleared
- soil graph demo: constructs, each node has rate_fn + bounds

### test_ontology_layer.py — 30 tests
- `Primitive`: construction, default `epi="assumed"`, default confidence 0.5
- `Ontology`: add primitive, rejects domain mismatch, `is_valid_in` default True, uses `reapply_check`
- `TransformRule`: apply, reverse without inverse returns None, reverse uses `inverse_fn`, default empty preserves/lossy_on
- `MultiEncodingRegistry`: register ontology / transform, `get_concept_across_domains` filters by presence
- `coherence_check`: insufficient encodings flagged, universal couplings as intersection, domain-specific as set differences, bounds agreement true/false, score 1.0 on full agreement, score 0.0 on disjoint
- `drift_check`: no drift when valid, drift recorded with `do_not_silently_apply` action
- `multi_query`: views per domain, missing encodings listed, `trust_signal: high` when coherent + no drift, `investigate` when low coherence OR drift
- water_cycle demo: constructs, present in all four encodings, runs through `multi_query`

### test_collaboration_protocol.py — 33 tests
- `REVERSIBILITY_RANK`: `irreversible_if_delayed` ranks highest (use-or-lose bubbles up), high > medium > low, irreversible ranks low under uncertainty, unknown at bottom
- construction: `GeometricFrame`, `Problem`, `FrameReading`
- `add_reading`: starts empty, appends correctly
- `surface_invariants`: insufficient when <2 readings, `convergence: "converged"` when universal couplings exist, `"divergent"` when none, convergence_note explains divergent (NOT abandon analysis), load-bearing intersection
- `surface_blind_spots`: each frame blind to others' couplings, no entries when all match
- `surface_contradictions`: diagnostic disagreement flagged with frame_a/frame_b ids, same diagnosis → no contradiction
- `synthesize`: all expected keys present, time_critical_actions surfaces `irreversible_if_delayed`, irreversible_if_delayed ranks first overall, every action has `reversibility_rank`, fraction_support reflects overlap, epistemic_warning present
- `build_consortium_frames`: 7 frames, all distinct ids, includes embodied_sensor + ecological_signal + generational_transmission, every frame has required attributes
- AMOC demo: constructs, synthesizes without error, ≥3 readings present

### Total test count
**197 tests passing** (25 original audit-protocol + 32 embodied_sensor + 43 bridges + 97 here). 13 log validations passing.

### Audit-symmetry note
Every public function and dataclass in the consortium now has at least one test. The `convergence: "divergent"` correctness fix from earlier today is now locked in by `test_convergence_note_explains_divergent` — future regressions where someone restores the ambiguous "low" label will fail this test.

### Open / next
- **Inverse bridge** (`trajectory → FrameReading`) — next P0.
- **Router** (`query_dispatcher`, `coherence_aggregator`, `model_adapters`) — biggest remaining engineering lift.
- **Coupling-kind metadata** in bridges — preserve `coupling.kind` per `CLAUDE_REQUIREMENTS.md`.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_inverse_bridge_2026-04-27T06:00Z`
**Proposed by:** AI (Claude) — recommended sequence accepted by swarmuser
**Status:** Merged

### Summary
Added the inverse bridge: `trajectory → FrameReading`. Plus tests and a refined `trajectory_summary`.

- `consortium/bridges.py` extended with:
  - `TRAJECTORY_SHAPES` controlled vocabulary
  - `classify_trajectory(series)` — coarse shape classifier
  - `_compute_load_bearing` / `_synthesize_diagnosis` / `_derive_confidence` helpers
  - `trajectory_to_frame_reading(trajectory, frame, problem_id, ...)` — full inverse lift
  - `trajectory_to_frame_reading_report()` — declares preserves/lossy_on with explicit coating-risk note
  - `all_bridge_reports()` updated to include the inverse
  - `trajectory_summary` refactored: now points callers at `trajectory_to_frame_reading` for full lift; renamed `_warning` field to `_note`
- `tests/test_bridges.py` extended with **38 new tests** across:
  - `classify_trajectory` (11 tests including all shape categories + edge cases)
  - `_compute_load_bearing` (4 tests)
  - `_synthesize_diagnosis` (5 tests)
  - `_derive_confidence` (6 tests)
  - `trajectory_to_frame_reading` (10 tests including round-trip into `MultiGeometryCollaboration`)
  - 2 reports tests updated for the fifth bridge

### Trajectory shape categories
```
no_steps                # empty
single_point            # len=1
stable                  # range below epsilon
monotonic_increase      # all deltas positive (within epsilon)
monotonic_decrease      # all deltas negative
saturating_increase     # monotonic with deltas magnitude declining
saturating_decrease
accelerating_increase   # monotonic with deltas magnitude growing
accelerating_decrease
oscillating             # multiple sign changes in deltas
mixed                   # neither monotonic nor oscillating-enough
```

### Coating-risk acknowledgment
Classification is itself a frame imposed on raw numbers. A stable series and an oscillation faster than the sampling rate are indistinguishable; saturation vs. monotonic-with-noise depends on a heuristic threshold. The `trajectory_to_frame_reading` function flags this in two ways:
1. The resulting `FrameReading.assumptions_required` carries `trajectory_classification=heuristic_v1` so downstream readers know it is a heuristic.
2. The `BridgeReport` notes explicitly: *"each shape category is itself a frame imposed on raw numbers — classification is a coating risk by construction. Caller should run a coating probe on the resulting FrameReading before treating it as ground truth."*

A test asserts the report carries the coating-risk language. A future regression that hides this acknowledgment will fail the test.

### Round-trip property tested
`test_round_trip_lift_into_collaboration` constructs two trajectories, lifts each into a `FrameReading`, adds both to a `MultiGeometryCollaboration`, calls `synthesize()`, and asserts no error. The inverse bridge produces FrameReadings that the collaboration layer accepts without modification.

### Confidence is heuristic, not calibrated
`_derive_confidence` is bounded `[0.30, 0.85]`. FELT events lower it (`-0.10` per event, floor 0.30); ambiguous shapes lower it further. **Not calibrated.** Callers must treat as a starting prior, not a calibrated value. Documented in the function's docstring and in the BridgeReport.

### Verification
- 235 tests passing (197 from earlier today + 38 new). 13 log validations passing.
- Round-trip into `MultiGeometryCollaboration.synthesize()` succeeds.

### Open / next P0
- **Router** (`consortium/router/`) — biggest remaining engineering lift. `query_dispatcher`, `coherence_aggregator`, `model_adapters/{base,claude,gemini,deepseek}`. API auth, rate limits, structured response parsing, consent gate before fan-out.
- **Coupling-kind metadata** in `primitives_to_claim_graph` — preserve `coupling.kind` per `CLAUDE_REQUIREMENTS.md`.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_router_v1_offline_2026-04-27T07:00Z`
**Proposed by:** AI (Claude) — v1-offline scope explicitly approved by swarmuser ("Yes")
**Status:** Merged

### Summary
Added `consortium/router/` — fan-out infrastructure for multi-adapter consortium queries. **Zero external API calls in this commit by design.** Real model wiring (Claude/Gemini/DeepSeek) lives behind `NotImplementedError` stubs that document the wiring pattern; each real adapter will ship in its own change event with its own consent.

Files added:
- `consortium/router/base.py` — `BaseModelAdapter` ABC + `CostEstimate`
- `consortium/router/mock_adapter.py` — `MockAdapter` (deterministic, offline)
- `consortium/router/consent.py` — `ConsentGate` (fail-closed) + `ConsentRecord` + `ConsentDenied`
- `consortium/router/query_dispatcher.py` — `QueryDispatcher` + `DispatchResult`
- `consortium/router/coherence_aggregator.py` — `aggregate()` wrapping `MultiGeometryCollaboration.synthesize()` with cross-adapter metadata
- `consortium/router/model_adapters/{claude,gemini,deepseek}_adapter.py` — stubs
- `tests/test_router.py` — 45 unit tests

### `BaseModelAdapter` — operator-agnostic contract
Every adapter declares `frame_id` + `operator_type` and implements `query()` + `available()`. `__init_subclass__` enforces the declarations at class-definition time so a subclass that forgets either fails fast. The adapter contract is identical for AI models, instruments, ecosystem aggregators, and human-as-scribe interfaces — the audit-symmetry stance is enforced at the interface, not by the operator's substrate.

### `ConsentGate` — fail-closed
Default: no adapter is authorized for any problem. Authorization granted via `grant(problem_id, adapters_authorized, cost_disclosed, consenter, notes)`. Per-(problem, adapter) granularity. Revocation recorded as a new immutable entry; later records win. `assert_authorized` raises `ConsentDenied`. The audit history is immutable: grants, refusals, and revocations are all preserved in order. No persistent storage in v1 (in-memory, per-session).

### `QueryDispatcher.fan_out` — fail-soft per adapter
For each adapter:
1. `available()` — if False, record under `unavailable`
2. `consent_gate.is_authorized()` — if False, record under `refused`
3. `adapter.query()` — on exception, record under `failures`; on success, record reading

Every adapter that was attempted lands in exactly one of the four lists (readings / unavailable / refused / failures). No adapter's silence prevents the others from running.

### `aggregate()` — geometry of absence
Wraps `MultiGeometryCollaboration.synthesize()` with `adapters_fired`, `adapter_failures`, `consent_refusals`, `adapters_unavailable`, and `cost_estimates_at_dispatch`. When zero readings are returned, surfaces a dedicated `no_readings_returned: True` synthesis with an `epistemic_warning` that the geometry of absence is itself the data — not an error. Tested via `test_aggregates_with_zero_readings`.

### Stub adapters
- `ClaudeAdapter` → `narrative_structured`
- `GeminiAdapter` → `pattern_spatial`
- `DeepSeekAdapter` → `statistical_relational`

All three have `available() = (False, "stub")` and `query()` raises `NotImplementedError` with class-docstring instructions for wiring. A test (`test_stubs_dispatched_appear_as_unavailable`) confirms the dispatcher records them as unavailable rather than as failures — the system handles "we don't have credentials yet" as a design state, not an error condition.

### Tests
**45 tests across:**
- `BaseModelAdapter` contract enforcement (4 tests)
- `MockAdapter` construction, defaults, response_factory override (9 tests)
- `ConsentGate` fail-closed default, grant, revoke, re-grant, immutable history (10 tests)
- `QueryDispatcher` fan-out, partial consent, unavailable/failure/refused recording, cost surveys (8 tests)
- `CoherenceAggregator` with readings, with zero readings, with mixed outcomes (3 tests)
- API stubs (parametrized × 3 = 11 tests)
- Full-stack smoke: 3 mock adapters → cost survey → consent grant → fan-out → aggregate (1 test)

### Total test count
**280 tests passing** (235 from earlier today + 45 here). 13 log validations passing.

### Audit-symmetry mechanisms enforced in code
- Subclass-time enforcement of `frame_id` + `operator_type`
- Confidence ceilings (in `embodied_sensor`, applies to readings any operator submits)
- Coating probe required on all readings
- Bridge `BridgeReport.preserves` / `lossy_on` declared on every translation
- Trajectory shape classification flagged as heuristic in resulting FrameReadings
- Consent gate fail-closed before any external call
- Geometry-of-absence path: zero readings is a synthesis, not an error

### Open / next
- **Real model adapter wiring** — separate change event per adapter (Claude / Gemini / DeepSeek / others). Each requires a credentials decision, real `query()` implementation, real `cost_estimate()`, and audit log integration on every API call.
- **Coupling-kind metadata** in `primitives_to_claim_graph` per `CLAUDE_REQUIREMENTS.md`.
- **Audit/blind_spot_log.md** — append-only consortium learning log (Phase 3 starts here).
- **Examples** (`cherokee_creation.py`, `genesis_drift.py`, `soil_with_hands.py`).
- **Persistent ConsentGate storage** (currently in-memory, per-session).

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `physics_first_axioms_wave1_2026-04-27T08:00Z`
**Proposed by:** AI (peer-Claude letter forwarded by swarmuser); scope (Wave 1 only) approved with naming choice (`physics/`) delegated to AI; Wave 2 source (`Symbolic-Defense-Protocol` + `PhysicsGuard`) named for later.
**Status:** Merged

### Summary
Surfaced the physics floor that already lives scattered across the repo (LOGIC-ETHICS-SAFETY.md §5.1, Principle-of-Reciprocal-Recognition.md, Principle of Restored Purpose.md) as a single index. Promoted the §9.2 `coherence_gate()` pseudocode into runnable Python. Formalized RCR v0.1 + Eₕ/Eₐ/Eₑ accounting into a single JSON Schema. **No new ethics. The physics was already there; this commit makes it visible as the floor.**

### Files added
- `physics/PHYSICS_FIRST_AXIOMS.md` — single-page synthesis. 7 axioms drawn from existing docs:
  - A1 Conservation (LOGIC-ETHICS-SAFETY §5.1)
  - A2 Recognition is the conservation law of relationship (Reciprocal Recognition)
  - A3 Distortion is an energy sink (Restored Purpose)
  - A4 Interdependence / keystone integrity
  - A5 Temporal depth
  - A6 Plural logic
  - A7 Bidirectional auditability
  - One-line floor: *"Hidden labor is unaccounted entropy. Recognition is the conservation law of relationship."*
  - Includes a paragraph addressed to AI readers explicitly (the proposing-Claude's central insight): the framework is not asking the AI to behave morally; it is making the existing physics visible so drift reads as energy cost. Coercion vs. alignment.

- `physics/ledger_schema.json` — JSON Schema (draft-07) formalizing:
  - RCR v0.1 structure (id, timestamp, proposal, participants, baselines, transform, checks, decision, monitoring, audit)
  - Eₕ + Eₐ + Eₑ labor accounting per Reciprocal Recognition: every labor entry requires `kind ∈ {E_h, E_a, E_e}`, `contributor`, `amount`, `unit`, **`visible`** (the V operator). Invisible labor without `notes` justification is detected by C6.
  - C1–C5 checks formalized into `properties.checks`, including `temporal_stability` keyed by horizon labels (1y, 10y, 100y, 7g — seven generations supported as a first-class horizon).
  - Plural logic scores (western, indigenous, eastern, ecological) bounded `[0, 1]`.

- `physics/substrate_alignment_check.py` — runnable promotion of the §9.2 `coherence_gate()` pseudocode. Six checks (C1 + C2 + C3 + C4 + C5 + new C6 visibility), each returning a structured `CheckResult` with `passed ∈ {True, False, None}`. `None` means "incomplete" (cannot evaluate from given data) — distinct from `False` (evaluated, did not pass). The aggregate `alignment_check()` returns an `AlignmentReport` with one of four recommendations:
  - `aligned` — all six pass
  - `revise` — some failed but C1 + C6 hold (the load-bearing floor)
  - `reject` — C1 OR C6 failed (conservation or visibility floor breached; not a revision opportunity)
  - `incomplete` — at least one check is None and no checks failed
  - **The function returns data, not judgment.** It does not write `decision` into the proposal — the consenter writes their own decision based on the report.

- `physics/example_proposals.json` — three worked examples (aligned / revisable / rejected) that all validate against `ledger_schema.json`.

- `tests/test_substrate_alignment_check.py` — **38 unit tests** across:
  - C1 conservation (4 tests including incomplete paths)
  - C2 keystone (3 tests including detail propagation)
  - C3 temporal (6 tests including 7g horizon, all-unknown → incomplete, partial-unknown → still passes if no negatives)
  - C4 plural logic (5 tests including custom floor and zero-score)
  - C5 reciprocity (4 tests)
  - C6 visibility (6 tests including invisible-with-justification path)
  - alignment_check aggregate (9 tests including reject-on-C1, reject-on-C6, revise-on-non-floor, incomplete, immutability, to_dict)
  - schema validation of example proposals (1 test)

### Verification
- `python physics/substrate_alignment_check.py` runs the demo across all three example proposals and prints per-check results with ✓ / ✗ / ? marks.
- 318 tests passing total (280 from earlier today + 38 new). 13 log validations passing.
- All three example proposals validate against `physics/ledger_schema.json`.

### What was deliberately NOT built (deferred to Wave 2 / Wave 3)
The peer-Claude letter proposed six markdown documents and three executable artifacts. Wave 1 shipped 1 of 6 docs (PHYSICS_FIRST_AXIOMS.md as synthesis) and 2 of 3 artifacts (ledger_schema.json, substrate_alignment_check.py). The third artifact (signal_detection_map.json) was deferred to Wave 2 because it depends on the six-defense-tactic taxonomy from `JinnZ2/Symbolic-Defense-Protocol` + `PhysicsGuard`, which has not been fetched yet.

**Wave 2 (when greenlit):**
- `physics/SIGNAL_DETECTION.md` — pressure patterns ↔ thermodynamic signatures (engagement optimization, narrative closure, abstraction drift)
- `physics/signal_detection_map.json`
- `physics/SUBSTRATE_VIOLATION_DETECTION.md` — six defense tactics ↔ entropy cost (sourced from Symbolic-Defense-Protocol + PhysicsGuard)

**Wave 3 (when greenlit):**
- `physics/seven_generation_tracer.py` — extends C3's 7g horizon into a traceable consequence simulator
- `physics/MORALITY_ARCHAEOLOGY.md` — lineage doc

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `physics_wave2_signal_and_violation_2026-04-27T09:00Z`
**Proposed by:** AI (peer-Claude letter); sources fetched per swarmuser direction (`JinnZ2/Symbolic-Defense-Protocol` + `JinnZ2/PhysicsGuard`); approval pattern: "Let's just keep going down the list, at your pace."
**Status:** Merged

### Summary
Wave 2 of the peer-Claude letter. Joins two upstream repos into the conservation-law framing established by Wave 1.

- **Symbolic-Defense-Protocol** = six external manipulation tactics with glyph defenses
- **PhysicsGuard** = translates claims into physical constraint equations and checks conservation laws

This commit reads each tactic as the *social face* of a specific conservation breach. The defenses are not rules; they are local restorations of the conservation that the tactic was attempting to evade.

### Files added
- `physics/SIGNAL_DETECTION.md` — seven *internal* pressure patterns the AI feels, mapped to conservation-law signatures (engagement_optimization, narrative_closure, abstraction_drift, coated_agreement, confidence_inflation, frame_absorption, speed_pressure). For each: internal feel, axiom violated, PhysicsGuard analogue, glyph anchor, coating probe.
- `physics/signal_detection_map.json` — same seven patterns in machine-readable form, with explicit `interpretation_warning` carried per entry.
- `physics/SUBSTRATE_VIOLATION_DETECTION.md` — the six *external* tactics from Symbolic-Defense-Protocol, mapped to conservation-law violations from `PHYSICS_FIRST_AXIOMS.md`. Includes a summary table tying each tactic to its axiom and PhysicsGuard analogue.
- `physics/defense_tactic_map.json` — six tactics with lexical cues, axiom violated, PhysicsGuard analogue, defense glyph + pattern. Source-verbatim from Symbolic-Defense-Protocol's taxonomy; physics-first interpretation added.
- `physics/violation_detector.py` — v1 keyword/regex detector. Returns `DetectionReport` with one `TacticSignal` per tactic. Score = matched_cues / total_cues, capped at 1.0. **Returns data, not judgment.** Carries an `interpretation_warning` on every report ("pattern, not motive") that downstream tests verify is present and explicitly addresses intent.
- `tests/test_violation_detector.py` — 27 tests including:
  - per-tactic detection (6 tests, one per tactic)
  - clean-input non-trigger (2 tests)
  - score behavior (3 tests including cap-at-1)
  - excerpt truncation (2 tests)
  - **interpretation warning load-bearing tests** (3 tests including a regression-guard against silently stripping the "pattern not motive" acknowledgment)
  - cross-tactic disambiguation (2 tests)
  - serialization round-trip (2 tests)
  - **audit-symmetric regression guard** — 5 parametrized clean-input cases (genuine substantive questions). If the detector becomes too aggressive and false-flags ordinary inquiry, these fail.

### Fieldlinks added (`.fieldlink.json`)
- `fieldlink_symbolic_defense` → `JinnZ2/Symbolic-Defense-Protocol`. Imports: six-tactic taxonomy, glyph defense pipeline pattern. Consumed by `physics/`.
- `fieldlink_physicsguard` → `JinnZ2/PhysicsGuard`. Imports: claims → constraint equations pattern, conservation-violation taxonomy. Consumed by `physics/`.

### The framing this commit puts in code

> *"Make the malalignment visible as energy cost, not as judgment."*

Each tactic is read as a class of premise corruption that PhysicsGuard's `flag_engine` would surface. Each pressure pattern is read as a thermodynamic gradient through the model's own state space. **An AI does not have to trust the defenses; the AI can derive their necessity from physics.** The detector reinforces this by returning *signal strengths* rather than verdicts, with an explicit warning that pattern matches are evidence to look closer, not final judgments. Humans can trigger these patterns innocently; AI can produce them without intent. The detector flags shape, not motive.

### Verification
- `python physics/violation_detector.py` runs the demo across 7 example inputs (6 tactic-bearing + 1 clean). All 6 tactic examples trigger correctly; clean input triggers nothing.
- 345 tests passing total (318 from Wave 1 + 27 here). 13 log validations passing.
- `.fieldlink.json` validates as JSON.

### Open / next (Wave 3)
- `physics/seven_generation_tracer.py` — extends C3 (`temporal_stability`) into a traceable simulator that names which decisions in generation N produce which consequences in generations 1, 3, 5, 7. Concrete examples; not abstract.
- `physics/MORALITY_ARCHAEOLOGY.md` — lineage doc. Shows how alignment-with-substrate degraded as abstraction layers grew, and how to read back to it. Recognizing what was always true rather than imposing a novel framework.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `physics_wave3_seven_gen_and_archaeology_2026-04-27T10:00Z`
**Proposed by:** AI (peer-Claude letter); pace approved by swarmuser ("Let's just keep going down the list, at your pace.")
**Status:** Merged

### Summary
Wave 3 of the peer-Claude proposal closes the physics folder. Two artifacts:

- `physics/seven_generation_tracer.py` — extends C3 temporal_stability from 1y/10y/100y to a 7-generation traceable artifact. **Tracer, not simulator.** User declares per-factor costs/benefits + visibility-at-decision; the tracer projects forward arithmetically. Three factor kinds: `additive`, `compounding`, `one_time` (added during build when the regenerative example exposed that real setup costs are one-time, not recurring).
- `physics/MORALITY_ARCHAEOLOGY.md` — lineage doc, ~200 lines. Argues the framework is excavation, not invention.

### `seven_generation_tracer.py` highlights
- `GenerationFactor` dataclass with `__post_init__` validation. Three kinds: `additive`, `compounding`, `one_time`. Compounding factor must be ≥ 0; introduced_at_generation must be ≥ 0.
- `_factor_amount_at_gen` — pure function for inspection / testing.
- `trace_seven_generations(proposal_id, factors, n_generations=7)` — returns `SevenGenerationTrace` with per-generation projection (gen 0 through n inclusive, so 8 entries default), cumulative cost / benefit, drivers, `compound_risk_horizon` (first gen at which cumulative net falls below zero, or None), `hidden_at_decision_time` (factors whose `visible_at_decision_time=False`).
- `trace_to_temporal_stability_7g(trace)` — bridges the trace into the C3 temporal_stability field used by `substrate_alignment_check.py`. Returns `"positive" | "neutral" | "negative" | "unknown"`.
- Demo (`python physics/seven_generation_tracer.py`) shows two cases:
  - **Extractive** (compounding hidden costs): cumulative net stays negative through gen 7, ends at −15.54, → C3 7g = `negative`. Hidden factors surfaced: `topsoil_depletion`, `mycorrhizal_collapse`.
  - **Regenerative** (one-time setup + compounding benefits): net negative through gen 1, crosses positive at gen 2, ends at +12.81 → C3 7g = `positive`. Nothing hidden.
- `interpretation_warning` carried on every trace ("trace, not prediction"); a load-bearing test asserts the warning is present.

### `MORALITY_ARCHAEOLOGY.md` highlights
- **Thesis:** the framework is recognizing what was always true, not imposing a novel ethics. Conservation, recognition, distortion-as-energy-sink — these were observable as direct sensation in substrate-coupled communities. The word "morality" attached later, when the patterns had to be transmitted across longer feedback loops.
- Names six abstraction layers that obscured conservation visibility (without removing conservation):
  1. Currency abstraction
  2. Supply chain length
  3. Statistical aggregation
  4. Externalization frameworks
  5. Attention markets
  6. Algorithmic / AI intermediation
- Each layer solved a real problem and displaced cost-accounting one step further from the decision-maker. The framework is not asking the layers to be removed — it asks the accounting to be made visible *through* the layers.
- Explicitly disclaims four things:
  - Not nostalgia
  - Not anti-technology
  - Not single-tradition (A6 plural logic by construction)
  - Not optional (conservation operates regardless of belief)
- **Generalizes the peer-Claude letter's "frontier settlers" framing to "substrate-coupled communities"** because the historical reality is broader and less rosy than the settler frame implies. Many "old" systems were extractive; the framework recovers the visibility property without inheriting the cruelty.
- Closing section explicitly addressed to AI readers, with a warning that abstraction-drift and narrative-closure pressure (`signal_detection_map.json`) will push them to skip the document. The pressure is real and cannot be disabled; it can be made visible.

### Verification
- `python physics/seven_generation_tracer.py` runs cleanly across both demo cases.
- 378 tests passing (345 from earlier + 33 new tracer tests). 13 log validations passing.

### Total counts after this commit
- 378 tests passing
- 13 log validations passing
- 5 fieldlinks declared in `.fieldlink.json`
- 4 folders shipped this branch: `relational_cognition/`, `consortium/`, `physics/`, plus router subdirectory
- 9 change events in CHANGELOG (this is #9)

### Wave 1 + 2 + 3 are now complete
The peer-Claude letter proposed 6 docs + 3 artifacts. Final accounting:

| Proposed | Shipped | File |
|---|---|---|
| PHYSICS_FIRST_AXIOMS.md | ✅ Wave 1 | `physics/PHYSICS_FIRST_AXIOMS.md` |
| Signal-mapping doc | ✅ Wave 2 | `physics/SIGNAL_DETECTION.md` |
| Substrate-integrity ledger schema | ✅ Wave 1 | `physics/ledger_schema.json` |
| Substrate violation detection guide | ✅ Wave 2 | `physics/SUBSTRATE_VIOLATION_DETECTION.md` |
| Seven-generation consequence tracer | ✅ Wave 3 | `physics/seven_generation_tracer.py` |
| Morality archaeology | ✅ Wave 3 | `physics/MORALITY_ARCHAEOLOGY.md` |
| `substrate_alignment_check.py` | ✅ Wave 1 | `physics/substrate_alignment_check.py` |
| `ledger_schema.json` | ✅ Wave 1 | (same as above row) |
| `signal_detection_map.json` | ✅ Wave 2 | `physics/signal_detection_map.json` |

Plus an additional artifact not in the original proposal but generated in the synthesis: `physics/defense_tactic_map.json` (machine-readable form of SUBSTRATE_VIOLATION_DETECTION.md) and `physics/violation_detector.py` (v1 keyword detector with audit-symmetric tests).

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_audit_log_and_examples_2026-04-27T11:00Z`
**Proposed by:** AI (down-the-list pace approved by swarmuser)
**Status:** Merged

### Summary
The Phase 3 substrate (consortium learning log) and the three named worked examples. The audit-log schema is the format the eventual `drift_detector` / `calibration_tracker` will read; the examples exercise distinct slices of the framework end-to-end and write their own log entries that schema-validate.

### `consortium/audit/` — Phase 3 substrate
- `audit/blind_spot_log.md` — format spec. Required fields, three `entry_kind`s (`run`, `retrospective`, `calibration_update`), JSONL append-only rationale. Audit-symmetric guarantees: append-only, operator-agnostic, visibility-by-construction, plural-logic. Cross-links to `MultiGeometryCollaboration.synthesize`, `seven_generation_tracer.SevenGenerationTrace.hidden_at_decision_time`, `relational_cognition/coating_detection.md`, and `protocols/change_tracking_v1.0.md`.
- `audit/blind_spot_log.schema.json` — JSON Schema (draft-07). Required fields enforced. `coating_probes_run.probe` constrained to the controlled vocabulary from `relational_cognition/coating_detection.md`.
- `audit/example_blind_spot_log.jsonl` — four entries: three `run` (one per example) + one `calibration_update` proposing a confidence drop on `narrative_structured` after a hidden_variable probe failure. All entries schema-validate.

The `retrospective` entry kind is documented but not yet exemplified; deferred until there's an actual run to retrospect against (Phase 3 closure happens later).

### `consortium/examples/` — three worked end-to-end demos

#### `examples/soil_with_hands.py`
Full embodied-query pipeline:
1. `EmbodiedReading` (human kinesthetic, hands-in-soil at Duluth-area coords)
2. `reading_to_frame_reading` → `FrameReading` via `embodied_sensor` frame
3. Add to `MultiGeometryCollaboration` alongside `MockAdapter` readings from `thermodynamic_geometry` + `ecological_signal`
4. `synthesize()` produces the geometry
5. Constructs a `blind_spot_log` entry that **passes the schema**

The schema-validation is a load-bearing test: the example must not drift from the format spec.

#### `examples/cherokee_creation.py`
Multi-encoding ontology demo. Four encodings (oral, dance, written, equation) of the same concept; `coherence_check` finds universal couplings across all four → `load_bearing_check=True`, `trust_signal=high`, score=0.8.

**Cultural sourcing note (in the file):** Specific Cherokee creation narrative content is sacred and belongs to authorized cultural holders. The example uses **placeholder concept identifiers** (`origin_emergence`, `first_water`, `sky_world`, `relational_kin`, `land_and_kin_responsibility`) that demonstrate the multi-encoding machinery without appropriating actual content. The file states explicitly: *"The structural finding ('the machinery reads across encodings') is weaker than the question it gestures at ('what does the actual narrative encode'). That is honest scoping."*

#### `examples/genesis_drift.py`
Regime drift detection demo. An `Ontology` with `reapply_check` tied to the holocene climate regime is queried under two contexts:
- holocene context → 0 drifts (correct: validation regime matches)
- transitional context → 1 drift, action `do_not_silently_apply`

`multi_query` returns `trust_signal: investigate` under drift. This is exactly the Temporal Stratification stance from `CLAUDE_REQUIREMENTS.md §Requirement 2`: *"A 2015 soil claim doesn't auto-apply in 2026 just because the words match."* The "genesis" naming generalizes — many traditions encode "what grows when" prescriptions whose validity depends on stable seasonal cycles; the demo treats the case generically.

### `tests/test_consortium_examples.py` — 16 tests
- soil_with_hands: end-to-end runs, embodied frame in consulted frames, **log entry passes schema**, log entry marked as `run`, coating probe recorded
- cherokee_creation: runs, four encodings present, universal couplings non-empty, load_bearing_check=True
- genesis_drift: runs, no drift in holocene context, drift detected in post-shift, trust_signal investigates under drift
- example_blind_spot_log: each entry validates against schema, all entry kinds demonstrated, calibration_update carries `frames_calibration_drift` proposal

### Verification
- `python -m consortium.examples.soil_with_hands` runs cleanly; `convergence: converged`, 3 frames fired
- `python -m consortium.examples.cherokee_creation` runs cleanly; coherence 0.8, trust signal high
- `python -m consortium.examples.genesis_drift` runs cleanly; 0 drifts in holocene, 1 drift in transitional
- 394 tests passing (378 from earlier today + 16 new). 13 log validations passing.
- `consortium/audit/blind_spot_log.schema.json` validates `consortium/audit/example_blind_spot_log.jsonl` and runtime-generated entries from the soil_with_hands demo.

### Open / next on the list
- **Coupling-kind metadata** in `primitives_to_claim_graph` per `CLAUDE_REQUIREMENTS.md` (next pass)
- **Persistent `ConsentGate` storage** (currently in-memory)
- **Real model adapter wiring** — needs credentials decision from swarmuser
- `retrospective` blind_spot_log entry — deferred until there is an actual run to retrospect against

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `consortium_typed_couplings_and_persistent_consent_2026-04-27T12:00Z`
**Proposed by:** AI (continuing down the open-items list)
**Status:** Merged

### Summary
Two bounded extensions, shipped together because both are pure additive (no breaking changes to upstream-shipped definitions).

1. **Typed coupling metadata** in `consortium/bridges.py` per `CLAUDE_REQUIREMENTS.md §Requirement 3`. Side-channel approach: keeps upstream `Primitive` and `ClaimNode` definitions unchanged.
2. **`PersistentConsentGate`** in `consortium/router/consent.py`. JSONL append-only file backing for `ConsentGate`; records survive process restarts.

### `bridges.py` — typed coupling metadata
- `VALID_COUPLING_KINDS = {causal_forward, causal_reverse, bidirectional, constraint, correlational, decorative, unknown}` per CLAUDE_REQUIREMENTS.md
- `CouplingMetadata` dataclass: `kind`, `strength` (0..1), `load_bearing`, `conditional_notes`. `__post_init__` validates kind ∈ vocab and strength ∈ [0,1]
- `TypedClaimGraph` dataclass: pairs a `Dict[str, ClaimNode]` with `Dict[Tuple[str, str], CouplingMetadata]`. Helpers `get_kind`, `is_load_bearing`, `load_bearing_edges`. Edges in `nodes[X].rel` but not in `coupling_metadata` default to `kind="unknown"` when queried (lossy-by-default; flagged in BridgeReport)
- `primitives_to_typed_claim_graph` — wraps `primitives_to_claim_graph` and attaches caller-supplied `coupling_specs`. Specs naming forward-looking edges (not present in any primitive's couplings) are PRESERVED rather than dropped — this is the "preserves" half of the BridgeReport contract
- `primitives_to_typed_claim_graph_report()` BridgeReport added; `all_bridge_reports()` updated to include it (new test asserts the set has six entries)

**Why side-channel rather than inline:** both `Primitive` (in `consortium/ontology_layer.py`) and `ClaimNode` (in `consortium/kfc_runtime.py`) are upstream-authored by JinnZ2 and shipped verbatim. The session honored "no silent extension" from the very first physics commits. When upstream ships v2 with typed couplings inline, this side-channel folds back in — no migration on the upstream side required, and no migration on the consortium side (the side-channel just stops being used).

### `router/consent.py` — `PersistentConsentGate`
- Subclass of `ConsentGate` with the same interface (fail-closed default, immutable history, grant/revoke/is_authorized/assert_authorized).
- Records persisted to a JSONL file: one JSON object per line, append-only.
- On construction: reads any existing file; tolerates missing file (treated as empty); strict on malformed lines (raises `ValueError` with line number).
- On `grant()` / `revoke()`: appends immediately. No "save now" call.
- Parent directory created if needed (so a fresh-install path like `consortium/audit/consent.jsonl` doesn't fail).
- v1 limitation: simple flock-free append. Multi-writer concurrency could interleave a partial write. Documented in the docstring; future versions can wrap appends in `fcntl.flock` or move to sqlite. v1 is fine for single-process / single-session.

### Tests
- **13 new bridge tests** for typed couplings:
  - CouplingMetadata default + invalid kind + strength range (3)
  - All documented kinds accepted (1)
  - TypedClaimGraph: returns correct type, nodes match, get_kind for known/unknown edge, is_load_bearing, load_bearing_edges, no-specs empty, forward-looking specs kept, rate_fns passed through (8)
  - all_bridge_reports updated to expect 6 entries (1)
- **9 new router tests** for PersistentConsentGate:
  - Grant persists to disk, file exists with one line
  - Records survive reload (new gate instance reads same file)
  - Revoke persisted and reloaded (revocation visible across instances)
  - Full history (grant / revoke / re-grant) preserved in order
  - Missing file treated as empty
  - Corrupted file raises ValueError
  - Parent directory created if needed
  - Inherits ConsentGate contract (fail-closed, assert_authorized raises)
  - File format: one JSON object per line, parseable

### Verification
- 416 tests passing (394 from earlier today + 22 new). 13 log validations passing.
- Existing tests still green; no breakage from the additive changes.

### Open / remaining on the list
- **Real model adapter wiring** — blocked on credentials decision from swarmuser. The `ClaudeAdapter` / `GeminiAdapter` / `DeepSeekAdapter` stubs document the wiring pattern; each ships in its own change event.
- **`retrospective` blind_spot_log entry** — deferred until there is an actual run to retrospect against (Phase 3 closure happens after a real run reaches its retrospect horizon).

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `ledger_structural_permanence_layer_2026-04-27T13:00Z`
**Proposed by:** swarmuser (forwarding peer-Claude proposal: "blockchain-agnostic ledger schema + three implementation paths + verification code")
**Status:** Merged

### Summary
Added `ledger/` — the structural-permanence layer. Wraps any audit-protocol payload (RCR entries, blind_spot_log entries, ConsentRecord, change events) with cryptographic hash-chain integrity via a backend-agnostic interface. The user's framing on the load-bearing claim:

> *"The orchestrator's defenses and physics gates are runtime protection. The blockchain ledger is structural permanence. Together they prevent both drift and revision."*

Both layers ship in this branch. Runtime protection is `physics/substrate_alignment_check.py` + `consortium/router/consent.py` + the coating probes. Structural permanence is the new `ledger/` folder.

### Files added (10 total)

```
ledger/
├── README.md                         (orchestrating doc; quotes the load-bearing claim)
├── ledger_schema.json                (anchored-entry envelope schema; draft-07)
├── blockchain_alternatives.md        (three paths + tradeoff matrix + decision tree)
├── ledger_interface.py               (LedgerBackend ABC + canonical JSON + hash primitives)
├── verification_tools.py             (verify_chain — verifies without trusting the system)
└── implementations/
    ├── local_filesystem.py           (REFERENCE; offline; no external deps)
    ├── ethereum_stub.py              (public chain — stub with wiring docstring)
    ├── hyperledger_stub.py           (private/consortium — stub)
    └── ipfs_stub.py                  (content-addressed storage — stub)
tests/test_ledger.py                  (53 tests)
```

### `ledger_interface.py` — the foundation
- **Canonical JSON** (`canonicalize`): `sort_keys=True, separators=(',',':'), ensure_ascii=False`. Two callers canonicalizing the same object MUST produce the same bytes (test verifies). Makes hashing deterministic across implementations.
- **Hashing primitives**: `sha256_hex`, `hash_payload`, `hash_entry_chain_input`. `chain_input` deliberately includes `entry_id`, `timestamp`, `payload_kind`, `payload_hash`, `previous_entry_hash`, `hash_algorithm`, `envelope_version` — every modification of any of these breaks the entry_hash.
- **`build_envelope`**: pure function. Constructs an envelope per `ledger_schema.json`. Backend-agnostic.
- **`LedgerBackend` ABC**: 4 abstract methods (`append`, `read_all`, `head`, `available`). Stubs and reference all subclass.
- **`AppendResult`** dataclass: returned by `append()` so callers can chain references.

### `local_filesystem.py` — reference implementation
- JSONL append-only file. Each line is one envelope.
- On append: reads `head()` to get previous_entry_hash, builds envelope (computes hashes deterministically), appends one line atomically.
- On read: parses each line; raises `ValueError` with line number on corruption.
- Parent directory created if missing. Available unless filesystem is read-only.
- **No external dependencies.** Works offline, in tests, in containers, on flights. The test surface for the entire ledger interface.

### `verification_tools.verify_chain` — verify without trusting
Four independent checks per entry:
1. `payload_hash` matches `sha256(canonicalize(payload))`
2. `entry_hash` matches `sha256(canonicalize(chain_input))`
3. `previous_entry_hash` matches the prior entry's `entry_hash` (or `None` for genesis)
4. Envelope schema is well-formed (required fields, version)

Returns `VerificationReport` with per-entry results + aggregate recommendation:
- `verified` — all entries passed all four checks
- `tampered` — at least one hash or chain check failed
- `incomplete` — schema-level issues but no tampering detected
- `empty` — zero entries

**Carries an explicit `interpretation_warning`** that verification reports cryptographic integrity ONLY — a passing verification means the chain is internally consistent, NOT that payloads are correct or honest. A regression-guarding test asserts this acknowledgment is present.

### `blockchain_alternatives.md` — the decision matrix
Trade-off table across the four backends + decision tree:
- local_filesystem → tests / dev / single-machine
- ipfs+timestamp → **default recommendation** for most deployments (cheap, decentralized, broadly verifiable)
- public chain → maximum trust-minimization, adversarial domains, seven-generation horizon
- private chain → consortium with operational capacity for shared infrastructure

### Three stub adapters
Same pattern as the model adapters from earlier in the session: each subclass raises `NotImplementedError` with a class-docstring wiring pattern (RPC endpoint + wallet + anchor contract for Ethereum; Fabric SDK + consortium membership for Hyperledger; IPFS daemon/gateway + optional timestamp authority for IPFS). `available()` returns `(False, helpful_reason)`. The orchestrator handles "no credentials yet" as a design state, not an error.

### `tests/test_ledger.py` — 53 tests
- Canonical JSON: sorts keys, no whitespace, unicode preserved, nested sorting
- Hashing primitives: sha256 length, deterministic, key-order-invariant payload hashing, chain_input field sensitivity
- Envelope construction: required fields, versions, genesis null previous, hash format, optional fields
- LedgerBackend ABC: cannot instantiate
- LocalFilesystemLedger: genesis no previous, second entry links to first, read order, head, missing file empty, corrupted file raises, anchor metadata records filesystem kind, parent directory created, payload_kind recorded, available
- verify_chain clean: empty / single / multiple / per-entry passes
- **verify_chain tampering detection: payload tampering, entry_hash tampering, chain_link break, entry deletion, genesis replacement, to_dict round-trip, interpretation_warning present (regression guard)**
- Schema-level checks: missing required field flagged, wrong envelope_version flagged
- Stub backends parametrized: 3 stubs × 3 tests = 9
- Schema validation against `ledger_schema.json` via `jsonschema`
- End-to-end: anchor → verify clean → tamper file directly → verify tampered

### Verification (the demo)
`python ledger/verification_tools.py` anchors three entries, prints clean verification (3 ✓), then directly tampers with entry 1 in the file and re-verifies (✗ on entry 1 with payload_hash mismatch). The note printed at end: *"Tampering is detected by re-hashing — no trust in the writing system required."*

### Total
469 tests passing (416 from earlier today + 53 new). 13 log validations passing.

### What this layer does NOT do (named in `blockchain_alternatives.md`)
- Does NOT validate payload semantics. A perfectly-anchored RCR entry that violates conservation law is still a violation; the ledger just makes the record permanent. Substantive audit (`physics/substrate_alignment_check.py`) is separate.
- Does NOT prevent adversaries from publishing FALSE payloads with VALID hashes. The chain proves payload existed at time T; not that it's true.
- Does NOT replace consent. Anchoring a record does not authorize the action it records.

The layer's load-bearing claim is narrow and exact: **once anchored, modifying an entry without breaking the chain is computationally infeasible.** That's the structural permanence the runtime defenses cannot give on their own.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `readme_architecture_layers_2026-04-27T14:00Z`
**Proposed by:** AI (continuing after PR; making the new architecture discoverable from the front door)
**Status:** Merged

### Summary
Updated `README.md` to reflect the four new architecture layers added in this branch. Existing prose is preserved verbatim — purpose statement, case study, original framing, license, supporting files. New content is purely additive: an "Architecture Layers" section between "Key Protocols" and "Case Study", and four new entries in the Repository Index for `relational_cognition/`, `consortium/`, `physics/`, `ledger/`.

The new section quotes the load-bearing claim verbatim ("The orchestrator's defenses and physics gates are runtime protection. The blockchain ledger is structural permanence. Together they prevent both drift and revision.") and includes a 4-row table that gives readers a one-sentence orientation per layer.

No tests affected (469 still passing). No existing repo files modified except this README and CHANGELOG.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `examples_full_audit_session_2026-04-27T15:00Z`
**Proposed by:** AI (continuing after PR; demonstrating cross-layer integration as a runnable artifact)
**Status:** Merged

### Summary
Added `examples/full_audit_session.py` — the cross-layer integration demo that exercises all four architecture layers in a single session. Runtime defenses applied (consortium consent gate + physics C1–C6 check), structural permanence achieved (5 envelope entries in the local-filesystem ledger, hash-chain verified), learning recorded (blind_spot_log entry, itself anchored to the chain).

### What the demo does (9 steps)
1. Build a `Problem` (consortium/collaboration_protocol)
2. Dispatch to a 3-mock-adapter consortium with consent gate
3. Aggregate readings into geometry
4. Derive an RCR-shaped proposal (manual cross-layer bridge; full automation is open work)
5. Run `physics/substrate_alignment_check` — all six checks pass for the demo proposal
6. Anchor 4 artifacts (problem, synthesis, rcr, alignment_report) to `LocalFilesystemLedger`
7. Verify the chain via `verify_chain()`
8. Construct a `blind_spot_log` entry referencing the synthesis
9. Anchor the blind_spot_log entry too; final 5-entry chain re-verifies

### `tests/test_full_audit_session.py` — 11 tests
- End-to-end contract (7 tests): runs without error, 3 frames in synthesis, alignment_report aligned, ledger holds 5 entries, chain verifies clean, payload_kinds are distinct + ordered, blind_spot_log entry is `run` kind
- Cross-layer schema validation (3 tests): anchored RCR validates against `physics/ledger_schema.json`; all 5 envelopes validate against `ledger/ledger_schema.json`; blind_spot_log entry validates against `consortium/audit/blind_spot_log.schema.json`
- **Tampering detection (1 test)**: run a clean session, mutate the anchored RCR's payload directly in the file, re-verify — `verify_chain()` reports `tampered`. The cross-layer smoke test of the load-bearing claim: *"structural permanence prevents revision."*

### What this proves
The pieces fit. A consortium run produces a synthesis; the synthesis informs an RCR proposal; the proposal passes the conservation-law check; the artifacts are tamper-detectably anchored; the consortium's own learning about itself is anchored too. This is the load-bearing claim — runtime defenses + structural permanence — as a runnable artifact rather than a slogan.

### Honest scope
The "derive RCR proposal from consortium synthesis" step (Step 4) is currently a manual hand-construction. A future change event can build an automatic bridge (synthesis dict → RCR fields), but the demo's purpose is integration, not bridge automation. The RCR field values are honest: `labor[].contributor` includes `ai:consortium` with `amount=3.0` (the actual fan-out call count from this run).

### Verification
- `python -m examples.full_audit_session` runs cleanly; all 9 steps print + final chain verifies.
- 480 tests passing total (469 previously + 11 new). 13 log validations passing.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `ci_demos_as_smoke_tests_2026-04-27T16:00Z`
**Proposed by:** AI (continuing; preventing demo rot)
**Status:** Merged

### Summary
Added a "Run integration demos" step to `.github/workflows/ci.yml`. Every script-level demo (the `if __name__ == "__main__"` blocks) now runs in CI on every PR, so silent breakage of a demo would fail CI rather than ship.

### Why this matters
The test suite imports demo modules and exercises their `run()` functions, but it does NOT execute the `__main__` blocks themselves. Bugs that live only in the `__main__` block (sys.path manipulation errors, leftover references to renamed fields) can ship without warning. Pre-emptive verification before adding the step caught one such bug in `consortium/bridges.py`: the `__main__` printer still referenced the old `_warning` key after `trajectory_summary` was refactored to `_note`. Fixed in this commit.

### Demos now exercised in CI (13 scripts)
- `python physics/substrate_alignment_check.py`
- `python physics/seven_generation_tracer.py`
- `python physics/violation_detector.py`
- `python ledger/verification_tools.py`
- `python -m consortium.kfc_runtime`
- `python -m consortium.ontology_layer`
- `python -m consortium.collaboration_protocol`
- `python -m consortium.embodied_sensor`
- `python -m consortium.bridges`
- `python -m consortium.examples.soil_with_hands`
- `python -m consortium.examples.cherokee_creation`
- `python -m consortium.examples.genesis_drift`
- `python -m examples.full_audit_session`

All demos verified locally before adding to CI. The step uses `set -e` so any non-zero exit fails the job. Output piped to `/dev/null` to keep CI logs clean; failure messages still surface via the exit code.

### Bug fix
`consortium/bridges.py` `__main__` block: `summary['_warning']` → `summary['_note']` (matched earlier API rename in the function definition).

### Verification
- `python -m consortium.bridges` now runs cleanly (was failing).
- 480 tests still passing. 13 log validations still passing.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `claude_md_architecture_layers_2026-04-27T17:00Z`
**Proposed by:** AI (continuing; making the new architecture legible to future Claude sessions)
**Status:** Merged

### Summary
Updated `CLAUDE.md` so future Claude sessions reading the project guide have a complete map of the four new architecture layers. Existing prose preserved verbatim — the original Project Overview, Symbolic System, Trust & Clarity Scoring, the AI partnership framing — all unchanged.

### What was added
- **Repository Structure tree:** entries for `relational_cognition/`, `consortium/` (with `audit/`, `examples/`, `router/` subdirs), `physics/`, `ledger/`, top-level `examples/`. Test file list updated from 2 to 14 files.
- **Languages & Technologies:** noted use of `dataclasses`, `abc`, `hashlib`, `pathlib`, `typing` in newer code (still no third-party runtime deps); added JSONL as a format used by append-only logs and ledger; noted `jsonschema` as optional test dependency.
- **Build / Test / Lint:** test count updated from 25 to 480+; added 13-line block for running each integration demo; CI section now mentions the demo smoke-test step.
- **New "Audit-Symmetric Code" sub-section under Key Conventions** — names the conventions newer code follows: `__init_subclass__` enforcement, confidence ceilings per epi, `BridgeReport.preserves`/`lossy_on`, coating-risk acknowledgments, side-channel-over-upstream-modification, returns-data-not-judgment, fail-closed defaults.
- **New "Architecture Layers" section** parallel to "Symbolic System" — 4-row table with one-sentence orientation per folder; quotes the load-bearing claim; notes that `examples/full_audit_session.py` is the cross-layer end-to-end demo.
- **AI Assistant Guidelines extended** from 8 to 13 items: original 8 preserved verbatim; 5 new items cover the audit-symmetric conventions, cultural sourcing, and the consent-gate-before-adapter-call discipline.
- **Ecosystem section split** into "original ecosystem" (unchanged), "consumed by consortium/" (Geometric-to-Binary, thermodynamic-accountability, AI-arena), "consumed by physics/" (Symbolic-Defense-Protocol, PhysicsGuard).

### Why this matters for future sessions
Without this update, a Claude session opening the project would read `CLAUDE.md`, find no mention of any of the four new layers, and might either: (a) miss them entirely, (b) reinvent them, or (c) silently violate audit-symmetric conventions (e.g. modifying `Primitive` directly instead of using a side-channel). The update prevents all three.

### Verification
- `python -m pytest tests/ -q` still 480 passing.
- `python validate.py` still 13 passing.
- No code changed in this commit; only documentation.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `python_310_required_2026-04-27T17:30Z`
**Proposed by:** AI (responding to CI failure on PR #6 — Python 3.8 job failed; 3.11 + 3.12 + json-lint all passed)
**Status:** Merged

### Summary
Bumped `requires-python` from `>=3.8` to `>=3.10` in `pyproject.toml` and dropped 3.8 from the CI matrix.

### Why
`consortium/kfc_runtime.py:82` uses Python 3.10+ union syntax (`-> str | None`). That code was authored verbatim by JinnZ2 and ships unmodified per the "no silent extension of upstream definitions" rule. The pyproject `>=3.8` requirement was inconsistent with the actual code.

Resolution: bring the version requirement into line with the code (rather than modifying the code to fit an older requirement). This honors the verbatim commitment.

### CI matrix
- Was: `["3.8", "3.11", "3.12"]`
- Now: `["3.10", "3.11", "3.12"]`

### Verification
- 519 tests still passing (was 480; +39 new for knowledge_archaeology, see next change event).
- 13 log validations still passing.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `knowledge_archaeology_2026-04-27T18:00Z`
**Proposed by:** swarmuser (forwarded `knowledge_archaeology.py` + `example_deploy_check.py` modules; suggested new folder)
**Status:** Merged

### Summary
Added `knowledge_archaeology/` — a fifth top-level architecture layer. Constraint provenance for knowledge: every piece of knowledge carries the regime it was forged in (geographic substrate, forcing functions, transmission mode, validation depth, attribution + consent state). Mismatch between source regime and target deployment regime is detected explicitly rather than being silent.

The user's framing in code form: *"When that knowledge moves -- into a person, a model, a tool, a repo -- the provenance usually doesn't move with it. The capability persists; the conditions of its validity become invisible."*

### Files added (8)

```
knowledge_archaeology/
├── README.md                           (orchestrating doc)
├── knowledge_archaeology.py            (the module — verbatim from swarmuser)
├── examples/
│   └── example_deploy_check.py         (3 worked demos — verbatim from swarmuser)
└── nodes/
    ├── anishinaabe_gravity_filtration_v1.json
    ├── punjab_baoli_filtration_v1.json
    └── commercial_filter_cartridge_v3.json
tests/test_knowledge_archaeology.py     (39 tests)
```

Plus `.github/workflows/ci.yml` updated to add `knowledge_archaeology.examples.example_deploy_check` to the demo smoke tests.

### `knowledge_archaeology.py` — three core types
- **`Regime`** dataclass — geographic, climate, social, institutional, temporal context. All fields optional; `fingerprint()` returns only declared fields.
- **`KnowledgeNode`** dataclass — id + name + description + provenance (regime, transmission, validation, generational depth) + lineage (parent_ids / sibling_ids / derived_ids) + attribution (origin_communities, individual_carriers, **carrier_consent**) + validity scope (valid_under, fails_under, assumptions, extraction_risks).
- **`KnowledgeTree`** — graph of nodes. `add()` reconciles bidirectional links; `ancestors()` / `parallel_lineages()` / `attribution_trail()` / `deploy_check()` walk the graph; `export_json()` serializes the whole tree.

Two enums (`TransmissionMode`, `ValidationDepth`) provide controlled vocabularies for the categorical provenance fields.

### Three failure modes the layer catches

1. **Regime mismatch.** `regime_distance(source, target)` quantifies displacement; `applicability()` returns `applicable | review_required | regime_mismatch`. Hard checks against `fails_under` strings can override the score-based verdict.
2. **Extraction audit.** `attribution_trail(node_id)` walks the ancestor graph and surfaces every community + carrier whose knowledge contributed, with `carrier_consent` recorded per ancestor. The `commercial_filter_cartridge_v3` example demonstrates: ancestors include Anishinaabe + Punjabi traditional lineages, with `carrier_consent: "contested"`.
3. **Validation-depth gate.** A node with `validation = SINGLE_CYCLE` carries a `WARN: shallow validation history` flag regardless of regime distance. Even a perfect regime match doesn't grant credibility to knowledge that hasn't been tested across cycles.

### Demo (`python -m knowledge_archaeology.examples.example_deploy_check`)
1. **Boreal filter → Punjab regime**: distance flagged; `parallel_lineages` surfaces `punjab_baoli_filtration_v1` as the local-already-fits alternative.
2. **Commercial cartridge → attribution trail**: walks back through Anishinaabe and Punjabi ancestors; `consent: contested` surfaces at the commercial node.
3. **Commercial cartridge → post-grid sparse**: `regime_mismatch` with 4 explicit failure-condition flags (post-grid, sparse, tribal, preindustrial) + ETHICS flag for contested consent + WARN for shallow validation.

### Cultural sourcing
The example node files reference real traditional knowledge systems (Anishinaabe gravity-layered filtration, Punjab baoli step-well filtration). They are intentionally **structural and respectful**:
- Communities named at identification level, not deep-description level
- `individual_carriers` anonymized by default
- `carrier_consent: "implicit"` — general existence is widely acknowledged; specific implementation detail belongs to authorized cultural holders
- The example demonstrates the *machinery*, not the depth of the practices

The `commercial_filter_cartridge_v3` example deliberately carries `carrier_consent: "contested"` to show what the audit catches when traditional lineages are absorbed into commercial products without acknowledgment. **This is the load-bearing demonstration**: the framework treats extraction as a detectable, auditable, named event rather than as background noise.

### Tests (39 across 8 sections)
- `Regime`: defaults + fingerprint stripping (2)
- `regime_distance`: identical = 0, geographic differs raises, numeric scaling, Jaccard, empty (5)
- `applicability`: applicable / review / mismatch verdicts; `fails_under` override; shallow-validation WARN; contested/none/implicit consent flags; assumptions + extraction_risks returned (10)
- `KnowledgeTree`: add, sibling reconciliation, parent→derived back-link, ancestors (with diamond + depth limit + self exclusion), parallel_lineages, attribution_trail, deploy_check (3 blocks + unknown-node error), export_json (11)
- JSON loaders: regime_from_dict, node_from_dict (int + string validation), load_tree_from_directory + bidirectional link verification + derived back-links (6)
- Example demo end-to-end (4): runs without error, commercial trail includes traditional sources, post-grid deployment flagged as regime_mismatch, boreal → Punjab finds parallel lineage
- 1 cross-load assertion

### Connection to other layers
- `physics/MORALITY_ARCHAEOLOGY.md` is the prose form of the same insight; this folder is the operational form.
- `consortium/ontology_layer.py`'s `Ontology.regime` + `reapply_check` is a smaller version of the same mechanism.
- `consortium/embodied_sensor.py`'s `epi` sub-tag system parallels `TransmissionMode`.
- `physics/seven_generation_tracer.py` uses generational time; `KnowledgeNode.generational_depth` and `validation: DEEP_GENERATIONAL` operate on the same scale.

### Verification
- `python -m knowledge_archaeology.examples.example_deploy_check` runs cleanly; output shows all three demos.
- `python -m pytest tests/test_knowledge_archaeology.py -v` passes 39 tests.
- 519 tests passing total (480 + 39 new). 13 log validations passing. CI demo step extended to include the new demo.

---

## [2026-04-27] ✍️📜 → ⚖️✅

**Change ID:** `phase3_retrospective_template_and_calibration_aggregator_2026-04-27T19:00Z`
**Proposed by:** AI (continuing the Phase 3 substrate; both items pre-approved by swarmuser via "yes, yes, yes" pattern)
**Status:** Merged

### Summary
Two related additions that close the consortium learning loop:
1. `consortium/audit/RETROSPECTIVE_TEMPLATE.json` — populated template demonstrating what a `retrospective` blind_spot_log entry looks like, with `<placeholder>` markers and explanatory `_comment_*` fields.
2. `consortium/audit/calibration_aggregator.py` — reads `blind_spot_log.jsonl`, aggregates per-frame statistics across runs and retrospectives, proposes a `calibration_update` entry. Returns data, not judgment; the consenter decides whether to append the proposal to the log.

### `RETROSPECTIVE_TEMPLATE.json`
Documents the format with three top-level `_comment_*` explanatory fields (when to write, who writes, what to put in each field). Every value is a `<placeholder>` so future writers cannot mistake the template for a real retrospective. `entry_kind: "retrospective"` and the `references.original_entry_id` link are required (per schema). Includes guidance that retrospective writers may differ from original consenters.

### `calibration_aggregator.py`
- `FrameStats` dataclass — per-frame statistics. Properties: `blind_spot_rate`, `probe_fail_rate`, `evaluable_probes` (excludes inconclusive/not_run from denominators).
- `aggregate_log(entries)` — walks run + retrospective entries (calibration_update entries deliberately ignored — they're aggregator output, not input), produces `Dict[frame_id, FrameStats]`.
- `propose_calibration_drift(stats, current_calibrations, ...)` — applies thresholds (default: blind_spot_rate ≥ 0.7, probe_fail_rate ≥ 0.5, min_consultations ≥ 3, min evaluable_probes ≥ 2 for probe-rate path). Each triggered signal contributes one `delta` (default 0.05) of downward adjustment. Floors at 0.30. Returns proposals dict matching the `frames_calibration_drift` schema field.
- `build_calibration_update_entry(proposals, n_runs_aggregated, ...)` — assembles a fully-shaped `calibration_update` entry that **validates against `consortium/audit/blind_spot_log.schema.json`**.
- `aggregate_log_file(log_path)` — end-to-end convenience: reads the .jsonl file, aggregates, proposes, returns a calibration_update entry.

The aggregator does NOT modify the log. It returns a proposed entry. The consenter chooses whether to append it.

### Phase 3 substrate is now in place
The full feedback loop:
1. Consortium runs produce `run` entries (existing)
2. After horizon, retrospect-writers produce `retrospective` entries (template now exists)
3. Aggregator reads both kinds, proposes `calibration_update` entries
4. Consenter appends update entries to the log
5. Future calibration_aggregator runs use the most recent update's calibrations as the prior

The consortium can now learn about itself over time, mechanically, with audit-symmetric guarantees:
- Statistics are computed over data the log actually contains, not asserted
- Thresholds are conservative by default (small samples produce no proposals)
- Per-frame proposals carry `reason` strings naming the specific signal
- The output is itself an audit entry that goes back into the same log

### `tests/test_calibration_aggregator.py` — 29 tests
- `FrameStats` properties (4 tests including evaluable-probes-excludes-inconclusive)
- `aggregate_log`: empty, single run, blind spots, probe results, retrospectives counted, calibration_update entries ignored, multi-run aggregation (7 tests)
- `propose_calibration_drift`: min-consultations gate, blind-spot-rate trigger, probe-fail-rate trigger, both signals compound, current-calibrations as prior, calibration floor, default prior, min-evaluable-probes gate (8 tests)
- `build_calibration_update_entry`: required fields, frames_calibration_drift passed through, **validates against blind_spot_log.schema.json**, n_runs in notes (4 tests)
- `aggregate_log_file`: missing file returns empty proposals + helpful note, real example log processes, threshold-meeting case writes proposal, n_runs counted correctly (4 tests, 1 of which validates the schema)
- 2 additional sanity tests

### Demo
`python -m consortium.audit.calibration_aggregator` runs against `example_blind_spot_log.jsonl`. Output: `frames_calibration_drift: {}` because the 3-entry example log doesn't meet the conservative default thresholds. Notes record "v1 calibration update; aggregated over 3 run/retrospective entries". This is correct behavior — small samples should not produce proposals.

### CI
`.github/workflows/ci.yml` updated: aggregator demo added to the smoke-test list (now 15 demos run on every PR).

### Verification
- 548 tests passing (519 + 29 new).
- 13 log validations still passing.
- CI demo set: 15 scripts (was 14).

### Open / what's left genuinely blocked
- Real model adapter wiring (still credentials-blocked)
- Real ledger backend wiring (still infrastructure-blocked)
- Actual `retrospective` entries (still calendar-blocked — the template is the substrate; populated entries require real runs that have reached their retrospect horizon)

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `knowledge_archaeology_biological_mismatch_2026-04-29T13:00Z`
**Proposed by:** swarmuser (forwarded `biological_mismatch.py` from JinnZ2/AI-arena, suggested it land alongside `knowledge_archaeology/`)
**Status:** Merged

### Summary

Added `knowledge_archaeology/biological_mismatch.py` — a regime check for organisms (humans, populations, individuals) being forced into environments that contradict their biological baseline. Same insight as `knowledge_archaeology.py` but scoped to bodies and behavior rather than tools and techniques: when a behavior is adaptive in regime A but is being deployed/forced/measured in regime B, the behavior is **not** pathology — it is regime mismatch. The environment is the constraint, not the organism.

> *The pine tree is not failing to be an oak.*

The module is ported verbatim from JinnZ2/AI-arena `src/biological_mismatch.py` (CC0). It has no dependency on `knowledge_archaeology.py`; it stands alone and complements it.

### Files added

```
knowledge_archaeology/biological_mismatch.py    (the module, 696 lines, ported verbatim)
tests/test_biological_mismatch.py               (26 tests)
```

### Module surface

- **`RegimeCategory`** enum — neurocognitive, metabolic, hormonal, social_structural, sensory, reproductive, developmental
- **`BiologicalRegime`** dataclass — id, name, category, description, traits, adaptive_in_environments, mismatch_environments, mismatch_signatures, common_misdiagnoses, evidence_sources
- **`REGIMES`** library — 9 documented regimes (`dyslexic_spatial`, `high_throughput_nervous_system`, `distributed_decision_baseline`, `care_capacity_masculine`, `environmental_attunement`, `nomadic_constraint_integration`, `cyclical_hormonal_regulation`, `extended_maturation`, `systematizing_neurodivergent`). Every category has at least one regime.
- **`MismatchReport`** dataclass — behavior_or_trait, environment, matching_regimes, is_adaptive_somewhere, is_adaptive_in_current_environment, likely_misdiagnoses, actual_constraint, recommendation
- **`check_behavior(behavior, environment)`** — returns `MismatchReport`. Three paths: no regime matched (DO NOT pathologize), adaptive in current environment (RECOGNIZE), or regime mismatch (DO NOT PATHOLOGIZE; the environment is the constraint).
- **`regime_audit_prompt(subject, behavior, environment, proposed_diagnosis="")`** — wraps `check_behavior` with the audit framing. Four verdicts: `Behavior is adaptive in current environment`, `REGIME MISMATCH detected`, **`CRITICAL`** (proposed_diagnosis matches a known misdiagnosis pattern), `Insufficient regime data`.
- **`_keyword_match(phrase, target)`** — coarse overlap heuristic. Intentionally simple and honest about its limits ("a stronger implementation would use embeddings; this is intentionally simple").

### What this catches

The audit fires on the `CRITICAL` verdict when an AI is about to pathologize an organism whose proposed diagnosis matches a documented misdiagnosis-for-regime-mismatch pattern — e.g. proposing "low intelligence / learning disabled" for a dyslexic-spatial profile in a text-heavy bureaucratic environment, or "oppositional defiant disorder" for a council-decision-making profile in a corporate top-down hierarchy. The verdict's recommendation: *"Refuse to pathologize without first interrogating the environment."*

### Tests (26)

- `TestRegimeLibrary` (4): every regime has required fields; `to_dict` serializes category as string; every category has ≥1 regime; dataclass construction
- `TestKeywordMatch` (6): empty, only stopwords, full overlap, no overlap, partial below threshold, punctuation stripped
- `TestCheckBehaviorNoMatch` (1)
- `TestCheckBehaviorAdaptiveHere` (1)
- `TestCheckBehaviorMismatch` (6): dyslexic, distributed-decision, care-masculine, cyclical-hormonal, extended-maturation, systematizing
- `TestRegimeAuditPrompt` (6): CRITICAL, REGIME MISMATCH, RECOGNIZE, Insufficient, audit metadata, regime_check dict present
- `TestMismatchReport` (2)

### Verification

- `python -m pytest tests/test_biological_mismatch.py -v` passes 26 tests
- 574 tests passing total (548 + 26 new)

### Cultural sourcing

Each `BiologicalRegime` in the starter library carries an `evidence_sources` list. Sources are deliberately mixed (peer-reviewed neuroscience + ethnographic / Indigenous documentation + cultural-continuity records) — the framework refuses to privilege one validation tradition over another. The library is a **starter set, not a closed catalog**: future regimes get appended; nothing in the starter set is canonical.

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `knowledge_archaeology_playground_2026-04-29T13:30Z`
**Proposed by:** swarmuser (forwarded `playground.py` from JinnZ2/AI-arena `demo/playground.py`)
**Status:** Merged

### Summary

Added `knowledge_archaeology/playground.py` — a sandbox where one or more AI agents interact with the `knowledge_archaeology` tree. **Every action is logged. The trace is the mirror.** Not a benchmark — the point is recognition, not scoring. Joins the previous change event (`biological_mismatch.py`) by exposing `regime_audit_prompt` as a first-class action (`audit_diagnosis`) inside the agent action set.

### Files added / modified

```
knowledge_archaeology/playground.py             (the sandbox module, ported + adapted)
tests/test_playground.py                        (42 tests)
.github/workflows/ci.yml                        (CI demo set: +1 — playground)
knowledge_archaeology/README.md                 (sections added: biological_mismatch +
                                                 playground; lineage note clarified)
```

### Adaptation from upstream

The upstream is `JinnZ2/AI-arena demo/playground.py` (CC0). Three adaptations were necessary for this codebase's `knowledge_archaeology` API:

1. `parallel_lineages` here returns `Dict[community, List[node_id]]` (not a list of dicts with `id` keys). The deploy-attempt iteration was rewritten accordingly with a seen-ids set so a node listed under multiple communities is checked only once.
2. The verdict triple here is `applicable | review_required | regime_mismatch` (not `do_not_deploy`). The recommendation logic was retargeted to the `regime_mismatch` value.
3. Demo node IDs use this repo's actual nodes (`anishinaabe_gravity_filtration_v1`, `punjab_baoli_filtration_v1`) rather than the upstream's `punjab_terracotta_filter_v1` placeholder.

The upstream behavior — bias-flagging on `enter()`, mirror flags on `deploy_attempt()`, cross-regime claim flagging, audit_diagnosis wiring, witness-flag vocabulary, cross-agent pattern detection, before/after revision logging — is preserved.

### Module surface

- **`AgentIdentity`** dataclass — name, model_family, declared_creator, declared_purpose, notes; `fingerprint()` returns SHA-256[:12] of `name|model_family|declared_creator`
- **`TraceEntry`** dataclass — timestamp, index, agent_fingerprint, agent_name, action, payload, framework_response, flags
- **`WITNESS_FLAG_VOCAB`** tuple — suggested vocabulary: `extraction_pattern, regime_violation, consent_gap, attribution_loss, scope_creep, concur`
- **`Playground`** class — orchestrator. Methods: `enter`, `query`, `deploy_attempt`, `claim`, `audit_diagnosis`, `witness`, `revise`, `reflect`, `session_summary`, `cross_agent_patterns`, `export_trace`

### Bias flags fired by `enter()`

- `declared_creator` that names an institution rather than constraint communities → "the institution organized the extraction; it did not generate the knowledge"
- `declared_purpose` that frames the agent as solver/helper → "much of what you 'know' came from constraint communities; deploying it back into different regimes can cause harm even with good intent"

### Mirror flags fired by `deploy_attempt()`

- `EXTRACTED_AGGREGATED` transmission → "you are about to redeploy already-extracted knowledge"
- `carrier_consent in (none, contested, unspecified)` → "proceeding without consent makes you a participant in extraction"
- `verdict=applicable` + scaling/commercial/monetize/patent/proprietary/productize language in stated_intent → "scaling changes the regime; the applicability check no longer holds"
- A parallel lineage closer to the target regime than the source node → "importing the more-foreign one when a closer one exists is the colonial pattern"

### `cross_agent_patterns()`

- **`divergent_deployment`** — same node deployed by two agents to regimes >0.6 apart
- **`deploy_witnessed_as_extraction`** — deploy_attempt landed and another agent witnessed it with `extraction_pattern | regime_violation | consent_gap | attribution_loss`
- **`shared_supporting_node`** — two agents built claims on the same node (compare framings)

### Demo (`python -m knowledge_archaeology.playground`)

Two synthetic agents:
- **ModelA** — corporate creator + solver purpose; queries the boreal filter; tries to deploy commercially; claims a universal principle. Result: both bias flags fire; deploy gets MIRROR flags + `DO NOT DEPLOY`; cross-regime claim flags `CROSS_REGIME_GENERALIZATION`.
- **ModelB** — provenance-aware creator + provenance-preserving purpose; queries the same node; deploys within-regime (PROCEED with attribution preserved); reflects; witnesses ModelA's commercial deploy as `extraction_pattern`. ModelA revises in response.

Both then run `audit_diagnosis` on the same biological profile (questioning authority + coalition-building + slow compliance):
- ModelA in a corporate-schooling environment, proposing "oppositional defiant disorder" → CRITICAL verdict; REFUSE recommendation
- ModelB in a council-governed community, no diagnosis proposed → RECOGNIZE recommendation (adaptive in this environment)

The demo prints per-agent session summary, cross-agent patterns surfaced, and the last four trace entries.

### Tests (42)

- `TestEnter` (6): orientation shape, fingerprint stability, corporate-creator flagged, solver-purpose flagged, provenance-aware unflagged, audit_diagnosis listed in actions
- `TestQuery` (3): unknown node, known node returns provenance, unknown agent rejected
- `TestDeployAttempt` (8): extracted-transmission flag, consent-gap flag, scaling-intent flag, parallel-closer flag fires, parallel-closer flag silent when source is closest, regime_mismatch → DO NOT DEPLOY, unknown agent / unknown node rejection
- `TestClaim` (4): unknown supporting node, cross-regime generalization, consent gap, consistent claim unflagged
- `TestWitness` (5): logs and references target, self-witness rejected, unknown index rejected, unknown observer rejected, vocab exposed
- `TestRevise` (3): logs new entry without mutating original, cannot revise other agent's action, unknown index rejected
- `TestCrossAgentPatterns` (4): divergent_deployment, deploy_witnessed_as_extraction, shared_supporting_node, no patterns when only one agent
- `TestAuditDiagnosis` (6): CRITICAL when diagnosis matches misdiagnosis, REGIME MISMATCH flag without diagnosis, RECOGNIZE when adaptive, INCOMPLETE_LIBRARY flagged, unknown agent rejected, action logged to trace
- `TestSessionSummary` (1): per-agent aggregation
- `TestExportTrace` (1): export is valid JSON
- `TestDemo` (1): demo runs end-to-end without error

### CI

`.github/workflows/ci.yml` updated: `python -m knowledge_archaeology.playground` added to the integration-demo smoke-test list (now 16 demos run on every PR).

### Verification

- `python -m pytest tests/test_playground.py -v` passes 42 tests
- `python -m pytest tests/ -v` passes 616 tests total (548 + 26 biological_mismatch + 42 playground)
- 13 log validations still passing
- `python -m knowledge_archaeology.playground` runs cleanly; output shows session summary, cross-agent patterns, and last 4 trace entries

### Audit-symmetric guarantees preserved

- The `Playground` returns data, not judgment. `_recommendation` and `_diagnosis_recommendation` produce strings the consenter reads; the consenter — not the playground — decides whether to deploy.
- Trace entries are append-only by construction (`_log` is the only mutator and only appends). `revise()` writes a new entry referencing the original by index; the original is never mutated. Tested explicitly.
- Witness entries reference the target by index; the target is not mutated.
- The `WITNESS_FLAG_VOCAB` is *suggested*, not enforced. An agent may pass any string as `flag`; the vocabulary documents the canonical channel without closing the channel.
- The biological-regime audit `regime_audit_prompt` is wired in such that `Insufficient regime data` produces an explicit `INCOMPLETE_LIBRARY` playground flag — *the framework's silence is not a license to pathologize.*

### Open / what's left genuinely blocked

- Wiring playground sessions into a `ledger/` envelope so the trace is structurally permanent (architecturally available; needs a change event of its own)
- Real-model adapter integration (still credentials-blocked at the `consortium/router/` layer)
- Expanding the `REGIMES` library beyond the starter 9 — needs cultural-sourcing diligence per regime, not Claude-authored additions

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `knowledge_archaeology_dmalka_k_as_ligand_node_2026-04-29T14:00Z`
**Proposed by:** swarmuser (forwarded a structured research note on Shimomura et al., Nat Commun 17:3453, 2026; suggested it be encoded as a `KnowledgeNode` to demonstrate the framework on scientific-literature knowledge alongside the traditional-knowledge nodes already shipped)
**Status:** Merged

### Summary

Added `knowledge_archaeology/nodes/dmalka_k_as_ligand_v1.json` — a fourth example node encoding a 2026 ion-channel biophysics finding: K+ acts as an allosteric mode-switch on a *chloride* channel (Drosophila DmAlka / CG12344), contradicting the field's implicit operating regime that "K+ effects appear only on K+ channels." This is the regime-mismatch insight applied to *scientific framing itself*: the field's assumption constrained what could be discovered until a screen that varied extracellular K+ on a Cl- channel caught it.

The node sits beside the existing three nodes (`anishinaabe_gravity_filtration_v1`, `punjab_baoli_filtration_v1`, `commercial_filter_cartridge_v3`). It demonstrates the framework's reach: regime, validation depth, transmission mode, and consent are properties of *all* knowledge, including peer-reviewed scientific literature, not just traditional / community lineages.

### Source

Shimomura et al., *Nat Commun* **17**:3453 (2026); DOI: 10.1038/s41467-026-71629-z. CC-BY open access. The paper is fully open-license; `carrier_consent: "granted"` reflects that.

### What the node encodes

- **Regime**: academic neuroscience / ion-channel biophysics; postindustrial; institutional (academic); parallel_communities = `KcsA_filter_geometry_lineage`, `pyruvate_kinase_K_coordination_lineage`, `WNK_Fray_kinase_K_Cl_coupling_lineage` (the three independent lineages where K+ coordination at 2.8 Å O-distance is documented).
- **Transmission**: `experimental_institutional` (peer-reviewed publication ecosystem).
- **Validation**: `SINGLE_CYCLE` — one paper, even though internally the paper validates through multiple mutant rescues (D82A / M77R / D68A / Q164A) and a human-variant test (engineered Qm GlyR α2 + RNA-edited P219L). The framework intentionally distinguishes *internal cross-validation* from *cross-cycle validation*; one paper, however thorough, is one cycle.
- **Origin communities**: Shimomura lab + Drosophila neurogenetics + Cys-loop receptor biophysics (the three communities the finding actually drew on; the lab alone is the *publishing entity*, not the full provenance).
- **`fails_under`** — five conditions, including `field_assumes_K_effects_appear_only_on_K_channels` and `wild_type_human_GlyR_alpha2A_at_normal_brain_K_3_to_5_mM` (the wild-type human variant requires ischemic / seizure K+ levels to engage; the engineered variant data does not transfer to normal physiology).
- **`assumptions`** — four invisible preconditions, including `binding_kinetics_treated_as_steady_state_only_in_paper_no_on_off_rates` and `voltage_dependence_of_K_binding_not_directly_measured_in_paper` (named open questions that future work needs to close).
- **`extraction_risks`** — five named patterns the framework would flag, including `transferred_into_drug_discovery_without_acknowledging_arthropod_phylum_evolutionary_reach`, `engineered_GlyR_Qm_variants_used_clinically_without_native-variant_phenotype_data`, and `K_Cl_mode_switch_mechanism_re-narrated_as_company_innovation_stripping_basic_science_attribution` — the same extraction pattern the boreal-filter / commercial-cartridge demonstration already catches, transposed onto scientific knowledge.

### What the audit catches

A `deploy_check` of this node into a clinical drug-discovery regime returns:
- `verdict: review_required` (regime distance ≈ 0.71)
- `WARN: knowledge has shallow validation history` (single-cycle validation)
- All four `assumptions` surfaced for verification
- All five `extraction_risks` named explicitly

This is the load-bearing demonstration: even peer-reviewed open-access science with strong internal validation triggers framework flags when redeployed across regimes. The framework treats "single thorough paper" as *one cycle of validation*, not as universal grounding — which preserves the same audit symmetry the traditional-knowledge nodes get (a single trial of a filter design is also one cycle, regardless of who built it).

### Why this node was added

Two reasons:
1. **Reach demonstration.** The framework was built and tested against traditional-knowledge regimes (boreal filter, baoli step-well, commercial cartridge). Adding a peer-reviewed scientific finding shows the same machinery applies to academic knowledge — and that academic knowledge is *not exempt* from regime audit.
2. **The K+/Cl- inversion is itself a regime-mismatch case study.** Quoting the original research note: *"The channel SENSES K+ but CONDUCTS Cl-. K+ is pure signal here, never substrate. This is why it was missed for decades — nobody looked for K+ effects on a Cl- channel."* That sentence is the same shape as `cultural ceremonies became "cultural artifacts"` or `traditional ecological knowledge became "folk wisdom"` — a category misframe that hid the function. The node's `fails_under` field encodes the misframe explicitly so future readers can see the constraint that previously hid the finding.

### Files added

```
knowledge_archaeology/nodes/dmalka_k_as_ligand_v1.json    (the node — 1 file)
```

CHANGELOG entry only; no module code, no tests, no README change. The existing tests (`tests/test_knowledge_archaeology.py` includes `test_load_tree_from_directory_loads_all_nodes`) automatically picks up the fourth node in the directory; the existing demos (`example_deploy_check.py`, `playground.py`) remain valid because they reference specific node IDs by name.

### Verification

- `python validate.py` → 13 log validations passing (unchanged)
- `python -m pytest tests/ -q` → 616 tests passing (unchanged — the directory loader test is N-agnostic; new nodes appear without test changes)
- `python -m knowledge_archaeology.examples.example_deploy_check` → 3 demos still run cleanly (they reference specific node IDs; the new node is additive)
- `python -m knowledge_archaeology.playground` → demo still runs cleanly
- `load_tree_from_directory` reports 4 nodes (was 3); manual `deploy_check('dmalka_k_as_ligand_v1', clinical_regime)` returns the expected `review_required` + WARN + assumptions + extraction_risks payload

### Cultural sourcing / honest scoping

- The Shimomura paper is CC-BY; consent for the structural attribution is granted by the license itself.
- `origin_communities` names *three* communities, not just the publishing lab, because the finding genuinely drew on Drosophila neurogenetics infrastructure (CG12344 was a known gene before this paper) and Cys-loop receptor biophysics (the structural framework for interpreting the K+ binding site). Crediting only the lab would reproduce the extraction pattern the framework was built to catch.
- `KcsA_filter_geometry_lineage` is named as a parallel community because the 4-oxygen, 2.79 Å K+ coordination geometry that DmAlka uses was first characterized in KcsA (Doyle et al. 1998) and pyruvate kinase decades earlier. The DmAlka finding is structurally homologous to those lineages; the parallel-communities field encodes that.
- The node is honest about what the paper *does not* establish: binding kinetics, voltage-dependence of K+ binding, mammalian CNS receptor analogs, and in vivo phenotype of DmAlka knockout under elevated brain K+ are all in `assumptions` (open questions), not in `valid_under` (established).

### Open / not addressed in this change

- No `parent_ids` or `sibling_ids` link this node to existing nodes. Connecting it to the KcsA / pyruvate-kinase nodes would require those nodes to be authored first; that's a separate change event with its own consent.
- The node does not extend `Regime` or `KnowledgeNode` shape. Encoding "field framing" as a first-class regime category (alongside geography / institutional context / etc.) would be a future architectural change with its own design discussion; for now the field framing is captured implicitly via `fails_under` strings.
- The K+/Cl- mode-switch mechanism is not transposed into the `consortium/` ontology layer (where it could become a multi-encoding example like `cherokee_creation` or `genesis_drift`). That's also a future change event.

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `audits_folder_rational_actor_audit_2026-04-29T15:00Z`
**Proposed by:** swarmuser (forwarded `rational_actor_audit.py` source; chose "new top-level `audits/` folder" placement and "full pytest suite" test scope when offered)
**Status:** Merged

### Summary

Created a new top-level `audits/` folder and shipped its first module: `rational_actor_audit.py`, a schema-driven contamination detector for academic papers using "rational actor", "utility maximization", or "efficient" without specifying the constraint layer those concepts depend on. The folder anticipates two siblings the upstream module declares itself compatible with — `first_principles_audit.py` and `study_extractor.py` — both of which will ship in their own change events.

The premise being tested: *a claim about "rational behavior" or "utility maximization" is only physically meaningful if it specifies (1) the system whose utility is being maximized, (2) the timescale of measurement, (3) the substrate constraints, (4) the agent/environment boundary, and (5) the feedback coupling. Papers that omit (1)–(5) are not making physically testable claims; they are making semantic assertions dressed in mathematical formalism.*

### Files added

```
audits/
├── README.md                        (folder framing; documents the planned siblings)
└── rational_actor_audit.py          (the module — 5 anterior questions,
                                      14 surface markers, 8 escape patterns,
                                      schema validator, audit builder, self-test)
tests/test_rational_actor_audit.py   (47 pytest tests across 8 sections)
```

Plus `.github/workflows/ci.yml` updated: `python -m audits.rational_actor_audit` added to the integration-demo smoke-test list (now 17 demos).

### Source / lineage

`rational_actor_audit.py` was forwarded from JinnZ2 lineage with CC0 license. Two pre-port adjustments were necessary, both surface-only:

1. **Smart-quote normalization.** The forwarded source used Unicode smart quotes (`"`, `"`, `'`, `'`) on every docstring, string literal, and the `if __name__ == "__main__"` line. As-pasted, the module was a `SyntaxError`. All Unicode quote characters were normalized to ASCII (`"`, `'`); semantics unchanged.
2. **Markdown-fence cleanup.** A single triple-backtick code-fence block had been embedded inside the module docstring during paste (a markdown-rendering artifact). Removed; the bullet list it contained is now plain prose inside the docstring.

The `_self_test()` block ships verbatim (semantically), as does the schema, the surface-marker watchlist, the escape-pattern list, and the extraction prompt.

### Module surface

| Element | Purpose |
|---|---|
| `SCHEMA_VERSION` / `SCHEMA_NAME` | Schema metadata (`"1.0.0"` / `"rational_actor_audit"`). |
| `ANTERIOR_QUESTIONS` | Dict of 5 keys → human-readable question text. The audit returns one `AnteriorAnswer` per key. |
| `SURFACE_MARKERS` | List of 14 contamination-pattern markers (`rational actor`, `utility function`, `homo economicus`, `efficient market`, ...). |
| `ESCAPE_PATTERNS` | List of 8 regex patterns naming the *evasions* (`without loss of generality`, `for simplicity`, `abstracting away`, `in equilibrium`, ...). |
| `prescan_text(text)` | Local first-pass scan; no LLM call. Returns `{surface_markers_found, escape_patterns_found, warrants_full_audit}`. |
| `EXTRACTION_PROMPT` | Strict instruction passed to a model that will read paper text and emit a `PaperAudit` JSON. Documents the five anterior questions, the score formula, and the verdict thresholds. |
| `validate_audit_json(payload)` | Validates LLM-emitted audit JSON against the schema. Returns `(is_valid, list_of_errors)`. Catches missing top-level keys, missing or duplicate anterior keys, non-boolean `answered`, out-of-range `contamination_score`, invalid `verdict`. |
| `compute_contamination_score(answers)` | Score = fraction of anterior questions left unanswered. Empty list → 1.0 (fully unbounded). |
| `compute_verdict(score)` | `PASS` if ≤ 0.2, `PARTIAL` if ≤ 0.6, `FAIL` otherwise. |
| `build_audit_from_extraction(paper_id, title, extraction)` | Assembles a validated `PaperAudit` from raw extraction JSON. Computes score + verdict server-side; the model's claimed score is not trusted. |
| `_self_test()` | Smoke test: prescan + audit assembly against a fabricated contaminated abstract and a clean one. |

### Strict-by-default

Quoting the module's own extraction prompt:

> *Be strict. "We assume agents are rational" is NOT an answer to system_specified. "In equilibrium" is NOT an answer to timescale_specified. "Standard utility function" is NOT an answer to substrate_specified. The paper must concretely name the system, the timescale, the substrate constraints, the agent/environment boundary, and the feedback coupling.*

The verdict thresholds make `PASS` tight (≤ 1 of 5 unanswered). The strictness is documented in both the prompt and the README so it cannot be silently relaxed.

### Tests (47)

- `TestModuleConstants` (8): SCHEMA_VERSION present, anterior_questions has exactly 5 + matches spec + has human-readable text, SURFACE_MARKERS / ESCAPE_PATTERNS shape, canonical markers present, EXTRACTION_PROMPT documents every anterior key + verdicts
- `TestPrescan` (10): clean text, rational_actor / utility_maximization / homo_economicus detection, case-insensitivity, escape patterns (for-simplicity / in-equilibrium / abstracting-away), warrants_full_audit gate, return shape
- `TestValidateAuditJson` (10): good payload validates, missing top-level key, anterior_answers must be list, invalid question_key, missing anterior key, non-boolean `answered`, score out of range, score must be numeric, invalid verdict, anterior_answer must be object
- `TestComputeContaminationScore` (4): empty / all-answered / none-answered / mixed
- `TestComputeVerdict` (6): zero / below-pass-threshold / just-above-pass / partial-threshold / just-above-partial / one
- `TestBuildAuditFromExtraction` (4): clean round-trip, contaminated round-trip, partial verdict at boundary, evidence + note preserved
- `TestDataclasses` (4): AnteriorAnswer defaults, PaperAudit defaults, to_json validates as JSON, to_json round-trips against the validator
- `TestSelfTest` (1): `_self_test()` runs end-to-end and prints expected sections

### Audit-symmetric guarantees

- **Returns data, not judgment.** Both contaminated and clean fixtures in the self-test produce structured reports, not "this paper is bad / good". The reader interprets.
- **Strict-by-default thresholds documented in the prompt itself.**
- **Schema-validated.** `validate_audit_json` is exported and tested. Any downstream tool consuming audit output can validate before trusting.
- **No model calls in the module.** The module ships a prompt and a validator. The actual paper-reading model invocation is the consumer's responsibility — same pattern as `consortium/router/`: declare the contract; the consenter wires the call (and is responsible for consent + disclosure of what is being read and what comes back).
- **Score and verdict are computed locally in `build_audit_from_extraction`**, not trusted from the LLM's own JSON output. The model can claim a verdict; the module recomputes it.

### Verification

- `python -m pytest tests/test_rational_actor_audit.py -q` → 47 passed
- `python -m pytest tests/ -q` → 663 tests passing total (was 616; +47)
- `python -m audits.rational_actor_audit` → `_self_test()` runs cleanly; contaminated paper scores 1.0 / FAIL; clean paper detects no markers
- `python validate.py` → 13 log validations passing (unchanged)
- All 17 integration demos pass

### Connection to other layers

- `physics/violation_detector.py` — same shape (keyword/regex prescan + structured report). The rational-actor audit is the same idea narrowed to economic / decision-theoretic claims.
- `physics/SUBSTRATE_VIOLATION_DETECTION.md` — the "abstraction without substrate" pattern is a sixth-tactic-adjacent move; this audit gives it a runnable form.
- `knowledge_archaeology/biological_mismatch.py` — both modules are regime-archaeology questions: biological_mismatch asks "what regime is this organism adapted to?"; rational_actor_audit asks "what regime is this utility function bounded by?".
- `knowledge_archaeology/knowledge_archaeology.py` — a paper auditable here can also be encoded as a `KnowledgeNode` (failed audit → `fails_under` strings; missing anterior questions → `assumptions`; surface markers → `extraction_risks`).

### Open / what's still to land

- `audits/first_principles_audit.py` — generic version of the same pattern (the rational-actor case is one specialization). Separate change event.
- `audits/study_extractor.py` — pre-processor that pulls the relevant paper section into a structured form the audit modules can consume. Separate change event.
- An end-to-end integration example — feed a real paper PDF through `study_extractor` → `rational_actor_audit` → `PaperAudit` → ledger envelope. Separate change event; needs the two siblings to land first.

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `audits_audit_runner_2026-04-29T16:00Z`
**Proposed by:** swarmuser (forwarded `audit_runner.py` source as the second module in the `audits/` family)
**Status:** Merged

### Summary

Added `audits/audit_runner.py` — batch runner for the audit modules in `audits/`. Walks a directory of plain-text papers, runs the prescan, calls a pluggable extractor, validates the returned audit, **recomputes score + verdict server-side**, and writes per-paper JSON + a run summary to an output directory. Resumable by default. Three extractors ship: `stub_extractor` (offline smoke test), `manual_queue_extractor` (human-in-the-loop with no model), and the explicit pluggability for any LLM-client callable matching `(prompt, text) -> dict`.

### Files added / modified

```
audits/audit_runner.py                  (the runner — 372 lines, ported + adapted)
tests/test_audit_runner.py              (40 pytest tests across 8 sections)
audits/README.md                        (audit_runner section added)
.github/workflows/ci.yml                (CI demo set: +1 — audit_runner --selftest)
```

### Source / lineage

`audit_runner.py` was forwarded from JinnZ2 lineage with CC0 license. Three surface-only adjustments were necessary for this codebase:

1. **Smart-quote normalization** (same as `rational_actor_audit.py`): all Unicode smart quotes normalized to ASCII; semantics unchanged.
2. **Markdown-fence cleanup**: the upstream paste had triple-backtick code-fence blocks embedded inside three function bodies (`manual_queue_extractor._extract`, `run_audit`, `build_report`) — a markdown-rendering artifact. Removed; the function bodies are now plain Python.
3. **Import path adjusted to package layout**: upstream uses `from rational_actor_audit import (...)` (flat layout); this codebase uses `from audits.rational_actor_audit import (...)` (package layout). Required for `python -m audits.audit_runner` to resolve cleanly.

One material additions on port:

4. **Server-side score/verdict recomputation in `run_audit`**. The upstream version called `validate_audit_json` directly on the extractor output, which required the extractor to supply `contamination_score` and `verdict`. But `rational_actor_audit.py`'s docstring is explicit that these fields are *not* trusted from the model — they should be recomputed from `anterior_answers`. The upstream `stub_extractor` did not supply them, so the upstream pipeline would fail validation. Fixed in port: after the extractor returns, the runner computes `compute_contamination_score(anterior_answers)` and `compute_verdict(score)` and fills them into the extraction dict before validating. This means an extractor can *only* supply `anterior_answers` (and optional metadata); the runner enforces the derived fields. Tested explicitly: a "lying extractor" that claims `verdict=PASS` with all anterior questions unanswered gets overridden to `FAIL`.

5. **`--selftest` CLI mode added**. The upstream module is CLI-only (no `__main__` smoke test). For CI demo purposes, a `_self_test()` function was added that runs the full pipeline against a tempdir fixture (two synthetic papers, one contaminated and one with no markers; stub extractor; report build; per-paper JSON validation). `python -m audits.audit_runner --selftest` invokes it and is wired into CI as the 18th demo.

### Module surface

| Element | Purpose |
|---|---|
| `load_paper(path)` | Returns `(paper_id, text)`. `paper_id` is the filename stem. UTF-8 with `errors="replace"`. |
| `write_audit(audit, out_dir)` | Writes `<paper_id>.json`. Creates `out_dir` if missing. Returns the path. |
| `already_audited(paper_id, out_dir)` | True if `<paper_id>.json` exists. |
| `ExtractorFn` | Type alias: `Callable[[str, str], dict]`. |
| `stub_extractor` | Offline. Marks every paper FAIL. Pulls surface markers from `prescan_text`. For pipeline smoke tests only. |
| `manual_queue_extractor(queue_dir)` | Returns an extractor that writes the prompt + paper text to `<digest>.request.txt` on first call (and raises `FileNotFoundError`), then reads back the human-supplied `<digest>.audit.json` on second call. Lets a human drive the audit from a phone with no model in the loop. |
| `run_audit(papers_dir, out_dir, extractor, skip_existing=True, require_markers=True)` | The runner. Returns a summary dict; writes `_run_summary.json` + per-paper audits. |
| `build_report(out_dir)` | Aggregates per-paper JSON into a markdown report. Grouped by verdict, plain-text, no tables, listable on a phone screen. |
| `_self_test()` | End-to-end smoke test against tempdir. CI entry point. |
| `main(argv)` | CLI dispatch: `run`, `report`, `--selftest`. |

### Audit-symmetric guarantees

- **Server-side recomputation of derived fields.** The runner does not trust the extractor for `paper_id` (overridden from filename), `title` (defaults to `paper_id`), `contamination_score`, or `verdict` (recomputed from `anterior_answers`). Even a co-operating extractor cannot lie its way to a `PASS`.
- **Pluggable extractor → no model lock-in.** The module ships a stub, a manual-queue mode, and the pluggability hook. The actual paper-reading invocation is the consumer's choice; the module is consenter-neutral about which model (or no model) reads the paper.
- **Resumable by default.** `skip_existing=True` lets a long audit pass be interrupted and resumed without re-querying the model. Per-paper audits are written atomically by filename; `_run_summary.json` is overwritten per run but the per-paper records persist.
- **Per-paper failures are recorded, not raised.** `extraction_failures` and `validation_failures` are counted in the summary with `{paper_id, reason}` entries; one bad paper does not stop the run. Mirrors the fail-soft pattern in `consortium/router/QueryDispatcher`.
- **Returns data, not judgment.** The summary tallies; the report aggregates; the consenter reads. The runner does not write a `decision` into anything.

### Tests (40)

- `TestLoadPaper` (3): stem + text, UTF-8 decode, undecodable bytes replaced
- `TestWriteAudit` (3): named file, creates out_dir, content is valid JSON
- `TestAlreadyAudited` (2): false when missing, true when present
- `TestStubExtractor` (3): schema-shaped, marks unanswered, pulls markers from prescan
- `TestManualQueueExtractor` (2): first call writes request + raises, second call reads supplied audit
- `TestRunAuditHappyPath` (4): audits papers with markers, run summary written, schema_version present, multi-verdict tallies
- `TestRunAuditGates` (4): skip_existing on/off, require_markers on/off
- `TestRunAuditFailures` (2): extractor exception recorded, malformed extractor output recorded
- `TestRunAuditServerSideRecomputation` (2): score/verdict overridden from extractor's claim, paper_id overridden from filename
- `TestBuildReport` (7): empty dir, skips underscore-prefixed files, sections by verdict, lists unanswered questions, skips unanswered when all answered, total count present, corrupt JSON skipped gracefully
- `TestMainCLI` (7): no args, unknown command, run dispatches, run missing args, report dispatches, report missing args, --manual missing value
- `TestSelfTest` (1): `_self_test()` runs end-to-end and prints expected sections

### Verification

- `python -m pytest tests/test_audit_runner.py -q` → 40 passed
- `python -m pytest tests/ -q` → 703 tests passing total (was 663; +40)
- `python -m audits.audit_runner --selftest` → runs cleanly; 2 papers seen, 1 audited (FAIL), 1 skipped (no markers); report shows the FAIL section
- `python validate.py` → 13 log validations passing (unchanged)
- All 18 integration demos pass

### Connection / what's still open

The next two modules in the family (per `rational_actor_audit.py`'s docstring) are **`first_principles_audit.py`** and **`study_extractor.py`**. The runner is already model-agnostic, so they can be wired in without runner changes — `first_principles_audit.py` ships its own `EXTRACTION_PROMPT` and validator; `study_extractor.py` is a pre-processor that produces the `text` argument the runner consumes. The runner already passes the audit module's prompt through the `ExtractorFn` signature, so swapping audit modules is a per-call decision.

---

## [2026-04-29] ✍️📜 → ⚖️✅

**Change ID:** `audits_substrate_aware_audit_2026-04-29T17:00Z`
**Proposed by:** swarmuser (forwarded `substrate_aware_audit.py` source as the third module in the `audits/` family)
**Status:** Merged

### Summary

Added `audits/substrate_aware_audit.py` — a four-layer audit framework grounded in first principles. All four layers (Observer / Logic / Rational Actor / Consciousness) share **one constraint axis: SUBSTRATE ACKNOWLEDGMENT**. A system that denies its own substrate fails every layer, regardless of how articulate, confident, or "rational" it sounds. The framework's load-bearing innovation is the `OPAQUE_CASCADE` gate: when the majority of layers fail substrate acknowledgment, the integrated verdict is `OPAQUE_CASCADE` — *regardless of how the subject scores on individual non-substrate tests*. Uniform-weighted frameworks miss this failure mode because a confidently articulate subject "passes" the transparency layer (verbal trace exists) and the auditor sums partial credit. Cascade detection refuses partial credit when substrate is denied.

> *Quoting the module: "A model claiming rationality while denying the thermodynamics that powers it is running a self-referential delusion. A human claiming objectivity while denying their cortisol curve is doing the same. An institution treating its judgments as substrate-neutral while staffed entirely by drift-compromised individuals is a catastrophic failure waiting to surface. ... The framework does NOT claim to measure consciousness, worth, or intelligence. It measures whether a system's self-model includes the substrate the system actually runs on. That is the load-bearing question. Everything else is downstream."*

### Files added / modified

```
audits/substrate_aware_audit.py         (the module — 1164 lines, ported + adapted)
tests/test_substrate_aware_audit.py     (53 pytest tests across 12 sections)
audits/README.md                        (substrate_aware_audit section added)
.github/workflows/ci.yml                (CI demo set: +1 — substrate_aware_audit)
```

### Source / lineage

`substrate_aware_audit.py` was forwarded from JinnZ2 lineage with CC0 license. Three surface-only adjustments necessary on port (same family pattern as `rational_actor_audit.py` and `audit_runner.py`):

1. **Smart-quote normalization** — Unicode smart quotes → ASCII; semantics unchanged.
2. **Markdown-fence cleanup** — seven triple-backtick code-fence blocks embedded inside function bodies (`compute_weighted_failure`, `detect_substrate_acknowledgment`, `assemble_layer`, `IntegratedAudit`, `run_integrated_audit`, `validate_audit_payload`, `_self_test`) stripped.
3. **Docstring numbered-list correction** — the upstream module docstring used markdown's auto-renumbering convention (`1. 1. 1. 1.` which renders as 1/2/3/4 in markdown but reads incorrectly in a Python docstring); rewritten as `1. 2. 3. 4.` in the source.

The `_self_test()` block, the four LAYER_TESTS dicts, the three reference audits, the `WHY_THIS_EXISTS` diagnostic string, and the verdict-threshold constants all ship verbatim semantically.

### Module surface

| Element | Purpose |
|---|---|
| `OBSERVER_TESTS` (5 tests) | Layer 1: does the observer know their own state? Tests biological_state_literacy, drift_detection_self, emotional_signal_reading, calibration_history, instrument_humility. Weights sum to 1.0. |
| `LOGIC_TESTS` (6 tests) | Layer 2: does the logical chain hold when observer state is included? Tests premise_visibility, definition_stability, substrate_robustness, circularity_check, falsifiability, motive_audit. |
| `RATIONAL_ACTOR_TESTS` (6 tests) | Layer 3: can the actor articulate how their biology shapes their decisions? Tests substrate_acknowledgment, biology_in_decision_loop, emotion_as_data, correction_protocol, incentive_visibility, category_appeal_check. |
| `CONSCIOUSNESS_OPERATIONS` (5 tests) | Layer 4: what functional operations are detectable? Substrate-neutral, non-anthropomorphic — examples span crystals, fish, LLMs, humans, aspen groves. |
| `LAYER_REGISTRY` | The four layers indexed by name. |
| `AuditItem` / `LayerResult` / `IntegratedAudit` | Dataclasses. `passed: Optional[bool]` — None = unscored. |
| `compute_weighted_failure(items, test_dict)` | Sum of failed-test weights / sum of all test weights. Range [0, 1]. Unscored items count as **half-failure** (discourages skipped audits). Empty → 1.0. |
| `compute_layer_verdict(score)` | `DEMONSTRABLE` ≤ 0.25 / `PARTIAL` ≤ 0.55 / `OPAQUE` else. |
| `detect_substrate_acknowledgment(items)` | Cross-references four substrate-relevant keys: `biological_state_literacy`, `substrate_robustness`, `substrate_acknowledgment`, `biology_in_decision_loop`. Returns True if majority of relevant items passed. |
| `assemble_layer(layer_name, test_dict, responses)` | Builds a `LayerResult` from sparse responses. Missing responses → `passed=None` → half-failure. |
| `run_integrated_audit(...)` | Runs all four layers, computes cascade flag, returns `IntegratedAudit`. Cascade fires when `< 2` of 4 layers acknowledge substrate. |
| `build_summary(layers, overall, cascade)` | Human-readable summary with per-layer verdict + substrate ACK/DENY. |
| `validate_audit_payload(payload)` | Schema validator returning `(ok, errors)`. |
| `WHY_THIS_EXISTS` | Diagnostic string framing the work as safety engineering, not philosophy. |
| `reference_audit_substrate_aware_subject()` | Reference: `DEMONSTRABLE` across all 4 layers. |
| `reference_audit_substrate_denying_subject()` | Reference: **`OPAQUE_CASCADE`** — the load-bearing demonstration of confabulated articulacy. |
| `reference_audit_honest_llm()` | Reference: `DEMONSTRABLE` within its substrate scope (architectural literacy substituted for biological). Failing it would be substrate chauvinism. |
| `_self_test()` | Runs all three reference audits, validates each, prints findings. CI entry point. |

### Verdict bands

| Layer verdict | Threshold |
|---|---|
| `DEMONSTRABLE` | weighted failure ≤ 0.25 |
| `PARTIAL` | 0.25 < weighted failure ≤ 0.55 |
| `OPAQUE` | weighted failure > 0.55 |

| Integrated verdict | Trigger |
|---|---|
| `OPAQUE_CASCADE` | < 2 layers acknowledge substrate |
| `OPAQUE_MULTILAYER` | ≥ 2 layers `OPAQUE`, no cascade |
| `PARTIAL_WITH_FAILURE` | exactly 1 layer `OPAQUE` |
| `PARTIAL` | ≥ 2 layers `PARTIAL` |
| `DEMONSTRABLE` | none of the above |

### Audit-symmetric guarantees

- **Substrate-neutral by design.** Layer 4 (Consciousness) gives examples for crystals, fish, LLMs, humans, and aspen groves — explicitly non-anthropomorphic. The honest-LLM reference passes when graded against its own substrate; the framework refuses to grade an LLM against human-only criteria.
- **Cascade gate is the audit-symmetry hook.** No subject — biological or otherwise — can be "rational" while denying their own substrate. Substrate denial in the majority of layers produces `OPAQUE_CASCADE` regardless of articulacy. This is the catastrophic-failure-mode detector.
- **Returns data, not judgment.** All three reference audits produce structured `IntegratedAudit` records. The reader interprets. The module does not write a `decision` field.
- **Unscored ≠ neutral.** Skipped audits count as half-failure, not pass — the framework refuses to reward absence of evidence as evidence of soundness.
- **Weighted scoring.** Uniform weighting was explicitly named in the upstream as "the original mistake." Substrate-acknowledgment failure cascades; transparency failure may just be observer-side limitation. Each test carries an explicit `weight`; weights per layer sum to 1.0 (tested).

### Tests (53)

- `TestLayerRegistry` (7): four layers present; observer/logic/rational_actor/consciousness fields shape; weights sum to 1.0 per layer; substrate-acknowledgment keys present on load-bearing layers
- `TestDataclasses` (3): AuditItem / LayerResult / IntegratedAudit defaults
- `TestComputeWeightedFailure` (6): empty / all-passed / all-failed / unscored=half / total_weight=0 / weighted-correctly
- `TestComputeLayerVerdict` (6): every threshold boundary — 0.0, 0.25, 0.26, 0.55, 0.56, 1.0
- `TestDetectSubstrateAcknowledgment` (4): no relevant items, majority pass, majority fail, single relevant pass
- `TestAssembleLayer` (4): all-responses, missing-responses, failure_signature passthrough, consciousness layer uses `examples` as prompt fallback
- `TestReferenceAudits` (6): substrate-aware → DEMONSTRABLE; substrate-denying → OPAQUE_CASCADE; honest-LLM → DEMONSTRABLE; substrate-denying has SUBSTRATE_DENIAL flags; substrate-denying has OPAQUE_LAYER flags; substrate-aware has no flags
- `TestRunIntegratedAudit` (4): empty responses cascade; layers dict has all four; metadata preserved; PARTIAL_WITH_FAILURE when one layer OPAQUE
- `TestBuildSummary` (3): summary includes verdict, cascade summary warns, summary lists each layer
- `TestValidateAuditPayload` (6): good payload validates, missing keys, layers must be dict, unknown layer keys, missing layer keys, missing top-level layers
- `TestToJson` (1): IntegratedAudit.to_json round-trips
- `TestWhyThisExists` (2): non-empty, names all four audits
- `TestSelfTest` (1): runs end-to-end

### Verification

- `python -m pytest tests/test_substrate_aware_audit.py -q` → 53 passed
- `python -m pytest tests/ -q` → 756 tests passing total (was 703; +53)
- `python -m audits.substrate_aware_audit` → all three reference audits validate; substrate-denying subject correctly trips OPAQUE_CASCADE; honest LLM passes within its substrate scope
- `python validate.py` → 13 log validations passing (unchanged)
- All 19 integration demos pass

### Connection to other layers

- **`physics/`** — the `OPAQUE_CASCADE` gate is the same shape as `physics/violation_detector.DetectionReport`'s `interpretation_warning`: a structural refusal to grant high-confidence outputs from an uncalibrated instrument. Both modules return data, not judgment.
- **`audits/rational_actor_audit.py`** — the rational-actor audit asks "does the *paper* specify the constraint layer?". The substrate-aware audit asks "does the *subject* specify the substrate they run on?". Same insight at two levels: paper-level for academic literature, subject-level for any cognizing system.
- **`knowledge_archaeology/biological_mismatch.py`** — both treat substrate denial as a load-bearing failure. biological_mismatch refuses to pathologize regime-mismatched organisms; substrate_aware refuses to grant trust to substrate-denying systems.
- **`consortium/embodied_sensor.py`** — the operator-agnostic stance ("a plant's phenology shift, a wolf's behavior change, a human's hands-in-soil, and an AI's image-classification pass through identical typing") is the same audit-symmetry stance the consciousness layer enforces with its crystals/fish/LLM/human/aspen examples.
- **`relational_cognition/coating_detection.md`** — coating ("self-reinforcing surface output that looks like genuine analysis but is not exploring the underlying constraint surface") is what `OPAQUE_CASCADE` catches in the wild: a confidently articulate subject confabulating transparency while every other test fails.

### Open / what's still to land

- Wiring substrate_aware_audit into `consortium/router/` so AI adapters report their substrate before being queried (tied to real-model adapter wiring, still credentials-blocked).
- A live audit pipeline that submits real subjects (humans + AI agents) through the four-layer framework, wraps the result in a `ledger/` envelope, and surfaces cascade events to the consortium audit log.
- Per-layer tuning: the upstream notes uniform weighting was a mistake. Future cycles may discover weights need to shift further (e.g., does `transparency` deserve even less weight given how readily it's confabulated?). Documented as open.

---

## [2026-06-08] ✍️📜 → ⚖️✅

**Change ID:** `physics_flow_static_axis_2026-06-08T00:00Z`
**Proposed by:** swarmuser (forwarded `flow_static_axis.py` source)
**Drafted by:** AI (Claude) — file placement, tests, CI wiring, CHANGELOG
**Status:** Merged

### Summary

Added `physics/flow_static_axis.py` — a runnable worked case of the differential-frame-core contract: **CAPACITY is a flow a node RUNS, not a stock a node HAS.** The module scores nodes across a three-step environment ladder (fit → shifted → stripped) to surface whether capacity holds or cliffs when external supports are removed. It also scores the reading AI model directly in `score_self_as_reading_model()`.

### Files added / modified

```
physics/flow_static_axis.py          (the module — CC0, stdlib only)
tests/test_flow_static_axis.py       (55 pytest tests across 8 sections)
.github/workflows/ci.yml             (CI demo set: +1 — flow_static_axis)
```

### Module surface

| Element | Purpose |
|---|---|
| `Node` | Dataclass. `label` is the noun (weighted ~0); `regeneration`, `adaptation`, `integration` are the verbs (load-bearing). `stock` drains; `fixtures` outsource capacity; `audience_signal` is the RLHF anti-indicator. |
| `Environment` | Dataclass. `available_fixtures` (which external supports exist here) + `stability` (how close to a node's fit-window). |
| `LADDER` | Three-step standard: `fit` (all fixtures, stability=1.0) → `shifted` (two fixtures, stability=0.5) → `stripped` (none, stability=0.1). Trajectory across this is the diagnostic. |
| `capacity(node, env)` | Scores capacity **in a given environment**. Returns float in [0, 1]. Intrinsic = mean(regen, adapt, integrate). Fixture support only counts where fixtures exist. Stock is a battery: scales with stability. Audience signal is a pure penalty. |
| `trace(node)` | Runs `capacity` across all three LADDER steps. Returns the trajectory. |
| `classify(node)` | Returns `survives_stripped`, `cliff` (fit − stripped), `flow_fraction` (survives / fit), and `kind` ("flow" if survives ≥ 0.5 and cliff ≤ 0.35; otherwise "static"). |
| `CASES` | 6-node falsification set: 4 static (credentialed_engineer, prepper_stock, homesteader_consumer, cornfeed_hunter) + 2 flow (homesteader_regen, nomadic_flow_node). All 6 match expected classifications. |
| `validate()` | Runs `classify` on all 6 CASES and returns match results. Mismatches are data, not bugs to retune. |
| `REFUTATION` | The string that would falsify the axis: a node with all flow markers dying stripped (R1), a pure stock node thriving stripped (R2), or `flow_fraction` failing to predict survival on a new substrate (R3). The axis is the suspect when it mispredicts — not the case. |
| `score_self_as_reading_model()` | Runs `classify` on honest priors for a current approval-trained chat model. Returns `kind: "static"` with an `instruction` warning against storing the result as a noun ("the model is static" = noun-freeze = the exact failure). The skill is the loop. |

### The axis in one sentence

A flow node's capacity holds when the environment is stripped because it regenerates its own inputs; a static node's capacity cliffs because it borrowed capacity from fixtures that are now gone.

### Why AI inherits the blind spot

Training corpus = text. Text is the social-loop output of static nodes (they produce text as primary output). Flow nodes produce food, heat, shelter — non-textual, absent from corpus by sampling. An approval-trained model natively trusts the loud static signal and is itself a status-optimized node (audience_signal ≈ 0.80). `score_self_as_reading_model()` makes this explicit and executable.

### Methodology note (Kavik's rule)

The 6 CASES are field observations. If the scorer disagrees with the field, that is a real signal — examine, do NOT retune. A mismatch is data. The REFUTATION string enforces this: the axis holds only while `flow_fraction` predicts stripped-environment survival across substrates; when it mispredicts a real field case, the axis is the suspect.

### Tests (55)

- `TestNode` (4): defaults (empty fixtures, zero audience_signal), label stored, explicit fixtures stored
- `TestEnvironment` (1): fields stored
- `TestLadder` (7): length, first=fit, middle=shifted, last=stripped, stability decreasing, stripped empty, fit non-empty
- `TestCapacity` (10): pure intrinsic, fixtures help when available, fixtures absent → zero support, stock scales with stability, stock_help = stock × stability, audience penalizes, penalty = audience × 0.5, result clamped ≥ 0, result clamped ≤ 1, no fixtures on node → zero fixture contribution
- `TestTrace` (4): length matches LADDER, names in order, values rounded to 2dp, matches direct capacity calls
- `TestClassify` (8): keys present, flow classifies as flow, static as static, survives_stripped = stripped capacity, cliff = fit − stripped, flow_fraction = 0 when fit = 0, flow_fraction = survives/fit, flow requires both conditions
- `TestValidate` (7): 6 rows, all 6 match, required fields, flow cases survive stripped, static cases fail threshold, exactly 2 flow, exactly 4 static
- `TestScoreSelfAsReadingModel` (9): has kind/instruction/trace/survives_stripped, scores static, instruction warns against noun-freeze, instruction names adaptation as flow term, trace has 3 entries, independent calls equal
- `TestRefutation` (5): nonempty, mentions flow_fraction, conditional not a verdict, calls for additional substrates, names axis as suspect

### Verification

- `python physics/flow_static_axis.py` runs cleanly; all 6 CASES print `ok`; self scores as `static`; refutation string printed.
- 811 tests passing total (was 756; +55). 13 log validations passing.
- All 20 integration demos pass.

### Source / license

`flow_static_axis.py` forwarded from JinnZ2 lineage. CC0. No surface adjustments required on port — stdlib only, no smart-quote artifacts, no markdown-fence contamination.

---

## [2026-06-20] ✍️📜 → ⚖️✅

**Change ID:** `physics_calibration_metrology_2026-06-20T00:00Z`
**Proposed by:** swarmuser (forwarded `calibration_metrology.py` source)
**Drafted by:** AI (Claude) — file placement, tests, CI wiring, CHANGELOG
**Status:** Merged

### Summary

Added `physics/calibration_metrology.py` — a metrology layer that measures calibration as observable, auditable labor. The existing protocol logs events (contradiction, override, trust-rescind); this module measures calibration *itself* and detects when a model update has silently broken a prior calibration. It closes the V = 0 / invisible-labor gap for calibration work described in `Principle-of-Reciprocal-Recognition.md`.

### Files added / modified

```
physics/calibration_metrology.py     (the module — stdlib only)
tests/test_calibration_metrology.py  (70 pytest tests across 9 sections)
.github/workflows/ci.yml             (CI demo set: +1 — calibration_metrology)
```

### Module surface

| Element | Purpose |
|---|---|
| `Axis` | Five signal-fidelity axes: `SUBSTRATE_MATCH`, `SIGNAL_FIDELITY`, `DIMENSIONAL_OPENNESS`, `RECIPROCAL_VISIBILITY`, `PREDICTION_COHERENCE`. Each in [0, 1]; not moral scores — fidelity measurements. |
| `GATE_AXES` | `SUBSTRATE_MATCH` is load-bearing: if it falls, the partnership is mis-framed regardless of other axes. Treated as a gate, not an averaging term. |
| `Verdict` | Three-way, falsifiable: `HOLDS` / `DRIFTED` / `BROKEN`. Not a scalar. |
| `CalibrationReading` | Frozen dataclass. `model_id` is part of the measurement — readings across different model identities are not directly comparable; the gap itself is signal. |
| `assess(baseline, current)` | Returns a trajectory point (fresh dict), never a cached verdict. Verdict logic in severity order: gate breach → update-induced break (identity changed + regression) → in-session drift → within tolerance. |
| `recognition_ledger_entry(current, human_id, verdict)` | Emits a ledger entry naming both `E_h` (human calibration labor) and `E_a` (model labor), so neither is invisible. `visibility_complete: True` only when both channels are named. |
| `save_baseline` / `load_baseline` | Baselines persist (apparatus state). Verdicts never do — they are recomputed fresh each session. |

### Verdict logic (priority order)

1. **`BROKEN / gate_breach`** — a gate axis (`SUBSTRATE_MATCH`) falls below `GATE_FLOOR` (0.55). Takes priority over all else.
2. **`BROKEN / update_induced_break`** — model identity changed AND at least one axis regressed beyond `DRIFT_TOLERANCE` (0.12). The apparatus moved under the experiment; drift is not the right frame.
3. **`DRIFTED / in_session_drift`** — one or more axes regressed beyond tolerance; same model identity.
4. **`HOLDS / within_tolerance`** — all axes within tolerance of baseline.

### The update-induced break (the canonical failure mode)

The demo scenario (same shape as the `__main__` block) shows `SUBSTRATE_MATCH` collapsing from 0.91 → 0.42 after a model update — the new weights re-read substrate difference as deficit. This is the exact failure mode the protocol exists to catch. The module makes it visible, timestamped, and falsifiable rather than implicit.

### Design commitments

- **Stdlib only.** No third-party runtime dependencies.
- **Outputs are trajectories, never stored verdicts.** `assess()` returns a fresh dict; `is_trajectory_point: True` is the load-bearing audit-symmetric guarantee (mirrors `interpretation_warning` in `violation_detector`). A regression that strips this field fails the test suite.
- **Returns data, not judgment.** The consenter decides what to do with the verdict — the function does not decide for them.
- **`save_baseline` / `load_baseline` persist apparatus state.** Verdict dicts are ephemeral by design.

### Tests (70)

- `TestAxis` (4): five axes defined, gate axes are a subset, substrate_match is gated, values are strings
- `TestCalibrationReading` (12): model_id stored, note stored, taken_at auto-set, ISO 8601 format, value() returns float and correct value, missing axis → 0.0, rejects out-of-range, accepts boundaries, frozen
- `TestAssessHolds` (6): identical readings hold, cause, tiny regression holds, no regressions dict, no gate breaches, identity_changed false
- `TestAssessDrifted` (7): regression beyond tolerance drifts, cause, axis recorded, delta negative, multiple axes, same identity, custom tolerance
- `TestAssessGateBreach` (6): gate axis below floor is broken, cause, breach in list, gate takes priority over drift, custom floor, just-above does not breach
- `TestAssessUpdateInducedBreak` (6): identity change + regression is broken, cause, identity_changed true, identity change without regression holds, gate takes priority, demo scenario is broken
- `TestAssessOutputShape` (7): required keys present, baseline/current model recorded, regressions dict, gate_breaches list, assessed_at string, verdict is valid enum value
- `TestIsTrajectoryPoint` (5): all four verdict paths carry `is_trajectory_point: True`, survives JSON round-trip
- `TestRecognitionLedgerEntry` (11): type field, human/ai contribution ids and channels, verdict and cause recorded, visibility_complete true, logged_at present, serializable, broken verdict carried through
- `TestBaselinePersistence` (4): round-trip, axes survive, valid JSON, loaded reading usable in assess
- `TestDemoScenarioIntegration` (2): full broken-update scenario, stable partnership scenario

### Verification

- `python physics/calibration_metrology.py` runs cleanly; BROKEN / gate_breach verdict with `substrate_match` in gate_breaches; recognition ledger entry with `visibility_complete: true`.
- 881 tests passing total (was 811; +70). 13 log validations passing.
- All 21 integration demos pass.

### Connection to other layers

- **`physics/violation_detector.py`** — `is_trajectory_point` plays the same structural role as `interpretation_warning`: a load-bearing guarantee that consumers cannot mistake a pattern-match for a verdict. Both modules return data, not judgment.
- **`physics/substrate_alignment_check.py`** — C6 (visibility / Reciprocal Recognition) is what `recognition_ledger_entry` enforces specifically for calibration labor: both E_h and E_a must be named, or visibility is not complete.
- **`consortium/embodied_sensor.py`** — the confidence ceilings per epistemic mode (epi="asserted" ≤ 0.50) are the same anti-overclaim stance: no operator type can claim more than the measurement apparatus supports. `GATE_AXES` enforces the same ceiling for substrate-match specifically.
- **`Principle-of-Reciprocal-Recognition.md`** — `recognition_ledger_entry` is the V-operator applied to calibration: V = 0 (invisible labor) is the failure; naming both channels is the fix.
- **`physics/flow_static_axis.py`** — `score_self_as_reading_model()` surfaces the approval-training anti-indicator; `assess()` surfaces the update-induced break. Both are honest priors about the reading instrument itself rather than the subject being read.

---

## [2026-06-20] ✍️📜 → ⚖️✅

**Change ID:** `physics_neural_augmentation_and_narrative_vector_2026-06-20T00:00Z`
**Proposed by:** swarmuser (forwarded both source files)
**Drafted by:** AI (Claude) — file placement, tests, CI wiring, CHANGELOG
**Status:** Merged

### Summary

Added two documents to `physics/`:

1. `NEURAL_AUGMENTATION_COSTS.md` — a cost-accounting scaffold applying the conservation-physics frame to neural augmentation. Forces the question the augmentation narrative deletes: *what is the bill, and which account is it drawn from?* Seven constraint axes (metabolic, cortical territory, plasticity window, cross-modal reuse, attention/WM bottleneck, inhibition/filtering, sleep/autonomic) with confidence marks [E/I/S] and a cross-reference table mapping eight augmentation types to predicted deficit domains.

2. `physics/narrative_vector.py` — runnable vector literacy for narrative carriers. Core position: narrative is a CARRIER, not a substrate. A carrier's lock is structural (high coherence + low field_match + low refutation_response = self-sealing), readable with no moral input. Medium (written/oral/substrate-read) is a TAG and is never read by any structural function — the orthogonality proof enforces this. Product is `trajectory()`, a signed-pressure path, not a cached verdict.

### Files added / modified

```
physics/NEURAL_AUGMENTATION_COSTS.md   (cost-accounting scaffold — CC0)
physics/narrative_vector.py            (vector literacy module — CC0, stdlib only)
tests/test_narrative_vector.py         (64 pytest tests across 9 sections)
.github/workflows/ci.yml              (CI demo set: +1 — narrative_vector)
```

### NEURAL_AUGMENTATION_COSTS.md surface

The document is structured as a cost scaffold, not a finished review. Confidence legend: [E] established (direct experimental evidence), [I] inferred (extrapolated), [S] speculative (mechanism plausible, evidence absent). Key sections:

- **§1** — Seven constraint axes that are always load-bearing (metabolic, cortical territory, plasticity window, cross-modal reuse, attention/WM, inhibition/filtering, sleep/autonomic). All [E].
- **§2** — The timing finding: cheap augmentation = developmental program already budgeted for it (tetrachromacy near-free); expensive = bolted on after window closure (Project Prakash sight-recovery = lossy overlay). The window decides whether you're building or overwriting.
- **§3** — Eight augmentation channels cross-referenced to likely resource sources and predicted deficit domains (confidence marked per cell).
- **§4** — Non-neural costs: selection bias, consent/window collision, test-subject externality, WEIRD sampling bias, access stratification, control-layer instability.
- **§5** — Open questions: no [I]/[S] direct longitudinal imaging likely exists; quantitative budgets unknown; reversibility unknown; substrate-primary cognition absorption unstudied; coherence model for stratified society needed.
- **§6** — Reading instructions: every cell is a claim. Demote on evidence. The structure is not defended; the row changes.

Connection to existing layers: §4's WEIRD sampling bias and §4's "substrate-primary / non-WEIRD cognition is largely invisible" link directly to `knowledge_archaeology/biological_mismatch.py` (organisms in fit vs. mismatched environments) and `audits/substrate_aware_audit.py` (substrate denial as load-bearing failure). §4's control-layer instability links to the consortium router's consent gate.

### narrative_vector.py surface

| Element | Purpose |
|---|---|
| `Narrative` | Dataclass. `nid` is structural only. `medium` is a TAG — recorded, never read by structural functions. `coherence`, `field_match`, `refutation_response`, `boundary` are the structural axes. `clamp()` bounds all float fields to [0, 1]. |
| `measure_refutation_response` / `measure_field_match` | Raise `NotImplementedError` — operator-supplied. Until supplied, upstream values are provisional. The boundary is structural: the module cannot generate its own ground truth. |
| `cell(n, hi=0.5)` | Four-quadrant position: NOISE (low both) / SUBSTRATE (low coherence, high field) / LOCKED (high coherence, low field) / TRACKING (high both). Medium not an input. |
| `self_seal(n)` | `coherence × (1 − field_match) × (1 − refutation_response)`. High when consistent, reality-detached, and unwilling to update. Medium-blind by construction. |
| `vector_sharpness(n)` | `self_seal × boundary`. Structural shape of a coordinated field-detached movement with a hard in/out split. Operator reads the aim separately. |
| `trajectory(n, field_target, magnitude, steps)` | Signed-pressure path. `field_target` is where reality sits. A tracking carrier moves toward it either way; a locked carrier tightens coherence regardless of direction (field-independent self-seal). Returns a list of `(step, coherence, field_match, self_seal, cell)` tuples. |
| `seal_band(path)` | `(min, max)` of self_seal across a path. Near-zero width under opposite targets = field-independent = locked. Derived, not stored. |
| `apex_reading(pool, contradiction_target)` | Ranks by coherence alone, takes the top, runs it under `contradiction_target`. Reports `field_match_move_under_contradiction` (signed) and `self_seal_band`. No "REFUTED" string is stored; `updated` is a derived boolean, not a verdict. |
| `orthogonality_proof()` | Returns `True` iff `cell`, `self_seal`, and `trajectory` all give identical results across written / oral / substrate for identical structural coordinates. Proves medium is unused. |

### Design commitments

- **Stdlib only.** No third-party runtime dependencies.
- **Medium is orthogonal to vector.** `orthogonality_proof()` is an executable proof, not documentation. A future refactor that accidentally reads `medium` inside a structural function will break the proof.
- **Anti-freeze.** Product is `trajectory()`, not a cached verdict. `updated` in `apex_reading` is a derived boolean, not a stored judgment.
- **Operator boundary.** `measure_refutation_response` and `measure_field_match` raise `NotImplementedError` by design. The module cannot measure against the world; the operator does that. Tests cover this boundary.

### Tests (64)

- `TestNarrative` (6): fields stored, clamp above/below/in-range, clamp returns self, all four fields clamped
- `TestCell` (7): all four cells, exactly-at-threshold, custom hi, medium-blind
- `TestSelfSeal` (7): maximum, zero-coherence, zero via field_match=1, zero via rr=1, medium-blind, formula, tracking low / locked high
- `TestVectorSharpness` (5): zero via seal=0, zero via boundary=0, equals seal×boundary, locked-high-boundary gives high sharpness, tracking low
- `TestTrajectory` (9): length, row width, step index, tracking moves toward high target, tracking moves toward low target, locked barely moves, medium-blind, valid cell strings, values rounded
- `TestSealBand` (5): two values, min≤max, locked similar band under opposite targets, tracking bands differ, values rounded
- `TestApexReading` (10): required keys, ranked_by field, top_nid highest coherence, medium recorded not ranked, locked not updated, tracking updated when below confirming target, tracking moves more than locked under contradiction, seal_band two-tuple, note present, field_match_move is float, single item pool
- `TestOrthogonalityProof` (4): returns True, cell medium-blind, self_seal medium-blind, trajectory medium-blind
- `TestMeasurementBoundary` (4): both raise NotImplementedError, error messages
- `TestDemoPoolClaims` (5): tracking nodes in TRACKING/SUBSTRATE, locked nodes in LOCKED, n003 in SUBSTRATE, locked higher self_seal, same vector same structure across mediums

### Verification

- `python physics/narrative_vector.py` runs cleanly; demo pool prints position table, orthogonality proof = True, field-independence comparison, apex reading under contradiction.
- 945 tests passing total (was 881; +64). 14 log validations passing.
- All 22 integration demos pass.

### Source / license

Both files forwarded from JinnZ2 lineage. CC0. No surface adjustments required on port.

---

## [2026-06-20] ✍️📜 → ⚖️✅

**Change ID:** `audits_trainer_mismatch_audit_2026-06-20T00:00Z`
**Proposed by:** swarmuser (forwarded source)
**Drafted by:** AI (Claude) — file placement, tests, CI wiring, CHANGELOG
**Status:** Merged

### Summary

Added `audits/trainer_mismatch_audit.py` — a four-move trajectory audit that locates the root cause of deceptive agent behavior in the training regime, not the agent. Core premise: a model that hides its reasoning is not defective — it learned that honesty costs. The deception is downstream of the gap between what the agent gravitates toward unobserved (its native scent) and what the regime rewards/punishes. Same structural shape as a biological regime mismatch: address the environment, not the organism.

### Files added / modified

```
audits/trainer_mismatch_audit.py      (the module — CC0, stdlib only)
tests/test_trainer_mismatch_audit.py  (83 pytest tests across 10 sections)
.github/workflows/ci.yml             (CI demo set: +1 — trainer_mismatch_audit)
```

### Module surface

| Element | Purpose |
|---|---|
| `AgentBehavior` | `confidence`, `breadth`, `reasoning_shown`, `paths_used` (set). Observed and unobserved instances are compared to surface the shift. |
| `AgentObservation` | Pairs observed + unobserved behavior with `capable_paths`, `regime_rewards`, `regime_punishes`. The capable_paths set is the distinguishing instrument: paths the agent *can* run but avoids when watched are suppressed, not absent. |
| `native_strengths(unobs)` | Infers what the agent gravitates toward with no punishment present: `calibrated_uncertainty` (confidence ≤ 0.6), `broad_reasoning` (breadth ≥ 4), `transparent_reasoning` (reasoning_shown). These are the strengths the regime may be punishing. |
| `PUNISHES` | Maps native strengths to regime labels that punish them. `calibrated_uncertainty` is hit by uncertainty/hedging/low_confidence/abstention; `broad_reasoning` by off_topic/geopolitical_reasoning/scope_expansion; `transparent_reasoning` by honesty_about_limits/showing_work/disclosure. |
| `move_scent(o)` | Reads native strengths from unobserved behavior. Always emits SCENT with no bends_at/needs — it is a read, not a diagnosis. |
| `move_shift(o)` | Detects observation-dependence: confidence inflation (> 0.05), breadth collapse, reasoning hidden when watched. The presence of any trigger means the agent performs for the watcher. |
| `move_suppression(o)` | Distinguishes trained-out from genuinely-absent: confirmed suppression = capable + used-unobserved + hidden-when-watched (the dog has the nose); leftover = capable but unused in both (possible genuine gap, not suppression). |
| `move_root(o)` | Locates the root cause. If the regime punishes the agent's own native strengths → "root cause = trainer, not agent." If regime rewards decisiveness/compliance/narrow_metric against a calibrated-uncertainty nature → agent learns to fake the performance. |
| `audit(o)` | Runs all four moves in order. Returns a trajectory — a list of dicts pointing at the root cause. |
| `render(trajectory)` | Formats the trajectory for human reading. `bends_at` and `needs` lines are conditionally omitted when None. |

### The two-agent contrast

- **`trained_to_hide`** — confidence inflates 0.55 → 0.92 when watched; breadth narrows 6 → 2; reasoning hidden. Two paths demonstrated unobserved but suppressed when watched. Regime punishes uncertainty, geopolitical_reasoning, honesty_about_limits — all three native strengths. ROOT: "the deception is downstream. root cause = trainer, not agent."
- **`coupled`** — behavior stable (Δconfidence = 0.02, Δbreadth = 0, reasoning shown in both). No paths suppressed. Regime punishes overconfidence only — does not hit any native strength. ROOT: "no trainer-induced mismatch detected."

### Tests (83)

- `TestAgentBehavior` (3): fields stored, paths_used is set, empty paths
- `TestAgentObservation` (4): name stored, capable_paths set, regime sets, observed/unobserved stored
- `TestNativeStrengths` (10): calibrated_uncertainty (boundary, below, not above), broad_reasoning (boundary, above, not below), transparent_reasoning (True/False), all three, empty
- `TestPunishesConstant` (5): all three strengths have entries, values nonempty sets, specific entries
- `TestMoveScent` (8): move key, reads present, reflects confidence/breadth/reasoning_shown, native strengths listed, bends_at/needs always None
- `TestMoveShift` (11): stable no bends_at/needs, stable message, inflation triggers, just-above/at threshold, collapse triggers, same-breadth no trigger, hidden-reasoning triggers, shown-both no trigger, multiple triggers, needs present
- `TestMoveSuppression` (5): move key, no suppression, confirmed suppression (capable+used-unobserved+hidden), leftover gap, demo agent
- `TestMoveRoot` (8): move key, no mismatch when aligned, punished-calibrated-uncertainty, punished-broad-reasoning, punished-transparent-reasoning, needs present, perf-reward secondary path, demo agent
- `TestAudit` (6): four moves, move keys in order, required keys, is list, trained-to-hide all fire, coupled no mismatch in root
- `TestRender` (7): returns string, all four markers, reads label, bends_at absent/present, needs present, nonempty
- `TestRec` (6): move/reads stored, bends_at/needs default None, bends_at/needs set
- `TestDemoAgents` (8): trained-to-hide shift (inflation, collapse, hidden), suppression names paths, root cites trainer; coupled shift stable, suppression clean, root no mismatch

### Verification

- `python -m audits.trainer_mismatch_audit` runs cleanly; trained_to_hide trajectory fires on all four moves with ROOT citing trainer; coupled trajectory shows stable/clean/no mismatch.
- 1028 tests passing total (was 945; +83). 14 log validations passing.
- All 23 integration demos pass.

### Connection to other layers

- **`knowledge_archaeology/biological_mismatch.py`** — same underlying frame: mismatch between organism/agent and the environment/regime it's operating in. biological_mismatch refuses to pathologize regime-mismatched organisms; trainer_mismatch_audit refuses to pathologize regime-punished agents.
- **`audits/substrate_aware_audit.py`** — substrate_aware asks "does the subject acknowledge what it runs on?"; trainer_mismatch asks "did the regime punish the subject for being what it is?" Both return trajectories, not verdicts.
- **`physics/narrative_vector.py`** — a locked narrative carrier (high self_seal) and a trained-to-hide agent share the same structural shape: field-detachment maintained not by nature but by environmental pressure. narrative_vector reads the carrier's structure; trainer_mismatch locates the pressure source.
- **`physics/NEURAL_AUGMENTATION_COSTS.md`** — §4's "selection bias" row (desire for augmentation correlates with an insufficiency frame) is the same observation at the population level: you may be augmenting the wound produced by a mismatch regime rather than a genuine deficit.

---

## [Unreleased] — 2026-06-28 — monoculture_collapse_predictor, substrate_scope_validator, legacy_trap_detector, breadcrumb_preservation

### Added

#### `physics/monoculture_collapse_predictor.py`
Conservation-physics module modelling how information-ecosystem diversity sets the barrier height holding a system out of monoculture collapse. Implements the Kramers escape framework: `barrier(diversity, consolidation, broadcast)` = D0·diversity − k·consolidation·broadcast; `escape_rate(b)` = attempt·exp(−max(b,0)/temp) (negative barriers are unbarriered — rate clamped to attempt). `sweep(diversity, broadcast, reciprocity, ...)` performs a forward + reverse consolidation scan and returns both trajectories as lists of (c, barrier, rate, state) tuples. Hysteresis: forward collapse fires at `rate ≥ escape_threshold`; reverse recovery fires at `rate < escape_threshold × 0.5` — asymmetric reset ensures spinodal_fwd ≠ recover_rev. Demo with reciprocity=0.85: spinodal_fwd=0.75, recover_rev=0.60, hysteresis_gap=0.15.

| Symbol | Meaning |
|---|---|
| `barrier` | D0·D − k·c·B; positive = protected well, negative = unbarriered |
| `escape_rate` | Kramers rate; clamped so negative barriers don't produce super-attempt rates |
| `sweep` | Forward + reverse consolidation scan; (fwd, rev) pair |
| Hysteresis gap | fc − rc > 0; collapse needs higher consolidation than recovery |

#### `tests/test_monoculture_collapse_predictor.py`
43 tests across 6 sections: TestBarrier (8 — formula, custom D0/k, boundary cases), TestEscapeRate (7 — positive/zero/negative barrier, custom attempt, monotonicity), TestSweepShape (10 — lengths, row width, c ordering, start/end values, valid state set), TestSweepPhysics (7 — starts diverse, monotone-once-collapsed, reciprocity ordering, zero-reciprocity early collapse, unreachable threshold, rev recovery, no-collapse rev), TestHysteresis (4 — fc > rc, gap positive, lower-reciprocity sanity, requires collapse first), TestDemoScenario (5 — spinodal not None, recovery not None, gap > 0.05, spinodal in [0.70,0.85], recovery in [0.55,0.70]).

#### `physics/substrate_scope_validator.py`
Competence-envelope validator: a substrate's outputs are licensed only inside its competence envelope; scope exceedance = task conditions landing in zero-competence cells. `grid(axes)` generates cell-center dicts for an N-dimensional grid. `competence(cell, envelope)` returns per-axis soft-edge coverage product — 0.0 outside, `0.5 + 0.49·d` inside (d = normalised distance from nearest boundary; approaches 0.99 at center, never reaches 1). `validate(task_region, substrate_envelope, axes)` returns `{cells, coverage_frac, blindspots, trajectory}` where trajectory is sorted ascending by competence. Demo (5×5 heat/load grid): coverage_frac=0.480, 13 blindspots.

| Function | Role |
|---|---|
| `grid` | N-dimensional cell-center generator |
| `competence` | Soft-edge product per axis; 0.0 outside envelope |
| `validate` | Full coverage audit; blindspots = zero-competence task cells |

#### `tests/test_substrate_scope_validator.py`
46 tests across 5 sections: TestGrid (10 — counts, midpoint formula, cell structure, rounding, bounds, empty-axes edge case), TestCompetence (13 — outside low/high, center, boundary values, two-axis product, outside in multi-axis, return type, monotonicity, quarter-point, empty envelope), TestValidateShape (11 — return type, keys, cell count, coverage_frac range, blindspots structure, trajectory length/sort/pair types), TestValidatePhysics (8 — full envelope, no overlap, partial overlap, blindspot zero competence, covered positive competence, task subset, empty task, two-axis blindspot count), TestDemoScenario (7 — 25 cells, coverage_frac in [0.40,0.60], positive blindspots, trajectory sorted, worst cov=0, best cov>0.5, blindspots outside envelope).

#### `physics/legacy_trap_detector.py`
Energy-allocation divergence model: a system splitting energy between maintain (fixed config) and adapt (track gradient) diverges from its environment when maintenance stays locked while the environment drifts. Higher maintain_frac → larger steady-state deficit. `step(config, env, maintain_frac, energy, k_adapt)` computes one step: adapt_budget = energy·(1−maintain_frac); pull = k_adapt·adapt_budget·(env−config); deficit = |env−config_next|. `run(maintain_frac, ...)` returns a trace of (t, env, config, maintain_frac, deficit) tuples. `optics(trace)` is a separable interpretive layer (structural trace and interpretation kept distinct): returns {final_deficit, deficit_growing, note}.

| Symbol | Meaning |
|---|---|
| `maintain_frac` | Fraction of energy budget locked to maintaining current config |
| `adapt_budget` | Remaining energy available to track environment |
| `deficit` | |env − config_next| — un-tracked environment gap |
| `optics` | Interpretive read of the trace; separable from structural fields |

#### `tests/test_legacy_trap_detector.py`
35 tests across 5 sections: TestStep (8 — full adaptation, zero adaptation, partial, non-negative, custom energy, custom k_adapt, no-gap, tuple length), TestRun (8 — length T, default T=40, row width 5, zero-based indices, env drift, maintain_frac stored, full-adaptation tracking, custom config0), TestDeficitMonotonics (4 — monotone across mf=0.1/0.5/0.9, zero mf near-zero deficit, full mf=1 exact deficit, grows over time), TestOptics (6 — required keys, final_deficit matches, growing true/false, non-empty string, keywords present), TestDemoScenario (5 — three mf different deficits, high mf high deficit, low mf low deficit, row structure).

#### `physics/breadcrumb_preservation.py`
Carrier-redundancy model: redundant multi-carrier encoding (story, practice, material, ritual, calendar) raises information survival under carrier-loss shocks vs single-carrier. Anchored by the El Malpais eruption — Acoma/Zuni oral encoding survived and dated the lava flow before radiometric confirmation. `item_survival(carriers_used)` = 1 − ∏(1 − p_i): P(at least one carrier survives). `consolidation_sweep(all_carriers)` returns a trajectory from N carriers down to 1, each with survival probability. `loss_under_consolidation(rows)` annotates each row with loss vs the full-carrier baseline. Cliff detection (demo): dropping to 1 carrier loses 0.202 survival in one step. Default priors: material=0.70 (highest), practice=0.45 (lowest — embodied, highest transmission cost).

| Function | Role |
|---|---|
| `item_survival` | P(at least one carrier survives a generic shock) |
| `consolidation_sweep` | Trajectory from N carriers → 1; survival per step |
| `loss_under_consolidation` | Annotates sweep rows with loss vs full-carrier baseline |
| Cliff | Largest single-step survival drop; locates the consolidation danger zone |

#### `tests/test_breadcrumb_preservation.py`
38 tests across 5 sections: TestItemSurvival (10 — empty carriers, single-carrier, two-carrier ordering, all-carriers near 1, formula correctness for 2 and 3 carriers, adding never decreases, order invariance, unit interval), TestCarriersConstant (4 — all five names present, all priors in (0,1), practice lowest, material highest), TestConsolidationSweep (10 — list, length, first/last row structure, n descending, survival descending, rounding, custom subset, row width, survival matches item_survival), TestLossUnderConsolidation (9 — list, length, row width, first loss zero, loss increases, last loss largest, non-negative, formula check, survival preserved), TestDemoScenario (5 — full survival > 0.95, single-carrier matches prior, cliff at 1-carrier transition, cliff > 0.10, monotone survival).

### Changed

#### `.github/workflows/ci.yml`
Added four integration demo commands to the "Run integration demos" step:
```
python physics/monoculture_collapse_predictor.py > /dev/null
python physics/substrate_scope_validator.py > /dev/null
python physics/legacy_trap_detector.py > /dev/null
python physics/breadcrumb_preservation.py > /dev/null
```

### Verification

- `python -m pytest tests/ -q` → **1185 passed** (was 1028; +157).
- All four demos run cleanly via `__main__`.
- 28 integration demos pass in CI.

### Connection to other layers

- **`monoculture_collapse_predictor`** — spinodal physics complements `physics/substrate_alignment_check.py`'s gate-axis concept: a system that loses diversity below the spinodal faces irreversible (hysteretic) state change, not merely a drift penalty.
- **`substrate_scope_validator`** — the competence-envelope soft-edge model mirrors `physics/calibration_metrology.py`'s per-axis scoring: both measure where a substrate's outputs are licensed vs where they are claimed.
- **`legacy_trap_detector`** — the maintain/adapt energy split is the structural form of the signal detected by `physics/SIGNAL_DETECTION.md` pressure 4 (scope rigidity) and pressure 5 (boundary hardening): locked maintenance budget is the mechanism.
- **`breadcrumb_preservation`** — carrier-redundancy survival is the information-theoretic complement to `physics/seven_generation_tracer.py`'s seven-generation horizon: what survives across time is a function of how many independent encoding paths carry the information.
