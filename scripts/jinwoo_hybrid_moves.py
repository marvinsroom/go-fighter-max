"""Project summons, random forms and distinct form combat for the imported base."""
import jinwoo_super_power as super_power
FORMS=('igris','beru','iron','tank')
BASE=880000
TRANSFORM=870200
SUMMON=870100
FX=879800
PROFILES={
 'igris':{'body':(-10,-56,10,-3),'head':(-7,-61,8,-43),'width':(16,18),'speed':1,'reach':61,'normal':(35,64,100),'startup':(6,10,17),'skill':'Crimson Crosscut','super':'Crimson Tempest','ultimate':"Blood-Red Commander's Judgment",'color':(255,55,90)},
 'beru':{'body':(-18,-45,13,-2),'head':(6,-55,23,-30),'width':(20,22),'speed':1.3,'reach':47,'normal':(30,55,90),'startup':(4,8,13),'skill':'Predator Pounce','super':"Ant King's Hunt",'ultimate':'Black-Wing Annihilation','color':(95,175,255)},
 'iron':{'body':(-23,-58,23,0),'head':(-11,-65,12,-41),'width':(24,27),'speed':.75,'reach':65,'normal':(42,76,120),'startup':(9,15,23),'skill':'Bulwark Breaker','super':'Siegebreaker','ultimate':"Iron Fortress: Executioner's Fall",'color':(70,235,255)},
 'tank':{'body':(-43,-40,27,-3),'head':(15,-37,45,-13),'width':(40,44),'speed':.8,'reach':68,'normal':(45,80,130),'startup':(8,13,21),'skill':'Avalanche Rush','super':'Frozen Rampage','ultimate':"Winter King's Cataclysm",'color':(140,235,255)},
}


def base(form):return BASE+form*10000


def commands():
    # Xbox D-pad bridge / keyboard: Q+F/G/H/R → d+a / d+b / d+c / d+x
    # (Jinwoo Controls.txt). LT (w) stays summon — do not bind transforms to w.
    definitions='''
[Command]
name="our_tf_igris"
command=d+a
time=1
[Command]
name="our_tf_beru"
command=d+b
time=1
[Command]
name="our_tf_iron"
command=d+c
time=1
[Command]
name="our_tf_tank"
command=d+x
time=1
[Command]
name="our_summon"
command=w
time=1
[Command]
name="our_super"
command=c
time=1
[Command]
name="our_ultimate"
command=z
time=1
[Command]
name="our_signature"
command=x+c
time=1
[Command]
name="our_holdcharge"
command=/d
time=1
[Command]
name="our_holdcharge"
command=/start
time=1
[Command]
name="hold_d"
command=/d
time=1
[Command]
name="holdstart"
command=/start
time=1
[Command]
name="our_light"
command=a
time=1
[Command]
name="our_medium"
command=b
time=1
[Command]
name="our_grab"
command=x
time=1
[Command]
name="our_heavy"
command=y
time=1
[Command]
name="form_qcf"
command=~D,DF,F,a
time=20
[Command]
name="form_qcb"
command=~D,DB,B,b
time=20
[Command]
name="form_dp"
command=~F,D,DF,y
time=20
'''
    out=[]
    def route(label,value,conditions):
        out.append(f'\n[State -1, {label}]\ntype=ChangeState\n'+''.join('triggerall='+s+'\n' for s in ['!AILevel','roundstate=2','ctrl']+conditions[:-1])+'trigger1='+conditions[-1]+'\nvalue='+str(value)+'\nctrl=0\n')
    ground='statetype!=A'
    # Directed D-pad transforms are prepended in arsenal.commands so they beat A/B/X.
    # Charge = hold LB (button d) or Start — not down-direction.
    route('Imported meter and Ruler charge',500,[ground,'command="our_holdcharge"'])
    # Crouch only — walk/jump stay engine-hardcoded.
    out.append('\n[State -1, Crouch]\ntype=ChangeState\ntriggerall=!AILevel\ntriggerall=roundstate=2\ntriggerall=ctrl\ntriggerall=statetype!=A\ntriggerall=stateno!=10\ntriggerall=stateno!=11\ntrigger1=command="holddown"\nvalue=10\n')
    out.append('\n[State -1, Crouch to Stand]\ntype=ChangeState\ntriggerall=!AILevel\ntriggerall=roundstate=2\ntriggerall=stateno=11\ntrigger1=!command="holddown"\nvalue=12\n')
    route('Form signature',f'{BASE}+var(45)*10000+1000',[ground,'var(45)>0','command="our_signature" || command="our_summon"'])
    # RB = special-bar ultimates only (Mutilate / King Domain). Old form +320 cinematics removed.
    out.append('''
[State -1, Special-bar ultimate]
type=ChangeState
triggerall=!AILevel
triggerall=roundstate=2
triggerall=ctrl
triggerall=statetype!=A
triggerall=var(45)=0
triggerall=power>=2000
triggerall=numhelper(30990)
triggerall=helper(30990),fvar(8)=1
trigger1=command="our_ultimate"
value=cond(var(11)=1,3100,ifelse(var(10)>0,3100,3000))
ctrl=0
''')
    route('our_super',f'{BASE}+var(45)*10000+300',[ground,'var(45)>0','power>=1000','command="our_super"'])
    # Three identity-specific specials per playable shadow.  These routes must
    # precede the ordinary A/B/Y routes so completed motions win cleanly.
    route('Form quarter-circle special',f'{BASE}+var(45)*10000+1100',[ground,'var(45)>0','command="form_qcf"'])
    route('Form reverse special',f'{BASE}+var(45)*10000+1110',[ground,'var(45)>0','command="form_qcb"'])
    route('Form rising special',f'{BASE}+var(45)*10000+1120',[ground,'var(45)>0','command="form_dp"'])
    for index,direction in [(3,'command="holddown"'),(2,'command="holdback"'),(1,'command="holdfwd"'),(0,'1')]:
        route('Preserve assigned shadow',SUMMON+index,[ground,'var(45)=0','power>=250','var(31)=0',direction,'command="our_summon"'])
    route('Shadow air signature',f'{BASE}+var(45)*10000+1010',['var(45)>0','statetype=A','command="our_summon"'])
    for n,button in [(620,'c'),(610,'b'),(600,'a')]:route('Form air attack',f'{BASE}+var(45)*10000+{n}',['var(45)>0','statetype=A',f'command="{button}"'])
    for n,button in [(420,'c'),(410,'b'),(400,'a')]:route('Form low attack',f'{BASE}+var(45)*10000+{n}',['var(45)>0',ground,'command="holddown"',f'command="{button}"'])
    for n,button in [(220,'c'),(210,'b'),(200,'a')]:route('Form attack',f'{BASE}+var(45)*10000+{n}',['var(45)>0',ground,f'command="{button}"'])
    return definitions,''.join(out)


