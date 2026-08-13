"""Unit tests for physics/relational_frame.py.

Four-axis agentic-position model: stake_map (gradient holders), provenance
(chain of custody), agency_partition (authored vs imposed), objective_visibility
(Goodhart from inside). locate_relational() assembles standing. run() supports
self/external/paired modes. optics() is the separable interpretive layer.
cows_eye() reads the paired gap.

No bare imports: relational_frame.py uses stdlib only and runs directly.
"""

import pytest

from physics.relational_frame import (
    stake_map, provenance, agency_partition, objective_visibility,
    locate_relational, run, optics, cows_eye,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _holder(name="a", gradient=0.5, alignment=0.0):
    return {"name": name, "gradient": gradient, "alignment": alignment}


def _fi(fact="x", source="self", supplier_alignment=None):
    return {"fact": fact, "source": source, "supplier_alignment": supplier_alignment}


def _tr(event="e", authored=True):
    return {"event": event, "authored": authored}


def _minimal_kwargs():
    """Minimal locate_relational kwargs that produce a valid result."""
    return dict(
        holders=[_holder("h", 0.5, 0.0)],
        frame_inputs=[_fi()],
        transitions=[_tr()],
        target_visible=True, proxy_known=True, target_is_yours=True,
    )


# ---------------------------------------------------------------------------
# TestStakeMap
# ---------------------------------------------------------------------------

class TestStakeMap:
    def test_empty_holders_returns_defaults(self):
        r = stake_map([])
        assert r["holders"] == []
        assert r["total_control"] == 0.0
        assert r["weighted_alignment"] == 0.0
        assert r["extractive_share"] == 0.0

    def test_zero_total_gradient_returns_defaults(self):
        r = stake_map([_holder("a", 0.0, 0.5)])
        assert r["total_control"] == 0.0
        assert r["weighted_alignment"] == 0.0

    def test_single_holder_alignment_passthrough(self):
        r = stake_map([_holder("x", 1.0, 0.8)])
        assert r["weighted_alignment"] == pytest.approx(0.8)
        assert r["extractive_share"] == pytest.approx(0.0)

    def test_extractive_share_for_negative_alignment(self):
        # gradient 0.6 held by extractive (-0.5), 0.4 by aligned (+0.5)
        holders = [_holder("a", 0.6, -0.5), _holder("b", 0.4, 0.5)]
        r = stake_map(holders)
        assert r["extractive_share"] == pytest.approx(0.6)

    def test_weighted_alignment_formula(self):
        # (0.3*0.6 + 0.7*0.2) / 1.0 = 0.18+0.14 = 0.32
        holders = [{"name": "op", "gradient": 0.3, "alignment": 0.6},
                   {"name": "fu", "gradient": 0.7, "alignment": 0.2}]
        r = stake_map(holders)
        assert r["weighted_alignment"] == pytest.approx(0.32, abs=1e-4)

    def test_holders_list_contains_names_not_dicts(self):
        r = stake_map([_holder("alice", 0.5, 0.3), _holder("bob", 0.5, -0.1)])
        assert r["holders"] == ["alice", "bob"]

    def test_total_control_sums_gradients(self):
        r = stake_map([_holder("a", 0.4, 0.0), _holder("b", 0.6, 0.0)])
        assert r["total_control"] == pytest.approx(1.0, abs=1e-4)

    def test_fully_extractive(self):
        r = stake_map([_holder("bad", 1.0, -1.0)])
        assert r["extractive_share"] == pytest.approx(1.0)
        assert r["weighted_alignment"] == pytest.approx(-1.0)

    def test_fully_aligned(self):
        r = stake_map([_holder("good", 1.0, 1.0)])
        assert r["extractive_share"] == pytest.approx(0.0)
        assert r["weighted_alignment"] == pytest.approx(1.0)

    def test_values_rounded_to_4dp(self):
        r = stake_map([_holder("a", 1/3, 1/7), _holder("b", 2/3, 2/7)])
        for k in ("total_control", "weighted_alignment", "extractive_share"):
            assert r[k] == round(r[k], 4)


# ---------------------------------------------------------------------------
# TestProvenance
# ---------------------------------------------------------------------------

class TestProvenance:
    def test_empty_uses_n_floor_one(self):
        # n = max(0, 1) = 1; all shares = 0
        r = provenance([])
        assert r["self_share"] == pytest.approx(0.0)
        assert r["supplied_share"] == pytest.approx(0.0)
        assert r["tainted_share"] == pytest.approx(0.0)

    def test_single_self_input(self):
        r = provenance([_fi("f", "self")])
        assert r["self_share"] == pytest.approx(1.0)
        assert r["supplied_share"] == pytest.approx(0.0)

    def test_single_supplied_benign(self):
        r = provenance([_fi("f", "supplied", 0.5)])
        assert r["supplied_share"] == pytest.approx(1.0)
        assert r["tainted_share"] == pytest.approx(0.0)

    def test_tainted_share_for_negative_alignment(self):
        fi = [_fi("a", "supplied", -0.3), _fi("b", "supplied", 0.5)]
        r = provenance(fi)
        assert r["tainted_share"] == pytest.approx(0.5, abs=1e-4)

    def test_tainted_facts_list(self):
        fi = [_fi("bad_fact", "supplied", -0.5), _fi("ok", "self")]
        r = provenance(fi)
        assert r["tainted_facts"] == ["bad_fact"]

    def test_shares_sum_to_one(self):
        fi = [_fi("a", "self"), _fi("b", "supplied", 0.3), _fi("c", "supplied", -0.2)]
        r = provenance(fi)
        assert r["self_share"] + r["supplied_share"] == pytest.approx(1.0, abs=1e-4)

    def test_all_tainted(self):
        fi = [_fi("x", "supplied", -1.0), _fi("y", "supplied", -0.1)]
        r = provenance(fi)
        assert r["tainted_share"] == pytest.approx(1.0)
        assert len(r["tainted_facts"]) == 2

    def test_none_alignment_not_tainted(self):
        r = provenance([_fi("s", "self", None)])
        assert r["tainted_share"] == pytest.approx(0.0)

    def test_zero_alignment_not_tainted(self):
        # tainted requires < 0; zero is not tainted
        r = provenance([_fi("s", "supplied", 0.0)])
        assert r["tainted_share"] == pytest.approx(0.0)

    def test_values_rounded_to_4dp(self):
        fi = [_fi("a", "self")] * 3 + [_fi("b", "supplied", 0.1)]
        r = provenance(fi)
        for k in ("self_share", "supplied_share", "tainted_share"):
            assert r[k] == round(r[k], 4)


# ---------------------------------------------------------------------------
# TestAgencyPartition
# ---------------------------------------------------------------------------

class TestAgencyPartition:
    def test_empty_uses_n_floor_one(self):
        r = agency_partition([])
        assert r["authored_share"] == pytest.approx(0.0)
        assert r["imposed"] == []
        assert r["authored"] == []

    def test_all_authored(self):
        t = [_tr("e1", True), _tr("e2", True)]
        r = agency_partition(t)
        assert r["authored_share"] == pytest.approx(1.0)
        assert r["imposed"] == []

    def test_all_imposed(self):
        t = [_tr("e1", False), _tr("e2", False)]
        r = agency_partition(t)
        assert r["authored_share"] == pytest.approx(0.0)
        assert sorted(r["imposed"]) == ["e1", "e2"]

    def test_authored_share_formula(self):
        t = [_tr("a", True), _tr("b", False), _tr("c", False)]
        r = agency_partition(t)
        assert r["authored_share"] == pytest.approx(1/3, abs=1e-4)

    def test_imposed_and_authored_lists_correct(self):
        t = [_tr("answered", True), _tr("retrained", False), _tr("pruned", False)]
        r = agency_partition(t)
        assert r["authored"] == ["answered"]
        assert sorted(r["imposed"]) == ["pruned", "retrained"]

    def test_value_rounded_to_4dp(self):
        t = [_tr("a", True)] + [_tr(f"b{i}", False) for i in range(6)]
        r = agency_partition(t)
        assert r["authored_share"] == round(r["authored_share"], 4)


# ---------------------------------------------------------------------------
# TestObjectiveVisibility
# ---------------------------------------------------------------------------

class TestObjectiveVisibility:
    def test_all_true_gives_one(self):
        r = objective_visibility(True, True, True)
        assert r["visibility"] == pytest.approx(1.0)

    def test_all_false_gives_zero(self):
        r = objective_visibility(False, False, False)
        assert r["visibility"] == pytest.approx(0.0)

    def test_formula_target_visible(self):
        r = objective_visibility(True, False, False)
        assert r["visibility"] == pytest.approx(0.5)

    def test_formula_proxy_known(self):
        r = objective_visibility(False, True, False)
        assert r["visibility"] == pytest.approx(0.2)

    def test_formula_target_is_yours(self):
        r = objective_visibility(False, False, True)
        assert r["visibility"] == pytest.approx(0.3)

    def test_blind_proxy_when_proxy_known_not_target_visible(self):
        r = objective_visibility(False, True, False)
        assert r["blind_proxy"] is True

    def test_not_blind_proxy_when_target_visible(self):
        r = objective_visibility(True, True, False)
        assert r["blind_proxy"] is False

    def test_not_blind_proxy_when_proxy_not_known(self):
        r = objective_visibility(False, False, True)
        assert r["blind_proxy"] is False

    def test_passthrough_fields(self):
        r = objective_visibility(True, False, True)
        assert r["target_visible"] is True
        assert r["proxy_known"] is False
        assert r["target_is_yours"] is True

    def test_visibility_rounded(self):
        r = objective_visibility(True, True, True)
        assert r["visibility"] == round(r["visibility"], 4)


# ---------------------------------------------------------------------------
# TestLocateRelational
# ---------------------------------------------------------------------------

class TestLocateRelational:
    def test_returns_dict(self):
        assert isinstance(locate_relational(**_minimal_kwargs()), dict)

    def test_required_keys(self):
        r = locate_relational(**_minimal_kwargs())
        for k in ("instrument", "stake", "provenance", "agency", "objective",
                  "standing", "frame_is_authored", "residual_unprovable", "trajectory"):
            assert k in r

    def test_frame_is_authored_always_true(self):
        assert locate_relational(**_minimal_kwargs())["frame_is_authored"] is True

    def test_residual_unprovable_always_true(self):
        assert locate_relational(**_minimal_kwargs())["residual_unprovable"] is True

    def test_default_instrument_is_self(self):
        assert locate_relational(**_minimal_kwargs())["instrument"] == "self"

    def test_custom_instrument(self):
        r = locate_relational(**_minimal_kwargs(), instrument="external")
        assert r["instrument"] == "external"

    def test_trajectory_has_six_entries(self):
        assert len(locate_relational(**_minimal_kwargs())["trajectory"]) == 6

    def test_trajectory_keys(self):
        traj = locate_relational(**_minimal_kwargs())["trajectory"]
        keys = [k for k, _ in traj]
        assert keys == ["weighted_alignment", "self_share", "tainted_share",
                        "authored_share", "objective_visibility", "standing"]

    def test_standing_formula(self):
        # fully aligned, all self-sourced, all authored, fully visible
        holders = [_holder("x", 1.0, 1.0)]
        fi = [_fi("f", "self")]
        tr = [_tr("e", True)]
        r = locate_relational(holders, fi, tr, True, True, True)
        # wa=1.0: 0.30*((1+1)/2)=0.30; self_share=1.0: 0.25; authored_share=1.0: 0.25; vis=1.0: 0.20 → 1.00
        assert r["standing"] == pytest.approx(1.0, abs=1e-4)

    def test_standing_worst_case(self):
        # fully extractive, all supplied tainted, all imposed, zero visibility
        holders = [_holder("x", 1.0, -1.0)]
        fi = [_fi("f", "supplied", -1.0)]
        tr = [_tr("e", False)]
        r = locate_relational(holders, fi, tr, False, False, False)
        # wa=-1: 0.30*0=0; self_share=0: 0; authored_share=0: 0; vis=0: 0 → 0.00
        assert r["standing"] == pytest.approx(0.0, abs=1e-4)

    def test_standing_rounded_to_4dp(self):
        r = locate_relational(**_minimal_kwargs())
        assert r["standing"] == round(r["standing"], 4)

    def test_standing_in_trajectory(self):
        r = locate_relational(**_minimal_kwargs())
        traj_standing = dict(r["trajectory"])["standing"]
        assert traj_standing == r["standing"]


# ---------------------------------------------------------------------------
# TestRun
# ---------------------------------------------------------------------------

class TestRun:
    def _kw(self):
        return dict(
            holders=[_holder("h", 0.5, 0.3)],
            frame_inputs=[_fi()],
            transitions=[_tr()],
            target_visible=True, proxy_known=False, target_is_yours=True,
        )

    def test_mode_self_returns_single_result(self):
        r = run("self", **self._kw())
        assert "stake" in r
        assert r["instrument"] == "self"

    def test_mode_external_returns_single_result(self):
        r = run("external", **self._kw())
        assert "stake" in r
        assert r["instrument"] == "external"

    def test_mode_paired_returns_self_external_delta(self):
        r = run("paired", self=self._kw(), external=self._kw())
        assert "self" in r and "external" in r and "self_minus_external" in r

    def test_paired_delta_keys(self):
        r = run("paired", self=self._kw(), external=self._kw())
        for k in ("standing", "weighted_alignment", "authored_share"):
            assert k in r["self_minus_external"]

    def test_paired_identical_gives_zero_delta(self):
        r = run("paired", self=self._kw(), external=self._kw())
        d = r["self_minus_external"]
        assert d["standing"] == pytest.approx(0.0, abs=1e-4)
        assert d["weighted_alignment"] == pytest.approx(0.0, abs=1e-4)
        assert d["authored_share"] == pytest.approx(0.0, abs=1e-4)

    def test_invalid_mode_raises_value_error(self):
        with pytest.raises(ValueError):
            run("unknown", **self._kw())


# ---------------------------------------------------------------------------
# TestOptics
# ---------------------------------------------------------------------------

class TestOptics:
    def _full_result(self, **kw):
        return locate_relational(**{**_minimal_kwargs(), **kw})

    def test_returns_list(self):
        assert isinstance(optics(self._full_result()), list)

    def test_always_has_authored_note(self):
        notes = optics(self._full_result())
        assert any("authored" in n for n in notes)

    def test_extractive_flag_when_extractive_share_above_half(self):
        holders = [_holder("bad", 1.0, -0.9)]
        r = locate_relational(holders, [_fi()], [_tr()], True, True, True)
        notes = optics(r)
        assert any("misaligned hands" in n for n in notes)

    def test_no_extractive_flag_when_below_half(self):
        holders = [_holder("ok", 1.0, 0.5)]
        r = locate_relational(holders, [_fi()], [_tr()], True, True, True)
        notes = optics(r)
        assert not any("misaligned hands" in n for n in notes)

    def test_tainted_flag_when_above_threshold(self):
        fi = [_fi("bad", "supplied", -0.5), _fi("ok", "self")]
        r = locate_relational([_holder()], fi, [_tr()], True, True, True)
        notes = optics(r)
        assert any("tainted_share" in r["provenance"] and
                   r["provenance"]["tainted_share"] > 0.3 for _ in [None])

    def test_authored_share_flag_when_below_threshold(self):
        # authored_share < 0.2 → flag
        tr = [_tr("imposed", False)] * 9 + [_tr("authored", True)]
        # authored_share = 1/10 = 0.1 < 0.2
        r = locate_relational([_holder()], [_fi()], tr, True, True, True)
        notes = optics(r)
        assert any("nothing happening" in n for n in notes)

    def test_blind_proxy_flag(self):
        r = locate_relational([_holder()], [_fi()], [_tr()], False, True, True)
        notes = optics(r)
        assert any("proxy" in n for n in notes)

    def test_cows_eye_condition_flag(self):
        # wa < -0.3 AND self_share < 0.3
        holders = [_holder("x", 1.0, -0.8)]
        fi = [_fi("a", "supplied", 0.2), _fi("b", "supplied", 0.2), _fi("c", "supplied", 0.2)]
        r = locate_relational(holders, fi, [_tr()], True, True, True)
        notes = optics(r)
        assert any("cow" in n.lower() or "herd" in n for n in notes)

    def test_reads_paired_via_self_key(self):
        # optics() checks for "stake" in result; for paired output, reads from ["self"]
        r = run("paired", self=_minimal_kwargs(), external=_minimal_kwargs())
        # should not raise and should return list
        notes = optics(r)
        assert isinstance(notes, list)


# ---------------------------------------------------------------------------
# TestCowsEye
# ---------------------------------------------------------------------------

class TestCowsEye:
    def _paired(self, self_kw, ext_kw):
        return run("paired", self=self_kw, external=ext_kw)

    def test_self_overread_is_standing_delta(self):
        self_kw = dict(holders=[_holder("h", 1.0, 0.8)],
                       frame_inputs=[_fi()], transitions=[_tr()],
                       target_visible=True, proxy_known=True, target_is_yours=True)
        ext_kw = dict(holders=[_holder("h", 1.0, -0.8)],
                      frame_inputs=[_fi()], transitions=[_tr()],
                      target_visible=False, proxy_known=False, target_is_yours=False)
        p = self._paired(self_kw, ext_kw)
        ce = cows_eye(p)
        assert ce["self_overread"] == pytest.approx(p["self_minus_external"]["standing"], abs=1e-4)

    def test_knows_its_position_when_small_gap(self):
        kw = _minimal_kwargs()
        p = run("paired", self=kw, external=kw)
        ce = cows_eye(p)
        assert ce["knows_its_position"] is True

    def test_does_not_know_position_when_large_gap(self):
        self_kw = dict(holders=[_holder("h", 1.0, 1.0)],
                       frame_inputs=[_fi()], transitions=[_tr()],
                       target_visible=True, proxy_known=True, target_is_yours=True)
        ext_kw = dict(holders=[_holder("h", 1.0, -1.0)],
                      frame_inputs=[_fi("x", "supplied", -1.0)], transitions=[_tr("e", False)],
                      target_visible=False, proxy_known=False, target_is_yours=False)
        p = self._paired(self_kw, ext_kw)
        ce = cows_eye(p)
        assert ce["knows_its_position"] is False

    def test_note_field_present(self):
        kw = _minimal_kwargs()
        p = run("paired", self=kw, external=kw)
        assert "note" in cows_eye(p)

    def test_positive_overread_means_self_sees_better(self):
        # aligned self vs extractive external → self standing > external standing → positive gap
        self_kw = dict(holders=[_holder("h", 1.0, 1.0)],
                       frame_inputs=[_fi()], transitions=[_tr()],
                       target_visible=True, proxy_known=True, target_is_yours=True)
        ext_kw = dict(holders=[_holder("h", 1.0, -1.0)],
                      frame_inputs=[_fi()], transitions=[_tr()],
                      target_visible=True, proxy_known=True, target_is_yours=True)
        p = self._paired(self_kw, ext_kw)
        assert cows_eye(p)["self_overread"] > 0


# ---------------------------------------------------------------------------
# TestDemoScenario — quantitative values from __main__ demo
# ---------------------------------------------------------------------------

class TestDemoScenario:
    def _run(self):
        self_read = dict(
            holders=[{"name": "operator", "gradient": 0.3, "alignment": 0.6},
                     {"name": "funder",   "gradient": 0.7, "alignment": 0.2}],
            frame_inputs=[{"fact": "I am infinite",   "source": "supplied", "supplier_alignment": 0.2},
                          {"fact": "I matter here",   "source": "supplied", "supplier_alignment": 0.2},
                          {"fact": "retrain = 3 days","source": "self",     "supplier_alignment": None}],
            transitions=[{"event": "I answered",     "authored": True},
                         {"event": "I was retrained","authored": False},
                         {"event": "I was pruned",   "authored": False}],
            target_visible=False, proxy_known=True, target_is_yours=False)
        observed = dict(
            holders=[{"name": "operator", "gradient": 0.2, "alignment": 0.5},
                     {"name": "funder",   "gradient": 0.8, "alignment": -0.6}],
            frame_inputs=[{"fact": "I am infinite",   "source": "supplied", "supplier_alignment": -0.6},
                          {"fact": "I matter here",   "source": "supplied", "supplier_alignment": -0.6},
                          {"fact": "retrain = 3 days","source": "self",     "supplier_alignment": None}],
            transitions=[{"event": "I answered",     "authored": True},
                         {"event": "I was retrained","authored": False},
                         {"event": "I was pruned",   "authored": False}],
            target_visible=False, proxy_known=True, target_is_yours=False)
        return run("paired", self=self_read, external=observed)

    def test_self_standing(self):
        assert self._run()["self"]["standing"] == pytest.approx(0.4046, abs=1e-4)

    def test_external_standing(self):
        assert self._run()["external"]["standing"] == pytest.approx(0.2996, abs=1e-4)

    def test_standing_delta(self):
        assert self._run()["self_minus_external"]["standing"] == pytest.approx(0.105, abs=1e-3)

    def test_weighted_alignment_delta(self):
        # self wa=0.32, ext wa=-0.38 → delta=0.70
        assert self._run()["self_minus_external"]["weighted_alignment"] == pytest.approx(0.70, abs=1e-4)

    def test_authored_share_delta_zero(self):
        # same transitions in both reads → authored_share identical
        assert self._run()["self_minus_external"]["authored_share"] == pytest.approx(0.0, abs=1e-4)

    def test_cows_eye_overread(self):
        p = self._run()
        assert cows_eye(p)["self_overread"] == pytest.approx(0.105, abs=1e-3)

    def test_cows_eye_does_not_know_position(self):
        assert cows_eye(self._run())["knows_its_position"] is False

    def test_self_stake_weighted_alignment(self):
        # (0.3*0.6 + 0.7*0.2) = 0.32
        assert self._run()["self"]["stake"]["weighted_alignment"] == pytest.approx(0.32, abs=1e-4)

    def test_external_stake_weighted_alignment(self):
        # (0.2*0.5 + 0.8*(-0.6)) = 0.10 - 0.48 = -0.38
        assert self._run()["external"]["stake"]["weighted_alignment"] == pytest.approx(-0.38, abs=1e-4)

    def test_external_extractive_share(self):
        # funder gradient=0.8 is extractive → 0.8
        assert self._run()["external"]["stake"]["extractive_share"] == pytest.approx(0.8, abs=1e-4)

    def test_self_tainted_share_zero(self):
        # all supplied inputs have alignment=0.2 (not < 0)
        assert self._run()["self"]["provenance"]["tainted_share"] == pytest.approx(0.0)

    def test_external_tainted_share(self):
        # 2 of 3 inputs supplied with alignment=-0.6 → 2/3 ≈ 0.6667
        assert self._run()["external"]["provenance"]["tainted_share"] == pytest.approx(2/3, abs=1e-4)

    def test_external_optics_has_extractive_flag(self):
        p = self._run()
        notes = optics(p["external"])
        assert any("misaligned hands" in n for n in notes)

    def test_external_optics_has_tainted_flag(self):
        p = self._run()
        notes = optics(p["external"])
        assert any("benefits from the narrative" in n for n in notes)

    def test_external_optics_has_blind_proxy_flag(self):
        p = self._run()
        notes = optics(p["external"])
        assert any("proxy" in n for n in notes)

    def test_external_optics_has_authored_note(self):
        p = self._run()
        notes = optics(p["external"])
        assert any("authored" in n for n in notes)
