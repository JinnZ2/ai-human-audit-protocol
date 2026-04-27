"""
genesis_drift.py — regime drift detection demo.

Demonstrates the ontology_layer's `drift_check` applied to a case
where a narrative was validated under one climate regime and is
silently re-applied under a shifted regime.

Concrete scenario: an agricultural narrative (here using "genesis"
generically — pre-industrial/holocene-validated agricultural
prescriptions, which appear across many traditions and texts) was
validated under the holocene climate regime. In a transitional or
post-shift regime, the same narrative is sometimes silently
re-applied. The drift_check should fire.

This is exactly the case that `CLAUDE_REQUIREMENTS.md §Requirement 2`
names as Temporal Stratification: "A 2015 soil claim doesn't auto-
apply in 2026 just because the words match." The narrative does not
need to be discarded — it needs to be flagged so the consenter can
decide whether the validating regime still holds.

Run: python -m consortium.examples.genesis_drift
"""

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from datetime import date

from consortium.ontology_layer import (
    MultiEncodingRegistry,
    Ontology,
    Primitive,
    drift_check,
    multi_query,
)


def build_registry() -> MultiEncodingRegistry:
    """Build a registry with one ontology that names its regime
    explicitly. The regime is `holocene_agricultural` — validated
    against pre-industrial climate stability. The reapply_check
    fires on regimes outside that band."""
    reg = MultiEncodingRegistry()

    pre_industrial = Ontology(
        domain="agricultural_prescription",
        validated_at=date(1850, 1, 1),
        regime={
            "climate": "holocene",
            "frost_dates": "stable",
            "growing_season_length": "predictable_baseline",
            "validation_basis": "centuries_of_observation",
        },
        # the prescription only re-applies in the regime it was
        # validated against. holocene-stable conditions: yes;
        # transitional / post-shift: no.
        reapply_check=lambda ctx: ctx.get("climate") == "holocene",
    )

    # The actual content is generic agricultural wisdom; calling it
    # "genesis" because the peer-Claude letter named the file that
    # way — many traditions encode "what grows when" prescriptions
    # whose validity depends on stable seasonal cycles.
    pre_industrial.add(Primitive(
        concept_id="planting_window_prescription",
        domain="agricultural_prescription",
        form=("plant after final frost; harvest before first frost; "
              "rotate three fields on year-cycle"),
        role="prescription",
        couplings=["frost_timing", "soil_temperature",
                   "seasonal_predictability"],
        bounds=("temperate_region", "annual_cycle", "field_scale"),
        epi="measured",
        epi_confidence=0.95,  # high in its validating regime
    ))

    reg.register_ontology(pre_industrial)
    return reg


def run(verbose: bool = True):
    reg = build_registry()

    # Two contexts: one matches the validating regime, one does not.
    holocene_ctx = {"climate": "holocene", "year": 1900}
    transitional_ctx = {"climate": "transitional", "year": 2026}

    if verbose:
        print(f"[1/2] CONTEXT: climate=holocene (within validating regime)")
    drifts_holocene = drift_check(reg, holocene_ctx)
    if verbose:
        print(f"      drifts detected: {len(drifts_holocene)}")
        if not drifts_holocene:
            print(f"      → reapply_check passes; prescription "
                  f"silently applies (correctly)")

    if verbose:
        print()
        print(f"[2/2] CONTEXT: climate=transitional "
              f"(outside validating regime)")
    drifts_post_shift = drift_check(reg, transitional_ctx)
    if verbose:
        print(f"      drifts detected: {len(drifts_post_shift)}")
        for d in drifts_post_shift:
            print(f"      → domain={d['domain']!r} "
                  f"validated_at={d['validated_at']}")
            print(f"         action={d['action']!r}")
            print(f"         regime_was={d['regime_was']}")
        print()
        print("Reading: the prescription is not wrong; it is "
              "regime-bound. The drift_check surfaces the binding "
              "so the consenter decides whether the original "
              "validating regime still holds. This is exactly the "
              "Temporal Stratification stance from "
              "CLAUDE_REQUIREMENTS.md §Requirement 2: "
              "'A 2015 soil claim doesn't auto-apply in 2026 just "
              "because the words match.'")

    full = multi_query(reg, "planting_window_prescription",
                       transitional_ctx)
    if verbose:
        print()
        print(f"[multi_query trust signal under transitional ctx]: "
              f"{full['trust_signal']}")
        print(f"[regime_drifts in synthesis]: "
              f"{len(full['regime_drifts'])}")

    return drifts_holocene, drifts_post_shift, full


if __name__ == "__main__":
    print("=" * 72)
    print("GENESIS DRIFT — regime drift detection demo")
    print("=" * 72)
    h, t, _ = run(verbose=True)
    print()
    print("=" * 72)
    print(f"Holocene context: {len(h)} drift(s) detected (expected 0)")
    print(f"Transitional context: {len(t)} drift(s) detected (expected 1)")
    print("=" * 72)
