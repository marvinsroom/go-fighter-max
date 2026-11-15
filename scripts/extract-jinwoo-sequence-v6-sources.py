"""Extract the 12 exact original cells used to rebuild the v6 sequence."""
from pathlib import Path
import json

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sprite-fighter/characters/jinwoo-mugen-reskin/art/approved-native-v5/jinwoo-03.png"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen-reskin/art/sequence-v6/sources"
OUT.mkdir(parents=True, exist_ok=True)

image = Image.open(SOURCE).convert("RGBA")
entries = []
for index in range(12):
    column, row = index % 4, index // 4
    left = round(column * image.width / 4)
    right = round((column + 1) * image.width / 4)
    top = round(row * image.height / 3)
    bottom = round((row + 1) * image.height / 3)
    cell = image.crop((left, top, right, bottom))
    path = OUT / f"source-{index:02d}.png"
    cell.save(path)
    entries.append({"cell": index, "source": str(path.relative_to(ROOT)), "size": list(cell.size)})

(OUT / "manifest.json").write_text(json.dumps({"source_sheet": str(SOURCE.relative_to(ROOT)), "cells": entries}, indent=2), encoding="utf-8")
print(json.dumps({"status": "PASS", "cells": len(entries), "cell_size": entries[0]["size"]}))
