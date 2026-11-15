"""Expand the stature audit to every current select.def entry, preserving rollback files."""
from pathlib import Path
import json,re,sys,shutil,hashlib
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];E=R/'sprite-fighter/engine/ikemen-go-v1.0.0';O=R/'sprite-fighter/face-audit/identity-scale-v5';p=O/'profiles.json';state=json.loads(p.read_text());rows=state['fighters'];known={r['engine'] for r in rows}
extras={
 'edward':('edward',149,.94,'secondary reported','Early teenage Edward; visibly shorter than adult fighters. Hair and boots remain part of the original drawing.','https://fma.fandom.com/wiki/Edward_Elric'),
 'prince':('prince',180,.98,'portrayal estimate','Dave Chappelle portrayal, rather than the real musician Prince. The paired Rick James portrayal retains the same actor stature.','https://www.celebheights.com/s/Dave-Chappelle-49049.html'),
 'tyrone':('tyrone',180,.94,'portrayal estimate','Dave Chappelle as Tyrone/Negan. Tyrone slouches; Negan is more upright.','https://www.celebheights.com/s/Dave-Chappelle-49049.html'),
 'will_full':('will',188,.98,'secondary reported','Adult Will Smith portrayal.','https://www.celebheights.com/s/Will-Smith-181.html'),
 'urkel':('urkel',180,.94,'portrayal estimate','Adult Jaleel White, Urkel slouch retained; Stefan has a straighter stance.','https://healthyceleb.com/jaleel-white/'),
 'yamal':('yamal',178,.97,'official player profile','FC Barcelona lists 178cm on the current player profile.','https://www.fcbarcelona.com/en/futbol/primer-equip/jugadors/129404/lamine-yamal'),
 'cid_shadow':('cid',170,.98,'visual estimate','Teen Cid/Shadow; no primary numeric height confirmed. Existing hood, cloak and build retained.','https://www.reddit.com/r/TheEminenceInShadow/comments/1jpe1in'),
 'rimuru':('rimuru',130,.98,'secondary reported, era-specific','Masked human Demon Lord Seed body 130cm; Demon Lord 140cm; compact slime silhouette estimated40cm.','https://tensura.fandom.com/wiki/Rimuru_Tempest'),
 'ichigo':('ichigo',174,.96,'official later / secondary earlier','Early Shikai/Bankai body174cm; later forms181cm per official TYBW profile. Horned silhouette has a separate visual allowance.','https://bleach-anime.com/en/character/'),
 'luffy':('luffy',174,.94,'official base / estimated transformations','Official base174cm. Inflated forms have no verified numeric stature; larger silhouettes are explicitly estimates, preserving their broad drawn builds.','https://one-piece.com/character/luffy/index.html'),
 'goku':('goku',175,.94,'secondary reported databook figure','Adult Goku175cm. Saiyan transformations retain adult stature and their existing build/hair differences.','https://dragonball.fandom.com/wiki/Goku'),
 'gt_goku':('gt-goku',120,.94,'child visual estimate / reported adult','GT child body estimated120cm, adult SS4 body175cm. SS1/SS2/SS3 retain the child body.','https://dragonball.fandom.com/wiki/Goku')}
selected=[]
for line in (E/'data/select.def').read_text().split('[Characters]',1)[1].split(';How to add characters')[0].splitlines():
 line=line.strip()
 if line and not line.startswith(';'):selected.append(line.split(',')[0].strip())
for roster in selected:
 engine=roster;n=E/'chars'/engine;definition=n/(engine+'.def');de=definition.read_text(encoding='utf-8',errors='replace')
 def field(k):return re.search(r'(?im)^\s*'+k+r'\s*=\s*([^;\r\n]+)',de)[1].strip()
 cns=field('cns');air=field('anim');sff=field('sprite');w=float(re.search(r'(?im)^\s*localcoord\s*=\s*([\d.]+)',de)[1]) if re.search(r'(?im)^\s*localcoord\s*=',de) else 320
 if engine not in known:
  slug,height,stance,evidence,reason,source=extras[engine];at=(n/air).read_text(encoding='utf-8',errors='replace');ct=(n/cns).read_text(encoding='utf-8',errors='replace');sy=float(re.search(r'(?im)^\s*yscale\s*=\s*([\d.]+)',ct)[1]);block=re.search(r'(?ims)^\s*\[Begin Action 0\](.*?)(?=^\s*\[Begin Action|\Z)',at)[1];line=next(x for x in block.splitlines() if re.match(r'^\s*\d+\s*,\s*\d+',x));parts=[x.strip() for x in line.split(',')];key=tuple(map(int,parts[:2]));scale=float(parts[8]) if len(parts)>8 and parts[8] else 1;sprites=Sff(n/sff);b=sprites.decode(sprites.keys[key]).getchannel('A').getbbox();world=(b[3]-b[1])*scale*sy*320/w
  rows.append(dict(slug=slug,engine=engine,sff=sff,neutral_key=key,air_scale=scale,global_scale=sy,localcoord_width=w,bounds=b,current_neutral_world_height=world,height_cm=height,neutral_stance_ratio=stance,evidence=evidence,reason=reason,source=source,target_neutral_world_height=height*.5*stance))
 row=next(x for x in rows if x['engine']==engine);row.update(roster_entry=roster,cns=cns,air=air,definition=definition.name)
 archive=O/'archive'/engine
 if not (archive/'manifest.json').exists():
  archive.mkdir(parents=True,exist_ok=True);files={definition.name}
  for line in de.splitlines():
   m=re.match(r'\s*(?:cns|cmd|anim|sprite|sound|st\d*|stcommon|pal\d+)\s*=\s*([^;\r\n]+)',line,re.I)
   if m and (n/m[1].strip()).is_file():files.add(m[1].strip())
  hashes={}
  for name in files:
   target=archive/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(n/name,target);hashes[name]=hashlib.sha256(target.read_bytes()).hexdigest()
  (archive/'manifest.json').write_text(json.dumps(dict(engine=engine,runtime_sha256=hashes),indent=2))
assert len(rows)==len(selected)==26
state.update(scope='Every playable select.def entry (26 fighters), including their existing forms',fighters=rows,status='In progress')
p.write_text(json.dumps(state,indent=2));print('ALL_ROSTER_PROFILED_AND_ARCHIVED',len(rows))