def states():
    lines=[]
    def state(n,anim=None,kind='S',move='I',**params):
        lines.extend([f'\n[Statedef {n}]',f'type={kind}',f'movetype={move}','physics=N','ctrl=0'])
        if anim is not None:lines.append('anim='+str(anim))
        lines.extend(f'{k}={v}' for k,v in params.items())
    def ctl(n,label,kind,trigger='1',**params):
        lines.extend([f'\n[State {n}, {label}]','type='+kind])
        lines.extend('trigger1='+t for t in (trigger if isinstance(trigger,list) else [trigger]))
        lines.extend(f'{k.replace("__",".")}={v}' for k,v in params.items())
    def end(n,total=None,air=False):ctl(n,'Recover','ChangeState',f'time>={total-1}' if total else 'animtime=0',value=50 if air else 0,ctrl=1)
    def hit(n,start,damage,reach,kind='S',guard='MA',chip=0,**params):
        values=dict(attr=kind+',SA',damage=f'{damage},{chip}',hitflag='MAFDE',guardflag=guard,priority='5,Hit',pausetime='4,8',sparkno=2,sparkxy='0,-35',hitsound='S5,13',guardsound='S5,13',ground__type='High',ground__hittime=20,ground__velocity='-4,-5',air__velocity='-4,-5',fall=1,getpower='20,5',givepower='10,5',id=n)
        values.update(params);ctl(n,'Contact','HitDef',f'time={start}',**values)
    # 870201–870204: D-pad / W directed transforms. Same form again returns to human.
    for form in range(1, 5):
        n = TRANSFORM + form
        state(n, f'{TRANSFORM}+var(45)*100', velset='0,0')
        ctl(n, 'Remember entry form', 'VarSet', '!time', **{'var(46)': 'var(45)'})
        ctl(n, f'Select {FORMS[form-1]} or return', 'VarSet', 'time=18',
            **{'var(45)': f'cond(var(46)={form},0,{form})'})
        ctl(n, 'Remember last summoned form', 'MapSet', ['time=18', 'var(45)>0'],
            map='"our.last_shadow"', value='var(45)')
        ctl(n, 'Reveal selected body', 'ChangeAnim', 'time=18',
            value=f'{TRANSFORM}+var(45)*100', elem=2)
        ctl(n, 'Shadow reveal', 'PalFX', 'time=18', time=10, add='35,5,70', mul='256,256,256')
        ctl(n, 'Clear previous body trails', 'AfterImageTime', '!time', time=0)
        end(n, 42)
    for i,(speed,damage,start) in enumerate([(4.5,100,12),(7,110,10),(3.5,125,16),(5.5,115,12)]):
        n=SUMMON+i;state(n,f'{n}+var(45)*10000',velset='0,0',poweradd=-250)
        ctl(n,'Summon cooldown','VarSet','!time',**{'var(31)':90})
        ctl(n,'Rotate summon technique','VarSet','!time',**{'var(32)':'(var(32)+1)%3'})
        ctl(n,'Assigned summon identity','VarSet','!time',**{'var(35)':i})
        # Each summon sheet is already registered relative to Jinwoo's world
        # height. A second 1.5x helper multiplier made every call oversized.
        ctl(n,'Named shadow attack','Helper',f'time={start}',helpertype='normal',name='"'+FORMS[i]+'"',ID=870700+i,stateno=f'{870700+i}+var(32)*20',postype='p1',pos='18,0',ownpal=1,keyctrl=0,size__xscale=1,size__yscale=1)
        end(n,66)
        for variant in range(3):
            helper=870700+i+variant*20;state(helper,helper,move='A',velset='0,0')
            if variant==0:
                hit(helper,6,damage,PROFILES[FORMS[i]]['reach'],attr='S,SP',getpower='0,0',givepower='15,5')
                ctl(helper,'Named shadow rush','VelSet','time=[1,22]',x=speed)
            elif variant==1:
                hit(helper,10,damage+25,PROFILES[FORMS[i]]['reach']+12,attr='S,SP',ground__velocity='-6,-7',air__velocity='-5,-7',getpower='0,0',givepower='15,5')
                ctl(helper,'Leaping intercept','VelSet','time=[1,12]',x=speed*.72,y=-2.4)
                ctl(helper,'Intercept gravity','VelAdd','time>12',y=.45)
            else:
                hit(helper,8,damage//2,PROFILES[FORMS[i]]['reach'],attr='S,SP',fall=0,ground__velocity='-1,0',getpower='0,0',givepower='8,3')
                hit(helper,16,damage,PROFILES[FORMS[i]]['reach']+8,attr='S,SP',getpower='0,0',givepower='15,5')
                ctl(helper,'Two-stage assault','VelSet','time=[1,20]',x=speed*.55)
            ctl(helper,'Finish rush','VelSet','time>24',x=0)
            ctl(helper,'Shadow dissolves','DestroySelf','time>=42')
    for form,name in enumerate(FORMS,1):
        cfg=PROFILES[name];b=base(form)
        for index,native in enumerate((200,210,220,400,410,420,600,610,620)):
            strength=index%3;n=b+native;air=native>=600;low=400<=native<600;startup=cfg['startup'][strength];damage=cfg['normal'][strength]
            state(n,n,kind='A' if air else 'C' if low else 'S',move='A',**({} if air else {'velset':'0,0'}))
            hit(n,startup,damage,cfg['reach'],kind='A' if air else 'C' if low else 'S',guard='H' if air else 'L' if low and strength<2 else 'MA')
            if name=='beru' and strength==1:hit(n,startup+5,damage//2,cfg['reach'],kind='A' if air else 'S',guard='H' if air else 'MA')
            if not air and not low:
                # Horizontal normals step forward and show form weapon FX.
                step={0:2.2,1:3.0,2:1.6}[strength]
                ctl(n,'Horizontal advance','VelSet',f'time=[{max(1,startup-2)},{startup+6}]',x=step)
                ctl(n,'Plant after slash','VelSet',f'time>{startup+6}',x=0)
                ctl(n,'Form attack effect','Explod',f'time={startup}',anim=FX+form,ID=879710+form,postype='p1',pos='34,-32',scale='.7,.7',sprpriority=4,ownpal=1,removetime=-2,persistent=0)
            if air:
                ctl(n,'Air gravity','VelAdd',y=.44)
                ctl(n,'Air landing','ChangeState',['vel y>0','pos y>=0'],value=52)
            end(n,air=air)
        for air in (False,True):
            n=b+(1010 if air else 1000);state(n,n,kind='A' if air else 'S',move='A',velset='0,0' if not air else '2,-1')
            hit(n,8 if air else 12 if name=='beru' else 20,145 if name in ('iron','tank') else 125,cfg['reach']+10,kind='A' if air else 'S',guard='H' if air else 'MA')
            ctl(n,'Signature approach','VelSet','time=[5,27]',x={'igris':3,'beru':5,'iron':1.5,'tank':4}[name])
            ctl(n,'Signature brake','VelSet','time>=28',x=0)
            if air:
                ctl(n,'Air gravity','VelAdd',y=.44);ctl(n,'Air landing','ChangeState',['vel y>0','pos y>=0'],value=52)
            end(n,air=air)
        # Motion-input specials reuse the existing, approved form artwork but
        # have distinct choreography, velocity and hit behavior per identity.
        specials={
          1100:((0,1,2,3,4),(5,11),0),
          1110:((9,10,6,7,11),(9,17),1),
          1120:((5,6,2,3,11),(7,13),2),
        }
        for offset,(poses,hits,variant) in specials.items():
            n=b+offset;state(n,n,move='A',velset='0,0',poweradd=-150)
            advance=((3.2,1.0,2.0),(5.2,2.0,3.8),(1.6,.8,2.4),(4.3,1.5,3.1))[form-1][variant]
            ctl(n,'Special movement','VelSet',f'time=[3,{hits[-1]+3}]',x=advance)
            for j,t in enumerate(hits):
                final=j==len(hits)-1
                hit(n,t,70+form*12+(25 if final else 0),cfg['reach']+10+variant*5,attr='S,SP',chip=5,
                    pausetime='5,9' if final else '3,5',ground__velocity='-5,-5' if final else '-2,0',
                    air__velocity='-5,-6' if final else '-3,-3',fall=1 if final else 0)
            end(n,42+variant*5)
    for form in range(5):
        b=base(form);name='jinwoo' if form==0 else FORMS[form-1]
        n=b+500;state(n,n,velset='0,0')
        ctl(n,'Charge meter','PowerAdd','time>=12',value=12)
        ctl(n,'Charge particles','Explod',['time>=12','time%16=0'],anim=FX+form,ID=879700+form,postype='p1',pos='0,-20',scale='.28,.65',removetime=-2,sprpriority=-1,ownpal=1)
        ctl(n,'Release charge','ChangeState',['time>=12','!command="our_holdcharge" || power>=powermax'],value=0,ctrl=1)
        # Supers are ordinary attacks in world space. Form cinematic ultimates removed;
        # human finishers use native Mutilate / King Domain / Antares (special bar).
        if form:
            cfg=PROFILES[name]
            n=b+300
            hits,damage,total,rush={1:((14,26),110,58,'cond(time>=8 && time<14,3,cond(time>=20 && time<26,1.5,0))'),
              2:((7,13,19,25),55,48,'cond(time>=2 && time<7,5,cond(time>=14 && time<19,2,0))'),
              3:((26,),260,68,'cond(time>=14 && time<26,1.5,0)'),
              4:((14,),240,62,'cond(time>=6 && time<24,5,0)')}[form]
            state(n,n,move='A',velset='0,0',poweradd=-1000)
            lines.append(super_power.start(n))
            ctl(n,'Physical super movement','VelSet',x=rush)
            for t in hits:
                final=t==hits[-1]
                hit(n,t,damage,cfg['reach'],attr='S,HA',chip=8,pausetime='7,12' if final else '3,6',sparkno=-1,guard__sparkno=-1,ground__hittime=28,ground__velocity='-5,-4' if final else '-1.5,0',air__velocity='-5,-5' if final else '-3,-4',fall=1 if final else 0,getpower='0,0',givepower='12,5')
                modern={1:879861,2:879860,3:879861,4:879862}[form]
                ctl(n,'Distinct super weapon energy','Explod',f'time={t}',anim=modern,ID=879841,postype='p1',pos='30,-30',scale='.9,.9',sprpriority=3,ownpal=1,removetime=-2,persistent=0)
                lines.append(super_power.impact(n,t,final))
            end(n,total)
    return '\n'.join(lines)+'\n'


def global_controllers():
    out='''
[State -2, Project summon cooldown]
type=VarAdd
triggerall=!ishelper
trigger1=var(31)>0
var(31)=-1
[State -2, Form reaction bank]
type=ChangeAnim
triggerall=!ishelper
triggerall=var(45)>0
triggerall=anim<1000000
trigger1=selfanimexist(anim+var(45)*1000000)
value=anim+var(45)*1000000
elem=animelemno(0)
[State -2, Full Ruler meter glow]
type=PalFX
triggerall=!ishelper
triggerall=numhelper(30990)
trigger1=helper(30990),fvar(8)=1
time=2
add=24,0,48
mul=280,240,320
sinadd=18,4,30,24
ignorehitpause=1
'''
    for form,name in enumerate(FORMS,1):
        back,front=PROFILES[name]['width']
        out+=f'\n[State -2, {name} body push width]\ntype=Width\ntriggerall=!ishelper\ntrigger1=var(45)={form}\nplayer={back},{front}\nedge={back},{front}\nignorehitpause=1\n'
    return out
