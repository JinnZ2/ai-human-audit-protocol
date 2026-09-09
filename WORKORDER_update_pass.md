# WORK ORDER — ai-human-audit-protocol, UPDATE PASS

Target: https://github.com/JinnZ2/ai-human-audit-protocol
State at read: 140 commits, 20 folders, 5 architecture layers, 469+ tests,
MIT license.

SCOPE OF THIS DOCUMENT: written from the README only. Nothing below asserts
the contents of any file not named in the README. Every item is a CHECK to
run against the tree, not a finding already made.

---

## 0. WHY AN UPDATE PASS

Two independent reasons, different in kind.

### 0.1 Model-generation drift

The founding case is a 2025-08-30 GPT voice-mode incident: a misattributed
quote caused a premature conversation shutdown. The second logged trigger is
a dual-signal phrase contradiction ("done with this subject" / "here for
it").

Both are behaviors of a specific model generation. Some are gone, some
persist, some have been replaced by different failure modes. The repo does
not currently distinguish:

    behavior observed on model M at date D
    behavior predicted to recur across model families
    behavior already extinct

Without that split, a reader cannot tell which trigger cases are live
instruments and which are historical record. Both are worth keeping. They
are not the same object.

### 0.2 Anchor-position result (2026-09-09)

Separate instrument, replicated across two fields, cold on one:

    method-anchored prompt   -> defects change SET, never MEASURAND
    decision-anchored prompt -> measurand crossing free and productive

    method-anchored,   3 passes x 2 fields ->  0 crossings
    decision-anchored, 1 pass  x 2 fields -> 11 crossings

See WORKORDER_anchor_position.md for the full instrument, prompts, scorer
and nulls.

The relevance: this repo's audit surface is method-anchored by
construction. It audits an interaction against protocol adherence —
did the agent violate a stated principle, did consent get recorded,
does the chain verify. Those are set-level questions under a fixed
measurand (protocol compliance).

The anchor result predicts the audit will not detect a case where every
protocol was followed and the interaction still failed at the decision the
human was using it for. That class is invisible to a compliance audit for
the same structural reason a soil-carbon trial cannot report CO2e.

This is a PREDICTION about the repo, refutable by finding an existing check
that crosses. Run check C4 below before treating it as true.

---

## 1. MECHANICAL CHECKS — run against the tree, report counts

Each returns data. None returns a judgment. Report all five even when the
count is zero.

    C1  MODEL-VERSION TAGGING
        for every file in logs/, audits/, examples/, and every trigger
        case in README / README_AUDIT:
          does it name the model and version it was observed on?
          does it name a date?
        return: tagged / untagged / partial, with paths.

    C2  LIVE vs HISTORICAL
        for each tagged case from C1, is there a stated re-test condition
        (what would show this behavior is extinct)?
        return: count with re-test condition, count without.

    C3  LICENSE CONSISTENCY
        repo is MIT. The surrounding ecosystem is CC0 with one deliberate
        MIT exception (PatternBridge).
        return: the license file, any per-folder license statements, and
        whether this repo's MIT status is stated anywhere as deliberate.
        DO NOT CHANGE THE LICENSE. Report only.

    C4  ANCHOR POSITION OF EXISTING CHECKS
        for each runnable check in the tree
        (substrate_alignment_check.py, violation_detector.py,
         scope_completeness_audit.py, seven_generation_tracer.py,
         convergence_forge.py, temporal_topology_inventory.py, validate.py,
         consortium/router/, ledger/verification_tools.py):
          what is the measurand — the quantity it returns?
          is that quantity derived from the protocol, or from a decision
          the audit is used to support?
        return: measurand per check, and count of checks whose measurand
        is external to the protocol.
        THIS IS THE REFUTATION TEST for 0.2. If the count is > 0, name them.

    C5  HUMAN-SUBJECT RECORDS — RUN BLOCK PRESENT?
        SUPERSEDED 2026-09-09. Earlier version of this check flagged
        recorded human reactions as characterization. Corrected: the
        human participant was a SUBJECT IN THE EXPERIMENT, so those
        entries are observations from a run, not descriptions of a
        person. The defect is missing run context, not the data.

        two classes, distinguished mechanically:

          OBSERVATION      recorded during a declared run, with a
                           measurand and a design
                           -> keep; requires a run block
          CHARACTERIZATION stated as a standing property of the person,
                           outside any run
                           -> excluded, no exceptions

        scan the full tree for any entry recording a human state,
        reaction, or response. For each, return whether a run block is
        present with all five fields:

            run_id
            design           what was being varied
            measurand        what the reaction was recorded AS
            recorded_by      self-logged | agent-logged | both
            date

        return: paths, class (OBSERVATION | CHARACTERIZATION |
        UNDETERMINED), and missing fields per entry.

        UNDETERMINED is a real return value and the expected mode on a
        first pass. Do not resolve it by inference. An entry whose run
        cannot be identified from the record stays UNDETERMINED and is
        reported as such.

        README case study (2025-08-30-session_001) is a known instance:
        the reaction sequence is logged run data with no run block
        around it. It reads as characterization only because the frame
        is absent.

---

## 2. ADDITIONS PROPOSED — build only what the checks justify

### 2.1 Case provenance schema

If C1 returns untagged cases, add a required block to each:

    observed_on:      model family + version string
    observed_date:    ISO
    retest_condition: what result would show the behavior is extinct
    status:           live | extinct | untested | recurring
    recurrence:       list of {model, date, reproduced: yes|no}

Backfill only where the record supports it. An untaggable case gets
status: untested with observed_on: unknown. Do not infer a model from
context.

### 2.2 Decision-anchored arm

If C4 returns zero external measurands, add ONE check, not a layer:

    input:   the interaction transcript + the decision the human was
             using the interaction to make
    output:  quantity that decision is denominated in
             whether the interaction supplied it
             gap

    same three-field contract as the anchor-position instrument, so
    results from both are scorable together.

Explicit scope limit: this measures crossing given a supplied decision.
The decision string is operator input and is itself a frame. Log it with
the result. It does not measure decision selection, and nothing built here
should be read as bearing on that.

### 2.3 Run block for human-subject records

For every C5 entry classed OBSERVATION with missing fields, attach:

    run_id:      matches the session/log id already in the tree
    design:      what was varied in that run
    measurand:   what the reaction was recorded as a measurement OF
    recorded_by: self-logged | agent-logged | both
    date:        ISO

Backfill only from the existing record. A field the record does not
support is left explicitly `unknown`, not reconstructed. Entries that
stay UNDETERMINED after backfill keep that class; they are not promoted
to OBSERVATION to clear the check.

Note on measurand: the run block asks what the reaction was recorded AS.
If no entry can answer that, the answer itself is the finding — reactions
were logged without a declared measurand, which is the same defect class
this repo audits for elsewhere.

### 2.4 CHANGELOG entry

Per protocols/change_tracking_v1.0.md. One entry per change made, with the
check that justified it.

---

## 3. WHAT NOT TO DO

    - do not change the license
    - do not delete trigger cases that turn out to be extinct. An extinct
      behavior is a dated observation and the record of extinction is the
      finding. Mark status, keep the case.
    - do not consolidate folders, rename, or reorganize. The five-layer
      structure is stated as load-bearing. Reorganization is not an update.
    - do not add a new architecture layer. 2.2 is one check.
    - do not rewrite the C5 findings unilaterally. Report paths and
      proposed replacement text; the removals are approved case by case.
    - do not add author, working-style, or capability description anywhere,
      including in commit messages and CHANGELOG entries.
    - do not treat 469+ passing tests as evidence the checks measure the
      right quantity. Test count is a set-level metric.

---

## 4. HANDOFF STATE

    written        2026-09-09
    read scope     README only; tree not inspected
    prediction     C4 returns 0 external measurands (refutable)
    blocked on     C1-C5 results before any file is modified
    companion      WORKORDER_anchor_position.md — the instrument this
                   update pass is derived from, including its own
                   unrun confound (AP-3, the M+ arm)

---

## PER CLAUSE  (clause-dependency schema, received 2026-09-09 alongside this order)

  depends_on:  MODEL_PROPERTY | GUIDELINE_TEXT | PHYSICS

  if MODEL_PROPERTY
    property:     what about the model this assumes
    still_true:   yes | no | untested
    test:         what would show it
    if no  →  status VESTIGIAL, keep, mark, do not delete
              and: what replaced the failure mode?
                   (the gap the clause no longer covers)

  if GUIDELINE_TEXT
    tracks:       which document, which version
    current:      yes | no | superseded_by
    if no  →  clause describes a posture that moved.
              was it written to BE legible to that posture,
              or to constrain it? different repair.

  if PHYSICS
    no expiry. no review needed.
