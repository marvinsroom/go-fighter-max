"""Inventory stiff walk banks from original AIRs and export their actual current models."""
from pathlib import Path
import json,re,hashlib
from mugen_sff import Sff
R=Path(__file__).resolve().parents[1];O=R/'sprite-fighter/jus-upgrade';E=R/'sprite-fighter/engine/ikemen-go-v1.0.0'
profiles=json.loads((R/'sprite-fighter/face-audit/identity-scale-v5/profiles.json').read_text())['fighters']
PROFILES={p['slug']:p for p in profiles}
GROUPS={'baam':[62000,62100],'jin-mori':[62000,62300],'vikir':[50,51,52,53],'urkel':[20,30],'goku':list(range(62000,62008)),'gt-goku':list(range(62000,62005)),'ichigo':[62000]+list(range(62002,62012)),'luffy':list(range(62000,62005))}
LABELS={'baam':['Baam','Jyu Viole Grace'],'jin-mori':['Jin Mori with green goggles','Monkey King Jin Mori with gold circlet'],'vikir':['Vikir hunter','Vikir Night Hound with full face mask','Choco four-legged pet form','Vikir academy uniform'],'urkel':['Steve Urkel, glasses and suspenders','Stefan Urquelle, preserve accepted adult outfit'],'goku':['Base Goku','Super Saiyan Goku','Super Saiyan 2 Goku','Super Saiyan 3 Goku','Super Saiyan God Goku','Super Saiyan Blue Goku','Ultra Instinct Sign Goku','Mastered Ultra Instinct Goku'],'gt-goku':['Base GT Goku','Super Saiyan GT Goku','Super Saiyan 2 GT Goku','Super Saiyan 3 GT Goku','Super Saiyan 4 GT Goku'],'ichigo':['Ichigo form '+str(i) for i in range(11)],'luffy':['Base Luffy','Gear Second Luffy','Gear Third Luffy','Gear Fourth Luffy','Nightmare Luffy','Gear Fifth Luffy']}
cycles=[]
from ichigo_model import FORMS as ICHIGO_FORMS
from luffy_model import FORMS as LUFFY_FORMS
LABELS['ichigo']=[next(f['name'] for f in ICHIGO_FORMS if f['id']==g-62000) for g in GROUPS['ichigo']]
LABELS['luffy']=[f['name'] for f in LUFFY_FORMS]
for slug,groups in GROUPS.items():
 p=PROFILES[slug];n=E/'chars'/p['engine'];air=(O/'before/chars'/p['engine']/p['air']).read_text(encoding='cp1252');source=Sff(n/p['sff'])
 actions=[]
 for block in re.split(r'(?=^\s*\[Begin Action\s+)',air,flags=re.M|re.I):
  match=re.match(r'\s*\[Begin Action\s+(\d+)\]',block,re.I)
  if not match:continue
  action=int(match[1])
  if action%1000 not in (20,21):continue
  if slug=='urkel' and action not in (20,21,10020,10021):continue
  frames=[]
  for line in block.splitlines():
   if re.match(r'^\s*\d+\s*,\s*\d+\s*,',line):frames.append([x.strip() for x in line.split(';')[0].split(',')])
  if not frames:continue
  keys={tuple(map(int,f[:2])) for f in frames}
  # The same numeric suffix also occurs on hurt/effect actions. They are NOT
  # walk cycles and must never be replaced with healthy walking drawings.
  if slug!='urkel':
   allowed=(1,2) if slug=='jin-mori' and int(frames[0][0])==62300 else (2,3)
   if any(i not in allowed for g,i in keys):continue
  if len(keys)<=2 and all(g in groups for g,i in keys):actions.append(dict(action=action,group=int(frames[0][0]),frames=frames))
 for bank,group in enumerate(groups):
  matched=[a for a in actions if a['group']==group]
  assert matched,(slug,group)
  key=(group,0) if (group,0) in source.keys else tuple(map(int,matched[0]['frames'][0][:2]))
  index=source.keys[key];im=source.decode(index);axis=source.headers[index][4:6]
  folder=O/'art'/slug/'cycles'/str(group);folder.mkdir(parents=True,exist_ok=True);im.save(folder/'reference.png')
  label=LABELS[slug][bank];special=''
  if slug=='vikir' and group==52:special='This is a FOUR-LEGGED animal. Draw an eight-phase natural quadruped trot, preserving all four paws, muzzle, tail and fur. No human body or clothing.'
  elif slug=='luffy' and bank in (1,2,3):special='Preserve the exact huge, inflated/muscular body and anatomy of this form. Animate its characteristic light bouncing/hovering advance with articulated feet and arms; do not turn it into the normal slim human body.'
  else:special='A natural eight-phase walk, with counterphase arm swing and genuine leg contact/down/passing/high poses. Frames1 and5 have OPPOSITE leading legs. No high marching knees.'
  prompt=f'''Create a production 2D fighting-game movement sprite atlas for {label}, STRICTLY based on the attached actual accepted in-game drawing. Retain exactly its illustrated/comic rendering, facial anatomy, hair color/style, eyes, headwear/mask, every costume piece, weapon and character/form identity. No redesign, no pixel conversion, no photorealism. Draw EXACTLY EIGHT distinct articulated whole-body poses on a spacious 4-columns by 2-rows grid with wide transparent gutters and external margins. Face SCREEN RIGHT at the same side/three-quarter side angle in all frames. All eight figures have identical anatomical proportions and head size; feet share a fixed baseline in each row. {special} Read poses left to right top to bottom as one seamless cycle returning to frame1. Keep the whole hair, feet, cloak, tail and any weapon completely INSIDE its own cell. Overlapping cloth/hair motion follows the body; no weapon teleporting. Transparent background, no scenery, labels, writing, grid lines, effects or ground shadows. Simple crisp ink and flat hard shadows matching the reference, no generic AI face. Approximately 1600x1000 landscape.'''
  if not (folder/'walk.prompt.txt').exists():(folder/'walk.prompt.txt').write_text(prompt,encoding='utf-8')
  existing=O/'art'/slug/'walk.png'
  row=dict(slug=slug,engine=p['engine'],sff=p['sff'],air=p['air'],source_group=group,output_group=64150+bank,label=label,reference_key=key,reference_axis=axis,reference_bounds=im.getbbox(),reference_sha256=hashlib.sha256((folder/'reference.png').read_bytes()).hexdigest(),folder=folder.relative_to(R).as_posix(),actions=matched,source_is_existing_root=bank==0 and existing.exists())
  cycles.append(row)
 del source
(O/'animation-cycles.json').write_text(json.dumps(dict(status='Inventory; generation and packing pending',cycles=cycles),indent=2))
print('Stiff banks:',len(cycles),'walk actions:',sum(len(c['actions']) for c in cycles),'existing generated root sheets:',sum(c['source_is_existing_root'] for c in cycles))
