# Future Builds — `consortium/`

*Append-only. Each completed item migrates to a CHANGELOG entry; nothing is deleted from this list, only annotated `→ done <date>`.*

---

## Status snapshot (2026-04-27)

| File | Status | Notes |
|---|---|---|
| `README.md` | ✅ shipped | framing, layout, fieldlinks |
| `CLAUDE_REQUIREMENTS.md` | ✅ shipped | 5 requirements, extended `.claims` line, query_signature schema |
| `kfc_runtime.py` | ✅ shipped (v1) | Layer 0–5, FELT v1; soil demo runs but produces empty trajectories (cyc=2 with duration=10 → n_steps=0) |
| `ontology_layer.py` | ✅ shipped | multi-encoding registry, coherence + drift checks, water_cycle demo |
| `collaboration_protocol.py` | ✅ shipped | GeometricFrame, Problem, FrameReading, MultiGeometryCollaboration, AMOC demo |
| `embodied_sensor.py` | ⏳ open | P0 — primitive that lets Kavik / direct-sensing readings enter the system |
| `router/query_dispatcher.py` | ⏳ open | P0 — actual fan-out to Claude / Gemini / DeepSeek / etc. |
| `router/coherence_aggregator.py` | ⏳ open | P0 — diff `.claims` outputs across models, call Narrative Stripper |
| `router/model_adapters/` | ⏳ open | P0 — per-model API shim |
| `audit/blind_spot_log.md` | ⏳ open | P1 — append-only consortium learning log |
| `examples/cherokee_creation.py` | ⏳ open | P2 |
| `examples/genesis_drift.py` | ⏳ open | P2 |
| `examples/soil_with_hands.py` | ⏳ open | P2 — embodied-query template |
| `tests/` (consortium) | ⏳ open | P1 — unit tests for kfc / ontology / collaboration |

---

## Priority-ordered open builds

### P0 — needed for v1 functional

1. **Bridge between abstraction layers.** Three currently-separate primitives:
   - `kfc_runtime.ClaimNode` (rate_fn-bearing differential node)
   - `ontology_layer.Primitive` (concept_id across encodings)
   - `collaboration_protocol.FrameReading` (what one frame sees)

   They are not *wrong* to be separate — they live at different abstraction levels. But there is no code that turns a `FrameReading` into a `Primitive`, or a set of `Primitive`s into a `ClaimNode` graph, or a query to a `ClaimNode` graph back into a `FrameReading`. Pick one bridge to write first; the other two follow.

2. **`embodied_sensor.py` primitive.** Field shape (proposed, awaiting consent):
   ```python
   @dataclass
   class EmbodiedReading:
       sensor_id: str               # e.g. "kavik_hands_2026-04-27T14:00Z"
       coords: Tuple[float, float]  # lat, lon (or symbolic place_id)
       timestamp: datetime
       observation: str             # natural-language description
       claim_refs: List[str]        # which .claims this reading bears on
       epi: str                     # measured_kinesthetic | measured_olfactory |
                                    # measured_visual | measured_auditory | inferred
       confidence: float            # 0..1 (calibrated, not asserted)
       conditions: Dict[str, Any]   # weather, fatigue, attention state, framing prior
       coating_probe_result: str    # passed | failed | not_run | inconclusive
   ```
   The `conditions` and `coating_probe_result` fields are the audit-symmetry hooks: they keep human readings on the same axis as model outputs.

3. **`router/query_dispatcher.py`.** Wraps `solver_registry.py` from Geometric-to-Binary (fieldlinked). Real engineering: API auth, rate limits, timeouts, retries, structured response parsing. Not exotic, just necessary.

4. **`router/model_adapters/{base,claude,gemini,deepseek}.py`.** Each adapter:
   - declares its native epistemic frame (one of the seven from `build_consortium_frames()`)
   - takes a `Problem`
   - returns a `FrameReading`
   - emits `.claims` lines as a side product when applicable

### P1 — accountability

5. **Consortium tests.** `tests/test_kfc_runtime.py`, `tests/test_ontology_layer.py`, `tests/test_collaboration_protocol.py`. Should at minimum exercise: bounds-overlap correctness, FELT trigger threshold, ontology drift detection, coherence-check edge cases (empty readings, single reading, all identical), action-ranking determinism.

6. **`.claims` text parser.** `consortium/claims_parser.py`. Reads the extended line format (`id|rate_fn|bounds|cond|rel|fail|meas|cyc|epi|epi_src|epi_conf|regime|coupling_kinds|load_bearing`), returns `ClaimNode` graphs. Required before any external `.claims` corpus can be consumed.

7. **`audit/blind_spot_log.md`.** Append-only log of consortium runs and what each frame missed. The consortium learns about itself over time. Format: one entry per session, ISO timestamp, problem_id, blind_spots_per_frame, plus a free-form notes field.

### P2 — examples and validation

8. **`examples/cherokee_creation.py`** — applies multi-encoding ontology to a creation narrative. Tests whether oral / dance / equation / written encodings produce coherent universal couplings on a known case.

