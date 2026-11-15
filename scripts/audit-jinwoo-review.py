"""Create visual contact sheets and metadata diagnostics for Jinwoo's review."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / "sprite-fighter/characters/jinwoo"
manifest = json.loads((CHAR / "validation/controller-review.json").read_text(encoding="utf-8"))
metadata = {}
for source in manifest["sources"]:
    report_path = CHAR / "validation" / f"{source}.json"
    if not report_path.exists():
        continue
    report = json.loads(report_path.read_text(encoding="utf-8"))
    for frame in report.get("frames", []):
        rel = f'replays/{source}/Jinwoo_hybrid{frame["index"] - 1:03d}.png'
        metadata[rel] = frame

rows = []
for recording in manifest["recordings"]:
    frames = recording["frames"]
    meta = [metadata.get(path, {}) for path in frames]
    states = sorted({int(item["state"]) for item in meta if "state" in item})
    groups = sorted({int(item["group"]) for item in meta if "group" in item})
    scales = [float(item["body_scale_x"]) for item in meta if "body_scale_x" in item]
    target_life = [int(item["target_life"]) for item in meta if "target_life" in item]
    rows.append({
        "name": recording["name"],
        "passed": recording["passed"],
        "frames": len(frames),
        "states": states,
        "groups": groups,
        "scale_min": min(scales) if scales else None,
        "scale_max": max(scales) if scales else None,
        "target_damage": (max(target_life) - min(target_life)) if target_life else 0,
        "idle_only": bool(states) and set(states) <= {0},
        "source": frames[0].split("/")[1] if frames else "",
    })

out_dir = CHAR / "audit"
out_dir.mkdir(exist_ok=True)
(out_dir / "review-audit.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

tile_w, tile_h, label_h = 480, 90, 34
per_sheet = 24
for sheet_index, start in enumerate(range(0, len(manifest["recordings"]), per_sheet), 1):
    batch = manifest["recordings"][start:start + per_sheet]
    sheet = Image.new("RGB", (tile_w, len(batch) * (tile_h + label_h)), "#080d18")
    draw = ImageDraw.Draw(sheet)
    for row_index, recording in enumerate(batch):
        y = row_index * (tile_h + label_h)
        frames = recording["frames"]
        picks = sorted({0, len(frames) // 2, len(frames) - 1})
        while len(picks) < 3:
            picks.append(picks[-1])
        for col, pick in enumerate(picks[:3]):
            image = Image.open(CHAR / frames[pick]).convert("RGB")
            image.thumbnail((160, tile_h))
            x = col * 160 + (160 - image.width) // 2
            sheet.paste(image, (x, y + (tile_h - image.height) // 2))
        mark = "PASS" if recording["passed"] else "CHECK"
        draw.text((5, y + tile_h + 3), f'{start + row_index + 1:03d} {mark}  {recording["name"]}', fill="#f2f5ff")
    sheet.save(out_dir / f"review-sheet-{sheet_index:02d}.jpg", quality=88)

print("JINWOO_AUDIT", len(rows), "sheets", (len(rows) + per_sheet - 1) // per_sheet,
      "idle_only", sum(row["idle_only"] for row in rows),
      "failed", sum(not row["passed"] for row in rows))
