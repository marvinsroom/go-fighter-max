"""Agent J form extensions for the shared Will package; source PNGs stay intact."""
from PIL import Image
import math
import re

def effect_sprites(emit):
    # Original code-native effects, isolated from all Fresh Prince imagery.
    field=bytearray()
    for y in range(360):
        for x in range(640):
            grid=x%48==0 or y%48==0
            star=(x*137+y*97)%2701==0
            field.extend((80 if star else 5,200 if star else (30 if grid else 9),255 if star else (65 if grid else 26),255))
    emit(0,640,360,field,(0,0))
    ring=bytearray()
    for y in range(256):
        for x in range(256):
            radius=math.hypot(x-127.5,y-127.5)
            alpha=int(255*max(0,1-abs(radius-100)/8))
            ring.extend((80,235,255,alpha))
    emit(1,256,256,ring,(128,128))
    beam=bytearray()
    for y in range(512):
        for x in range(128):
            distance=abs(x-63.5)/64
            core=max(0,1-distance*4)
            beam.extend((int(50+205*core),int(180+75*core),255,int(255*(1-distance)**.6)))
    emit(2,128,512,beam,(64,512))

POSES={'idle':(375,512),'fire':(375,500),'flash':(375,500),'kick':(375,330),
       'crouch':(235,510),'hurt':(375,510),'down':(145,900)}
REMAP={'idle':'idle','pass':'idle','plant':'idle','lead':'idle','jab':'fire','palm':'flash',
       'elbow':'fire','airkick':'kick','crouch':'crouch','hurt':'hurt','down':'down',
       'sweep':'kick','whistle':'idle','shrug':'idle'}

def animation_value(expression):
    # Select the actual suited AIR action before its first frame is drawn.
    expression=str(expression)
    return f'ifelse(var(30)=1 && selfanimexist(10000+({expression})),10000+({expression}),({expression}))'

def victim_animation_value(state_number):
    """Victims use their own reaction art and active form at the first frame."""
    reaction=5050 if state_number in (821,1420) else 5000
    return f'ifelse(var(45)>0 && selfanimexist({reaction}+var(45)*10000),{reaction}+var(45)*10000,{animation_value(reaction)})'

def animation_variants(air,meta):
    """Bake shared animations into an immutable Agent bank, including scales."""
    by_sprite={(0,meta[key]['number']):(meta[key],meta['agent_'+pose]) for key,pose in REMAP.items()}
    text='\n'.join(air)
    variants=[]
    for block in re.split(r'(?=\[Begin Action )',text):
        header=re.match(r'\[Begin Action (\d+)\]',block)
        if not header:continue
        number=int(header[1])
        if number in (3900,3901) or number>=10000:continue
        lines=block.splitlines();changed=False;has_other_sprite=False
        for i,line in enumerate(lines[1:],1):
            if not re.match(r'^-?\d+,',line):continue
            fields=line.split(',');key=(int(fields[0]),int(fields[1]))
            if key not in by_sprite:
                has_other_sprite=True;continue
            old,new=by_sprite[key]
            fields[0]=str(new['group']);fields[1]=str(new['number'])
            ratio=new['scale']/old['scale']
            fields[7]=f'{float(fields[7])*ratio:.7f}'
            fields[8]=f'{float(fields[8])*ratio:.7f}'
            lines[i]=','.join(fields);changed=True
        if changed and not has_other_sprite:
            lines[0]=f'\n[Begin Action {10000+number}]'
            variants.append('\n'.join(lines))
    air.extend(variants)

def common_states(text):
    """Keep stock common-state mechanics, selecting the form's animation bank."""
    lines=[]
    for line in text.splitlines():
        if not line.lstrip().startswith('[Function'):
            line=re.sub(r'(?<![\w$])anim\b(?!\s*:)', '(anim % 10000)',line,flags=re.I)
        lines.append(line)
    text='\n'.join(lines)+'\n'
    text=re.sub(r'(changeAnim2?\s*\{\s*value:\s*)([^;\r\n}]+)',
                lambda m:m[1]+animation_value(m[2]),text,flags=re.I)
    text=re.sub(r'(\[StateDef[^\r\n]*?\banim:\s*)(-?\d+)',
                lambda m:m[1]+animation_value(m[2]),text,flags=re.I)
    return '# Local Will copy: form-aware animation selection; stock mechanics preserved.\n'+text

