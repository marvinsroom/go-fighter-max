"""Rebuild illustrated Rimuru over the preserved SoulFire combat package."""
from pathlib import Path
import io,json,hashlib,re,shutil,struct,statistics
from PIL import Image,ImageOps
import numpy as np
from scipy import ndimage
from rimuru_source import ROOT,SOURCE,UP,sprites
from jinwoo_motion import atlas_rects
from mugen_sff import Sff

E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0';OUT=E/'chars/rimuru';OUT.mkdir(exist_ok=True)
ART=SOURCE/'art/illustrated-v1'

def entry(im,axis):
    buf=io.BytesIO();im.save(buf,format='PNG');return dict(image=im,png=buf.getvalue(),axis=axis,rgba_sha256=hashlib.sha256(im.tobytes()).hexdigest())

def source_container():
    cache=SOURCE/'source/converted-v2.sff'
    if cache.exists():return cache
    rows=sprites();headers=[];payload=bytearray();seen={}
    for i,r in enumerate(rows):
        im=r['image'];w,h=im.size;key=hashlib.sha256(im.tobytes()).digest()
        if key in seen:offset=length=0;link=seen[key]
        else:
            f=entry(im,r['axis']);block=struct.pack('<I',w*h*4)+f['png'];offset=len(payload);length=len(block);payload.extend(block);link=0;seen[key]=i
        headers.append(struct.pack('<HHHHhhHBBIIHH',r['group'],r['number'],w,h,*r['axis'],link,12,32,offset,length,0,0))
    head=bytearray(512);head[:12]=b'ElecbyteSpr\0';head[12:16]=bytes((0,0,1,2));start=512+28*len(headers)
    struct.pack_into('<IIIIIIII',head,36,512,len(headers),start,0,start,len(payload),start+len(payload),0)
    cache.write_bytes(head+b''.join(headers)+payload);return cache

