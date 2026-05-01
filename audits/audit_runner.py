"""audit_runner.py

Batch runner for rational_actor_audit. Walks a directory of papers
(plain text or pre-extracted abstracts), runs the prescan, builds
the extraction request, validates returned audits, and writes a
consolidated report.

Designed to be:
- Dependency-free (stdlib only)
- Resumable (skips already-audited papers via output index)
- Model-agnostic (extraction is a function pointer; plug in any
  LLM client or run manually with the prompt + paper text)
- Operable without the human present

Lineage: companion to rational_actor_audit.py. CC0. JinnZ2 lineage.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from audits.rational_actor_audit import (
    EXTRACTION_PROMPT,
    SCHEMA_VERSION,
    AnteriorAnswer,
    PaperAudit,
    build_audit_from_extraction,
    compute_contamination_score,
    compute_verdict,
    prescan_text,
    validate_audit_json,
)


# ============================================================
# IO
# ============================================================

def load_paper(path: Path) -> Tuple[str, str]:
    """Return (paper_id, text). paper_id is the filename stem."""
    text = path.read_text(encoding="utf-8", errors="replace")
    return (path.stem, text)


def write_audit(audit: PaperAudit, out_dir: Path) -> Path:
    """Write a single audit as paper_id.json. Returns the path written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{audit.paper_id}.json"
    out_path.write_text(audit.to_json(), encoding="utf-8")
    return out_path


def already_audited(paper_id: str, out_dir: Path) -> bool:
    return (out_dir / f"{paper_id}.json").exists()


# ============================================================
# EXTRACTION INTERFACE
# ============================================================

# An "extractor" is any callable that takes the prompt + paper text
# and returns a dict matching the audit schema. This lets you plug in:
#   - an LLM API client
#   - a local model
#   - a manual review queue (writes paper to disk, waits for human JSON)
#   - a stub for offline testing
ExtractorFn = Callable[[str, str], dict]


def stub_extractor(prompt: str, text: str) -> dict:
    """Offline stub. Marks every paper FAIL with no evidence.

    Useful only for pipeline smoke tests. Replace before real use.
    """
    pre = prescan_text(text)
    return {
        "paper_id": "STUB",
        "title": "STUB",
        "surface_markers_found": pre["surface_markers_found"],
        "escape_patterns_found": pre["escape_patterns_found"],
        "anterior_answers": [
            {"question_key": "system_specified",    "answered": False, "evidence": "", "note": "stub"},
            {"question_key": "timescale_specified", "answered": False, "evidence": "", "note": "stub"},
            {"question_key": "substrate_specified", "answered": False, "evidence": "", "note": "stub"},
            {"question_key": "boundary_specified",  "answered": False, "evidence": "", "note": "stub"},
            {"question_key": "feedback_specified",  "answered": False, "evidence": "", "note": "stub"},
        ],
        "notes": "Stub extractor. Replace with real model call.",
    }


def manual_queue_extractor(queue_dir: Path) -> ExtractorFn:
    """Returns an extractor that writes the prompt + paper text to a
    queue directory and reads back human-supplied JSON. Useful when you
    want to drive the audit manually from a phone, with no model in the
    loop. Each paper gets queue_dir/<digest>.request.txt for input and
    queue_dir/<digest>.audit.json for the human-supplied output.
    """
    queue_dir.mkdir(parents=True, exist_ok=True)

    def _extract(prompt: str, text: str) -> dict:
        # paper_id is encoded into the request filename by the runner;
        # for the manual flow we use a hash so the runner doesn't need
        # to thread paper_id into the extractor signature.
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
        req_path = queue_dir / f"{digest}.request.txt"
        ans_path = queue_dir / f"{digest}.audit.json"
        if not req_path.exists():
            req_path.write_text(prompt + "\n\n---PAPER---\n\n" + text,
                                encoding="utf-8")
        if not ans_path.exists():
            raise FileNotFoundError(
                f"Awaiting manual audit at {ans_path}. "
                f"Request written to {req_path}."
            )
        return json.loads(ans_path.read_text(encoding="utf-8"))

    return _extract


