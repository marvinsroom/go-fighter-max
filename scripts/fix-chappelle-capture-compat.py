"""Fix only Will's victim animation selection; retain all combat controllers."""
from pathlib import Path
import re,hashlib,json
import will_agent_j as agent
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'sprite-fighter/engine/ikemen-go-v1.0.0/chars/will_full'
path=C/'will.cns';source=path.read_text();backup=C/'will-before-chappelle-captures.cns'
if not backup.exists():backup.write_text(source)
blocks=re.split(r'(?=\[Statedef )',source,flags=re.I);changed=[]
pattern=r'(\[State [^\]]+\]\s*\ntype=)ChangeAnim2?(\ntrigger1=time=0\nvalue=)[^\n]+'
for i,block in enumerate(blocks):
    head=re.match(r'\[Statedef (\d+)\]',block,re.I)
    if not head or int(head[1]) not in (820,821,1420,3050,3250,4550):continue
    number=int(head[1]);value=agent.victim_animation_value(number)
    updated,n=re.subn(pattern,lambda m:m[1]+'ChangeAnim'+m[2]+value,block)
    assert n==1,(number,n)
    # No damage, binds, velocity, meter, timing or control values may change.
    assert re.sub(pattern,'REACTION_ANIM',updated)==re.sub(pattern,'REACTION_ANIM',block)
    blocks[i]=updated;changed.append(number)
assert len(changed)==6,changed
path.write_text(''.join(blocks))
report={'changed_victim_states':changed,'scope':'Victim-owned form-aware ChangeAnim only; all other controllers byte-identical after newline normalization',
        'before_sha256':hashlib.sha256(source.encode()).hexdigest(),'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(ROOT/'sprite-fighter/characters/chappelle').mkdir(exist_ok=True)
(ROOT/'sprite-fighter/characters/chappelle/capture-compatibility.json').write_text(json.dumps(report,indent=2))
print('CHAPPELLE_CAPTURE_COMPATIBILITY',changed)
