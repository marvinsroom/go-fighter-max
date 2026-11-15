"""Exercise all four existing kits through the corrected two-slot layout."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';CH=ROOT/'sprite-fighter/characters';E=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0'
def encode(v):
    if isinstance(v,bool):return str(v).lower()
    if isinstance(v,str):return json.dumps(v)
    if isinstance(v,dict):return '{'+','.join(k+'='+encode(x) for k,x in v.items())+'}'
    if isinstance(v,list):return '{'+','.join(encode(x) for x in v)+'}'
    return str(v)
for slug in ['prince','tyrone']:
    build=json.loads((CH/slug/'paired-build-report.json').read_text());cases=[]
    for form,source in enumerate(build['form_sources']):
        component=source['component'];selected=source['selected_source_form'];mapping={int(k):v for k,v in source['state_map'].items()}
        original=json.loads((CH/component/'test-cases.json').read_text())
        if component=='rick' and selected:
            # Full universal controls, Tyrone-specific specials/reactions, and
            # complete guard/meter/whiff/foreign-capture coverage.
            chosen=original[:14]+[c for c in original if c.get('tyrone') and c.get('pulse')!=13]+original[-15:]
        elif component=='rick':chosen=[c for c in original if not c.get('tyrone') and c.get('pulse')!=13 and not c['name'].startswith('Transformation')]
        else:chosen=original
        for original_case in chosen:
            c=dict(original_case);c['name']=build['forms'][form]+' / '+c['name'];c.pop('tyrone',None);c['pairAlt']=bool(form)
            if c.get('actor',2)==2:
                for key in ['state','notState']:
                    if key not in c:continue
                    n=c[key]
                    if selected:n={3000:4400,3010:4410,3200:4500,3210:4510}.get(n,n)
                    c[key]=mapping.get(n,n)
            cases.append(c)
    for alt in [False,True]:
        cases.append(dict(name='Actual toggle '+('return' if alt else 'activation'),pairAlt=alt,pulse=13,state=3900,form=0 if alt else 1,noDamage=True,power=3000))
        cases.append(dict(name='Toggle preserves health '+str(alt),pairAlt=alt,pulse=13,startLife=600,life=600,state=3900,form=0 if alt else 1,noDamage=True))
    cases += [dict(name='Transformation free at zero meter',pulse=13,meter=0,state=3900,form=1,noDamage=True,power=0),dict(name='Transformation cooldown',pulse=13,probeAt=90,state=3900,form=1,noDamage=True),dict(name='Alternate incoming normal',pairAlt=True,enemyAt=30,state=5000,noDamage=True,life=966)]
    for form,label in enumerate(build['forms']):
        shift=form*10000
        ground_damage={'Prince':95,'Rick James':105,'Tyrone Biggums':55,'Negan':90}[label]
        air_damage={'Prince':100,'Rick James':95,'Tyrone Biggums':90,'Negan':130}[label]
        for mode in ['hit','blocked','whiff']:
            c=dict(name=label+' / Signature ground '+mode,pairAlt=bool(form),pulse=18,state=1500+shift)
            if mode=='hit':c['exact']=ground_damage
            else:c.update(noDamage=True,guard=mode=='blocked',far=mode=='whiff',targetDown=label=='Rick James')
            if label=='Prince' and mode=='whiff':c['needBounce']=True
            cases.append(c)
            c=dict(name=label+' / Signature air '+mode,pairAlt=bool(form),pulse=4,jump=True,state=1510+shift)
            if mode=='hit':
                c['exact']=air_damage
                if label=='Rick James':c['requireState']=1512+shift
            else:c.update(noDamage=True,guard=mode=='blocked',far=mode=='whiff')
            cases.append(c)
        if label=='Negan':cases.append(dict(name='Negan / Full charge signature',pairAlt=True,pulse=18,state=11501,exact=145,holdSignature=True))
    C=E/'chars'/slug
    (C/(slug+'_paired_test.def')).write_text((C/(slug+'.def')).read_text().replace(f'st={slug}.cns',f'st={slug}.cns\nst1={slug}-paired-tests.cns'))
    fixture='[Statedef -3]\n'
    for i,key in enumerate(['L','M','H','skill','super_short','ultimate_short','throw','special_light','special_medium','special_heavy','anti_air','back_light','transform','back_medium','back_heavy','side_switch','holdup'],1):fixture+=f'\n[State -3, Test command]\ntype=AssertCommand\ntrigger1=map(test.pulse)={i}\nname="{key}"\nbuffer.time=1\n'
    fixture+='''
[State -3, Signature command]
type=AssertCommand
trigger1=map(test.pulse)=18
name="signature"
buffer.time=1
[State -3, Hold signature skill]
type=AssertCommand
trigger1=map(test.charge)>0
name="holdskill"
[State -3, Hold signature heavy]
type=AssertCommand
trigger1=map(test.charge)>0
name="holdheavy"

[State -3, Select pair form]
type=VarSet
trigger1=map(test.form)>0
var(45)=map(test.form)-1
[State -3, Clear pair cooldown]
type=VarSet
trigger1=map(test.form)>0
var(47)=0
[State -3, Consume pair setup]
type=MapSet
trigger1=map(test.form)>0
map="test.form"
value=0
'''+(S/'chappelle-test-inputs.cns').read_text()
    fixture=fixture.replace('stateno=0 || stateno=10 || stateno=21','stateno=0 || stateno=10 || stateno=21 || stateno=10000 || stateno=10010 || stateno=10021')
    if slug=='prince':fixture=fixture.replace('[Statedef -3]','''[Statedef -3]
[State -3, Track actual ball bounce]
type=MapSet
triggerall=numhelper(7600)>0
trigger1=helper(7600),var(0)>0
map="test.bounced"
value=1
''',1)
    (C/(slug+'-paired-tests.cns')).write_text(fixture)
    lua=(S/'chappelle-test-harness.lua').read_text().replace('CASE_DATA',encode(cases)).replace('CHAR_SLUG',slug).replace('CHAR_NAME',slug.title()+' pair').replace('CHAR_UPPER',slug.upper()+'_PAIR')
    lua=lua.replace('c.stefan and 2 or 1','c.pairAlt and 2 or 1').replace("local form=_G['var'](30)","local form=_G['var'](45)")
    lua=lua.replace('local correct=group==0 or group==50','local correct=form==1 and (group==51 or group==10) or form==0 and (group==0 or group==50)')
    lua=lua.replace("if c.form and _G['var'](30)~=c.form then", "if c.form~=nil and _G['var'](45)~=c.form then")
    lua=lua.replace("mapSet('test.pulse',12)","mapSet('test.pulse',13)")
    lua=lua.replace('c.branch and tick==43','c.branch and tick==36')
    lua=lua.replace('if c.jump then changeState(40)',"if c.jump then mapSet('test.pulse',17)")
    lua=lua.replace('actorFinal~=0 and actorFinal~=10','actorFinal~=0 and actorFinal~=10 and actorFinal~=10000 and actorFinal~=10010')
    lua=lua.replace('targetFinal~=0 and targetFinal~=10','targetFinal~=0 and targetFinal~=10 and targetFinal~=10000 and targetFinal~=10010')
    lua=lua.replace('runtime-validation.json','paired-runtime-validation.json')
    lua=lua.replace("'robotSeen','robotMissing','robotLeak'","'robotSeen','robotMissing','robotLeak','charge','bounced'")
    lua=lua.replace("  player(actor);setPower", "  player(actor);mapSet('test.charge',c.holdSignature and 1 or 0);setPower")
    lua=lua.replace("  if c.exact and damage~=c.exact then", "  if c.requireState and not seen[tostring(c.requireState)] then ok=false end\n  if c.needBounce and map('test.bounced')~=1 then ok=false end\n  if c.exact and damage~=c.exact then")
    (E/'external/mods'/('-'+slug+'-paired-tests.lua')).write_text(lua)
    config=(E/'save/yamal-combat-tests.ini').read_text()
    config=re.sub(r'^Modules\s*=.*$','Modules = external/mods/-'+slug+'-paired-tests.lua',config,flags=re.M)
    (E/'save'/(slug+'-paired-tests.ini')).write_text(config)
    (CH/slug/'paired-test-cases.json').write_text(json.dumps(cases,indent=2))
    print('CHAPPELLE_PAIR_TESTS',slug,len(cases))
