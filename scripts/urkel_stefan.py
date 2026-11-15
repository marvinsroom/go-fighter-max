"""Stefan Urquelle's own sprite bank and close-combat form."""
import re
POSES={'idle':350,'palm':350,'kick':320,'crouch':225,'hurt':350,'down':135}
REPLACEMENTS={'idle':'idle','palm':'palm','kick':'kick','crouch':'crouch','gadget':'palm','stumble':'kick','hurt':'hurt','down':'down'}
NORMALS={4100:('Smooth Palm','palm',6,3,12,34,'S','MA',False),
         4110:('Polished Straight','palm',9,4,15,56,'S','MA',False),
         4120:('Suave Heel','kick',15,5,22,90,'S','MA',True),
         4140:('Low Check','crouch',6,3,12,30,'C','L',False),
         4150:('Tailored Sweep','kick',13,4,23,60,'C','L',True),
         4160:('Perfect Timing','palm',10,5,22,78,'C','MA',True),
         4180:('Air Elegance','kick',9,6,18,65,'A','H',True)}
def variants(air,meta):
    lookup={(20,meta[key]['number']):(meta[key],meta['stefan_'+pose]) for key,pose in REPLACEMENTS.items()}
    copies=[]
    for block in re.split(r'(?=\[Begin Action )','\n'.join(air)):
        head=re.match(r'\[Begin Action (\d+)\]',block)
        if not head or int(head[1]) in (3900,3901):continue
        lines=block.splitlines();changed=False;foreign=False
        for i,line in enumerate(lines[1:],1):
            if not re.match(r'^-?\d+,',line):continue
            parts=line.split(',');key=(int(parts[0]),int(parts[1]))
            if key not in lookup:foreign=True;continue
            old,new=lookup[key]
            if int(head[1]) in (20,21):new=meta['stefan_idle']
            ratio=new['scale']/old['scale']
            parts[0]=str(new['group']);parts[1]=str(new['number'])
            parts[7]=f'{float(parts[7])*ratio:.7f}';parts[8]=f'{float(parts[8])*ratio:.7f}'
            lines[i]=','.join(parts);changed=True
        if changed and not foreign:
            lines[0]=f'\n[Begin Action {10000+int(head[1])}]';copies.append('\n'.join(lines))
    air.extend(copies)
def animations(action):
    action(3900,[('idle',24),('stefan_idle',24)])
    action(3901,[('stefan_idle',24),('idle',24)])
    for num,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
        base='stefan_crouch' if kind=='C' else 'stefan_kick' if kind=='A' else 'stefan_idle'
        action(num,[(base,start),('stefan_'+pose,active),(base,recovery)],active=(1,),kind=kind,
               attack=(15,-85,215,-5) if guard=='L' else (15,-310,220,-105))
    for num,pose,start,active,recovery in [(4300,'palm',10,5,20),(4310,'kick',20,5,25),(4330,'idle',4,1,27),
                                          (4400,'palm',14,5,28),(4500,'palm',24,5,35)]:
        action(num,[('stefan_idle',start),('stefan_'+pose,active),('stefan_idle',recovery)],active=(1,) if num!=4330 else ())
    action(4410,[('stefan_palm',24),('stefan_kick',24),('stefan_palm',24),('stefan_kick',24),('stefan_idle',48)])
    action(4510,[('stefan_idle',24),('stefan_palm',36),('stefan_kick',36),('stefan_palm',36),('stefan_kick',48),('stefan_idle',60)])
def commands(command):
    g=['roundstate=2','statetype!=A','ctrl']
    command('Become Stefan',3900,g+['var(30)=0','var(31)=0','power>=1000','command="transform"'])
    command('Return to Steve',3901,g+['var(30)=1','var(31)=0','command="transform"'])
    a=g+['var(30)=1']
    for name,num,cost in [('ultimate_short',4500,2000),('super_short',4400,1000)]:command('Stefan '+name,num,a+[f'power>={cost}',f'command="{name}"'])
    for name,num in [('cheese',4300),('snap',4310),('retreat',4330),('skill',4300),('stumble',4300)]:command('Stefan '+name,num,a+[f'command="{name}"'])
    for button,num in [('H',4160),('M',4150),('L',4140)]:command('Stefan low '+button,num,a+['command="holddown"',f'command="{button}"'])
    for button,num in [('H',4120),('M',4110),('L',4100)]:command('Stefan '+button,num,a+[f'command="{button}"'])
    command('Stefan air',4180,['roundstate=2','var(30)=1','statetype=A','ctrl','command="L" || command="M" || command="H"'])
