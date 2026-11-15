"""Distinct technique choreography and the Endless Sky cinematic."""
import io,math,struct,wave
import numpy as np

ULTIMATE_BASE=600
ULTIMATE_VIOLE=680
ULTIMATE_TICKS=164

def powerfx(a,n,pose,t,pos='28,-31',scale='.10,.10',duration=18,**params):
    settings=dict(anim=9100+pose,ID=9100+pose,pos=pos,postype='p1',bindtime=1,removetime=duration,scale=scale,sprpriority=-2,ownpal=1,removeongethit=1)
    settings.update(params)
    a.ctl(n,'Shinsu choreography','Explod',f'time={t}',**settings)

def combat_actions(a):
    for n,frames,active,box in [
        (1000,[(1,14),(2,6),(3,8)],(1,),(8,-44,65,-10)),
        (1100,[(4,12),(5,6),(3,12)],(1,),(8,-44,65,-10)),
        (1200,[(6,32),(0,10)],(0,),(-11,-52,38,0)),
        (1201,[(6,6),(7,8),(3,10)],(),(0,0,0,0)),
        (1300,[(8,16),(9,8),(3,12)],(),(0,0,0,0)),
        (2000,[(10,12),(11,6),(12,6),(12,6),(13,6),(13,6),(3,14)],(1,3,5),(8,-45,76,-8)),
        (2100,[(6,32),(0,12)],(0,),(-11,-52,38,0)),
        (2101,[(7,8),(3,12)],(),(0,0,0,0)),
        (2200,[(14,20),(15,6),(14,8),(15,6),(3,14)],(1,3),(8,-46,88,-7)),
    ]:a.action(n,[(62400,p,t) for p,t in frames],active=active,box=box)
    a.action(3000,[(62600,0,12),(62600,1,12),(62600,2,8),(62600,7,10)],active=(2,),box=(8,-47,76,-6))
    a.action(3001,[(62600,p,t) for p,t in [(1,24),(2,24),(3,32),(4,24),(5,36),(6,12),(7,12)]])
    for i in range(16):a.animations[9100+i]=f'\n[Begin Action {9100+i}]\n63100,{i},0,0,-1\n'
    for n,p in [(9120,6),(9121,2)]:
        a.animations[n]=f'\n[Begin Action {n}]\n63100,{p},0,0,2,,,0.045,0.045\n63100,{p},0,0,3,,,0.075,0.075\n'
    a.animations[9010]='\n[Begin Action 9010]\nClsn1Default: 1\nClsn1[0]=-7,-7,7,7\n63100,3,0,0,4\n63100,3,0,0,4\nLoopStart\n63100,3,0,0,4\n'