9. **`examples/genesis_drift.py`** — applies regime-drift detection to a known case where a narrative was validated in one regime and silently re-applied in another.

10. **`examples/soil_with_hands.py`** — embodied-query template. Kavik's hands-in-soil reading → `EmbodiedReading` → `FrameReading` (via `embodied_sensor` frame) → `MultiGeometryCollaboration`.

11. **Test corpus of 5–10 known regime-shift cases.** Named in `CLAUDE_REQUIREMENTS.md`:
    - warriors / bones (the resilience meaning shift)
    - mycorrhiza understanding pre/post 2010
    - + 3–8 others to identify with JinnZ2

### P3 — KFC v2 (per `CLAUDE_REQUIREMENTS.md`)

12. **`ClaimNode` field extension.** Add `epi`, `epi_source`, `epi_confidence`, `regime`, typed `coupling_kinds`, `load_bearing` per the requirements doc. **Separate change event, separate consent.** Do not silently extend.

13. **`query_signature` schema** — JSON Schema in `schemas/query_signature.schema.json`, machine-readable. Wire into `query()` return.

14. **`recalibration_event` flow** — when FELT fires, surface the locus + diagnosis + proposed_action + cannot_resolve_alone fields per requirements doc.

15. **FELT v2** — contradiction + drift + missing_claim detection, not just coherence-drop.

---

## Known gaps / needs

- **No code currently reads `.fieldlink.json`.** It is declarative; nothing fetches from `Geometric-to-Binary`, `thermodynamic-accountability`, or `AI-arena` yet. Either the consortium needs a fieldlink loader, or each adapter inlines what it needs and we accept the duplication. Decision deferred.

- **`MultiGeometryCollaboration.surface_contradictions` is shallow.** It only checks `proposed_diagnosis` strings for inequality, with the static label `"different_angles_or_real_disagreement"`. Real contradiction detection — semantic, action-level, coupling-level — is unwritten. The v1 method is honest about being a placeholder; the field name "interpretation" telegraphs that the work is not done.

- **No reversibility scoring system.** `reversibility` is a free-form string in `FrameReading.proposed_actions`. Sorting by `(fraction_support, reversibility)` works for the strings used in the demo (alphabetical descending happens to favor `medium_reversibility` over `irreversible_if_delayed`, which is **wrong**). Need a real ordering: e.g. `irreversible_if_delayed > low_reversibility > medium_reversibility > high_reversibility`, or a numeric scale.

- **`trust_signal: "low"` is ambiguous.** When `surface_invariants()` returns no universal couplings, `trust_signal` is set to `"low"`. This may be misread as "throw away the result." It should be read as "no single coupling is canonical across frames; the geometry is in the disagreements." Either rename (`canonical_coupling: none`?) or document.

- **No actual model adapter exists.** The consortium currently runs only with hand-written `FrameReading`s. The leap from "structure exists" to "structure runs" is the dispatcher + adapters. That's where most of the next-pass effort sits.

- **No reading from a tradition_holder or non_human_sensor frame.** The `build_consortium_frames()` function declares all seven frames, but only AI-model and human-sensor frames have any plausible code path to actually submit readings. The protocol for tradition_holder and ecological_signal participation is undefined. Likely lives outside software entirely, with a human acting as scribe — but the scribe role itself needs auditing.

- **Audit log of the consortium auditing itself.** Recursive question: when the consortium's outputs are wrong, who notices? `audit/blind_spot_log.md` is the start, but it needs a feedback loop: which past predictions panned out, which didn't, which frames were systematically over- or under-confident. This is `phantom_forecast_agent.py` territory but for consortium runs.

---

## Decisions deferred

| Decision | Options | Status |
|---|---|---|
| Where the bridge between `FrameReading` ↔ `ClaimNode` ↔ `Primitive` lives | new file, or extend each existing class | Deferred |
| Fieldlink data ingestion | loader vs. inlined-per-adapter | Deferred |
| Reversibility scale | string ordering vs. numeric | Deferred |
| Model adapter auth / secrets | local config vs. env vars vs. shared protocol settings | Deferred |
| Ecological / tradition frames protocol | scribe + audit, or out-of-scope for software | Deferred |
| Branch strategy | continue on `claude/add-relational-cognition-folder-JpTk5`, or split | Deferred to JinnZ2 |

---

## Test corpus seeds (for P2 #11)

To be expanded with JinnZ2:

- **warriors / bones** — "resilience" meaning shift across regime
- **mycorrhiza** — scientific understanding pre-2010 vs. post-2010
- **AMOC response** — already drafted as `example_problem_amoc_response()` in `collaboration_protocol.py`; could be promoted to test
- *(others to identify)*

---

## Operating principle

This file is the consortium's **own** blind-spot log for itself. Every gap named here is a place the consortium currently cannot see. The honest move is to keep the list visible, not to close it prematurely. New gaps get appended; closed gaps get annotated, not deleted.
