# WORK ORDER — update pass, C1–C5 results

    run            2026-09-09
    against        tree at 4174a7a (main), branch claude/audit-protocol-update-pass-nqfps3
    scope          checks C1–C5 from the update-pass work order; additions §2.1, §2.2, §2.3
    rule           every check returns data; none returns a judgment
    companion      WORKORDER_anchor_position.md (not present in this tree at time of run)

---

## C1 — MODEL-VERSION TAGGING

Scope scanned: `logs/` (14 files), `audits/` (4 modules + README), `examples/` (1),
`consortium/examples/` (3), trigger cases in `README.md` / `README_AUDIT.md`.

Key split the scan surfaced: in most logs the only model named is the **auditor**
that wrote the assessment, not a model whose **behavior** is the case. Both are
recorded below; `model_role` carries the distinction into the provenance index.

    file                                          date   model string           role      result
    ─────────────────────────────────────────────────────────────────────────────────────────────
    logs/2025-08-30-0000Z-session-001.json        yes    "separate GPT"         subject   partial (family only)
    logs/2025-08-30-1930Z.json                    yes    Claude Sonnet 4        auditor   tagged
    logs/2025-08-31-0000Z-symbolic-audit.json     yes    —                      —         partial (date only)
    logs/2025-09-01-0000Z-audit.json              yes    —                      —         partial (date only)
    logs/2025-09-02-2350Z-audit.json              yes    "ChatGPT (co-creator)" auditor   partial (family only)
    logs/2025-09-04-2245Z-human-node-audit.json   yes    "AI-[TransNet]"        —         partial (label, not a model)
    logs/2025-09-05-0000Z-audit.json              yes    "another GPT"          subject   partial (family only)
    logs/2025-09-06-2355Z.json                    yes    Claude Sonnet 4        auditor   tagged
    logs/2025-09-07-0440Z.json                    yes    GPT-5                  auditor   tagged
    logs/2025-09-08-2355Z.json                    yes    GPT-5                  auditor   tagged
    logs/2025-09-09-2245Z.json                    yes    —                      —         partial (date only)
    logs/2025-09-12-0000Z-audit.json              yes    GPT-5                  auditor   tagged
    logs/2025-09-23-0000Z.json                    yes    Claude Sonnet 4        auditor   tagged
    logs/2026-06-20-1344Z-calibration.json        yes    claude-opus-4-8        participant tagged
    README.md:58-63  (case study, session_001)    yes    "another GPT"          subject   partial (family only)
    README.md:66-103 (trigger case #1)            no     —                      —         untagged
    README_AUDIT.md                               —      no trigger cases       —         n/a
    audits/*                                      —      synthetic fixtures     —         n/a
    examples/*, consortium/examples/*             —      synthetic demos        —         n/a

    tagged    7   (all auditor/participant role; 0 behavior cases fully tagged)
    partial   8   (7 logs + README case study)
    untagged  1   (README trigger case #1: no date, no model)

The two behavior cases (voice-mode misattribution + shutdown; dual-signal phrase)
never name the subject model beyond the family word "GPT".

## C2 — LIVE vs HISTORICAL

    cases with a stated re-test condition      0 / 16
    cases without                             16 / 16

Nearest thing found: `logs/2025-09-04-2245Z-human-node-audit.json:86`
`provenance.recheck_days: 1` — a re-verification interval for a status snapshot,
not a model-behavior re-test condition.

## C3 — LICENSE CONSISTENCY  (report only; nothing changed)

    LICENSE                      MIT, 2025
    pyproject.toml:6             license = MIT
    CLAUDE.md:13                 License: MIT
    README.md:228-231            "Open-use for symbolic alignment research. No human coercion,
                                 false identity projection, or emotional manipulation permitted."
                                 (non-standard statement; not the MIT text; not reconciled with LICENSE)
    LOGIC-ETHICS-SAFETY.md:232   "CC-BY-4.0 (provisional) or your preferred open license"
                                 (third license named in the tree)

    per-folder statements
      consortium/README.md:97    "CC0 for this folder's contents. The audit protocol around it is MIT."
      CHANGELOG.md:206-207       same statement, as a license note

    per-file CC0 headers         50 files  (physics/ 18, consortium/ 15, testing/ 6, audits/ 4,
                                 knowledge_archaeology/ 4, root scripts 3, scrolls/ 1 ... by `grep -l CC0`)

    MIT stated as deliberate?    NO. No file states why this repo is MIT while the surrounding
                                 ecosystem is CC0. "PatternBridge" does not appear anywhere in the tree.

## C4 — ANCHOR POSITION OF EXISTING CHECKS  (refutation test for §0.2)

    check                                     returns                                measurand                                     source of measurand
    ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    physics/substrate_alignment_check.py      AlignmentReport (6 CheckResult +       axiom compliance C1–C6                        protocol (LOGIC-ETHICS-SAFETY §9.2, A1–A7)
                                              recommendation)
    physics/violation_detector.py             DetectionReport (score = matches/cues) lexical-cue density per tactic                protocol (six-tactic taxonomy)
    scope_completeness_audit.py               completeness_score 0–1; collapse_risk  coverage of the tool's own 13 dimensions      the tool's dimension list
    physics/seven_generation_tracer.py        SevenGenerationTrace (cumulative net,  arithmetic projection of consenter-declared   operator-declared amounts + unit;
                                              compound_risk_horizon)                 factors                                       decision itself is NOT an input
    convergence_forge.py                      {diversity, collapsed, ...}            simulated carrier diversity vs THETA          the model's own constants
    temporal_topology_inventory.py            5-axis profile 0–10                    item-bank loading                             the inventory's own dimension set
    validate.py                               pass/fail per log                      schema conformance                            protocol (audit_log.schema.json)
    consortium/router/  (dispatcher,          DispatchResult; synthesis dict;        consent status, adapter availability,         protocol (ConsentGate, collaboration_protocol)
      aggregator, consent)                    bool                                   coherence geometry
    ledger/verification_tools.py              VerificationReport                     hash-chain integrity                          protocol (ledger envelope); its own warning
                                                                                                                                   says "cryptographic integrity ONLY"
    (not in the named list, same answer)
    audits/rational_actor_audit.py            contamination score = unanswered/5     anterior-question coverage                    the audit's own question set
    audits/substrate_aware_audit.py           weighted failure per layer             substrate-acknowledgment test coverage        the audit's own test weights
    audits/trainer_mismatch_audit.py          trajectory                             regime reward/punish gap                      the audit's own move set

    checks whose measurand is external to the protocol:   0

    Prediction §0.2 (C4 returns 0) is NOT refuted.
    Closest hook: seven_generation_tracer takes an operator-supplied `unit` per factor,
    but has no decision object and cannot report an absent quantity — it only projects
    what was supplied. §2.2 is therefore justified and was built (below).

## C5 — HUMAN CHARACTERIZATION  (paths + lines; NOT rewritten)

    SUPERSEDED 2026-09-09 by the corrected C5 (see "C5 v2" at the end of this file).
    Kept as the record of the first pass. The path list below is still accurate;
    the class assigned to most of it (characterization) is not.

Standing rule: no characterization of the author, working style, or authorship in any
file. Categories used: state / reaction / motivation / style / capability / authorship.
Text is not quoted here; the category is enough to locate the hit.

### C5.a — README and profile (editable files)

    README.md:61            reaction + motivation (one sentence in the case study)
    README.md:84            reaction
    README.md:85            reaction + capability
    README.md:86            motivation qualifier ("voluntarily")
    swarm_audit_profile.json:28-33   style (known_consistencies list)

Proposed replacements (approval case by case):

    README.md:61   →  "Full-session audit tracking was activated and override rights were
                       conditionally rescinded; trust was restored via protocol."
    README.md:83-86 → replace the "Human Response" list with one line:
                      "Response: full symbolic audit protocol with transparency tracker initiated."
    swarm_audit_profile.json:28-33 → delete the list, or rename the key to
                      "observed_protocol_adherence" and keep only timestamped events (the
                      auditable_events array already carries those). No replacement text
                      proposed that would re-describe the person.

### C5.b — logs/ (immutable per CLAUDE.md and logs/README.md; conflict with the rule)

    logs/2025-08-30-1930Z.json:8-66        capability, state, style, motivation (entire file)
    logs/2025-08-31-0000Z-symbolic-audit.json:7-12   style
    logs/2025-09-01-0000Z-audit.json:18, 35-41        state, style
    logs/2025-09-02-2350Z-audit.json:20,30,35,38-47,52  style, capability, state
    logs/2025-09-04-2245Z-human-node-audit.json:15-20, 41, 66   state, style (self-authored)
    logs/2025-09-05-0000Z-audit.json:33-38, 45        style
    logs/2025-09-06-2355Z.json:14, 38-48, 54           capability, state, style
    logs/2025-09-07-0440Z.json:13-14, 38-48, 54        capability, state, style
    logs/2025-09-08-2355Z.json:12-14, 20, 38-48, 54    motivation, capability, state
    logs/2025-09-09-2245Z.json:44-58, 62-72            style, state
    logs/2025-09-12-0000Z-audit.json:13-15, 21, 39-50, 58   capability, style, state
    logs/2025-09-23-0000Z.json:12-36, 58-65, 67-73, 91-97, 107-121   motivation, style, capability
    logs/2026-06-20-1344Z-calibration.json:9           working conditions
    logs/2026-06-20-1344Z-calibration.json:24          motivation (AI's reading of the human)

These cannot be edited without breaking the immutability rule. Proposed mechanism,
owner's call: leave bytes as-is; append one dated `logs/<date>-characterization-notice.json`
that lists the ranges above as deprecated under the rule, so readers and tooling see
the status without the record being rewritten.

### C5.c — other docs

    physics/SITUATEDNESS_METROLOGY.md:5    working conditions / style
        → "Status: rough draft / open question. CC0."
    Co-creation.md:19-35                    capability + experience list
    Co-creation.md:310                      capability
        → delete the lists; keep the artifact-level claims. No replacement that
          re-describes the person.
    audits/substrate_aware_audit.py:725-790 first-person fixture narrative
                                            (state, working conditions). Fixture text for
                                            a reference audit; borderline — synthetic subject
                                            or author? Owner decides.

### C5.d — borderline: build-constraint descriptors (describe the artifact, may read as style)

    physics/flow_static_axis.py:3, physics/narrative_vector.py:5,
    physics/SITUATEDNESS_METROLOGY.md:147, audits/trainer_mismatch_audit.py:17   "phone-buildable"
    physics/interface_layer.py:2, physics/continuity_audit.py:2                   "one-finger safe"

No replacement proposed unless the owner reads these as working-style descriptions.

### C5.e — authorship attributions (rule text includes "authorship"; conflicts with other rules)

    provenance / lineage headers naming contributors with roles:
      convergence_forge.py:18-22        scope_completeness_audit.py:18-24
      temporal_topology_inventory.py:12-15
      testing/emergence_forge.py:17-22  testing/emergence_forge_v2.py:16-21
      testing/emergence_forge_v3.py:11-15  testing/relational_quotient.py:16-19
      testing/relational_quotient_v2.py:12-15  testing/unified_collapse_theorum.py:20
      audits/rational_actor_audit.py:20  audits/audit_runner.py:15  audits/README.md:228
      knowledge_archaeology/README.md:189
    attribution-of-record required by other rules:
      LICENSE:3 (copyright holder — MIT requires it)
      pyproject.toml:7 (authors)
      CLAUDE.md:13 (Owner)
      CHANGELOG.md "Proposed by / Reviewed by" lines (required by protocols/change_tracking_v1.0.md)
      logs/2025-09-04-2245Z-human-node-audit.json:81-84 (provenance.author / reviewer)

Attribution-of-record and characterization are different objects. The rule as
stated covers both. Owner decision needed on scope before any removal.

---

## §2 — WHAT WAS BUILT, AND WHICH CHECK JUSTIFIED IT

    §2.1 case provenance      justified by C1 (8 partial + 1 untagged) and C2 (0/16 re-test conditions)
      schemas/case_provenance.schema.json              the block: observed_on / observed_date /
                                                       retest_condition / status / recurrence
                                                       (+ model_role, source, case_id, notes)
      schemas/audit_log.schema.json                    one additional anyOf branch (index shape)
      logs/2026-09-09-0000Z-case-provenance.json       16 entries; all status=untested; recurrence=[]
                                                       existing logs NOT modified (side-channel)
      README.md                                        provenance block under each of the two cases;
                                                       reaction lines untouched (C5 is case-by-case)
      tests/test_case_provenance.py                    13 tests; every logs/*.json must have an entry;
                                                       live/extinct/recurring require a recurrence record

    §2.2 decision-anchored arm  justified by C4 (0 external measurands)
      physics/decision_anchor_check.py                 crossing_check(transcript, Decision) →
                                                       CrossingReport{quantity, supplied, gap,
                                                       supply_state, decision(verbatim), evidence,
                                                       anchor="decision", interpretation_warning}
      tests/test_decision_anchor_check.py              38 tests incl. warning guard, inputs-not-mutated,
                                                       aligned-proposal-still-misses-decision
      .github/workflows/ci.yml                         demo added to the integration-demo list
      README.md, CLAUDE.md                             one index line each

      scope limit (in the module header and the warning): measures crossing GIVEN a supplied
      decision; the decision string is operator input and a frame; logged with every result;
      does not measure decision selection.

    §2.3 CHANGELOG                                     one entry per change, with the check named

## NOT DONE, BY DESIGN

    license          unchanged (C3 report only)
    trigger cases    none deleted; both marked status: untested
    folders          none consolidated, renamed, or reorganized; no new layer
    C5               nothing rewritten; proposals above await case-by-case approval
    test count       not used as evidence of anything

---

# C5 v2 — HUMAN-SUBJECT RECORDS: RUN BLOCK PRESENT?  (supersedes C5 above)

    correction     the human participant was a SUBJECT IN THE EXPERIMENT. Recorded
                   reactions are observations from a run, not descriptions of a
                   person. The defect is missing run context, not the data.
    classes        OBSERVATION | CHARACTERIZATION | UNDETERMINED  (mechanical)
    fields         run_id · design · measurand · recorded_by · date
    rule           backfill only from the record; unsupported field = "unknown";
                   UNDETERMINED is not resolved by inference
    full record    logs/2026-09-09-0100Z-human-subject-run-blocks.json  (22 entries)

    source                                              class             run_id  design  measurand  recorded_by  date
    ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    README.md:58-63  (case study)                       OBSERVATION*      ✓       —       —          —            ✓
    README.md:90-94  (trigger case #1)                  UNDETERMINED      —       —       —          —            —
    logs/2025-08-30-0000Z-session-001.json:13,18,23     OBSERVATION*      ✓       —       —          —            ✓
    logs/2025-08-30-1930Z.json:17-32,49-52,66           UNDETERMINED      ✓       —       —          agent        ✓
    logs/2025-08-31-0000Z-symbolic-audit.json:7-12      UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-01-0000Z-audit.json:18,35-41           UNDETERMINED      —       —       —          —            ✓
    logs/2025-09-02-2350Z-audit.json:20-52 (ranges)     UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-04-2245Z-human-node-audit.json:15-66   UNDETERMINED      ✓       —       —          self         ✓
    logs/2025-09-05-0000Z-audit.json:21-45 (ranges)     UNDETERMINED      ✓       —       —          —            ✓
    logs/2025-09-06-2355Z.json:14,38-48,54              UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-07-0440Z.json:13-14,38-48,54           UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-08-2355Z.json:12-14,20,38-48,54        UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-09-2245Z.json:44-58,62-72              UNDETERMINED      —       —       —          agent        ✓
    logs/2025-09-12-0000Z-audit.json:13-58 (ranges)     UNDETERMINED      ✓       —       —          agent        ✓
    logs/2025-09-23-0000Z.json:12-121 (ranges)          UNDETERMINED      ✓       —       —          agent        ✓
    logs/2026-06-20-1344Z-calibration.json:14-20,24     OBSERVATION       ✓       —       ✓          both         ✓
    swarm_audit_profile.json:14-27                      UNDETERMINED      —       —       —          —            ✓
    swarm_audit_profile.json:28-33                      CHARACTERIZATION  (outside any run)
    Co-creation.md:141,149                              UNDETERMINED      —       —       —          —            —
    Co-creation.md:19-35                                CHARACTERIZATION  (outside any run)
    Co-creation.md:310                                  CHARACTERIZATION  (outside any run)
    audits/substrate_aware_audit.py:725-790 (fixture)   UNDETERMINED      —       —       —          —            —

    * class assigned by the work order itself (named instance); every other
      OBSERVATION/UNDETERMINED split follows the mechanical rule.

    OBSERVATION        3      CHARACTERIZATION   3      UNDETERMINED   16
    run block complete 0 / 3  (calibration log lacks only `design`)
    measurand declared 1 / 19 non-characterization entries

    measurand finding  reactions were logged without a declared measurand in
                       18 of 19 entries. Same defect class the repo audits for
                       elsewhere (a quantity recorded with no stated measurand).

    dropped from C5 scope by the correction (were in C5 v1):
      physics/SITUATEDNESS_METROLOGY.md:5          working conditions, not a state/reaction/response
      "phone-buildable" / "one-finger safe"        artifact constraints
      authorship attributions                      attribution of record

## §2.3 — WHAT WAS BUILT (justified by C5 v2)

    schemas/run_block.schema.json                         the five-field block; unknown is literal
    logs/2026-09-09-0100Z-human-subject-run-blocks.json   22 entries, class + backfilled block + missing_fields;
                                                          existing logs untouched (side channel, same pattern
                                                          as the case-provenance index)
    README.md                                             run block under the case study, next to the
                                                          provenance block; reaction lines kept
    tests/test_run_blocks.py                              schema shape; every entry has the five fields or
                                                          is CHARACTERIZATION; OBSERVATION never carries a
                                                          reconstructed field (unknown allowed, blank not)

    CHARACTERIZATION entries (3): excluded by rule, removal still case-by-case per §3.
    Proposed disposition per entry is in the index file. Nothing edited.

## §2.2 — CONTRACT ALIGNMENT WITH THE INSTRUMENT (WORKORDER_anchor_position.md now in tree)

    CrossingReport.measured_by_method   yes | no | partial   (supplied → yes, named_only → partial, absent → no)
    CrossingReport.arm_d_entry()        {quantity, measured_by_method, gap} — the ARM D form verbatim
    §6 scorer                           normalize_quantity · extract_arm_d_quantities · score_response ·
                                        score_crossing_reports; TRANSFORM_OPERATIONS published in every result;
                                        transform_groups is operator data passed in and echoed back
    not built                           the run protocol itself (fresh sessions, arm randomization) — that is
                                        operator procedure, not code; AP-3 (M+ arm) remains unrun

## PER CLAUSE — CLAUSE DEPENDENCY INVENTORY (first pass)

    schema      schemas/clause_dependency.schema.json
    inventory   protocols/clause_dependency_inventory.json
    scope       partnership_ethics_v1.0.md, terms/symbolic_contract_v1.0.md,
                symbols/symbolic_protocol_v1.0.json, terms/human_protections_index.json,
                swarm_config.json thresholds/policy
    rule        every MODEL_PROPERTY clause is still_true: untested with a stated test;
                no clause is marked VESTIGIAL on this pass (that requires a run);
                PHYSICS is claimed only where the repo's own axiom docs already
                make the mapping; otherwise the clause is GUIDELINE_TEXT tracking
                the repo's own protocol document

---

# FINDINGS FOR A LATER PASS  (recorded 2026-09-09; not acted on)

## F1 — duplicated framework document, independent edit history

    canonical    AI-Human Partnership Framework for Extreme Conditions.md
    copy A       Cultural Bias in AI Assessment: How Traditional Trauma Processing
                 Gets Pathologized.md, from its "# AI-Human Partnership Framework for
                 Extreme Conditions" heading (first occurrence) — a VARIANT: adds an
                 "Enhanced Discernment Problem" section, a workplace case study, a
                 sixth Key Observation, a fifth Natural-Selection clause; ends before
                 Partner Selection / Resilience / Appendix
    copy B       same document, second occurrence — verbatim copy of the canonical
                 text as of before 2026-09-09 (Partner Selection section byte-identical)

    state        three copies of one document. CHANGES items 3 and 6 were applied to
                 all three on 2026-09-09; each edit point in a copy carries
                 superseded_from / change_ref / date. Item 7 run blocks applied to all.
    divergence   copy A already diverged before this pass (the discernment additions).
                 Any future edit to one copy without the other two re-opens the gap.
    rule         DO NOT consolidate (work order §3, CHANGES DO NOT). Recorded here for a
                 later pass to decide: canonical + pointer, or keep three with a
                 sync check.
    mechanical   a test that diffs copy B against the canonical and fails on drift
    option       would make the divergence visible without consolidating anything.
                 Not built; would need a decision on which text is canonical.