def author_techniques(a,moves):
    st,ct=a.state,a.ctl
    for name,key,n,cost,label in moves:
        st(n,n,move='A',velset='0,0',poweradd=-cost)
        ct(n,'Technique wind','PlaySnd','time=3',value='0,5',volumescale=80)
        if n in (1200,2100):
            ct(n,'Reverse incoming strike','ReversalDef','time=1',reversal__attr='SCA,NA,SA,HA',pausetime='6,10',p1stateno=n+1,p2stateno=3050,sparkno=-1,hitsound='S0,6')
            powerfx(a,n,2,1,pos='9,-28',scale='.12,.17' if n==1200 else '.22,.26',duration=32,bindtime=-1)
        elif n==1300:
            powerfx(a,n,3,3,pos='17,-32',scale='.055,.055',duration=13,bindtime=-1)
            ct(n,'Release baang','Helper','time=16',name='"Shinsu Baang"',ID=10001,stateno=10001,postype='p1',pos='28,-31',ownpal=1,keyctrl=0)
            ct(n,'Release tone','PlaySnd','time=16',value='0,3')
        elif n==3000:
            ct(n,'Ultimate declaration','SuperPause','!time',time=12,movetime=0,anim=-1,darken=1,p2defmul=1,poweradd=0)
            ct(n,'Gathering roar','PlaySnd','!time',value='0,7')
            powerfx(a,n,7,1,pos='0,-2',scale='.22,.055',duration=35)
            powerfx(a,n,3,12,pos='20,-35',scale='.09,.09',duration=22)
            a.hit(n,24,40,attr='S,HA',damage='40,12',p1stateno=3001,p2stateno=3050,getpower='0,0',givepower='20,10')
        elif n==1100:
            ct(n,'Drive through space','VelSet','time=[5,12]',x=4)
            ct(n,'Plant the piercer','VelSet','time=13',x=0)
            ct(n,'Piercer afterimages','AfterImage','time=4',time=13,length=4,timegap=1,framegap=2,palcolor=0,palbright='0,15,35',palcontrast='140,200,230',trans='add1')
            a.hit(n,12,150,attr='S,SA',fall=True,getpower='0,0',pausetime='7,10',ground__velocity='5,-4')
            powerfx(a,n,1,7,pos='18,-29',scale='.18,.12',duration=16)
            ct(n,'Piercer impact','EnvShake','MoveHit',time=5,ampl=-3,freq=75,persistent=0)
        else:
            timing={1000:[14],2000:[12,24,36],2200:[20,34]}[n]
            if n==1000:
                ct(n,'Palm weight transfer','VelSet','time=[5,9]',x=1.8)
                ct(n,'Plant palm strike','VelSet','time=10',x=0)
            if n==2000:
                ct(n,'Butterfly advancing footwork','VelSet','time=[2,5]',x=2)
                ct(n,'Butterfly stance','VelSet','time=6',x=0)
            for j,t in enumerate(timing):
                a.hit(n,t,{1000:120,2000:90,2200:160}[n],attr='S,SA' if n==1000 else 'S,HA',fall=j==len(timing)-1 and n!=1000,getpower='0,0',ground__hittime=28,pausetime='5,7',**(dict(ground__velocity='3.5') if n==1000 else {}))
                powerfx(a,n,0 if n==1000 else 4 if n==2000 else 5,t,pos='32,-29',scale='.13,.12' if n!=2200 else '.22,.23',duration=14 if n!=2200 else 20)
                ct(n,'Technique impact','EnvShake',f'time={t+1} && MoveHit',time=4,ampl=-2 if n!=2200 else -4,freq=75)
        a.end(n)
    for n in (1201,2101):
        st(n,n,velset='0,0')
        ct(n,'Counter contact','TargetBind','time<10 && NumTarget>0',pos='34,0',time=1)
        ct(n,'Counter damage','TargetLifeAdd','!time && NumTarget>0',value=-120 if n==1201 else -200)
        ct(n,'Counter release','TargetState','time=10 && NumTarget>0',value=3051)
        powerfx(a,n,0 if n==1201 else 5,0,pos='28,-30',scale='.18,.18',duration=18)
        ct(n,'Counter punch','PlaySnd','!time',value='0,6')
        ct(n,'Counter impact','EnvShake','!time',time=5,ampl=-3,freq=70)
        a.end(n)
    st(10001,9010,kind='A',move='A',physics='N',bank=False,velset='4.8,0')
    ct(10001,'Baang silhouette','AngleDraw',scale='.10,.10')
    a.hit(10001,0,100,kind='A',attr='A,SP',fall=True,pausetime='0,6',getpower='0,0')
    powerfx(a,10001,14,0,pos='0,0',scale='.045,.045',duration=12)
    ct(10001,'Baang impact','EnvShake','MoveHit',time=4,ampl=-2,freq=75)
    ct(10001,'Retire baang','DestroySelf','time>=65 || MoveContact || root,stateno=99000 || frontedgebodydist<-40 || root,life<=0')

