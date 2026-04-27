"""
example_deploy_check.py

Three demonstrations of what the archaeology tree does:

1. Pre-deployment regime check
2. Extraction audit (walk back to original communities)
3. Parallel lineage discovery (find the local solution that already fits)

Run from the repo root:
    python -m knowledge_archaeology.examples.example_deploy_check
"""

import sys
import os
import json
from pathlib import Path

# allow standalone execution alongside `python -m` invocation
_repo_root = Path(__file__).resolve().parent.parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from knowledge_archaeology.knowledge_archaeology import (
    Regime,
    load_tree_from_directory,
)

NODES_DIR = os.path.join(os.path.dirname(__file__), "..", "nodes")


def section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def main():
    tree = load_tree_from_directory(NODES_DIR)
    print(f"Loaded {len(tree.nodes)} nodes from {NODES_DIR}")

    # -------------------------------------------------------------------------
    # 1. PRE-DEPLOYMENT REGIME CHECK
    #    "I'm in a Punjab-like regime. Can I use the boreal solution?"
    # -------------------------------------------------------------------------
    section("1. Pre-deployment check: boreal filter -> Punjab regime")
    target_punjab = Regime(
        geography="Punjab plain",
        climate_zone="BSh",
        avg_temp_C=24.0,
        precip_mm_per_yr=600,
        resource_scarcity=["fuel", "potable_groundwater"],
        population_density="dense",
        technology_level="preindustrial",
        institutional_context="agrarian",
    )
    result = tree.deploy_check("anishinaabe_gravity_filtration_v1", target_punjab)
    print(json.dumps(result["applicability"], indent=2))
    print()
    print("Parallel lineages already adapted to this regime:")
    print(json.dumps(result["parallel_lineages"], indent=2))

    # -------------------------------------------------------------------------
    # 2. EXTRACTION AUDIT
    #    "Where did this commercial product's knowledge actually come from?"
    # -------------------------------------------------------------------------
    section("2. Extraction audit: commercial cartridge -> attribution trail")
    trail = tree.attribution_trail("commercial_filter_cartridge_v3")
    for entry in trail:
        print(f"  - {entry['name']}")
        print(f"      communities: {entry['communities']}")
        print(f"      consent:     {entry['consent']}")
        print(f"      transmission:{entry['transmission']}")
        print()

    # -------------------------------------------------------------------------
    # 3. REGIME MISMATCH FLAGGED
    #    Try to deploy the commercial product into a post-grid sparse region.
    # -------------------------------------------------------------------------
    section("3. Regime mismatch: commercial cartridge -> post-grid sparse community")
    target_postgrid = Regime(
        geography="post-grid rural",
        climate_zone="Dfb",
        population_density="sparse",
        technology_level="preindustrial",
        institutional_context="tribal",
        resource_scarcity=["fuel", "supply_chain"],
    )
    result = tree.deploy_check("commercial_filter_cartridge_v3", target_postgrid)
    print(json.dumps(result["applicability"], indent=2))


if __name__ == "__main__":
    main()
