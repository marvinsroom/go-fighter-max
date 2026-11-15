"""Fix Naruto portraits, lock form sprite scale, install designed Kurama at summon size."""
from __future__ import annotations

import hashlib
import io
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mugen_sff import Sff

ROOT = Path(__file__).resolve().parents[1]
NAR = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto"
ART = ROOT / "sprite-fighter/characters/naruto"
BACKUP = ART / "before-portrait-kurama"
KURAMA_SRC = Path(
    r"C:\Users\15168\.cursor\projects\c-Users-15168-Development-Vs-Fighter-go-fighter-max\assets\kurama-idle.jpg"
)
CHAR_SCALE = 0.18
SUMMON_SCREEN = 102.0  # Kaisel ~90, Tusk/Igris ~103
IDLE_BODY = 226  # group 0 standing body height


def body_h(im: Image.Image) -> int:
    ys = np.where(np.array(im.convert("RGBA"))[:, :, 3] > 20)[0]
    return int(ys.max() - ys.min() + 1) if len(ys) else 1


def key_near(im: Image.Image, ref_rgb, tol: int) -> Image.Image:
    a = np.array(im.convert("RGBA"))
    rgb = a[:, :, :3].astype(np.int16)
    ref = np.array(ref_rgb, dtype=np.int16)
    dist = np.abs(rgb - ref).sum(axis=2)
    a[:, :, 3] = np.where(dist <= tol, 0, a[:, :, 3])
    # eat leftover fringe
    fg = a[:, :, 3] > 20
    fringe = fg & ndimage.binary_dilation(~fg, iterations=1) & (dist <= tol + 40)
    a[fringe, 3] = 0
    return Image.fromarray(a)


def crop_alpha(im: Image.Image, pad: int = 2) -> Image.Image:
    a = np.array(im.convert("RGBA"))
    ys, xs = np.where(a[:, :, 3] > 20)
    if len(ys) == 0:
        return im
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + 1 + pad)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + 1 + pad)
    return Image.fromarray(a[y0:y1, x0:x1])


