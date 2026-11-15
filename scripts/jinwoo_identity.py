"""One human identity: preserve native effects, suppress imported character stills."""
import re

# These are baked anime panels and portrait strips, not weapon/effect sprites.
# Source files and SFF originals remain preserved; only their derived AIR rows
# are blanked so no move can flash a different face or outfit over our fighter.
LEGACY_PICTURES={(500,n) for n in range(46,53)}|{(9001,n) for n in range(5)}


def hide_legacy_pictures(air):
    out=[]
    for line in air.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            raw,sep,comment=line.partition(';');parts=raw.split(',')
            if tuple(int(x.strip()) for x in parts[:2]) in LEGACY_PICTURES:
                parts[:2]=['-1','0'];line=','.join(parts)+(' ;'+comment if sep else '')
        out.append(line)
    return '\n'.join(out)+'\n'
