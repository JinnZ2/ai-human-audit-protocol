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
| `embodied_sensor.py` | ✅ shipped 2026-04-27 | operator-agnostic primitive (human/animal/plant/ai/instrument/ecosystem); `EmbodiedReading` with controlled vocabularies, confidence ceilings per `epi`, `CoatingProbeResult`, `OperatorBudget` stub, lift-to-`FrameReading`. 32 unit tests passing. |
| `router/base.py` | ✅ shipped 2026-04-27 | `BaseModelAdapter` ABC + `CostEstimate`. `__init_subclass__` enforces frame_id/operator_type at definition time. |
| `router/mock_adapter.py` | ✅ shipped 2026-04-27 | Deterministic offline `MockAdapter` — no external calls. Configurable `response_factory`. |
| `router/consent.py` | ✅ shipped 2026-04-27 | `ConsentGate` — fail-closed, immutable history, grant/revoke, `assert_authorized` raises `ConsentDenied`. |
| `router/query_dispatcher.py` | ✅ shipped 2026-04-27 | `QueryDispatcher.fan_out()`: per-adapter availability → consent → query; records readings, refused, failures, unavailable separately. Fail-soft per adapter. |
| `router/coherence_aggregator.py` | ✅ shipped 2026-04-27 | `aggregate(dispatch_result, problem, frames)` — wraps `MultiGeometryCollaboration.synthesize()` with cross-adapter audit metadata. Surfaces "geometry of absence" when zero readings. |
| `router/model_adapters/{claude,gemini,deepseek}_adapter.py` | ✅ shipped 2026-04-27 (stubs) | `available()` returns False with helpful reason; `query()` raises `NotImplementedError` with wiring instructions. Default frame_ids: Claude→narrative_structured, Gemini→pattern_spatial, DeepSeek→statistical_relational. |
| `tests/test_router.py` | ✅ shipped 2026-04-27 | 45 tests: BaseModelAdapter contract, MockAdapter, ConsentGate, QueryDispatcher, CoherenceAggregator, API stubs, full-stack smoke |
| `audit/blind_spot_log.md` | ✅ shipped 2026-04-27 | format spec + how-to-write. Required fields, three `entry_kind`s (run / retrospective / calibration_update), JSONL append-only. |
| `audit/blind_spot_log.schema.json` | ✅ shipped 2026-04-27 | JSON Schema (draft-07) for entries. Schema-validated by tests. |
| `audit/example_blind_spot_log.jsonl` | ✅ shipped 2026-04-27 | Worked examples covering run + calibration_update kinds. All entries schema-validate. |
| `examples/cherokee_creation.py` | ✅ shipped 2026-04-27 | multi-encoding ontology demo. **Placeholder content** with explicit cultural sourcing note — exercises the machinery without appropriating actual narrative content. |
| `examples/genesis_drift.py` | ✅ shipped 2026-04-27 | regime drift detection demo. holocene-validated agricultural prescription, drift_check fires under transitional climate context. |
| `examples/soil_with_hands.py` | ✅ shipped 2026-04-27 | embodied-query end-to-end. EmbodiedReading → FrameReading → MultiGeometryCollaboration → synthesize → blind_spot_log entry (schema-validated). |
| `tests/test_consortium_examples.py` | ✅ shipped 2026-04-27 | 16 tests across the three examples + the example log file |
| `bridges.py` | ✅ shipped 2026-04-27 | `FrameReading ↔ Primitive ↔ ClaimNode` connectors. Forward AND inverse direction complete: `reading_to_primitives`, `frame_reading_to_primitives`, `primitives_to_claim_graph`, `trajectory_summary` (lightweight), `trajectory_to_frame_reading` (full inverse with shape classification). Each function declares `preserves`/`lossy_on` via `BridgeReport`. 81 tests. |
| `tests/test_bridges.py` | ✅ shipped 2026-04-27 | 43 tests: mappings, frame selection, reading lift, frame reading lift, claim graph build, trajectory summary, bridge reports, end-to-end |
| `tests/test_kfc_runtime.py` | ✅ shipped 2026-04-27 | 34 tests: CYC_DT, scope/bounds overlap, _within, should_activate, step, felt_sensor, query, soil graph |
| `tests/test_ontology_layer.py` | ✅ shipped 2026-04-27 | 30 tests: Primitive, Ontology, TransformRule, MultiEncodingRegistry, coherence_check, drift_check, multi_query, water_cycle demo |
| `tests/test_collaboration_protocol.py` | ✅ shipped 2026-04-27 | 33 tests: REVERSIBILITY_RANK, frame/problem/reading construction, add_reading, invariants/blind_spots/contradictions, synthesize, build_consortium_frames, AMOC demo |

