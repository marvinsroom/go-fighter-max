"""Audit summon, super, and ultimate animations and inventory legacy groups."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/summon-super-v54"
SX, SY = 0.095218974, 0.089829218
OLD_BODY_GROUPS = {0, 10, 20, 200, 300, 400, 61000, 61010, 61011, 61012}
EXPECTED = {
    870100: ({61020}, 3), 870101: ({61020}, 3),
    870102: ({61020}, 3), 870103: ({61020}, 3),
    1500: ({61020}, 5), 2200: ({61020}, 3), 2201: ({61020}, 3),
    876290: ({61015}, 7), 876300: ({61016}, 8), 876310: ({61017}, 8),
    3000: ({61021}, 4), 3010: ({61021}, 4),
    3100: ({61021}, 4), 13100: ({61021}, 4), 23100: ({61021}, 4),
    503100: ({61021}, 4), 513100: ({61021}, 4), 523100: ({61021}, 4),
    3120: ({61021}, 10), 13120: ({61021}, 10), 23120: ({61021}, 10),
    503120: ({61021}, 10), 513120: ({61021}, 10), 523120: ({61021}, 10),
    3200: ({61016}, 7), 3210: ({61016}, 11), 3220: ({61016}, 2),
}


def parse_air() -> dict[int, list[tuple[int, int, float, float]]]:
    result = defaultdict(list); current = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); continue
        fields = raw.split(";", 1)[0].split(",")
        if current is None or len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        result[current].append((group, frame, sx, sy))
    return dict(result)


def main() -> None:
    parsed = parse_air(); sff = Sff(LIVE / "spr.sff"); failures = []
    checked = {}
    for number, (expected_groups, minimum_elements) in EXPECTED.items():
        rows = parsed.get(number, []); groups = {row[0] for row in rows}
        checked[str(number)] = {"groups": sorted(groups), "elements": len(rows)}
        if groups != expected_groups:
            failures.append(f"action {number} groups {sorted(groups)} != {sorted(expected_groups)}")
        if len(rows) < minimum_elements:
            failures.append(f"action {number} has {len(rows)} elements; needs {minimum_elements}")
        if groups & OLD_BODY_GROUPS:
            failures.append(f"action {number} still uses legacy body groups {sorted(groups & OLD_BODY_GROUPS)}")

    frame_report = []
    for group in (61020, 61021):
        for frame in range(6):
            key = (group, frame)
            if key not in sff.keys:
                failures.append(f"missing {key}"); continue
            image = sff.decode(sff.keys[key]).convert("RGBA"); box = image.getchannel("A").getbbox()
            if not box:
                failures.append(f"empty {key}"); continue
            margins = [box[0], box[1], image.width-box[2], image.height-box[3]]
            if min(margins) < 8:
                failures.append(f"clipped {key}: {margins}")
            frame_report.append({"key": list(key), "size": list(image.size), "bbox": list(box), "margins": margins})

    legacy = {}
    for number, rows in parsed.items():
        groups = sorted({group for group, _, _, _ in rows if group in OLD_BODY_GROUPS})
        if groups:
            legacy[str(number)] = groups
    target_ids = {str(number) for number in EXPECTED}
    target_leaks = {number: groups for number, groups in legacy.items() if number in target_ids}
    if target_leaks:
        failures.append(f"target summon/super/ultimate legacy leaks: {target_leaks}")

    state_ids = set()
    for name in ("cns.cns", "Mode.cns", "our-shadows.cns", "config.cns", "-2.cns", "base.cns"):
        source = (LIVE / name).read_text(encoding="latin1")
        state_ids.update(int(value) for value in re.findall(r"(?im)^\s*\[statedef\s+(-?\d+)\]", source))
    state_bound_legacy = {number: groups for number, groups in legacy.items() if int(number) in state_ids}

    report = {
        "status": "PASS" if not failures else "FAIL",
        "checked_actions": checked,
        "new_frames": frame_report,
        "target_legacy_leaks": target_leaks,
        "remaining_legacy_group_action_count": len(legacy),
        "remaining_legacy_group_actions": legacy,
        "state_number_matched_legacy_action_count": len(state_bound_legacy),
        "state_number_matched_legacy_actions": state_bound_legacy,
        "note": "Remaining list includes inactive imports, helpers, effects, shadow forms, utilities, and non-target moves; it is retained for the next cleanup pass.",
        "failures": failures,
    }
    (ART / "audit.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "failures": failures,
                      "target_legacy_leaks": target_leaks,
                      "remaining_legacy_group_action_count": len(legacy),
                      "report": str(ART / "audit.json")}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