def sprites(png_sprite,source):
    for i,(key,(height,axis)) in enumerate(POSES.items()):
        path=source/'art/agent-j-v1'/('flash-v2.png' if key=='flash' else key+'.png')
        with Image.open(path) as im:bottom=im.getchannel('A').point(lambda a:255 if a>200 else 0).getbbox()[3]
        png_sprite('agent_'+key,path,(axis,bottom),height,group=10,number=i)

NORMALS={4100:('Agency Check','fire',6,3,12,32,'S','MA',False),
 4120:('Black Tie Kick','kick',14,5,23,82,'S','MA',True),
 4140:('Cuff Check','crouch',7,3,13,28,'C','L',False),
 4160:('Sweep Protocol','kick',16,4,25,65,'C','L',True),
 4180:('Air Intercept','kick',10,6,18,65,'A','H',True)}

def animations(action,air):
    action(3900,[('idle',24),('agent_idle',24)])
    action(3901,[('agent_idle',24),('idle',24)])
    for num,(_,pose,startup,active,recovery,damage,kind,guard,fall) in NORMALS.items():
        action(num,[('agent_crouch' if kind=='C' else 'agent_idle',startup),('agent_'+pose,active),('agent_crouch' if kind=='C' else 'agent_idle',recovery)],
               active={1},hurt=(-60,-225,70,0) if kind=='C' else (-55,-355,65,0),
               attack=(20,-90,220,-5) if kind=='C' else (25,-310,235,-110))
    for num,startup,recovery,pose in [(4110,12,22,'fire'),(4150,14,24,'fire'),(4300,24,35,'fire'),
          (4310,34,36,'fire'),(4320,20,34,'flash'),(4330,5,30,'idle'),(4400,28,46,'fire'),(4500,24,34,'flash')]:
        action(num,[('agent_idle',startup),('agent_'+pose,6),('agent_idle',recovery)],
               active={1} if num in [4320,4500] else None,
               attack=(10,-350,225,-110))
    action(4510,[('agent_flash',36),('agent_fire',48),('agent_kick',24),('agent_fire',48),('agent_flash',48),('agent_idle',36)])
    action(4550,[('agent_hurt',-1)],hurt=None)
    for num,scale in [(6410,'1,.7'),(6411,'2,1.8')]:
        air.extend([f'\n[Begin Action {num}]','Clsn1: 1','Clsn1[0] = -55,-20,55,20',f'7100,0,0,0,-1,,,{scale}'])
    air.extend(['\n[Begin Action 6420]','7200,0,0,0,-1,,,2,2'])
    air.extend(['\n[Begin Action 6421]','7200,1,0,0,8,,,0.4,0.15','Interpolate Scale',
                '7200,1,0,0,8,,,1.3,0.4','Interpolate Scale','7200,1,0,0,8,,,2.8,0.8'])
    air.extend(['\n[Begin Action 6422]','7200,2,0,0,5,,,1.5,1.5','7200,2,0,0,5,,,2.5,1.5',
                '7200,2,0,0,5,,,1.8,1.5','7200,2,0,0,5,,,3,1.5'])

