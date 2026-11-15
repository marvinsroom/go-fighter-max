"""Do not interpolate calibrated drawing scales across different raster sizes."""
import re


def stabilize(text,body_keys):
    changes=[];out=[]
    for block in re.split(r'(?=^\[Begin Action )',text,flags=re.I|re.M):
        keys=[]
        for line in block.splitlines():
            if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):keys.append(tuple(int(x.strip()) for x in line.split(',')[:2]))
        if any(key in body_keys for key in keys):
            block,count=re.subn(r'(?im)^[ \t]*Interpolate[ \t]+Scale[ \t]*(?:;[^\n]*)?\r?\n','',block)
            if count:
                h=re.match(r'\[Begin Action (\d+)\]',block,re.I)
                changes.append({'action':int(h[1]) if h else None,'removed_scale_interpolations':count})
        out.append(block)
    return ''.join(out),changes
