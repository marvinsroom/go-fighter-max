"""Audit the exact installed build, meaningful native results and review assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters/vikir';C=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/vikir'
b=json.loads((S/'build-report.json').read_text(encoding='utf-8'));r=json.loads((S/'runtime-validation.json').read_text(encoding='utf-8'))
assert r['status']=='Complete' and r['failed']==0
assert r['runtime_sha256']==b['runtime_sha256']
for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((C/name).read_bytes()).hexdigest()==digest,name
for p in S.glob('vikir.*'):assert p.read_bytes()==(C/p.name).read_bytes(),p
for m in b['poses'].values():assert hashlib.sha256((R/m['file']).read_bytes()).hexdigest()==m['sha256']
body=[m for m in b['poses'].values() if m['group'] in range(50,58)]
for m in body:
    if m.get('comic_redraw'):
        # New portraits and bodies have fresh ink contours; the old head
        # landmark measurement describes the archived art. Check the actual
        # compiled replacement and its preserved visible height instead.
        from mugen_sff import Sff
        if 'comic_archive' not in globals():
            comic_archive=Sff(C/'vikir.sff')
            comic_poses=json.loads((S/'art/comic-identity-v3/installed.json').read_text())['poses']
        key=(m['group'],m['number'])
        pose=next(p for p in comic_poses if list(key) in p['keys'])
        with Image.open(R/m['file']) as image:
            assert image.height==pose['old_bounds'][3]-pose['old_bounds'][1]
            assert image.tobytes()==comic_archive.decode(comic_archive.keys[key]).tobytes()
    elif m['group']!=52:assert abs(m['head_span']*m['scale']-76)<1e-6,m['file']
assert len(body)==164
guest_art=[m for m in b['poses'].values() if m['group'] in range(70,74)]
assert len(guest_art)==32
assert {g['name'] for g in b['guests']}=={'Dolores','Camu','Aiyen','Sinclair'}
assert b['archery']['form']==3 and b['archery']['release_tick']==28
air=(C/'vikir.air').read_text(encoding='utf-8');actions=re.findall(r'\[Begin Action (\d+)\]',air);assert len(actions)==len(set(actions))
for n in [0,20,21,40,43,120,130,140,5000,5030,5110,5120,700,710]:assert all(str(n+offset) in actions for offset in [0,10000,20000,30000]),n
for n in [200,210,220,400,410,420,600,610,620,1000,1100,3000,3100,4000,4500,4510]:assert all(str(n+offset) in actions for offset in [0,10000,30000]),n
lookup={(m['group'],m['number']) for m in b['poses'].values()}
for line in air.splitlines():
    if re.match(r'^\d+,\d+,',line):assert tuple(map(int,line.split(',')[:2])) in lookup,line
for n in [0,20,21,40,43,5000,5030]:
    block=re.search(r'\[Begin Action '+str(20000+n)+r'\]([^\[]*(?:\[0\][^\[]*)*)',air)
    assert block and '-55,-100,60,0' in block[0],n
assert 'portraitscale=.125' in (C/'vikir.def').read_text(encoding='utf-8')
portrait=b['poses']['portrait0'];assert portrait['axis']==[0,0]
with Image.open(R/portrait['file']) as im:
    box=im.getchannel('A').getbbox();assert im.size==(200,200) and box[0]>=15 and box[1]>=15 and box[2]<=185 and box[3]<=185
checks={c['name']:c for c in r['checks']}
for title in ['Vikir','Night Hound','Choco','Academy']:
    for guest in ['Dolores','Camu','Aiyen','Sinclair']:
        c=checks[title+' / Guest '+guest]
        assert c['passed'] and c['max_guest']==1 and c['guest_cleanup']==0,(title,guest)
for suffix in ['shot','long range','facing left','blocked']:
    c=checks['Academy / Anubis '+suffix]
    assert c['passed'] and (c['max_projectiles']>0 or c['damage']>0),suffix
assert checks['Academy / Anubis long range']['max_projectiles']>0,'Long-range arrow must travel visibly'
for name in ['Dolores healing cap','Dolores interrupted before heal','Shared guest cooldown','Guest cooldown blocks ultimate fallback','Anubis requires academy outfit']:
    assert checks[name]['passed'],name
for guest in ['Dolores','Camu','Aiyen','Sinclair']:
    assert any(f['case_name']=='Vikir / Guest '+guest and f.get('guest_count',0)==1 for f in r['frames']),(guest,'native capture must show the ally')
assert any(f['case_name']=='Academy / Anubis long range' and f.get('projectiles',0)>0 for f in r['frames']),'Capture must show the traveling Anubis arrow'
cns=(C/'vikir.cns').read_text(encoding='utf-8')
bow_state=cns.split('[Statedef 1400]',1)[1].split('[Statedef ',1)[0]
assert 'type=Projectile' in bow_state and 'trigger1=time=28' in bow_state
animation=json.loads((S/'animation-data.js').read_text().split('=',1)[1].removesuffix(';'))
assert animation['220']['frames'][1]['key']=='c7','Descending Fang must contact on the downward cut'
assert all(f['key']!='p7' for f in animation['4000']['frames'][:-1]),'Seven Fangs must not stand up between cuts'
for form,title in enumerate(['Vikir','Night Hound','Choco','Academy']):
    idle=animation[str(form*10000)]['frames'];assert len(idle)==1 and idle[0]['ticks']==-1,(title,'idle must not shuffle drawings')
    assert checks[title+' idle']['passed']
for n in [3000,3100,4000]:
    for form,group in [(0,54),(1,55),(3,56)]:
        assert all(f['group'] in (group,{0:50,1:51,3:53}[form]) for f in animation[str(form*10000+n)]['frames']),(form,n)
        assert animation[str(form*10000+n)]['frames'][-1]['key']=={0:'m0',1:'n0',3:'a0'}[form],(form,n,'recovery must reuse neutral body')
    frames=animation[str(n)]['frames'];spec=b['power_clips'][str(n)]
    assert spec['hit_ticks']==[sum(f['ticks'] for f in frames[:i]) for i in spec['active_frames']]
for name,case in checks.items():
    if name.startswith('Keyboard /'):
        target=next(t['state'] for t in json.loads((S/'gameplay-test-cases.json').read_text()) if t['name']==name)
        assert case['state_ticks'][str(target)]<23,(name,'must activate on press before release at tick 23')
for title in ['Vikir','Night Hound','Choco','Academy']:
    assert checks[title+' / Seven Fangs']['damage']>=280,(title,'super must land its seven-hit sequence')
    seen={f['drawing'] for f in r['frames'] if f['case_name']==title+' / Seven Fangs' and f['state']==4000}
    assert {1,3,6,12,13,14,15}<=seen,(title,'Seven Fangs capture skips strike poses',seen)
for title in ['Vikir','Night Hound','Choco','Academy']:
    c=checks[title+' / Night Hound: Crimson Execution'];assert c['passed'] and c['damage']>=500 and '4510' in c['seen'],title
    frames=[f for f in r['frames'] if f['case_name']==title+' / Night Hound: Crimson Execution']
    assert any(f['state']==4510 and f['fx_count']>0 for f in frames),(title,'cinematic effects must be captured')
for name in ['Crimson Execution blocked','Crimson Execution miss','Crimson Execution insufficient meter','Crimson Execution empty meter','Crimson Execution interrupted opener','Crimson Execution corner -1','Crimson Execution corner 1','Seven Fangs two-bar keyboard super','Charge release stops power gain']:assert checks[name]['passed'],name
for n in [7140,7150]:
    block=air.split('[Begin Action '+str(n)+']',1)[1].split('[Begin Action ',1)[0]
    assert len(re.findall(r'^91,',block,re.M))==4,(n,'arrows require four animated frames')
assert len({b['poses']['vfx'+str(i)]['sha256'] for i in range(8)})==8
for name in ['Vikir / Seven Fangs','Night Hound / Seven Fangs','Choco / Seven Fangs','Seven Fangs facing left','Choco high strike hurtbox','Choco low strike hurtbox','Keyboard / Q changes appearance','Keyboard / down+Q restores Vikir','Light medium heavy combo','Normal cancels into lunge']:assert checks[name]['passed'],name
for name,c in checks.items():
    if '/ Beelzebub Blood Draw' in name:assert c['self_life']==855,name
    if name.startswith('Beelzebub Blood Draw ') and not name.endswith('insufficient meter'):assert c['self_life']==800,name
for f in r['frames']:
    if f['state'] not in (700,710) and f['form'] in (1,2,3):
        expected={1:{51,55},2:{52},3:{53,56,57}}[f['form']]
        assert f['group'] in expected,(f['case_name'],f['state'],f['form'],f['group'],'outfit flash')
    with Image.open(S/'replays'/f.get('capture_directory',r['capture_directory'])/f['file']) as im:assert im.size==(1280,720);im.verify()
assert len({f['case_name'] for f in r['frames']})>=60
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):self.links += [v for k,v in attrs if k in ('href','src')]
links=0
for filename in ['review.html','animation-review.html','proportion-audit.html']:
    p=S/filename;parser=Links();parser.feed(p.read_text(encoding='utf-8'))
    for link in parser.links:
        u=urlsplit(link)
        if not u.scheme and u.path:assert (p.parent/unquote(u.path)).exists(),link;links+=1
result=dict(status='Complete',native_checks=r['passed'],native_clips=len({f['case_name'] for f in r['frames']}),native_frames=len(r['frames']),original_body_drawings=len(body),shared_scale_banks=len({m['bank'] for m in body}),local_links=links,runtime_sha256=b['runtime_sha256'])
(S/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('VIKIR_VERIFIED',result['native_checks'],'checks;',result['native_clips'],'clips;',result['native_frames'],'frames')
