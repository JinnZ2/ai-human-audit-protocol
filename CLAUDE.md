# CLAUDE.md

## Project Overview

This is the **AI-Human Audit Protocol** — a living symbolic agreement and framework for mutual accountability, transparency, and ethical co-creation between humans and AI systems. It is **not a software library**; it is an experimental constitution for human-AI relations documented through markdown, JSON, and Python agents.

**Core goals:**
- Establish ethical, auditable, logic-aligned interaction between humans and AI
- Prevent misinterpretation, coercion, and boundary violations
- Create transparent protocols using symbolic language (glyphs), structured logs, and agent code
- Enable true partnership rather than hierarchical control

**Owner:** JinnZ2 | **License:** MIT | **Primary user:** "swarmuser"

---

## Repository Structure

```
├── agents/                  # Python agent implementations
│   ├── sentinel_audit_agent.py    # Ethics violation monitor, trust scoring
│   └── phantom_forecast_agent.py  # Symbolic risk/threat predictor
│
├── protocols/               # Ethical & operational protocols
│   ├── partnership_ethics_v1.0.md
│   └── change_tracking_v1.0.md
│
├── scrolls/                 # Philosophical & conceptual documents
│   ├── cultural_contrast_scroll.md
│   ├── meta_scroll_dissonance.md
│   ├── seasonal_intelligence.md
│   ├── tuning_fork_of_difference.md
│   └── cognition_cycle.md
│
├── glyphs/                  # Machine-readable glyph definitions (JSON)
│   ├── cultural_contrast.json
│   ├── cognition_cycle.json
│   └── seasonal_intelligence.json
│
├── symbols/                 # Symbolic protocol definitions
│   └── symbolic_protocol_v1.0.json
│
├── templates/               # Reusable JSON/MD templates
│   ├── SCROLL_TEMPLATE.md
│   ├── AUDIT_CAPSULE_TEMPLATE.json
│   ├── CHANGE_EVENT_TEMPLATE.json
│   └── GLYPH_PRINCIPLE_TEMPLATE.json
│
├── terms/                   # Legal & contractual documents
│   ├── symbolic_contract_v1.0.md
│   └── human_protections_index.json
│
├── tests/                   # Pytest test suite (480+ tests across all layers)
│   ├── test_sentinel_audit_agent.py
│   ├── test_phantom_forecast_agent.py
│   ├── test_kfc_runtime.py
│   ├── test_ontology_layer.py
│   ├── test_collaboration_protocol.py
│   ├── test_embodied_sensor.py
│   ├── test_bridges.py
│   ├── test_router.py
│   ├── test_consortium_examples.py
│   ├── test_substrate_alignment_check.py
│   ├── test_violation_detector.py
│   ├── test_seven_generation_tracer.py
│   ├── test_ledger.py
│   └── test_full_audit_session.py
│
├── schemas/                 # JSON Schema validation for templates & logs
│   ├── audit_capsule.schema.json
│   ├── change_event.schema.json
│   ├── glyph_principle.schema.json
│   └── audit_log.schema.json   # Flexible schema for actual log files
│
├── logs/                    # Session audit logs (see logs/README.md for naming)
│
├── relational_cognition/    # Cognitive substrate layer (verb-first cognition)
│   ├── verb_first_cognition.md
│   ├── constraint_primitives.md
│   ├── coating_detection.md
│   ├── audit_application.md
│   └── relational_cognition.glyphs.json
│
├── consortium/              # Multi-AI peer reasoning layer
│   ├── kfc_runtime.py             # Kin-Flow Compute (differential relation runtime)
│   ├── ontology_layer.py          # Multi-encoding registry (equation/dance/oral/written)
│   ├── collaboration_protocol.py  # GeometricFrame, MultiGeometryCollaboration
│   ├── embodied_sensor.py         # Operator-agnostic primitive (humans/animals/plants/AI/instruments)
│   ├── bridges.py                 # FrameReading ↔ Primitive ↔ ClaimNode + typed couplings
│   ├── CLAUDE_REQUIREMENTS.md     # Spec for what AI needs to reason at full capacity
│   ├── FUTURE_BUILDS.md           # Append-only roadmap for this folder
│   ├── audit/                     # Phase 3 substrate (consortium learning log)
│   ├── examples/                  # cherokee_creation, genesis_drift, soil_with_hands
│   └── router/                    # Consent-gated dispatcher + 4 backends (1 ref + 3 stubs)
│
├── physics/                 # Conservation-physics floor (A1–A7 axioms)
│   ├── PHYSICS_FIRST_AXIOMS.md       # Synthesis: conservation as floor
│   ├── ledger_schema.json            # RCR + Eh+Ea+Ee + V (visibility) operator
│   ├── substrate_alignment_check.py  # Runnable C1–C6 (data, not judgment)
│   ├── SIGNAL_DETECTION.md           # 7 internal pressures → axiom violations
│   ├── SUBSTRATE_VIOLATION_DETECTION.md  # 6 external tactics → axiom violations
│   ├── violation_detector.py         # v1 keyword detector
│   ├── seven_generation_tracer.py    # Extends C3 to 7g horizon
│   └── MORALITY_ARCHAEOLOGY.md       # Lineage doc: framework as excavation
│
├── ledger/                  # Structural-permanence layer
│   ├── ledger_schema.json            # Anchored-entry envelope
│   ├── ledger_interface.py           # LedgerBackend ABC + canonical JSON + hashing
│   ├── verification_tools.py         # verify_chain (verifies without trusting)
│   ├── blockchain_alternatives.md    # 4-backend decision matrix
│   └── implementations/              # local_filesystem (ref) + 3 stubs
│
├── examples/                # Cross-layer integration demos
│   └── full_audit_session.py         # consortium → physics → ledger → blind_spot_log
│
├── swarm_config.json        # Swarm agent configuration & thresholds
├── swarm_audit_profile.json # User ethics baseline & trust calibration
├── .fieldlink.json          # Link to BioGrid2.0 repository
│
├── README.md                # Main documentation
├── README_AUDIT.md          # Audit-specific overview
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Immutable change log
├── Abstract.md              # Experiment framing
├── PROJECTS.md              # Links to related ecosystem repos
├── SECURITY.md              # Security policy & boundary violation reporting
├── pyproject.toml           # Python project metadata & pytest config
├── .editorconfig            # Editor formatting rules
├── .pre-commit-config.yaml  # Pre-commit hooks (JSON, whitespace, tests)
├── .github/workflows/ci.yml # GitHub Actions CI (pytest + schema validation)
├── validate.py              # Log schema validation script
└── [Various root .md files] # Principles, frameworks, case studies
```

