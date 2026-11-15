"""Build a standalone, fully illustrated Baam with documented engine foundation."""
from baam_model import *
from edward_assets import write_v2
from isolated_sprite_atlas import extract
from fighter_assets import FighterAssets
from PIL import Image
import re,hashlib,shutil
import numpy as np
from baam_combat_v3 import combat_actions,write_combat_sound,ULTIMATE_BASE,ULTIMATE_VIOLE,ULTIMATE_TICKS
from baam_vfx import effect_tiles

ART=S/'art/canonical-v2';O=E/'chars/baam_build';O.mkdir(parents=True,exist_ok=True)
COMBAT=S/'art/combat-v3'
source=S/'source/engine-foundation';source.mkdir(parents=True,exist_ok=True)
foundation=[E/'chars/kfm/kfm.cns',E/'chars/kfm/kfm.air',E/'chars/kfm/readme.txt',E/'data/common1.cns.zss']
for p in foundation:shutil.copy2(p,source/p.name)
(S/'source/source-report.json').write_text(json.dumps(dict(kind='custom adaptation',upstream_baam_release=None,reason='No verifiable public Baam MUGEN archive found; gameplay is authored for this project.',foundation={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in foundation},identity_sources=['https://tog-anime.com/1st/character/','https://tog-anime.com/chara/','https://www.webtoons.com/en/fantasy/tower-of-god/list?title_no=95'],credits='Tower of God / SIU; common movement foundation Elecbyte and IKEMEN GO contributors; original fan adaptation and built-in generated artwork.'),indent=2))

