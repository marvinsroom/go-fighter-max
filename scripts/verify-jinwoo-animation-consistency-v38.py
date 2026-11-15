"""Fast regression gate for Jinwoo jump, body scale, and Igris routing."""
from __future__ import annotations

import json
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

audit_spec = importlib.util.spec_from_file_location(
    "jinwoo_animation_audit_v38", ROOT / "scripts/audit-jinwoo-animation-consistency-v38.py"
)
assert audit_spec and audit_spec.loader
audit_module = importlib.util.module_from_spec(audit_spec)
audit_spec.loader.exec_module(audit_module)
actions, metric = audit_module.actions, audit_module.metric

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/audit-v38/verification-v38.json"


def main() -> None:
    air_text = (LIVE / "anim.air").read_text(encoding="latin1")
    cns_text = (LIVE / "cns.cns").read_text(encoding="latin1")
    parsed = actions(LIVE / "anim.air")
    sff = Sff(LIVE / "spr.sff")
    failures: list[str] = []

    expected_jump = {
        40: [(300, 119), (300, 120), (300, 118)],
        41: [(300, 118), (300, 115)],
        42: [(300, 115), (300, 116)],
        43: [(300, 128), (300, 127)],
        44: [(300, 116), (300, 117)],
        47: [(300, 129), (300, 130), (300, 131), (300, 101)],
    }
    for action, expected in expected_jump.items():
        actual = [(int(f["group"]), int(f["image"])) for f in parsed.get(action, [])]
        if actual != expected:
            failures.append(f"jump action {action}: {actual!r} != {expected!r}")

    # Group 1000 is now intentionally used by the approved Tusk/Kaisel banks.
    # Legacy knight leakage is checked only in the knight actions below; group
    # 1001 remains globally forbidden.
    old_knight_refs = len(re.findall(r"(?m)^\s*1001\s*,", air_text))
    if old_knight_refs:
        failures.append(f"{old_knight_refs} old knight frame references remain")
    for action in (2210, 2211, 2215, 2216, 2220, 2221, 2225, 2226):
        groups = {int(f["group"]) for f in parsed.get(action, [])}
        if groups != {61001}:
            failures.append(f"knight action {action} uses groups {sorted(groups)}")
    state_2220 = re.search(r"(?ms)^\[Statedef 2220\].*?(?=^\[Statedef |\Z)", cns_text)
    if not state_2220 or "(2225)" in state_2220.group(0):
        failures.append("knight forward state still routes to backward animation 2225")

    representatives = {0: (300, 101), 870100: (61000, 5), 876310: (61005, 48), 500: (61011, 48)}
    heights: dict[str, float] = {}
    for action, key in representatives.items():
        frame = next((f for f in parsed.get(action, []) if (int(f["group"]), int(f["image"])) == key), None)
        value = metric(sff, frame) if frame else None
        if not value:
            failures.append(f"missing representative {action}:{key}"); continue
        heights[f"{action}:{key[0]},{key[1]}"] = float(value["world_height"])
    if heights and max(heights.values()) - min(heights.values()) > 0.1:
        failures.append(f"standing body banks differ in height: {heights}")

    duplicate_targets = {str(action): len(re.findall(rf"(?m)^\[Begin Action {action}\]$", air_text)) for action in (*expected_jump, 50, 52, 2210, 2211, 2215, 2216, 2220, 2221, 2225, 2226)}
    bad_duplicates = {key: value for key, value in duplicate_targets.items() if value != 1}
    if bad_duplicates:
        failures.append(f"target action definition counts are invalid: {bad_duplicates}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "canonical_world_height": 43.657,
        "representative_world_heights": heights,
        "old_knight_frame_references": old_knight_refs,
        "jump_actions": {str(k): v for k, v in expected_jump.items()},
        "failures": failures,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
