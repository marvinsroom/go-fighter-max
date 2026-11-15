"""Native combat and transformation validation for the new roster slots."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
def case(name,**kw):return dict(name=name,**kw)
BASE=[case(name,pulse=pulse,state=state,exact=damage,**extra) for name,pulse,state,damage,extra in [
 ('Standing light',1,200,30,{}),('Standing medium',2,210,52,{}),('Standing heavy',3,220,82,{}),
 ('Crouch light',1,400,26,{'down':True}),('Crouch medium',2,410,58,{'down':True}),('Crouch heavy',3,420,78,{'down':True})]]
BASE += [case('Air '+str(i),pulse=i,jump=True,state=590+i*10,damage=True) for i in [1,2,3]]
BASE += [case('Jump landing',jump=True),case('Walk forward',walk=1,state=20,noDamage=True),case('Walk backward',walk=-1,state=21,noDamage=True),case('Forward throw',pulse=7,state=801,exact=105),case('Back throw',pulse=7,back=True,state=811,exact=105)]
FINISH=[case('Super confirmed',pulse=5,state=3010,exact=620,power=2000),case('Super blocked',pulse=5,guard=True,notState=3010,noDamage=True,power=2000),case('Super needs meter',pulse=5,meter=0,notState=3000,noDamage=True,power=0),case('Super whiff',pulse=5,far=True,notState=3010,noDamage=True,power=2000),
 case('Ultimate confirmed',pulse=6,state=3210,exact=950,power=1000),case('Ultimate blocked',pulse=6,guard=True,notState=3210,noDamage=True,power=1000),case('Ultimate needs meter',pulse=6,meter=1000,notState=3200,noDamage=True,power=1000),case('Ultimate whiff',pulse=6,far=True,notState=3210,noDamage=True,power=1000),
 case('Standing guard',defend=True,state=150,noDamage=True),case('Crouch guard',defend=True,down=True,state=152,noDamage=True),
 case('Thrown by Will',actor=1,pulse=7,state=801,exact=110),case('Fresh Prince captures',actor=1,pulse=6,state=3210,exact=420),case('Agent J captures',actor=1,agentWill=True,pulse=6,state=4510,exact=390),case('Throw Agent J',agentWill=True,pulse=7,state=801,exact=105),case('Ultimate captures Agent J',agentWill=True,pulse=6,state=3210,exact=950)]
def cases_for(slug):
    out=list(BASE)
    if slug=='prince':
        out += [case('Royal Bounce '+str(i),pulse=8+i,state=1000+i*10,exact=d) for i,d in enumerate([48,60,72])]
        out += [case('Check Ball stance',pulse=4,state=1100,noDamage=True),case('Purple Slide',pulse=4,walk=1,state=1110,exact=85),case('Ruffle Counter whiff',pulse=4,walk=-1,state=1120,noDamage=True),case('Ruffle Counter catches strike',pulse=4,walk=-1,enemyAt=30,state=1121,exact=100),case('Baseline Cut',pulse=4,down=True,state=1130,noDamage=True),case('Royal Rejection',pulse=11,state=1200,exact=90),case('Slide Feint',pulse=12,state=1400,noDamage=True),
          case('Check Ball light branch',pulse=4,branch=1,state=1000,exact=48),case('Check Ball medium branch',pulse=4,branch=2,state=1130,noDamage=True),case('Check Ball heavy branch',pulse=4,branch=3,state=1200,exact=90)]
    elif slug=='negan':
        out += [case('Meet Lucille '+str(i),pulse=8+i,state=1000+i*10,exact=d) for i,d in enumerate([72,100,125])]
        out += [case('Whistle stance',pulse=4,state=1100,noDamage=True),case('Take a Knee',pulse=4,walk=1,state=1110,exact=85),case('Swing and a Miss',pulse=4,walk=-1,state=1120,noDamage=True),case('Business Meeting',pulse=4,down=True,state=801,exact=105),case('Back Off',pulse=11,state=1200,exact=90),
          case('Whistle light branch',pulse=4,branch=1,state=1000,exact=72),case('Whistle medium branch',pulse=4,branch=2,state=1110,exact=85),case('Whistle heavy branch',pulse=4,branch=3,state=1200,exact=90)]
    else:
        out += [case('Cold Blooded '+str(i),pulse=8+i,state=1000+i*10,exact=d) for i,d in enumerate([72,100,125])]
        out += [case('Unity Slap',pulse=4,state=1100,exact=85),case('Platform Rush',pulse=4,walk=1,state=1110,exact=85),case('Couch Surf',pulse=4,walk=-1,state=1120,noDamage=True),case('Couch Crusher',pulse=4,down=True,state=1130,exact=95),case('Funk Flash',pulse=11,state=1200,exact=90)]
        out += [case('Become Tyrone',pulse=13,state=2000,form=1,noDamage=True,power=3000),case('Return to Rick',tyrone=True,pulse=13,state=2000,form=0,noDamage=True,power=3000),case('Transformation free at zero meter',pulse=13,meter=0,state=2000,form=1,noDamage=True,power=0),case('Transformation preserves health',pulse=13,startLife=600,life=600,state=2000,form=1,noDamage=True),case('Transformation cooldown',pulse=13,probeAt=90,state=2000,form=1,noDamage=True)]
        out += [case('Tyrone light',tyrone=True,pulse=1,state=200,exact=30),case('Tyrone low',tyrone=True,pulse=1,down=True,state=400,exact=26),case('Tyrone heavy',tyrone=True,pulse=3,state=220,exact=82),case('Tyrone air',tyrone=True,pulse=3,jump=True,state=620,damage=True),case('Tyrone walk',tyrone=True,walk=1,state=20,noDamage=True),case('Tyrone throw',tyrone=True,pulse=7,state=801,exact=105),case('Tyrone incoming throw',tyrone=True,actor=1,pulse=7,state=801,exact=110),case('Tyrone incoming cinematic',tyrone=True,actor=1,pulse=6,state=3210,exact=420)]
        out += [case('Quick Rush',tyrone=True,pulse=4,state=4100,exact=75),case('Panic Lunge',tyrone=True,pulse=4,walk=1,state=4110,exact=90),case('Backpedal',tyrone=True,pulse=4,walk=-1,state=4120,noDamage=True),case('Floor Scramble',tyrone=True,pulse=4,down=True,state=4130,exact=65),case('Rising Flail',tyrone=True,pulse=11,state=4200,exact=90)]
        out += [case('Tyrone super',tyrone=True,pulse=5,state=4410,exact=620,power=2000),case('Tyrone super blocked',tyrone=True,pulse=5,guard=True,notState=4410,noDamage=True,power=2000),case('Tyrone super needs meter',tyrone=True,pulse=5,meter=0,notState=4400,noDamage=True,power=0),case('Tyrone ultimate',tyrone=True,pulse=6,state=4510,exact=950,power=1000),case('Tyrone ultimate blocked',tyrone=True,pulse=6,guard=True,notState=4510,noDamage=True,power=1000),case('Tyrone ultimate needs meter',tyrone=True,pulse=6,meter=1000,notState=4500,noDamage=True,power=1000)]
        out += [case('Tyrone normal hit reaction',tyrone=True,enemyAt=30,state=5000,noDamage=True,life=966),case('Tyrone captured by Agent J',tyrone=True,actor=1,agentWill=True,pulse=6,state=4510,exact=390)]
    return out+FINISH
def lua_value(v):
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,dict):return '{'+','.join(k+'='+lua_value(x) for k,x in v.items())+'}'
    if isinstance(v,list):return '{'+','.join(lua_value(x) for x in v)+'}'
    return str(v)
for slug in sys.argv[1:] or ['prince','negan','rick']:
    C=E/'chars'/slug
    (C/(slug+'_test.def')).write_text((C/(slug+'.def')).read_text().replace(f'st={slug}.cns',f'st={slug}.cns\nst1={slug}-tests.cns'))
    fixture='[Statedef -3]\n'
    for i,key in enumerate(['L','M','H','skill','super_short','ultimate_short','throw','special_light','special_medium','special_heavy','anti_air','back_light','transform','back_medium','back_heavy','side_switch'],1):fixture+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{key}"\nbuffer.time=1\n'
    if slug=='rick':fixture+='''
[State -3, Form setup]
type=VarSet
trigger1=map(test.form)>0
var(45)=map(test.form)-1
[State -3, Setup cooldown]
type=VarSet
trigger1=map(test.form)>0
var(47)=0
[State -3, Consume setup]
type=MapSet
trigger1=map(test.form)>0
map="test.form"
value=0
'''
    fixture+=(S/'chappelle-test-inputs.cns').read_text()
    (C/(slug+'-tests.cns')).write_text(fixture)
    cases=cases_for(slug)
    lua=(S/'chappelle-test-harness.lua').read_text().replace('CASE_DATA',lua_value(cases)).replace('CHAR_SLUG',slug).replace('CHAR_NAME',slug.title()).replace('CHAR_UPPER',slug.upper())
    lua=lua.replace('c.stefan and 2 or 1','c.tyrone and 2 or 1')
    lua=lua.replace('local form=_G[\'var\'](30)','local form=_G[\'var\'](45)')
    lua=lua.replace('local correct=group==0 or group==50','local correct=form==1 and (group==51 or group==10) or form==0 and (group==0 or group==50)')
    lua=lua.replace("if c.form and _G['var'](30)~=c.form then", "if c.form~=nil and _G['var'](45)~=c.form then")
    lua=lua.replace("mapSet('test.pulse',12)","mapSet('test.pulse',13)")
    lua=lua.replace('c.branch and tick==43','c.branch and tick==36')
    (E/'external/mods'/('-'+slug+'-combat-tests.lua')).write_text(lua)
    config=(E/'save/yamal-combat-tests.ini').read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-combat-tests.lua',config,flags=re.M)
    (E/'save'/(slug+'-combat-tests.ini')).write_text(config)
    (ROOT/'sprite-fighter/characters'/slug/'test-cases.json').write_text(json.dumps(cases,indent=2))
    print('CHAPPELLE_NATIVE_READY',slug,len(cases))
