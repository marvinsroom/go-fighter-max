"""Audit exact AIR playback order and packed v9 locomotion rasters."""
from pathlib import Path
import hashlib
import json
import re
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff

CHAR = ROOT / "sprite-fighter/characters/jinwoo-reskin-v8"
ART = CHAR / "art/locomotion-v9"
STAGE = CHAR / "runtime-staging"
INSTALL = json.loads((ART / "installation.json").read_text(encoding="utf-8"))
AIR = (STAGE / "anim.air").read_text(encoding="cp1252")
SFF = Sff(STAGE / "spr.sff")


def action_frames(number):
    match = re.search(rf"(?ims)^\s*\[Begin Action\s+{number}\]\s*$\n(.*?)(?=^\s*\[Begin Action|\Z)", AIR)
    if not match:
        raise AssertionError(f"Missing action {number}")
    frames = []
    for line in match.group(1).splitlines():
        parsed = re.match(r"^\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)", line)
        if parsed and int(parsed[1]) >= 0 and int(parsed[2]) >= 0:
            frames.append({"key": [int(parsed[1]), int(parsed[2])], "duration": int(parsed[5])})
    return frames


expected_walk = [[61011, 108], [61011, 109], [61011, 110], [61011, 111]] * 2
expected_run = [[61000, 52], [61000, 53], [61000, 54], [61000, 55]] * 2
walk = action_frames(20)
back_walk = action_frames(21)
run = action_frames(100)
failures = []
if [frame["key"] for frame in walk] != expected_walk:
    failures.append("Action 20 does not play the alternating walk cycle twice in order")
if [frame["key"] for frame in back_walk] != list(reversed(expected_walk[:4])) * 2:
    failures.append("Action 21 does not reverse the alternating walk cycle")
if [frame["key"] for frame in run] != expected_run:
    failures.append("Action 100 does not play the alternating run cycle twice in order")
if len({tuple(frame["key"]) for frame in walk}) != 4:
    failures.append("Walk does not contain four distinct runtime keys")
if len({tuple(frame["key"]) for frame in run}) != 4:
    failures.append("Run does not contain four distinct runtime keys")

raster_hashes = {}
for frame in INSTALL["frames"]:
    key = tuple(frame["key"])
    image = SFF.decode(SFF.keys[key]).convert("RGBA")
    digest = hashlib.sha256(image.tobytes()).hexdigest()
    if digest != frame["rgba_sha256"]:
        failures.append(f"Packed raster mismatch {key}")
    if image.size != tuple(INSTALL["canvas"]):
        failures.append(f"Wrong canvas {key}: {image.size}")
    if tuple(SFF.headers[SFF.keys[key]][4:6]) != tuple(INSTALL["axis"]):
        failures.append(f"Wrong axis {key}")
    raster_hashes[key] = digest
if len(set(raster_hashes.values())) != 8:
    failures.append("Walk/run contains duplicate packed drawings")

report = {
    "status": "PASS" if not failures else "FAIL",
    "walk_action": 20,
    "back_walk_action": 21,
    "run_action": 100,
    "walk_phases": INSTALL["walk_order"],
    "run_phases": INSTALL["run_order"],
    "walk_frames": walk,
    "back_walk_frames": back_walk,
    "run_frames": run,
    "distinct_packed_drawings": len(set(raster_hashes.values())),
    "manual_visual_proof": "runtime-proof.png",
    "failures": failures,
}
(ART / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
if failures:
    raise SystemExit(1)
