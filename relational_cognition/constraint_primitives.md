# ⚙️ Constraint Primitives

**Glyphs:** 🌊 (flow) • 🔗 (coupling) • 🚪 (threshold) • 〰️ (phase) • ↯ (disruption)

**Thesis:** Relational cognition operates on a small set of verbs that name *how energy, attention, or constraint moves between nodes*. These primitives are the audit protocol's working vocabulary whenever surface English would otherwise flatten a relation into a noun.

The set below is adapted from the Energy English specification (see `README.md` for source). It is intentionally small — the audit protocol does not need the full upstream grammar, only enough verbs to keep substrate visible during a review.

---

## Energy movement 🌊

| Primitive | Meaning |
|---|---|
| `DRIVES` | A pushes B's state in a direction; remove A and B relaxes. |
| `DAMPS` | A reduces the amplitude or rate of B without removing it. |
| `FEEDS` | A supplies the resource B's process consumes. |
| `DISSIPATES` | Energy/structure leaves the system, not transferred elsewhere. |

## Coupling 🔗

| Primitive | Meaning |
|---|---|
| `COUPLES` | A and B share state such that change in one shifts the other. |
| `MEDIATES` | C carries the influence between A and B; remove C and the link breaks. |
| `MODULATES` | A changes B's responsiveness without driving B directly. |
| `AMPLIFIES` | A increases B's effect without being its source. |
| `SHIELDS` | A blocks or attenuates a coupling that would otherwise hold. |

## Phase / coherence 〰️

| Primitive | Meaning |
|---|---|
| `PHASE_LOCKS` | A and B settle into a fixed relative timing. |
| `RESONATES` | A and B share a natural frequency and reinforce each other on it. |
| `SYNCHRONIZES` | A and B align timing without necessarily locking. |
| `DECOHERES` | A previously coherent relation loses its phase relationship. |

## Thresholds 🚪

| Primitive | Meaning |
|---|---|
| `CONSTRAINS` | A bounds the space B can occupy. |
| `THRESHOLDS` | Behavior changes qualitatively past a level, not gradually. |
| `SATURATES` | Past a level, additional input produces no additional response. |
| `HYSTERETIC` | The path in differs from the path out; history is part of state. |

## Disruption ↯

| Primitive | Meaning |
|---|---|
| `BIFURCATES` | The system splits into two qualitatively different regimes. |
| `DESTABILIZES` | A previously stable state becomes a transient. |

---

## Usage in audits

When a reviewer (human or AI) writes an audit note, prefer the primitive over the noun-form:

- ❌ *"The override caused trust degradation."*
- ✅ *"The override `DAMPS` clarity; trust `THRESHOLDS` at 0.85; below that, override rights `BIFURCATE` back to the human."*

The second form is longer, but it (a) names the mechanism, (b) is checkable against the system's actual behavior, and (c) survives translation across communities that disagree about what "trust" means as a noun.

---

## Mapping to existing protocol metrics

| Existing metric | Primitive form |
|---|---|
| `clarity_score` drops below 0.90 | clarity `DAMPS` past `THRESHOLDS`; override `BIFURCATES` to human. |
| `trust_score` floor at 0.85 | trust `SATURATES` downward; cannot decay further without explicit consent event. |
| Violation penalty −0.05 | violation `DRIVES` trust downward by a fixed step. |
| Cognition cycle (7 stages) | dissonance `DRIVES` curiosity → curiosity `FEEDS` collection → ... → settling `DAMPS` the cycle (temporarily). |

---

## Protocol Hooks

- **Logs:** Optional `relations` array on capsules listing `{source, primitive, target, strength}` triples for the event.
- **Audits:** When a noun-form claim is made (e.g. "the model was deceptive"), require it to be expressible as at least one primitive triple. If it cannot, flag the claim as unverifiable surface.
- **Swarms:** Agents may negotiate disagreements at the primitive level even when their noun-level vocabularies differ.
