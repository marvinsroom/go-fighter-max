"""Match Naruto's human-form stature to Jinwoo while preserving giant Kurama."""
from pathlib import Path
import hashlib
import json
import re

R = Path(__file__).resolve().parents[1]
cns = R / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto/Naruto.cns"
specials = R / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto/Specials.cns"
out = R / "sprite-fighter/characters/naruto/size-fixes/human-v2"
out.mkdir(parents=True, exist_ok=True)
backup = out / "before.cns"
if not backup.exists():
    backup.write_bytes(cns.read_bytes())

raw = backup.read_bytes().decode("cp1252")
target = 0.18
updated, nx = re.subn(r"(?im)^(\s*xscale\s*=\s*)[-+.0-9]+", rf"\g<1>{target}", raw, count=1)
updated, ny = re.subn(r"(?im)^(\s*yscale\s*=\s*)[-+.0-9]+", rf"\g<1>{target}", updated, count=1)
assert nx == ny == 1
cns.write_bytes(updated.encode("cp1252"))

# The Rasengan contact helper had an explicit .05 scale that was effectively
# multiplied by Naruto's old root scale. Compensate only that helper so its
# established contact size survives the visual body correction.
specials_backup = out / "before-Specials.cns"
if not specials_backup.exists():specials_backup.write_bytes(specials.read_bytes())
specials_raw=specials_backup.read_bytes().decode("cp1252")
rasengan_scale=.05*(.5/target)
specials_updated,nx=re.subn(r"(?im)^(size\.xscale\s*=\s*)\.05\s*$",rf"\g<1>{rasengan_scale:.12g}",specials_raw,count=1)
specials_updated,ny=re.subn(r"(?im)^(size\.yscale\s*=\s*)\.05\s*$",rf"\g<1>{rasengan_scale:.12g}",specials_updated,count=1)
assert nx==ny==1
specials.write_bytes(specials_updated.encode("cp1252"))

report = {
    "status": "Installed",
    "player_scale_before": 0.7,
    "player_scale_after": target,
    "screen_ratio": target / 0.7,
    "reason": "Naruto's 217-230px imported body rasters were still oversized after local-coordinate conversion; 0.18 matches Jinwoo's actual rendered stature.",
    "kurama_compensation": "Kurama AIR geometry is rebuilt at 5.83333333333x so its approved on-screen size is preserved after the player-scale change.",
    "before_sha256": hashlib.sha256(backup.read_bytes()).hexdigest(),
    "installed_sha256": hashlib.sha256(cns.read_bytes()).hexdigest(),
    "rasengan_helper_scale": rasengan_scale,
    "rasengan_specials_sha256": hashlib.sha256(specials.read_bytes()).hexdigest(),
    "recording": False,
}
(out / "installation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
