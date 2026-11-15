"""Jinwoo proportions / movement pass (v73), applied on top of consistency-v72.

User report (Nov 2): feet in the ground, much bigger than Naruto, slides
when walking, sprite glitches when jumping, attacks miss, clones/miniature
Jinwoo in supers.  Root causes and fixes:

* [Size] was xscale=1.39 / yscale=1.07, so every pose was ~38% wider than
  drawn and ~25-40% taller than Naruto.  Now uniform (it also cancels the
  1.06 x/y ratio baked into the AIR bank scales) and sized so his standing
  height is ~1.08x Naruto's (adult vs. teen).
* Feet: many drawings put the shoes 8-17 sprite pixels below the axis.
  Every AIR row using a body sprite is lifted by that amount.
* Sliding / jump glitches: base states compare anim%500000 with N+var(10).
  The -2 artwork remap swaps 20020 -> 500020 and the state swaps it back
  every tick, restarting the animation.  The comparisons now use anim%10000.
* Clone / miniature Jinwoo: the explods that drew extra copies of the old
  bare-hand body (879860-879862, 876311, anim 6) are disabled.

Every run restores from live-before-v73 first.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/proportions-v73"
BACKUP = ART / "live-before-v73"
FILES = ["anim.air", "cns.cns", "base.cns", "Mode.cns", "config.cns", "our-shadows.cns", "-2.cns"]

BODY_GROUPS = set(range(61013, 61025)) | {61091}
# AIR bank scales are x/y = 1.0600; cancel it so pixels stay square.
AIR_XY = 0.208072691 / 0.196294992
SIZE_Y = 0.92
SIZE_X = round(SIZE_Y / AIR_XY, 4)
CLONE_ANIMS = {879860, 879861, 879862, 876311}


def feet_lift(sff: Sff) -> dict[tuple[int, int], int]:
    """Sprite pixels the shoes reach below the axis, per body sprite."""
    out = {}
    for index, h in enumerate(sff.headers):
        key = (h[0], h[1])
        if key[0] not in BODY_GROUPS or key in out:
            continue
        a = np.array(sff.decode(index)).astype(int)
        r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
        weapon = ((b > 150) & (g > 110) & (r < 150)) | ((b > 170) & (b - g > 90) & (r > 110))
        body = (al > 100) & ~weapon
        rows = np.nonzero(body.sum(1) >= 14)[0]
        if len(rows):
            out[key] = int(rows.max()) - int(h[5])
    return out


def lift_air(air: str, lifts: dict, scales_seen: dict) -> tuple[str, int]:
    changed = 0
    lines = air.splitlines()
    for i, line in enumerate(lines):
        body, sep, comment = line.partition(";")
        f = body.split(",")
        if len(f) < 5:
            continue
        try:
            key = (int(f[0]), int(f[1]))
            oy = int(f[3])
        except ValueError:
            continue
        below = lifts.get(key, 0)
        if key[0] not in BODY_GROUPS or below <= 0:
            continue
        sy = float(f[8]) if len(f) > 8 and f[8].strip() else 1.0
        delta = int(round(below * sy))
        if delta <= 0:
            continue
        f[3] = str(oy - delta)
        lines[i] = ",".join(f) + (sep + comment if sep else "")
        changed += 1
    return "\n".join(lines) + "\n", changed


def align_hitboxes(air: str, sff: Sff) -> tuple[str, int]:
    """Stretch each explicit Clsn1 box to the weapon/fist actually drawn.

    Only grows boxes (never shrinks), only toward the front, by at most
    30 units, and only for frames drawn with the unified body banks.
    """
    extents: dict = {}

    def front(key, sx, sy):
        if key not in extents:
            i = sff.keys.get(key)
            if i is None:
                extents[key] = None
            else:
                h = sff.headers[i]
                al = np.array(sff.decode(i))[..., 3] > 90
                cols = np.nonzero(al.any(0))[0]
                extents[key] = (h, al, cols)
        e = extents[key]
        if not e or not len(e[2]):
            return None
        h, al, cols = e
        right = (cols.max() - h[4]) * sx
        # vertical span of whatever sits in the front 40% of the reach
        cut = int(h[4] + (cols.max() - h[4]) * 0.6)
        rows = np.nonzero(al[:, cut:].any(1))[0]
        if not len(rows):
            return None
        return right, (rows.min() - h[5]) * sy, (rows.max() - h[5]) * sy

    lines = air.split("\n")
    pending: list[int] = []
    changed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"\s*Clsn1\s*:", line, re.I):
            pending = []
            j = i + 1
            while j < len(lines) and re.match(r"\s*Clsn1\[", lines[j], re.I):
                pending.append(j)
                j += 1
            i = j
            continue
        if re.match(r"\s*Clsn2", line, re.I) or re.match(r"\s*\[Begin Action", line, re.I):
            if re.match(r"\s*\[Begin Action", line, re.I):
                pending = []
            i += 1
            continue
        f = [x.strip() for x in line.split(";", 1)[0].split(",")]
        if len(f) >= 5 and re.fullmatch(r"-?\d+", f[0] or "x") and re.fullmatch(r"-?\d+", f[1] or "x"):
            key = (int(f[0]), int(f[1]))
            if pending and key[0] in BODY_GROUPS:
                sx = float(f[7]) if len(f) > 7 and f[7] else 1.0
                sy = float(f[8]) if len(f) > 8 and f[8] else 1.0
                ox, oy = float(f[2] or 0), float(f[3] or 0)
                flip = len(f) > 5 and "h" in f[5].lower()
                ext = None if flip else front(key, sx, sy)
                if ext:
                    reach, top, bottom = ext[0] + ox, ext[1] + oy, ext[2] + oy
                    for j in pending:
                        m = re.match(r"(\s*Clsn1\[\d+\]\s*=\s*)(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)(.*)",
                                     lines[j], re.I)
                        if not m:
                            continue
                        x1, y1, x2, y2 = (float(m.group(k)) for k in range(2, 6))
                        lo, hi = min(x1, x2), max(x1, x2)
                        if reach - hi > 3 and hi > 0:
                            new_hi = min(reach - 1, hi + 30)
                            ylo, yhi = min(y1, y2, top), max(y1, y2, bottom)
                            lines[j] = (f"{m.group(1)}{int(round(lo))}, {int(round(ylo))}, "
                                        f"{int(round(new_hi))}, {int(round(yhi))}{m.group(6)}")
                            changed += 1
            pending = []
        i += 1
    return "\n".join(lines), changed


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    BACKUP.mkdir(exist_ok=True)
    for name in FILES:
        if not (BACKUP / name).exists():
            shutil.copy2(LIVE / name, BACKUP / name)
    for name in FILES:
        shutil.copy2(BACKUP / name, LIVE / name)
    report: dict[str, object] = {"revision": "proportions-v73", "size": [SIZE_X, SIZE_Y]}

    # Uniform size.
    cns = (LIVE / "cns.cns").read_text(encoding="latin1")
    cns, n = re.subn(r"(?m)^xscale=1\.39\nyscale=1\.07\n", f"xscale={SIZE_X}\nyscale={SIZE_Y}\n", cns)
    assert n == 1, n
    cns = cns.replace("; V48 frames are normalized in AIR. Keep the character-wide transform\n"
                      "; close to uniform so horizontal poses do not balloon across the screen.\n",
                      "; V73: uniform transform (cancels the 1.06 x/y ratio of the AIR bank\n"
                      "; scales) sized to stand ~1.08x Naruto's height.\n")
    (LIVE / "cns.cns").write_text(cns, encoding="latin1")

    # Feet on the floor.
    sff = Sff(LIVE / "spr.sff")
    lifts = feet_lift(sff)
    air = (LIVE / "anim.air").read_text(encoding="latin1")
    air, rows = lift_air(air, lifts, {})
    air, boxes = align_hitboxes(air, sff)
    report["hitboxes_extended_to_weapon"] = boxes
    (LIVE / "anim.air").write_text(air, encoding="latin1")
    report["feet_rows_lifted"] = rows
    report["feet_below_axis_px"] = {f"{k[0]},{k[1]}": v for k, v in sorted(lifts.items()) if v > 0}

    # Animation restarts: compare the base action number, not anim%500000.
    fixed = {}
    for name in ("base.cns", "Mode.cns"):
        text = (LIVE / name).read_text(encoding="latin1")
        text, a = re.subn(r"\(anim%500000\)\s*(!?=)\s*(\d+)\s*\+\s*var\(10\)",
                          lambda m: f"(anim%10000) {m.group(1)} (({m.group(2)}+var(10))%10000)", text, flags=re.I)
        text, b = re.subn(r"\(anim%500000\)\s*(!?=)\s*(\d+)\b(?!\s*\+)",
                          lambda m: f"(anim%10000) {m.group(1)} {int(m.group(2)) % 10000}", text)
        fixed[name] = a + b
        (LIVE / name).write_text(text, encoding="latin1")
    report["anim_compare_fixed"] = fixed

    # The v72 template's sword branch built 500000+(N+20000) (never exists),
    # so it always detoured through the legacy number for a tick.
    def wrap_sword(line: str) -> str:
        out, i, token = [], 0, "500000+("
        while True:
            j = line.find(token, i)
            if j < 0:
                out.append(line[i:])
                return "".join(out)
            k, depth = j + len(token), 1
            while depth:
                depth += {"(": 1, ")": -1}.get(line[k], 0)
                k += 1
            inner = line[j + len(token):k - 1]
            out.append(line[i:j] + (f"500000+(({inner})%10000)" if "%10000" not in inner else line[j:k]))
            i = k

    swords = {}
    for name in ("cns.cns", "Mode.cns", "config.cns", "base.cns"):
        text = (LIVE / name).read_text(encoding="latin1")
        lines = text.split("\n")
        count = 0
        for i, line in enumerate(lines):
            if "var(48)" in line and "500000+(" in line:
                lines[i] = wrap_sword(line)
                count += 1
        swords[name] = count
        (LIVE / name).write_text("\n".join(lines), encoding="latin1")
    report["sword_branch_fixed"] = swords

    # Test-only positioner (never reachable from commands): stands Jinwoo
    # 40 units in front of the opponent, facing him.
    shadows = (LIVE / "our-shadows.cns").read_text(encoding="latin1")
    shadows = shadows.rstrip() + """