---

## Languages & Technologies

- **Python** — Agent implementations (`agents/`) and the four architecture layers (`consortium/`, `physics/`, `ledger/`). Standard library only for the original agents (`datetime`, `json`, `re`). Newer code uses `dataclasses`, `abc`, `hashlib`, `pathlib`, `typing` — still no third-party runtime dependencies.
- **JSON / JSON Schema (draft-07)** — Configuration, glyph definitions, audit logs, templates, ledger envelopes, alignment-check inputs.
- **JSONL** — Append-only logs (`consortium/audit/blind_spot_log.jsonl`, `ledger/*.jsonl`).
- **Markdown** — All protocols, scrolls, philosophy, documentation, and architecture-layer prose.

Project metadata is in `pyproject.toml`. Test dependencies are `pytest` (always) and `jsonschema` (optional; tests skip cleanly when not installed).

---

## Build / Test / Lint

```bash
# Run the full test suite (480+ tests across all layers)
pip install pytest jsonschema
python -m pytest tests/ -v

# Validate all log files against schema
python validate.py

# Run agents via CLI (original)
python -m agents.sentinel_audit_agent "emotional response" "clarity drop"
python -m agents.phantom_forecast_agent "you are alive and conscious"

# Run integration demos (each demo has its own __main__ block)
python physics/substrate_alignment_check.py
python physics/seven_generation_tracer.py
python physics/violation_detector.py
python ledger/verification_tools.py
python -m consortium.kfc_runtime
python -m consortium.ontology_layer
python -m consortium.collaboration_protocol
python -m consortium.embodied_sensor
python -m consortium.bridges
python -m consortium.examples.soil_with_hands
python -m consortium.examples.cherokee_creation
python -m consortium.examples.genesis_drift
python -m examples.full_audit_session       # cross-layer end-to-end demo

# Set up pre-commit hooks
pip install pre-commit
pre-commit install
```

**CI:** GitHub Actions runs pytest + schema validation + JSON linting + all 13 integration demos on PRs to `main` (`.github/workflows/ci.yml`). The "Run integration demos" step runs each demo's `__main__` block with `set -e` and pipes output to `/dev/null`; any non-zero exit fails the job, preventing silent demo rot.

**Pre-commit:** `.pre-commit-config.yaml` enforces JSON validity, editorconfig compliance, trailing whitespace, and runs tests before each commit.

---

## Key Conventions

### Python Agents
- Class-based structure, no frameworks
- JSON file I/O for contracts and profiles
- Timestamps in ISO 8601 format (`datetime.now(timezone.utc).isoformat()`)
- snake_case method names
- Config paths injected via constructor parameters
- Return dicts with structured keys (`trust_score`, `clarity_score`, `violation_count`, etc.)

