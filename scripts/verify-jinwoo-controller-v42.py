"""Verify dedicated controller access to Tusk and Kaisel summons."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
CMD = LIVE / "cmd.cmd"
CNS = LIVE / "cns.cns"
BRIDGE = ROOT / "scripts/jinwoo-dpad-bridge.ps1"
CONTROLS = ROOT / "sprite-fighter/characters/jinwoo-mugen/CONTROLS.md"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/controller-map-v42/verification.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cmd = CMD.read_text(encoding="latin1")
    cns = CNS.read_text(encoding="latin1")
    bridge = BRIDGE.read_text(encoding="utf-8")
    controls = CONTROLS.read_text(encoding="utf-8")
    failures: list[str] = []
    checks = {
        "kaisel_command": 'name="pad_summon_kaisel"\ncommand=w+a' in cmd,
        "tusk_command": 'name="pad_summon_tusk"\ncommand=w+b' in cmd,
        "kaisel_route": 'command="pad_summon_kaisel"\nvalue=2400' in cmd,
        "tusk_route": 'command="pad_summon_tusk"\nvalue=1500' in cmd,
        "kaisel_state_exists": bool(re.search(r"(?im)^\[statedef\s+2400\]", cns)),
        "tusk_state_exists": bool(re.search(r"(?im)^\[statedef\s+1500\]", cns)),
        "diagonal_tusk_selector": 'triggerall = command = "holdup"\ntrigger1 = command = "holdfwd"\nvalue = 1500' in cns,
        "bridge_kaisel": "Send-Chord 0x12 0x21" in bridge,
        "bridge_tusk": "Send-Chord 0x12 0x22" in bridge,
        "controls_kaisel": "LT + D-pad up" in controls,
        "controls_tusk": "LT + D-pad right" in controls,
    }
    failures.extend(name for name, passed in checks.items() if not passed)
    form_counts = {}
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    for form in range(1, 7):
        form_counts[str(form)] = len(re.findall(rf"(?im)^\[Begin Action {form}\d{{6}}\]", air))
    for form in ("5", "6"):
        if form_counts[form] != 444:
            failures.append(f"playable form {form} is incomplete: {form_counts[form]}/444 actions")
    report = {
        "status": "PASS" if not failures else "FAIL",
        "controller_routes": {"LT+D-pad up": "Kaisel summon / state 2400", "LT+D-pad right": "Tusk summon / state 1500"},
        "playable_transformations": ["Igris", "Beru", "Iron", "Tank", "Tusk", "Kaisel"],
        "independent_summons": ["Tusk", "Kaisel"],
        "form_action_counts": form_counts,
        "checks": checks,
        "runtime_sha256": {p.name: sha(p) for p in (CMD, CNS, BRIDGE, CONTROLS)},
        "failures": failures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
