"""
cherokee_creation.py — multi-encoding ontology demo.

Demonstrates the multi-encoding ontology layer's coherence_check
applied to a creation narrative across four encodings (oral, dance,
written, equation). The test: do the four encodings converge on
universal couplings? If yes, the geometry is load-bearing across
encodings — what survives translation is what the narrative actually
encoded.

CULTURAL SOURCING NOTE
======================
Specific Cherokee creation narrative content is sacred and belongs
to authorized cultural holders. This example uses **placeholder
concept identifiers** (origin_emergence, first_water, sky_world,
relational_kin, etc.) that demonstrate the multi-encoding machinery
without appropriating actual narrative content.

A real implementation would:
  1. Source the actual narrative content from authorized holders
  2. Represent each encoding (oral / dance / written) faithfully
  3. Run the same multi_query() against the populated registry
  4. Treat any coherence finding with humility — it shows the
     ontology layer can read across encodings, not that the
     content has been comprehended

The structural finding this demo tests is therefore weaker than
the question it gestures at. That is honest scoping.

Run: python -m consortium.examples.cherokee_creation
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
    coherence_check,
    multi_query,
)


def build_registry() -> MultiEncodingRegistry:
    """Build a 4-encoding registry for a creation-narrative concept,
    using placeholder content. The point is the machinery, not the
    narrative."""
    reg = MultiEncodingRegistry()

    # Same concept_id appears in four encodings. The couplings list
    # is what the demo tests: do all four name the same relational
    # geometry? If yes, the coherence_check finds universal couplings.
    shared_couplings = [
        "first_water",
        "sky_world",
        "relational_kin",
        "land_and_kin_responsibility",
    ]

    # ---------- ORAL ----------
    oral = Ontology(
        domain="oral",
        validated_at=date(1850, 1, 1),
        regime={"transmission": "spoken_in_community",
                "data_source": "generational_observation"},
        # constraint logic survives regime
        reapply_check=lambda ctx: True,
    )
    oral.add(Primitive(
        concept_id="origin_emergence",
        domain="oral",
        form="<placeholder for authorized oral content>",
        role="agent_chain",
        couplings=list(shared_couplings),
        bounds=("Cherokee_homelands", "creation_horizon", "ecosystem"),
        epi="measured",
        epi_confidence=0.85,
    ))

    # ---------- DANCE ----------
    dance = Ontology(
        domain="dance",
        validated_at=date(1900, 1, 1),
        regime={"encoding": "movement", "data_source": "embodied_practice"},
        reapply_check=lambda ctx: True,
    )
    dance.add(Primitive(
        concept_id="origin_emergence",
        domain="dance",
        form="<placeholder for authorized movement sequence>",
        role="movement",
        couplings=list(shared_couplings),
        bounds=("Cherokee_homelands", "creation_horizon", "ecosystem"),
        epi="inferred",
        epi_confidence=0.70,
    ))

    # ---------- WRITTEN ----------
    written = Ontology(
        domain="written",
        validated_at=date(2000, 1, 1),
        regime={"encoding": "text", "data_source": "documentation"},
        reapply_check=lambda ctx: True,
    )
    written.add(Primitive(
        concept_id="origin_emergence",
        domain="written",
        form="<placeholder for documented written form>",
        role="claim",
        couplings=list(shared_couplings) + ["literary_context"],
        bounds=("Cherokee_homelands", "creation_horizon", "ecosystem"),
        epi="inferred",
        epi_confidence=0.75,
    ))

    # ---------- EQUATION ----------
    # Note: the equation encoding is the most lossy. It typically
    # cannot represent agency, obligation, or relational kin without
    # collapsing them into variables. The demo shows the equation
    # encoding adding a domain-specific coupling (literary frame), and
    # losing the agency/kin couplings might also be expected — but here
    # we keep them so the universal coupling set is non-empty for
    # demonstration. A real implementation should be honest about which
    # couplings the equation form drops.
    equation = Ontology(
        domain="equation",
        validated_at=date(2024, 1, 1),
        regime={"encoding": "math", "data_source": "modeling"},
        reapply_check=lambda ctx: True,
    )
    equation.add(Primitive(
        concept_id="origin_emergence",
        domain="equation",
        form="dW/dt | initial_condition_from_narrative",
        role="variable",
        couplings=list(shared_couplings),
        bounds=("Cherokee_homelands", "creation_horizon", "ecosystem"),
        epi="inferred",
        epi_confidence=0.50,
    ))

    for o in (oral, dance, written, equation):
        reg.register_ontology(o)

    return reg


def run(verbose: bool = True):
    reg = build_registry()
    ctx = {}  # no regime constraints in this demo

    coh = coherence_check(reg, "origin_emergence")
    full = multi_query(reg, "origin_emergence", ctx)

    if verbose:
        print(f"[concept]    origin_emergence (placeholder)")
        print(f"[encodings]  {coh['encodings_present']}")
        print(f"[universal]  {coh['universal_couplings']}")
        print(f"[per-domain] {coh['domain_specific_couplings']}")
        print(f"[score]      {coh['coherence_score']}")
        print(f"[load-bearing] {coh['load_bearing_check']}")
        print(f"[trust]      {full['trust_signal']}")
        print()
        print("Reading: the multi-encoding ontology layer detects "
              "universal couplings across the four placeholder encodings "
              "and reports them as load-bearing.")
        print()
        print("Honest caveat: this demo uses placeholder content. "
              "A real implementation must source narrative content "
              "from authorized cultural holders. The structural "
              "finding ('the machinery reads across encodings') "
              "is weaker than the question it gestures at "
              "('what does the actual narrative encode').")

    return coh, full


if __name__ == "__main__":
    print("=" * 72)
    print("CHEROKEE CREATION — multi-encoding ontology demo")
    print("(placeholder content; see CULTURAL SOURCING NOTE in file)")
    print("=" * 72)
    coh, full = run(verbose=True)
    print()
    print("=" * 72)
    print(f"Coherence score: {coh['coherence_score']}")
    print(f"Trust signal: {full['trust_signal']}")
    print("=" * 72)
