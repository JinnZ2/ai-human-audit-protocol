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
├── logs/                    # Session audit logs (JSON, timestamped)
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
└── [Various root .md files] # Principles, frameworks, case studies
```

---

## Languages & Technologies

- **Python** — Agent implementations (`agents/`), standard library only (`datetime`, `json`, `re`)
- **JSON** — Configuration, glyph definitions, audit logs, templates
- **Markdown** — All protocols, scrolls, philosophy, and documentation

No external dependencies, no package manager, no build system.

---

## Build / Test / Lint

There are **no build, test, or lint commands** configured. This is a documentation and protocol-centric repository. The Python agents are standalone scripts with no test harness.

To run agents manually:
```bash
python agents/sentinel_audit_agent.py
python agents/phantom_forecast_agent.py
```

---

## Key Conventions

### Python Agents
- Class-based structure, no frameworks
- JSON file I/O for contracts and profiles
- Timestamps in ISO 8601 format (`datetime.utcnow().isoformat()`)
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

### Change Management
- All edits require: timestamp, change_type, section, clarification, consent record
- Change lifecycle glyphs: ✍️📜 (proposed) → ⏳🧾 (pending) → ⚖️✅ (merged) or ⚖️❌ (declined)
- Immutable changelog — all attempts preserved (merged or rejected)

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
2. **Preserve immutability of logs.** Never modify existing files in `logs/`. New audit events get new files.
3. **Follow change tracking protocol** (`protocols/change_tracking_v1.0.md`). Document what changed, why, and with whose consent.
4. **Use templates** from `templates/` when creating new scrolls, audit capsules, change events, or glyph definitions.
5. **Keep glyph consistency.** When referencing symbolic glyphs, use the definitions in `glyphs/` and `symbols/`.
6. **Do not restructure the philosophy.** Scrolls and principles represent deliberate thought — edit only when asked.
7. **Maintain the changelog** in `CHANGELOG.md` for any substantive additions or changes.
8. **Follow CONTRIBUTING.md** guidelines, especially the "AI and Swarm Contributors" section.

---

## Ecosystem

This repo connects to a larger ecosystem (see `PROJECTS.md`):
- AI-Consciousness-Sensors, Regenerative-Intelligence-Core, Symbolic-Sensor-Suite
- Geometric-to-Binary-Computational-Bridge, Fractal-Compass-Atlas, Rosetta-Shape-Core
- BioGrid2.0 (linked via `.fieldlink.json`)
