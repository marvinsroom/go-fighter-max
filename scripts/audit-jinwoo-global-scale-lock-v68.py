"""Audit live Jinwoo for stale anatomy scales and inconsistent body banks."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/global-scale-lock-v68"

OLD_SCALES = {
    (0.095218974, 0.089829218),
    (0.156339262, 0.147489865),
    (0.194438745, 0.183432773),
}
EXPECTED = {
    61013: (0.101895680, 0.096128000),
    61015: (0.101895680, 0.096128000),
    61016: (0.167301691, 0.157831784),
    61017: (0.208072691, 0.196294992),
    61019: (0.101895680, 0.096128000),
    61020: (0.101895680, 0.096128000),
    61021: (0.101895680, 0.096128000),
}
SPECIAL_BODY_EFFECT_ACTIONS = {876311, 879860, 879861, 879862}


def main() -> None:
    failures: list[str] = []
    current: int | None = None
    counts: Counter[int] = Counter()
    stale: list[dict[str, object]] = []
    drift: list[dict[str, object]] = []
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    for line_number, raw in enumerate(air.splitlines(), 1):
        found = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if found:
            current = int(found.group(1))
            continue
        fields = raw.split(";", 1)[0].split(",")
        if len(fields) < 2:
            continue
        try:
            group, frame = int(fields[0].strip()), int(fields[1].strip())
        except ValueError:
            continue
        if not 61013 <= group <= 61024:
            continue
        sx = float(fields[7]) if len(fields) > 7 and fields[7].strip() else 1.0
        sy = float(fields[8]) if len(fields) > 8 and fields[8].strip() else 1.0
        scale = round(sx, 9), round(sy, 9)
        counts[group] += 1
        if scale in OLD_SCALES:
            stale.append({"action": current, "line": line_number, "key": [group, frame], "scale": list(scale)})
        expected = EXPECTED.get(group)
        if expected and scale != expected:
            if not (group == 61013 and current in SPECIAL_BODY_EFFECT_ACTIONS):
                drift.append({"action": current, "line": line_number, "key": [group, frame], "scale": list(scale)})

    if stale:
        failures.append(f"{len(stale)} rows still use pre-v64 human scales")
    if drift:
        failures.append(f"{len(drift)} approved-bank rows use an inconsistent scale")

    sff = Sff(LIVE / "spr.sff")
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    char_x = float(re.search(r"(?im)^\s*xscale\s*=\s*([0-9.]+)", cns).group(1))
    char_y = float(re.search(r"(?im)^\s*yscale\s*=\s*([0-9.]+)", cns).group(1))

    def dimensions(key: tuple[int, int], scale: tuple[float, float]) -> tuple[float, float]:
        image = sff.decode(sff.keys[key]).convert("RGBA")
        box = image.getchannel("A").getbbox()
        return ((box[2] - box[0]) * scale[0] * char_x,
                (box[3] - box[1]) * scale[1] * char_y)

    idle = dimensions((61013, 24), EXPECTED[61013])
    dagger = [dimensions((61016, frame), EXPECTED[61016])[1] for frame in (0, 1, 2)]
    summon_call = [dimensions((61020, frame), EXPECTED[61020])[1] for frame in (0, 1, 2)]
    ratios = {
        "idle": 1.0,
        "dagger_standing": [value / idle[1] for value in dagger],
        "summon_call_standing": [value / idle[1] for value in summon_call],
    }
    if not 50.35 <= idle[1] <= 50.45:
        failures.append(f"idle height escaped 50.4 target: {idle[1]:.3f}")
    if any(not 0.97 <= ratio <= 1.02 for ratio in ratios["dagger_standing"]):
        failures.append(f"dagger anatomy differs from idle: {ratios['dagger_standing']}")
    if any(not 0.98 <= ratio <= 1.08 for ratio in ratios["summon_call_standing"]):
        failures.append(f"summon-call anatomy differs from idle: {ratios['summon_call_standing']}")

    report = {
        "status": "PASS" if not failures else "FAIL",
        "target_world_height": 50.4,
        "idle_world_size": [round(value, 3) for value in idle],
        "dagger_standing_heights": [round(value, 3) for value in dagger],
        "summon_call_standing_heights": [round(value, 3) for value in summon_call],
        "ratios_to_idle": {key: [round(v, 3) for v in value] if isinstance(value, list) else value
                            for key, value in ratios.items()},
        "body_rows_by_group": {str(key): value for key, value in sorted(counts.items())},
        "stale_rows": stale[:30],
        "scale_drift_rows": drift[:30],
        "failures": failures,
    }
    ART.mkdir(parents=True, exist_ok=True)
    (ART / "audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
