"""Static completeness gate for playable Tusk and Kaisel forms."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/playable-tusk-kaisel-v43/verification.json"


def actions(text: str) -> dict[int, str]:
    matches = list(re.finditer(r"(?im)^\[Begin Action\s+(-?\d+)\]\s*$", text))
    return {int(m.group(1)): text[m.start(): matches[i + 1].start() if i + 1 < len(matches) else len(text)] for i, m in enumerate(matches)}


def main() -> None:
    air_text = (LIVE / "anim.air").read_text(encoding="latin1")
    shadow_text = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    cmd = (LIVE / "cmd.cmd").read_text(encoding="latin1")
    bridge = (ROOT / "scripts/jinwoo-dpad-bridge.ps1").read_text(encoding="utf-8")
    bank = actions(air_text)
    sff = Sff(LIVE / "spr.sff")
    failures: list[str] = []
    details = {}
    base = sorted(number for number in bank if 1_000_000 <= number < 2_000_000)
    for form, name, delta, frames in ((5, "Tusk", 4_000_000, {20, 21, 22, 222}), (6, "Kaisel", 5_000_000, {27, 28, 29})):
        expected = [number + delta for number in base]
        missing_actions = [number for number in expected if number not in bank]
        state_numbers = sorted(int(n) for n in re.findall(rf"(?im)^\[Statedef\s+({88 + form}\d{{4}})\]", shadow_text))
        wrong_body_rows = []
        missing_sprite_rows = []
        distinct_rows = set()
        for number in expected:
            for match in re.finditer(r"(?m)^\s*(-?\d+)\s*,\s*(-?\d+)\s*,", bank.get(number, "")):
                key = (int(match.group(1)), int(match.group(2)))
                if key[0] < 0:
                    continue
                if key not in sff.keys:
                    missing_sprite_rows.append([number, *key])
                if key[0] == 1000:
                    distinct_rows.add(key)
                    if key[1] not in frames:
                        wrong_body_rows.append([number, *key])
                if key[0] == 61001:
                    wrong_body_rows.append([number, *key])
        if missing_actions:
            failures.append(f"{name}: {len(missing_actions)} missing actions")
        if len(state_numbers) != 16:
            failures.append(f"{name}: expected 16 states, found {len(state_numbers)}")
        if wrong_body_rows:
            failures.append(f"{name}: wrong body sprite rows")
        if missing_sprite_rows:
            failures.append(f"{name}: missing SFF sprite references")
        expected_distinct = 4 if name == "Tusk" else 3
        if len(distinct_rows) != expected_distinct:
            failures.append(f"{name}: expected {expected_distinct} approved body phases")
        details[name] = {"actions": len(expected) - len(missing_actions), "states": len(state_numbers), "body_keys": [list(k) for k in sorted(distinct_rows)], "missing_actions": missing_actions[:10], "missing_sprite_rows": missing_sprite_rows[:10], "wrong_body_rows": wrong_body_rows[:10]}

    route_checks = {
        "tusk_transform_state": bool(re.search(r"(?im)^\[Statedef 870205\]", shadow_text)),
        "kaisel_transform_state": bool(re.search(r"(?im)^\[Statedef 870206\]", shadow_text)),
        "tusk_command": 'command="pad_tf_tusk"\nvalue=870205' in cmd,
        "kaisel_command": 'command="pad_tf_kaisel"\nvalue=870206' in cmd,
        "tusk_controller": "RT + D-pad right / transform Tusk" in bridge,
        "kaisel_controller": "RT + D-pad up / transform Kaisel dragon" in bridge,
        "tusk_reveal": 879805 in bank,
        "kaisel_reveal": 879806 in bank,
    }
    failures.extend(name for name, passed in route_checks.items() if not passed)
    report = {"status": "PASS" if not failures else "FAIL", "forms": details, "routes": route_checks, "failures": failures}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
