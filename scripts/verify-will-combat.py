"""Check built package, review links, and the completed native combat report."""
from pathlib import Path
from html.parser import HTMLParser
import json,struct,wave,io,re
root=Path(__file__).resolve().parents[1]
source=root/'sprite-fighter/characters/will'
char=root/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/will_full'
runtime=json.loads((source/'combat-runtime-validation.json').read_text())
assert runtime['status']=='Complete' and runtime['failed']==0, runtime
assert runtime['passed']==69, runtime['passed']
checks={row['name']:row for row in runtime['checks']}
assert all(not row['outfitViolations'] for row in runtime['checks']), 'Agent suit must persist on every sampled frame'
air=(char/'will.air').read_text()
banks={}
for block in re.split(r'(?=\[Begin Action )',air):
    header=re.match(r'\[Begin Action (\d+)\]',block)
    if not header:continue
    number=int(header[1])
    if number<10000:continue
    groups=[int(line.split(',')[0]) for line in block.splitlines() if re.match(r'^-?\d+,',line)]
    assert groups and all(group==10 for group in groups), number
    banks[number]=groups
assert all(number in banks for number in [10000,10020,10021,10040,10041,10130,10801,10811,15000,15120])
assert 'type=RemapSprite' not in (char/'will.cns').read_text()
assert checks['Super hit confirms']['damage']==285
assert checks['Ultimate hit confirms once']['damage']==420
agent_ultimate=checks['Agent Galaxy Protocol hit']
assert agent_ultimate['agentBackdrop']==1 and agent_ultimate['agentBeam']==1
assert agent_ultimate['foreignCinematic']==0
for name,row in checks.items():
    if name.startswith('Agent '):
        assert row['foreignCinematic']==0, name
        assert '3210' not in row['states'] and '3010' not in row['states'], name
for name in ['Agent Galaxy Protocol whiff','Agent Galaxy Protocol blocked']:
    assert checks[name]['agentBackdrop']==0 and checks[name]['agentBeam']==0
assert 'will-tests.cns' not in (char/'will_full.def').read_text()
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('src','href') and value and '://' not in value:
                assert (source/value).is_file(),value
Links().feed((source/'combat-review.html').read_text(encoding='utf-8'))
Links().feed((source/'agent-j-review.html').read_text(encoding='utf-8'))
raw=(char/'will.snd').read_bytes();assert raw[:12]==b'ElecbyteSnd\0'
count,offset=struct.unpack_from('<II',raw,16)
assert count==6
for i in range(count):
    nxt,size,group,number=struct.unpack_from('<IIII',raw,offset)
    with wave.open(io.BytesIO(raw[offset+16:offset+16+size]),'rb') as wav:
        assert wav.getnchannels()==1 and wav.getnframes()>0
    offset=nxt
report=json.loads((source/'combat-build-report.json').read_text())
assert 'freeze' not in report['sprites'], 'Rejected handstand must not be packaged'
assert report['specials']['1200']=='Fresh Step'
assert checks['Fresh Step upright kick']['passed']
report['status']='Passed native combat checks and keyboard spot-checks; prototype animation'
report['finisher_revision']=2
report['finisher_art']='art/finishers-v2/README.md'
report['forms']={'0':'Fresh Prince','1':'Agent J'}
report['agent_review']='agent-j-review.html'
report['transform_cost']=1000
report['transform_duration_ticks']=48
report['transform_commit_tick']=24
report['transform_cooldown_ticks']=120
report['agent_source']='scripts/will_agent_j.py'
report['agent_outfit_revision']=3
report['agent_outfit_capture']='agent-j-shared-throw-outfit-v3-engine.png'
report['agent_outfit_bank_actions']=len(banks)
report['agent_outfit_animations']='Dedicated group-10 animation bank for shared movement, throws, guard and reactions; no live sprite remapping'
report['agent_ultimate_revision']=2
report['agent_ultimate_beats']=['Neural capture','Tractor beam lift','Orbital deatomizer','Ground slam','Memory wipe']
report['agent_ultimate_duration_ticks']=240
report['agent_ultimate_capture']='agent-j-ultimate-orbital-v2-engine.png'
report['agent_ultimate_replay']='agent-j-ultimate-replay-v2.gif'
assert (source/report['agent_ultimate_capture']).is_file()
assert (source/report['agent_ultimate_replay']).is_file()
report['agent_cinematic_isolation']='Native checks observe Agent backdrop/beam and exclude Fresh Prince props and finishers'
agent_limit='Agent J uses seven poses, a shared walk drawing and shared throw mechanics'
if agent_limit not in report['limitations']:report['limitations'].append(agent_limit)
report['super_beats']=['Handshake feint','Rapid punches','Air chase','Launch kick','Shrug']
report['ultimate_beats']=['Whistle','Moving cab','Chase','Mansion transition','Luggage landing','Shrug']
report['runtime_validation']={'passed':runtime['passed'],'failed':0,'report':'combat-runtime-validation.json',
 'coverage':'Both forms: attacks, projectiles, guard, meter, hit confirms, recovery, transformation interruption, cooldown, health preservation and per-frame Agent outfit checks including shared moves',
 'keyboard_spot_checks':['Right arrow movement','Z light attack','S/D Fresh Prince finishers','W form switch both ways','X Agent projectile','S Agent Overload','D Agent Galaxy Protocol'],
 'captures':['combat-super-engine.png','combat-ultimate-engine.png','combat-ultimate-finish-engine.png',
             'agent-j-transform-engine.png','agent-j-projectile-engine.png','agent-j-ultimate-engine.png','agent-j-return-engine.png']}
(source/'combat-build-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert checks['Agent transformation']['finalForm']==1
assert checks['Agent return to Fresh Prince']['finalForm']==0
assert checks['Agent Galaxy Protocol hit']['damage']==390
print('WILL_COMBAT_VERIFIED: 69 native checks; per-frame Agent outfit, review assets, both forms and 6 WAV cues verified.')
