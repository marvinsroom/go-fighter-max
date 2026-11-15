"""Install and prove a human alternating walk/run cycle in v8 staging only."""
from pathlib import Path
import hashlib
import io
import json
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff

CHAR = ROOT / "sprite-fighter/characters/jinwoo-reskin-v8"
ART = CHAR / "art/locomotion-v9"
REVIEWED = ART / "reviewed"
LIVE = CHAR / "runtime-staging/spr.sff"
CANVAS = (260, 220)
AXIS = (130, 210)
FRAMES = [
    ((61011, 108), "walk-01-left-contact.png", "walk", "left-contact"),
    ((61011, 109), "walk-02-right-pass.png", "walk", "right-pass"),
    ((61011, 110), "walk-03-right-contact.png", "walk", "right-contact"),
    ((61011, 111), "walk-04-left-pass.png", "walk", "left-pass"),
    ((61000, 52), "run-01-left-contact.png", "run", "left-contact"),
    ((61000, 53), "run-02-right-flight.png", "run", "right-flight"),
    ((61000, 54), "run-03-right-contact.png", "run", "right-contact"),
    ((61000, 55), "run-04-left-flight.png", "run", "left-flight"),
]


def encode(image):
    payload = io.BytesIO()
    image.save(payload, format="PNG")
    return {"image": image, "png": payload.getvalue(), "axis": AXIS,
            "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest()}


source = Sff(LIVE)
replacements = {}
report_frames = []
for key, filename, cycle, phase in FRAMES:
    image = Image.open(REVIEWED / filename).convert("RGBA")
    # Run generations contain only low-alpha presentation glow outside the
    # opaque character. Threshold it away before crop/pack.
    cutoff = 128 if cycle == "run" else 16
    alpha = image.getchannel("A").point(lambda value: 0 if value < cutoff else value)
    image.putalpha(alpha)
    bounds = alpha.getbbox()
    if bounds is None:
        raise AssertionError(f"Empty reviewed frame {filename}")
    pose = image.crop(bounds)
    target_height = 169 if cycle == "walk" else 154
    scale = min(target_height / pose.height, (CANVAS[0] - 20) / pose.width)
    pose = pose.resize((max(1, round(pose.width * scale)), max(1, round(pose.height * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS)
    canvas.alpha_composite(pose, ((CANVAS[0] - pose.width) // 2, AXIS[1] - pose.height))
    visible = canvas.getbbox()
    if visible is None or min(visible[0], visible[1], CANVAS[0] - visible[2], CANVAS[1] - visible[3]) < 5:
        raise AssertionError(f"Unsafe packed frame {filename}: {visible}")
    replacements[key] = encode(canvas)
    report_frames.append({"key": list(key), "file": filename, "cycle": cycle,
                          "phase": phase, "visible": list(visible), "axis": list(AXIS),
                          "rgba_sha256": replacements[key]["rgba_sha256"]})

pending = LIVE.with_suffix(".sff.pending")
pending.write_bytes(source.derive(replacements, {}))
proof_sff = Sff(pending)
proof = Image.new("RGBA", (4 * CANVAS[0], 2 * CANVAS[1]))
draw = ImageDraw.Draw(proof)
for index, frame in enumerate(report_frames):
    key = tuple(frame["key"])
    decoded = proof_sff.decode(proof_sff.keys[key]).convert("RGBA")
    if hashlib.sha256(decoded.tobytes()).hexdigest() != frame["rgba_sha256"]:
        raise AssertionError(f"Packed raster mismatch {key}")
    if tuple(proof_sff.headers[proof_sff.keys[key]][4:6]) != AXIS:
        raise AssertionError(f"Packed axis mismatch {key}")
    x, y = (index % 4) * CANVAS[0], (index // 4) * CANVAS[1]
    proof.alpha_composite(decoded, (x, y))
    draw.text((x + 6, y + 5), frame["phase"], fill="white")
pending.replace(LIVE)
proof.save(ART / "runtime-proof.png")

report = {
    "status": "PASS",
    "revision": "locomotion-v9",
    "target": "unregistered runtime-staging only",
    "walk_order": ["left-contact", "right-pass", "right-contact", "left-pass"],
    "run_order": ["left-contact", "right-flight", "right-contact", "left-flight"],
    "installed_keys": len(FRAMES),
    "canvas": list(CANVAS),
    "axis": list(AXIS),
    "frames": report_frames,
    "runtime_sff_sha256": hashlib.sha256(LIVE.read_bytes()).hexdigest(),
}
(ART / "installation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({key: report[key] for key in ("status", "revision", "target", "walk_order", "run_order", "installed_keys")}, indent=2))