; V73 TEST HARNESS ONLY - not reachable from any command.
[Statedef 879990]
type=S
movetype=I
physics=N
ctrl=0
velset=0,0
[State 879990, Place]
type=PosSet
trigger1=1
x=(enemynear,pos x)-30
y=0
[State 879990, Face]
type=Turn
trigger1=facing<0
[State 879990, Done]
type=ChangeState
trigger1=time>=1
value=0
ctrl=1
"""
    (LIVE / "our-shadows.cns").write_text(shadows, encoding="latin1")

    # No clone / miniature Jinwoo.
    disabled = []
    for name in ("cns.cns", "Mode.cns", "our-shadows.cns", "config.cns"):
        text = (LIVE / name).read_text(encoding="latin1")
        blocks = re.split(r"(?im)^(?=\[State)", text)
        current = None
        for i, block in enumerate(blocks):
            m = re.match(r"\[Statedef\s+(-?\d+)", block, re.I)
            if m:
                current = int(m.group(1))
                continue
            if not re.search(r"(?im)^\s*type\s*=\s*explod\s*$", block):
                continue
            anim = re.search(r"(?im)^\s*anim\s*=\s*(\d+)\s*$", block)
            if not anim:
                continue
            number = int(anim.group(1))
            if number in CLONE_ANIMS or (number == 6 and current in (700, 2270)):
                blocks[i] = re.sub(r"(?im)^(\s*type\s*=\s*explod\s*\n)",
                                   r"\1triggerall = 0 ; v73: no clone / miniature Jinwoo\n", block, count=1)
                disabled.append(f"{name}:{current}:{number}")
        (LIVE / name).write_text("".join(blocks), encoding="latin1")
    report["clone_explods_disabled"] = disabled

    report["hashes"] = {n: hashlib.sha256((LIVE / n).read_bytes()).hexdigest() for n in FILES}
    (ART / "installation.json").write_text(json.dumps(report, indent=1))
    print(json.dumps({k: v for k, v in report.items() if k not in ("hashes", "feet_below_axis_px")}, indent=1)[:2500])


if __name__ == "__main__":
    main()