def commands(command_state):
    g=['roundstate=2','statetype!=A','ctrl']
    command_state('Suit up',3900,g+['var(30)=0','var(31)=0','power>=1000','command="transform"'])
    command_state('Return to Fresh Prince',3901,g+['var(30)=1','var(31)=0','command="transform"'])
    a=['roundstate=2','var(30)=1','statetype!=A','ctrl']
    for label,st,cost,command in [('Galaxy Protocol',4500,2000,'ultimate_short'),('Noisy Cricket Overload',4400,1000,'super_short')]:
        command_state(label,st,a+[f'power>={cost}',f'command="{command}"'])
    for label,st,command in [('Noisy Cricket',4300,'three'),('Deatomizer',4310,'windmill'),('Evasive Protocol',4330,'taxi')]:
        command_state(label,st,a+[f'command="{command}"'])
    command_state('Neuralyzer',4320,a+['var(32)=0','power>=250','command="skill" || command="freeze"'])
    command_state('Agent air kick',4180,['roundstate=2','var(30)=1','statetype=A','ctrl','command="L" || command="M" || command="H"'])
    for button,num in [('H',4160),('M',4150),('L',4140)]:
        command_state('Agent crouch '+button,num,a+['command="holddown"',f'command="{button}"'])
    for button,num in [('H',4120),('M',4110),('L',4100)]:command_state('Agent '+button,num,a+[f'command="{button}"'])

def global_states(ctl,meta,records):
    # Form effects have explicit ownership. Clear them even after interruption.
    for effect in [6000,6001,6400,6401]:
        ctl(-2,'Agent excludes Fresh Prince cinematic '+str(effect),'RemoveExplod','var(30)=1',ID=effect)
    for effect in [6420,6421,6422]:
        ctl(-2,'Agent cinematic cleanup '+str(effect),'RemoveExplod','stateno!=4510',ID=effect)
    for var in [31,32]:ctl(-2,'Agent cooldown','VarAdd',f'var({var})>0',**{f'var({var})':-1})
    ctl(-2,'Synchronize animation after form change','ChangeAnim',
        'var(30)!=var(33) && anim!=3900 && anim!=3901',value='anim%10000',elem='animelemno(0)',ignorehitpause=1)
    ctl(-2,'Remember current animation bank','VarSet','var(30)!=var(33)',**{'var(33)':'var(30)','ignorehitpause':1})
    # Shared movement, throws and reactions now select baked group-10 AIR actions.
    # No live RemapSprite map or per-tick scale correction is needed.