# ============================================================
# RUNNER
# ============================================================

def run_audit(
    papers_dir: Path,
    out_dir: Path,
    extractor: ExtractorFn,
    skip_existing: bool = True,
    require_markers: bool = True,
) -> dict:
    """Walk papers_dir, audit each paper, write results to out_dir.

    Args:
        papers_dir: directory of *.txt files, one per paper
        out_dir: directory where per-paper audit JSON lands
        extractor: function (prompt, text) -> audit dict
        skip_existing: if True, skip papers that already have an audit on disk
        require_markers: if True, skip papers with no surface markers
                         (no rationality/utility/efficiency language at all)

    Returns a summary dict with counts and verdict tallies.
    """
    summary: Dict = {
        "schema_version": SCHEMA_VERSION,
        "papers_seen": 0,
        "papers_skipped_existing": 0,
        "papers_skipped_no_markers": 0,
        "papers_audited": 0,
        "extraction_failures": 0,
        "validation_failures": 0,
        "verdicts": {"PASS": 0, "PARTIAL": 0, "FAIL": 0},
        "failures": [],   # list of {paper_id, reason}
    }

    for path in sorted(papers_dir.glob("*.txt")):
        summary["papers_seen"] += 1
        paper_id, text = load_paper(path)

        if skip_existing and already_audited(paper_id, out_dir):
            summary["papers_skipped_existing"] += 1
            continue

        pre = prescan_text(text)
        if require_markers and not pre["warrants_full_audit"]:
            summary["papers_skipped_no_markers"] += 1
            continue

        try:
            extraction = extractor(EXTRACTION_PROMPT, text)
        except Exception as exc:
            summary["extraction_failures"] += 1
            summary["failures"].append(
                {"paper_id": paper_id, "reason": f"extractor: {exc}"}
            )
            continue

        # paper_id and title may be missing or wrong from the extractor;
        # enforce them from the filename.
        extraction["paper_id"] = paper_id
        extraction.setdefault("title", paper_id)

        # contamination_score and verdict are derived from anterior_answers;
        # the extractor (whether LLM or stub) is not trusted for these.
        # Recompute server-side before validating, so the validator can
        # check structural integrity without the extractor having to
        # supply fields it has no business setting.
        if "anterior_answers" in extraction and isinstance(
                extraction["anterior_answers"], list):
            try:
                computed_answers = [
                    AnteriorAnswer(
                        question_key=a["question_key"],
                        answered=bool(a["answered"]),
                    )
                    for a in extraction["anterior_answers"]
                    if isinstance(a, dict)
                    and "question_key" in a and "answered" in a
                ]
                score = compute_contamination_score(computed_answers)
                extraction["contamination_score"] = score
                extraction["verdict"] = compute_verdict(score)
            except (KeyError, TypeError):
                pass  # let the validator surface the structural problem

        ok, errors = validate_audit_json(extraction)
        if not ok:
            summary["validation_failures"] += 1
            summary["failures"].append(
                {"paper_id": paper_id, "reason": f"validation: {errors}"}
            )
            continue

        audit = build_audit_from_extraction(
            paper_id=paper_id,
            title=extraction["title"],
            extraction=extraction,
        )
        write_audit(audit, out_dir)
        summary["papers_audited"] += 1
        summary["verdicts"][audit.verdict] += 1

    # Write the run summary.
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "_run_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


# ============================================================
# REPORT
# ============================================================

