"""Extract the eight dagger-contaminated normal frames for bare-hand restyling."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
OUT = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/bare-hands-v47/source"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sff = Sff(LIVE / "spr.sff")
    for number in range(8):
        index = sff.keys[(61011, number)]
        image = sff.decode(index).convert("RGBA")
        image.save(OUT / f"bare-source-{number}.png")
    sff.decode(sff.keys[(300, 101)]).convert("RGBA").save(OUT / "canonical-idle-300-101.png")
    print(OUT)


if __name__ == "__main__":
    main()
