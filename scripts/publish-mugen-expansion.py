"""Register startup-tested original imports and publish the unfinished source queue."""
from pathlib import Path
import json,hashlib,re,html,shutil,io,struct
from PIL import Image
from mugen_sff import Sff,decode_pcx
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter';E=G/'engine/ikemen-go-v1.0.0';O=G/'mugen-expansion';Q=O/'queue.json'
d=json.loads(Q.read_text());ready=[]
style_queue=G/'style-wave2/queue.json';style_requests={r['slug'] for r in json.loads(style_queue.read_text())['targets']} if style_queue.exists() else set()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(t):return html.escape(str(t))
style='<style>body{background:#111824;color:#eef2fa;font:17px/1.6 system-ui;max-width:1120px;margin:30px auto;padding:20px}a{color:#a8d9ff}article,section{background:#1d2a3c;padding:18px;margin:16px 0;border-radius:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}img{max-width:180px;max-height:160px;image-rendering:pixelated}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:7px;border-bottom:1px solid #40526d}code{overflow-wrap:anywhere}.notice{background:#453e26;padding:16px}</style>'
def page(title,body):return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title>'+style+body+'</html>'
def portrait(path,dest):
 raw=path.read_bytes()
 if raw[15]!=1:
  sf=Sff(path);key=next((k for k in [(9000,1),(9000,0),(0,0)] if k in sf.keys),next(iter(sf.keys)));im=sf.decode(sf.keys[key])
 else:
  count,offset=struct.unpack_from('<II',raw,20);headers=[];pal=None
  for i in range(count):
   nxt,length,x,y,g,n,link,same=struct.unpack_from('<IIhhHHHB',raw,offset);pcx=raw[offset+32:offset+32+length]
   if length and (not same or pal is None) and len(pcx)>=769 and pcx[-769]==12:pal=pcx[-768:]
   headers.append((g,n,link,pcx,pal));offset=nxt
  selected=next((i for k in [(9000,1),(9000,0),(0,0)] for i,h in enumerate(headers) if h[:2]==k),0)
  seen=set()
  while not headers[selected][3]:
   assert selected not in seen;seen.add(selected);selected=headers[selected][2]
  g,n,link,pcx,pal=headers[selected];im=decode_pcx(pcx,pal)
 im.save(dest)

