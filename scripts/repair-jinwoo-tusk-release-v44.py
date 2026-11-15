"""Add the Tusk spell-release sprite key omitted because it was absent in live SFF."""
import hashlib
import io
import sys
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from mugen_sff import Sff  # noqa: E402

SFF_PATH=ROOT/"sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo/spr.sff"
SOURCE=ROOT/"sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/loco-final-v32/tusk-kaisel-restyle-v32/tusk-release-normalized-v32.png"

def main():
    archive=Sff(SFF_PATH); key=(1000,222)
    if key in archive.keys:
        print("Tusk release key already installed"); return
    image=Image.open(SOURCE).convert("RGBA"); payload=io.BytesIO(); image.save(payload,format="PNG",optimize=True)
    frame={"image":image,"png":payload.getvalue(),"axis":(768,1236),"rgba_sha256":hashlib.sha256(image.tobytes()).hexdigest()}
    SFF_PATH.write_bytes(archive.derive({}, {key:frame}))
    print("Installed",key)

if __name__=="__main__": main()