def globals(ctl):
    ctl(-2,'Transformation cooldown','VarAdd','var(31)>0',**{'var(31)':-1})
    ctl(-2,'Synchronize form animation','ChangeAnim','var(30)!=var(33) && anim!=3900 && anim!=3901',
        value='anim%10000',elem='animelemno(0)',ignorehitpause=1)
    ctl(-2,'Remember form bank','VarSet','var(30)!=var(33)',**{'var(33)':'var(30)','ignorehitpause':1})
def states(state,ctl,end,hit):
    for num,form,cost in [(3900,1,1000),(3901,0,0)]:
        state(num,num,velset='0,0',poweradd=-cost)
        ctl(num,'Commit form','VarSet','time=24',**{'var(30)':form})
        ctl(num,'Switch cooldown','VarSet','time=24',**{'var(31)':120})
        ctl(num,'Transform flash','PalFX','time=24',time=7,add='120,110,90',mul='256,256,256')
        end(num)
    for num,(_,pose,start,active,recovery,damage,kind,guard,fall) in NORMALS.items():
        state(num,num,kind=kind,move='A',poweradd=15,**({} if kind=='A' else {'velset':'0,0'}))
        hit(num,start,damage,kind,guard,fall)
        if kind=='A':ctl(num,'Gravity','VelAdd',y=.65);ctl(num,'Land','ChangeState',['vel y>0','pos y>=0'],value=52)
        end(num,kind=='A',kind=='C')
    for num,start,damage,guard in [(4300,10,60,'MA'),(4310,20,95,'H')]:
        state(num,num,move='A',velset='0,0');hit(num,start,damage,guard=guard,fall=num==4310,attr='S,SA')
        if num==4300:
            ctl(num,'Smooth approach','VelSet','time<15',x=5)
            ctl(num,'Plant feet','VelSet','time>=15',x=0)
        end(num)
    state(4330,4330,velset='0,0');ctl(4330,'Smooth retreat','VelSet','time<16',x=-6)
    ctl(4330,'Stop','VelSet','time>=16',x=0);end(4330)
    for num,target,cost,start in [(4400,4410,1000,14),(4500,4510,2000,24)]:
        state(num,num,move='A',velset='0,0',poweradd=-cost)
        ctl(num,'Style pause','SuperPause','time=0',time=12,anim=-1,movetime=0,unhittable=0)
        hit(num,start,0,attr='S,HA',p1stateno=target,p2stateno=8250,getpower='0,0',givepower='0,0');end(num)
    for num,total,final,damage in [(4410,144,96,245),(4510,240,180,390)]:
        state(num,num,move='A',velset='0,0')
        ctl(num,'Confirmed protection','NotHitBy',value='SCA',time=1)
        ctl(num,'Keep camera still','ScreenBound',value=0,movecamera='0,0')
        ctl(num,'Frame Stefan','PosSet',x='camerapos x-facing*180',y=0)
        ctl(num,'Fluid combo','TargetBind',f'time<{final}',pos='150+25*sin(time*.3),-abs(sin(time*.045))*160')
        ctl(num,'Silhouette trails','AfterImage','time=20',time=final-12,length=10,timegap=2,framegap=2,trans='add')
        for tick in ([24,48,72,96] if num==4410 else [24,48,72,96,120,150,180]):
            ctl(num,'Golden impact','Explod',f'time={tick}',anim=6407,ID=6407,postype='p1',pos='150,-180',removetime=-2,sprpriority=6,ownpal=1)
            ctl(num,'Combo cue','PlaySnd',f'time={tick}',value='0,1')
            ctl(num,'Impact shake','EnvShake',f'time={tick}',time=8,ampl=12 if tick==final else 4,freq=90)
        ctl(num,'Resolve once','TargetLifeAdd',f'time={final}',value=-damage,kill=1)
        ctl(num,'Release','TargetState',f'time={final}',value=8260)
        ctl(num,'Recover','ChangeState',f'time>={total-1}',value=0,ctrl=1)
