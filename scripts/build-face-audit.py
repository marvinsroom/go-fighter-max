"""Publish transparent comic-reference comparisons and face-pass decisions."""
from pathlib import Path
from manhwa_fighters import PROFILES
from PIL import Image
import json,html,hashlib
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter';O=S/'face-audit';O.mkdir(exist_ok=True)
notes={
'gang-ryong':'Replaced rounded build and cheeks with the requested lean serious panel design, long ponytail, narrower jaw and gray robe. Movement, combat, cinematic poses and portrait corrected.',
'cha-yeon-woo':'Corrected the comic mask: open dark eye sockets, visible amber eyes, sculpted nose and slim chin across movement, combat, story and portrait.',
'kim-dokja':'Corrected straight falling fringe, softer oval jaw, calm horizontal eyes and restrained expression across body sheets and portrait.',
'mok-gyeongwoon':'Retained: narrow calm eyes, slender jaw, long dark half-up hair and unsettling restrained expression align with the comic references.',
'arthur':'Retained comic-era auburn hair, teal eyes and youthful slender face. This is the earlier Arthur requested for this roster.',
'eugene':'Retained adult Eugene: silver hair, golden eyes and defined youthful jaw. Hamel remains a separate past-life effect.',
'jin-mu-won':'Retained: straight dark brows, narrow focused eyes, long black hair and lean angular face match the selected comic-era reference.',
'lloyd':'Retained: swept brown hair, angular expressive face and exaggerated comic grin. Nightmare Grin is intentional.',
'baam':'Retained early Baam and Jue Viole appearances. Soft youthful face and golden eyes checked against SIU comic artwork; Viole uses the longer fringe.',
'jin-mori':'Retained youthful dark eyes, pointed brown hair and goggles; Monkey King keeps the circlet and the same facial identity. Early comic eyes differ from later awakened depictions; this pass preserves the existing era and transition.',
'vikir':'Retained: messy dark hair, red eyes and focused youthful face align with the licensed comic cover.',
'zhuo-fan':'New comic-based fighter. Licensed Kuaikan cover guides charcoal-lavender hair, sharp red-orange eyes, angular jaw and calculating smirk.'}
notes.update(jinwoo='Retained: mature angular jaw, narrow focused eyes and dark swept fringe checked against the licensed Solo Leveling comic artwork. Both dagger and greatsword forms retain this adult identity.',pyowol='Retained the user-selected white-haired manhwa appearance: delicate face, red eye rims, slit pupils and long face-framing locks. The previously accepted likeness study remains the body-art model.')
cards=[];report=[]
for slug,note in notes.items():
 f=S/'characters'/slug;a=f/('art/daggers' if slug=='jinwoo' else 'art/animation-v5' if slug=='pyowol' else 'art/canonical-v2' if slug=='baam' else 'art/v3' if slug=='vikir' else 'art/illustrated-v1')
 refs=O/'references'
 ref=next((x for x in ([f/'art/v3/references/face-three-quarter.jpg'] if slug=='pyowol' else [refs/'cha-yeon-woo-mask.png'] if slug=='cha-yeon-woo' else [refs/'kim-dokja-white-coat.png'] if slug=='kim-dokja' else [refs/(slug+'-official.png')] if slug in ('baam','vikir','jinwoo') else [refs/'jin-mori-early.png'] if slug=='jin-mori' else [a/'references/panel-reference.png',a/'references/official-cover.png',a/'references/official-cover.jpg']) if x.exists()),None)
 assert ref is not None,slug
 name=PROFILES.get(slug,{}).get('name',{'baam':'Baam','jin-mori':'Jin Mori','vikir':'Vikir','jinwoo':'Sung Jinwoo','pyowol':'Pyo Wol'} .get(slug,slug))
 portrait=a/('idle.png' if slug=='jinwoo' else 'profile-portrait.png' if slug=='pyowol' else 'portrait.png')
 source=PROFILES.get(slug,{}).get('source',{'baam':'https://www.webtoons.com/en/fantasy/tower-of-god/list?title_no=95','jin-mori':'https://www.webtoons.com/en/action/the-god-of-high-school/list?title_no=66','vikir':'https://tapas.io/series/revenge-of-the-baskerville-bloodhound/info'}.get(slug,''))
 if slug=='jinwoo':source='https://tapas.io/series/solo-leveling-comic/info'
 if slug=='pyowol':source='https://www.tappytoon.com/en/book/the-reaper'
 def rel(p):return '../'+p.relative_to(S).as_posix()
 images='<figure><img src="'+rel(ref)+'" alt="Comic identity reference"><figcaption>Comic reference</figcaption></figure>'
 before=f/'art/before-manhwa-faces-v2/portrait.png'
 if before.exists():images+='<figure><img src="'+rel(before)+'" alt="Previous portrait"><figcaption>Before</figcaption></figure>'
 images+='<figure><img src="'+rel(portrait)+'" alt="Current likeness"><figcaption>Current likeness</figcaption></figure>'
 body=next((x for x in [a/'poses/movement-0.png',a/'movement.png',a/'motion.png',a/'idle.png'] if x.exists()))
 images+='<figure><img src="'+rel(body)+'" alt="Current body art"><figcaption>Current body art</figcaption></figure>'
 native=f/'runtime-validation.json'
 if native.exists():
  proof=json.loads(native.read_text());frame=next((v for v in proof.get('frames',[]) if v.get('case_name')=='Idle'),None)
  if frame:
   capture=f/'replays'/frame.get('capture_directory',proof.get('capture_directory',''))/frame['file']
   if capture.exists():images+='<figure><img src="'+rel(capture)+'" alt="Native game capture"><figcaption>Native game capture</figcaption></figure>'
 cards.append('<article id="'+slug+'"><h2>'+name+'</h2><p>'+html.escape(note)+'</p><div class="images">'+images+'</div><p><a href="'+source+'">Official comic</a> Â· <a href="../characters/'+slug+'/review.html">Combat review</a></p></article>')
 report.append(dict(slug=slug,name=name,decision=note,reference=str(ref.relative_to(S)),portrait_sha256=hashlib.sha256(portrait.read_bytes()).hexdigest(),source=source))
 (a/'face-audit.json').write_text(json.dumps(report[-1],indent=2))
page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Comic Face Review</title><style>body{margin:0;background:#101825;color:#eef4ff;font:17px/1.6 system-ui}main{max-width:1500px;margin:auto;padding:30px}a{color:#a9dbff}article{background:#1b293b;border:1px solid #3b4a60;padding:24px;margin:24px 0;border-radius:12px}.images{display:flex;flex-wrap:wrap;gap:16px}figure{flex:1 1 230px;margin:0;min-width:0}img{width:100%;height:340px;object-fit:contain;background:#28364a}figcaption{color:#bbcee5}</style><main><a href="../manhwa-roster.html">Fighter roster</a><h1>Comic face review</h1><p>Side-by-side comic references, current portraits and body art for all fourteen manhwa/manhua fighters in this pass. Generated adaptations retain the roster rendering; the notes record which likenesses changed and which were retained. Some panel references are publicly reposted comic artwork; official series links are provided for attribution. Visual likeness remains available for your review.</p>'+''.join(cards)+'</main></html>'
(O/'review.html').write_text(page,encoding='utf-8');(O/'audit.json').write_text(json.dumps(dict(date='2026-10-21',fighters=report),indent=2));print('FACE_AUDIT',len(report))
