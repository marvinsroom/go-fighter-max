"""Save licensed-series references for an inspectable likeness audit."""
from pathlib import Path
from urllib.parse import quote
from html import unescape
import subprocess,re,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'sprite-fighter/face-audit/references';A.mkdir(parents=True,exist_ok=True)
sources={
'jinwoo':'https://tapas.io/series/solo-leveling-comic/info',
'zhuo-fan':'https://tapas.io/series/the-servant-is-the-demon-king/info',
'zhuo-fan-classic':'https://www.voyce.me/series/the-devils-butler',
'baam':'https://www.webtoons.com/en/fantasy/tower-of-god/list?title_no=95',
'jin-mori':'https://www.webtoons.com/en/action/the-god-of-high-school/list?title_no=66',
'vikir':'https://tapas.io/series/revenge-of-the-baskerville-bloodhound/info'}
def fetch(url,path):
 if not path.exists():subprocess.run(['curl.exe','-L','--fail','--silent','--show-error','-A','Mozilla/5.0','-e','https://www.webtoons.com/',url,'-o',str(path)],check=True)
for slug,url in sources.items():
 page=A/(slug+'-official.html');fetch(url,page);tags=re.findall(r'<meta\b[^>]+>',page.read_text(encoding='utf-8'))
 tag=next(t for t in tags if re.search(r'(?:property|name)=["\']og:image["\']',t));imageurl=quote(unescape(re.search(r'content=["\']([^"\']+)',tag)[1]),safe=':/?=&%')
 original=A/(slug+'-original.img');fetch(imageurl,original);Image.open(original).convert('RGB').save(A/(slug+'-official.png'))
 (A/(slug+'-source.json')).write_text(json.dumps(dict(official_series=url,image_url=imageurl,kind='Official licensed comic series artwork'),indent=2));print('FACE_REFERENCE',slug,flush=True)
url='https://www.webtoons.com/en/action/omniscient-reader/episode-87/viewer?title_no=2154&episode_no=88'
page=A/'kim-dokja-episode87.html';fetch(url,page);raw=page.read_text(encoding='utf-8')
urls=[unescape(x) for x in re.findall(r'<img[^>]*class="_images"[^>]*data-url="([^"]+)"',raw)]
if not urls:urls=[unescape(x) for x in re.findall(r'data-url="([^"]+)',raw) if 'webtoon' in x]
for i,imageurl in enumerate(urls[:10]):
 path=A/(f'kim-dokja-episode87-{i:02d}.jpg');fetch(quote(imageurl,safe=':/?=&%'),path)
(A/'kim-dokja-source.json').write_text(json.dumps(dict(official_episode=url,downloaded_images=urls[:10],kind='Official WEBTOON comic panels; select face reference after inspection'),indent=2))
print('KIM_PANELS',len(urls[:10]),flush=True)
