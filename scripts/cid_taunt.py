"""Add a grounded, interruptible hood-adjusting taunt on the roster's W button."""
from pathlib import Path

DURATIONS=(8,10,10,12,78,12,10,10)


def install(out,art):
    out=Path(out)
    command=(out/'Cid.cmd').read_text(encoding='cp1252')
    start=command.lower().index('[statedef -1]')
    command=command[:start]+'[Command]\nname="cid_taunt"\ncommand=w\ntime=1\n\n'+command[start:]
    start=command.lower().index('[statedef -1]')+len('[statedef -1]')
    route='''
[State -1, Hood taunt]
type=ChangeState
triggerall=!AILevel
triggerall=statetype=S
triggerall=ctrl
trigger1=command="cid_taunt"
value=7900
'''
    command=command[:start]+'\n'+route+command[start:]
    (out/'Cid.cmd').write_text(command,encoding='utf-8')
    air=['\n[Begin Action 7900]']
    for n,ticks in enumerate(DURATIONS):
        scale=art[f'taunt:{n}']['scale']
        air.extend(['Clsn2: 1','Clsn2[0] = -20,-55,20,0',f'7900,{n},0,0,{ticks},,,{scale:.9f},{scale:.9f}'])
    with (out/'Cid.air').open('a',encoding='utf-8') as f:f.write('\n'.join(air)+'\n')
    state='''; Hood-adjusting taunt. No damage, resource change or invulnerability.
[Statedef 7900]
type=S
movetype=I
physics=S
anim=7900
ctrl=0
velset=0,0
sprpriority=2

[State 7900, Voice]
type=PlaySnd
trigger1=time=28
value=S10,6
channel=7
volumescale=80

[State 7900, Purple aura]
type=Explod
triggerall=time=[28,112]
trigger1=time%24=4
anim=550
ID=7901
postype=p1
pos=0,0
bindtime=-1
removetime=24
scale=.24*const(size.xscale),.24*const(size.yscale)
sprpriority=-2
ownpal=1
removeongethit=1

[State 7900, Aura glints]
type=Explod
triggerall=time=[36,108]
trigger1=time%18=0
anim=580
ID=7902
postype=p1
pos=-8,-30
bindtime=1
removetime=24
scale=.08,.08
sprpriority=3
ownpal=1
removeongethit=1

[State 7900, End aura]
type=RemoveExplod
trigger1=animtime=0
ID=7901

[State 7900, End glints]
type=RemoveExplod
trigger1=animtime=0
ID=7902

[State 7900, Recover]
type=ChangeState
trigger1=animtime=0
value=0
ctrl=1
'''
    (out/'cid_taunt.cns').write_text(state,encoding='utf-8')
    definition=(out/'cid_shadow.def').read_text(encoding='utf-8')
    (out/'cid_shadow.def').write_text(definition+'\nst6 = cid_taunt.cns\n',encoding='utf-8')
    return {'state':7900,'button':'W / P2 ]','duration_ticks':sum(DURATIONS),'voice':[10,6],
            'drawings':8,'grounded':True,'interruptible':True,'meter_cost':0,'damage':0}
