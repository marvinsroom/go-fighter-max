"""Install a tightly framed 100x100 Naruto lifebar portrait as SFF 9000,1."""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

CHAR = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto"
ART = ROOT / "sprite-fighter/characters/naruto/art/hud-portrait-v2"
SOURCE = ART / "naruto-hud-portrait-v2-source.png"
FINAL = ART / "naruto-hud-portrait-v2.png"
SFF_PATH = CHAR / "Naruto_Ashura_JUS.sff"
BACKUP = ART / "Naruto_Ashura_JUS.pre-hud-portrait-v2.sff"
REPORT = ART / "installation.json"
KEYS = ((9000, 0), (9000, 1))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    image = Image.open(SOURCE).convert("RGB")
    image = image.resize((100, 100), Image.Resampling.LANCZOS).convert("RGBA")
    image.save(FINAL, optimize=True)

    payload = io.BytesIO()
    image.save(payload, format="PNG", optimize=True)
    frame = {
        "image": image,
        "png": payload.getvalue(),
        "axis": (0, 0),
        "rgba_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
    }

    if not BACKUP.exists():
        shutil.copy2(SFF_PATH, BACKUP)
    source = Sff(SFF_PATH)
    pending = SFF_PATH.with_suffix(".sff.pending")
    pending.write_bytes(source.derive({key: frame for key in KEYS}, {}))
    pending.replace(SFF_PATH)

    proof = Sff(SFF_PATH)
    for key in KEYS:
        index = proof.keys[key]
        decoded = proof.decode(index).convert("RGBA")
        assert decoded.size == (100, 100)
        assert decoded.getchannel("A").getbbox() == (0, 0, 100, 100)
        assert hashlib.sha256(decoded.tobytes()).hexdigest() == frame["rgba_sha256"]

    report = {
        "status": "INSTALLED",
        "sprites": [list(key) for key in KEYS],
        "size": [100, 100],
        "visible_bbox": [0, 0, 100, 100],
        "asset": str(FINAL.relative_to(ROOT)),
        "sff_sha256": sha(SFF_PATH),
        "backup": str(BACKUP.relative_to(ROOT)),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
