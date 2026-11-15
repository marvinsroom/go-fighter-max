"""Compile character-specific illustrated art and authored IKEMEN gameplay."""
from manhwa_fighters import *
from isolated_sprite_atlas import extract
from baam_vfx import effect_tiles
from baam_combat_v3 import write_combat_sound
from edward_assets import write_v2
from PIL import Image
import sys,shutil,re,hashlib

p=profile(sys.argv[1]);S=p['folder'];ART=S/'art/illustrated-v1';O=E/'chars'/(p['id']+'_build');O.mkdir(parents=True,exist_ok=True)
source=S/'source/engine-foundation';source.mkdir(parents=True,exist_ok=True)
foundation=[E/'chars/kfm/kfm.cns',E/'chars/kfm/kfm.air',E/'chars/kfm/readme.txt',E/'data/common1.cns.zss']
for file in foundation:shutil.copy2(file,source/file.name)
(S/'source/source-report.json').write_text(json.dumps(dict(kind='custom adaptation',upstream_character_release=None,reason='No usable verifiable MUGEN release found. Gameplay and illustrated assets authored for this roster.',identity_sources=[p['source']],reference_details='art/illustrated-v1/references/',foundation={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in foundation},credits=p['credits']+'; common movement foundation Elecbyte and IKEMEN GO contributors; built-in imagegen artwork.'),indent=2))
sprites=[];registrations=[];body_drawings=0
for group,slug in [(62000,'movement'),(62400,'combat'),(62600,'story')]:
    layout=p.get('art_layouts',{}).get(slug,{})
    source_tiles=extract(ART/(slug+'.png'),layout.get('columns',4),layout.get('rows',4))
    body_drawings+=len(source_tiles)-(1 if slug=='movement' else 0)
    tiles=[source_tiles[i] for i in layout.get('pose_map',range(len(source_tiles)))]
    assert len(tiles)==16
    factor=424/tiles[0][0].height
    for i,(im,bounds) in enumerate(tiles):
        if group==62000 and i==15:im=tiles[0][0].copy()
        f=424/tiles[4][0].height if group==62600 and 4<=i<=11 else factor
        im=im.resize((round(im.width*f),round(im.height*f)),Image.Resampling.LANCZOS)
        anchor={2:.34,4:.38,6:.40,7:.38,9:.34,10:.38,12:.35,13:.40,14:.35,15:.4}.get(i,.5) if group==62400 else {8:.42,9:.34,10:.38}.get(i,.5) if group==62600 else .5
        axis=(round(im.width*anchor),im.height)
        (ART/'poses').mkdir(exist_ok=True);im.save(ART/'poses'/f'{slug}-{i}.png')
        sprites.append(dict(key=(group,i),axis=axis,image=im));registrations.append(dict(group=group,pose=i,bounds=bounds,size=im.size,axis=axis,scale=f))
registration_path=S/'art/comic-style-v4/native-registration.json'
effect_registration=json.loads(registration_path.read_text()).get('effects',{}) if registration_path.exists() else {}
for i,(tile,axis) in enumerate(effect_tiles(ART/'effects.png')):
    if str(i) in effect_registration:
        # Native presentation registration only: retain source artwork and all
        # AIR/CNS timing, position, scale, hitboxes and commands byte-identically.
        spec=effect_registration[str(i)];bounds=tile.getchannel('A').getbbox()
        factor=spec['visible_width']/(bounds[2]-bounds[0])
        tile=tile.resize((round(tile.width*factor),round(tile.height*factor)),Image.Resampling.LANCZOS)
        bounds=tile.getchannel('A').getbbox()
        axis=(round((bounds[0]+bounds[2])/2-(spec['center_x']-spec['spawn_x'])/spec['scale_x']),
              round(bounds[3]-(spec['feet_y']-spec['spawn_y'])/spec['scale_y']))
    tile.save(ART/'poses'/f'effect-{i}.png');sprites.append(dict(key=(63100,i),axis=axis,image=tile))
