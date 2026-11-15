"""Remove unreachable payloads from Jinwoo's repeatedly-derived SFF v2 file."""
from __future__ import annotations

import json
import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from mugen_sff import Sff  # noqa: E402

LIVE = ROOT / "sprite-fighter/engine/ikemen-go-v1.0.0/chars/jinwoo"
ART = ROOT / "sprite-fighter/characters/jinwoo-mugen/art/naruto-style-v2/unified-base-v48/compact-v62"
SFF_PATH = LIVE / "spr.sff"


def main() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    source = Sff(SFF_PATH)
    if source.ts != 0:
        raise RuntimeError("texture payload compaction is not supported")

    before = len(source.data)
    output = bytearray(source.data[:source.lo])

    # Palette payloads live in the same local-data section as sprites. Copy
    # every referenced block and rewrite its relative offset.
    for index in range(source.palcount):
        pos = source.paloff + index * 16
        group, number, colors, link, offset, length = struct.unpack_from("<HHHHII", source.data, pos)
        if length:
            new_offset = len(output) - source.lo
            output.extend(source.data[source.lo + offset:source.lo + offset + length])
            struct.pack_into("<HHHHII", output, pos, group, number, colors, link, new_offset, length)

    # Copy only payloads that a current sprite header can reach. Linked
    # sprites retain their original link indices and require no payload.
    for index, header in enumerate(source.headers):
        values = list(header)
        length = header[10]
        if length:
            if header[12] & 1:
                raise RuntimeError(f"unexpected texture sprite at header {index}")
            new_offset = len(output) - source.lo
            start = source.lo + header[9]
            output.extend(source.data[start:start + length])
            values[9] = new_offset
        struct.pack_into("<HHHHhhHBBIIHH", output, source.offset + index * 28, *values)

    struct.pack_into("<IIII", output, 52, source.lo, len(output) - source.lo, len(output), 0)
    pending = ART / "spr.compacted.pending.sff"
    pending.write_bytes(output)

    # Structural and representative decode validation before touching live.
    check = Sff(pending)
    if check.count != source.count or check.keys.keys() != source.keys.keys():
        raise RuntimeError("compacted SFF changed the sprite table")
    for key in ((61013, 24), (61022, 0), (61023, 0), (61024, 1), (61019, 0)):
        check.decode(check.keys[key]).load()

    backup = ART / "spr.before-compaction.sff"
    if not backup.exists():
        shutil.copy2(SFF_PATH, backup)
    try:
        pending.replace(SFF_PATH)
    except PermissionError:
        shutil.copy2(pending, SFF_PATH)
        pending.unlink()

    installed = Sff(SFF_PATH)
    report = {
        "status": "INSTALLED",
        "sprite_headers": installed.count,
        "unique_keys": len(installed.keys),
        "before_bytes": before,
        "after_bytes": len(installed.data),
        "removed_bytes": before - len(installed.data),
        "reduction_percent": round((before - len(installed.data)) * 100 / before, 2),
    }
    (ART / "installation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