def author_ultimate(a):
    st,ct=a.state,a.ctl
    st(3001,3001,move='A',physics='N',velset='0,0')
    ct(3001,'Make room for the captured opponent','PosAdd','!time && frontedgebodydist<88',x='-(88-frontedgebodydist)')
    ct(3001,'Foreground silhouette','SprPriority',value=3)
    ct(3001,'Suspend captured opponent','TargetBind','time<140 && NumTarget>0',pos='48+ifelse(time>=92,10,0),ifelse(time<24,0,ifelse(time<60,-10,ifelse(time<128,-22,-10)))',time=1)
    ct(3001,'Cinematic protection','NotHitBy',value='SCA',time=1)
    ct(3001,'Field contrast','BGPalFX','!time',time=148,mul='95,120,165')
    ct(3001,'Moment of stillness','SuperPause','!time',time=8,movetime=0,anim=-1,darken=0,p2defmul=1,poweradd=0)
    powerfx(a,3001,8,0,pos='10,-42',scale='.24,.25',duration=96,bindtime=-1)
    powerfx(a,3001,7,0,pos='0,-2',scale='.30,.075',duration=144)
    powerfx(a,3001,9,24,pos='48,-37',scale='.17,.23',duration=87)
    powerfx(a,3001,10,56,pos='48,-42',scale='.14,.34',duration=28)
    powerfx(a,3001,15,88,pos='28,-37',scale='.27,.30',duration=40,anim='ifelse(map(baam.form)=1,9111,9115)')
    powerfx(a,3001,12,112,pos='23,-32',scale='.48,.32',duration=34,anim='ifelse(map(baam.form)=1,9113,9112)')
    powerfx(a,3001,14,128,pos='58,-33',scale='.24,.30',duration=24)
    for t,damage,amplitude in [(28,80,3),(60,100,4),(92,120,5),(128,'260+80*map(baam.form)',8)]:
        ct(3001,'Endless Sky contact','TargetLifeAdd',f'time={t} && NumTarget>0',value=f'-({damage})',kill=int(t==128))
        ct(3001,'Escalating impact','EnvShake',f'time={t}',time=5 if t<128 else 12,ampl=-amplitude,freq=75)
        ct(3001,'Impact audio','PlaySnd',f'time={t}',value='0,6' if t<128 else '0,8')
        if t<128:powerfx(a,3001,14,t,pos='48,-35',scale='.10,.13',duration=14)
    ct(3001,'Release flash','BGPalFX','time=128',time=5,add='95,110,135',mul='200,220,255')
    ct(3001,'Dissipating field','BGPalFX','time=144',time=20,mul='225,235,255')
    ct(3001,'Hurl opponent from release','TargetState','time=140 && NumTarget>0',value=3052)
    a.end(3001)
    st(3050,kind='S',move='H',physics='N',bank=False,velset='0,0')
    ct(3050,'Keep victim in camera framing','ScreenBound',value=1,movecamera='1,1')
    ct(3050,'Victim own hurt art','ChangeAnim','!time',value='5000+1000000*map(baam.form)')
    ct(3050,'Victim stays visible','SprPriority',value=4)
    ct(3050,'Emergency release','SelfState','time>=220',value=5050,ctrl=0)
    for n,velocity in [(3051,'2,-3'),(3052,'6,-5')]:
        st(n,kind='A',move='H',physics='N',bank=False,velset=velocity)
        ct(n,'Return victim own physics','SelfState',value=5050,ctrl=0)

def write_combat_sound(path):
    """Layered original wind, bass and noise; deterministic, no borrowed voices."""
    rng=np.random.default_rng(725);rate=22050;sounds=[]
    for i,(frequency,duration) in enumerate([(400,.12),(850,.10),(110,.28),(1200,.30),(140,.65),(650,.16),(85,.30),(55,1.0),(42,.85)]):
        t=np.arange(round(rate*duration))/rate;env=(1-t/duration)**2
        if i<5:signal=np.sin(2*math.pi*(frequency*t+120*t*t))*env*.33
        elif i==5:signal=rng.normal(0,.3,len(t))*np.sin(math.pi*t/duration)**2+np.sin(2*math.pi*(900*t-1700*t*t))*env*.15
        elif i==6:signal=(np.sin(2*math.pi*(85*t+30*(1-np.exp(-20*t))))*.45+rng.normal(0,.25,len(t)))*env
        elif i==7:signal=(np.sin(2*math.pi*(55*t+160*t*t))*.24+np.sin(2*math.pi*110*t)*.15+rng.normal(0,.13,len(t)))*np.sin(math.pi*t/duration)
        else:signal=(np.sin(2*math.pi*(42*t+12*(1-np.exp(-10*t))))*.45+rng.normal(0,.35,len(t)))*env
        pcm=(np.clip(signal,-.92,.92)*32767).astype('<i2').tobytes();stream=io.BytesIO()
        with wave.open(stream,'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(pcm)
        sounds.append(stream.getvalue())
    snd=bytearray(512);snd[:12]=b'ElecbyteSnd\0';snd[12:16]=bytes((0,0,0,1));struct.pack_into('<II',snd,16,len(sounds),512)
    for i,sound in enumerate(sounds):snd.extend(struct.pack('<IIII',len(snd)+16+len(sound) if i<len(sounds)-1 else 0,len(sound),0,i)+sound)
    path.write_bytes(snd)
