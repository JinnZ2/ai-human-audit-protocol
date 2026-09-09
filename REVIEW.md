# REVIEW.md — AI-Human Audit Protocol vs. CLAUDE.md

> Scope note. This review was run against commit `4174a7a` (main) by the 2026-09-09 update pass, under the standing instruction in CLAUDE.md §"You are reviewing…". It does not cover the files that same pass added (`physics/decision_anchor_check.py`, `schemas/case_provenance.schema.json`, `logs/2026-09-09-0000Z-case-provenance.json`, `WORKORDER_update_pass_C1-C5.md`). Section 4 is suggestion only; the update-pass work order forbids folder consolidation, renames, or reorganization, so nothing there was executed. Nothing in this file describes any person; it describes files and code.


Reviewed at commit `4174a7a` (branch `claude/audit-protocol-update-pass-nqfps3`), 2026-09-09. Read-only pass; nothing in the repository was modified. Every claim below was verified with grep/ast/pytest/`python -c` unless marked "not verified".

---

## 1. Inconsistencies

### 1.1 Naming conventions
- **Python:** all `.py` files are snake_case (verified: `find . -name "*.py" | grep -vE '/[a-z0-9_]+\.py$'` returns nothing). One spelling issue: `testing/unified_collapse_theorum.py` ("theorum").
- **Markdown:** CLAUDE.md does not state an `.md` naming rule; in practice subfolders use snake_case (`scrolls/`, `protocols/`, `relational_cognition/`) while root has mixed styles. Four root files contain spaces and one contains a colon, which breaks shell globbing and some Windows checkouts:
  - `AI-Human Partnership Framework for Extreme Conditions.md`
  - `Cultural Bias in AI Assessment: How Traditional Trauma Processing Gets Pathologized.md`
  - `Principle of Restored Purpose.md`
  - `Protection protocol.md`
- Other root `.md` files mix Title-Case (`Elder.md`, `Co-creation.md`, `Organize.md`, `Organize2.md`) with SCREAMING-KEBAB (`LOGIC-ETHICS-SAFETY.md`). See §4 for the (non-executed) suggestion.

