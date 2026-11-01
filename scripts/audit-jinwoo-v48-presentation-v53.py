"""Audit corrected jump, intro, idle, victory, and charge presentation banks."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/presentation-v53"
SX, SY = 0.095218974, 0.089829218
EXPECTED = {
    0: {61013}, 5: {61013}, 6: {61013},
    170: {61018}, 180: {61018}, 181: {61018}, 878500: {61018},
    500: {61019}, 501: {61019}, 10500: {61019}, 10501: {61019},
    20500: {61019}, 20501: {61019},
    510: {61019}, 10510: {61019}, 20510: {61019},
    600: {61015}, 610: {61015}, 620: {61015},
    630: {61015}, 640: {61015}, 650: {61015},
}


def actions() -> dict[int, list[tuple[int, int, float, float]]]:
    result: dict[int, list[tuple[int, int, float, float]]] = {}
    current = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1)); result.setdefault(current, []); continue
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
    return result


def main() -> None:
    parsed = actions()
    sff = Sff(LIVE / "spr.sff")
    failures = []
    action_report = {}
    for number, expected_groups in EXPECTED.items():
        rows = parsed.get(number, [])
        groups = {row[0] for row in rows}
        scales = {(round(row[2], 9), round(row[3], 9)) for row in rows}
        action_report[str(number)] = {"groups": sorted(groups), "scales": [list(x) for x in sorted(scales)]}
        if not rows:
            failures.append(f"missing action {number}")
        if groups != expected_groups:
            failures.append(f"action {number} groups {sorted(groups)} != {sorted(expected_groups)}")
        if scales != {(round(SX, 9), round(SY, 9))}:
            failures.append(f"action {number} scale drift {sorted(scales)}")

    frames = []
    for group, count in ((61015, 6), (61018, 6), (61019, 4)):
        for frame in range(count):
            key = (group, frame)
            if key not in sff.keys:
                failures.append(f"missing SFF frame {key}")
                continue
            image = sff.decode(sff.keys[key]).convert("RGBA")
            box = image.getchannel("A").getbbox()
            if not box:
                failures.append(f"empty SFF frame {key}")
                continue
            margins = [box[0], box[1], image.width - box[2], image.height - box[3]]
            if min(margins) < 6:
                failures.append(f"clipped SFF frame {key}: margins={margins}")
            frames.append({"key": list(key), "size": list(image.size), "bbox": list(box), "margins": margins})

    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    if not re.search(r"(?is)\[Statedef 191\].*?type=ChangeAnim.*?value=878500", cns):
        failures.append("intro state 191 does not select action 878500")
    if not re.search(r"(?is)\[Statedef 181\].*?anim=.*?180", cns):
        failures.append("victory state 181 does not select action 180")
    if len(re.findall(r"integrated into v53 charge body", cns)) != 2:
        failures.append("legacy charge overlays are not both disabled")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "actions": action_report,
        "frames": frames,
        "failures": failures,
    }
    (ART / "audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "failures": failures, "report": str(ART / "audit.json")}, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
