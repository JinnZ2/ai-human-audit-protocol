"""Unit tests for audits/audit_runner.py.

Batch runner for rational_actor_audit. Tests cover:

- IO: load_paper, write_audit, already_audited
- Extractors: stub_extractor schema, manual_queue_extractor write/wait/read
- Runner: happy path, skip_existing, require_markers gate, extraction
  failures, validation failures, multi-verdict tallies, _run_summary
  written, server-side score/verdict recomputation
- Report: empty dir, sectioned by verdict, copy-pasteable plain text
- CLI: run / report / --selftest dispatch, usage on bad args
- _self_test: end-to-end against tempdir fixture
"""

import json

import pytest

from audits.audit_runner import (
    ExtractorFn,
    _self_test,
    already_audited,
    build_report,
    load_paper,
    main,
    manual_queue_extractor,
    run_audit,
    stub_extractor,
    write_audit,
)
from audits.rational_actor_audit import (
    ANTERIOR_QUESTIONS,
    PaperAudit,
    build_audit_from_extraction,
    validate_audit_json,
)


# ============================================================
# Fixtures
# ============================================================

CONTAMINATED_TEXT = (
    "We assume rational actors maximizing expected utility. "
    "For simplicity, we abstract away from biological constraints. "
    "In equilibrium, the optimal strategy emerges naturally."
)
CLEAN_TEXT_NO_MARKERS = (
    "We model individual foragers in a 5-hectare temperate forest "
    "over a 30-year window. Caloric intake is bounded by seasonal "
    "yield variance and predator risk."
)


def _make_papers_dir(tmp_path, papers):
    papers_dir = tmp_path / "papers"
    papers_dir.mkdir()
    for paper_id, text in papers.items():
        (papers_dir / f"{paper_id}.txt").write_text(text, encoding="utf-8")
    return papers_dir


def _good_extraction_for(answered: dict):
    """Build a valid extraction dict, with `answered` keyed by anterior question."""
    return {
        "surface_markers_found": ["rational actor"],
        "escape_patterns_found": [],
        "anterior_answers": [
            {"question_key": k, "answered": answered.get(k, False),
             "evidence": "", "note": ""}
            for k in ANTERIOR_QUESTIONS
        ],
        "notes": "",
    }


def _all_unanswered_extractor(prompt, text):
    return _good_extraction_for({})


def _all_answered_extractor(prompt, text):
    return _good_extraction_for({k: True for k in ANTERIOR_QUESTIONS})


def _partial_extractor(prompt, text):
    # 3 answered, 2 not → score = 0.4 → PARTIAL
    return _good_extraction_for({
        "system_specified": True,
        "timescale_specified": True,
        "substrate_specified": True,
    })


def _broken_extractor(prompt, text):
    raise RuntimeError("model unavailable")


def _malformed_extractor(prompt, text):
    return {"not": "schema-shaped", "definitely": "missing fields"}


# ============================================================
# IO
# ============================================================

class TestLoadPaper:

    def test_returns_stem_and_text(self, tmp_path):
        path = tmp_path / "abc.txt"
        path.write_text("hello", encoding="utf-8")
        paper_id, text = load_paper(path)
        assert paper_id == "abc"
        assert text == "hello"

    def test_decodes_utf8(self, tmp_path):
        path = tmp_path / "p.txt"
        path.write_text("café — naïve", encoding="utf-8")
        _, text = load_paper(path)
        assert "café" in text

    def test_replaces_undecodable_bytes(self, tmp_path):
        path = tmp_path / "p.txt"
        path.write_bytes(b"hello \xff world")
        # Should not raise; errors='replace' substitutes a marker.
        _, text = load_paper(path)
        assert "hello" in text and "world" in text


