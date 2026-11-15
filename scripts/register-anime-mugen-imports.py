"""Register the two verified original imports and preserve earlier roster files."""
from pathlib import Path
import json,hashlib,shutil,re
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';E=S/'engine/ikemen-go-v1.0.0'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as stream:
  for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
old=json.loads((S/'face-audit/identity-scale-v5/profiles.json').read_text());preserved=[]
for row in old['fighters']:
 for name,digest in row['runtime_sha256'].items():assert sha(E/'chars'/row['engine']/name)==digest,('Earlier fighter changed',row['slug'],name)
 preserved.append(row['slug'])
print('PREVIOUS_ROSTER_PRESERVED',len(preserved),flush=True)
report=json.loads((S/'anime-import-validation.json').read_text())
for row in report['fighters']:
 slug=row['slug'];f=S/'characters'/slug;m=json.loads((f/'import-report.json').read_text());native=json.loads((f/'runtime-validation.json').read_text());browser=json.loads((f/'viewer-validation.json').read_text())
 assert native['status']=='Complete' and not native['failed'] and browser['status']=='PASS' and browser['review_sha256']==sha(f/'review.html')
 actual={name:sha(E/'chars'/slug/name) for name in m['source_files_sha256']};assert actual==m['source_files_sha256']==native['runtime_sha256']
 row['status']='Complete';row['browser']=browser;row['runtime_sha256']=actual
 source=f/'source/source-report.json';d=json.loads(source.read_text());d['creator']=m['creator'];d['status']='Original archive imported and native verified';source.write_text(json.dumps(d,indent=2));m['source']=d;(f/'import-report.json').write_text(json.dumps(m,indent=2))
select=E/'data/select.def';archive=S/'anime-import-backup';archive.mkdir(exist_ok=True)
if not (archive/'select.def').exists():shutil.copy2(select,archive/'select.def')
text=select.read_text()
for slug in ('naruto','saitama'):
 if not re.search(r'(?im)^\s*'+slug+r'\s*(?:,|$)',text):text=text.replace('[Characters]','[Characters]\n'+slug+', stages/stage0-720.def, order=1',1)
select.write_text(text)
entries=[]
for line in text.split('[Characters]',1)[1].splitlines():
 if line.strip().startswith('['):break
 if line.strip() and not line.lstrip().startswith(';'):entries.append(line.split(',')[0].strip())
assert len(entries)==len(set(entries))
engine_examples=[name for name in entries if name in ('kfm_zss','kfm720','kfm_zaxis','randomselect')]
entries=[name for name in entries if name not in engine_examples]
assert len(entries)==28
queue=json.loads((S/'anime-import-queue.json').read_text());queue['status']='Confirmed fighters imported; remaining names pending'
for row in queue['confirmed']:row['status']='Imported original MUGEN release; native and browser verified';row['review']='characters/'+row['slug']+'/review.html'
queue['artwork_stage']='Original MUGEN artwork retained. Any later illustrated upgrade is separate from this completed import.'
(S/'anime-import-queue.json').write_text(json.dumps(queue,indent=2))
report.update(status='Complete',roster_entries=entries,unchanged_engine_example_slots=engine_examples,preserved_existing_fighters=preserved,original_artwork_preserved=True,total_native_control_checks=sum(x['checks'] for x in report['fighters']),production_startup_matches=2,validation_scope='Natural production entrances/AI contact; original movement and selected command routes; Naruto base/Sage/chakra-form attacks, transformations and resource gates. Not an exhaustive audit of every upstream move.')
(S/'anime-import-validation.json').write_text(json.dumps(report,indent=2))
readme=S/'README.md';intro='**New original MUGEN imports: [Saitama and Naruto Shippuden](anime-imports.html).** Both are playable with the creators\' original sprites, voices and moves. Naruto includes Sage and Kurama forms; Saitama retains his original unkillable behavior. Open the import reviews for controls and native recordings. The roster now has 28 fighters; the earlier stature comparison covers the previous 26.\n\n';body=readme.read_text(encoding='utf-8')
if not body.startswith(intro):readme.write_text(intro+body,encoding='utf-8')
page=S/'face-audit/style-v4-review.html';body=page.read_text(encoding='utf-8');notice='<!-- anime-imports --><p style="padding:16px;background:#24364a"><a href="../anime-imports.html">New: original MUGEN Saitama and Naruto Shippuden imports, controls and native recordings</a></p><!-- /anime-imports -->'
if '<!-- anime-imports -->' not in body:page.write_text(body.replace('<main>','<main>'+notice,1),encoding='utf-8')
design=R/'design/roster.json';d=json.loads(design.read_text())
for row in report['fighters']:
 if not any(x['id']==row['slug'] for x in d['characters']):d['characters'].append(dict(id=row['slug'],name=row['name'],role='Original MUGEN import',firstPrototype=False,playableStatus='Native and browser verified original release',creator=row['creator'],review='sprite-fighter/characters/'+row['slug']+'/review.html',spritePackage='sprite-fighter/engine/ikemen-go-v1.0.0/chars/'+row['slug']))
design.write_text(json.dumps(d,indent=2))
with (R/'PROJECT_MEMORY.md').open('ab') as stream:stream.write(b'\n\n## Anime MUGEN imports COMPLETE (2026-10-21)\nConfirmed requested fighters SAITAMA and NARUTO SHIPPUDEN with SAGE/KURAMA. User explicitly instructed IMPORT FROM MUGEN FIRST. Imported original creator-linked packages: Saitama BoyBoyz (MFFA release MediaFire5g9ey4rupgd6ot5) and Naruto Mikel8888 edited by viniciusonico (release video l4aXsRu5Yr4, MediaFiresi0mmjlhlmgf638). Original archives/data preserved under characters/{slug}/source; production files byte-identical to original, only byte-identical folder-name DEF aliases added. No imagegen/reskin/rebalance. Naruto17 native checks PASS, Saitama8 PASS; BOTH natural production intro/AI contact matches PASS. Browser players desktop/narrow all121native captures PASS. Initial Saitama fixture failed8 because DEF inline comments prevented test-CNS replacement, corrected fixture and fresh8/0; production untouched. Original Naruto forms base/Sage/Ashura/KCM1/KCM2/four/six tails/Kurama avatar. Verified actual Sage/KCM1/KCM2/Kurama transitions, base reset and chakra/meter gates. Source controls preserved: Enter charge, holdS Sage, A KCM1, downA KCM2, S inKCM Kurama, D4tails/downD6tails, downS Ashura, downEnter exitchakraforms. Source Saitama intentionally unkillable; QCF+D SeriousPunch; QCF+S ConsecutivePunches. All26 earlier production hashes rechecked unchanged. select.def28unique entries, backup anime-import-backup/select.def. Play/FightCPU/Review launchers for Saitama and Naruto Shippuden. Hub anime-imports.html, proof anime-import-validation.json, saved queue anime-import-queue.json. Other requested anime names still await user; DO NOT GUESS. Source scale/pixel artwork retained for this first import phase. No further import work pending for these two.\n')
print('ANIME_MUGEN_IMPORTS_COMPLETE',len(entries),'fighters;',report['total_native_control_checks'],'native control checks; original26 preserved')
