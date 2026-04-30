# 🔎 Audits

*Schema-driven contamination detectors for foundational assumptions in academic literature.*

This folder is the home for an **audit family** — a small set of modules that scan academic papers for foundational-assumption contamination. Each module asks: *does this paper specify the constraint layer its core concept depends on, or does the concept float in unbounded abstraction?*

The audits return **data, not judgment**. Each module produces a structured `PaperAudit`-style report with surface markers found, anterior questions answered or not, a contamination score, and a verdict (PASS / PARTIAL / FAIL). The reader — author, reviewer, editor, downstream model — decides what to do with the report.

---

## What lives here

```
audits/
├── README.md                           (this file)
├── rational_actor_audit.py             (rational-actor / utility / efficiency claims)
└── audit_runner.py                     (batch runner: walks papers/, calls extractor,
                                         validates, writes per-paper JSON + report;
                                         model-agnostic; resumable; manual-queue mode)
```

### Planned siblings (per upstream module docstrings)

`rational_actor_audit.py` declares itself *"Compatible with `first_principles_audit.py` and `study_extractor.py`"*. Those siblings are not yet written and will ship in their own change events:

- **`first_principles_audit.py`** — generic version of the same pattern: any claim of physical / mathematical / computational principle is checked for whether it specifies system, timescale, substrate, boundary, and feedback.
- **`study_extractor.py`** — pre-processor that pulls the relevant paper section (abstract / methods / model section) into a structured form the audit modules can consume.

When those land, the import surface here becomes:

```python
from audits.rational_actor_audit import audit  # noqa
from audits.first_principles_audit import audit  # noqa
from audits.study_extractor import extract     # noqa
```

---

## `rational_actor_audit.py`

**Premise being tested.** A claim about "rational behavior" or "utility maximization" is only physically meaningful if it specifies:

1. **`system_specified`** — whose utility is being maximized? (individual organism, tribe, ecosystem, firm, abstraction)
2. **`timescale_specified`** — over what timescale is utility measured? (seconds, generations, geological)
3. **`substrate_specified`** — what thermodynamic / biological / ecological constraints bound the optimization?
4. **`boundary_specified`** — where is the boundary between agent and environment drawn, and is it stable under the proposed action?
5. **`feedback_specified`** — what feedback couples agent action to substrate state, and how does it modify the utility function over time?

Papers that omit (1)–(5) are not making physically testable claims. They are making semantic assertions dressed in mathematical formalism.

### What the module ships

| Surface | What it does |
|---|---|
| `SURFACE_MARKERS` | List of 14 contamination-pattern markers (`rational actor`, `utility maximization`, `efficient market`, `homo economicus`, ...). Presence is *not* failure; failure is unanswered anterior questions. |
| `ESCAPE_PATTERNS` | List of 8 regex patterns naming the *evasions* (`without loss of generality`, `for simplicity`, `abstracting away`, `in equilibrium`, ...). Presence is the smell test. |
| `ANTERIOR_QUESTIONS` | Dict of 5 keys → human-readable question text. The audit returns one `AnteriorAnswer` per key. |
| `prescan_text(text)` | First-pass local scan: returns `{surface_markers_found, escape_patterns_found, warrants_full_audit}`. No LLM call. |
| `EXTRACTION_PROMPT` | The instruction passed to a model that will read the paper text and emit a JSON `PaperAudit`. |
| `validate_audit_json(payload)` | Validates an LLM-emitted audit JSON against the schema. Returns `(is_valid, list_of_errors)`. |
| `compute_contamination_score(answers)` | Score = fraction of anterior questions left unanswered. |
| `compute_verdict(score)` | `PASS` if ≤ 0.2, `PARTIAL` if ≤ 0.6, `FAIL` otherwise. |
| `build_audit_from_extraction(paper_id, title, extraction)` | Assembles a validated `PaperAudit` object from raw extraction JSON. |
| `_self_test()` | Smoke test: runs prescan + audit assembly against a fabricated contaminated abstract and a clean one. |

### Strict-by-default

Per the extraction prompt:

> *Be strict. "We assume agents are rational" is NOT an answer to system_specified. "In equilibrium" is NOT an answer to timescale_specified. "Standard utility function" is NOT an answer to substrate_specified. The paper must concretely name the system, the timescale, the substrate constraints, the agent/environment boundary, and the feedback coupling.*

The module returns the verdict; the consenter (you, your reviewer, your editor) decides whether to publish, revise, or reject. The audit does not write a `decision` field into the input. This is the same audit-symmetry stance the rest of the protocol enforces: data, not judgment.

### Run the self-test

```bash
python -m audits.rational_actor_audit
```

Output: a contaminated abstract scores 1.0 / FAIL across all five anterior questions; a clean abstract that names the system (foragers in a 5-hectare temperate forest), timescale (30-year window), substrate (seasonal yield variance + predator risk), boundary (2 km foraging radius), and feedback (soil depletion reducing future yield) scores 0.0 / PASS.

