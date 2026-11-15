"""Monarch's dagger storm and deterministic full-army execution."""
import math

SUPER={'damage':620,'last':190,'total':240,'start':12}
ULTIMATE={'damage':950,'last':350,'total':420,'start':24}
SHADOW_MOVES=[
    {'name':'Igris','state':1100,'selection':0,'damage':100,'startup':20,'speed':2,'launch':'-5,-7'},
    {'name':'Beru','state':1110,'selection':1,'damage':110,'startup':14,'speed':8,'launch':'-9,-4'},
    {'name':'Iron','state':1120,'selection':2,'damage':125,'startup':30,'speed':0,'launch':'-6,-10'},
    {'name':'Tank','state':1130,'selection':3,'damage':115,'startup':18,'speed':6,'launch':'-8,-4'},
]

def effects(assets):
    # Existing cel drawings supply characters; these are game-native effects.
    def gate(x,y):
        nx=(x-127.5)/103;ny=(y-255.5)/230;r=math.hypot(nx,ny)
        edge=max(0,1-abs(r-1)/.045)
        rune=.7 if .88<r<.94 and math.cos(math.atan2(ny,nx)*24)>.55 else 0
        return (int(95+120*edge),int(25+125*edge),255,int(245*max(edge,rune)))
    assets.raw(4,256,512,gate,(128,512))
    def pillar(x,y):
        center=abs(x-63.5)/63.5
        a=max(0,1-center)**2*(.8+.2*math.sin(y*.23))
        return (int(120+135*a),int(25+220*a),255,int(a*255))
    assets.raw(5,128,512,pillar,(64,512))
    crown=[(28,155),(64,185),(86,104),(128,172),(170,104),(192,185),(228,155),(213,226),(43,226),(28,155)]
    def crest(x,y):
        for (ax,ay),(bx,by) in zip(crown,crown[1:]):
            t=max(0,min(1,((x-ax)*(bx-ax)+(y-ay)*(by-ay))/((bx-ax)**2+(by-ay)**2)))
            if math.hypot(x-ax-t*(bx-ax),y-ay-t*(by-ay))<2.5:return (200,145,255,235)
        return (0,0,0,0)
    assets.raw(6,256,256,crest,(128,256))
    assets.raw(7,256,256,lambda x,y:(200,155,255,int(230*max(0,1-abs(abs(x-127.5)-abs(y-127.5))/10)))
        if 12<x<244 and 12<y<244 else (0,0,0,0))

def animations(assets):
    a=assets.action;air=assets.air
    for n,cfg in [(3000,SUPER),(3200,ULTIMATE)]:
        a(n,[('dagger-cycle_1',4),('dagger-cycle_2',cfg['start']-4),('dagger-cycle_4',6),('dagger-cycle_7',28)],
            active=(2,),attack=(-900,-460,1100,0) if n==3200 else (0,-355,470,-50))
    a(3010,[(f'dagger-cycle_{i}',2) for _ in range(12) for i in range(8)]+[('summon',18),('idle',30)])
    a(3210,[('summon',48)]+[(f'dagger-cycle_{i}',3) for _ in range(12) for i in range(8)]+[('summon',24),('idle',60)])
    air.extend(['\n[Begin Action 6800]','7000,4,0,0,8,,,1,1','7000,4,0,0,-1,,,1.2,1.2',
        '\n[Begin Action 6801]','7000,5,0,0,6,,,1,1','7000,5,0,0,12,,,2,1.5','7000,5,0,0,12,,,3,1.5',
        '\n[Begin Action 6802]','7000,6,0,0,-1,,,1.2,1.2',
        '\n[Begin Action 6803]','7000,7,0,0,4,,,1,1','7000,7,0,0,8,,,3,3','7000,7,0,0,12,,,5,5',
        '\n[Begin Action 6804]','7000,0,0,0,90,,,1.6,1.6,-90'])

