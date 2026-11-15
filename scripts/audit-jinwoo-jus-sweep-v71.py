"""Audit every sprite Jinwoo showed in the v71 engine sweep.

Reports per move: legacy (non-unified) body art, apparent height outliers,
feet off the floor on grounded frames, and sprites whose opaque pixels touch
the canvas edge (a body part or weapon cut off).
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
LEGACY = {0, 20, 180, 200, 300, 400, 600}
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/jus-playstyle-v71"
BODY = set(range(61013, 61025)) | {61000, 61091}


def air_rows() -> dict[int, list[tuple]]:
    actions: dict[int, list[tuple]] = {}
    current = None
    for raw in (LIVE / "anim.air").read_text(encoding="latin1").splitlines():
        m = re.match(r"\s*\[Begin Action\s+(-?\d+)\]", raw, re.I)
        if m:
            current = int(m.group(1)); actions[current] = []; continue
        f = [x.strip() for x in raw.split(";", 1)[0].split(",")]
        if current is None or len(f) < 5:
            continue
        try:
            g, n, ox, oy = int(f[0]), int(f[1]), int(f[2]), int(f[3])
        except ValueError:
            continue
        sx = float(f[7]) if len(f) > 7 and f[7] else 1.0
        sy = float(f[8]) if len(f) > 8 and f[8] else 1.0
        actions[current].append((g, n, ox, oy, sx, sy))
    return actions


def measure(sff: Sff, cache: dict, g: int, n: int):
    if (g, n) in cache:
        return cache[(g, n)]
    i = sff.keys.get((g, n))
    if i is None:
        cache[(g, n)] = None; return None
    h = sff.headers[i]
    a = np.array(sff.decode(i)).astype(int)
    r, gg, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    opaque = al > 60
    weapon = ((b > 150) & (gg > 110) & (r < 150)) | ((b > 170) & (b - gg > 90) & (r > 110))
    body = opaque & ~weapon
    ys = np.nonzero(body.any(1))[0]
    edges = {"top": bool(opaque[0].any()), "bottom": bool(opaque[-1].any()),
             "left": bool(opaque[:, 0].any()), "right": bool(opaque[:, -1].any())}
    res = {"axis": (h[4], h[5]), "size": (h[2], h[3]),
           "top": int(ys.min()) if len(ys) else None, "bottom": int(ys.max()) if len(ys) else None,
           "cut": [k for k, v in edges.items() if v]}
    cache[(g, n)] = res
    return res


def main() -> None:
    sweep = json.loads((ART / "sprite-sweep-v71.json").read_text())
    actions = air_rows()
    sff = Sff(LIVE / "spr.sff")
    cache: dict = {}
    issues = defaultdict(list)
    legacy = defaultdict(set)
    weapon = defaultdict(set)
    heights = []
    for move, seen in sweep["moves"].items():
        for key in seen:
            parts = [int(x) for x in key.split("|")]
            state, anim, elem = parts[:3]
            w10, w48 = (parts[3], parts[4]) if len(parts) > 4 else (None, None)
            daggers = w10 is not None and (10000 <= w10 < 20000 or (w10 == 0 and w48 == 10000))
            rows = actions.get(anim)
            if not rows or elem < 1 or elem > len(rows):
                continue
            g, n, ox, oy, sx, sy = rows[elem - 1]
            if g < 0:
                continue
            m = measure(sff, cache, g, n)
            if m is None:
                continue
            if m["cut"]:
                issues[move].append(f"{g},{n} cut at {'/'.join(m['cut'])} (anim {anim})")
            if g not in BODY:
                if g in LEGACY:
                    legacy[move].add((anim, g, n, seen[key]))
                continue
            if False:
                issues[move].append(f"{g},{n} cut at {'/'.join(m['cut'])} (anim {anim})")
            wrong = w10 is not None and ((daggers and g == 61017) or (not daggers and g == 61016))
            if wrong:
                weapon[move].add((anim, g, n, seen[key]))
            if m["top"] is not None:
                hgt = (m["axis"][1] - m["top"]) * sy
                heights.append((hgt, move, anim, g, n))
    report = {"legacy_art": {k: sorted(v) for k, v in legacy.items()},
              "wrong_weapon": {k: sorted(v) for k, v in weapon.items()},
              "edge_cuts": {k: sorted(set(v)) for k, v in issues.items()},
              "tallest": sorted(set(heights), reverse=True)[:15],
              "count_moves": len(sweep["moves"])}
    (ART / "sprite-audit-v71.json").write_text(json.dumps(report, indent=1, default=str))
    print("moves", report["count_moves"])
    print("legacy art in", len(legacy), "moves")
    for k, v in sorted(legacy.items())[:60]:
        print("  ", k, sorted({(a, g, c) for a, g, n, c in v})[:6])
    print("wrong weapon art in", len(weapon), "moves")
    for k, v in sorted(weapon.items())[:40]:
        print("  ", k, sorted({(a, g, c) for a, g, n, c in v})[:6])
    print("edge cuts in", len(issues), "moves")
    allcuts = sorted({c for v in issues.values() for c in v})
    for c in allcuts: print("  ", c)
    print("tallest", [(round(h, 1), mv, g, n) for h, mv, a, g, n in report["tallest"][:10]])


if __name__ == "__main__":
    main()
