"""Create a lossless visual-replacement plan for the imported Kenpachi SFF."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sprite-fighter/style-wave2/kenpachi/inventory.json"
OUT = ROOT / "sprite-fighter/style-wave2/kenpachi/conversion-v1"
ATLAS_CAPACITY = 16

inventory = json.loads(SOURCE.read_text())
sprites = inventory["sprites"]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def layer(row):
    group = row["key"][0]
    if group < 6000:
        return "body"
    if group < 9000:
        return "effect"
    return "portrait-ui"

layers = {name: [] for name in ("body", "effect", "portrait-ui")}
for sprite in sprites:
    layers[layer(sprite)].append({
        "key": sprite["key"],
        "axis": sprite["axis"],
        "size": sprite["size"],
        "source_index": len(sum(layers.values(), [])),
    })

batches = []
for name, rows in layers.items():
    for start in range(0, len(rows), ATLAS_CAPACITY):
        chunk = rows[start:start + ATLAS_CAPACITY]
        batches.append({
            "id": f"{name}-{start // ATLAS_CAPACITY:02d}",
            "layer": name,
            "status": "pending",
            "cells": chunk,
        })

actions = {
    str(row["action"]): [frame["key"] for frame in row["frames"]]
    for row in inventory["actions"]
}
referenced = {tuple(key) for frames in actions.values() for key in frames}
available = {tuple(row["key"]) for row in sprites}
missing_source_keys = sorted(referenced - available)
assert sum(len(rows) for rows in layers.values()) == len(sprites)

candidate = OUT / "body-movement-00-candidate.png"
attack_candidate = OUT / "body-attacks-01-candidate.png"
plan = {
    "status": "Prepared; generation and visual review pending; runtime unchanged",
    "revision": "kenpachi-style-conversion-v1",
    "source": "Original imported MUGEN release",
    "source_sprite_count": len(sprites),
    "source_action_count": len(inventory["actions"]),
    "source_animation_rows": sum(len(row["frames"]) for row in inventory["actions"]),
    "classification": {name: len(rows) for name, rows in layers.items()},
    "inherited_missing_air_keys": missing_source_keys,
    "batches": batches,
    "actions": actions,
    "preservation_contract": [
        "AIR action numbers, row order, duration, offsets, flips, blend flags and collisions",
        "CNS/CMD/DEF state logic, commands, damage, meter and AI",
        "SND and palette resources",
        "original axes adjusted only in proportion to approved replacement bounds",
        "every original SFF key retained; body, effects and portraits audited separately",
    ],
    "design_reference": "../design-reference-v1.png",
    "candidate": {
        "file": candidate.name,
        "sha256": digest(candidate),
        "status": "Candidate only; not mapped or installed",
    },
    "generated_assets": [
        {
            "file": candidate.name,
            "sha256": digest(candidate),
            "kind": "movement",
            "status": "candidate-review-passed-alpha-layout; mapping pending",
        },
        {
            "file": attack_candidate.name,
            "sha256": digest(attack_candidate),
            "kind": "basic-attacks",
            "status": "candidate-review-passed-alpha-layout; mapping pending",
            "cell_order": [
                "light-windup", "light-contact", "light-follow-through", "light-recovery",
                "heavy-windup", "heavy-contact", "heavy-follow-through", "heavy-recovery",
                "low-windup", "low-contact", "low-follow-through", "low-recovery",
                "rising-strike", "forward-thrust", "standing-block", "hit-stun",
            ],
        },
    ],
    "runtime_modified": False,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "conversion-plan.json").write_text(json.dumps(plan, indent=2))
print("KENPACHI_CONVERSION_PLAN", plan["classification"], len(batches), "atlases")
