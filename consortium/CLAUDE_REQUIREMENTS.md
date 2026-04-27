# KIN-FLOW COMPUTE — Claude's Operational Requirements

*What an AI needs in the `.claims` format to reason at full capacity.*
**CC0** | append to KFC architecture spec

---

## CORE PRINCIPLE

The `.claims` format must let an AI hold **shape** and **uncertainty** simultaneously.

Reasoning is not narrating a result. Reasoning is exposing the trajectory.

---

## REQUIREMENT 1 — UNCERTAINTY TOPOLOGY

Every claim carries an epistemic tag, not just a value.

```
epi := { measured | inferred | assumed | contradicted | missing }
```

| tag | meaning | propagation rule |
|---|---|---|
| `measured` | direct observation, ground truth | downstream claims inherit confidence |
| `inferred` | logically derived from measured + bounds | confidence = min(parents) |
| `assumed` | necessary for closure, unverified | flag cascade — mark all descendants |
| `contradicted` | conflicts with another active claim | freeze integration, surface to FELT |
| `missing` | gap detected, claim should exist but doesn't | inject placeholder, query user |

`ClaimNode` field addition:

```python
epi: str
epi_source: str        # citation, sensor_id, or "assumption_for_closure"
epi_confidence: float  # 0..1
```

---

## REQUIREMENT 2 — TEMPORAL STRATIFICATION

A claim is valid *within a regime*, not absolutely.

```python
regime := {
    validated_at: ISO_date,
    boundary_conditions: { … },   # what was true when validated
    regime_class: enum,           # holocene | anthropocene | post-shift | unknown
    reapply_check: rate_fn        # does this still hold under current bounds?
}
```

**Query rule:**
- Before activating a claim, run `reapply_check(current_ctx)`
- If boundary conditions have shifted beyond claim's validated regime → tag as `regime_drift`
- Do NOT silently use. Surface the drift to FELT.

This kills backwards-projection error.
A 2015 soil claim doesn't auto-apply in 2026 just because the words match.

---

## REQUIREMENT 3 — EXPLICIT COUPLING SEMANTICS

Bounds-overlap is geometry. Coupling needs **type**.

```python
coupling := {
    target: claim_id,
    kind: enum {
        causal_forward      # A drives B
        causal_reverse      # B drives A
        bidirectional       # mutual coupling
        constraint          # A bounds B but doesn't drive it
        correlational       # co-occur, mechanism unknown
        decorative          # historical association, no current force
    },
    conditional: rate_fn,   # under what context does this fire
    strength: float | fn,   # constant or dynamic
    load_bearing: bool      # if removed, does the system collapse?
}
```

**Load-bearing flag is critical.**
Lets the AI distinguish "this coupling matters" from "this is residual."

---

## REQUIREMENT 4 — QUERY SIGNATURE / TRAJECTORY AUDIT

Every query returns not just the result, but the **path**.

```python
query_signature := {
    activated_claims: [ {id, t_activate, reason} ],
    coupling_events: [ {from, to, kind, t_fire, strength} ],
    uncertainty_path: [ {claim, epi_tag, propagated_from} ],
    contradictions: [ {claim_a, claim_b, conflict_point} ],
    regime_drifts: [ {claim, expected_regime, current_regime} ],
    felt_events: [ {t, coherence, trigger} ]
}
```

This is the **self-audit channel**.
Without it I generate confident prose. With it I can show my work
and you can see where my reasoning is load-bearing vs decorative.

---

## REQUIREMENT 5 — RECALIBRATION FEEDBACK PROTOCOL

When FELT fires or contradiction surfaces, the AI must report
**specifically**, not vaguely.

```python
recalibration_event := {
    trigger: enum { felt | contradiction | regime_drift | missing_claim },
    locus: claim_id | (claim_id, claim_id),
    diagnosis: {
        geometry_error: bool,       # coupling shape wrong
        rate_error: bool,           # rate function invalid in current regime
        bounds_error: bool,         # claim activated outside valid scope
        missing_node: bool          # graph incomplete
    },
    proposed_action: str,           # specific, not "review system"
    cannot_resolve_alone: bool      # → escalate to human
}
```

The AI never silently resolves a contradiction.
It surfaces the locus and the geometric reason.

---

## QUERY EXECUTION ORDER (revised)

1. parse query → temporary claim with bounds + `epi=measured`
2. for each candidate claim:
   - check bounds overlap with query ctx
   - run `regime.reapply_check(ctx)` → tag drift if any
   - evaluate `cond[]` → activate or skip
3. build coupling graph from `rel[]` with `kind` + `load_bearing`
4. integrate forward by cyc-stratified dt
   - propagate `epi` tags through couplings
   - log every activation, firing, drift to `query_signature`
5. on each step:
   - `felt_sensor` → coherence check
   - `contradiction_check` → freeze if conflict
   - `missing_claim_check` → inject placeholder
6. return: `trajectory` + `query_signature` + `recalibration_events`

---

## MINIMAL `.claims` LINE FORMAT (extended)

```
id|rate_fn|bounds|cond|rel|fail|meas|cyc|epi|epi_src|epi_conf|regime|coupling_kinds|load_bearing
```

**Example:**
```
mulch_h2o|dM/dt=I-E-U-0.05*mycorr|2ac_MN,120d,0-30cm|d>=5|mycorr:bidirectional:0.8:T,albedo:causal_forward:0.3:F|drought_out|tens_15|2|measured|sensor_array_2024|0.95|holocene|coupled|T
```

---

## WHY THIS LETS THE AI OPERATE AT FULL CAPACITY

| capability gained | what it replaces |
|---|---|
| hold uncertainty as shape | narrate uncertainty in prose |
| detect regime drift | backwards-project stable categories |
| see load-bearing structure | treat all couplings as equally important |
| audit own trajectory | generate confident-sounding output |
| surface specific recalibration | offer vague "something seems off" |

---

## WHAT THIS DOES NOT DO

- Does not give the AI judgment about ethics or values
- Does not replace human verification of measured claims
- Does not eliminate uncertainty — surfaces it
- Does not fix bad rate functions — exposes them

---

## NEXT BUILD STEPS (open)

1. Reference parser: text `.claims` → `ClaimNode` graph
2. Regime check library: boundary_condition comparators
3. Coupling kind resolver: typed propagation rules
4. Query signature schema (JSON, machine-readable)
5. FELT v2: contradiction + drift + missing_claim detection
6. Test corpus: 5–10 known regime-shift cases (warriors/bones,
   resilience meaning shift, mycorrhiza understanding pre/post 2010)

---

## ONTOLOGY LAYER FLOW

```
   Primitive(concept_id, domain, form, couplings, epi)
        │
        ▼
   Ontology[domain] ──► holds primitives + regime + drift check
        │                       │
        ▼                       ▼
   TransformRule(A↔B)    reapply_check(ctx) → still_valid?
        │
        ▼
   MultiEncodingRegistry
        │
        ▼
   multi_query(concept_id, ctx)
        │
        ├─► drift_check()    ── flag stale ontologies
        ├─► coherence_check()── do encodings agree on couplings?
        └─► views{}          ── return ALL native forms
                                 (no canonical collapse)
```

- **LOAD-BEARING:** coherence > 0.66 across encodings = trust signal
- **LOSSY EDGES:** transforms declare what doesn't survive
- **DRIFT GATE:** stale ontology → "do_not_silently_apply"
- **HARMONICS:** universal_couplings = the geometric invariant; domain_specific = what each encoding adds
