"""Remove chroma-magenta spill / unfinished pink rim from loco v26 frames."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v26"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v26-clean"
OUT.mkdir(parents=True, exist_ok=True)


def key_and_clean(path: Path) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    a = np.array(im).astype(np.int16)
    r, g, b, al = a[:, :, 0], a[:, :, 1], a[:, :, 2], a[:, :, 3]

    # Base chroma key
    mag = (r > 170) & (b > 170) & (g < 140) & (np.abs(r - b) < 90)
    near = (r > 200) & (b > 150) & (g < 170) & (np.abs(r - b) < 100)
    al = np.where(mag | near, 0, al)

    fg = al > 40
    # Magenta/pink-ish (chroma spill + AI rim)
    pink = fg & (r > 130) & (b > 120) & (g < 170) & ((r.astype(np.int16) + b) > (g * 2 + 30)) & (
        np.abs(r.astype(np.int16) - b) < 90
    )
    # Strong pure magenta (very close to key color)
    pure = fg & (r > 200) & (b > 180) & (g < 120) & (np.abs(r - b) < 50)

    # Edge fringe: pink near transparent
    dil = ndimage.binary_dilation(~fg, iterations=2)
    fringe = pink & dil
    al = np.where(fringe | pure, 0, al)
    fg = al > 40
    pink = fg & (r > 130) & (b > 120) & (g < 170) & ((r.astype(np.int16) + b) > (g * 2 + 30)) & (
        np.abs(r.astype(np.int16) - b) < 90
    )

    # Remap remaining pink interiors to cool purple / grey highlights (not chroma pink)
    # Keep dagger purple energy: high B, moderate R, low G but not equal R≈B magenta
    daggerish = fg & (b > 150) & (r > 80) & (r < 200) & (g < 100) & (b > r + 20)
    remap = pink & ~daggerish

    # Convert magenta highlight -> muted violet-grey based on luminance
    lum = (0.3 * r + 0.4 * g + 0.3 * b).astype(np.float32)
    # dark areas get deep purple shadow edge; bright get soft lavender-grey
    nr = np.clip(lum * 0.55 + 35, 0, 255)
    ng = np.clip(lum * 0.35 + 20, 0, 255)
    nb = np.clip(lum * 0.70 + 55, 0, 255)
    r = np.where(remap, nr, r)
    g = np.where(remap, ng, g)
    b = np.where(remap, nb, b)

    out = np.stack([r, g, b, al], axis=-1).astype(np.uint8)
    ys, xs = np.where(out[:, :, 3] > 40)
    if len(ys) == 0:
        raise RuntimeError(f"empty {path}")
    pad = 2
    crop = out[
        max(0, ys.min() - pad) : min(out.shape[0], ys.max() + 1 + pad),
        max(0, xs.min() - pad) : min(out.shape[1], xs.max() + 1 + pad),
    ]
    return Image.fromarray(crop)


def main() -> None:
    files = sorted(list(SRC.glob("*.png")) + list(SRC.glob("*.jpg")))
    # prefer png
    seen = set()
    for path in files:
        stem = path.stem
        if stem in seen:
            continue
        if (SRC / f"{stem}.png").exists():
            path = SRC / f"{stem}.png"
        seen.add(stem)
        cleaned = key_and_clean(path)
        cleaned.save(OUT / f"{stem}.png")
        # preview on dark
        prev = Image.new("RGB", cleaned.size, (36, 36, 42))
        prev.paste(cleaned, mask=cleaned.split()[-1])
        prev.save(OUT / f"{stem}-preview.jpg", quality=92)
        a = np.array(cleaned)
        r, g, b, al = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int), a[:, :, 3]
        fg = al > 40
        pink = fg & (r > 140) & (b > 140) & (g < 160) & (np.abs(r - b) < 80)
        print(f"{stem}: pink%={100*pink.sum()/max(1,fg.sum()):.2f}")
    print("CLEANED", len(seen), "->", OUT)


if __name__ == "__main__":
    main()