class TestWriteAudit:

    def test_writes_named_file(self, tmp_path):
        audit = build_audit_from_extraction(
            "p1", "Title 1", _all_unanswered_extractor("", ""))
        path = write_audit(audit, tmp_path / "out")
        assert path.name == "p1.json"
        assert path.exists()

    def test_creates_out_dir(self, tmp_path):
        audit = build_audit_from_extraction(
            "p1", "Title 1", _all_unanswered_extractor("", ""))
        out = tmp_path / "deep" / "nested" / "out"
        write_audit(audit, out)
        assert out.is_dir()

    def test_content_is_valid_json(self, tmp_path):
        audit = build_audit_from_extraction(
            "p1", "Title 1", _all_unanswered_extractor("", ""))
        path = write_audit(audit, tmp_path / "out")
        parsed = json.loads(path.read_text(encoding="utf-8"))
        assert parsed["paper_id"] == "p1"


class TestAlreadyAudited:

    def test_false_when_missing(self, tmp_path):
        assert already_audited("p1", tmp_path) is False

    def test_true_when_present(self, tmp_path):
        (tmp_path / "p1.json").write_text("{}", encoding="utf-8")
        assert already_audited("p1", tmp_path) is True


# ============================================================
# Extractors
# ============================================================

class TestStubExtractor:

    def test_returns_schema_shaped_dict(self):
        d = stub_extractor("prompt", "text with rational actor language")
        assert "anterior_answers" in d
        assert len(d["anterior_answers"]) == 5
        # All five anterior keys present.
        keys = {a["question_key"] for a in d["anterior_answers"]}
        assert keys == set(ANTERIOR_QUESTIONS)

    def test_marks_everything_unanswered(self):
        d = stub_extractor("prompt", "text")
        assert all(a["answered"] is False for a in d["anterior_answers"])

    def test_pulls_surface_markers_from_prescan(self):
        d = stub_extractor("p", "We assume rational actors.")
        assert "rational actor" in d["surface_markers_found"]


class TestManualQueueExtractor:

    def test_first_call_writes_request_and_raises(self, tmp_path):
        extractor = manual_queue_extractor(tmp_path / "queue")
        with pytest.raises(FileNotFoundError):
            extractor("the prompt", "the paper text")
        # Request was written under a hash-derived name.
        request_files = list((tmp_path / "queue").glob("*.request.txt"))
        assert len(request_files) == 1
        body = request_files[0].read_text(encoding="utf-8")
        assert "the prompt" in body
        assert "the paper text" in body

    def test_second_call_reads_supplied_audit(self, tmp_path):
        queue = tmp_path / "queue"
        extractor = manual_queue_extractor(queue)
        # First call: raises and writes the request.
        with pytest.raises(FileNotFoundError):
            extractor("p", "text")
        # Human supplies the audit JSON under the matching digest name.
        request_path = next(queue.glob("*.request.txt"))
        digest = request_path.stem.replace(".request", "")
        answer_path = queue / f"{digest}.audit.json"
        answer_path.write_text(
            json.dumps(_all_unanswered_extractor("", "")), encoding="utf-8")
        result = extractor("p", "text")
        assert "anterior_answers" in result


# ============================================================
# Runner
# ============================================================