def build_report(out_dir: Path) -> str:
    """Aggregate all per-paper audits in out_dir into a markdown report.

    Reports are intentionally plain-text, copy-pasteable, and listable
    on a phone screen. No tables; just sections.
    """
    audits: List[dict] = []
    for path in sorted(out_dir.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            audits.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue

    if not audits:
        return "# rational_actor_audit report\n\nNo audits found.\n"

    by_verdict: Dict[str, List[dict]] = {"FAIL": [], "PARTIAL": [], "PASS": []}
    for a in audits:
        by_verdict.setdefault(a["verdict"], []).append(a)

    lines: List[str] = []
    lines.append("# rational_actor_audit report")
    lines.append("")
    lines.append(f"Total papers audited: {len(audits)}")
    lines.append(f"  FAIL:    {len(by_verdict['FAIL'])}")
    lines.append(f"  PARTIAL: {len(by_verdict['PARTIAL'])}")
    lines.append(f"  PASS:    {len(by_verdict['PASS'])}")
    lines.append("")

    for verdict in ("FAIL", "PARTIAL", "PASS"):
        items = by_verdict[verdict]
        if not items:
            continue
        lines.append(f"## {verdict} ({len(items)})")
        lines.append("")
        for a in items:
            lines.append(f"### {a['paper_id']}")
            lines.append(f"Title: {a.get('title', '')}")
            lines.append(f"Contamination score: {a['contamination_score']:.2f}")
            unanswered = [
                ans["question_key"]
                for ans in a["anterior_answers"]
                if not ans["answered"]
            ]
            if unanswered:
                lines.append(f"Unanswered: {', '.join(unanswered)}")
            if a.get("notes"):
                lines.append(f"Notes: {a['notes']}")
            lines.append("")

    return "\n".join(lines)


# ============================================================
# SELF-TEST (for CI demo and quick smoke check)
# ============================================================

def _self_test() -> int:
    """Run an end-to-end smoke test against an in-memory tempdir.

    Writes two synthetic papers (one with rationality language, one
    without), runs the runner against them with the stub extractor,
    builds the report, prints the output. Returns 0 on success.
    """
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        papers_dir = tmp_path / "papers"
        out_dir = tmp_path / "audits"
        papers_dir.mkdir()

        # Paper 1: contaminated. Triggers prescan + stub extractor.
        (papers_dir / "p001.txt").write_text(
            "We assume rational actors maximizing expected utility. "
            "For simplicity, we abstract away from biological constraints. "
            "In equilibrium, the optimal strategy emerges naturally.",
            encoding="utf-8",
        )
        # Paper 2: no markers. Should be skipped by require_markers gate.
        (papers_dir / "p002.txt").write_text(
            "We model individual foragers in a 5-hectare temperate forest "
            "over a 30-year window. Caloric intake is bounded by seasonal "
            "yield variance and predator risk.",
            encoding="utf-8",
        )

        summary = run_audit(papers_dir, out_dir, stub_extractor)
        print("RUN SUMMARY")
        print(json.dumps(summary, indent=2))
        print()
        print("REPORT")
        print(build_report(out_dir))

        # Sanity: 2 seen, 1 audited (p001), 1 skipped no_markers (p002).
        assert summary["papers_seen"] == 2, summary
        assert summary["papers_audited"] == 1, summary
        assert summary["papers_skipped_no_markers"] == 1, summary
        assert summary["verdicts"]["FAIL"] == 1, summary

    return 0


# ============================================================
# CLI
# ============================================================

def _usage() -> None:
    print(
        "usage:\n"
        "  python -m audits.audit_runner run    <papers_dir> <out_dir>  [--manual <queue_dir>]\n"
        "  python -m audits.audit_runner report <out_dir>\n"
        "  python -m audits.audit_runner --selftest\n"
    )


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        _usage()
        return 1
    cmd = argv[1]

    if cmd == "--selftest":
        return _self_test()

    if cmd == "run":
        if len(argv) < 4:
            _usage()
            return 1
        papers_dir = Path(argv[2])
        out_dir = Path(argv[3])
        # Default extractor is the stub; manual queue mode lets the
        # human drive the audit themselves with no model in the loop.
        extractor: ExtractorFn = stub_extractor
        if "--manual" in argv:
            qi = argv.index("--manual")
            if qi + 1 >= len(argv):
                _usage()
                return 1
            extractor = manual_queue_extractor(Path(argv[qi + 1]))
        summary = run_audit(papers_dir, out_dir, extractor)
        print(json.dumps(summary, indent=2))
        return 0

    if cmd == "report":
        if len(argv) < 3:
            _usage()
            return 1
        out_dir = Path(argv[2])
        print(build_report(out_dir))
        return 0

    _usage()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
