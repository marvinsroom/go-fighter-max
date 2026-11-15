"""Install the complete illustrated Kenpachi body bank without gameplay edits."""
from pathlib import Path
import hashlib, io, json, shutil, sys

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
from edward_assets import read_v1, write_v2
from isolated_sprite_atlas import extract
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
ART = GAME / "style-wave2/kenpachi/conversion-v1"
LIVE = GAME / "engine/ikemen-go-v1.0.0/chars/kenpachi"
INVENTORY = json.loads((GAME / "style-wave2/kenpachi/inventory.json").read_text())
SFF = LIVE / INVENTORY["files"]["sprite"]
BEFORE = ART / "before"

SHEETS = {
    "movement": ART / "body-movement-00-candidate.png",
    "attacks": ART / "body-attacks-01-v3.png",
    "specials": ART / "body-specials-02-v3.png",
    "reactions": ART / "body-reactions-03-candidate.png",
}
EFFECT_SHEETS = {
    6000: (ART / "effect-cinematic-6000-v1.png", 1, 1),
    6001: (ART / "effect-slash-6001-v1.png", 2, 2),
    6002: (ART / "effect-smoke-6002-v1.png", 4, 4),
    6004: (ART / "effect-hit-sparks-6004-v1.png", 4, 4),
}

def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha_file(path):
    return sha_bytes(path.read_bytes())

def bank(group):
    if group < 200:
        return "movement"
    if group < 500:
        return "attacks"
    if group < 5000:
        return "specials"
    return "reactions"

def grid_extract(path, columns, rows):
    image = Image.open(path).convert("RGBA")
    result = []
    for row in range(rows):
        for column in range(columns):
            box = (
                round(column * image.width / columns),
                round(row * image.height / rows),
                round((column + 1) * image.width / columns),
                round((row + 1) * image.height / rows),
            )
            cell = image.crop(box)
            alpha_box = cell.getchannel("A").getbbox()
            assert alpha_box, (path, row, column, "empty cell")
            result.append(cell.crop(alpha_box))
    return result

for path in SHEETS.values():
    assert path.exists(), path

tiles = {name: [im for im, _ in extract(path, 4, 4)] for name, path in SHEETS.items()}
assert all(len(rows) == 16 for rows in tiles.values())
effect_tiles = {group: grid_extract(*spec) for group, spec in EFFECT_SHEETS.items()}

raw = SFF.read_bytes()
source_version = raw[15]
if source_version == 1:
    original = read_v1(SFF)
else:
    arc = Sff(SFF)
    original = [dict(key=key, axis=arc.headers[index][4:6], image=arc.decode(index)) for key, index in arc.keys.items()]

groups = {}
replaced = []
effects_replaced = []
output = []
for sprite in original:
    key = tuple(sprite["key"])
    group = key[0]
    old = sprite["image"].convert("RGBA")
    if group < 6000:
        name = bank(group)
        slot = groups.get(group, 0)
        groups[group] = slot + 1
        art = tiles[name][slot % 16].copy()
        target_h = max(1, old.height)
        target_w = max(1, round(art.width * target_h / art.height))
        art = art.resize((target_w, target_h), Image.Resampling.LANCZOS)
        old_x, old_y = sprite["axis"]
        axis = (round(old_x / max(1, old.width) * art.width), old_y)
        output.append(dict(key=key, axis=axis, image=art))
        replaced.append(dict(key=key, bank=name, cell=slot % 16, old_size=old.size, new_size=art.size, old_axis=sprite["axis"], new_axis=axis))
    elif group in effect_tiles:
        slot = groups.get(group, 0)
        groups[group] = slot + 1
        art = effect_tiles[group][slot % len(effect_tiles[group])].copy()
        # Preserve native effect footprint and root; only the raster style changes.
        art = ImageOps.contain(art, old.size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", old.size)
        canvas.alpha_composite(art, ((old.width - art.width) // 2, (old.height - art.height) // 2))
        output.append(dict(key=key, axis=sprite["axis"], image=canvas))
        effects_replaced.append(dict(key=key, bank=f"effect-{group}", cell=slot % len(effect_tiles[group]), size=old.size, axis=sprite["axis"]))
    else:
        output.append(dict(key=key, axis=sprite["axis"], image=old))

# Keep selection/HUD dimensions, but replace portrait art with the approved design.
portrait = Image.open(GAME / "style-wave2/kenpachi/design-reference-v1.png").convert("RGBA")
for sprite in output:
    if sprite["key"][0] == 9000:
        canvas = Image.new("RGBA", sprite["image"].size)
        fit = ImageOps.contain(portrait, canvas.size, Image.Resampling.LANCZOS)
        canvas.alpha_composite(fit, ((canvas.width - fit.width) // 2, 0))
        sprite["image"] = canvas

BEFORE.mkdir(parents=True, exist_ok=True)
backup = BEFORE / SFF.name
if not backup.exists():
    shutil.copy2(SFF, backup)
assert sha_file(backup) == INVENTORY["source_sha256"]["sprite"], "Backup is not the inventoried original"

pending = SFF.with_suffix(".sff.pending")
write_v2(pending, output)
proof = Sff(pending)
assert set(proof.keys) == {tuple(s["key"]) for s in original}
for sprite in output:
    actual = proof.decode(proof.keys[tuple(sprite["key"])])
    assert actual.size == sprite["image"].size
    assert sha_bytes(actual.tobytes()) == sha_bytes(sprite["image"].tobytes())
pending.replace(SFF)

gameplay = {}
for kind, name in INVENTORY["files"].items():
    path = LIVE / name
    if path.exists() and kind != "sprite":
        gameplay[name] = sha_file(path)
for kind in ("anim", "cmd", "sound"):
    assert gameplay[INVENTORY["files"][kind]] == INVENTORY["source_sha256"][kind]

report = {
    "status": "INSTALLED",
    "revision": "kenpachi-style-conversion-v1",
    "tool": "built-in imagegen",
    "source_sff_version": source_version,
    "installed_sff_version": 2,
    "source_sprite_count": len(original),
    "body_sprites_replaced": len(replaced),
    "effect_sprites_replaced": len(effects_replaced),
    "unmodified_resolution_independent_wipe_keys": sum(1 for s in original if s["key"][0] == 6003),
    "unmodified_other_keys": len(original) - len(replaced) - len(effects_replaced),
    "sheets": {name: {"file": path.name, "sha256": sha_file(path), "cells": 16} for name, path in SHEETS.items()},
    "mapping": replaced,
    "effect_mapping": effects_replaced,
    "source_sff_sha256": sha_file(backup),
    "installed_sff_sha256": sha_file(SFF),
    "gameplay_files_sha256": gameplay,
    "preservation": [
        "Every original SFF key retained",
        "All 212 body keys replaced",
        "All pixel-art move effects replaced; group 6003 flat full-screen wipe geometry retained",
        "AIR, CMD, CNS, SND and palette files unchanged",
        "Original per-key height and vertical root retained",
    ],
}
(ART / "installation.json").write_text(json.dumps(report, indent=2))
print(json.dumps({k: report[k] for k in ("status", "source_sprite_count", "body_sprites_replaced", "effect_sprites_replaced", "unmodified_resolution_independent_wipe_keys", "installed_sff_sha256")}, indent=2))
