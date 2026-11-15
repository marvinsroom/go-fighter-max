"""Download public Goku candidates and retain exact source provenance."""
from pathlib import Path
import urllib.request,re,html,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
name=sys.argv[1]
urls={'tta':'https://www.mediafire.com/file/ihnsx1ea4b2wsbu/TTA%2527Goku_JUS_V2.rar/file','dbs':'https://www.mediafire.com/file/smexuldsahhoy16/Goku_DBS.rar/file','lora':'https://www.dropbox.com/scl/fi/tbgnnj3ko8fylaevq27wg/Goku-DBS-V3.5-LoraTWolf46.rar?rlkey=3ziysr2igu3t9iml4x2x33ue4&dl=1'}
url=urls[name];folder=R/'sprite-fighter/characters/goku/source/candidates'/name;folder.mkdir(parents=True,exist_ok=True)
if 'mediafire.com' in url:
 page=urllib.request.urlopen(url,timeout=45).read().decode()
 tag=next(t for t in re.findall(r'<a\b[^>]*>',page) if 'id="downloadButton"' in t)
 direct=html.unescape(re.search(r'href="([^"]+)"',tag)[1])
else:direct=url
archive=folder/(name+'.rar')
urllib.request.urlretrieve(direct,archive)
record=dict(release=url,download=direct,listing='https://mugenfreeforall.com/topic/52595-dragon-ball-series-part-2-includes-dr-slump/',bytes=archive.stat().st_size,sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
(folder/'source-report.json').write_text(json.dumps(record,indent=2))
subprocess.run([r'C:\Program Files\7-Zip\7z.exe','x',str(archive),'-o'+str(folder/'upstream'),'-y'],check=True,stdout=subprocess.DEVNULL)
print(name,'DOWNLOADED',record['bytes'],record['sha256'])
for p in (folder/'upstream').rglob('*.def'):print(p.relative_to(folder))
