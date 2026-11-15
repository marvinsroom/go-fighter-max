"""Preserve the public GT Goku release and its source provenance."""
from pathlib import Path
import urllib.request, re, html, hashlib, json, subprocess

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'sprite-fighter/characters/gt-goku/source'
folder.mkdir(parents=True,exist_ok=True)
url='https://www.mediafire.com/download/5qxhmx1652saxnz'
request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
page=urllib.request.urlopen(request,timeout=60).read().decode()
tag=next(t for t in re.findall(r'<a\b[^>]*>',page) if 'id="downloadButton"' in t)
direct=html.unescape(re.search(r'href="([^"]+)"',tag)[1])
archive=folder/'goku-gt.rar'
urllib.request.urlretrieve(direct,archive)
with archive.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
report=dict(release=url,download=direct,listing='https://mugenfreeforall.com/topic/52595-dragon-ball-series-part-2-includes-dr-slump/',listed_authors='Mikel8888, Inseph & RafaMugen',bytes=archive.stat().st_size,sha256=digest)
(folder/'source-report.json').write_text(json.dumps(report,indent=2))
subprocess.run([r'C:\Program Files\7-Zip\7z.exe','x',str(archive),'-o'+str(folder/'upstream'),'-y'],check=True,stdout=subprocess.DEVNULL)
print('GT_GOKU_DOWNLOADED',report['bytes'],digest)
for p in (folder/'upstream').rglob('*.def'):print(p.relative_to(folder))
