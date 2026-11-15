"""Show corrected likenesses and the complete playable roster at one world scale."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,re,html,sys
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';O=S/'face-audit/identity-scale-v5';E=S/'engine/ikemen-go-v1.0.0';state=json.loads((O/'profiles.json').read_text())
def rel(p):return __import__('os').path.relpath(p,O).replace('\\','/')
def name(r):return {'gang-ryong':'Gang Ryong','mok-gyeongwoon':'Mok Gyeongwoon','jin-mu-won':'Jin Mu-Won','kim-dokja':'Kim Dokja','cha-yeon-woo':'Cha Yeon-woo','jin-mori':'Jin Mori','pyowol':'Pyo Wol','jinwoo':'Sung Jinwoo','will':'Will','gt-goku':'GT Goku'}.get(r['slug'],r['slug'].replace('-',' ').title())
def assets(row):
 n=E/'chars'/row['engine'];sff=Sff(n/row['sff']);air=(n/row['air']).read_text(encoding='utf-8',errors='replace');scales={}
 for line in air.splitlines():
  if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):
   f=[v.strip() for v in line.split(';',1)[0].split(',')];key=tuple(map(int,f[:2]));scales.setdefault(key,[(float(f[j]) if len(f)>j and f[j] else 1) for j in (7,8)])
 return sff,scales
cached={};tiles=[];world=2.5;cellw=200;cellh=320
for row in sorted(state['fighters'],key=lambda x:x['height_cm']):
 sff,scales=assets(row);cached[row['slug']]=(sff,scales);key=tuple(row['neutral_key']);i=sff.keys[key];im=sff.decode(i);axis=sff.headers[i][4:6];sx,sy=scales[key];fx=sx*row['native_scale'][0]*320/row['localcoord_width']*world;fy=sy*row['native_scale'][1]*320/row['localcoord_width']*world
 im=im.resize((max(1,round(im.width*abs(fx))),max(1,round(im.height*abs(fy)))),Image.Resampling.LANCZOS);tile=Image.new('RGBA',(cellw,cellh),'#354352');draw=ImageDraw.Draw(tile)
 for cm in (100,150,180,200):
  y=285-cm*.5*world;draw.line((0,y,cellw,y),fill='#536270',width=1)
 tile.alpha_composite(im,(round(cellw/2-axis[0]*fx),round(285-axis[1]*fy)));draw.line((0,285,cellw,285),fill='#9faebc',width=2);draw.text((8,4),name(row),fill='white');draw.text((8,25),str(row['height_cm'])+' cm | '+('estimate' if 'estimate' in row['evidence'] else 'reported'),fill='#e8ddbd');tiles.append(tile)
board=Image.new('RGBA',(cellw*13,cellh*2),'#354352')
for i,tile in enumerate(tiles):board.alpha_composite(tile,(i%13*cellw,i//13*cellh))
board.convert('RGB').save(O/'roster-lineup.jpg',quality=93)
cards=[];native_count=0
for row in state['fighters']:
 f=S/'characters'/row['slug'];proof=O/'native'/row['slug']/'current.json';native='Native recording pending.'
 if proof.exists():
  d=json.loads(proof.read_text());right=[v for v in d.get('frames',[]) if v.get('facing')==1 and v.get('label')!='Basic attack connects'];frames=right[:4]
  if row['slug'] in ('jinwoo','vikir'):frames+= [v for v in right if 'shadow form' in v['label'] or 'pet form' in v['label']]
  if d.get('status')=='Complete' and not d.get('failed') and d.get('runtime_sha256')==row['runtime_sha256']:
   native_count+=1;native=f'{d["passed"]} native pose / contact checks passed.'
   if frames:
    board=Image.new('RGB',(1280,385*((len(frames)+1)//2)),'#18202c');draw=ImageDraw.Draw(board)
    for i,v in enumerate(frames):
     im=Image.open(E/v['file']).convert('RGB');im.thumbnail((640,360));x=i%2*640;y=i//2*385;board.paste(im,(x,y+25));draw.text((x+8,y+5),v['label'],fill='white')
    board.save(proof.parent/'contact.jpg',quality=90);native+=f'<a href="{rel(proof.parent/"contact.jpg")}"><img class="native" src="{rel(proof.parent/"contact.jpg")}" alt="Current {name(row)} native captures"></a>'
 art=f/'art/identity-scale-v5';extra=''
 if (f/'art/comic-face-v6/visual-review.json').exists():art=f/'art/comic-face-v6'
 if (art/'visual-review.json').exists():
  reference=O/'references'/('jin-mu-won-panel.jpg' if row['slug']=='jin-mu-won' else 'eugene-adult-comic.jpg')
  extra='<div class="faces"><figure><img src="'+rel(reference)+'" alt="Published comic reference"><figcaption>Published comic reference</figcaption></figure><figure><img src="'+rel(art/'portrait.png')+'" alt="Corrected adult portrait"><figcaption>Corrected portrait</figcaption></figure><figure><img src="'+rel(art/'extracted/movement-00.png')+'" alt="Corrected complete body"><figcaption>Corrected body</figcaption></figure></div>'
  extra+='<details><summary>Full corrected sheets and exact prompts</summary>'
  for kind in ('movement','combat','story','portrait'):extra+=f'<p><a href="{rel(art/(kind+".png"))}">{kind} artwork</a> · <a href="{rel(art/(kind+".prompt.txt"))}">Exact prompt</a> · <a href="{rel(art/(kind+".generation.json"))}">Provenance</a></p>'
  extra+='</details>'
 review=f/'review.html';links=f'<a href="{rel(review)}">Controls and move review</a>' if review.exists() else ''
 cards.append(f'<article id="{row["slug"]}"><h2>{name(row)}</h2><p><strong>{row["height_cm"]} cm</strong> · {html.escape(row["evidence"])}. {html.escape(row["reason"])}</p><p><a href="{html.escape(row["source"])}">Height / character reference</a> · {links}</p>{extra}<p>{native}</p><details><summary>Transformation sizing</summary><p>{html.escape(row.get("form_height_notes",""))}</p></details></article>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Roster stature and corrected likenesses</title><style>*{box-sizing:border-box}body{margin:0;background:#111824;color:#eef3fa;font:17px/1.6 system-ui}main{max-width:1400px;margin:auto;padding:24px}a{color:#b6d9ff}article{padding:24px;margin:26px 0;background:#202c3c;border-radius:12px}h1{line-height:1.2}.lineup{overflow:auto;background:#354352}.lineup img{display:block;width:2600px;max-width:none}.faces{display:flex;gap:18px;flex-wrap:wrap}.faces figure{flex:1 1 240px;margin:0}.faces img{width:100%;height:360px;object-fit:contain;background:#354352}.native{display:block;width:100%;height:auto;margin-top:18px}details{margin:14px 0}summary{cursor:pointer;color:#d9e8fa}</style><main><h1>Character likeness and roster proportions</h1>'''
page+=f'<p>{native_count}/26 playable fighters have current native size captures. Jin Mu-Won uses stronger comic references and an adult face; Eugene uses his older silver-haired design.</p><p>Every fighter is shown at the same world scale and foot baseline. Heights use published or reported values where available; estimates are labelled. Stance, hair, footwear and headwear affect the visible silhouette. Shorter characters are no longer normalized to adult height.</p><div class="lineup"><img src="roster-lineup.jpg" alt="All 26 playable fighters, sorted by stature, drawn at one shared world scale"></div><p>Scroll sideways for the full lineup. <a href="profiles.json">Height sources and sizing records</a> · <a href="native-validation.json">Current native checks</a></p>'+''.join(cards)+'</main></html>'
(O/'review.html').write_text(page,encoding='utf-8');print('V5_REVIEW',native_count,'/26')