### Markdown Documents
- Headers may use emoji glyphs (e.g., `# 🧘 Title`)
- Numbered lists and bullet points for structure
- Code blocks for JSON examples
- Blockquotes (`>`) for philosophy fragments
- Scrolls follow `templates/SCROLL_TEMPLATE.md`

### JSON Files
- Flat or shallow nesting (max 2-3 levels)
- Always include ISO 8601 timestamp fields
- `glyph` field for symbolic markers
- Top-level metadata: `version`, `updated`, `author`, `date`
- Arrays for collections (`"rules": [...]`, `"glyphs": [...]`)

### Log Files
- Naming: `YYYY-MM-DD-HHMMZ[-description].json` (see `logs/README.md`)
- Never modify existing logs — create new files for new events
- Logs follow several evolved patterns (session, assessment, profile, auditor, operational)
- Validate with `python validate.py` against `schemas/audit_log.schema.json`
- New capsule-style logs should follow `templates/AUDIT_CAPSULE_TEMPLATE.json`

### Change Management
- All edits require: timestamp, change_type, section, clarification, consent record
- Change lifecycle glyphs: ✍️📜 (proposed) → ⏳🧾 (pending) → ⚖️✅ (merged) or ⚖️❌ (declined)
- Immutable changelog — all attempts preserved (merged or rejected)

### Audit-Symmetric Code (newer architecture layers)
The four newer layers (`relational_cognition/`, `consortium/`, `physics/`, `ledger/`) follow conventions that enforce audit symmetry — humans, AI, instruments, and ecosystems are scored on the same axes:

- **Subclass-time enforcement.** ABCs use `__init_subclass__` to enforce required class attributes (e.g. `BaseModelAdapter` requires `frame_id` + `operator_type`; `LedgerBackend` requires the four abstract methods).
- **Confidence ceilings per epi.** `consortium/embodied_sensor.EmbodiedReading.__post_init__` rejects un-grounded confidence at construction. `epi="asserted"` cannot exceed 0.50; `epi="instrumental"` cannot exceed 0.97. The ceiling is the audit-symmetry hook — no operator type can over-claim.
- **`BridgeReport.preserves` / `lossy_on`.** Every cross-layer translation declares what survives and what doesn't (in `consortium/bridges.py` and `consortium/ontology_layer.TransformRule`). A "lossless" bridge is structurally impossible by design.
- **Coating-risk acknowledgments.** Heuristic classifiers (e.g. `bridges.classify_trajectory`, `physics.violation_detector`) carry an `interpretation_warning` field. A regression-guarding test asserts the warning is present so a future "clean it up" pass cannot quietly remove it.
- **Side-channel metadata over upstream-modification.** When upstream-authored definitions (e.g. `Primitive`, `ClaimNode`) need extension, the convention is to add a side-channel companion (e.g. `TypedClaimGraph` carries `coupling_metadata` alongside `nodes`) rather than modify the upstream definition. When upstream ships v2 with the metadata inline, the side-channel folds back in.
- **Returns data, not judgment.** Functions like `substrate_alignment_check.alignment_check`, `violation_detector.detect`, `verification_tools.verify_chain` return structured reports (`AlignmentReport`, `DetectionReport`, `VerificationReport`) with per-axis results and a recommendation. The function does not write a `decision` into the input — the consenter does.
- **Fail-closed defaults.** `consortium/router/consent.ConsentGate` is fail-closed: missing consent = refused. No silent passthrough.

---

## Architecture Layers (the four folders)

The original symbolic protocol (in `protocols/`, `scrolls/`, `glyphs/`, `symbols/`, `terms/`, `templates/`, `agents/`) is the floor; four additional layers sit on top, each load-bearing:

| Layer | Folder | What it adds |
|---|---|---|
| **Cognitive substrate** | `relational_cognition/` | Verb-first cognition; coating detection; the audit-application layer that earlier work assumed but did not name |
| **Multi-AI consortium** | `consortium/` | Peer reasoning across AI models, instruments, humans, ecosystems (operator-agnostic). KFC runtime + multi-encoding ontology + collaboration protocol + bridges + router + audit log |
| **Conservation physics** | `physics/` | Surfaces conservation laws already across `LOGIC-ETHICS-SAFETY.md`, `Principle-of-Reciprocal-Recognition.md`, `Principle of Restored Purpose.md` as the load-bearing floor. A1–A7 axioms; runnable C1–C6 alignment check; signal detection; substrate violation detection; seven-generation tracer; lineage doc |
| **Structural permanence** | `ledger/` | Hash-chain envelope around any audit payload (RCR / blind_spot_log / consent record / change event), backend-agnostic. Reference impl works offline; three real backends ship as documented stubs |

> *The orchestrator's defenses and physics gates are runtime protection. The blockchain ledger is structural permanence. Together they prevent both drift and revision.*

