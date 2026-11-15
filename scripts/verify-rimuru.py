"""Verify source provenance, native results, sprite identity and local review links."""
import json,hashlib,re,sys
from pathlib import Path
from PIL import Image
from rimuru_source import ROOT,SOURCE,UP
from mugen_sff import Sff
import importlib.util
spec=importlib.util.spec_from_file_location('port',ROOT/'scripts/port-rimuru.py');port=importlib.util.module_from_spec(spec);spec.loader.exec_module(port)
report=json.loads((SOURCE/'runtime-validation.json').read_text());assert report['status']=='Complete' and report['failed']==0,report.get('checks')
checks={c['name']:c for c in report['checks']}
if (SOURCE/'forms-build.json').exists():
    forms=json.loads((SOURCE/'forms-build.json').read_text())
    assert len(forms['moves'])==51 and forms['attacks_per_form']==17
    for form in range(3):assert len([m for m in forms['moves'] if m['form']==form])==17
    for move in forms['moves']:
        name=move['form_name']+' / '+move['name']+' hit';check=checks[name]
        assert check['form']==move['form'] and check['damage']>0,name
        assert str(move['state']) in check['seen'],name
        if move['offset']==90:assert check['damage']==move['damage'] and str(move['confirmed']) in check['seen'],name
        if move['cost']:assert check['min_power']==3000-move['cost'],name
else:
    for name,damage in [('Tempest Sever hit',210),('Predator Collapse hit',300),('Megiddo',426),('Megiddo blocked',4),('Megiddo miss',0)]:assert checks[name]['damage']==damage,name
assert checks['Charge empty meter and release']['max_power']>=500
assert checks['Charge reaches full meter']['max_power']==3000
for name,form in [('Demon Lord transformation',1),('Slime transformation',2),('Return to masked human',0)]:assert checks[name]['form']==form,name
provenance=json.loads((SOURCE/'source/source-report.json').read_text());assert hashlib.sha256((SOURCE/'source'/provenance['archive']).read_bytes()).hexdigest()==provenance['sha256']
build=json.loads((SOURCE/'build-report.json').read_text());assert hashlib.sha256((UP/'Rimuru Demon Lord.sff').read_bytes()).hexdigest()==build['source_sha256']
for name,digest in build['runtime_sha256'].items():assert hashlib.sha256((port.OUT/name).read_bytes()).hexdigest()==digest,name
art,_=port.art();sff=Sff(port.OUT/'Rimuru Demon Lord.sff')
decoded={}
def sprite_hash(key):
    index=sff.keys[key]
    while sff.headers[index][10]==0:index=sff.headers[index][6]
    if index not in decoded:decoded[index]=hashlib.sha256(sff.decode(index).tobytes()).hexdigest()
    return decoded[index]
if (SOURCE/'forms-build.json').exists():
    for key,meta in forms['added_sprites'].items():
        g,n=map(int,key.split(','));assert sprite_hash((g,n))==meta['rgba_sha256'],key
    for key,meta in forms.get('cinematic_sprites',{}).items():
        g,n=map(int,key.split(','));assert sprite_hash((g,n))==meta['rgba_sha256'],key
    for name,digest in forms['art'].items():assert hashlib.sha256((SOURCE/'art/forms-v3'/name).read_bytes()).hexdigest()==digest,name
    for name,digest in forms.get('cinematic_art',{}).items():assert hashlib.sha256((SOURCE/'art/ultimates-v5'/name).read_bytes()).hexdigest()==digest,name
    assert forms['clean_casting']['frames']==8 and forms['clean_casting']['separate_effects']
    framing=json.loads((SOURCE/'framing-validation.json').read_text());assert framing['status']=='Passed' and framing['walk_drawings']==list(range(8)),framing['failures'][:5]
for key,meta in build['sprites'].items():
    g,n=map(int,key.split(','))
    if g==9000:continue
    assert sprite_hash((g,n))==art[meta['pose']]['rgba_sha256'],key
for i in range(8):assert sprite_hash((7900,i))==art[f'intro:{i}']['rgba_sha256']
complete=json.loads((SOURCE/'complete-build.json').read_text())
if (SOURCE/'art/complete-v2/effects-v4.png').exists():
    from rimuru_complete import load
    effects=load(SOURCE/'art/complete-v2','effects-v4',4,[0])
    assert len(effects)==16
    for i,effect in enumerate(effects):assert sprite_hash((7952,i))==effect['rgba_sha256'],('Complete effect drawing',i)
assert complete['replaced_effects']>=1000
for key,meta in complete['effect_sprites'].items():
    g,n=map(int,key.split(','));assert sprite_hash((g,n))==meta['rgba_sha256'],key
for filename,digest in complete['source_art'].items():assert hashlib.sha256((SOURCE/'art/complete-v2'/filename).read_bytes()).hexdigest()==digest
air=(port.OUT/'Rimuru Demon Lord.air').read_text(encoding='utf-8')
for number in complete['form_actions']:
    for offset in (20000,40000):assert f'[Begin Action {number+offset}]' in air,number
assert 'anim%20000' in (port.OUT/'common1.cns').read_text(encoding='utf-8')
for page in ['review.html','proportion-audit.html']:
    text=(SOURCE/page).read_text(encoding='utf-8')
    for target in re.findall(r'(?:src|href)="([^"]+)"',text):
        if not target.startswith(('http','#','data:')):assert (SOURCE/target.split('?')[0]).exists(),target
frames=report['frames']
for row in frames:
    with Image.open(SOURCE/'replays'/row.get('capture_directory',report['capture_directory'])/row['file']) as im:im.verify()
select=(port.E/'data/select.def').read_text();assert len(re.findall(r'^rimuru,',select,re.M))==1
for slug in ['cid_shadow','jinwoo','will_full','prince','tyrone','urkel','yamal']:assert re.search(r'^'+slug+',',select,re.M)
print('RIMURU_VERIFIED',report['passed'],'native checks;',len(build['sprites']),'illustrated body entries; 8 intro drawings;',len(frames),'decoded captures')