def states(state,ctl,hit,end,army_scale,army_bounds,shadows):
    for starter,confirmed,cost,cfg in [(3000,3010,1000,SUPER),(3200,3210,2000,ULTIMATE)]:
        state(starter,starter,move='A',velset='0,0',poweradd=-cost)
        ctl(starter,'Monarch awakening','SuperPause','time=0',time=16,anim=-1,movetime=0,unhittable=0)
        # Large, guardable starters: super catches farther out; ultimate covers
        # the screen. All cinematic damage still requires a confirmed hit.
        hit(starter,cfg['start'],0,attr='S,HA',p1stateno=confirmed,p2stateno=8250,getpower='0,0',givepower='0,0')
        end(starter)
    for n,cfg in [(3010,SUPER),(3210,ULTIMATE)]:
        last,total=cfg['last'],cfg['total']
        state(n,n,move='A',velset='0,0')
        ctl(n,'Remember entry direction','VarSet','time=0',**{'var(44)':'facing'})
        ctl(n,'Monarch protection','NotHitBy',value='SCA',time=1)
        ctl(n,'Domain framing','ScreenBound',value=0,movecamera='0,0')
        ctl(n,'Initial position','PosSet','time<48',x='camerapos x-var(44)*280',y=0)
        ctl(n,'Shadow exchange pursuit','PosSet',f'time=[48,{last-1}]',
            x='camerapos x+var(44)*ifelse((time/16)%2=0,-185,185)',y='-45*abs(sin(time*.15))')
        ctl(n,'Final position','PosSet',f'time>={last}',x='camerapos x-var(44)*280',y=0)
        ctl(n,'Face captured opponent','Turn','p2dist x<0')
        # Bind from world-camera coordinates so teleporting Jinwoo never
        # drags the victim from one side of the screen to the other.
        ctl(n,'Center victim','TargetBind',f'time<{last}',
            pos='(camerapos x-pos x)*facing,-170-80*abs(sin(time*.08))-pos y')
        ctl(n,'Shadow domain','Explod','time=0',anim=6401,ID=6401,postype='left',pos='0,0',bindtime=-1,
            removetime=total,sprpriority=-10,ownpal=1)
        ctl(n,'Monarch crown','Explod','time=0',anim=6802,ID=6802,postype='left',pos='640,230',bindtime=-1,
            removetime=last,sprpriority=-5,ownpal=1,scale='.65,.65')
        ctl(n,'Afterimage pursuit','AfterImage','time=36',time=last-36,length=20,timegap=1,framegap=2,
            palcolor=0,palbright='15,0,45',palcontrast='170,100,256',trans='add')
        for x in [140,1140]:
            ctl(n,'Shadow gate','Explod','time=0',anim=6800,ID=6800,postype='left',pos=f'{x},660',bindtime=-1,
                removetime=last,sprpriority=-4,ownpal=1)
        if n==3210:
            for i,(x,facing) in enumerate([(200,1),(490,1),(790,-1),(1080,-1)]):
                name=shadows[i];scale=army_scale(name,x,facing,.65)
                for frame in range(4):army_bounds(f'{name}_{frame}',x,facing,scale)
                ctl(n,name+' royal formation','Explod','time=0',anim=6600+i,ID=6402,postype='left',pos=f'{x},660',
                    facing=facing,scale=f'{scale},{scale}',bindtime=-1,removetime=total,sprpriority=-3,ownpal=1)
            # Tank crushes in, Iron launches, Igris cuts, Beru pursues, then a
            # full-army pincer. The choreography is deliberate on every cast.
            waves=[(48,3),(88,2),(128,0),(168,1),(208,3),(240,2),(272,0),(304,1),(336,0)]
            for i,name in enumerate(shadows):
                for side,(x,facing) in enumerate([(350,1),(930,-1)]):
                    scale=army_scale(name,x,facing,1.4)
                    for frame in range(4):army_bounds(f'{name}_{frame}',x,facing,scale)
                    for tick,leader in waves:
                        if i not in (leader,(leader+2)%4):continue
                        if side!=int(i!=leader):continue
                        ctl(n,name+' commanded assault','Explod',f'time={tick}',anim=6700+i,ID=6700+i,
                            postype='left',pos=f'{x},660',facing=facing,scale=f'{scale},{scale}',bindtime=-1,
                            removetime=40,sprpriority=3,ownpal=1)
        else:
            for tick in [48,96,144]:
                ctl(n,'Beru tandem claws','Explod',f'time={tick}',anim=6701,ID=6701,postype='left',pos='350,660',
                    facing=1,scale='1,1',bindtime=-1,removetime=32,sprpriority=3,ownpal=1)
        for tick in range(36,last,8 if n==3010 else 12):
            for x in [470+(tick*17)%330,510+(tick*29)%260]:
                ctl(n,'Dagger rain','Explod',f'time={tick}',anim=6804,ID=6804,postype='left',pos=f'{x},80',
                    velocity='0,24',removetime=23,sprpriority=5,ownpal=1)
        for tick in list(range(40,last,12 if n==3010 else 16))+[last]:
            ctl(n,'Royal barrage hit count','HitAdd',f'time={tick}',value=3 if n==3010 else 4)
            ctl(n,'Cross-cut impact','Explod',f'time={tick}',anim=6803,ID=6803,postype='left',pos='640,370',
                scale='.35,.35' if tick!=last else '.9,.9',removetime=-2,sprpriority=6,ownpal=1)
            ctl(n,'Impact cue','PlaySnd',f'time={tick}',value='0,3')
            ctl(n,'Impact quake','EnvShake',f'time={tick}',time=8,ampl=18 if tick==last else 4,freq=85)
        for tick in ([last] if n==3010 else [last-30,last-15,last]):
            for x in ([640] if n==3010 else [440,640,840]):
                ctl(n,'Monarch annihilation pillar','Explod',f'time={tick}',anim=6801,ID=6801,postype='left',pos=f'{x},660',
                    bindtime=-1,removetime=-2,sprpriority=6,ownpal=1)
        ctl(n,'Monarch final flash','EnvColor',f'time={last}',value='195,155,255',time=5,under=0)
        ctl(n,'Resolve damage once','TargetLifeAdd',f'time={last}',value=-cfg['damage'],kill=1)
        ctl(n,'Release opponent','TargetState',f'time={last}',value=8260)
        ctl(n,'Recover','ChangeState',f'time>={total-1}',value=0,ctrl=1)