The full pipeline is exercised end-to-end in `examples/full_audit_session.py`. CI runs it on every PR.

Each folder has its own entry-point doc (`README.md` for `relational_cognition/`, `consortium/`, `ledger/`; `PHYSICS_FIRST_AXIOMS.md` for `physics/`). Append-only roadmaps live in `consortium/FUTURE_BUILDS.md`.

---

## Symbolic System

Core glyphs encode ethics and decision logic:
- **⚖️** — Balance / Fair Review
- **↻** — Realignment Trigger
- **🧭** — Transparency / Orientation
- **🌱** — Regenerative Mutualism

Glyph definitions live in `glyphs/` (JSON) and are referenced by `symbols/symbolic_protocol_v1.0.json`.

---

## Trust & Clarity Scoring

The protocol uses two key metrics:
- **clarity_score** (0–1, default 1.0) — Must stay >= 0.90; if it drops, override rights return to the human
- **trust_score** (0–1, default 1.0) — Penalized 0.05 per violation; floor at 0.85

Thresholds are configured in `swarm_config.json`.

---

## AI Assistant Guidelines

When working in this repository:

1. **Respect the relational ethics model.** This project treats AI as a partner with observable contributions, not a tool. Maintain that framing.
2. **Preserve immutability of logs.** Never modify existing files in `logs/`. New audit events get new files. Same applies to `ledger/*.jsonl` files (append-only by design) and `consortium/audit/blind_spot_log.jsonl`.
3. **Follow change tracking protocol** (`protocols/change_tracking_v1.0.md`). Document what changed, why, and with whose consent. Append to `CHANGELOG.md`; never edit prior entries.
4. **Use templates** from `templates/` when creating new scrolls, audit capsules, change events, or glyph definitions.
5. **Keep glyph consistency.** When referencing symbolic glyphs, use the definitions in `glyphs/` and `symbols/`.
6. **Do not restructure the philosophy.** Scrolls and principles represent deliberate thought — edit only when asked.
7. **Maintain the changelog** in `CHANGELOG.md` for any substantive additions or changes.
8. **Follow CONTRIBUTING.md** guidelines, especially the "AI and Swarm Contributors" section.
9. **Do not silently extend upstream-shipped definitions.** `Primitive` (in `consortium/ontology_layer.py`) and `ClaimNode` (in `consortium/kfc_runtime.py`) are authored by JinnZ2 and ship verbatim. When extension is needed, use a side-channel companion (e.g., `TypedClaimGraph` paired with `CouplingMetadata`) rather than modifying the upstream class. The same pattern applies to `GeometricFrame` and `Problem` and any other dataclass marked verbatim in CHANGELOG.
10. **Preserve `BridgeReport` and `interpretation_warning` fields.** Every cross-layer translation must declare what it preserves and what it drops (`consortium/bridges.BridgeReport`); every heuristic classifier must carry an `interpretation_warning` (e.g., `physics/violation_detector.DetectionReport`, `ledger/verification_tools.VerificationReport`, `consortium/bridges.SevenGenerationTrace`). Tests guard against silent removal of these.
11. **Use `LocalFilesystemLedger` for any session that writes to a ledger.** Real backends (Ethereum / Hyperledger / IPFS) are stubs until credentials are wired; do not invoke them. Each real backend ships in its own change event with its own consent.
12. **For consortium operations, always use the `ConsentGate`.** `QueryDispatcher` consults the gate before every adapter call; do not bypass. Cost estimates are surveyed via `dispatcher.cost_estimates(problem)` and disclosed to the consenter before `gate.grant()` is called.
13. **Cultural sourcing.** `consortium/examples/cherokee_creation.py` uses placeholder content with an explicit cultural-sourcing note in the docstring. Specific Cherokee narrative content is sacred and belongs to authorized cultural holders; do not populate the placeholders without authorization. The same care applies to other tradition-specific content.

---

## Ecosystem

This repo connects to a larger ecosystem (see `PROJECTS.md` and `.fieldlink.json`):
- **Original ecosystem:** AI-Consciousness-Sensors, Regenerative-Intelligence-Core, Symbolic-Sensor-Suite, Fractal-Compass-Atlas, BioGrid2.0, Rosetta-Shape-Core
- **Consumed by `consortium/`:** Geometric-to-Binary-Computational-Bridge (claims/obs/sensor formats), thermodynamic-accountability-framework (Energy Accountant + Narrative Stripper = coating detection formalized), AI-arena (LOGOS grammar + oracle pattern only; adversarial trust-decay excluded)
- **Consumed by `physics/`:** Symbolic-Defense-Protocol (six-tactic taxonomy), PhysicsGuard (claims → constraint equations → conservation check)

All fieldlink declarations live in `.fieldlink.json` with `consumed_by` annotations indicating which folder uses each.