---

## Priority-ordered open builds

### P0 — needed for v1 functional

1. ~~**Bridge between abstraction layers.**~~ → forward + inverse done 2026-04-27 in `consortium/bridges.py`. Forward: `reading_to_primitives`, `frame_reading_to_primitives`, `primitives_to_claim_graph`. Inverse: `trajectory_to_frame_reading` with shape classification (`stable | monotonic_increase | monotonic_decrease | saturating_* | accelerating_* | oscillating | mixed`), load-bearing detection by total |delta|, FELT-aware diagnosis synthesis, heuristic confidence. Each function declares `preserves`/`lossy_on`. The inverse explicitly flags itself as a coating risk via `assumptions_required: trajectory_classification=heuristic_v1` so downstream readers can audit the heuristic. Round-trip tested: lifted FrameReadings can be re-injected into `MultiGeometryCollaboration.synthesize()` without error.

2. **`embodied_sensor.py` primitive — operator-agnostic.** A direct reading is a direct reading regardless of substrate. Plants, animals, humans, AI vision/audio models, and instruments all produce readings that share the same primitive shape; they differ only in `operator_type`, `epi` sub-tag, and confidence calibration. The audit-symmetry stance fails the moment one operator type is privileged as automatic ground truth.

   Field shape (proposed, awaiting consent):
   ```python
   @dataclass
   class EmbodiedReading:
       sensor_id: str               # e.g. "human:kavik:hands:2026-04-27T14:00Z"
                                    #      "plant:phenology:bur_oak_grove_42"
                                    #      "animal:behavior:wolf_pack_north"
                                    #      "ai:vision:claude:image_xyz"
                                    #      "instrument:soil_probe:ds18b20:42"
       operator_type: str           # human | animal | plant | ai | instrument | ecosystem
       location: Any                # coords, place_id, or topological reference
       timestamp: datetime
       observation: str             # natural-language description (or structured form)
       claim_refs: List[str]        # which .claims this reading bears on
       epi: str                     # measured_kinesthetic | measured_olfactory |
                                    # measured_visual | measured_auditory |
                                    # measured_phenological | measured_behavioral |
                                    # measured_instrumental | inferred
       confidence: float            # 0..1 (calibrated, not asserted)
       conditions: Dict[str, Any]   # weather, fatigue, attention, framing prior,
                                    # sensor calibration date, model version, etc.
       coating_probe_result: str    # passed | failed | not_run | inconclusive
   ```
   The `conditions` and `coating_probe_result` fields are the audit-symmetry hooks: every operator's reading carries the same accountability shape. A plant's phenology shift, a wolf's behavior change, a human's hands-in-soil, and an AI's image-classification pass through identical typing — only their `epi` sub-tag and `confidence` differ.

3. ~~**`router/query_dispatcher.py`.**~~ → done 2026-04-27 (v1-offline). `QueryDispatcher.fan_out()` runs the available + consent + query loop per adapter and records each adapter's outcome (reading / refused / failure / unavailable) separately. Fail-soft per adapter. The dispatcher is wrapped by a fail-closed `ConsentGate` (`router/consent.py`) — no adapter is queried without explicit per-(problem, adapter) authorization. Real model API wiring is open; see #4.