def art():
    result={};sheets={}
    for name,rows,reference in [('movement',4,[0,1,2,3]),('combat',4,[0,3,15]),('intro',2,[4,5,6,7])]:
        im=Image.open(ART/(name+'.png')).convert('RGBA');rects=atlas_rects(im,4,rows);tiles=[im.crop(r) for r in rects];bounds=[]
        for tile in tiles:
            labels,_=ndimage.label(np.array(tile.getchannel('A'))>48);areas=np.bincount(labels.ravel());areas[0]=0
            yy,xx=ndimage.find_objects(labels)[areas.argmax()-1];bounds.append((xx.start,yy.start,xx.stop,yy.stop))
        scale=50/statistics.median(bounds[i][3]-bounds[i][1] for i in reference)
        for i,(tile,b,rect) in enumerate(zip(tiles,bounds,rects)):
            # Exclude disconnected neighboring weapon tips outside the main
            # figure's rectangle; do not resample or repaint generated pixels.
            tile=tile.crop(b);axis=(tile.width//2,tile.height)
            rect=(rect[0]+b[0],rect[1]+b[1],rect[0]+b[2],rect[1]+b[3])
            f=entry(tile,axis);f.update(scale=scale,bounds=b,rect=rect,source=name);result[f'{name}:{i}']=f
        sheets[name]=dict(scale=scale,cells=len(tiles),size=im.size)
    return result,sheets

def pose(g,n):
    m=lambda i:f'movement:{i}';c=lambda i:f'combat:{i}'
    if g==9000:return m(0)
    if g==17000:return c(10)
    if g>=6000:return None
    if g==0:return m(n%4)
    if g==20:return m(4+n%4)
    if g==6:return m(8)
    if g in (120,121,122):return m(8 if g==121 else 9)
    if g in (40,100,400,404):return m(10 if g==40 else 12)
    if 5000<=g:return m(15 if g in (5040,5041,5042,5120) else 14)
    if g in (180,181,190,191):return c(15)
    if g in (1400,1500):return c(10)
    if g==1100:return c(9)
    if g==1200:return c(8)
    if g in (4500,4501,4502):return c([0,1,11,10,9,11,10,15][min(n,7)])
    if g==500:return c(9)
    if g in (600,610,620,640,660):return c(12+n%3)
    if g==340:return c(7)
    if g==250:return c(8+n%4)
    if g in (200,210,220,230):return c([0,1,2,3,4,5,6][n%7])
    return c(n%8)

def build():
    cache=source_container();drawings,sheets=art();source=Sff(cache);replacements={};metadata={}
    for g,n in source.keys:
        key=pose(g,n)
        if key:
            f=drawings[key];replacements[g,n]=f;metadata[f'{g},{n}']=dict(pose=key,scale=f['scale'],axis=f['axis'])
    # Proper large and small illustrated portraits; original cut-in also replaced.
    portrait=drawings['movement:0']['image']
    for n,size in [(0,(224,200)),(1,(640,800))]:
        crop=portrait.crop((0,0,portrait.width,round(portrait.height*.48))) if n==0 else portrait
        im=Image.new('RGBA',size);fit=ImageOps.contain(crop,size);im.alpha_composite(fit,((size[0]-fit.width)//2,0));replacements[9000,n]=entry(im,(0,0))
    additions={(7900,i):drawings[f'intro:{i}'] for i in range(8)}
    (OUT/'Rimuru Demon Lord.sff').write_bytes(source.derive(replacements,additions))
    for p in UP.iterdir():
        if p.suffix.lower() in ('.cns','.cmd','.snd','.act'):shutil.copy2(p,OUT/p.name)
    for original in UP.glob('*.cns'):
        p=OUT/original.name
        t=original.read_text(encoding='cp1252',errors='replace')
        if p.name=='Rimuru Demon Lord.cns':
            t=re.sub(r'(?im)^(xscale|yscale)\s*=\s*1.05\s*$',lambda m:m[1]+' = 1.65',t)
            t=re.sub(r'(?is)\[statedef\s+190\].*?(?=\[statedef)',intro_state()+'\n',t,count=1)
        p.write_text(t,encoding='utf-8')
    definition=(UP/'Rimuru Demon Lord.def').read_text(encoding='cp1252').replace('[Files]','localcoord = 320,240\nportraitscale = 0.125\n\n[Files]').replace('displayname ="Rimuru Demon Lord"','displayname ="Rimuru Tempest"')
    (OUT/'rimuru.def').write_text(definition,encoding='utf-8')
    air=(UP/'Rimuru Demon Lord.air').read_text(encoding='cp1252',errors='replace');lines=[]
    for line in air.splitlines():
        if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
            parts=line.split(';')[0].split(',');key=','.join(str(int(x.strip())) for x in parts[:2]);meta=metadata.get(key)
            if meta:
                while len(parts)<9:parts.append('')
                parts[7]=parts[8]=str(meta['scale']);line=','.join(parts)
        lines.append(line)
    air='\n'.join(lines)+'\n\n[Begin Action 7900]\n'
    for i,ticks in enumerate([18,10,10,10,10,10,10,18]):
        s=drawings[f'intro:{i}']['scale'];air+=f'7900,{i},0,0,{ticks},,,{s},{s}\n'
    (OUT/'Rimuru Demon Lord.air').write_text(air,encoding='utf-8')
    cmd=(OUT/'Rimuru Demon Lord.cmd').read_text(encoding='cp1252',errors='replace')
    # Physical A/S/D are logical x/y/z; preserve the creator's full motions too.
    extra='[Command]\nname="rimuru_hell"\ncommand=~y\ntime=15\n[Command]\nname="rimuru_lightning"\ncommand=/$D,~y\ntime=15\n[Command]\nname="rimuru_flare"\ncommand=~x\ntime=15\n'
    cmd=cmd.replace('[Statedef -1]',extra+'\n[Statedef -1]\n'+route('rimuru_lightning',1400,2000)+route('rimuru_hell',1100,1000)+route('rimuru_flare',1000,1000),1)
    cmd=cmd.replace('command = ~x','command = ~z',1)
    (OUT/'Rimuru Demon Lord.cmd').write_text(cmd,encoding='utf-8')
    from rimuru_complete import install as complete
    complete(OUT,drawings)
    report=dict(status='Built; native validation pending',creator='SoulFire',display_scale=1.65,sheets=sheets,sprites=metadata,source_sha256=hashlib.sha256((UP/'Rimuru Demon Lord.sff').read_bytes()).hexdigest(),runtime_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.suffix in ('.def','.air','.cns','.cmd','.sff') and not p.name.startswith(('test-','rimuru_test'))})
    (SOURCE/'build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('RIMURU_BUILT',len(metadata),'body sprites')
    if (SOURCE/'art/forms-v3/slime-walk.png').exists():
        from rimuru_forms import install as form_movesets
        form_movesets(OUT)
        if (SOURCE/'art/forms-v3/clean-casters.png').exists():
            from rimuru_casting import install as clean_casting
            clean_casting(OUT)
            if (SOURCE/'art/ultimates-v5/cinematics.png').exists():
                from rimuru_cinematics import install as cinematic_ultimates
                cinematic_ultimates(OUT)

def route(command,state,meter):
    return f'[State -1, Illustrated quick command]\ntype=ChangeState\ntriggerall=command="{command}"\ntriggerall=power>={meter}\ntriggerall=statetype!=A\ntrigger1=ctrl\nvalue={state}\n'

def intro_state():
    return '''[Statedef 190]
type=S
movetype=I
physics=N
anim=7900
ctrl=0
velset=0,0
[State 190, Transformation]
type=AssertSpecial
trigger1=1
flag=intro
[State 190, Ground]
type=PosSet
trigger1=1
y=0
[State 190, Voice]
type=PlaySnd
trigger1=time=48
value=S0,15
[State 190, Ready]
type=ChangeState
trigger1=animtime=0
value=0
ctrl=1
'''

if __name__=='__main__':build()
