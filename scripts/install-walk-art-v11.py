"""Install the approved Lloyd v11 walk redraw without touching gameplay data."""
from pathlib import Path
import hashlib, io, json, shutil, statistics

from PIL import Image
from isolated_sprite_atlas import extract
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sprite-fighter/walk-fix-v11/artwork/lloyd"
CHAR = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/lloyd"
PACK = ROOT / "sprite-fighter/jus-upgrade/art/lloyd/packing.json"
SOURCE = OUT / "walk-v2.png"
BACKUP = OUT / "before"


def sha(data):
    return hashlib.sha256(data).hexdigest()


BACKUP.mkdir(exist_ok=True)
sff_path = CHAR / "lloyd.sff"
backup_sff = BACKUP / "lloyd.sff"
if not backup_sff.exists():
    shutil.copy2(sff_path, backup_sff)
for suffix in ("air", "cns", "cmd", "def", "zss", "snd"):
    path = CHAR / f"lloyd.{suffix}"
    backup = BACKUP / path.name
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)

packing = json.loads(PACK.read_text())
keys = [tuple(frame["key"]) for frame in packing["frames"]]
tiles = extract(SOURCE, 4, 2, count=8)
original = Sff(sff_path)
old_images = [original.decode(original.keys[key]) for key in keys]
factor = statistics.median(image.height for image in old_images) / statistics.median(image.height for image, _ in tiles)
replacements = {}
records = []
extracted = OUT / "extracted"
extracted.mkdir(exist_ok=True)

for index, ((image, bounds), key, old) in enumerate(zip(tiles, keys, old_images)):
    image = image.resize((round(image.width * factor), round(image.height * factor)), Image.Resampling.LANCZOS)
    header = original.headers[original.keys[key]]
    axis = (round(header[4] / old.width * image.width), image.height + header[5] - old.height)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    rgba_sha = sha(image.tobytes())
    replacements[key] = {"image": image, "png": buffer.getvalue(), "axis": axis, "rgba_sha256": rgba_sha}
    image.save(extracted / f"{index:02d}.png")
    records.append({"key": key, "axis": axis, "bounds": bounds, "size": image.size, "rgba_sha256": rgba_sha, "scale": factor})

result = original.derive(replacements, {})
pending = sff_path.with_suffix(".sff.pending")
pending.write_bytes(result)
pending.replace(sff_path)
fresh = Sff(sff_path)
for key, replacement in replacements.items():
    assert sha(fresh.decode(fresh.keys[key]).tobytes()) == replacement["rgba_sha256"]
for suffix in ("air", "cns", "cmd", "def", "zss", "snd"):
    before = BACKUP / f"lloyd.{suffix}"
    live = CHAR / f"lloyd.{suffix}"
    if before.exists():
        assert before.read_bytes() == live.read_bytes(), suffix

packing.update(
    status="Installed v11 corrected alternating gait; recordings deferred",
    source="sprite-fighter/walk-fix-v11/artwork/lloyd/walk-v2.png",
    source_sha256=sha(SOURCE.read_bytes()),
    revision="walk-fix-v11-art-v2",
    frames=records,
)
PACK.write_text(json.dumps(packing, indent=2))
report = {
    "status": "Installed; static validation passed; native validation pending",
    "tool": "built-in imagegen",
    "source": str(SOURCE.relative_to(ROOT)).replace("\\", "/"),
    "source_sha256": sha(SOURCE.read_bytes()),
    "installed_sff_sha256": sha(result),
    "uniform_scale": factor,
    "frames": records,
    "preserved": ["AIR", "CNS", "CMD", "DEF", "ZSS", "SND", "all unrelated SFF sprites"],
}
(OUT / "installation.json").write_text(json.dumps(report, indent=2))
print("LLOYD_WALK_ART_V11_INSTALLED", len(records), sha(result))