4. **Real model adapter wiring.** `router/model_adapters/{claude,gemini,deepseek}_adapter.py` exist as stubs that raise `NotImplementedError` with wiring instructions. Each declares its default consortium frame and an `operator_type=ai`. Wiring requires:
   - Decision on credentials handling (env var / config file / per-run injection)
   - Implementation of the adapter's `query()` to call its API and parse the response into a `FrameReading` with honest `assumptions_required` recording the model version, system prompt, and disclosed input
   - Implementation of `cost_estimate()` to return real token / USD figures
   - Audit log entry on every API call (which key was read, what was disclosed, what came back)

   Each real adapter ships in its own change event with its own consent.

### P1 — accountability

5. ~~**Consortium tests.**~~ → done 2026-04-27. 97 tests across the three files (34 + 30 + 33). All pass. Total consortium test count: 172 (97 here + 32 embodied_sensor + 43 bridges).

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

- ~~**No reversibility scoring system.**~~ → done 2026-04-27: `REVERSIBILITY_RANK` constant added; sort uses numeric rank; `irreversible_if_delayed` actions are bubbled into a separate `time_critical_actions` list because the cost of *inaction* is unrecoverable.

- ~~**`trust_signal: "low"` is ambiguous.**~~ → done 2026-04-27: renamed to `convergence: "converged" | "divergent"` with explicit `convergence_note` explaining that divergent does NOT mean abandon the analysis — the geometry is in the disagreements.

- ~~**No actual model adapter exists.**~~ → infrastructure done 2026-04-27. `MockAdapter` runs offline; `ClaudeAdapter`/`GeminiAdapter`/`DeepSeekAdapter` exist as stubs with explicit wiring instructions. The leap from "structure runs" to "structure runs against live models" is now just per-adapter wiring, not architectural work.

- ~~**No consent gate before fan-out.**~~ → done 2026-04-27. `ConsentGate` is fail-closed by default; `QueryDispatcher` consults it before every `adapter.query()` call. Per-(problem, adapter) granularity. Immutable audit history. Cost estimates available for disclosure to consenter via `dispatcher.cost_estimates(problem)`.

- **Most operator types have no code path to submit readings.** `build_consortium_frames()` declares seven frames, but only AI-model and human-sensor frames have any plausible code path to actually submit readings. Plants, animals, ecosystems, instruments, and tradition holders all participate via a *scribe* — a human observer, an instrument's data logger, an AI vision pass, a recording device. The act of scribing is itself a coating risk: the scribe imposes their own frame on what they record. We have no rule yet for who can scribe, what gets logged about the scribe's own state at scribing-time, or how the scribe's framing gets audited.

- **No protection against over-querying any embodied operator.** Embodied readings are finite for *every* operator: humans get tired, plants have phenological windows, animals have behavioral budgets, AI vision/audio models have rate limits and inference costs, instruments have battery and calibration cycles. A consortium that treats any single operator as inexhaustible ground truth will burn the substrate it depends on. Each operator type needs a budget appropriate to its substrate, not a single global rate-limit.

- **Audit log of the consortium auditing itself.** Recursive question: when the consortium's outputs are wrong, who notices? `audit/blind_spot_log.md` is the start, but it needs a feedback loop: which past predictions panned out, which didn't, which frames were systematically over- or under-confident. This is `phantom_forecast_agent.py` territory but for consortium runs.

---

## Decisions deferred

| Decision | Options | Status |
|---|---|---|
| ~~Where the bridge between `FrameReading` ↔ `ClaimNode` ↔ `Primitive` lives~~ | ~~new file, or extend each existing class~~ | Resolved 2026-04-27: new file `consortium/bridges.py`; existing classes untouched |
| Fieldlink data ingestion | loader vs. inlined-per-adapter | Deferred |
| ~~Reversibility scale~~ | ~~string ordering vs. numeric~~ | Resolved 2026-04-27: numeric `REVERSIBILITY_RANK` |
| ~~Model adapter auth / secrets~~ | ~~local config vs. env vars vs. shared protocol settings~~ | Still open per real-adapter wiring; v1-offline ships without a decision because no real API call is made yet. |
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
