"""Report rendered body heights for every Jinwoo AIR action."""
from pathlib import Path
import re
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
sff = Sff(CHAR / "spr.sff")
air = (CHAR / "anim.air").read_text(encoding="utf-8")

results = []
audited = set(range(0, 700)) | set(range(870000, 870704)) | set(range(876000, 876321)) | set(range(878400, 878512)) | set(range(890000, 930000)) | {1000, 1100, 1260, 1300, 1400, 1500, 1600, 1700, 1900, 2000, 2600, 2700, 2800, 2900, 3000, 3010, 3020}
for block in re.split(r"(?=^\[Begin Action )", air, flags=re.M | re.I):
    match = re.match(r"\[Begin Action (\d+)", block, re.I)
    if not match:
        continue
    if int(match[1]) not in audited:
        continue
    heights = []
    keys = []
    for line in block.splitlines():
        if not re.match(r"^\s*\d+\s*,\s*\d+\s*,", line):
            continue
        fields = line.split(";", 1)[0].split(",")
        fields += [""] * (9 - len(fields))
        key = tuple(int(value.strip()) for value in fields[:2])
        if key not in sff.keys:
            continue
        bounds = sff.decode(sff.keys[key]).getchannel("A").getbbox()
        if not bounds:
            continue
        scale = float(fields[8].strip() or 1)
        heights.append((bounds[3] - bounds[1]) * scale * 1.1)
        keys.append(key)
    if heights:
        results.append((int(match[1]), min(heights), max(heights), sum(heights) / len(heights), len(heights), keys))

print("action,min_height,max_height,average_height,frames,sprites")
for action, low, high, average, count, keys in results:
    print(f"{action},{low:.2f},{high:.2f},{average:.2f},{count},{sorted(set(keys))}")
