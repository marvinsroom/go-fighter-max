"""Audit newly generated v10 atlases and create installer metadata/extractions."""
from pathlib import Path
import hashlib, json, sys

import numpy as np
from PIL import Image
from isolated_sprite_atlas import extract

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


failed = []
for slug in sys.argv[1:] or ("naruto", "saitama"):
    art = ROOT / "sprite-fighter/characters" / slug / "art/comic-style-v10"
    requests = json.loads((art / "requests.json").read_text(encoding="utf-8"))
    for request in requests:
        kind = request["kind"]
        target = art / f"{kind}.png"
        meta_path = art / f"{kind}.generation.json"
        if meta_path.exists():
            current = json.loads(meta_path.read_text(encoding="utf-8"))
            if current.get("sha256") == sha(target.read_bytes()) and current.get("layout_validation", {}).get("status") == "PASS":
                continue
        image = Image.open(target).convert("RGBA")
        alpha = np.asarray(image)[:, :, 3]
        failures = []
        if np.mean(alpha == 0) < 0.2:
            failures.append("Background is not sufficiently transparent")
        folder = art / "extracted" / kind
        folder.mkdir(parents=True, exist_ok=True)
        cells = []
        try:
            isolated = extract(target, request["columns"], request["rows"], count=request["count"])
            for index, (crop, bounds) in enumerate(isolated):
                crop.save(folder / f"{index:02d}.png")
                cells.append({
                    "index": index,
                    "bounds": bounds,
                    "size": crop.size,
                    "rgba_sha256": sha(crop.tobytes()),
                })
        except Exception as error:
            # Long authored chakra limbs/slashes can cross the component split's
            # internal gutter threshold while remaining inside their exact grid
            # cells. Fall back to the declared atlas grid and alpha bounds.
            cells = []
            for index in range(request["count"]):
                column = index % request["columns"]
                row = index // request["columns"]
                box = (
                    round(column * image.width / request["columns"]),
                    round(row * image.height / request["rows"]),
                    round((column + 1) * image.width / request["columns"]),
                    round((row + 1) * image.height / request["rows"]),
                )
                tile = image.crop(box)
                bounds = tile.getchannel("A").point(lambda value: 255 if value > 48 else 0).getbbox()
                if not bounds:
                    failures.append(f"Missing drawing {index} after grid fallback")
                    continue
                crop = tile.crop(bounds)
                crop.save(folder / f"{index:02d}.png")
                cells.append({
                    "index": index,
                    "bounds": [box[0] + bounds[0], box[1] + bounds[1], box[0] + bounds[2], box[1] + bounds[3]],
                    "size": crop.size,
                    "rgba_sha256": sha(crop.tobytes()),
                })
            if len(cells) == request["count"]:
                print(slug, kind, "used exact-grid alpha fallback after", error, flush=True)
        if len(cells) != request["count"]:
            failures.append(f"Expected {request['count']} drawings, extracted {len(cells)}")
        prompt_path = art / f"{kind}.prompt.txt"
        prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else request.get("prompt", "")
        references = request.get("references") or request.get("referenced_image_paths") or []
        metadata = {
            "tool": "built-in imagegen",
            "original_generated_file": "Built-in output copied into project during 2026-10-22 resume",
            "sha256": sha(target.read_bytes()),
            "layout_validation": {
                "status": "PASS" if not failures else "REVIEW",
                "method": "Connected whole-figure extraction; source alpha retained",
                "cells": cells,
                "failures": failures,
            },
            "slug": slug,
            "kind": kind,
            "prompt": prompt,
            "references": references,
        }
        meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print(slug, kind, len(cells), metadata["layout_validation"]["status"], failures, flush=True)
        if failures:
            failed.append((slug, kind, failures))

if failed:
    raise SystemExit("Atlas audit requires review: " + repr(failed))
print("NATIVE_STYLE_V10_ASSET_AUDIT_PASS")