def states(state,ctl,finish,hit):
    for num,form,cost,pose in [(3900,1,1000,3900),(3901,0,0,3901)]:
        state(num,pose,velset='0,0',poweradd=-cost)
        ctl(num,'Commit form','VarSet','time=24',**{'var(30)':form})
        ctl(num,'Switch cooldown','VarSet','time=24',**{'var(31)':120})
        ctl(num,'Suit flash','PalFX','time=24',time=7,add='140,170,200',mul='256,256,256')
        ctl(num,'Cue','PlaySnd','time=24',value='0,3');finish(num)
    for num,(_,pose,startup,active,recovery,damage,kind,guard,fall) in NORMALS.items():
        state(num,num,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}))
        hit(num,startup,damage,kind,guard,fall)
        if kind=='A':
            ctl(num,'Gravity','VelAdd',y=.65);ctl(num,'Land','ChangeState',['vel y>0','pos y>=0'],value=52,ctrl=0)
        finish(num,air=kind=='A',crouch=kind=='C')
    for num,startup,damage,speed,recoil,cost in [(4110,12,48,12,-1,0),(4150,14,45,12,-1,0),
          (4300,24,100,15,-5,0),(4310,34,140,10,-2,0),(4400,28,220,18,-8,1000)]:
        state(num,num,kind='C' if num==4150 else 'S',move='A',velset='0,0',poweradd=-cost)
        if cost:ctl(num,'Overload flash','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0)
        ctl(num,'Alien energy shot','Projectile',f'time={startup}',projid=num,projanim=6411 if num in [4310,4400] else 6410,
            projhitanim=-1,projremanim=-1,projremove=1,projremovetime=100,projsprpriority=4,
            velocity=f'{speed},0',offset='130,-325',attr='S,HP' if cost else 'S,SP',damage=f'{damage},{int(damage*.04)}',
            guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=22,
            ground__velocity='-4,-4' if num in [4300,4310,4400] else '-3',air__velocity='-4,-5',
            fall=1 if num in [4300,4310,4400] else 0,getpower='0,0' if cost else '60,15',givepower='30,10',hitsound='S0,1')
        ctl(num,'Comic recoil','VelSet',f'time={startup}',x=recoil)
        ctl(num,'Recoil drag','VelMul',f'time>{startup}',x=.82)
        ctl(num,'Energy cue','PlaySnd',f'time={startup}',value='0,0')
        finish(num,crouch=num==4150)
    state(4320,4320,move='A',velset='0,0',poweradd=-250)
    hit(4320,20,20,attr='SA',ground__hittime=48,ground__velocity='-1',getpower='0,0')
    ctl(4320,'Prevent flash loops','VarSet','time=0',**{'var(32)':180})
    ctl(4320,'Localized flash','Explod','time=20',anim=7001,postype='p1',pos='150,-300',scale='3,3',removetime=-2,sprpriority=6)
    finish(4320)
    state(4330,4330,velset='0,0');ctl(4330,'Vulnerable retreat','VelSet','time<18',x=-5)
    ctl(4330,'End retreat','VelSet','time>=18',x=0);finish(4330)
    state(4500,4500,move='A',velset='0,0',poweradd=-2000)
    ctl(4500,'Protocol flash','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0)
    hit(4500,24,0,attr='HA',p1stateno=4510,p2stateno=4550,getpower='0,0',givepower='0,0');finish(4500)
    state(4510,4510,move='A',velset='0,0')
    ctl(4510,'Confirmed sequence','NotHitBy',value='SCA',time=1)
    ctl(4510,'Agent camera framing','ScreenBound',value=0,movecamera='0,0')
    ctl(4510,'Frame agent','PosSet',x='camerapos x-facing*240',y=0)
    ctl(4510,'Agency star field','Explod','time=0',anim=6420,ID=6420,postype='left',pos='0,0',
        bindtime=-1,removetime=240,sprpriority=-9,ownpal=1)
    ctl(4510,'Neural capture','TargetBind','time<36',pos='220,-(time*3)')
    ctl(4510,'Tractor beam lift','TargetBind','time=[36,83]',pos='220,-108-(time-36)*5')
    ctl(4510,'Orbital suspension','TargetBind','time=[84,155]',pos='220+25*sin(time*.3),-348+15*sin(time*.2)')
    ctl(4510,'Slam back to earth','TargetBind','time=[156,179]',pos='220,-348+(time-156)*14')
    ctl(4510,'Orbital deatomizer beam','Explod','time=84',anim=6422,ID=6422,postype='p1',pos='220,0',
        bindtime=-1,removetime=96,sprpriority=5,ownpal=1)
    for t in [0,24,48,72,96,120,144,180]:
        ctl(4510,'Alien shock ring','Explod',f'time={t}',anim=6421,ID=6421,postype='p1',pos='220,-50',
            scale='1.5,1.5',removetime=-2,sprpriority=6,ownpal=1)
        ctl(4510,'Protocol shake','EnvShake',f'time={t}',time=12,ampl=14 if t==180 else 5,freq=80)
        ctl(4510,'Protocol cue','PlaySnd',f'time={t}',value='0,3')
    ctl(4510,'Memory wipe flash','EnvColor','time=180',value='200,245,255',time=6,under=0)
    ctl(4510,'Resolve protocol once','TargetLifeAdd','time=180',value=-390,kill=1)
    ctl(4510,'Release','TargetState','time=180',value=821)
    ctl(4510,'End','ChangeState','time>=239',value=0,ctrl=1)
    state(4550,move='H');ctl(4550,'Reaction','ChangeAnim','time=0',value=5000)
    ctl(4550,'Capture protection','NotHitBy',value='SCA',time=1)
    ctl(4550,'Captured target camera','ScreenBound',value=0,movecamera='0,0')
    ctl(4550,'Escape orphan capture','SelfState','time>300',value=0,ctrl=1)
