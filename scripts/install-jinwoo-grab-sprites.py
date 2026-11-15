"""Pack the generated 3x2 Jinwoo grab atlas into the runtime SFF/AIR."""
from pathlib import Path
from PIL import Image
import hashlib, io, re, shutil
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ATLAS = CHAR / "jinwoo-grab-atlas-v2.png"
SFF = CHAR / "spr.sff"
AIR = CHAR / "anim.air"
GROUP = 61009

atlas = Image.open(ATLAS).convert("RGBA")
assert atlas.size == (1536, 1024)
tiles = []
heights = []
for row in range(2):
    for col in range(3):
        tile = atlas.crop((col * 512, row * 512, (col + 1) * 512, (row + 1) * 512))
        alpha = tile.getchannel("A")
        # Remove the unwanted low-alpha generation halo while preserving antialiasing.
        clean_alpha = alpha.point(lambda a: 0 if a < 150 else a)
        tile.putalpha(clean_alpha)
        bounds = clean_alpha.point(lambda a: 255 if a >= 200 else 0).getbbox()
        assert bounds, (row, col)
        margin = 6
        crop = (max(0, bounds[0]-margin), max(0, bounds[1]-margin),
                min(512, bounds[2]+margin), min(512, bounds[3]+margin))
        tile = tile.crop(crop)
        solid = tile.getchannel("A").point(lambda a: 255 if a >= 200 else 0)
        b = solid.getbbox(); assert b
        heights.append(b[3]-b[1])
        tiles.append((tile, b))

# One scale for all frames prevents animation pulsing.
scale = 63.0 / sorted(heights)[len(heights)//2]
extras = {}
for number, (tile, bounds) in enumerate(tiles):
    # Register at the visual ground center; every frame shares one baseline.
    axis = ((bounds[0] + bounds[2]) // 2, bounds[3])
    stream = io.BytesIO(); tile.save(stream, format="PNG")
    extras[(GROUP, number)] = {
        "image": tile,
        "png": stream.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(tile.tobytes()).hexdigest(),
    }

archive = Sff(SFF)
assert not any(key in archive.keys for key in extras), "Grab sprite group already installed"
backup = SFF.with_name("spr.pre-grab-v2.sff")
if not backup.exists(): shutil.copy2(SFF, backup)
pending = SFF.with_suffix(".sff.pending")
pending.write_bytes(archive.derive({}, extras))
proof = Sff(pending)
assert all(key in proof.keys for key in extras)
pending.replace(SFF)

air = AIR.read_text(encoding="utf-8")
def replace_action(number, body):
    global air
    pattern = rf"(?ims)^\[Begin Action {number}\].*?(?=^\[Begin Action|\Z)"
    air, count = re.subn(pattern, body.rstrip()+"\n\n", air)
    assert count == 1, (number, count)

replace_action(879920, """[Begin Action 879920]
Clsn2Default: 1
 Clsn2[0] = -14,-57,15,0
61009,0,0,0,4,,,%.9f,%.9f
Clsn1: 1
 Clsn1[0] = 0,-50,44,-8
61009,1,0,0,7,,,%.9f,%.9f""" % ((scale,)*4))
replace_action(879921, """[Begin Action 879921]
Clsn2Default: 1
 Clsn2[0] = -16,-57,16,0
61009,2,0,0,6,,,%.9f,%.9f
61009,3,0,0,6,,,%.9f,%.9f
61009,4,0,0,6,,,%.9f,%.9f
61009,5,0,0,10,,,%.9f,%.9f""" % ((scale,)*8))
AIR.write_text(air, encoding="utf-8")
print(f"Installed 6 grab sprites in group {GROUP} at fixed scale {scale:.6f}")
