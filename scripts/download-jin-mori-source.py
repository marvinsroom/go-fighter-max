"""Preserve the publicly linked Jin Mori archive and inspect data files only."""
import urllib.request, re, html, json, hashlib, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'sprite-fighter/characters/jin-mori/source'
p.mkdir(parents=True, exist_ok=True)
u = 'https://www.mediafire.com/file/w4dv6sk6g9w317h/Jin_Mori.zip/file'
if not (p / 'Jin_Mori.zip').exists():
    s = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=45).read().decode()
    t = next(t for t in re.findall(r'<a\b[^>]*>', s) if 'id="downloadButton"' in t)
    d = html.unescape(re.search(r'href="([^"]+)"', t)[1])
    b = urllib.request.urlopen(d, timeout=60).read()
    (p / 'Jin_Mori.zip').write_bytes(b)
b = (p / 'Jin_Mori.zip').read_bytes()
with zipfile.ZipFile(p / 'Jin_Mori.zip') as z:
    for n in z.namelist():
        assert (p / 'upstream' / n).resolve().is_relative_to((p / 'upstream').resolve())
    z.extractall(p / 'upstream')
(p / 'source-report.json').write_text(json.dumps(dict(listing='https://brunomateus62.wixsite.com/bmmugenforever/post/others-downloads', release=u, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()), indent=2))
print('Downloaded', len(b), 'bytes')
for x in (p / 'upstream').rglob('*'):
    if x.is_file(): print(x.relative_to(p))