for row in d['fighters']:
 slug=row['slug'];f=G/'characters'/slug;n=E/'chars'/slug;reportpath=f/'import-report.json';validation=O/'validation'/(slug+'.json')
 if not reportpath.exists() or not validation.exists():continue
 v=json.loads(validation.read_text(encoding='utf-8-sig'))
 if v['status']!='PASS':row['status']='Imported; startup failed; not registered';continue
 report=json.loads(reportpath.read_text())
 for name,digest in report['source_files_sha256'].items():
  compatibility=report.get('native_compatibility',{}).get(name)
  if compatibility:assert sha(f/compatibility['original_retained'])==digest,('Original source modified',slug,name)
  assert sha(n/name)==(compatibility['installed_sha256'] if compatibility else digest),('Undocumented source modification',slug,name)
 assert sha(n/(slug+'.def'))==sha(n/report['original_definition']),slug
 definition=(n/(slug+'.def')).read_text(encoding='cp1252',errors='replace');section=re.search(r'(?ims)^\[Files\](.*?)(?=^\[|\Z)',definition)[1]
 refs={k.lower():val.split(';')[0].strip().strip('"') for k,val in re.findall(r'(?im)^\s*([\w.]+)\s*=\s*(.*?)\s*$',section)}
 for key,value in refs.items():
  if not value or key.startswith('pal') or key in ['intro.storyboard','ending.storyboard']:continue
  local=n/value.replace('\\','/')
  assert local.exists() or (E/value).exists() or (E/'data'/value).exists() or (E/'data'/(value+'.zss')).exists(),('Missing DEF dependency',slug,key,value)
 image=f/'import-portrait.png'
 try:portrait(n/refs['sprite'].replace('\\','/'),image)
 except Exception as exc:row['portrait_note']=str(exc)
 commandpath=n/refs['cmd'].replace('\\','/');commands=[]
 text=commandpath.read_text(encoding='cp1252',errors='replace')
 for block in re.split(r'(?im)^\s*\[Command\]',text)[1:]:
  block=block.split('[',1)[0];name=re.search(r'(?im)^\s*name\s*=\s*(.*?)(?:;.*)?$',block);keys=re.search(r'(?im)^\s*command\s*=\s*(.*?)(?:;.*)?$',block)
  if name and keys:commands.append((name[1].strip().strip('"'),keys[1].strip()))
 table='<table><tr><th>Original command</th><th>MUGEN input</th></tr>'+''.join('<tr><td>'+esc(name)+'</td><td><code>'+esc(keys)+'</code></td></tr>' for name,keys in commands)+'</table>'
 links=[]
 for p in n.rglob('*.txt'):
  if re.search('read|move|lei|lisez|control',p.name,re.I):links.append('<a href="../../engine/ikemen-go-v1.0.0/chars/'+slug+'/'+esc(p.relative_to(n).as_posix())+'">'+esc(p.name)+'</a>')
 body='<a href="../../mugen-expansion/review.html">Back to MUGEN imports</a><h1>'+esc(row['name'])+'</h1>'
 if image.exists():body+='<img src="import-portrait.png" alt="Original imported character portrait">'
 body+='<p>Original MUGEN import. Creator credit from package: '+esc(report['creator'])+'. Original sprites and moves retained; source audio retained with documented format fixes where needed.</p><p><a href="../../Play '+esc(row['name'])+'.cmd">Play this fighter</a> · <a href="source/source-report.json">Source archive and credits</a> · <a href="import-report.json">Import audit</a> · <a href="../../mugen-expansion/validation/'+slug+'.json">Startup check</a></p><p>'+esc(v['scope'])+'. No new recordings.</p>'
 if slug=='yuji':body+='<p><b>Sukuna:</b> S (MUGEN y), at least 1500 power, grounded with control. S again returns to Yuji when the source form timer permits. Both banks are in this fighter.</p>'
 if (G/'style-wave2'/slug/'inventory.json').exists():body+='<p><a href="../../style-wave2/review.html">Requested illustrated style conversion</a>: source inventory and design brief prepared; new artwork pending generator availability.</p>'
 if report.get('native_compatibility'):body+='<p>Audio compatibility: unsupported 32-bit PCM clips converted to supported 24-bit PCM with original sample rate, duration and channels. Original archive and SND retained unchanged; see the import audit for exact clip IDs and precision.</p>'
 body+='<p>Game keyboard: arrows move/guard; Z/X/C map to MUGEN a/b/c; A/S/D map to x/y/z; Enter maps to Start. Read the original commands below using those button names. Original files: '+', '.join(links[:12])+'.</p><details><summary>Original input commands ('+str(len(commands))+')</summary>'+table+'</details>'
 (f/'review.html').write_text(page(row['name'],body),encoding='utf-8')
 (G/('Play '+row['name']+'.cmd')).write_text('@echo off\ncd /d "%~dp0engine\\ikemen-go-v1.0.0"\nstart "" "Ikemen_GO.exe" -config save/config.ini -loadmotif -p1 '+slug+' -p2 baam -p1.ai 0 -p2.ai 8 -s stages/stage0-720.def\n')
 row.update(status='Playable original MUGEN import; startup PASS; '+('requested style conversion pending generator availability' if slug in style_requests else 'styling deferred'),review='characters/'+slug+'/review.html',creator=report['creator']);report['status']=row['status'];report['startup_validation']='../../mugen-expansion/validation/'+slug+'.json';reportpath.write_text(json.dumps(report,indent=2));ready.append(row)

select=E/'data/select.def';backup=O/'before-select.def'
if not backup.exists():shutil.copy2(select,backup)
text=select.read_text();insert=[]
for row in ready:
 if not re.search(r'(?im)^\s*'+re.escape(row['slug'])+r'\s*(?:,|$)',text):insert.append(row['slug']+', stages/stage0-720.def, order=1')
if insert:select.write_text(text.replace('[Characters]','[Characters]\n'+'\n'.join(insert),1))
entries=[]
for line in select.read_text().split('[Characters]',1)[1].splitlines():
 if line.strip().startswith('['):break
 if line.strip() and not line.lstrip().startswith(';'):entries.append(line.split(',')[0].strip())
