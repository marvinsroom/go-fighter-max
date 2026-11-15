"""Verify the v58 crouch, double jump, shadows, Tank guard, and Tusk route."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/shadow-defense-v58/audit.json"


def action_groups(text: str, number: int) -> list[tuple[int, int]]:
    match = re.search(rf"(?ims)^\[Begin Action\s+{number}\].*?(?=^\[Begin Action\s+-?\d+\]|\Z)", text)
    if not match:
        return []
    return [(int(a), int(b)) for a, b in re.findall(r"(?m)^\s*(-?\d+)\s*,\s*(-?\d+)\s*,", match.group(0))]


def main() -> None:
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    base = (LIVE / "base.cns").read_text(encoding="latin1")
    negative = (LIVE / "-2.cns").read_text(encoding="latin1")
    cmd = (LIVE / "cmd.cmd").read_text(encoding="latin1")
    sff = Sff(LIVE / "spr.sff")
    failures = []
    expected = {10: [0, 1], 11: [1], 12: [1, 2]}
    for action, frames in expected.items():
        rows = action_groups(air, action)
        if rows != [(61024, frame) for frame in frames]:
            failures.append(f"crouch action {action} escaped v58: {rows}")
    missing = [key for key in [(61024, n) for n in range(3)] if key not in sff.keys]
    if missing:
        failures.append(f"missing crouch sprites {missing}")
    state45 = re.search(r"(?ims)^\[Statedef 45\].*?(?=^\[Statedef 50\])", base)
    jump_ok = bool(state45 and "V58 human double-jump rise" in state45.group(0) and "V58 remember air-jump direction" in state45.group(0) and "value = 41" in state45.group(0))
    if not jump_ok:
        failures.append("double jump does not preserve direction through the v57 rising bank")
    tank_guard = all(token in negative for token in ("V58 Tank guard body", "anim = 2130", "stateno = [120,155]", "V58 dismiss Tank after guard"))
    if not tank_guard:
        failures.append("Tank is not bound to the complete guard-state range")
    rejected_effects = [effect for effect in ("V58 walking shadow wisps", "V58 jump shadow burst", "V58 crouch shadow pool") if effect in negative]
    if rejected_effects:
        failures.append(f"rejected movement overlays remain: {rejected_effects}")
    tusk_route = bool(re.search(r'(?ims)\[State -1, V58 Tusk replaces Tank summon\].*?command="holddown".*?value=1500', cmd))
    if not tusk_route:
        failures.append("down+summon does not route to Tusk")
    report = {"status": "PASS" if not failures else "FAIL", "double_jump": jump_ok,
              "tank_guard": tank_guard, "tusk_route": tusk_route, "missing_sprites": [list(k) for k in missing], "failures": failures}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
