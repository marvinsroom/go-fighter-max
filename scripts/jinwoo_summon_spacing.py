"""Body separation for illustrated shadow helpers; weapons may cross the gap."""
import math
import re
from jinwoo_hybrid_moves import PROFILES


def actor_actions(air):
    result = {}
    for block in re.split(r'(?=^\[Begin Action)', air, flags=re.I | re.M):
        action = re.match(r'\[Begin Action\s+(\d+)', block, re.I)
        if not action:
            continue
        names = set()
        for match in re.finditer(r'^\s*100[01]\s*,\s*(\d+)\s*,', block, re.M):
            n = int(match[1])
            names.add('igris' if n <= 10 or n == 51 else 'beru' if 11 <= n <= 19
                      else 'iron' if n in (23, 24, 25, 26, 260, 261)
                      else 'tank' if 35 <= n <= 37 else 'other')
        if len(names) == 1 and 'other' not in names:
            result[int(action[1])] = names.pop()
    result.update({870700 + i: name for i, name in enumerate(PROFILES)})
    return result


def guard(state, name):
    cfg = PROFILES[name]
    front = math.ceil(max(cfg['body'][2], cfg['head'][2])) + 2
    back = math.ceil(-min(cfg['body'][0], cfg['head'][0])) + 2
    # Width receives the helper's size scale in the engine, like the AIR boxes.
    # Only separate vertically overlapping bodies; aerial attacks keep their arc.
    common = 'triggerall=ishelper\ntriggerall=numenemy>0\ntriggerall=abs(p2dist y)<60\ntriggerall=p2dist x>=0\n'
    out = '; BEGIN PROJECT SHADOW SPACING\n'
    out += f'[State {state}, Shadow body width]\ntype=Width\ntrigger1=ishelper\nplayer={front},{back}\nignorehitpause=1\n'
    out += f'[State {state}, Shadow body separation]\ntype=PosAdd\n{common}trigger1=p2bodydist x<0\nx=p2bodydist x\nignorehitpause=1\n'
    # Cap only when overlapping; keep a minimum closing speed so assists still
    # rush forward instead of planting immediately on spawn.
    out += f'[State {state}, Shadow contact brake]\ntype=VelSet\n{common}trigger1=vel x>0\ntrigger1=p2bodydist x<8\nx=min(vel x,max(1.5,p2bodydist x))\n'
    return out + '; END PROJECT SHADOW SPACING\n'


def strip_adapters(text):
    return re.sub(r'; BEGIN PROJECT SHADOW SPACING\n.*?; END PROJECT SHADOW SPACING\n', '', text, flags=re.S)


def adapt(text, actions):
    out = []
    for block in re.split(r'(?=^\[statedef\s)', text, flags=re.I | re.M):
        state = re.match(r'\[statedef\s+(\d+)', block, re.I)
        animation = re.search(r'^\s*anim\s*=\s*(?:cond\(!ishelper[^\n]*?selfanimexist\(\()?([0-9]+)(?:\)|\s*$)', block, re.I | re.M)
        # Landing states inherit the previous animation rather than setting anim.
        inherited = {1420:'iron',1421:'iron',2130:'tank'}
        name = actions.get(int(animation[1])) if animation else inherited.get(int(state[1])) if state else None
        if state and name and not re.search(r'^\s*type\s*=\s*TargetBind\b', block, re.I | re.M):
            adapter = guard(int(state[1]), name)
            parts = re.split(r'(?=^\[state\s)', block, flags=re.I | re.M)
            # Run after source movement, including teleports, and before any exit.
            for i, part in enumerate(parts):
                if re.search(r'^\s*type\s*=\s*(ChangeState|SelfState|DestroySelf)\b', part, re.I | re.M):
                    parts[i] = adapter + part
            block = ''.join(parts) + adapter
        out.append(block)
    return ''.join(out)
