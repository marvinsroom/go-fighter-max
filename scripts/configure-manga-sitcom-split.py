"""Configure separate game rosters after moving files with PowerShell."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit
import json,re,os,hashlib,html
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';S=G/'sitcom';E=G/'engine/ikemen-go-v1.0.0';SE=S/'engine/ikemen-go-v1.0.0'
slugs=['will','prince','tyrone','urkel','yamal','rick','negan','chappelle']
if (S/'split-manifest.json').exists():raise SystemExit('Already configured; inspect split-manifest.json before changing this migration.')
engines=['will_full','will_idle','will_motion','prince','tyrone','urkel','yamal','rick','negan']
selected={'will_full','prince','tyrone','urkel','yamal'}
original=(S/'before/main-select.def').read_text()
authored={r['engine'] for r in json.loads((G/'jus-upgrade/manifest.json').read_text())['fighters']}|selected
def filter_roster(want):
 active=False;lines=[];entries=[]
 for line in original.splitlines():
  if line.lstrip().startswith('['):active=line.strip().lower()=='[characters]'
  key=line.split(';')[0].split(',')[0].strip()
  if active and key and not key.startswith('['):
   if key=='randomselect':lines.append(line);continue
   if key not in authored:continue
   if (key in selected)!=want:continue
   entries.append(key)
  lines.append(line)
 return '\n'.join(lines)+'\n',entries
main,main_entries=filter_roster(False);sitcom,sitcom_entries=filter_roster(True)
assert len(main_entries)==23 and len(sitcom_entries)==5
(E/'data/select.def').write_text(main);(SE/'data/select.def').write_text(sitcom)
for engine,title in [(E,'Manga vs Manhwa'),(SE,'Sitcom Fighter')]:
 p=engine/'save/config.ini';t=p.read_text();t=re.sub(r'(?im)^(WindowTitle\s*=).*$',lambda m:m[1]+' '+title,t);p.write_text(t)
# Production Play/CPU commands use an opponent from this game's own roster.
changed=[]
for p in (R/'scripts').glob('run-*.ps1'):
 if re.search(r'will|chappelle|urkel|yamal|prince|tyrone|negan|rick',p.name,re.I):continue
 t=p.read_text();new=t.replace("'will_full'","'naruto'")
 if new!=t:
  backup=S/'before/scripts'/p.name;backup.parent.mkdir(parents=True,exist_ok=True)
  if not backup.exists():backup.write_text(t)
  p.write_text(new);changed.append(p.name)
# Repair active review links relative to their old and new locations. Preserve
# original provenance JSON and prompts verbatim.
mapping=[(G/'characters'/s,S/'characters'/s) for s in slugs]+[(E/'chars'/s,SE/'chars'/s) for s in engines]
def relocate(path):
 for old,new in mapping:
  try:return new/path.relative_to(old)
  except ValueError:pass
 return path
link_changes=0
for slug in slugs:
 base=S/'characters'/slug
 if not base.exists():continue
 for p in base.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in ('.html','.js','.css'):continue
  old_file=G/'characters'/slug/p.relative_to(base)
  try:text=p.read_text(encoding='utf-8')
  except UnicodeDecodeError:continue
  def rewrite(m):
   global link_changes
   value=m['url'];u=urlsplit(value)
   if u.scheme or u.netloc:return m[0]
   old_target=(old_file.parent/u.path).resolve();new_target=relocate(old_target)
   relative=os.path.relpath(new_target,p.parent).replace('\\','/')
   result=urlunsplit(('', '',relative,u.query,u.fragment))
   if result!=value:link_changes+=1
   return m['quote']+result+m['quote']
  new=re.sub(r'''(?P<quote>["'])(?P<url>(?:\.\./)+[^"'<>\r\n]+)(?P=quote)''',rewrite,text)
  if new!=text:p.write_text(new,encoding='utf-8')
# The active JUS work now covers the main manga/manhwa roster. Keep the prior
# roster as historical evidence; no recording runs are started here.
J=G/'jus-upgrade';manifest=J/'manifest.json';d=json.loads(manifest.read_text())
backup=S/'before/jus-manifest.json'
if not backup.exists():backup.write_text(json.dumps(d,indent=2))
d['fighters']=[row for row in d['fighters'] if row['engine'] not in selected]
d['scope']='All 23 playable manga and manhwa fighters and their existing forms'
d['status']='Fixes in progress; recordings deferred at user request'
d['animation_status']='46 eight-drawing walk cycles retained for this roster (368 drawings); sitcom cycles are preserved separately.'
d['validation_status']='Earlier 28-fighter checks are historical after the roster split; fresh captures deferred.'
manifest.write_text(json.dumps(d,indent=2))
inventory=J/'animation-cycles.json';cycles=json.loads(inventory.read_text());cycles['cycles']=[c for c in cycles['cycles'] if c['slug']!='urkel'];cycles['status']='37 form-specific banks installed for the manga/manhwa roster; recordings deferred.';inventory.write_text(json.dumps(cycles,indent=2))
# Existing aggregate reports are historical, not evidence for the new roster.
for name in ['completion.json','native-mobility-validation.json','native-combat-validation.json','native-form-validation.json','native-camera-validation.json','browser-validation.json']:
 p=J/name
 if not p.exists():continue
 target=S/'before/jus-reports'/name;target.parent.mkdir(parents=True,exist_ok=True)
 if not target.exists():target.write_bytes(p.read_bytes())
 value=json.loads(p.read_text());value['status']='Historical: before manga/manhwa roster split; new recordings deferred';p.write_text(json.dumps(value,indent=2))
labels={'will_full':'Will','prince':'Prince / Rick James','tyrone':'Tyrone / Negan','urkel':'Urkel / Stefan','yamal':'Yamal'}
for engine in sitcom_entries:
 label={'will_full':'Will','prince':'Prince','tyrone':'Tyrone','urkel':'Urkel','yamal':'Yamal'}[engine]
 for cpu in [False,True]:
  filename=('Fight '+label+' CPU.cmd') if cpu else ('Play '+label+'.cmd')
  opponent='prince' if engine=='will_full' else 'will_full'
  cmd='@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-sitcom.ps1" -Character '+engine+' -Opponent '+opponent+(' -CPU' if cpu else '')+'\n'
  (S/filename).write_text(cmd)
(S/'Play Chappelle Pairs.cmd').write_text('@echo off\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-sitcom.ps1" -Character prince -Opponent tyrone\n')
def roster_page(title,rows):
 cards=''.join('<li><a href="characters/'+slug+'/review.html">'+html.escape(label)+'</a></li>' for slug,label in rows)
 return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>body{background:#111824;color:#eef2fa;font:18px/1.6 system-ui;max-width:960px;margin:40px auto;padding:20px}a{color:#a8d9ff}ul{columns:2;column-width:240px}li{margin:12px 0}</style><h1>'+title+'</h1><p>'+str(len(rows))+' playable fighters.</p><ul>'+cards+'</ul></html>'
rows=[(next(r['slug'] for r in d['fighters'] if r['engine']==engine),next(r['slug'] for r in d['fighters'] if r['engine']==engine).replace('-',' ').title()) for engine in main_entries]
(G/'roster.html').write_text(roster_page('Manga vs Manhwa',rows),encoding='utf-8')
(S/'roster.html').write_text(roster_page('Sitcom Fighter',[(engine.replace('will_full','will'),labels[engine]) for engine in sitcom_entries]),encoding='utf-8')
old=G/'README.md';b=S/'before/main-README.md'
if not b.exists():b.write_bytes(old.read_bytes())
old.write_text('''# Manga vs Manhwa

23 playable manga and manhwa fighters. Open **Launch Manga vs Manhwa.cmd** to play, or [the roster](roster.html) for character reviews and controls.

The current illustrated JUS movement fixes are retained: compact proportions, aerial dashes/pursuit, launchers, flight for eligible characters, and reactive Training Room scenery. [Shared controls](jus-upgrade/CONTROLS.md). Fresh recordings are deferred while fixes are the focus.

Will, Prince/Rick James, Tyrone/Negan, Urkel/Stefan and Yamal now live in the separate [sitcom folder](sitcom/README.md), with an independent game roster and launchers.

Earlier reviews and native recordings predate this roster split. Character artwork, source credits and existing moves are preserved.
''',encoding='utf-8')
report=dict(main_game='Manga vs Manhwa',main_entries=main_entries,sitcom_entries=sitcom_entries,moved_character_folders=slugs,moved_native_folders=engines,updated_main_launch_scripts=changed,repaired_review_links=link_changes,recordings='Deferred at user request')
(S/'split-manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
