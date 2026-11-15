"""Full live audit for Jinwoo identity, anatomy scale, and motion continuity."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/motion-style-v69"
TARGET = 50.4
CHAR_X, CHAR_Y = 1.39, 1.07
BASE_SCALE = (0.101895680, 0.096128000)
DAGGER_SCALE = (0.167301691, 0.157831784)
SWORD_SCALE = (0.208072691, 0.196294992)
EXPECTED_SCALE = {
    61013: BASE_SCALE, 61015: BASE_SCALE, 61016: DAGGER_SCALE,
    61017: SWORD_SCALE, 61019: BASE_SCALE, 61020: BASE_SCALE,
    61021: BASE_SCALE,
}
SPECIAL_BODY_EFFECT_ACTIONS = {876311, 879860, 879861, 879862}
FORBIDDEN_HUMAN_GROUPS = {61005, 61011}
HUMAN_GROUPS = {61000, 61013, 61015, 61016, 61017, 61018, 61019, 61020,
                61021, 61022, 61023, 61024}
JUMP_ACTIONS = (40, 41, 42, 43, 44, 45, 47, 50, 52)


def parse(text: str) -> dict[int, list[dict[str, object]]]:
    actions: dict[int, list[dict[str, object]]] = defaultdict(list)
    current = None
    for line_number, raw in enumerate(text.splitlines(), 1):
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1))
            continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        duration = int(fields[4].strip()) if len(fields) > 4 and fields[4].strip() else 1
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        actions[current].append({
            "group": group, "frame": frame, "duration": duration,
            "sx": sx, "sy": sy, "line": line_number,
        })
    return dict(actions)


def body_bbox(image: Image.Image) -> tuple[int, int, int, int] | None:
    rgba = np.asarray(image.convert("RGBA"), dtype=np.uint16)
    r, g, b, a = (rgba[:, :, index] for index in range(4))
    purple = (b > g * 1.22 + 12) & (r > g * 1.12 + 8) & (b > 55)
    cyan_weapon_energy = (b > 90) & (b > r * 1.35 + 12) & (g > r * 1.15 + 8)
    mask = (a >= 32) & ~(purple | cyan_weapon_energy)
    ys, xs = np.where(mask)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def signature(rows: list[dict[str, object]], group: int) -> tuple[int, ...]:
    return tuple(int(row["frame"]) for row in rows if int(row["group"]) == group)


def main() -> None:
    failures: list[str] = []
    actions = parse((LIVE / "anim.air").read_text(encoding="latin1"))
    sff = Sff(LIVE / "spr.sff")
    group_rows: Counter[int] = Counter()
    human_actions: set[int] = set()
    missing: list[dict[str, object]] = []
    forbidden: list[dict[str, object]] = []
    scale_drift: list[dict[str, object]] = []
    clipped: list[list[int]] = []
    used_human_keys: set[tuple[int, int]] = set()

    for action, rows in actions.items():
        for row in rows:
            group, frame = int(row["group"]), int(row["frame"])
            group_rows[group] += 1
            if group in FORBIDDEN_HUMAN_GROUPS:
                forbidden.append({"action": action, "key": [group, frame], "line": row["line"]})
            if group not in HUMAN_GROUPS:
                continue
            human_actions.add(action)
            key = (group, frame)
            used_human_keys.add(key)
            if key not in sff.keys:
                missing.append({"action": action, "key": list(key), "line": row["line"]})
                continue
            expected = EXPECTED_SCALE.get(group)
            actual = round(float(row["sx"]), 9), round(float(row["sy"]), 9)
            if expected and actual != expected:
                if not (group == 61013 and action in SPECIAL_BODY_EFFECT_ACTIONS):
                    scale_drift.append({"action": action, "key": list(key), "scale": list(actual)})

    if forbidden:
        failures.append(f"{len(forbidden)} legacy human sprite rows remain")
    if missing:
        failures.append(f"{len(missing)} referenced human sprites are missing")
    if scale_drift:
        failures.append(f"{len(scale_drift)} approved human-bank rows have scale drift")

    cache: dict[tuple[int, int], Image.Image] = {}
    for key in sorted(used_human_keys):
        if key not in sff.keys:
            continue
        image = sff.decode(sff.keys[key]).convert("RGBA")
        cache[key] = image
        box = image.getchannel("A").getbbox()
        if box and min(box[0], box[1], image.width - box[2], image.height - box[3]) < 1:
            clipped.append(list(key))
    if clipped:
        failures.append(f"{len(clipped)} active human sprites touch their packed canvas edge")

    # Shadow-step jump anatomy is calibrated independently from its purple trail.
    jump_metrics = []
    seen_jump_rows = {}
    for action in JUMP_ACTIONS:
        rows = actions.get(action, [])
        if not rows or {int(row["group"]) for row in rows} != {61023}:
            failures.append(f"bare jump action {action} escaped current shadow-step bank")
        for row in rows:
            key = (61023, int(row["frame"]))
            seen_jump_rows.setdefault(key, row)
    for key, row in sorted(seen_jump_rows.items()):
        box = body_bbox(cache[key])
        width, height = box[2] - box[0], box[3] - box[1]
        longest = max(width * float(row["sx"]) * CHAR_X, height * float(row["sy"]) * CHAR_Y)
        jump_metrics.append({"key": list(key), "body_bbox": list(box),
                             "world_longest_dimension": round(longest, 3)})
        if not TARGET - .35 <= longest <= TARGET + .35:
            failures.append(f"jump frame {key} body scale drift: {longest:.3f}")

    # Weapon jump phases must transition; only the dedicated apex may hold one pose.
    weapon_jump = {}
    for family, low, high in ((61017, 500000, 529999), (61016, 700000, 729999)):
        family_report = {}
        for action, rows in actions.items():
            base = action % 10000
            if not low <= action <= high or base not in JUMP_ACTIONS:
                continue
            frames = signature(rows, family)
            family_report[str(action)] = list(frames)
            if not frames:
                failures.append(f"weapon jump {action} lost group {family}")
            if base != 42 and len(frames) >= 2 and len(set(frames)) < 2:
                failures.append(f"weapon jump {action} still holds one stiff pose")
        weapon_jump[str(family)] = family_report

    # Light/medium/heavy signatures must be visibly distinct in every loadout.
    normal_signatures = {}
    for label, group, ids in (
        ("bare", 61013, (200, 210, 220)),
        ("dagger", 61016, (700200, 700210, 700220)),
        ("sword", 61017, (500200, 500210, 500220)),
    ):
        values = {str(action): list(signature(actions.get(action, []), group)) for action in ids}
        normal_signatures[label] = values
        if any(not value for value in values.values()) or len({tuple(value) for value in values.values()}) != 3:
            failures.append(f"{label} normals still recycle one animation: {values}")

    # Weapon changes must cross exactly one identity boundary at the handoff.
    switch_expectations = {
        876322: [61013, 61016],
        876323: [61016, 61017],
        876324: [61017, 61013],
    }
    switch_report = {}
    for action, expected in switch_expectations.items():
        rows = actions.get(action, [])
        compressed = []
        elapsed = 0
        boundaries = []
        for row in rows:
            group = int(row["group"])
            if not compressed or compressed[-1] != group:
                compressed.append(group)
                boundaries.append(elapsed)
            elapsed += int(row["duration"])
        switch_report[str(action)] = {"groups": compressed, "boundaries": boundaries, "duration": elapsed}
        if compressed != expected or boundaries != [0, 20]:
            failures.append(f"weapon switch {action} has an incoherent handoff: {switch_report[str(action)]}")

    # Runtime-sized identity references across the main combat loadouts.
    anatomy = {}
    for label, key, scale in (
        ("bare_idle", (61013, 24), BASE_SCALE),
        ("dagger_idle", (61016, 0), DAGGER_SCALE),
        # Frame 0 rests the blade above his head, so frame 1 is the clean
        # anatomical reference for the same sword bank/body scale.
        ("sword_idle", (61017, 1), SWORD_SCALE),
        ("charge", (61019, 0), BASE_SCALE),
        ("summon_call", (61020, 0), BASE_SCALE),
    ):
        box = body_bbox(cache[key])
        world_height = (box[3] - box[1]) * scale[1] * CHAR_Y
        anatomy[label] = round(world_height, 3)
    baseline = anatomy["bare_idle"]
    for label in ("dagger_idle", "charge", "summon_call"):
        if not .95 <= anatomy[label] / baseline <= 1.06:
            failures.append(f"{label} anatomy differs from bare idle: {anatomy[label] / baseline:.3f}")
    # The sword blade extends the silhouette; the non-purple body itself must remain human-sized.
    if not .93 <= anatomy["sword_idle"] / baseline <= 1.08:
        failures.append(f"sword body anatomy differs from bare idle: {anatomy['sword_idle'] / baseline:.3f}")

    # Render representative live sequences on one shared root/baseline.
    review_actions = [
        ("Bare light", 200), ("Bare medium", 210), ("Bare heavy", 220),
        ("Daggers light", 700200), ("Daggers medium", 700210), ("Daggers heavy", 700220),
        ("Sword light", 500200), ("Sword medium", 500210), ("Sword heavy", 500220),
        ("Bare jump", 41), ("Daggers jump", 700041), ("Sword jump", 500041),
        ("Bare to daggers", 876322), ("Daggers to sword", 876323), ("Sword to bare", 876324),
    ]
    cell_w, cell_h, columns = 320, 210, 6
    sheet = Image.new("RGBA", (columns * cell_w, len(review_actions) * cell_h), (15, 18, 28, 255))
    draw = ImageDraw.Draw(sheet)
    for row_index, (label, action) in enumerate(review_actions):
        rows = [row for row in actions.get(action, []) if int(row["group"]) in HUMAN_GROUPS]
        for column, row in enumerate(rows[:columns]):
            key = int(row["group"]), int(row["frame"])
            image = cache.get(key)
            if image is None:
                continue
            sx, sy = float(row["sx"]) * CHAR_X * 3, float(row["sy"]) * CHAR_Y * 3
            rendered = image.resize((max(1, round(image.width * sx)), max(1, round(image.height * sy))), Image.Resampling.LANCZOS)
            axis_x, axis_y = sff.headers[sff.keys[key]][4:6]
            root_x = column * cell_w + cell_w // 2
            root_y = row_index * cell_h + 175
            sheet.alpha_composite(rendered, (root_x - round(axis_x * sx), root_y - round(axis_y * sy)))
            draw.line((column * cell_w + 5, root_y, (column + 1) * cell_w - 5, root_y), fill=(52, 65, 94, 255))
            draw.text((column * cell_w + 7, row_index * cell_h + 7), f"{label} · A{action} · {key[0]},{key[1]}", fill="white")
    preview = ART / "full-motion-runtime-review.png"
    sheet.save(preview, optimize=True)

    report = {
        "status": "PASS" if not failures else "FAIL",
        "actions_total": len(actions),
        "sprite_rows_total": sum(len(rows) for rows in actions.values()),
        "human_actions_audited": len(human_actions),
        "unique_human_sprites_audited": len(used_human_keys),
        "human_rows_by_group": {str(group): group_rows[group] for group in sorted(HUMAN_GROUPS)},
        "forbidden_legacy_rows": forbidden[:40],
        "missing_human_rows": missing[:40],
        "scale_drift_rows": scale_drift[:40],
        "clipped_human_keys": clipped,
        "jump_metrics": jump_metrics,
        "weapon_jump_sequences": weapon_jump,
        "normal_signatures": normal_signatures,
        "weapon_switches": switch_report,
        "anatomy_world_heights": anatomy,
        "preview": str(preview.relative_to(ROOT)),
        "failures": failures,
    }
    (ART / "audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
