"""Pack Jinwoo locomotion-v11 sources at one locked character scale.

This writes project review assets only. It never edits a runtime SFF.
"""
from pathlib import Path
import hashlib
import json

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "sprite-fighter/New folder/jinwoo-reskin-v8/art"
MASTER = ART / "design-lock-v11/jinwoo-master-v11.png"
SOURCE = ART / "locomotion-v11/source"
PACKED = ART / "locomotion-v11/packed"
REPORT = ART / "locomotion-v11/build.json"
PROOF = ART / "locomotion-v11/runtime-proof.png"
EYE_PROOF = ART / "locomotion-v11/eye-proof.png"

CANVAS = (260, 220)
AXIS = (130, 210)
UPRIGHT_HEIGHT = 169
ALPHA_CUTOFF = 8

FRAMES = [
    ("idle-01.png", (61011, 48), "idle"),
    ("crouch-01.png", (61011, 54), "crouch"),
    ("walk-01-left-contact.png", (61011, 108), "walk left contact"),
    ("walk-02-right-pass.png", (61011, 109), "walk right pass"),
    ("walk-03-right-contact.png", (61011, 110), "walk right contact"),
    ("walk-04-left-pass.png", (61011, 111), "walk left pass"),
    ("run-01-left-contact.png", (61000, 52), "run left contact"),
    ("run-02-right-flight.png", (61000, 53), "run right flight"),
    ("run-03-right-contact.png", (61000, 54), "run right contact"),
    ("run-04-left-flight.png", (61000, 55), "run left flight"),
    ("air-01-takeoff.png", (61011, 56), "takeoff"),
    ("air-02-rise.png", (61011, 57), "rise"),
    ("air-03-apex-fall.png", (61011, 58), "apex fall"),
    ("air-04-land.png", (61011, 59), "land"),
]


def visible_bbox(image: Image.Image):
    alpha = image.getchannel("A")
    mask = alpha.point(lambda value: 255 if value >= ALPHA_CUTOFF else 0)
    return mask.getbbox()


def eye_centers(image: Image.Image, box):
    """Find the two iris clusters, favoring blue pixels surrounded by skin."""
    x0, y0, x1, y1 = box
    head_bottom = y0 + round((y1 - y0) * 0.24)
    blue = set()
    for y in range(y0, head_bottom):
        for x in range(x0, x1):
            r, g, b, a = image.getpixel((x, y))
            if a >= 160 and b >= 105 and b - max(r, g) >= 28:
                blue.add((x, y))
    components = []
    while blue:
        seed = blue.pop()
        stack = [seed]
        points = [seed]
        while stack:
            x, y = stack.pop()
            for nx in range(x - 1, x + 2):
                for ny in range(y - 1, y + 2):
                    point = (nx, ny)
                    if point in blue:
                        blue.remove(point)
                        stack.append(point)
                        points.append(point)
        if len(points) < 2:
            continue
        cx = round(sum(point[0] for point in points) / len(points))
        cy = round(sum(point[1] for point in points) / len(points))
        skin = 0
        for sy in range(max(y0, cy - 24), min(head_bottom, cy + 25), 4):
            for sx in range(max(x0, cx - 24), min(x1, cx + 25), 4):
                r, g, b, a = image.getpixel((sx, sy))
                if a >= 160 and r >= 125 and r > g * 1.08 and g >= b * 0.72:
                    skin += 1
        components.append({"center": (cx, cy), "pixels": len(points), "skin": skin})
    pairs = []
    for first_index, first in enumerate(components):
        for second in components[first_index + 1:]:
            dx = abs(first["center"][0] - second["center"][0])
            dy = abs(first["center"][1] - second["center"][1])
            if 18 <= dx <= 110 and dy <= 24:
                score = first["skin"] + second["skin"] + min(first["pixels"], 30) + min(second["pixels"], 30) - dy
                pairs.append((score, first["center"], second["center"]))
    if not pairs:
        raise SystemExit("could not locate two distinct v11 iris clusters")
    _, first, second = max(pairs)
    return sorted((first, second))


master = Image.open(MASTER).convert("RGBA")
master_box = visible_bbox(master)
if not master_box:
    raise SystemExit("master image is empty")
scale = UPRIGHT_HEIGHT / (master_box[3] - master_box[1])

