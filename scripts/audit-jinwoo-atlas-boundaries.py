"""Audit Jinwoo and shadow sprite sources for clipped/cross-cell artwork."""
from __future__ import annotations

from pathlib import Path
import json

import numpy as np
from PIL import Image
from scipy import ndimage

from jinwoo_motion import atlas_rects


ROOT = Path(__file__).resolve().parents[1]
CHAR = ROOT / "sprite-fighter/characters/jinwoo"
OUT = CHAR / "validation/atlas-boundary-audit.json"


def edge_counts(alpha: np.ndarray, margin: int = 4) -> dict[str, int]:
    ink = alpha > 48
    return {
        "left": int(ink[:, :margin].sum()),
        "right": int(ink[:, -margin:].sum()),
        "top": int(ink[:margin, :].sum()),
        "bottom": int(ink[-margin:, :].sum()),
    }


def audit_grid(path: Path, cols: int, rows: int) -> dict:
    with Image.open(path) as source:
        source = source.convert("RGBA")
        rects = atlas_rects(source, cols, rows)
        frames = []
        for index, rect in enumerate(rects):
            alpha = np.asarray(source.crop(rect).getchannel("A"))
            edges = edge_counts(alpha)
            frames.append({
                "index": index,
                "rect": list(rect),
                "edge_pixels": edges,
                "touches_cut": any(edges.values()),
            })
    return {
        "file": str(path.relative_to(ROOT)),
        "grid": [cols, rows],
        "frames": frames,
        "touching_frames": [f["index"] for f in frames if f["touches_cut"]],
    }


def audit_registered(path: Path, sheet: dict) -> dict:
    with Image.open(path) as source:
        pixels = np.asarray(source.convert("RGBA"))
    labels, count = ndimage.label(pixels[:, :, 3] > sheet["alpha_min"])
    objects = ndimage.find_objects(labels)
    frames = []
    for index, frame in enumerate(sheet["frames"]):
        x1, y1, x2, y2 = frame["rect"]
        chosen = set(frame["components"])
        intersecting = {int(value) for value in np.unique(labels[y1:y2, x1:x2])} - {0}
        omitted = sorted(intersecting - chosen)
        selected_bounds = []
        for component in sorted(chosen):
            obj = objects[component - 1] if 0 < component <= count else None
            if obj:
                selected_bounds.append([obj[1].start, obj[0].start, obj[1].stop, obj[0].stop])
        alpha = pixels[y1:y2, x1:x2, 3].copy()
        alpha[~np.isin(labels[y1:y2, x1:x2], list(chosen))] = 0
        edges = edge_counts(alpha)
        frames.append({
            "index": index,
            "rect": frame["rect"],
            "axis": frame["axis"],
            "components": sorted(chosen),
            "selected_component_bounds": selected_bounds,
            "omitted_intersecting_components": omitted,
            "edge_pixels": edges,
            "touches_rect": any(edges.values()),
        })
    return {
        "file": str(path.relative_to(ROOT)),
        "frames": frames,
        "touching_frames": [f["index"] for f in frames if f["touches_rect"]],
        "frames_with_omitted_components": [f["index"] for f in frames if f["omitted_intersecting_components"]],
    }


def main() -> None:
    report = {"shadow_grids": {}, "greatsword_registration": {}}
    shadow_dir = CHAR / "art/shadows"
    for form in ("igris", "beru", "iron", "tank"):
        for kind in ("movement", "combat"):
            versioned = shadow_dir / f"{form}-{kind}-v2.png"
            path = versioned if versioned.exists() else shadow_dir / f"{form}-{kind}.png"
            report["shadow_grids"][f"{form}-{kind}"] = audit_grid(path, 4, 3)

    sword_dir = CHAR / "art/greatsword"
    registration = json.loads((sword_dir / "registration.json").read_text(encoding="utf-8"))
    for name, sheet in registration["sheets"].items():
        path = sword_dir / sheet["file"]
        report["greatsword_registration"][name] = audit_registered(path, sheet)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    shadow_bad = {k: v["touching_frames"] for k, v in report["shadow_grids"].items() if v["touching_frames"]}
    sword_bad = {
        k: {"touching": v["touching_frames"], "omitted": v["frames_with_omitted_components"]}
        for k, v in report["greatsword_registration"].items()
        if v["touching_frames"] or v["frames_with_omitted_components"]
    }
    print(json.dumps({"shadow": shadow_bad, "greatsword": sword_bad, "report": str(OUT.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
