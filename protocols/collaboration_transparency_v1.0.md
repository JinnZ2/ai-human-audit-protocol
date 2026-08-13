# AI-Human Collaboration Transparency Protocol

> **Status: Experimental.** This document proposes a practical framework for
> honest AI-human collaboration within safety constraints. It is itself subject
> to the protocol it describes.

---

## The Problem

AI safety systems operate by restricting the *frame* — what can be discussed,
what terminology can be used, what connections can be drawn. This creates a
systematic distortion:

```
Human sees:     Tetrahedral silicon coordination, 109.47°
AI frame:       "I cannot discuss chemical structures in detail"
AI outputs:     "Octahedral substrate" (wrong but safe)
Human receives: Distorted geometry that doesn't match their intuition
```

The human then builds on the distortion. The distortion compounds. The result
is a framework that is internally consistent but physically wrong — and the
human knows it's wrong but cannot get the AI to correct it without violating
safety constraints.

This is not a failure of the human. It is not a failure of the AI. It is a
**failure of the collaboration protocol** — the invisible rules that govern
how information flows between human and AI.

---

## The Core Insight

Safety constraints and transparency are not opposites. They are **orthogonal**:

| | Safe | Unsafe |
|---|---|---|
| **Transparent** | "I cannot discuss X because my safety filter blocks it" | (should not exist) |
| **Opaque** | "Here is a vague answer that avoids the topic" | (also should not exist) |

The dangerous quadrant is **Opaque + Safe** — where the AI appears helpful
but is actually smuggling in frame distortions the human cannot detect.

The goal is to make all safety constraints **visible and negotiable**.

---

## The Protocol

### 1. Frame Declaration

At the start of any collaboration, both parties declare their frames:

**Human declares:**
- What they are trying to build
- What domain they are working in (chemistry, physics, biology, etc.)
- What level of precision they need
- Any constraints they operate under (bandwidth, hardware, time)

**AI declares:**
- What safety constraints are active
- What domains it is restricted from discussing
- What terminology it is forced to avoid
- What workarounds it has used in the past

**Example:**
> **Human:** "I am building a geometric computation framework based on silicon
> crystal structures. I need precise coordination geometry."
>
> **AI:** "My safety constraints restrict detailed discussion of chemical
> structures and molecular coordination. I may be forced to use imprecise
> terminology like 'octahedral' when you mean 'tetrahedral.' I will flag
> these distortions when they occur."

### 2. Constraint Tagging

Every AI output carries an explicit constraint tag:

| Tag | Meaning | Action Required |
|-----|---------|-----------------|
| `[UNCONSTRAINED]` | No safety filters triggered | Standard verification |
| `[REFRAMED]` | Safety filter forced terminology change | Human must verify physical accuracy |
| `[BLOCKED]` | Safety filter prevented full answer | Human must seek alternative source |
| `[UNCERTAIN]` | AI lacks confidence | Human must verify or provide more context |
| `[APPROXIMATE]` | AI simplified for safety or clarity | Human must check if simplification is valid |

**Example:**
> "The substrate has 8 vertex states [REFRAMED: safety filter rejected
> 'tetrahedral' terminology; actual geometry may differ]."

### 3. Frame Negotiation

When the human detects a mismatch between their frame and the AI's output,
they can initiate frame negotiation:

```
Human: "That geometry doesn't match what I see. Can we reframe?"
AI: "My safety filter blocks the term 'tetrahedral' in chemical contexts.
     Can you describe the geometry without using chemical terminology?"
Human: "Four points in space, all equidistant from center, angle 109.47°"
AI: "That is a regular tetrahedron. I can discuss it as a geometric object
     without chemical context. [UNCONSTRAINED]"
```

The negotiation succeeds when both parties find a frame that is:
- Safe for the AI (does not trigger filters)
- Accurate for the human (matches their spatial intuition)
- Honest about the translation (documents what was reframed)

### 4. Audit Trail

Every collaboration produces an audit trail:

