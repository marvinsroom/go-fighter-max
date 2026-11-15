"""Build Prince, Negan and Rick James/Tyrone as independent native fighters."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,re
from fighter_assets import FighterAssets
import chappelle_core as core
import will_agent_j as agent

ROOT=Path(__file__).resolve().parents[1]
KEYS=['idle','walk_a','walk_b','palm','kick','special','crouch','hurt','down']
CONFIGS={
 'prince':dict(name='Dave Chappelle as Prince',speed=4.1,reach=230,color=(180,95,255),
   normals=['Lace Flick','Royal Backhand','Purple Heel','Ankle Tap','Court Sweep','Royal Rejection','Air Check','Floating Heel','Purple Descent'],
   skills={1000:'Royal Bounce',1010:'Royal Bounce Medium',1020:'Royal Bounce High',1100:'Check Ball',1110:'Purple Slide',1120:'Ruffle Counter',1130:'Baseline Cut',1200:'Royal Rejection',1400:'Slide Feint'},
   supers=['Game, Blouses','Breakfast Is Served']),
 'negan':dict(name='Dave Chappelle as Negan',speed=2.9,reach=330,color=(235,90,65),
   normals=['Personal Space','Handle That','Big Introduction','Boot Check','Kneecap Notice','Heads Up','Air Check','Leather Sole','Heavy Baggage'],
   skills={1000:'Meet Lucille Light',1010:'Meet Lucille Medium',1020:'Meet Lucille Heavy',1100:'The Whistle',1110:'Take a Knee',1120:'Swing and a Miss',1130:'Business Meeting',1200:'Back Off',1400:'Measured Retreat'},
   supers=['Collection Day','The Last Laugh']),
 'rick':dict(name='Dave Chappelle as Rick James',speed=3.5,reach=235,color=(255,200,80),
   normals=['Ring Check','Royal Slap','Platform Heel','Low Check','Couch Sweep','Funk Uppercut','Air Palm','Platform Drop','Flying Funk'],
   skills={1000:'Cold Blooded',1010:'Cold Blooded Medium',1020:'Cold Blooded Heavy',1100:'Unity Slap',1110:'Platform Rush',1120:'Couch Surf',1130:'Couch Crusher',1200:'Funk Flash',1400:'Funk Retreat',4100:'Quick Rush',4110:'Panic Lunge',4120:'Backpedal',4130:'Floor Scramble',4200:'Rising Flail'},
   supers=['Unity Tour','Couch Demolition','Scramble City','Midnight Mayhem']),
}

def effects(a,slug,cfg):
    color=cfg['color']
    def ball(x,y):
        dx,dy=x-47.5,y-47.5;r=math.hypot(dx,dy)
        if r>46:return (0,0,0,0)
        seam=abs(dx)<2 or abs(dy)<2 or abs(abs(dx)-30*(1-(dy/46)**2))<2
        return (30,18,36,255) if r>43 or seam else (230,115+int(25*(1-r/46)),35,255)
    a.raw(0,96,96,ball)
    def scene(x,y):
        if slug=='prince':
            if y<430:return (20,12,45,255) if math.hypot(x-1020,y-130)>70 else (200,190,225,255)
            line=abs(x-640)<2 or abs(math.hypot(x-640,(y-580)*2)-180)<3
            return (175,130,220,255) if line else (65+(x//100)%2*7,35,90,255)
        if slug=='negan':
            beam=x%210<10 or y%150<8
            return (67,55,55,255) if beam else (25,25,33,255) if y<540 else (56,44,42,255)
        tile=(x//80+y//80)%2
        return (46+tile*15,18+tile*6,60+tile*15,255) if y>430 else (25,12,44,255)
    a.raw(1,1280,720,scene,(0,0))
    def prop(x,y):
        if slug=='prince':
            if 20<x<300 and 15<y<25 or 150<x<160 and 20<y<270:return (185,180,220,255)
            if 55<x<255 and 65<y<80:return (255,115,50,255)
            if 75<x<235 and 80<y<215 and (x%24<2 or y%24<2):return (235,225,245,215)
        elif slug=='negan':
            xx=x%100;yy=y%90
            if 4<xx<95 and 4<yy<85:
                return (145,100,60,255) if xx<10 or yy<10 or abs(xx-yy)<6 else (90,60,42,255)
        else:
            if 25<x<295 and 75<y<240:
                return (155,45,75,255) if x<55 or x>265 or y<135 else (100,28,58,255)
            if (40<x<65 or 255<x<280) and 235<y<270:return (170,115,55,255)
        return (0,0,0,0)
    a.raw(2,320,280,prop,(160,280))
    def slash(x,y):
        r=math.hypot((x-180)/1.4,y-100)
        alpha=int(240*max(0,1-abs(r-75)/12)) if x>30 else 0
        return (*color,alpha)
    a.raw(3,360,200,slash)
    a.raw(4,192,192,lambda x,y:(*color,int(245*max(0,1-abs(math.hypot(x-95.5,y-95.5)-65)/10))))
    a.raw(5,256,256,lambda x,y:(255,235,190,235) if (abs(x-128)<5 or abs(y-128)<5 or abs(abs(x-128)-abs(y-128))<4) and math.hypot(x-128,y-128)<120 else (0,0,0,0))
    def finale(x,y):
        if slug=='prince':
            if ((x-160)/143)**2+((y-200)/32)**2<1:return (230,235,255,255)
            for row in range(4):
                if ((x-160)/100)**2+((y-(170-row*17))/18)**2<1:return (235,175-row*7,75,255)
            if 143<x<177 and 94<y<110:return (255,230,130,255)
        elif slug=='negan':
            if abs(y-100-(x-160)*.5)<13:return (120,85,55,255)
        else:
            r=math.hypot(x-160,y-100)
            if r<95:return (210,205,255,245) if (x//12+y//12)%2 else (80,95,145,245)
        return (0,0,0,0)
    a.raw(6,320,240,finale)
    font=ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',44)
    for i,title in enumerate(cfg['supers']):
        im=Image.new('RGBA',(800,90));d=ImageDraw.Draw(im)
        d.text((400,40),title.upper(),font=font,fill=(*color,255),anchor='mm',stroke_width=2,stroke_fill=(15,10,30,255))
        a.raw(7+i,800,90,lambda x,y:im.getpixel((x,y)))

def build(slug,cfg):
    a=FighterAssets(ROOT,slug);S=a.source;O=a.output;forms=slug=='rick'
    for i,key in enumerate(KEYS):a.png(key,S/'art/v1'/f'{key}.png',365,i)
    scale=a.meta['idle']['scale']
    for m in a.meta.values():m['scale']=scale
    # Jump uses the dedicated rising pose, preserving the common sheet scale.
    a.meta['jump']=dict(a.meta['special'])
    if forms:
        for i,key in enumerate(KEYS):a.png('tyrone_'+key,S/'art/tyrone-v1'/f'{key}.png',365,i,group=51)
        ts=a.meta['tyrone_idle']['scale']
        for key in KEYS:a.meta['tyrone_'+key]['scale']=ts
        a.meta['tyrone_jump']=dict(a.meta['tyrone_special'])
    aliases=['idle']*4+['palm','crouch','kick','palm','palm','kick','hurt','down','idle','idle']
    for i,key in enumerate(aliases):a.alias(0,i,key)
    if forms:
        for i,key in enumerate(['idle','palm','palm','kick','crouch','hurt','down']):a.alias(10,i,'tyrone_'+key)
    effects(a,slug,cfg)
    N={}
    for i,(n,pose,start,active,recovery,damage,kind,guard,fall) in enumerate([
      (200,'palm',6,3,12,30,'S','MA',False),(210,'palm',11,4,17,52,'S','MA',False),(220,'kick' if slug!='negan' else 'palm',18,5,24,82,'S','MA',True),
      (400,'crouch',7,3,13,26,'C','L',False),(410,'kick',15,4,25,58,'C','L',True),(420,'special',12,5,24,78,'C','MA',True),
      (600,'palm',7,5,15,34,'A','H',False),(610,'kick',10,6,19,58,'A','H',True),(620,'special',15,7,22,72,'A','H',True)]):
        N[n]=(cfg['normals'][i],pose,start,active,recovery,damage,kind,guard,fall)
    core.basic_animations(a,N,cfg['reach']);action=a.action
    for n,start,active,recovery,pose in [(1000,14,5,24,'palm'),(1010,20,5,28,'palm'),(1020,28,6,32,'palm'),
       (1100,9,6,24,'palm'),(1110,12,6,25,'kick'),(1120,10,12 if slug=='prince' else 6,24,'palm' if slug=='prince' else 'idle'),(1130,16,6,26,'crouch'),(1200,10,8,25,'special'),(1400,6,6,18,'walk_a')]:
        damaging=(slug!='prince' and n in [1000,1010,1020]) or n in ([1110,1120,1200] if slug=='prince' else [1110,1200] if slug=='negan' else [1000,1010,1020,1100,1110,1130,1200])
        action(n,[('crouch' if n==1130 else 'idle',start),(pose,active),('idle',recovery)],active=(1,) if damaging else (),
          attack=(0,-100,cfg['reach'],-5) if n==1110 and slug!='rick' else (0,-420,170,-50) if n==1200 else (0,-320,cfg['reach']+40,-40))
    action(1121,[('palm',12),('idle',20)])
    for n,start in [(3000,12),(3200,24)]:
        action(n,[('idle',start),('palm',6),('idle',28)],active=(1,),attack=(0,-355,450 if n==3000 else 340,-20))
    for n,total in [(3010,240),(3210,420)]:action(n,[(k,5) for _ in range((total-40)//20) for k in ['walk_a','palm','special','kick']]+[('special',20),('idle',20)])
    if forms:
        action(2000,[('idle',18),('idle',12),('idle',12)])
        for n,pose,start,active,recovery in [(4100,'palm',8,5,20),(4110,'palm',10,6,24),(4120,'walk_b',6,1,20),(4130,'crouch',10,6,24),(4200,'special',8,8,24)]:
            action(n,[('tyrone_idle',start),('tyrone_'+pose,active),('tyrone_idle',recovery)],active=() if n==4120 else (1,),attack=(0,-100,230,-5) if n==4130 else (0,-340,240,-40))
        for n,start in [(4400,10),(4500,22)]:action(n,[('tyrone_idle',start),('tyrone_palm',6),('tyrone_idle',28)],active=(1,),attack=(0,-355,450 if n==4400 else 340,-20))
        for n,total in [(4410,240),(4510,420)]:action(n,[('tyrone_'+k,5) for _ in range((total-40)//20) for k in ['walk_a','palm','special','kick']]+[('tyrone_special',20),('tyrone_idle',20)])
    for n,sprite,scale0 in [(6400,0,.64),(6401,1,1),(6402,2,1),(6403,3,1),(6404,4,1),(6405,5,1),(6406,6,1)]+[(6407+i,7+i,1) for i in range(len(cfg['supers']))]:
        a.air.extend([f'\n[Begin Action {n}]'])
        if n==6400:a.air.extend(['Clsn1: 1','Clsn1[0]=-28,-28,28,28'])
        a.air.append(f'7000,{sprite},0,0,-1,,,{scale0},{scale0}')
    if forms:
        source='\n'.join(a.air)
        for block in re.split(r'(?=\[Begin Action )',source):
            h=re.match(r'\[Begin Action (\d+)\]',block)
            if not h or int(h[1])>=6000 or not re.search(r'^50,',block,re.M):continue
            lines=block.strip().splitlines();lines[0]=f'[Begin Action {int(h[1])+10000}]'
            for i,line in enumerate(lines[1:],1):
                if line.startswith('50,'):
                    p=line.split(',');p[0]='51';p[7]=p[8]=f'{ts:.7f}';lines[i]=','.join(p)
            a.air.append('\n'+'\n'.join(lines))
    a.write_sff(slug+'.sff');a.write_air(slug+'.air')
    (O/(slug+'.def')).write_text(f'[Info]\nname="{cfg["name"]}"\ndisplayname="{cfg["name"]}"\nauthor="Game1 project"\nmugenversion=1.1\nlocalcoord=1280,720\n[Files]\ncmd={slug}.cmd\ncns={slug}.cns\nst={slug}.cns\nstcommon=common1.cns.zss\nsprite={slug}.sff\nanim={slug}.air\nsound={slug}.snd\n')
    if forms:
        common=agent.common_states((O.parents[1]/'data/common1.cns.zss').read_text()).replace('var(30)','var(45)').replace('Local Will copy','Local Rick/Tyrone copy')
        (O/'rick-common.cns.zss').write_text(common)
        definition=O/'rick.def'
        definition.write_text(definition.read_text().replace('stcommon=common1.cns.zss','stcommon=rick-common.cns.zss'))
    commands={'L':'a','M':'b','H':'c','skill':'x','super_short':'y','ultimate_short':'z','throw':'d','transform':'w',
      'special_light':'D, DF, F, a','special_medium':'D, DF, F, b','special_heavy':'D, DF, F, c',
      'back_light':'D, DB, B, a','back_medium':'D, DB, B, b','back_heavy':'D, DB, B, c',
      'anti_air':'F, D, DF, c','side_switch':'D, D, x','holdfwd':'/$F','holdback':'/$B','holddown':'/$D','holdup':'/$U'}
    cmd='[Remap]\na=a\nb=b\nc=c\nx=x\ny=y\nz=z\nd=d\ns=s\nw=w\n[Defaults]\ncommand.time=20\ncommand.buffer.time=3\n'
    for name,keys in commands.items():cmd+=f'\n[Command]\nname="{name}"\ncommand={keys}\ntime={20 if "," in keys else 1}\n'
    cmd+='\n[Statedef -1]\n'
    def command(label,target,conditions):
        nonlocal cmd
        cmd+=f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join(f'triggerall={c}\n' for c in conditions[:-1])+f'trigger1={conditions[-1]}\nvalue={target}\nctrl=0\n'
    g=['roundstate=2','statetype!=A','ctrl'];base=g+(['var(45)=0'] if forms else [])
    if forms:
        command('Toggle Rick and Tyrone',2000,g+['var(47)=0','command="transform"'])
        t=g+['var(45)=1']
        for name,n,cost in [('ultimate_short',4500,2000),('super_short',4400,1000)]:command(name,n,t+[f'power>={cost}',f'command="{name}"'])
        for n,route in [(4130,'command="holddown"'),(4120,'command="holdback"'),(4110,'command="holdfwd"'),(4100,'1')]:command('Tyrone route',n,t+[route,'command="skill"'])
        for name,n in [('special_light',4100),('special_medium',4110),('special_heavy',4130),('back_light',4120),('back_medium',4130),('back_heavy',4120),('anti_air',4200)]:command(name,n,t+[f'command="{name}"'])
    for name,n,cost in [('ultimate_short',3200,2000),('super_short',3000,1000)]:command(name,n,base+[f'power>={cost}',f'command="{name}"'])
    motions=[('special_light',1000),('special_medium',1010),('special_heavy',1020),('back_light',1400 if slug=='prince' else 1120),('back_medium',1110),('back_heavy',1120 if slug=='prince' else 1130 if slug=='negan' else 1120),('anti_air',1200),('side_switch',1130)]
    for name,n in motions:command(name,n,base+(['numproj=0'] if slug=='prince' and n<1100 else [])+(['p2bodydist x<75','p2statetype!=A','p2movetype!=H'] if slug=='negan' and n==1130 else [])+[f'command="{name}"'])
    for n,route in [(1130,'command="holddown"'),(1120,'command="holdback"'),(1110,'command="holdfwd"'),(1100,'1')]:command('Skill route',n,base+(['p2bodydist x<75','p2statetype!=A','p2movetype!=H'] if slug=='negan' and n==1130 else [])+[route,'command="skill"'])
    if slug in ('prince','negan'):
        for key,n in [('L',1000),('M',1130 if slug=='prince' else 1110),('H',1200)]:command('Stance branch',n,['roundstate=2','stateno=1100','time=[8,26]']+(['numproj=0'] if slug=='prince' and n==1000 else [])+[f'command="{key}"'])
    for n,back in [(810,True),(800,False)]:command('Throw',n,g+['p2bodydist x<75','p2statetype!=A','p2movetype!=H',f'command="throw" && command{"=" if back else "!="}"holdback"'])
    for key,n in [('H',620),('M',610),('L',600)]:command('Air '+key,n,['roundstate=2','statetype=A','ctrl',f'command="{key}"'])
    for key,n in [('H',420),('M',410),('L',400)]:command('Low '+key,n,g+['command="holddown"',f'command="{key}"'])
    for key,n in [('H',220),('M',210),('L',200)]:command(key,n,g+[f'command="{key}"'])
    for label,n,conds in [('Crouch',10,['stateno!=10','command="holddown"']),('Jump',40,['command="holdup"']),('Forward',20,['stateno=0','command="holdfwd"']),('Back',21,['stateno=0','command="holdback"'])]:command(label,n,g+conds)
    command('CPU attack',210,g+['ailevel>0','p2bodydist x<180','random<35'])
    command('CPU approach',20,g+['ailevel>0','stateno=0','p2bodydist x>160'])
    (O/(slug+'.cmd')).write_text(cmd)
    core.reset(forms);state,ctl,hit,end=core.state,core.ctl,core.hit,core.end
    def globals_hook():
        if not forms:return
        ctl(-2,'Form cooldown','VarAdd','var(47)>0',**{'var(47)':-1})
        ctl(-2,'Keep Tyrone drawing','ChangeAnim',['var(45)>0','anim<10000','selfanimexist(anim+10000)'],value='anim+10000',elem='animelemno(0)')
        ctl(-2,'Restore Rick drawing','ChangeAnim',['var(45)=0','anim>=10000','selfanimexist(anim%10000)'],value='anim%10000',elem='animelemno(0)')
    core.basic_states(N,cfg['speed'],globals_hook)
    if slug=='prince':
        for n,start,speed,vy,damage in [(1000,14,8,-1.5,48),(1010,20,10,-3,60),(1020,28,7,-5,72)]:
            state(n,n,move='A',velset='0,0')
            ctl(n,'Royal Bounce','Projectile',f'time={start}',projid=n,projanim=6400,projhitanim=-1,projremanim=-1,projremove=1,projremovetime=100,
              velocity=f'{speed},{vy}',accel='0,.06',offset='100,-150',attr='S,SP',damage=f'{damage},2',guardflag='MA',hitflag='MAF',pausetime='0,8',ground__type='High',ground__hittime=22,ground__velocity=-3,air__velocity='-4,-5',getpower='40,10',givepower='20,10',hitsound='S0,1');end(n)
        state(1100,1100,velset='0,0');end(1100)
        ctl(1100,'Dribble','Explod','time=0',anim=6400,ID=6460,pos='85,-65',bindtime=-1,removetime=35,sprpriority=2,ownpal=1)
        state(1110,1110,kind='C',move='A',velset='0,0');hit(1110,12,85,kind='C',guard='L',fall=True,attr='C,SA')
        ctl(1110,'Purple slide','VelSet','time<19',x=5);ctl(1110,'Stop','VelSet','time>=19',x=0);end(1110)
        state(1120,1120,move='A',velset='0,0')
        ctl(1120,'Standing strike counter','ReversalDef','time=[10,21]',reversal__attr='S,NA,SA,HA',pausetime='0,0',sparkno=2,p1stateno=1121,p2stateno=8250);end(1120)
        state(1121,1121,move='A',velset='0,0');ctl(1121,'Counter hold','TargetBind','time<8',pos='120,0');ctl(1121,'Counter damage','TargetLifeAdd','time=8',value=-100,kill=1);ctl(1121,'Release','TargetState','time=8',value=8260);end(1121)
        state(1130,1130,velset='0,0');ctl(1130,'Baseline side switch','PosAdd','time=16',x='p2dist x+120');end(1130)
    else:
        for n,start,damage in [(1000,14,72),(1010,20,100),(1020,28,125)]:
            state(n,n,move='A',velset='0,0');hit(n,start,damage,fall=n!=1000,attr='S,SA');end(n)
            if slug=='rick':ctl(n,'Funk approach','VelSet',f'time<{start}',x=3)
        state(1100,1100,move='I' if slug=='negan' else 'A',velset='0,0')
        if slug=='rick':hit(1100,9,85,attr='S,SA')
        else:ctl(1100,'Whistle cue','PlaySnd','time=9',value='0,0')
        end(1100)
        state(1110,1110,move='A',velset='0,0');hit(1110,12,85,guard='L' if slug=='negan' else 'MA',fall=True,attr='C,SA' if slug=='negan' else 'S,SA')
        ctl(1110,'Approach','VelSet','time<12',x=3 if slug=='negan' else 5);ctl(1110,'Stop','VelSet','time>=12',x=0);end(1110)
        state(1120,1120,velset='0,0');ctl(1120,'Feint retreat','VelSet','time<10',x=-2 if slug=='negan' else -5);ctl(1120,'Stop','VelSet','time>=10',x=0);end(1120)
        if slug=='negan':
            # Reuse the validated capture/release states after a throw hit.
            state(1130,800,move='A',velset='0,0')
            ctl(1130,'Business Meeting grab','HitDef','time=5',attr='S,NT',hitflag='M-',priority='1,Miss',sparkno=-1,guard__dist=0,pausetime='0,0',p1stateno=801,p2stateno=8250,fall=1,numhits=0,getpower='0,0',givepower='0,0',id=1130);end(1130)
        else:
            state(1130,1130,move='A',velset='0,0');hit(1130,16,95,guard='H',fall=True,attr='S,SA');end(1130)
    state(1200,1200,move='A',velset='0,0');hit(1200,10,90,fall=True,attr='S,SA');end(1200)
    ctl(1200,'Rising impact','Explod','time=10',anim=6403,ID=6461,pos='80,-260',scale='.8,1.2',removetime=14,sprpriority=3,ownpal=1)
    state(1400,1400,velset='0,0');ctl(1400,'Retreat','VelSet','time<15',x=-6);ctl(1400,'Stop','VelSet','time>=15',x=0);end(1400)
    if forms:
        state(2000,2000,velset='0,0');ctl(2000,'Entry form','VarSet','time=0',**{'var(46)':'var(45)'})
        ctl(2000,'Toggle form','VarSet','time=18',**{'var(45)':'1-var(46)'})
        ctl(2000,'Same-frame reveal','ChangeAnim','time=18',value='ifelse(var(45)>0,12000,2000)',elem=2)
        ctl(2000,'Cooldown','VarSet','time=18',**{'var(47)':90})
        ctl(2000,'Form flash','PalFX','time=18',time=10,add='110,80,30',mul='256,256,256');end(2000)
        for n,start,damage,speed,guard in [(4100,8,75,6,'MA'),(4110,10,90,8,'MA'),(4130,10,65,5,'L'),(4200,8,90,0,'MA')]:
            state(n,n,move='A',velset='0,0');hit(n,start,damage,guard=guard,fall=True,attr='S,SA');ctl(n,'Scramble','VelSet',f'time<{start}',x=speed);ctl(n,'Stop','VelSet',f'time>={start}',x=0);end(n)
        state(4120,4120,velset='0,0');ctl(4120,'Backpedal','VelSet','time<15',x=-7);ctl(4120,'Stop','VelSet','time>=15',x=0);end(4120)
    finishers(a,slug,cfg,state,ctl,hit,end,forms)
    (O/(slug+'.cns')).write_text(core.cns)
    a.sounds(slug+'.snd',[(800,.13),(160,.14),(900,.07),(250,.42)])
    report={'character':cfg['name'],'slug':slug,'revision':1,'status':'Built; native validation pending','sprites':a.meta,
      'normals':{str(n):v[0] for n,v in N.items()},'specials':cfg['skills'],'supers':cfg['supers'],
      'super_damage':620,'ultimate_damage':950,'transformation':'Rick James <-> Tyrone Biggums' if forms else None,
      'limitations':['Nine key poses per look; shared attack/reaction drawings; further in-betweens, portraits and balance pending']}
    (S/'build-report.json').write_text(json.dumps(report,indent=2))
    print('CHAPPELLE_BUILT',slug,len(a.meta),'sprite metadata entries')

def finishers(a,slug,cfg,state,ctl,hit,end,forms):
    configs=[(3000,3010,1000,12,240,190,620,0),(3200,3210,2000,24,420,350,950,1)]
    if forms:configs += [(4400,4410,1000,10,240,190,620,2),(4500,4510,2000,22,420,350,950,3)]
    for starter,n,cost,start,total,last,damage,title in configs:
        state(starter,starter,move='A',velset='0,0',poweradd=-cost)
        ctl(starter,'Theatrical pause','SuperPause','time=0',time=16,anim=-1,movetime=0,unhittable=0)
        hit(starter,start,0,attr='S,HA',p1stateno=n,p2stateno=8250,getpower='0,0',givepower='0,0');end(starter)
        state(n,n,move='A',velset='0,0');ctl(n,'Entry direction','VarSet','time=0',**{'var(44)':'facing'})
        ctl(n,'Confirmed protection','NotHitBy',value='SCA',time=1);ctl(n,'Framing','ScreenBound',value=0,movecamera='0,0')
        ctl(n,'Pursuit','PosSet',f'time<{last-30}',x='camerapos x+var(44)*ifelse((time/20)%2=0,-210,210)',y='-55*abs(sin(time*.15))')
        ctl(n,'Final stance','PosSet',f'time>={last-30}',x='camerapos x-var(44)*280',y=0)
        ctl(n,'Face target','Turn','p2dist x<0')
        ctl(n,'Hold target','TargetBind',f'time<{last}',pos='(camerapos x-pos x)*facing,-150-90*abs(sin(time*.08))-pos y')
        ctl(n,'Backdrop','Explod','time=0',anim=6401,ID=6401,postype='left',pos='0,0',bindtime=-1,removetime=total,sprpriority=-10,ownpal=1)
        ctl(n,'Signature prop','Explod','time=0',anim=6402,ID=6402,postype='left',pos='640+var(44)*350,660',scale='1.4,1.4',bindtime=-1,removetime=total,sprpriority=-3,ownpal=1)
        ctl(n,'Afterimages','AfterImage','time=24',time=last-24,length=18,timegap=1,framegap=3,palcolor=0,palbright='25,0,35',palcontrast='190,130,256',trans='add')
        step=16 if total==240 else 12
        for tick in range(30,last-30,step):
            ctl(n,'Combo count','HitAdd',f'time={tick}',value=3)
            ctl(n,'Impact','Explod',f'time={tick}',anim=6405,ID=6405,postype='left',pos='640,390',scale='.4,.4',removetime=8,sprpriority=6,ownpal=1)
            ctl(n,'Impact cue','PlaySnd',f'time={tick}',value='0,1');ctl(n,'Shake','EnvShake',f'time={tick}',time=6,ampl=4,freq=80)
            if slug=='prince':
                ctl(n,'Royal ball rain','Explod',f'time={tick}',anim=6400,ID=6403,postype='left',pos=f'{350+(tick*19)%550},130',velocity='0,16',removetime=27,sprpriority=5,ownpal=1,scale='1.5,1.5')
            else:
                ctl(n,'Bat sweep' if slug=='negan' else 'Funk shockwave','Explod',f'time={tick}',anim=6403,ID=6403,postype='left',pos='640,390',facing='ifelse((time/12)%2=0,1,-1)',scale='1.6,1.6',removetime=12,sprpriority=5,ownpal=1)
        if slug=='prince' and title==1:
            ctl(n,'Pancakes served','Explod',f'time={last-30}',anim=6406,ID=6406,postype='left',pos='640,470',scale='1.8,1.8',bindtime=-1,removetime=80,sprpriority=5,ownpal=1)
        elif slug=='negan':
            for i in range(6):ctl(n,'Supply crate debris','Explod',f'time={last-20}',anim=6402,ID=6403,postype='left',pos=f'{440+i*80},400',velocity=f'{(i-3)*5},-10',accel='0,.5',scale='.35,.35',removetime=45,sprpriority=4,ownpal=1)
        else:
            ctl(n,'Disco finale','Explod',f'time={last-30}',anim=6406,ID=6406,postype='left',pos='640,170',scale='1.4,1.4',removetime=60,sprpriority=4,ownpal=1)
        ctl(n,'Huge final impact','Explod',f'time={last}',anim=6404,ID=6404,postype='left',pos='640,380',scale='5,5',removetime=20,sprpriority=6,ownpal=1)
        ctl(n,'Finisher title','Explod',f'time={last}',anim=6407+title,ID=6411,postype='left',pos='640,150',scale='1.1,1.1',bindtime=-1,removetime=45,sprpriority=8,ownpal=1)
        ctl(n,'Flash','EnvColor',f'time={last}',value='220,180,255',time=5,under=0)
        ctl(n,'Final quake','EnvShake',f'time={last}',time=20,ampl=18,freq=75)
        ctl(n,'Resolve once','TargetLifeAdd',f'time={last}',value=-damage,kill=1)
        ctl(n,'Release','TargetState',f'time={last}',value=8260);ctl(n,'Recover','ChangeState',f'time>={total-1}',value=0,ctrl=1)

if __name__=='__main__':
    # The user's two-pair correction supersedes standalone component builds.
    import runpy
    runpy.run_path(str(ROOT/'scripts/build-chappelle-pairs.py'),run_name='__main__')
