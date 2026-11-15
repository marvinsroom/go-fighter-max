"""Enlarge the full Kurama sprite bank and its per-frame collision geometry."""
from pathlib import Path
import hashlib,json,re

R=Path(__file__).resolve().parents[1]
air=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/naruto/Naruto_Ashura_JUS.air'
out=R/'sprite-fighter/characters/naruto/size-fixes/kurama'
out.mkdir(parents=True,exist_ok=True)
backup=out/'before.air'
if not backup.exists():backup.write_bytes(air.read_bytes())
raw=backup.read_bytes().decode('cp1252')
# Naruto's root scale was reduced from 0.7 to 0.18. This AIR multiplier
# preserves Kurama's approved on-screen size: 5.83333333333 * .18 = 1.5 * .7.
factor=5.83333333333
count=0
actions=[]
frame=re.compile(r'^\s*(\d+)\s*,\s*(\d+)\s*,')

def convert(block):
    global count
    if not re.search(r'^\s*2300\s*,',block,re.M):return block
    actions.append(int(re.search(r'Begin Action\s+(\d+)',block,re.I)[1]))
    defaults={1:[],2:[]};pending={};result=[];current=None
    for line in block.splitlines():
        header=re.match(r'\s*Clsn([12])(Default)?\s*:\s*(\d+)',line,re.I)
        box=re.match(r'\s*Clsn([12])\[\d+\]\s*=\s*([^;]+)',line,re.I)
        if header:
            kind=int(header[1]);current=[]
            if header[2]:defaults[kind]=current
            else:pending[kind]=current
            continue
        if box:
            assert current is not None,line
            current.append([int(v.strip()) for v in box[2].split(',')]);continue
        match=frame.match(line)
        if match:
            giant=int(match[1])==2300
            # Explicit boxes preserve defaults and one-frame overrides in mixed actions.
            for kind in (1,2):
                boxes=pending.get(kind,defaults[kind]);result.append(f'Clsn{kind}: {len(boxes)}')
                for i,coords in enumerate(boxes):
                    values=[round(v*factor) if giant else v for v in coords]
                    result.append(f'Clsn{kind}[{i}] = '+', '.join(map(str,values)))
            pending.clear()
            if giant:
                parts=line.split(';',1);fields=parts[0].split(',')
                while len(fields)<9:fields.append('')
                for i in (2,3):fields[i]=str(round(float(fields[i])*factor))
                for i in (7,8):fields[i]=format((float(fields[i]) if fields[i].strip() else 1)*factor,'.12g')
                line=','.join(fields)+(' ;'+parts[1] if len(parts)>1 else '')
                count+=1
        result.append(line)
    return '\r\n'.join(result)+'\r\n'

blocks=re.split(r'(?=\[Begin Action\s)',raw,flags=re.I)
updated=''.join(convert(b) for b in blocks).encode('cp1252')
assert count>0
old_frames=[m.group(0).split(';')[0].split(',') for m in re.finditer(r'^\s*\d+\s*,\s*\d+\s*,[^\r\n]*',raw,re.M)]
new_frames=[m.group(0).split(';')[0].split(',') for m in re.finditer(r'^\s*\d+\s*,\s*\d+\s*,[^\r\n]*',updated.decode('cp1252'),re.M)]
assert len(old_frames)==len(new_frames)
for old,new in zip(old_frames,new_frames):
    original=list(old)
    while len(old)<9:old.append('')
    while len(new)<9:new.append('')
    assert [v.strip() for v in old[:2]+old[4:7]]==[v.strip() for v in new[:2]+new[4:7]]
    if int(old[0])!=2300:assert old==new
air.write_bytes(updated)
(out/'approved.air').write_bytes(updated)
report=dict(multiplier=factor,effective_screen_multiplier=1.5,player_scale=0.18,sprite_group=2300,frames=count,actions=actions,collision_geometry='Scaled per Kurama frame; other bodies unchanged',before_sha256=hashlib.sha256(backup.read_bytes()).hexdigest(),installed_sha256=hashlib.sha256(updated).hexdigest(),recording=False)
(out/'installation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