---

## `audit_runner.py`

Batch runner for the audit modules. Walks a directory of plain-text papers (`papers_dir/*.txt`), runs the prescan, calls a pluggable extractor, validates the returned audit, recomputes score + verdict server-side, and writes per-paper JSON to an output directory. Resumable by default (skips papers that already have an audit on disk). Stdlib only.

### CLI

```bash
# Run an audit pass (default: stub extractor — for pipeline smoke tests only)
python -m audits.audit_runner run    <papers_dir> <out_dir>

# Run an audit pass with the manual-queue extractor (no model in the loop)
python -m audits.audit_runner run    <papers_dir> <out_dir> --manual <queue_dir>

# Build a markdown report from an existing out_dir
python -m audits.audit_runner report <out_dir>

# End-to-end smoke test (used by CI)
python -m audits.audit_runner --selftest
```

### Pluggable extractor

An "extractor" is any callable `(prompt: str, text: str) -> dict`. The runner ships three:

| Extractor | When to use |
|---|---|
| `stub_extractor` | Offline pipeline smoke tests. Marks every paper FAIL. |
| `manual_queue_extractor(queue_dir)` | Human-in-the-loop with **no model**. First call writes the prompt + paper text to `<digest>.request.txt` and raises `FileNotFoundError`. The human reads the request, supplies `<digest>.audit.json`, re-runs the runner — the second call reads the answer back. |
| Your LLM client | Plug in any callable matching the signature. The module makes no API calls itself; the consenter wires the call. |

The runner does **not** trust the extractor's claimed `paper_id`, `title`, `contamination_score`, or `verdict`:
- `paper_id` is overridden from the filename stem
- `title` defaults to `paper_id` if absent
- `contamination_score` and `verdict` are recomputed from `anterior_answers` server-side

This preserves audit symmetry: even a co-operating extractor cannot lie its way to a `PASS`.

### Resumability

`run_audit(..., skip_existing=True)` (default) skips papers whose `paper_id.json` already exists in `out_dir`. This lets a long audit pass be interrupted and resumed without re-querying the model for already-audited papers. `_run_summary.json` is overwritten on each run; per-paper audits are not.

### Marker gate

`run_audit(..., require_markers=True)` (default) skips papers with no surface markers from `prescan_text` — papers that don't even mention rationality / utility / efficiency don't warrant a full audit. Set to `False` to audit every paper regardless.

### Outputs

```
out_dir/
├── _run_summary.json          (counts, verdict tallies, per-paper failures)
├── p001.json                  (one PaperAudit per paper)
├── p002.json
└── ...
```

`build_report(out_dir)` aggregates the per-paper JSON into a markdown report grouped by verdict (FAIL / PARTIAL / PASS), with unanswered-question lists per paper. The report is intentionally plain-text, copy-pasteable, and listable on a phone screen — no tables, just sections.

---

## How this connects to the rest of the protocol

| Layer | Connection |
|---|---|
| `physics/violation_detector.py` | Same shape: keyword / regex prescan + structured report + `interpretation_warning`. The rational-actor audit is the same idea narrowed to economic / decision-theoretic claims. |
| `physics/SUBSTRATE_VIOLATION_DETECTION.md` | The "abstraction without substrate" pattern is a sixth-tactic-adjacent move. This audit gives it a runnable form. |
| `knowledge_archaeology/biological_mismatch.py` | Same insight: name the constraint layer or be invisible to misframe. The biological-mismatch module asks "what regime is this organism adapted to?"; the rational-actor audit asks "what regime is this utility function bounded by?" Both are regime-archaeology questions. |
| `knowledge_archaeology/knowledge_archaeology.py` | A paper auditable here can also be encoded as a `KnowledgeNode`: failed audit → `fails_under` strings; the missing anterior questions → `assumptions`; the surface markers → `extraction_risks`. |

---

## Audit-symmetric guarantees

- **Returns data, not judgment.** The contaminated and clean fixtures in the self-test produce structured reports, not "this paper is bad" / "this paper is good". The reader interprets.
- **Strict-by-default.** Default thresholds are tight (`PASS` requires ≤ 1 of 5 anterior questions unanswered). The module documents the strictness explicitly so it cannot be silently relaxed.
- **Schema-validated.** `validate_audit_json` is exported. Any downstream tool consuming audit output can validate it before trusting it.
- **No model calls in the module itself.** The module ships a prompt (`EXTRACTION_PROMPT`) and a validator. The actual paper-reading model invocation is the consumer's responsibility — and is the consenter's choice of provider, with full disclosure of what is being read and what is being returned. This matches the `consortium/router/` pattern: the module declares the contract; the consenter wires the call.

---

## Lineage

`rational_actor_audit.py` is forwarded from JinnZ2 lineage with CC0. Smart-quote characters in the upstream paste were normalized to ASCII on port; semantics unchanged. The `_self_test()` block ships verbatim.

Stdlib only. No external dependencies.
