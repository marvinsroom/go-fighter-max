"""Archive the reviewed v4 build and record sourced versus estimated stature."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'sprite-fighter/characters';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0/chars';O=R/'sprite-fighter/face-audit/identity-scale-v5';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Targets describe the actual outfit/era selected, not every version of a character.
# Estimates are explicit: absence of a reliable numeric source is not evidence of canon.
profiles={
 'gang-ryong':(168,.98,'visual estimate','Lean training-era variant retained from the existing requested design; shorter than the tall swordsmen.','https://gosuverse.fandom.com/wiki/Gang_Ryong'),
 'mok-gyeongwoon':(183,.98,'visual estimate','Tall slender early manhwa body; no verified numerical height found.','https://myst-might-mayhem.fandom.com/wiki/Mok_Gyeongwoon'),
 'arthur':(175,.98,'era estimate','Auburn-haired academy Arthur, not later asuran-body Arthur.','https://tbate.fandom.com/wiki/Arthur_Leywin'),
 'cha-yeon-woo':(182,.97,'secondary reported','Adult masked Cain; 182cm reported by the linked character profile.','https://mywaifulist.moe/waifu/yeon-woo-cha-second-life-ranker'),
 'kim-dokja':(176,.98,'secondary reported','176cm listed with source notes in character wiki.','https://omniscient-readers-viewpoint.fandom.com/wiki/Kim_Dokja'),
 'eugene':(185,.98,'adult visual estimate','Older silver-haired post-timeskip Eugene, lean muscular adult; no verified numeric height found.','https://damn-reincarnation.fandom.com/wiki/Eugene_Lionheart'),
 'jin-mu-won':(185,.98,'adult visual estimate','Adult travel-era Northern Blade. Mature rectangular face and broader shoulders from licensed cover/comic art; not a numeric canon claim.','https://www.tappytoon.com/en/book/legend-of-northern-blade'),
 'lloyd':(181,.98,'secondary reported','181cm/71kg listed in the character wiki with footnotes.','https://dragonschef.fandom.com/wiki/Lloyd_Frontera'),
 'zhuo-fan':(180,.98,'visual estimate','Classic brown-haired lean martial artist; no verified numeric height found.','https://magic-emperor.fandom.com/wiki/Zhuo_Fan'),
 'baam':(168,.93,'secondary reported','Part I red-vest Baam 168cm; long-haired Part II Viole 180cm. Their guard bends the knees.','https://towerofgod.fandom.com/wiki/Twenty-Fifth_Baam'),
 'jin-mori':(177,.97,'secondary reported','177cm athletic early Mori; King retains the same body with different headwear/pelt.','https://godofhighschool.fandom.com/wiki/Jin_Mori'),
 'vikir':(183,.98,'era visual estimate','Post-regression teenage Hunter/Academy body, same person under the Night Hound hood; no verified numeric height found.','https://revenge-of-the-ironblooded-sword-hound.fandom.com/wiki/Vikir_Van_Baskerville'),
 'jinwoo':(183,.98,'secondary reported, unverified primary','183cm commonly attributed to author comments; primary comment not verified. Adult post-awakening body.','https://www.reddit.com/r/sololeveling/comments/p4pl82'),
 'pyowol':(180,.98,'visual estimate','Slender adult white-haired Pyo Wol; no reliable numeric height found.','https://reaper-of-the-drifting-moon.fandom.com/wiki/Pyo_Wol')}
baseline=json.loads((R/'.tmp/identity-scale-v5-baseline.json').read_text());rows=[]
for b in baseline:
 slug=b['slug'];f=S/slug;archive=f/'archive/before-identity-scale-v5';n=E/b['engine'];height,stance,confidence,reason,source=profiles[slug]
 if not (archive/'manifest.json').exists():
  (archive/'runtime').mkdir(parents=True,exist_ok=True)
  saved={}
  # Only production files are archived; test fixtures are reproducible.
  existing=f/'art/comic-identity-v3/installed.json'
  names=json.loads(existing.read_text())['runtime_sha256'] if existing.exists() else json.loads((f/'build-report.json').read_text())['runtime_sha256']
  for name in names:
   p=n/name;shutil.copy2(p,archive/'runtime'/name);saved[name]=sha(p)
  for name in ('review.html','build-report.json','runtime-validation.json','comic-viewer-validation.json','viewer-validation.json'):
   if (f/name).exists():shutil.copy2(f/name,archive/name)
  (archive/'active-art').mkdir(exist_ok=True)
  for p in (f/'art/comic-identity-v3').iterdir():
   if p.is_file() and p.suffix in ('.png','.json','.txt'):shutil.copy2(p,archive/'active-art'/p.name)
  (archive/'manifest.json').write_text(json.dumps(dict(revision='before-identity-scale-v5',runtime_sha256=saved),indent=2))
 row=dict(b,height_cm=height,neutral_stance_ratio=stance,evidence=confidence,reason=reason,source=source,target_neutral_world_height=height*.5*stance)
 if slug=='baam':row['forms']={'base_cm':168,'viole_cm':180,'transition':'gradual 168 to180 across eight drawings'}
 rows.append(row)
state=dict(revision='identity-scale-v5',status='In progress',scope='14 manhwa fighters on current review page',world_units_per_cm=.5,method='One isotropic native character scale per fighter, accounting for localcoord, AIR and CNS scale. Natural stance/foreshortening retained; no per-animation bounding-box fitting or horizontal stretching.',height_policy='Secondary reported values and visual estimates clearly distinguished; estimates are not official canon.',fighters=rows)
(O/'profiles.json').write_text(json.dumps(state,indent=2));print('V5_ARCHIVED_AND_PROFILED',len(rows))
