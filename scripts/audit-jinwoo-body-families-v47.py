"""Inventory every live human Jinwoo body family and render comparable sheets."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/body-family-audit-v47"
BODY_GROUPS = {300, 400, 61000, 61005, 61011}
CANONICAL_GROUP = 300
CANONICAL_HEIGHT = 43.657


def parse(text: str) -> dict[int, list[dict[str, object]]]:
    result: dict[int, list[dict[str, object]]] = defaultdict(list)
    action = None
    for line in text.splitlines():
        match = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", line, re.I)
        if match:
            action = int(match.group(1))
            continue
        if action is None or not re.match(r"\s*-?\d+\s*,\s*-?\d+\s*,", line):
            continue
        fields = [part.strip() for part in line.split(";")[0].split(",")]
        fields += [""] * (9 - len(fields))
        try:
            group, number = int(fields[0]), int(fields[1])
            sx, sy = float(fields[7] or 1), float(fields[8] or 1)
        except ValueError:
            continue
        if group in BODY_GROUPS:
            result[action].append({"group": group, "number": number, "sx": sx, "sy": sy})
    return result


def make_sheet(group: int, items: list[dict[str, object]], cache: dict[tuple[int, int], Image.Image]) -> None:
    tiles = []
    for item in items:
        key = (group, int(item["number"]))
        source = cache[key]
        box = source.getchannel("A").getbbox()
        if not box:
            continue
        crop = source.crop(box)
        scale = min(190 / crop.width, 185 / crop.height)
        crop = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
        tile = Image.new("RGBA", (220, 220), (21, 23, 34, 255))
        tile.alpha_composite(crop, ((220 - crop.width) // 2, 190 - crop.height))
        label = f"{group},{item['number']} H{item['min_height']:.1f}-{item['max_height']:.1f}"
        tiles.append((label, tile))
    columns = 5
    rows = max(1, (len(tiles) + columns - 1) // columns)
    canvas = Image.new("RGB", (columns * 220, rows * 220), (14, 15, 23))
    draw = ImageDraw.Draw(canvas)
    for index, (label, tile) in enumerate(tiles):
        x, y = index % columns * 220, index // columns * 220
        canvas.paste(tile.convert("RGB"), (x, y))
        draw.text((x + 4, y + 198), label, fill=(238, 240, 252))
    canvas.save(OUT / f"family-{group}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parsed = parse((LIVE / "anim.air").read_text(encoding="latin1"))
    sff = Sff(LIVE / "spr.sff")
    uses: dict[tuple[int, int], dict[str, object]] = {}
    cache: dict[tuple[int, int], Image.Image] = {}
    action_groups: dict[str, list[int]] = {}
    for action, frames in parsed.items():
        action_groups[str(action)] = sorted({int(frame["group"]) for frame in frames})
        for frame in frames:
            key = (int(frame["group"]), int(frame["number"]))
            if key not in sff.keys:
                continue
            if key not in cache:
                cache[key] = sff.decode(sff.keys[key])
            box = cache[key].getchannel("A").getbbox()
            if not box:
                continue
            height = (box[3] - box[1]) * float(frame["sy"])
            entry = uses.setdefault(key, {"group": key[0], "number": key[1], "actions": set(), "heights": []})
            entry["actions"].add(action)
            entry["heights"].append(height)

    families: dict[str, list[dict[str, object]]] = {}
    for group in sorted(BODY_GROUPS):
        items = []
        for key, entry in uses.items():
            if key[0] != group:
                continue
            heights = list(entry["heights"])
            items.append({"group": group, "number": key[1], "actions": sorted(entry["actions"]),
                          "min_height": round(min(heights), 3), "max_height": round(max(heights), 3),
                          "outside_canonical_band": min(heights) < CANONICAL_HEIGHT * .88 or max(heights) > CANONICAL_HEIGHT * 1.12})
        items.sort(key=lambda item: int(item["number"]))
        families[str(group)] = items
        make_sheet(group, items, cache)

    mixed_actions = {action: groups for action, groups in action_groups.items() if len(groups) > 1}
    noncanonical_actions = {action: groups for action, groups in action_groups.items() if any(g != CANONICAL_GROUP for g in groups)}
    report = {
        "status": "AUDITED",
        "canonical_family": CANONICAL_GROUP,
        "canonical_height": CANONICAL_HEIGHT,
        "family_sprite_counts": {group: len(items) for group, items in families.items()},
        "mixed_body_family_actions": mixed_actions,
        "noncanonical_body_family_actions": noncanonical_actions,
        "families": families,
    }
    (OUT / "body-family-audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "AUDITED",
        "family_sprite_counts": report["family_sprite_counts"],
        "mixed_action_count": len(mixed_actions),
        "noncanonical_action_count": len(noncanonical_actions),
        "report": str(OUT / "body-family-audit.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
