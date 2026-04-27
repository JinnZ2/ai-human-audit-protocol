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