PACKED.mkdir(parents=True, exist_ok=True)
records = []
for filename, key, motion in FRAMES:
    source_path = SOURCE / filename
    image = Image.open(source_path).convert("RGBA")
    box = visible_bbox(image)
    if not box:
        raise SystemExit(f"empty source: {filename}")
    crop = image.crop(box)
    source_eyes = eye_centers(image, box)
    size = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    resized = crop.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = AXIS[0] - size[0] // 2
    y = AXIS[1] - size[1]
    if x < 5 or x + size[0] > CANVAS[0] - 5 or y < 5:
        raise SystemExit(f"unsafe canvas fit for {filename}: {(x, y, *size)}")
    canvas.alpha_composite(resized, (x, y))
    packed_eyes = []
    for eye_x, eye_y in source_eyes:
        packed_eye = (
            x + round((eye_x - box[0]) * scale),
            y + round((eye_y - box[1]) * scale),
        )
        packed_eyes.append(packed_eye)
        canvas.putpixel(packed_eye, (138, 157, 255, 255))
    if len(set(packed_eyes)) != 2:
        raise SystemExit(f"packed eyes collapsed together for {filename}: {packed_eyes}")
    packed_path = PACKED / filename
    canvas.save(packed_path)
    packed_box = visible_bbox(canvas)
    records.append({
        "file": filename,
        "key": list(key),
        "motion": motion,
        "source_bbox": list(box),
        "packed_bbox": list(packed_box),
        "packed_visible_size": [packed_box[2] - packed_box[0], packed_box[3] - packed_box[1]],
        "source_eye_centers": [list(point) for point in source_eyes],
        "packed_eye_centers": [list(point) for point in packed_eyes],
        "sha256": hashlib.sha256(packed_path.read_bytes()).hexdigest(),
    })

cell_w, cell_h = 300, 260
proof = Image.new("RGBA", (cell_w * 4, cell_h * 4), (8, 8, 14, 255))
draw = ImageDraw.Draw(proof)
for index, record in enumerate(records):
    row, col = divmod(index, 4)
    frame = Image.open(PACKED / record["file"]).convert("RGBA")
    left = col * cell_w + (cell_w - CANVAS[0]) // 2
    top = row * cell_h + 28
    proof.alpha_composite(frame, (left, top))
    draw.text((col * cell_w + 8, row * cell_h + 7), record["motion"], fill=(255, 255, 255, 255))
    draw.line((left, top + AXIS[1], left + CANVAS[0], top + AXIS[1]), fill=(60, 90, 150, 255))
proof.save(PROOF)

eye_cell_w, eye_cell_h = 240, 150
eye_proof = Image.new("RGBA", (eye_cell_w * 4, eye_cell_h * 4), (8, 8, 14, 255))
eye_draw = ImageDraw.Draw(eye_proof)
for index, record in enumerate(records):
    row, col = divmod(index, 4)
    frame = Image.open(PACKED / record["file"]).convert("RGBA")
    eyes = record["packed_eye_centers"]
    min_x = min(point[0] for point in eyes) - 8
    max_x = max(point[0] for point in eyes) + 9
    min_y = min(point[1] for point in eyes) - 6
    max_y = max(point[1] for point in eyes) + 7
    crop = frame.crop((min_x, min_y, max_x, max_y))
    zoom = crop.resize((crop.width * 8, crop.height * 8), Image.Resampling.NEAREST)
    left = col * eye_cell_w + (eye_cell_w - zoom.width) // 2
    top = row * eye_cell_h + 25
    eye_proof.alpha_composite(zoom, (left, top))
    eye_draw.text((col * eye_cell_w + 8, row * eye_cell_h + 7), record["motion"], fill=(255, 255, 255, 255))
eye_proof.save(EYE_PROOF)

report = {
    "status": "PASS",
    "revision": "locomotion-v11",
    "installed": False,
    "canvas": list(CANVAS),
    "axis": list(AXIS),
    "upright_height_px": UPRIGHT_HEIGHT,
    "shared_scale": scale,
    "master_visible_bbox": list(master_box),
    "frames": records,
}
REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({"status": "PASS", "frames": len(records), "shared_scale": scale,
                  "proof": str(PROOF), "eye_proof": str(EYE_PROOF),
                  "installed": False}, indent=2))
