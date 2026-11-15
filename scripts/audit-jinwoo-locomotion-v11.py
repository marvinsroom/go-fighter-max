"""Hard pre-install audit for Jinwoo locomotion-v11."""
from pathlib import Path
import json

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "sprite-fighter/New folder/jinwoo-reskin-v8/art/locomotion-v11"
PACKED = ART / "packed"
BUILD = json.loads((ART / "build.json").read_text(encoding="utf-8"))
REVIEW = json.loads((ART / "review.json").read_text(encoding="utf-8"))

EXPECTED_KEYS = {
    (61011, 48), (61011, 54),
    (61011, 108), (61011, 109), (61011, 110), (61011, 111),
    (61000, 52), (61000, 53), (61000, 54), (61000, 55),
    (61011, 56), (61011, 57), (61011, 58), (61011, 59),
}
UPRIGHT_KEYS = {(61011, 48), (61011, 108), (61011, 110)}

failures = []
records = {tuple(item["key"]): item for item in BUILD.get("frames", [])}
reviews = {tuple(item["key"]): item for item in REVIEW.get("frames", [])}
requirements = REVIEW.get("shared_requirements", {})

if REVIEW.get("status") != "APPROVED_FOR_STAGING_PACK_ONLY":
    failures.append(f"visual review is not approved: {REVIEW.get('status')}")

if set(records) != EXPECTED_KEYS:
    failures.append(f"build key coverage mismatch: {len(records)} of {len(EXPECTED_KEYS)}")
if set(reviews) != EXPECTED_KEYS:
    failures.append(f"review key coverage mismatch: {len(reviews)} of {len(EXPECTED_KEYS)}")
if not requirements or not all(value is True for value in requirements.values()):
    failures.append("shared visual requirements are not all approved")
if BUILD.get("canvas") != [260, 220] or BUILD.get("axis") != [130, 210]:
    failures.append("runtime canvas or axis changed")
if BUILD.get("upright_height_px") != 169:
    failures.append("canonical upright height is not 169 pixels")
if BUILD.get("installed") is not False:
    failures.append("build incorrectly claims to be installed")

for key in sorted(EXPECTED_KEYS):
    record = records.get(key)
    review = reviews.get(key)
    if not record or not review:
        continue
    image_path = PACKED / record["file"]
    if not image_path.exists():
        failures.append(f"{key}: missing packed file {record['file']}")
        continue
    image = Image.open(image_path).convert("RGBA")
    if image.size != (260, 220):
        failures.append(f"{key}: wrong canvas {image.size}")
    box = image.getbbox()
    if not box:
        failures.append(f"{key}: empty image")
        continue
    margins = (box[0], box[1], image.width - box[2], image.height - box[3])
    if min(margins) < 5:
        failures.append(f"{key}: unsafe transparent margin {margins}")
    eyes = [tuple(point) for point in record.get("packed_eye_centers", [])]
    if len(eyes) != 2 or len(set(eyes)) != 2:
        failures.append(f"{key}: expected two distinct packed eyes, got {eyes}")
    elif abs(eyes[0][0] - eyes[1][0]) < 3:
        failures.append(f"{key}: packed eyes are not visibly separated: {eyes}")
    for point in eyes:
        if image.getpixel(point) != (138, 157, 255, 255):
            failures.append(f"{key}: eye marker missing at {point}")
    if key in UPRIGHT_KEYS:
        height = box[3] - box[1]
        if not 166 <= height <= 172:
            failures.append(f"{key}: upright height {height} outside 169 +/- 3")
        if review.get("upright_grounded") is not True:
            failures.append(f"{key}: upright frame not marked grounded")

walk_motions = {records[key]["motion"] for key in EXPECTED_KEYS if records.get(key) and records[key]["motion"].startswith("walk")}
run_motions = {records[key]["motion"] for key in EXPECTED_KEYS if records.get(key) and records[key]["motion"].startswith("run")}
if walk_motions != {"walk left contact", "walk right pass", "walk right contact", "walk left pass"}:
    failures.append("walk phases do not cover alternating left/right contact and pass")
if run_motions != {"run left contact", "run right flight", "run right contact", "run left flight"}:
    failures.append("run phases do not cover alternating left/right contact and flight")

report = {
    "status": "PASS" if not failures else "FAIL",
    "installed": False,
    "frame_count": len(records),
    "reviewed_frame_count": len(reviews),
    "eye_approved_frame_count": sum(1 for record in records.values() if len(record.get("packed_eye_centers", [])) == 2),
    "upright_height_px": BUILD.get("upright_height_px"),
    "shared_scale": BUILD.get("shared_scale"),
    "failures": failures,
}
(ART / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(0 if not failures else 1)
