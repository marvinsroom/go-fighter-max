"""Manhwa-inspired guest assists and Academy Anubis archery.

Attack names, costs and balance are authored game mechanics. Reference images
are retained separately and never compiled into the sprite archive.
"""
from pathlib import Path
import json,hashlib
from PIL import Image
from isolated_sprite_atlas import extract

NAMES=['Dolores','Camu','Aiyen','Sinclair']
STATES=[2000,2010,2020,2030]
COSTS=[1250,1250,1000,1250]

def load_art(A,axis,clips):
    art=A.source/'art/guests-v1'
    if not (art/'ready.json').exists():return False
    layout=json.loads((art/'ready.json').read_text())
    (art/'poses').mkdir(exist_ok=True)
    for name,prefix,group,height in [('anubis','bo',57,375),('dolores','do',70,355),('camu','ca',71,355),('aiyen','ay',72,355),('sinclair','si',73,345)]:
        tiles=extract(art/(name+'.png'),4,2,layout.get('thresholds',{}).get(name,48))
        scale=height/tiles[0][0].height
        for i,(im,bounds) in enumerate(tiles):
            path=art/'poses'/f'{prefix}{i}.png';im.save(path);key=f'{prefix}{i}'
            A.png(key,path,height,i,group)
            root=layout[name][i];root=(root[0]-bounds[0],root[1]-bounds[1]);axis(*root)
            A.meta[key].update(axis=list(root),scale=scale,bank=name,source_bounds=bounds)
    effects=Image.open(art/'effects.png').convert('RGBA');w,h=effects.size
    for i in range(8):
        tile=effects.crop((i%4*w//4,i//4*h//2,(i%4+1)*w//4,(i//4+1)*h//2))
        bounds=tile.getchannel('A').getbbox();assert bounds,(i,'missing projectile art')
        tile=tile.crop(bounds);path=art/'poses'/f'fx{i}.png';tile.save(path)
        A.png(f'fx{i}',path,tile.height,i,90);axis(tile.width//2,tile.height//2)
        width=140 if i<2 else 115 if i<4 else 130 if i<6 else 290
        A.meta[f'fx{i}'].update(axis=[tile.width//2,tile.height//2],scale=width/tile.width,bank='effects')
    bow=[('bo0',5),('bo1',5),('bo2',5),('bo3',5),('bo4',8),('bo5',4),('bo6',6),('bo7',8)]
    A.action(31400,bow)
    clips['31400']=dict(name='Anubis Arrow',form=3,frames=[dict(key=k,ticks=t,**A.meta[k]) for k,t in bow])
    for i,prefix in enumerate(['do','ca','ay','si']):
        A.action(7000+i*10,[(prefix+str(j),6) for j in range(8)],hurt=False)
    for n,keys,box in [(7100,['fx0','fx1'],(-65,-12,65,12)),(7110,['fx2','fx3'],(-48,-42,48,42)),(7120,['fx4','fx5'],(-58,-28,58,28)),(7130,['fx6','fx7'],None)]:
        A.action(n,[(key,4) for key in keys],(0,1) if box else (),attack=box or (0,0,0,0),hurt=False)
    provenance={p.name:dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),prompt=p.with_suffix('.prompt.txt').name) for p in art.glob('*.png') if p.with_suffix('.prompt.txt').exists()}
    (art/'provenance.json').write_text(json.dumps(dict(generator='Built-in imagegen',assets=provenance),indent=2))
    return True

def tick(ctl):
    ctl(-2,'Observe live projectiles','MapSet',map='"guest.projectiles"',value='numproj')
    ctl(-2,'Guest cooldown','VarAdd','var(21)>0',**{'var(21)':-1})
    ctl(-2,'Reset guest cooldown','VarSet','roundstate=0',**{'var(21)':0})
    ctl(-2,'Remove interrupted blessing','RemoveExplod','stateno!=2000',ID=7130)

def states(ns,state,ctl,end):
    # Helpers use fixed animations, independently of the player's outfit.
    fixed=ns['base_state']
    for i,(n,name,cost) in enumerate(zip(STATES,NAMES,COSTS)):
        state(n,n,move='I' if i==0 else 'A',poweradd=-cost,velset='0,0')
        ctl(n,'Guest shared cooldown','VarSet','time=0',**{'var(21)':360})
        ctl(n,'Call '+name,'Helper','time=4',name=name+' guest',ID=7200+i*10,stateno=7200+i*10,postype='p1',pos='-230,0',ownpal=1,keyctrl=0)
        ctl(n,'Call sound','PlaySnd','time=4',value='0,4',volumescale=60)
        if i==0:
            ctl(n,'Dolores healing','LifeAdd',['time=28','numhelper(7200)>0'],value=120,absolute=1)
            ctl(n,'Healing sigil','Explod','time=24',anim=7130,ID=7130,pos='0,-190',postype='p1',bindtime=-1,removetime=24,sprpriority=3,ownpal=1)
        else:
            for j,vy in enumerate([0] if i!=2 else [-.8,0,.8]):
                projectile(ctl,n,28 if i!=2 else 34,7110 if i==1 else 7150 if i==2 else 7120,180 if i!=2 else 48,16 if i==1 else 25 if i==2 else 20,'-75,-230',vy,ID=n*10+j)
        end(n)
        helper=7200+i*10
        fixed(helper,7000+i*10,kind='S',move='I',velset='0,0')
        ctl(helper,'Nonblocking guest','PlayerPush',value=0)
        ctl(helper,'Guest fade','Trans',trans='addalpha',alpha='min(256,min(time*64,(48-time)*64)),256-min(256,min(time*64,(48-time)*64))')
        ctl(helper,'Guest ends','DestroySelf','time>=48 || root,stateno=99000 || root,life<=0 || root,movetype=H || root,stateno!='+str(n))
    state(1400,1400,move='A',velset='0,0')
    projectile(ctl,1400,28,7140,82,27,'115,-270',0,ID=1400)
    ctl(1400,'Bow release sound','PlaySnd','time=28',value='0,0')
    end(1400)

def projectile(ctl,n,t,anim,damage,speed,offset,vy=0,ID=None):
    ctl(n,'Traveling projectile','Projectile',f'time={t}',projid=ID or n,projanim=anim,projhitanim=-1,projremanim=-1,projremove=1,projremovetime=80,velocity=f'{speed},{vy}',offset=offset,attr='S,SP',damage=f'{damage},3',guardflag='MA',hitflag='MAF',pausetime='0,5',ground__type='High',ground__hittime=20,ground__velocity=-3,air__velocity='-3,-3',getpower='0,0',givepower='10,0',hitsound='S0,0')

def routes(route,g):
    common=['roundstate=2','ctrl','statetype!=A','ailevel=0','var(21)=0']
    for name,n,cost,direction in [('dolores',2000,1250,'holdfwd'),('camu',2010,1250,'holdfwd'),('aiyen',2020,1000,'holdback'),('sinclair',2030,1250,'holddown')]:
        conditions=common+[f'power>={cost}',f'command="{direction}"']
        if direction!='holddown':conditions+=['command!="holddown"']
        route('guest_'+name,n,conditions)
    route('bow',1400,['roundstate=2','ctrl','statetype!=A','ailevel=0','map(vikir.form)=3','command="holdfwd"','command!="holddown"'])
