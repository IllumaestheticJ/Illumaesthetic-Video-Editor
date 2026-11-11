"""Kit state of an Epsilon showroom car: which GLB nodes to hide so the car wears its kit.

Reads Epsilon-Site `showroom/models/manifest.json` + `manifest-lookbook.json` (one entry per car:
`glb`, `parts`, `replaces`, `requires`) and the GLB's own node list. Mirrors the showroom's rules
(`showroom/src/showroom-catalog.js`): a fitted part hides the stock nodes it `replaces`; parts in
the same slot group (two wings, lip vs splitter) are alternatives, only one is fitted.
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

SITE = Path("/home/user/Epsilon-Site")
# showroom-catalog.js SLOT_GROUP (+ variants of one product that share a spot)
SLOT_GROUP = {"front_lip": "front_lower", "splitter": "front_lower", "gt_wing": "rear_upper", "tc_wing_kit": "rear_upper", "rear_wing": "rear_upper",
              "wrc_wing": "rear_upper", "sport_wing": "rear_upper", "sport_wing_duckbill": "rear_upper", "mid_wing": "rear_upper"}


def glb_nodes(path) -> list[str]:
    with open(path, "rb") as f:
        f.read(12)
        n, _ = struct.unpack("<I4s", f.read(8))
        return [x.get("name", "") for x in json.loads(f.read(n))["nodes"]]


def manifest(site=SITE) -> dict:
    m = {}
    for name in ("manifest-lookbook.json", "manifest.json"):  # manifest.json wins on a clash
        p = Path(site) / "showroom/models" / name
        if p.exists():
            m.update(json.loads(p.read_text()))
    return m


def kit(car_id: str, without=(), prefer=(), site=SITE, glb=None) -> dict:
    """-> {glb, fitted[], hide[], notes[]}. `without`: part names to leave off ("fender_flares").
    `prefer`: which part wins a shared slot ("wrc_wing"); default = first in the GLB.
    `glb`: use this file instead of the repo's (e.g. a newer export from the "Epsilon-final-GLBs" zip on
    Drive). Newer exports name the stock pieces a part replaces `body_<part>_stock` / `trim_<part>_stock`,
    so the hide list also comes from the node names and the car need not be in the repo manifests."""
    m = manifest(site)
    if car_id not in m and not glb:
        raise SystemExit(f"{car_id}: no showroom model. Cars with one: {', '.join(sorted(m))}")
    e = m.get(car_id, {})
    glb = Path(glb) if glb else Path(site) / "showroom/models" / e["glb"]
    nodes = glb_nodes(glb)
    parts = [n[5:] for n in nodes if n.startswith("part_")]
    notes, fitted, taken = [], [], {}
    for p in sorted(parts, key=lambda p: (p not in prefer, parts.index(p))):
        if p in without:
            continue
        g = SLOT_GROUP.get(p)
        if g and g in taken:
            notes.append(f"{p} left off: shares the {g} slot with {taken[g]} (use --prefer {p} to swap)")
            continue
        if g:
            taken[g] = p
        fitted.append(p)
    hide = [f"part_{p}" for p in parts if p not in fitted]
    for p in fitted:
        for n in e.get("replaces", {}).get(p, []) + [f"body_{p}_stock", f"trim_{p}_stock"]:
            if n in nodes and n not in hide:
                hide.append(n)
    for child, needs in (e.get("requires") or {}).items():
        if any(n not in fitted for n in needs) and child in nodes:
            hide.append(child)
            notes.append(f"{child} hidden: needs {needs}")
    other = [n for n in nodes if n.endswith("_stock") and n not in hide and not any(n in (f"body_{p}_stock", f"trim_{p}_stock") for p in parts)]
    if other:
        notes.append(f"stock nodes with no matching part, left visible: {other} - look at a render")
    return {"car": car_id, "glb": str(glb), "fitted": sorted(fitted), "hide": hide, "notes": notes,
            "lengthM": e.get("lengthM"), "widthM": e.get("widthM"), "showcasePaint": (e.get("showcasePaint") or {}).get("hex")}
