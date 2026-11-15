"""Install the creator's Cid package as a reproducible, isolated reference.

Original files remain byte-identical under characters/cid/source/upstream.
The playable adapter swaps Atomic/teleport buttons to match our A/S/D layout.
"""
from pathlib import Path
import hashlib,json,re,shutil,struct,sys

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sprite-fighter/characters/cid'
UPSTREAM=SOURCE/'source/upstream/.Cid'
ENGINE=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
OUT=ENGINE/'chars/cid_shadow';OUT.mkdir(parents=True,exist_ok=True)

originals={}
for path in UPSTREAM.iterdir():
    if path.suffix.lower() not in {'.def','.cns','.cmd','.air','.sff','.snd','.txt'}:continue
    originals[path.name]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.suffix.lower()!='.def':shutil.copy2(path,OUT/path.name)

definition=(UPSTREAM/'.Cid.def').read_text(encoding='utf-8-sig')
definition=definition.replace('[Files]','localcoord = 320,240\n\n[Files]')
(OUT/'cid_shadow.def').write_text(definition,encoding='utf-8')
command=(UPSTREAM/'Cid.cmd').read_bytes()
command=re.sub(rb'(?im)^x\s*=\s*x\s*\r?$',b'x = z',command,count=1)
command=re.sub(rb'(?im)^z\s*=\s*z\s*\r?$',b'z = x',command,count=1)
(OUT/'Cid.cmd').write_bytes(command)
air=(UPSTREAM/'Cid.air').read_text(encoding='utf-8-sig',errors='replace')
actions={};duplicates=[]
for block in re.split(r'(?=\[Begin Action\s+)',air,flags=re.I):
    header=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
    if not header:continue
    n=int(header[1]);rows=[]
    for line in block.splitlines():
        if re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',line):
            fields=[p.strip() for p in line.split(';',1)[0].split(',')]
            if len(fields)>=5:rows.append(fields)
    if n in actions:duplicates.append(n);continue
    actions[n]={'frames':len(rows),'unique_sprites':len({tuple(row[:2]) for row in rows}),'ticks':sum(int(row[4]) for row in rows if re.fullmatch(r'-?\d+',row[4]))}
states={}
for path in UPSTREAM.glob('*.cns'):
    states[path.name]=[int(n) for n in re.findall(r'(?im)^\[statedef\s+(-?\d+)\]',path.read_text(encoding='utf-8-sig',errors='replace'))]
sff=(UPSTREAM/'Cid.sff').read_bytes()
assert sff.startswith(b'ElecbyteSpr\x00')
sprite_count=struct.unpack_from('<I',sff,40 if sff[15]==2 else 20)[0]
report={'status':'Installed; native verification pending','slug':'cid_shadow','display_name':'Cid Kagenou / Shadow',
 'creator':'RyoumenS','upstream_credits':['UNKNOWN XD','QINYAN','RyoumenS'],
 'source':json.loads((SOURCE/'source/source-report.json').read_text()),
 'localcoord':[320,240],'sff_version':list(sff[12:16]),'sprite_count':sprite_count,
 'actions':actions,'duplicate_upstream_actions':duplicates,'state_files':states,
 'original_files':originals,'adapters':['Explicit default 320x240 local coordinates','Atomic on D/Y; teleport on A/R through x/z input remap'],
 'movement_actions':{str(n):actions.get(n) for n in [0,10,20,21,40,41,42,43,45,50,52,60,61,70]},
 'preserved_roster':['prince','tyrone','will_full','urkel','jinwoo','yamal']}
(SOURCE/'port-report.json').write_text(json.dumps(report,indent=2))
print('CID_REFERENCE_INSTALLED',sprite_count,'sprites;',len(actions),'actions;',sum(len(v) for v in states.values()),'state definitions')
if '--reference-only' not in sys.argv and (SOURCE/'art/illustrated-v1/cinematic.png').exists():
    import cid_illustrated
    cid_illustrated.install(ROOT,OUT)