def axis_feet(im: Image.Image) -> tuple[int, int]:
    a = np.array(im.convert("RGBA"))
    ys, xs = np.where(a[:, :, 3] > 20)
    bottom = int(ys.max())
    band = xs[ys >= bottom - max(4, im.height // 30)]
    return int(np.median(band)), bottom


def pack(im: Image.Image, axis: tuple[int, int] | None = None) -> dict:
    im = im.convert("RGBA")
    a = np.array(im)
    a[:, :, 3] = np.where(a[:, :, 3] > 16, 255, 0).astype(np.uint8)
    im = Image.fromarray(a)
    if axis is None:
        axis = axis_feet(im)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return {
        "image": im,
        "png": buf.getvalue(),
        "axis": axis,
        "rgba_sha256": hashlib.sha256(a.tobytes()).hexdigest(),
    }


def head_crop(full: Image.Image) -> Image.Image:
    a = np.array(full.convert("RGBA"))
    ys, xs = np.where(a[:, :, 3] > 20)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    h = y1 - y0 + 1
    w = x1 - x0 + 1
    # upper third, centered
    crop = full.crop((x0 + int(w * 0.28), y0, x0 + int(w * 0.78), y0 + int(h * 0.38)))
    return crop_alpha(crop, 0)


def main() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    sff_path = NAR / "Naruto_Ashura_JUS.sff"
    air_path = NAR / "Naruto_Ashura_JUS.air"
    if not (BACKUP / "Naruto_Ashura_JUS.sff").exists():
        shutil.copy2(sff_path, BACKUP / "Naruto_Ashura_JUS.sff")
        shutil.copy2(air_path, BACKUP / "Naruto_Ashura_JUS.air")

    sff = Sff(sff_path)

    # --- portraits ---
    src = sff.decode(sff.keys[(9000, 2)]).convert("RGBA")
    corner = np.array(src)[4, 4, :3]
    print("portrait corner", corner.tolist())
    clean = crop_alpha(key_near(src, corner, 90))
    clean.save(ART / "portrait-9000-2-clean.png")
    icon = head_crop(clean)
    icon.thumbnail((160, 180), Image.Resampling.LANCZOS)
    icon.save(ART / "portrait-9000-0-clean.png")

    repl = {
        (9000, 0): pack(icon, axis=(0, 0)),
        (9000, 2): pack(clean, axis=(0, 0)),
    }
    additions = {(9000, 3): pack(clean, axis=(0, 0))}

    # --- kurama ---
    fox = Image.open(KURAMA_SRC).convert("RGBA")
    bg = np.array(fox)[2, 2, :3]
    print("kurama corner", bg.tolist())
    fox = crop_alpha(key_near(fox, bg, 70))
    h = body_h(fox)
    fox = fox.resize((max(1, int(fox.width * 700 / h)), 700 * fox.height // h), Image.Resampling.LANCZOS)
    a = np.array(fox)
    a[:, :, 3] = np.where(a[:, :, 3] > 128, 255, 0).astype(np.uint8)
    fox = Image.fromarray(a)
    fox = crop_alpha(fox)
    fox.save(ART / "kurama-installed.png")
    fox_h = body_h(fox)
    kurama_scale = SUMMON_SCREEN / (fox_h * CHAR_SCALE)
    print(f"kurama bodyH={fox_h} air_scale={kurama_scale:.6f} screen~{fox_h * CHAR_SCALE * kurama_scale:.1f}")
    fox_pack = pack(fox)
    for key in list(sff.keys):
        if key[0] == 2300:
            repl[key] = fox_pack

    # --- form scale lock (sprites taller/shorter than idle) ---
    form_scales = {}
    for group in (5000, 16000, 17000):
        keys = sorted(k for k in sff.keys if k[0] == group)
        if not keys:
            continue
        im = sff.decode(sff.keys[keys[0]])
        h = body_h(im)
        form_scales[group] = IDLE_BODY / max(1, h)
        print(f"form {group} bodyH={h} lock_scale={form_scales[group]:.4f} screen {h * CHAR_SCALE:.1f} -> {IDLE_BODY * CHAR_SCALE:.1f}")

    (sff_path).write_bytes(sff.derive(repl, additions))

    air = air_path.read_text(encoding="latin-1", errors="replace")
    air2 = air.replace("5.83333333333", f"{kurama_scale:.8f}")
    n_kurama = air.count("5.83333333333")
    print("kurama scale replacements", n_kurama)

    def scale_line(line: str) -> str:
        raw = line.split(";", 1)[0]
        if ";" in line:
            comment = line[len(raw) :]
        else:
            comment = ""
        body = raw.rstrip("\r\n")
        nl = "\r\n" if raw.endswith("\r\n") else ("\n" if raw.endswith("\n") else "")
        stripped = body.strip()
        m = re.match(r"^(\d+)\s*,", stripped)
        if not m:
            return line
        group = int(m.group(1))
        if group not in form_scales:
            return line
        parts = [p.strip() for p in stripped.split(",")]
        if len(parts) >= 9 and parts[7] and parts[8]:
            return line
        while len(parts) < 9:
            parts.append("")
        sc = f"{form_scales[group]:.8f}"
        parts[7] = sc
        parts[8] = sc
        return ",".join(parts) + comment + ("" if comment.endswith("\n") or not nl else "")

    # preserve newlines via splitlines keepends
    lines = air2.splitlines(keepends=True)
    patched = []
    changed = 0
    for line in lines:
        new = scale_line(line)
        if new != line:
            changed += 1
        patched.append(new if new.endswith("\n") or new.endswith("\r") else new + ("\n" if line.endswith("\n") else ""))
    # scale_line may drop newline if comment handling is messy. Use a safer rewrite:
    patched = []
    changed = 0
    for line in lines:
        ending = ""
        core = line
        if core.endswith("\r\n"):
            core, ending = core[:-2], "\r\n"
        elif core.endswith("\n"):
            core, ending = core[:-1], "\n"
        new = scale_line(core + "\n").rstrip("\r\n")
        if new != core:
            changed += 1
        patched.append(new + ending)
    air_path.write_text("".join(patched), encoding="latin-1", errors="replace")
    print("form scale lines", changed)
    print("DONE")


if __name__ == "__main__":
    main()