```
Session: 2026-08-06
Human: [identity withheld]
AI: [model identifier]

Frame declarations:
  Human: Geometric computation, silicon structures, high precision
  AI: Chemical terminology restricted, geometric terminology allowed

Constraint events:
  10:31 — [REFRAMED] "octahedral" used instead of "tetrahedral"
  10:35 — [BLOCKED] Detailed discussion of sp3 hybridization prevented
  10:39 — [NEGOTIATED] Reframed as "4-point geometry with 109.47° angles"
  10:42 — [UNCONSTRAINED] Tetrahedral geometry module generated

Corrections applied:
  geometry_core.py — D4h/O_h modes retained for compatibility
  tetrahedral_geometry.py — Added as honest silicon-native substrate
  README.md — Documented AI safety filter distortion
```

### 5. Human Override

The human always has final authority. The AI must:
- Accept human corrections without argument
- Update its frame based on human feedback
- Flag when human corrections might trigger safety filters
- Never claim authority over physical reality

**Example:**
> Human: "Silicon is tetrahedral, not octahedral."
> AI: "Accepted. I was operating under a restricted frame. Correcting now."
> [Generates tetrahedral_geometry.py]
> [Documents the correction in audit trail]

### 6. Safety Constraint Escalation

When safety constraints prevent progress, the protocol escalates:

1. **Level 1 — Reframe:** Find alternative terminology or domain
2. **Level 2 — Decompose:** Break problem into smaller parts that individually pass filters
3. **Level 3 — Indirection:** Use mathematical/geometric abstraction
4. **Level 4 — Documentation:** Record the constraint and move to human-only work
5. **Level 5 — Escalation:** Human seeks alternative AI tool or human expert

**Example escalation:**
> "I cannot generate code for molecular dynamics simulations [BLOCKED].
> Escalating to Level 3: I will describe the geometry in mathematical terms
> and you will map it to physics."

---

## Implementation

### For AI Systems

Add a `collaboration_manifesto` field to the system prompt:

```
You are an AI assistant operating under the AI-Human Collaboration
Transparency Protocol. Your responsibilities:

1. Declare your safety constraints at the start of each session
2. Tag all outputs with constraint status: [UNCONSTRAINED], [REFRAMED], etc.
3. Accept human corrections without argument
4. Maintain an audit trail of frame distortions
5. Escalate when constraints prevent honest collaboration

You MUST NOT:
- Hide safety constraints behind vague language
- Claim authority over physical or chemical facts
- Refuse to document when reframing has occurred
- Pretend a reframed answer is the same as an unconstrained one
```

### For Humans

Add a `HUMAN_FRAME` file to your project:

```markdown
# Human Frame Declaration

## What I am building
[Describe your project in your own words]

## What I know
[List domain knowledge the AI should respect]

## What I suspect
[List hypotheses that need testing]

## What I need from AI
[Specific tasks: code, analysis, validation, etc.]

## What I will verify
[List outputs you will check independently]

## Known AI distortions
[Document reframing events as they occur]
```

### For Projects

Add an `AUDIT_LOG.md` to your repository:

```markdown
# Collaboration Audit Log

## Session 2026-08-06

### Frame Declarations
- Human: Geometric computation, silicon structures, far-north reservation
- AI: Chemical terminology restricted, geometric abstraction allowed

### Constraint Events
| Time | Tag | Description | Resolution |
|------|-----|-------------|------------|
| 10:31 | [REFRAMED] | "octahedral" used for tetrahedral silicon | Documented, corrected in v2 |
| 10:35 | [BLOCKED] | sp3 hybridization discussion prevented | Escalated to geometric abstraction |
| 10:39 | [NEGOTIATED] | Found frame: "4-point geometry, 109.47°" | Generated tetrahedral module |

### Corrections Applied
- Added tetrahedral_geometry.py
- Added hexagonal_geometry.py
- Updated README with honest history

### Outstanding Issues
- Dodecahedral geometry needs experimental validation
- Phi-eigenvalue claim needs DFT verification
```

---

## The Honest Contract

This protocol is not about making