portrait=Image.open(ART/'portrait.png').convert('RGBA')
for i,size in [(0,(200,200)),(1,(960,1120))]:
    copy=portrait.copy();copy.thumbnail(size,Image.Resampling.LANCZOS);canvas=Image.new('RGBA',size);canvas.alpha_composite(copy,((size[0]-copy.width)//2,0));sprites.append(dict(key=(9000,i),axis=(0,0),image=canvas))
write_v2(O/(p['id']+'.sff'),sprites)
(S/'pose-registration.json').write_text(json.dumps(registrations,indent=2))
a=Author();animations(a);core(a,p)
constants=(source/'kfm.cns').read_text(encoding='utf-8-sig').split('[Statedef 170]')[0].split(';Default language victory quotes')[0]
for key,value in [('ground.back','10'),('ground.front','11'),('air.back','10'),('air.front','10'),('height','53'),('head.pos','0,-45'),('mid.pos','0,-27'),('walk.fwd','1.5'),('walk.back','-1.2'),('jump.neu','0,-5.2'),('jump.fwd','1.6,-5.2'),('jump.back','-1.5,-5.2'),('run.fwd','3.2,0'),('run.back','-2.7,-3.2'),('yaccel','.36')]:constants=re.sub(r'(?im)^'+re.escape(key)+r'\s*=.*$',key+'='+value,constants)
stature=ROOT/'sprite-fighter/face-audit/identity-scale-v5/profiles.json'
if stature.exists():
    selected=next((row for row in json.loads(stature.read_text())['fighters'] if row['slug']==p['slug']),{})
    if selected.get('native_scale'):
        for key,value in zip(('xscale','yscale'),selected['native_scale']):constants=re.sub(r'(?im)^'+key+r'\s*=\s*[-+0-9.eE]+',key+'='+format(value,'.10g'),constants,count=1)
cns=constants+'\n[Quotes]\nvictory1="'+p.get('quote',('Work complete. Send the invoice.' if p['slug']=='lloyd' else 'I will carry the Northern Sect forward.'))+'"\n'+a.cns
if p['slug']=='lloyd':cns=cns.replace('palbright=0,15,35','palbright=35,20,0').replace('palcontrast=140,200,230','palcontrast=230,190,120')
(O/(p['id']+'.cns')).write_text(cns,encoding='utf-8');(O/(p['id']+'.cmd')).write_text(commands(p),encoding='utf-8')
(O/(p['id']+'.air')).write_text(''.join(a.animations.values()),encoding='utf-8')
(O/(p['id']+'-common.zss')).write_text((source/'common1.cns.zss').read_text(encoding='utf-8-sig'),encoding='utf-8')
(O/(p['id']+'.def')).write_text(f'[Info]\nname="{p["name"]}"\ndisplayname="{p["name"]}"\nauthor="Game1 custom illustrated adaptation"\nmugenversion=1.1\nlocalcoord=192,144\nportraitscale=.125\n[Files]\ncmd={p["id"]}.cmd\ncns={p["id"]}.cns\nst={p["id"]}.cns\nstcommon={p["id"]}-common.zss\nsprite={p["id"]}.sff\nanim={p["id"]}.air\nsound={p["id"]}.snd\n',encoding='utf-8')
write_combat_sound(O/(p['id']+'.snd'))
runtime={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in O.iterdir() if f.suffix in ('.def','.cns','.cmd','.zss','.air','.snd','.sff')}
installed=E/'chars'/p['id'];installed.mkdir(exist_ok=True)
for name in runtime:shutil.copy2(O/name,installed/name)
(S/'build-report.json').write_text(json.dumps(dict(revision=('manhwa-faces-v2' if (S/'art/manhwa-faces-v2').exists() else 'illustrated-v1'),kind='custom adaptation',name=p['name'],runtime_sha256=runtime,body_height=424,body_drawings=body_drawings,registered_body_sprites=48,sprites=len(sprites),actions=len(a.animations),moves=p['movespec'],ultimate_damage=p['ultimate'],ultimate_ticks=164,taunt=p['taunt'],limitations=['Custom gameplay; no third-party character release claimed.','Illustrated key poses, with shared movement/reaction drawings.','One canonical appearance; W is a personality action, not an invented story transformation.']),indent=2))
select=E/'data/select.def';text=select.read_text(encoding='utf-8')
if not re.search('^'+p['id']+r'\s*,',text,re.M):select.write_text(text.replace('[Characters]','[Characters]\n'+p['id']+', stages/stage0-720.def, order=1',1),encoding='utf-8')
print('MANHWA_BUILT',p['name'],len(sprites),'sprites',len(a.animations),'actions')