import sys
if '--reuse-art' not in sys.argv:
    sprites=[];registration=[]
    for g,slug in [(62000,'movement'),(62001,'combat'),(62100,'ignited-movement'),(62101,'ignited-combat'),(62200,'story-spaced'),(62300,'transition-spaced'),(62400,'techniques'),(62500,'viole-techniques'),(62600,'ultimate')]:
        folder=COMBAT if g>=62400 else ART
        tiles=extract(folder/(slug+'.png'),4,2 if g==62300 else 4)
        factor=424/tiles[0][0].height
        for i,(im,bounds) in enumerate(tiles):
            # The atlas victory cells are knee-up. Keep complete silhouettes in
            # the game by using each form's full-body neutral for victory.
            if g in (62000,62100) and i==15:im=tiles[0][0].copy()
            f=424/im.height if g==62300 else 424/tiles[8][0].height if g==62600 and i>=8 else factor
            im=im.resize((round(im.width*f),round(im.height*f)),Image.Resampling.LANCZOS)
            anchor={2:.34,4:.45,6:.37,9:.36,10:.38,12:.34,13:.35,14:.34,15:.38}.get(i,.5) if g in (62001,62101) else {5:.38,6:.38,7:.32,9:.38,10:.38,11:.32,12:.35,13:.36}.get(i,.5) if g==62200 else .5
            axis=(round(im.width*anchor),im.height)
            if g in (62400,62500):axis=(round(im.width*{2:.34,5:.34,7:.43,9:.34,11:.38,12:.43,13:.4,15:.38}.get(i,.5)),im.height)
            if g==62600:axis=(round(im.width*{4:.42,5:.34,6:.38}.get(i%8,.5)),im.height)
            sprites.append(dict(key=(g,i),axis=axis,image=im))
            poses=folder/'poses';poses.mkdir(exist_ok=True);im.save(poses/f'{slug}-{i}.png')
            registration.append(dict(group=g,pose=i,bounds=bounds,size=im.size,axis=axis,scale=f))
    # FX are centered transparent tiles, rather than cropped to an off-center trail.
    im=Image.open(ART/'effects.png').convert('RGBA')
    for i in range(16):
        x=i%4;y=i//4;tile=im.crop((x*im.width//4,y*im.height//4,(x+1)*im.width//4,(y+1)*im.height//4))
        if i==15:
            # The Thorn's tip extends above the assumed row boundary. Extract its
            # whole red prop rather than slicing it at a synthetic grid line.
            pixels=np.array(im);yy,xx=np.indices(pixels.shape[:2])
            mask=(xx>im.width*.75)&(yy>im.height*.65)&(pixels[:,:,3]>180)&(pixels[:,:,0]>pixels[:,:,1].astype(float)*1.5)&(pixels[:,:,0]>pixels[:,:,2].astype(float)*1.5)
            py,px=np.where(mask);assert len(px)>100
            tile=im.crop((max(0,int(px.min())-16),max(0,int(py.min())-16),min(im.width,int(px.max())+17),min(im.height,int(py.max())+17)))
        sprites.append(dict(key=(63000,i),axis=(tile.width//2,tile.height//2),image=tile))
    for i,(tile,axis) in enumerate(effect_tiles(COMBAT/'effects.png')):
        tile.save(COMBAT/'poses'/f'effect-{i}.png')
        sprites.append(dict(key=(63100,i),axis=axis,image=tile))
    portrait=Image.open(ART/'portrait.png').convert('RGBA')
    for i,size in [(0,(200,200)),(1,(960,1120))]:
        copy=portrait.copy();copy.thumbnail(size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',size);canvas.alpha_composite(copy,((size[0]-copy.width)//2,0));sprites.append(dict(key=(9000,i),axis=(0,0),image=canvas))
    write_v2(O/'baam.sff',sprites)
    (S/'pose-registration.json').write_text(json.dumps(registration,indent=2))
else:
    assert (O/'baam.sff').exists()
    sprites=[None]*170

a=Author();act=a.action
act(0,[(62000,0,8),(62000,1,8)]);act(5,[(62000,0,4)])
for n,p,t in [(6,4,6),(10,4,4),(11,4,-1),(12,0,4),(40,4,3),(41,6,-1),(42,6,-1),(43,7,-1),(47,4,3),(52,4,5),(100,5,24),(105,5,20),(170,13,-1),(181,15,-1)]:act(n,[(62000,p,t)])
for n,poses in [(20,[2,3]),(21,[3,2])]:act(n,[(62000,p,8) for p in poses])
for n in range(120,156):act(n,[(62000,9 if n in (121,131,141,152,153) else 8,6)])
for n in [5000,5001,5002,5010,5011,5012,5020,5030,5040,5050,5060,5070,5080,5090]:act(n,[(62000,12 if n>=5030 else 10 if n%10==0 else 11,-1)])
for n in [5100,5110,5140,5150,5160,5170]:act(n,[(62000,13,6 if n in (5100,5160) else -1)],hurt=n!=5110)
act(5120,[(62000,13,8),(62000,14,8),(62000,0,5)])
for n in [5200,5210,5220,5300,5500,5510]:act(n,[(62000,14,6),(62000,0,6)])
act(190,[(62200,0,12),(62200,1,18),(62200,2,18),(62200,3,18),(62000,0,6)])
for n,(damage,start,duration,poses) in NORMALS.items():
    k='A' if n>=600 else 'C' if n>=400 else 'S'
    act(n,[(62001,poses[0],start),(62001,poses[1],5),(62001,poses[2],5),(62000,7 if k=='A' else 4 if k=='C' else 0,duration-start-10)],active=(1,),kind=k,box=(6,-24,54,0) if k=='C' else (8,-48,60,-8))
for n,frames,active,box in [
    (1000,[(8,14),(9,6),(15,8)],(1,),(8,-44,65,-10)),
    (1100,[(8,12),(9,6),(15,12)],(1,),(8,-44,65,-10)),
    (1200,[(11,32),(0,10)],(0,),(-11,-52,38,0)),
    (1201,[(11,6),(9,8),(0,10)],(),(0,0,0,0)),
    (1300,[(8,16),(10,8),(15,12)],(),(0,0,0,0)),
    (2000,[(8,12),(9,6),(8,6),(9,6),(8,6),(9,6),(15,14)],(1,3,5),(8,-45,76,-8)),
    (2100,[(11,32),(0,12)],(0,),(-11,-52,38,0)),
    (2101,[(11,8),(15,12)],(),(0,0,0,0)),
    (2200,[(8,20),(9,6),(8,8),(9,6),(15,14)],(1,3),(8,-46,88,-7)),
]:act(n,[(62001,p,t) for p,t in frames],active=active,box=box)
act(700,[(62001,8,8),(62001,10,8)])
act(900,[(62000,4,8),(62000,5,10),(62000,0,6)])
act(3000,[(62200,4,12),(62200,5,12),(62200,6,8),(62200,7,10)],active=(2,),box=(8,-47,76,-6))
act(3001,[(62200,5,12),(62200,6,14),(62200,7,10),(62200,5,10),(62200,6,14),(62200,7,12),(62200,4,12),(62000,0,14)])
for n,poses in [(800,range(8)),(801,range(7,-1,-1))]:act(n,[(62100 if n==801 else 62000,0,8)]+[(62300,p,10) for p in poses]+[(62000 if n==801 else 62100,0,10)])
for i in range(16):
    # Raw FX dimensions are scaled by the spawning controller, never by body scale.
    a.animations[9000+i]=f'\n[Begin Action {9000+i}]\n63000,{i},0,0,-1\n'
a.animations[9010]='\n[Begin Action 9010]\nClsn1Default: 1\nClsn1[0]=-5,-5,5,5\n63000,1,0,0,-1\n'
a.animations[9090]='\n[Begin Action 9090]\n63000,15,0,0,-1\n'
combat_actions(a)
bank={}
for n,text in a.animations.items():
    if n>=8000 or n in (800,801):continue
    text=text.replace(f'[Begin Action {n}]',f'[Begin Action {n+1000000}]')
    def replace(m):
        g,p=int(m[1]),int(m[2]);return f'{g+100 if g in (62000,62001,62400) else g},{p+8 if g==62600 else p+4 if g==62200 and 4<=p<=7 else p},'
    bank[n+1000000]=re.sub(r'^(62000|62001|62200|62400|62600),(\d+),',replace,text,flags=re.M)
(O/'baam.air').write_text(''.join((a.animations|bank).values()))
author_moves(a)
for n,vel in [(100,4),(105,-3)]:
    a.state(n,n,physics='N',velset=f'{vel},0');a.ctl(n,'Dash recovery','ChangeState','time>=18',value=0,ctrl=1)
constants=(source/'kfm.cns').read_text(encoding='utf-8-sig').split('[Statedef 170]')[0]
constants=constants.split(';Default language victory quotes')[0]
for key,value in [('ground.back','10'),('ground.front','11'),('air.back','10'),('air.front','10'),('height','53'),('head.pos','0,-45'),('mid.pos','0,-27'),('walk.fwd','1.5'),('walk.back','-1.2'),('jump.neu','0,-5.2'),('jump.fwd','1.6,-5.2'),('jump.back','-1.5,-5.2'),('run.fwd','3.2,0'),('run.back','-2.7,-3.2'),('yaccel','.36')]:constants=re.sub(r'(?im)^'+re.escape(key)+r'\s*=.*$',key+'='+value,constants)
constants+='\n[Quotes]\nvictory1="I will protect what is precious to me."\n'
(O/'baam.cns').write_text(constants+a.cns,encoding='utf-8')
(O/'baam.cmd').write_text(author_commands())
common=(source/'common1.cns.zss').read_text(encoding='utf-8-sig')
common=common.replace('IkSys_GuardShaking(anim)','IkSys_GuardShaking(local_anim)').replace('$anim','$local_anim')
common=re.sub(r'\banim\b(?!\s*:)',r'(anim%1000000)',common)
common=re.sub(r'(\[StateDef[^\n]*?\banim:)\s*([^;\n}]+)',lambda m:m[1]+' ('+m[2].strip()+')+1000000*map(baam.form)',common,flags=re.I)
common=re.sub(r'(changeAnim\s*\{\s*value:\s*)([^;\n}]+)',lambda m:m[1]+'('+m[2].strip()+')+1000000*map(baam.form)',common)
common=common.replace('[StateDef 5900; type: S;]', '[StateDef 5900; type: S;]\nmapSet{map: "baam.form"; value: 1}')
(O/'baam-common.zss').write_text(common,encoding='utf-8')
(O/'baam.def').write_text('[Info]\nname="Baam"\ndisplayname="Baam"\nauthor="Game1 custom Tower of God adaptation"\nmugenversion=1.1\nlocalcoord=192,144\nportraitscale=.125\n[Files]\ncmd=baam.cmd\ncns=baam.cns\nst=baam.cns\nstcommon=baam-common.zss\nsprite=baam.sff\nanim=baam.air\nsound=baam.snd\n',encoding='utf-8')
with (O/'baam.def').open('a', encoding='utf-8') as definition:
    definition.write('\n[Map]\nbaam.form = 1\n')
# Original synthesized tones; no unrelated fighter's character voice.
write_combat_sound(O/'baam.snd')
runtime={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.suffix in ('.def','.cns','.cmd','.zss','.air','.snd','.sff')}
(S/'build-report.json').write_text(json.dumps(dict(revision='combat-v3',kind='custom adaptation',runtime_sha256=runtime,body_height=424,forms=['Baam','Jue Viole Grace'],body_drawings=134,registered_body_sprites=136,transition_frames=8,transition_ticks=98,ultimate_ticks=ULTIMATE_TICKS,ultimate_damage=[ULTIMATE_BASE,ULTIMATE_VIOLE],moves=MOVES,source='source/source-report.json',limitations=['Authored Baam gameplay, not an imported third-party Baam release.','Key-pose animation; some common reaction and movement frames share drawings.','Two playable appearances, not every canonical power-up or outfit.']),indent=2))
installed=E/'chars/baam';installed.mkdir(exist_ok=True)
for p in O.iterdir():
    if p.name in runtime:shutil.copy2(p,installed/p.name)
select=E/'data/select.def';text=select.read_text(encoding='utf-8')
if not re.search(r'^baam\s*,',text,re.M):select.write_text(text.replace('[Characters]','[Characters]\nbaam, stages/stage0-720.def, order=1',1),encoding='utf-8')
print('BAAM_BUILT',len(sprites),'sprites;',len(a.animations)+len(bank),'actions')