assert len(entries)==len(set(entries))
entries=[name for name in entries if name!='randomselect']
assert not any(x in entries for x in ['will_full','prince','yamal','urkel','tyrone'])
pending=[r for r in d['fighters'] if r not in ready]
d.update(status='Original imports playable; remaining sources pending' if pending else 'Original imports complete',imported=len(ready),requested=len(d['fighters']),main_roster_count=len(entries),validation_scope='Startup and source preservation; original game balance retained; exhaustive moves/forms not yet audited',recordings=False)
Q.write_text(json.dumps(d,indent=2),encoding='utf-8')
body='<h1>Original MUGEN imports</h1><p><a href="../roster.html">Main roster</a> · <a href="queue.json">Full source and status list</a></p><p>'+str(len(ready))+' of '+str(len(d['fighters']))+' requested fighters imported and startup tested. Main game: '+str(len(entries))+' fighters. Original sprites, voices and gameplay retained. Requested style work is pending generator availability. Recordings remain deferred.</p><div class="grid">'
if style_requests:body=body.replace('<div class="grid">','<p><a href="../style-wave2/review.html">Requested style conversion: Hiei, Itachi, Kisame, Ash, Ben, the four Turtles, Shredder and Kenpachi</a>. Imports are playable; new artwork is pending generator availability.</p><div class="grid">',1)
for row in ready:
 body+='<article>'
 if (G/'characters'/row['slug']/'import-portrait.png').exists():body+='<img src="../characters/'+row['slug']+'/import-portrait.png" alt="'+esc(row['name'])+' original portrait">'
 body+='<h2><a href="../'+row['review']+'">'+esc(row['name'])+'</a></h2><p>'+esc(row['creator'])+'</p><a href="../Play '+esc(row['name'])+'.cmd">Play</a></article>'
body+='</div><section><h2>Source downloads pending</h2><ul>'+''.join('<li><b>'+esc(r['name'])+'</b>: '+esc(r.get('source_issue',r['status']))+'</li>' for r in pending)+'</ul></section><p>Startup checks cover loading and native script compilation. New imports additionally verify fighter identity and 180 active-round ticks; consult each report for its exact scope. They do not certify every move, transformation, or source balance choice. All original archives and credits are retained under each character’s source folder.</p>'
(O/'review.html').write_text(page('Original MUGEN imports',body),encoding='utf-8')
(G/'Review New MUGEN Imports.cmd').write_text('@echo off\nstart "" "%~dp0mugen-expansion\\review.html"\n')
roster=G/'roster.html';text=roster.read_text(encoding='utf-8');text=re.sub(r'\d+ playable fighters\.',str(len(entries))+' playable fighters.',text)
for row in ready:
 link='<li><a href="'+row['review']+'">'+esc(row['name'])+'</a></li>'
 if 'href="'+row['review']+'"' not in text:text=text.replace('</ul>',link+'</ul>',1)
roster.write_text(text,encoding='utf-8')
readme=G/'README.md';text=readme.read_text(encoding='utf-8');text=re.sub(r'\d+ playable (?:manga and manhwa fighters\.|fighters, including the requested anime and game-character imports\.)',str(len(entries))+' playable fighters, including the requested anime and game-character imports.',text)
notice='<!-- mugen-expansion -->\n**Original MUGEN imports:** [Source, controls and import status](mugen-expansion/review.html). '+str(len(ready))+'/'+str(len(d['fighters']))+' requested fighters added; styling deferred. Open **Review New MUGEN Imports.cmd**.\n<!-- /mugen-expansion -->'
if style_requests:notice=notice.replace('styling deferred.','[Requested next style pass](style-wave2/review.html) prepared; artwork pending generator availability.')
text=re.sub(r'<!-- mugen-expansion -->.*?<!-- /mugen-expansion -->',notice,text,flags=re.S) if '<!-- mugen-expansion -->' in text else text.replace('# Manga vs Manhwa','# Manga vs Manhwa\n\n'+notice,1)
readme.write_text(text,encoding='utf-8')
print('REGISTERED',len(ready),'new original fighters;',len(entries),'main roster entries;',len(pending),'source downloads pending')
