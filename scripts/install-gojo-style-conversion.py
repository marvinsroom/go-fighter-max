"""Install an illustrated body/VFX conversion while preserving gameplay."""
from pathlib import Path
import hashlib, json, shutil, sys
from PIL import Image, ImageFile, ImageOps

# Several otherwise-valid legacy SFF v1 archives contain PCX payloads whose
# declared scanline padding makes Pillow report a short final row.
ImageFile.LOAD_TRUNCATED_IMAGES = True

sys.path.insert(0, str(Path(__file__).resolve().parent))
from isolated_sprite_atlas import extract
from mugen_sff import Sff
from edward_assets import read_v1, write_v2

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "sprite-fighter"
SLUG = sys.argv[1] if len(sys.argv) > 1 else "gojo"
ART = GAME / "style-expansion" / SLUG / "conversion-v1"
LIVE = GAME / "engine/ikemen-go-v1.0.0/chars" / SLUG
SFF = next(LIVE.glob("*.sff"))
BACKUP = ART / "before" / SFF.name
BODY = ART / "body-v1.png"
FX = ART / "effects-v1.png"
SUPER = ART / "supers-v2.png"

def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()

def sha_file(path):
    return sha_bytes(path.read_bytes())

def fixed_grid(path):
    image = Image.open(path).convert("RGBA")
    cells = []
    for row in range(4):
        for col in range(4):
            cell = image.crop((round(col * image.width / 4), round(row * image.height / 4),
                               round((col + 1) * image.width / 4), round((row + 1) * image.height / 4)))
            box = cell.getchannel("A").getbbox()
            assert box, (row, col)
            cells.append(cell.crop(box))
    return cells

body = [image for image, _ in extract(BODY, 4, 4)]
effects = fixed_grid(FX)
assert len(body) == len(effects) == 16
supers = fixed_grid(SUPER) if SUPER.exists() else []
if supers:
    assert len(supers) == 16

ART.joinpath("before").mkdir(parents=True, exist_ok=True)
if not BACKUP.exists():
    shutil.copy2(SFF, BACKUP)

source_version = BACKUP.read_bytes()[15]
if source_version == 1:
    source = read_v1(BACKUP); seen = set()
    original = [sprite for sprite in source if not (tuple(sprite["key"]) in seen or seen.add(tuple(sprite["key"])))]
else:
    archive = Sff(BACKUP)
    original = [dict(key=key, axis=archive.headers[index][4:6], image=archive.decode(index))
                for key, index in archive.keys.items()]
gameplay = [path for path in LIVE.rglob("*") if path.is_file() and path.resolve() != SFF.resolve()]
gameplay_before = {str(path.relative_to(LIVE)): sha_file(path) for path in gameplay}

group_counts = {}
output = []
body_map = []
effect_map = []
super_map = []
ui = []
for sprite in original:
    key = tuple(sprite["key"])
    group = key[0]
    old = sprite["image"].convert("RGBA")
    occurrence = group_counts.get(group, 0)
    group_counts[group] = occurrence + 1
    super_cell = None
    if supers and SLUG == "zoro":
        number = key[1]
        if group == 1000 and 0 <= number <= 7:
            super_cell = number % 4
        elif group == 400 and 0 <= number <= 5:
            super_cell = 4 + number % 4
        elif group == 200 and 42 <= number <= 47:
            super_cell = 8 + (number - 42) % 4
        elif group == 1 and number in (3, 4):
            super_cell = 10 + (number - 3)
        elif group == 1100 and 0 <= number <= 6:
            super_cell = 12 + number % 4
    if super_cell is not None:
        art = supers[super_cell].copy()
        height = max(1, old.height)
        art = art.resize((max(1, round(art.width * height / art.height)), height), Image.Resampling.LANCZOS)
        axis = (round(sprite["axis"][0] / max(1, old.width) * art.width), sprite["axis"][1])
        output.append(dict(key=key, axis=axis, image=art))
        super_map.append(dict(key=key, cell=super_cell))
    elif supers and SLUG == "zoro" and group in (824, 1058, 1059):
        cell = (group + occurrence) % 16
        art = ImageOps.contain(effects[cell], old.size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", old.size)
        canvas.alpha_composite(art, ((old.width - art.width) // 2, (old.height - art.height) // 2))
        output.append(dict(key=key, axis=sprite["axis"], image=canvas))
        effect_map.append(dict(key=key, cell=cell))
    elif group < 6000:
        cell = occurrence % 16
        art = body[cell].copy()
        height = max(1, old.height)
        art = art.resize((max(1, round(art.width * height / art.height)), height), Image.Resampling.LANCZOS)
        axis = (round(sprite["axis"][0] / max(1, old.width) * art.width), sprite["axis"][1])
        output.append(dict(key=key, axis=axis, image=art))
        body_map.append(dict(key=key, cell=cell))
    elif group in (9000, 9001):
        output.append(dict(key=key, axis=sprite["axis"], image=old))
        ui.append(key)
    else:
        cell = (group + occurrence) % 16
        art = ImageOps.contain(effects[cell], old.size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", old.size)
        canvas.alpha_composite(art, ((old.width - art.width) // 2, (old.height - art.height) // 2))
        output.append(dict(key=key, axis=sprite["axis"], image=canvas))
        effect_map.append(dict(key=key, cell=cell))

pending = SFF.with_suffix(".sff.pending")
write_v2(pending, output)
proof = Sff(pending)
assert set(proof.keys) == {tuple(sprite["key"]) for sprite in original}
for sprite in output:
    decoded = proof.decode(proof.keys[tuple(sprite["key"])])
    assert decoded.size == sprite["image"].size
    assert sha_bytes(decoded.tobytes()) == sha_bytes(sprite["image"].tobytes())
pending.replace(SFF)

gameplay_after = {str(path.relative_to(LIVE)): sha_file(path) for path in gameplay}
assert gameplay_after == gameplay_before
report = {
    "status": "INSTALLED",
    "revision": f"{SLUG}-style-conversion-v1",
    "tool": "built-in imagegen",
    "source_sff_version": source_version,
    "installed_sff_version": 2,
    "source_sprite_count": len(original),
    "body_sprites_replaced": len(body_map),
    "move_effect_sprites_replaced": len(effect_map),
    "ui_keys_retained": len(ui),
    "body_sheet": {"file": BODY.name, "sha256": sha_file(BODY), "cells": 16},
    "effect_sheet": {"file": FX.name, "sha256": sha_file(FX), "cells": 16},
    "super_sheet": ({"file": SUPER.name, "sha256": sha_file(SUPER), "cells": 16} if supers else None),
    "mapping": body_map,
    "effect_mapping": effect_map,
    "super_mapping": super_map,
    "source_sff_sha256": sha_file(BACKUP),
    "installed_sff_sha256": sha_file(SFF),
    "gameplay_files_before_and_after_sha256": gameplay_after,
    "preservation": [
        "Every unique original SFF key retained",
        "All character and non-UI move/effect groups replaced",
        "Original body height, effect footprint, axes, and roots retained",
        "AIR, CMD, CNS, SND, DEF, and documentation files unchanged"
    ]
}
ART.joinpath("installation.json").write_text(json.dumps(report, indent=2))
print(json.dumps({key: report[key] for key in (
    "status", "source_sprite_count", "body_sprites_replaced",
    "move_effect_sprites_replaced", "ui_keys_retained", "installed_sff_sha256")}, indent=2))