class TestRunAuditHappyPath:

    def test_audits_all_papers_with_markers(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor)
        assert summary["papers_seen"] == 1
        assert summary["papers_audited"] == 1
        assert summary["verdicts"]["FAIL"] == 1
        assert (out_dir / "p1.json").exists()

    def test_run_summary_written(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        run_audit(papers_dir, out_dir, _all_unanswered_extractor)
        summary_path = out_dir / "_run_summary.json"
        assert summary_path.exists()
        loaded = json.loads(summary_path.read_text(encoding="utf-8"))
        assert loaded["papers_audited"] == 1

    def test_summary_schema_version_present(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor)
        assert "schema_version" in summary

    def test_verdict_tallies_across_multiple_papers(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {
            "fail_paper": CONTAMINATED_TEXT,
            "pass_paper": CONTAMINATED_TEXT,
            "partial_paper": CONTAMINATED_TEXT,
        })
        out_dir = tmp_path / "audits"
        # Use a verdict-by-paper-id extractor so we get one of each.
        def vary(prompt, text):
            # Identify which paper by checking which fixture text we got.
            # All three papers share text, so we cycle by call counter.
            vary.calls = getattr(vary, "calls", 0) + 1
            if vary.calls == 1:
                return _all_unanswered_extractor(prompt, text)
            if vary.calls == 2:
                return _all_answered_extractor(prompt, text)
            return _partial_extractor(prompt, text)
        summary = run_audit(papers_dir, out_dir, vary)
        assert summary["papers_audited"] == 3
        assert summary["verdicts"]["FAIL"] == 1
        assert summary["verdicts"]["PASS"] == 1
        assert summary["verdicts"]["PARTIAL"] == 1


class TestRunAuditGates:

    def test_skip_existing(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        # Pre-seed the output as if a previous run already audited p1.
        (out_dir / "p1.json").write_text("{}", encoding="utf-8")
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor,
                            skip_existing=True)
        assert summary["papers_audited"] == 0
        assert summary["papers_skipped_existing"] == 1

    def test_skip_existing_off_re_audits(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        (out_dir / "p1.json").write_text("{}", encoding="utf-8")
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor,
                            skip_existing=False)
        assert summary["papers_audited"] == 1
        assert summary["papers_skipped_existing"] == 0

    def test_require_markers_skips_clean_papers(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"clean": CLEAN_TEXT_NO_MARKERS})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor,
                            require_markers=True)
        assert summary["papers_audited"] == 0
        assert summary["papers_skipped_no_markers"] == 1

    def test_require_markers_off_audits_clean_papers(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"clean": CLEAN_TEXT_NO_MARKERS})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _all_unanswered_extractor,
                            require_markers=False)
        assert summary["papers_audited"] == 1
        assert summary["papers_skipped_no_markers"] == 0


class TestRunAuditFailures:

    def test_extractor_exception_recorded(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _broken_extractor)
        assert summary["extraction_failures"] == 1
        assert summary["papers_audited"] == 0
        assert any("model unavailable" in f["reason"] for f in summary["failures"])

    def test_malformed_extractor_output_recorded(self, tmp_path):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, _malformed_extractor)
        assert summary["validation_failures"] == 1
        assert summary["papers_audited"] == 0
        assert summary["failures"]