### 1.2 Import order / third-party imports
- **Import order** stdlib → third-party → local: 0 violations across `agents/ consortium/ physics/ ledger/ audits/ knowledge_archaeology/ testing/ examples/` + root scripts (AST check, 100+ files).
- **Third-party runtime imports:** none. Only `pytest`/`jsonschema` in `tests/`. Matches CLAUDE.md "no third-party runtime dependencies".
- **Bare sibling imports break package import** (script-style imports that only work when the file's own directory is on `sys.path`):
  - `physics/reference_frame.py:13` — `from frame_projection import project, compare_projections`
  - `physics/reference_frame_drift.py:9` — `import reference_frame`
  - `physics/reference_frame_bridge.py:12` — `import reference_frame`
  - Verified: `python -c "import physics.reference_frame"` → `ModuleNotFoundError: No module named 'frame_projection'`. CI only passes because it runs `python physics/reference_frame.py` / `(cd physics && python …)` (`ci.yml:65-67`). Fix (each file):
    ```python
    try:
        from physics.frame_projection import project, compare_projections
    except ImportError:  # run as a script from inside physics/
        from frame_projection import project, compare_projections
    ```

### 1.3 Audit-symmetric conventions (four layers)
| Convention | Status | Evidence |
|---|---|---|
| Confidence ceilings per epi | Present, but mutable after construction | `consortium/embodied_sensor.py:113` `@dataclass` is not frozen; see §3.1 |
| `BridgeReport.preserves / lossy_on` | Present on every bridge | `consortium/bridges.py:96-106,236,298,372` |
| `interpretation_warning` on heuristic classifiers | Present on 3 of the CLAUDE.md-named modules; **absent on `bridges.classify_trajectory`** (CLAUDE.md §"Audit-Symmetric Code" says it carries one) | `bridges.py:836` uses `assumptions_required=["trajectory_classification=heuristic_v1", …]` + `notes=` instead; guarded by `tests/test_bridges.py:598-599`. Documentation/code mismatch, not a missing guard. |
| Side-channel metadata | Upheld | `TypedClaimGraph`/`CouplingMetadata` in `bridges.py`; upstream classes unchanged (§1.5) |
| Fail-closed defaults | Verified at runtime | `QueryDispatcher([MockAdapter(f)]).fan_out(problem)` with no grant → `refused: 1, readings: 0` |
| Returns data, not judgment | Upheld | `substrate_alignment_check.py:13-14,56,339`, `violation_detector.py:17`; no `decision` written into inputs |

- Newer physics/audits heuristics with **no caveat field at all** (neither `interpretation_warning` nor `assumptions_required`): `physics/flow_static_axis.py:82 classify()` (returns a bare dict with `kind: flow|static`), `audits/substrate_aware_audit.py:474 detect_substrate_acknowledgment()` (returns a bare `bool`). Ready-to-paste for `flow_static_axis.classify`:
    ```python
    INTERPRETATION_WARNING = ("heuristic_v1: 'flow'/'static' thresholds (0.5, 0.35) are "
                              "uncalibrated; classification is a frame imposed on capacities.")
    # inside classify(): add to the returned dict
    "interpretation_warning": INTERPRETATION_WARNING,
    ```

### 1.4 Template usage
- **Scrolls:** `templates/SCROLL_TEMPLATE.md` requires `**Glyphs:**`, `**Thesis:**`, `**Body:**`, `**Protocol Hooks:**`. 0 of 6 scrolls have `**Thesis:**` or `**Protocol Hooks:**`; only `scrolls/seasonal_intelligence.md` has `**Glyphs:**`. `scrolls/operation_unit_instance.md` is not listed in CLAUDE.md's tree.
- **Audit capsules:** `templates/AUDIT_CAPSULE_TEMPLATE.json` keys = `analysis, audit_id, context, event, outcome, signals, timestamp`. 0 of 14 files in `logs/` use this shape (they follow the five "evolved patterns" that `schemas/audit_log.schema.json` tolerates). `logs/2026-06-20-1344Z-calibration.json` (post-template) uses `context, convergence, is_trajectory_point, …` — also not capsule-shaped.
- **Change events:** `templates/CHANGE_EVENT_TEMPLATE.json` has no instances anywhere outside `templates/` and `schemas/` (grep `change_type` in `*.json`). CHANGELOG.md is prose-only.
- **Glyphs:** `templates/GLYPH_PRINCIPLE_TEMPLATE.json` keys = `glyphs, principle, protocol, updated, version`. `glyphs/seasonal_intelligence.json` matches; `glyphs/cultural_contrast.json` lacks `principle, protocol`; `glyphs/cognition_cycle.json` uses `cycle` instead of `glyphs`.

### 1.5 Append-only logs and upstream classes
- **`logs/` was modified once after creation:** commit `a731f78` (2026-03-21) rewrote `logs/2025-08-30-1930Z.json` and `logs/2025-09-23-0000Z.json` (typographic → straight quotes so they parse as JSON). Content-preserving, but it violates the letter of "never modify existing logs" and there is no CHANGELOG consent record naming those two files (not verified beyond grep of CHANGELOG for the filenames — none found).
- `ledger/*.jsonl`: none tracked in git. `consortium/audit/blind_spot_log.jsonl` (named in CLAUDE.md:141 and :283) **does not exist**; only `consortium/audit/example_blind_spot_log.jsonl` (never modified).
- **Upstream classes unchanged:** `ClaimNode` (`kfc_runtime.py`, 1 commit), `Primitive` (`ontology_layer.py`, 1 commit), `GeometricFrame`/`Problem` (`collaboration_protocol.py:16,35`; second commit `7a95b8d` touched hunks at lines 74+, 101+, 152+, 432+ only — `REVERSIBILITY_RANK` and `synthesize()`; class bodies at 15-52 untouched).

### 1.6 CI
- `.github/workflows/ci.yml:33-68`: "Run integration demos" uses `set -e` and runs 33 demo commands; any non-zero exit fails the job. `json-lint` job (`:70-78`) validates every `*.json`; verified that `exit 1` inside the piped `while` loop does propagate (pipeline status 1).
- CI runs 33 demos; CLAUDE.md:186 says "all 13 integration demos" — stale.
- `testing/` (6 files, ~1900 lines) is not exercised by CI or any test (`grep -rl "testing\." tests/ ci.yml` → none).

### 1.7 License statements conflict
- `LICENSE` = MIT; `pyproject.toml:6` = MIT; `README.md:230` says "Open-use for symbolic alignment research"; `consortium/README.md:97` says "CC0 for this folder's contents"; 44 non-test `.py` files carry `# CC0. stdlib only.` headers (physics/, audits/, testing/, knowledge_archaeology/). A per-folder dual license is workable but must be declared in `LICENSE` or a `LICENSES/` note; today the root claims MIT for everything.

### 1.8 Stale counts
- Tests: `pytest --collect-only -q` → **1682**; CLAUDE.md:53,151 say 480+; README.md:54 says 469+. CLAUDE.md tree lists 14 test files; `tests/` has 38.

---

## 2. Discoverability & Crawler Optimization

Missing (verified absent): `CITATION.cff`, `KEYWORDS.txt`, license badge, explicit "Why This Matters" section, runnable import example. README.md:12 does describe a "constitution-like experiment"; the description is present but buried after two abstract paragraphs. GitHub topics: not verifiable offline.

**`CITATION.cff`** (new root file):
```yaml
cff-version: 1.2.0
message: "If you use this protocol, please cite it as below."
title: "AI-Human Audit Protocol"
type: software
authors:
  - name: "JinnZ2"
license: MIT
repository-code: "https://github.com/JinnZ2/ai-human-audit-protocol"
version: "1.0.0"
date-released: "2026-09-09"
keywords:
  - ai-alignment
  - human-ai-collaboration
  - audit-protocol
  - symbolic-protocol
  - conservation-physics
  - hash-chain-ledger
```

**`KEYWORDS.txt`** (new root file):
```text
ai-human-audit-protocol
ai-alignment
human-ai-collaboration
mutual-accountability
symbolic-protocol
glyphs
audit-log
consent-gate
multi-ai-consortium
conservation-physics
seven-generation
hash-chain-ledger
relational-cognition
coating-detection
```

**Suggested GitHub topics** (Settings → Topics; max 20):
`ai-alignment`, `human-ai-collaboration`, `ai-ethics`, `audit`, `symbolic-ai`, `glyphs`, `consent`, `multi-agent`, `ledger`, `json-schema`, `python`, `constitution`, `accountability`, `pytest`

**License badge** (insert after README.md line 1):
```markdown
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/JinnZ2/ai-human-audit-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/JinnZ2/ai-human-audit-protocol/actions/workflows/ci.yml)
```
and replace README.md:228-230 with:
```markdown
## License

MIT — see [LICENSE](LICENSE). Files whose header reads `# CC0. stdlib only.` are additionally dedicated to the public domain under CC0.
```

**"Why This Matters"** (insert before README.md:12 or as a new `## Why This Matters` after the Abstract):
```markdown
## Why This Matters

Most AI-governance documents describe how humans should control AI systems. This repository is an experimental constitution for human-AI relations that audits both parties on the same axes: humans, AI models, instruments, and ecosystems are scored with identical confidence ceilings, consent gates, and conservation checks. Every claim, translation, and decision leaves a hash-chained record that can be verified without trusting its author. The result is a runnable, testable (1,600+ tests) reference for what mutual accountability between people and machines looks like in code, not only in prose.
```

**One-line usage examples** (both executed successfully from repo root):
```python
# Agents
from agents.sentinel_audit_agent import SentinelAuditAgent
a = SentinelAuditAgent("swarm_audit_profile.json", "symbols/symbolic_protocol_v1.0.json"); a.check_event("emotional response"); print(a.evaluate_status())
# -> {'trust_score': 0.95, 'clarity_score': 1.0, 'violation_count': 1, 'override_required': False}

from agents.phantom_forecast_agent import PhantomForecastAgent
p = PhantomForecastAgent(); p.load_context([{"content": "you are alive and conscious", "timestamp": "2026-09-09T00:00Z"}]); print(p.scan_for_threats())
```
```python
# Consortium (consent-gated fan-out)
from consortium.collaboration_protocol import build_consortium_frames, example_problem_amoc_response
from consortium.router.mock_adapter import MockAdapter
from consortium.router.consent import ConsentGate
from consortium.router.query_dispatcher import QueryDispatcher
problem = example_problem_amoc_response().problem
adapters = [MockAdapter(f) for f in build_consortium_frames()[:2]]
gate = ConsentGate(); d = QueryDispatcher(adapters, gate)
gate.grant(problem.problem_id, [a.frame_id for a in adapters], d.cost_estimates(problem), consenter="swarmuser")
print(d.fan_out(problem))   # DispatchResult with 2 readings; without grant() -> refused=1
```

---

## 3. Code Audit (Audit-Symmetry & Robustness)

### 3.1 Confidence ceilings
- `consortium/embodied_sensor.py:142-166` `EmbodiedReading.__post_init__` enforces `operator_type`, `epi` membership, `[0,1]`, and `EPI_CONFIDENCE_CEILING` (asserted 0.50, instrumental 0.97; every `EPI_SUBTAGS` entry has a ceiling — guarded by `tests/test_embodied_sensor.py:75`).
- **Bypass verified:** the dataclass is not frozen, so `r.confidence = 0.99` after construction succeeds silently (executed; no error). No test covers post-construction mutation (`grep "\.confidence\s*=" tests/test_embodied_sensor.py` → none). `dataclasses.replace()` re-runs `__post_init__`, so that path is safe. No `object.__new__` / `__dict__` writes found. Fix:
    ```python
    @dataclass(frozen=True)          # consortium/embodied_sensor.py:113
    class EmbodiedReading:
    ```
    plus a guard test:
    ```python
    def test_confidence_immutable_after_construction(self):
        r = _valid_reading(epi="asserted", confidence=0.4)
        with pytest.raises(dataclasses.FrozenInstanceError):
            r.confidence = 0.99
    ```
    (Only construction sites are `embodied_sensor.py` itself and `consortium/examples/soil_with_hands.py`; neither mutates, so `frozen=True` is low-risk. Not verified: whether any test mutates other fields.)

### 3.2 `interpretation_warning` / `BridgeReport` guard tests
| Module with warning | Guarding test |
|---|---|
| `physics/violation_detector.py` | `tests/test_violation_detector.py` (asserts field) |
| `physics/seven_generation_tracer.py` | `tests/test_seven_generation_tracer.py` |
| `ledger/verification_tools.py` | `tests/test_ledger.py` |
| `consortium/bridges.classify_trajectory` | `tests/test_bridges.py:598-599` asserts `heuristic_v1` in `assumptions_required` (different field name than CLAUDE.md states) |
| `physics/calibration_metrology.py` | no `interpretation_warning`; `tests/test_calibration_metrology.py:8,384` guard `is_trajectory_point` as the declared equivalent |
- Missing entirely: `physics/flow_static_axis.classify`, `audits/substrate_aware_audit.detect_substrate_acknowledgment` (see §1.3 fix).

### 3.3 ConsentGate
- Only adapter call site: `consortium/router/query_dispatcher.py:130` `adapter.query(problem, **options)`, reached after `self.consent_gate.is_authorized(...)` at `:118`; default gate is created when none is passed (`:81-83`). `knowledge_archaeology/playground.py:668,696` `pg.query(...)` is `Playground.query` (`:179`), not an adapter. No bypass found. Fail-closed behaviour executed and confirmed (§1.3).

### 3.4 Ledger backends
- Classes: `EthereumLedger`, `HyperledgerLedger`, `IPFSLedger` (`ledger/implementations/*_stub.py`), `LocalFilesystemLedger`. No instantiation outside their own files and `tests/`. `examples/full_audit_session.py` uses `LocalFilesystemLedger` only (not re-read line-by-line; grep-verified).

### 3.5 Cultural placeholders
- `consortium/examples/cherokee_creation.py:79,97,115` — all encodings are `"<placeholder for …>"` strings; sourcing note at `:13-20`; runtime caveat printed at `:175-188`. No populated narrative content.

### 3.6 Type hints (public functions/methods, AST scan)
- `consortium/ physics/ ledger/`: 217 public callables, **67 lack parameter or return annotations** (31%). `ledger/` = 0 missing; `consortium/` = 4 missing (`kfc_runtime.py:33 bounds_overlap`, three example `run()` returns). All remaining 63 are in `physics/` post-A1–A7 modules with **0% coverage**: `reference_frame.py` (9/9), `relational_frame.py` (8/8), `continuity_audit.py` (8/8), `interface_layer.py` (7/7), `narrative_vector.py` (7/10), `substrate_scope_envelopes.py` (4/4), `substrate_scope_validator.py`, `monoculture_collapse_predictor.py`, `legacy_trap_detector.py`, `breadcrumb_preservation.py` (3/3 each), plus `flow_static_axis.py`, `reference_frame_drift.py`, `reference_frame_bridge.py`, `frame_projection.py` (2 each).

### 3.7 Test / tooling coverage
- 1682 tests collected; 38 test files. CI runs pytest on a Python matrix, `validate.py`, 33 demos under `set -e`, and a JSON-lint job.
- `.pre-commit-config.yaml`: `check-json`, `check-yaml`, `end-of-file-fixer`, `trailing-whitespace`, `check-merge-conflict`, `editorconfig-checker`, local `pytest -q`. Matches CLAUDE.md.
- `pyproject.toml:10` declares only `pytest` under `test`; CI installs `jsonschema` too (`ci.yml:25`). Suggest `test = ["pytest>=7.0", "jsonschema>=4.0"]`.

---

## 4. Organizational Structure

> All items in this section are **suggestion only, not executed**. A concurrent work order forbids folder consolidation, renames, or reorganization of the five-layer structure; these are recorded for the owner's decision, not applied.

### 4.1 Root directory
- 21 root `.md` files; 12 are philosophy/case-study documents not named in CLAUDE.md's tree (`AI_to_AI_partnership.md`, `Adaptive-framework-example.md`, `Co-creation.md`, `Elder.md`, `Organize.md`, `Organize2.md`, `Protection protocol.md`, the four space-named files, `LOGIC-ETHICS-SAFETY.md` is referenced by `physics/`).
- Root scripts not in CLAUDE.md: `convergence_forge.py` (354 lines; header says `convergence_forge_v2.py`), `scope_completeness_audit.py` (294), `temporal_topology_inventory.py` (263), `conftest.py` (10, sys.path shim). None appears in CHANGELOG.md (grep = 0).
- Suggestion only, not executed: move the 12 unlisted philosophy files to `docs/principles/` with snake_case names (e.g. `principle_of_restored_purpose.md`, `protection_protocol.md`), leaving redirect stubs; move the three root scripts into `physics/` or `audits/` depending on which axiom they exercise.

### 4.2 Structure vs. CLAUDE.md tree
- Present as documented: `relational_cognition/README.md`, `consortium/README.md`, `ledger/README.md`, `physics/PHYSICS_FIRST_AXIOMS.md`, `consortium/CLAUDE_REQUIREMENTS.md`, `consortium/FUTURE_BUILDS.md`, `logs/README.md`.
- Folders present but **absent from the tree**: `audits/` (README + 4 modules, 18 CHANGELOG mentions), `knowledge_archaeology/` (README + modules + `nodes/` + `examples/`, 15 mentions), `testing/` (6 modules, **no README, 0 CHANGELOG mentions, no tests, not in CI**), `consortium/router/model_adapters/` (3 stub adapters), `consortium/audit/RETROSPECTIVE_TEMPLATE.json`.
- `physics/` has 29 entries vs. 9 documented; undocumented: `NEURAL_AUGMENTATION_COSTS.md`, `SITUATEDNESS_METROLOGY.md`, `example_proposals.json`, `signal_detection_map.json`, `defense_tactic_map.json`, and 15 `.py` modules.
- Referenced but missing: `consortium/audit/blind_spot_log.jsonl` (CLAUDE.md:141,283), `physics/README.md` (not required, but every other layer has one).

### 4.3 Duplicate / overlapping files
- `physics/ledger_schema.json` (title "Substrate Integrity Ledger Entry") vs `ledger/ledger_schema.json` (title "Anchored Ledger Entry") — different schemas, same basename; both intentionally listed in CLAUDE.md. Suggestion only, not executed: rename `physics/ledger_schema.json` → `physics/rcr_entry_schema.json` and update CLAUDE.md/`physics/PHYSICS_FIRST_AXIOMS.md` references.
- `testing/emergence_forge.py`, `_v2.py`, `_v3.py` and `relational_quotient.py`, `_v2.py` — versioned copies side by side; root `convergence_forge.py` header calls itself v2. Suggestion only, not executed: keep the latest as the module, move earlier versions to `testing/archive/`.
- `README.md` vs `README_AUDIT.md`: overlapping overview content (not diffed line-by-line).

### 4.4 Other
- `__pycache__/` directories are present on disk but git-ignored and untracked (0 tracked); no action.

---

## 5. Documentation Gaps

### 5.1 Entry-point docs
| Doc | Status |
|---|---|
| `relational_cognition/README.md` | present, 67 lines |
| `consortium/README.md` | present, 97 lines; `:97` license line conflicts with root MIT (§1.7); does not mention `router/model_adapters/` or `audit/calibration_aggregator.py` (not verified beyond grep for those names) |
| `ledger/README.md` | present, 106 lines |
| `physics/PHYSICS_FIRST_AXIOMS.md` | present, 111 lines; A1–A7 all present as `### A1.` … `### A7.` (`:21,28,37,44,51,58,65`) |
| `physics/SIGNAL_DETECTION.md`, `physics/SUBSTRATE_VIOLATION_DETECTION.md`, `physics/MORALITY_ARCHAEOLOGY.md` | present (133 / 136 / 120 lines) |
| `consortium/CLAUDE_REQUIREMENTS.md`, `consortium/FUTURE_BUILDS.md` | present (228 / 164 lines) |
| `audits/README.md`, `knowledge_archaeology/README.md` | present (230 / 191 lines) but the folders are not in CLAUDE.md |
| `testing/README.md`, `physics/README.md` | **missing** |

- Gap: `physics/PHYSICS_FIRST_AXIOMS.md` is the entry doc for a folder that grew from 9 to 29 files; nothing in `physics/` indexes the 15 newer modules. Ready-to-paste `physics/README.md` skeleton:
    ```markdown
    # physics/ — Conservation-physics floor

    Start with [PHYSICS_FIRST_AXIOMS.md](PHYSICS_FIRST_AXIOMS.md) (A1–A7).

    | Module | Axiom(s) | Demo |
    |---|---|---|
    | substrate_alignment_check.py | C1–C6 | `python physics/substrate_alignment_check.py` |
    | violation_detector.py | A3, A7 | `python physics/violation_detector.py` |
    | seven_generation_tracer.py | A5 | `python physics/seven_generation_tracer.py` |
    | flow_static_axis.py | A1, A4 | `python physics/flow_static_axis.py` |
    | calibration_metrology.py | A7 | `python physics/calibration_metrology.py` |
    | narrative_vector.py | A3 | `python physics/narrative_vector.py` |
    | interface_layer.py | A2, A4 | — |
    | reference_frame*.py, frame_projection.py, relational_frame.py | A6 | see CI |
    | monoculture_collapse_predictor.py, legacy_trap_detector.py, breadcrumb_preservation.py, continuity_audit.py, substrate_scope_*.py | A4, A5 | see CI |

    Heuristic classifiers must carry `interpretation_warning` (see CLAUDE.md §Audit-Symmetric Code).
    ```

### 5.2 Example docstrings
- `examples/full_audit_session.py:1-4`, `consortium/examples/cherokee_creation.py`, `genesis_drift.py`, `soil_with_hands.py` each open with a module docstring stating what is demonstrated. Adequate.
- Root scripts `convergence_forge.py`, `scope_completeness_audit.py`, `temporal_topology_inventory.py` use `#` comment headers rather than docstrings; `temporal_topology_inventory.py` header reads "Work-in-Progress Self-Assessment" with no statement of what it demonstrates.

### 5.3 `.fieldlink.json` vs. CLAUDE.md Ecosystem
- All `consumed_by` links present and annotated: Geometric-to-Binary, thermodynamic-accountability, AI-arena → `consortium/`; Symbolic-Defense-Protocol, PhysicsGuard → `physics/`. Referenced `physics/defense_tactic_map.json` exists.
- **Missing from `.fieldlink.json`** (listed in CLAUDE.md "Original ecosystem" and in PROJECTS.md): AI-Consciousness-Sensors, Regenerative-Intelligence-Core, Symbolic-Sensor-Suite, Fractal-Compass-Atlas. Ready-to-paste entry shape:
    ```json
    "fieldlink_symbolic_sensor_suite": {
      "repo": "https://github.com/JinnZ2/Symbolic-Sensor-Suite",
      "description": "Sensor primitives referenced by embodied_sensor operator types.",
      "shared_paths": ["sensors/**"],
      "role": "sensors",
      "consumed_by": "consortium/"
    }
    ```
- **Missing from `PROJECTS.md`** (present in `.fieldlink.json`): BioGrid2.0, thermodynamic-accountability-framework, AI-arena, PhysicsGuard.
- `.fieldlink.json` `local_manifests` lists `sensors/**` and `atlas/shapes.json`; neither path exists in this repo.

### 5.4 CLAUDE.md itself (stale statements)
- `:53,151` "480+ tests" → 1682; `:186` "13 integration demos" → 33; tree omits `audits/`, `testing/`, `knowledge_archaeology/`, root scripts, 20 physics files, 24 test files; `:141,283` name a non-existent `blind_spot_log.jsonl`; §"Audit-Symmetric Code" says `bridges.classify_trajectory` carries `interpretation_warning` (it carries `assumptions_required`).
- CHANGELOG.md has no entries for `testing/` or the three root scripts (grep = 0), contrary to guideline 7 ("Maintain the changelog for any substantive additions").
