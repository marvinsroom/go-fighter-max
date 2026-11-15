"""Fail-closed reference audit for Jinwoo's v32 long sword and Antares chain."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32"
REPORT_PATH = BASE / "weapon-action-audit-v32.json"
ANTARES_CAST = BASE / "antares-normalized/300-136-antares-cast-v32.png"
ANTARES_REVIEW = BASE / "antares-review-v32.json"
ANTARES_SEQUENCE_REVIEW = BASE / "antares-sequence-review-v32.json"
ANTARES_EFFECT_REVIEW = BASE / "antares-effects-review-v32.json"
MIN_MARGIN = 16
ANTARES_SEQUENCE = {
    "200,110": "200-110-antares-charge-0-v32.png",
    "200,111": "200-111-antares-charge-1-v32.png",
    "200,112": "200-112-antares-charge-2-v32.png",
    "200,113": "200-113-antares-charge-3-v32.png",
    "200,114": "200-114-antares-full-charge-v32.png",
    "200,115": "200-115-antares-lunge-1-v32.png",
    "200,116": "200-116-antares-lunge-2-v32.png",
    "200,117": "200-117-antares-hit-v32.png",
}
ANTARES_EFFECTS = {
    "1988,7": "antares-cast-flare--1988-7-v32.png",
    "1988,8": "antares-cast-column--1988-8-v32.png",
    "1988,10": "antares-cast-core--1988-10-v32.png",
    **{f"2024,{index}": f"antares-impact-{index:02d}--2024-{index}-v32.png" for index in range(6)},
    **{f"2053,{index}": f"antares-finish-{index:02d}--2053-{index}-v32.png" for index in range(10)},
}

REQUIRED = {
    "long-sword-idle",
    "long-sword-walk",
    "long-sword-air",
    "antares-cast-jinwoo",
    *(f"antares-{index:02d}" for index in range(7)),
    "antares-hit",
    "antares-cast-flare",
    "antares-cast-column",
    "antares-cast-core",
    *(f"antares-impact-{index:02d}" for index in range(6)),
    *(f"antares-finish-{index:02d}" for index in range(10)),
}


def main() -> None:
    references = json.loads((BASE / "weapon-references/references.json").read_text(encoding="utf-8"))
    plan = json.loads((BASE / "weapon-action-plan-v32.json").read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - references.keys())
    failed = sorted(name for name in REQUIRED if references.get(name, {}).get("status") != "extracted")
    missing_files = []
    for name in sorted(REQUIRED):
        entry = references.get(name)
        if not entry or entry.get("status") != "extracted":
            continue
        group, image = entry["key"]
        if not (BASE / "weapon-references" / f"{name}--{group}-{image}.png").is_file():
            missing_files.append(name)

    candidate_masters = sorted(path.name for path in (BASE / "weapon-masters").glob("*.png"))
    approved_master = BASE / "weapon-masters/long-sword-approved-v32.png"
    rejected = sorted(path.name for path in (BASE / "rejected-wrong-weapons").glob("*.png"))
    rejected_anatomy = sorted(path.name for path in (BASE / "rejected-anatomy").glob("*.png"))
    references_ok = not missing and not failed and not missing_files
    cast_errors = []
    cast_data = {"file": str(ANTARES_CAST.relative_to(BASE)), "exists": ANTARES_CAST.is_file()}
    review = json.loads(ANTARES_REVIEW.read_text(encoding="utf-8")) if ANTARES_REVIEW.is_file() else {}
    if not ANTARES_CAST.is_file():
        cast_errors.append("missing_antares_cast_candidate")
    else:
        image = Image.open(ANTARES_CAST).convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.point(lambda value: 255 if value >= 96 else 0).getbbox()
        cast_data.update({"size": list(image.size), "opaque_bbox": list(bbox) if bbox else None})
        if image.size != (1536, 1536):
            cast_errors.append(f"wrong_antares_cast_size:{image.size}")
        if not bbox:
            cast_errors.append("empty_antares_cast")
        else:
            left, top, right, bottom = bbox
            margins = (left, top, image.width - right, image.height - bottom)
            cast_data["opaque_margins"] = list(margins)
            if min(margins) < MIN_MARGIN:
                cast_errors.append(f"unsafe_antares_cast_margin:{margins}")
    required_review = {
        "arms": 2,
        "hands": 2,
        "weapons": 2,
        "weapon_type": "dual-daggers",
        "right_hand": "dagger",
        "left_hand": "dagger",
        "sword_present": False,
        "dagger_design": "curved-black-shadow",
        "aura_color": "violet-purple",
        "grip_style": "forward-grip-both-hands",
        "blade_exit_side": "thumb-index",
        "facing": "screen-right",
        "eyes_visible": True,
        "feet_complete": True,
    }
    for field, expected in required_review.items():
        if review.get(field) != expected:
            cast_errors.append(f"antares_cast_review_failed:{field}")
    cast_ok = not cast_errors
    sequence_review = json.loads(ANTARES_SEQUENCE_REVIEW.read_text(encoding="utf-8")) if ANTARES_SEQUENCE_REVIEW.is_file() else {}
    sequence_errors = []
    sequence_data = {}
    for key, name in ANTARES_SEQUENCE.items():
        path = BASE / "antares-normalized" / name
        row = {"file": name, "exists": path.is_file()}
        sequence_data[key] = row
        if not path.is_file():
            sequence_errors.append(f"missing_antares_sequence_frame:{key}")
            continue
        image = Image.open(path).convert("RGBA")
        bbox = image.getchannel("A").point(lambda value: 255 if value >= 96 else 0).getbbox()
        row.update({"size": list(image.size), "opaque_bbox": list(bbox) if bbox else None})
        if image.size != (1536, 1536):
            sequence_errors.append(f"wrong_antares_sequence_size:{key}:{image.size}")
        if not bbox:
            sequence_errors.append(f"empty_antares_sequence_frame:{key}")
        else:
            left, top, right, bottom = bbox
            margins = (left, top, image.width - right, image.height - bottom)
            row["opaque_margins"] = list(margins)
            if min(margins) < MIN_MARGIN:
                sequence_errors.append(f"unsafe_antares_sequence_margin:{key}:{margins}")
        manual = sequence_review.get("frames", {}).get(key, {})
        row["manual_review"] = manual
        for field, expected in {
            "arms": 2,
            "hands": 2,
            "weapons": 2,
            "dagger_design": "curved-black-shadow",
            "aura_color": "violet-purple",
            "grip_style": "forward-grip-both-hands",
            "facing": "screen-right",
            "feet_complete": True,
        }.items():
            if manual.get(field) != expected:
                sequence_errors.append(f"antares_sequence_review_failed:{key}:{field}")
    sequence_ok = not sequence_errors
    effect_review = json.loads(ANTARES_EFFECT_REVIEW.read_text(encoding="utf-8")) if ANTARES_EFFECT_REVIEW.is_file() else {}
    effect_errors = []
    effect_data = {}
    for key, name in ANTARES_EFFECTS.items():
        path = BASE / "antares-effects-normalized" / name
        row = {"file": name, "exists": path.is_file()}
        effect_data[key] = row
        if not path.is_file():
            effect_errors.append(f"missing_antares_effect_frame:{key}")
            continue
        image = Image.open(path).convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.point(lambda value: 255 if value >= 32 else 0).getbbox()
        histogram = alpha.histogram()
        semi_transparent = sum(histogram[1:255])
        opaque = histogram[255]
        corners = [alpha.getpixel(point) for point in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1))]
        row.update({
            "size": list(image.size),
            "effect_bbox": list(bbox) if bbox else None,
            "semi_transparent_pixels": semi_transparent,
            "opaque_pixels": opaque,
            "corner_alpha": corners,
        })
        if image.size != (1536, 1536):
            effect_errors.append(f"wrong_antares_effect_size:{key}:{image.size}")
        if not bbox:
            effect_errors.append(f"empty_antares_effect_frame:{key}")
        else:
            left, top, right, bottom = bbox
            margins = (left, top, image.width - right, image.height - bottom)
            row["effect_margins"] = list(margins)
            if min(margins) < MIN_MARGIN:
                effect_errors.append(f"unsafe_antares_effect_margin:{key}:{margins}")
        if semi_transparent == 0:
            effect_errors.append(f"hard_edge_antares_effect:{key}")
        if any(value > 8 for value in corners):
            effect_errors.append(f"nontransparent_antares_effect_corner:{key}:{corners}")
        if opaque > image.width * image.height * 0.30:
            effect_errors.append(f"opaque_antares_effect_background:{key}:{opaque}")
    required_effect_review = {
        "effect_only": True,
        "body_pixels_present": False,
        "weapon_pixels_present": False,
        "palette": "black-indigo-violet-electric-purple",
        "transparent_background": True,
        "opaque_flash_frames_present": False,
        "pixel_art_present": False,
        "visual_review": "approved-candidate",
    }
    for field, expected in required_effect_review.items():
        if effect_review.get(field) != expected:
            effect_errors.append(f"antares_effect_review_failed:{field}")
    effects_ok = not effect_errors
    install_ready = references_ok and cast_ok and sequence_ok and effects_ok and approved_master.is_file() and plan.get("live_install_allowed") is True
    report = {
        "status": "CANDIDATE_PASS_INSTALL_BLOCKED" if references_ok and cast_ok and sequence_ok and effects_ok and not install_ready else "PASS" if install_ready else "FAIL",
        "references_ok": references_ok,
        "install_ready": install_ready,
        "required_reference_count": len(REQUIRED),
        "missing_reference_records": missing,
        "failed_extractions": failed,
        "missing_reference_files": missing_files,
        "candidate_weapon_masters": candidate_masters,
        "approved_weapon_master_present": approved_master.is_file(),
        "antares_cast_candidate": cast_data,
        "antares_cast_review": review,
        "antares_cast_errors": cast_errors,
        "antares_sequence_progress": f"{len(ANTARES_SEQUENCE)}/8 body frames",
        "antares_sequence_frames": sequence_data,
        "antares_sequence_errors": sequence_errors,
        "antares_effect_progress": f"{len(ANTARES_EFFECTS)}/19 auxiliary effect frames",
        "antares_effect_frames": effect_data,
        "antares_effect_review": effect_review,
        "antares_effect_errors": effect_errors,
        "rejected_weapon_files": rejected,
        "rejected_anatomy_files": rejected_anatomy,
        "install_block_reason": None if install_ready else "The long-sword locomotion, Antares body sequence, and auxiliary VFX candidates exist, but final in-engine visual approval and live_install_allowed are still required before installation.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not references_ok or not cast_ok or not sequence_ok or not effects_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
