"""Static gate for Jinwoo's Xbox/XInput controller layout and bridge shortcuts."""
from __future__ import annotations

import configparser
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0"
CONFIG = ENGINE / "save/config.ini"
CMD = ENGINE / "chars/jinwoo/cmd.cmd"
BRIDGE = ROOT / "scripts/jinwoo-dpad-bridge.ps1"
REPORT = ROOT / "sprite-fighter/characters/jinwoo-mugen/controller-map-v39.json"

EXPECTED = {
    "Joystick": "0", "up": "LS_Y-", "down": "LS_Y+", "left": "LS_X-", "right": "LS_X+",
    "a": "A", "b": "B", "c": "RT", "x": "X", "y": "Y", "z": "RB",
    "start": "START", "d": "LB", "w": "LT", "menu": "BACK", "RumbleOn": "1",
}


def main() -> None:
    failures: list[str] = []
    parser = configparser.ConfigParser(interpolation=None, strict=False)
    parser.optionxform = str
    parser.read(CONFIG, encoding="utf-8")
    actual = dict(parser["Joystick_P1"])
    for key, expected in EXPECTED.items():
        if actual.get(key) != expected:
            failures.append(f"Joystick_P1 {key}={actual.get(key)!r}, expected {expected!r}")

    cmd = CMD.read_text(encoding="latin1")
    bridge = BRIDGE.read_text(encoding="utf-8")
    expected_commands = {
        "pad_monarch": "w+y", "pad_spoiler": "w+z", "pad_skill_11": "d+w", "pad_skill_12": "d+y",
    }
    for name, command in expected_commands.items():
        pattern = rf'(?is)\[Command\]\s*name\s*=\s*"{re.escape(name)}"\s*command\s*=\s*{re.escape(command)}'
        if not re.search(pattern, cmd):
            failures.append(f"missing command {name}={command}")
        if f'command="{name}"' not in cmd:
            failures.append(f"missing State -1 route for {name}")

    bridge_expectations = {
        "D-pad Igris": "Send-Chord 0x10 ([byte]$key)",
        "right-stick left": "Send-Chord 0x12 0x14",
        "right-stick right": "Send-Chord 0x12 0x15",
        "R3": "Send-Chord 0x10 0x12",
        "L3": "Send-Chord 0x10 0x14",
    }
    for label, text in bridge_expectations.items():
        if text not in bridge:
            failures.append(f"bridge is missing {label}: {text}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "device_profile": "Xbox/XInput",
        "joystick_p1": {key: actual.get(key) for key in EXPECTED},
        "shortcut_commands": expected_commands,
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