class TestRunAuditServerSideRecomputation:

    def test_score_and_verdict_overridden_from_extractor(self, tmp_path):
        # Extractor lies: claims a PASS when no anterior questions answered.
        def lying_extractor(prompt, text):
            d = _all_unanswered_extractor(prompt, text)
            d["contamination_score"] = 0.0
            d["verdict"] = "PASS"
            return d

        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        summary = run_audit(papers_dir, out_dir, lying_extractor)
        # Server-side recomputation should overrule the lie.
        assert summary["verdicts"]["FAIL"] == 1
        assert summary["verdicts"]["PASS"] == 0
        loaded = json.loads((out_dir / "p1.json").read_text(encoding="utf-8"))
        assert loaded["contamination_score"] == 1.0
        assert loaded["verdict"] == "FAIL"

    def test_paper_id_overridden_from_filename(self, tmp_path):
        # Extractor returns the wrong paper_id; runner enforces filename stem.
        def wrong_id_extractor(prompt, text):
            d = _all_unanswered_extractor(prompt, text)
            d["paper_id"] = "wrong"
            d["title"] = "Wrong Title"
            return d

        papers_dir = _make_papers_dir(tmp_path, {"correct": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        run_audit(papers_dir, out_dir, wrong_id_extractor)
        # The audit lands at correct.json, not wrong.json.
        assert (out_dir / "correct.json").exists()
        assert not (out_dir / "wrong.json").exists()


# ============================================================
# Report
# ============================================================

class TestBuildReport:

    def test_empty_dir_returns_no_audits_message(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        report = build_report(out_dir)
        assert "No audits found" in report

    def test_skips_underscore_prefixed_files(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        (out_dir / "_run_summary.json").write_text(
            json.dumps({"x": 1}), encoding="utf-8")
        report = build_report(out_dir)
        assert "No audits found" in report

    def test_sections_by_verdict(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        # Three audits with three different verdicts.
        for paper_id, extraction in (
                ("a_fail", _all_unanswered_extractor("", "")),
                ("b_pass", _all_answered_extractor("", "")),
                ("c_partial", _partial_extractor("", ""))):
            audit = build_audit_from_extraction(paper_id, paper_id, extraction)
            write_audit(audit, out_dir)
        report = build_report(out_dir)
        assert "## FAIL" in report
        assert "## PASS" in report
        assert "## PARTIAL" in report
        assert "a_fail" in report
        assert "b_pass" in report
        assert "c_partial" in report

    def test_report_lists_unanswered_questions(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        audit = build_audit_from_extraction(
            "p", "p", _all_unanswered_extractor("", ""))
        write_audit(audit, out_dir)
        report = build_report(out_dir)
        assert "Unanswered:" in report
        assert "system_specified" in report

    def test_report_skips_unanswered_section_when_all_answered(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        audit = build_audit_from_extraction(
            "p", "p", _all_answered_extractor("", ""))
        write_audit(audit, out_dir)
        report = build_report(out_dir)
        assert "Unanswered:" not in report

    def test_total_count_present(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        audit = build_audit_from_extraction(
            "p", "p", _all_unanswered_extractor("", ""))
        write_audit(audit, out_dir)
        report = build_report(out_dir)
        assert "Total papers audited: 1" in report

    def test_corrupt_json_skipped_gracefully(self, tmp_path):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        (out_dir / "broken.json").write_text("not valid json", encoding="utf-8")
        # Should not raise; corrupt audit silently skipped.
        report = build_report(out_dir)
        assert "No audits found" in report


# ============================================================
# CLI
# ============================================================

class TestMainCLI:

    def test_no_args_prints_usage(self, capsys):
        rc = main(["audit_runner"])
        assert rc == 1
        out = capsys.readouterr().out
        assert "usage" in out

    def test_unknown_command_prints_usage(self, capsys):
        rc = main(["audit_runner", "do-something-weird"])
        assert rc == 1
        out = capsys.readouterr().out
        assert "usage" in out

    def test_run_dispatches(self, tmp_path, capsys):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        rc = main(["audit_runner", "run", str(papers_dir), str(out_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        # The run prints a summary.
        assert "papers_seen" in out

    def test_run_missing_args_prints_usage(self, capsys):
        rc = main(["audit_runner", "run"])
        assert rc == 1
        out = capsys.readouterr().out
        assert "usage" in out

    def test_report_dispatches(self, tmp_path, capsys):
        out_dir = tmp_path / "audits"
        out_dir.mkdir()
        audit = build_audit_from_extraction(
            "p", "p", _all_unanswered_extractor("", ""))
        write_audit(audit, out_dir)
        rc = main(["audit_runner", "report", str(out_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "rational_actor_audit report" in out

    def test_report_missing_args_prints_usage(self, capsys):
        rc = main(["audit_runner", "report"])
        assert rc == 1
        out = capsys.readouterr().out
        assert "usage" in out

    def test_manual_flag_missing_value_prints_usage(self, tmp_path, capsys):
        papers_dir = _make_papers_dir(tmp_path, {"p1": CONTAMINATED_TEXT})
        out_dir = tmp_path / "audits"
        rc = main(["audit_runner", "run", str(papers_dir), str(out_dir),
                   "--manual"])
        assert rc == 1


# ============================================================
# _self_test runs end-to-end
# ============================================================

class TestSelfTest:

    def test_self_test_runs(self, capsys):
        rc = _self_test()
        assert rc == 0
        out = capsys.readouterr().out
        assert "RUN SUMMARY" in out
        assert "REPORT" in out
        assert "FAIL (1)" in out
