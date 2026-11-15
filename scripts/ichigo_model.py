"""Imported all-forms IDs and reproducible source animation parsing."""
from pathlib import Path
import re
FORMS=[
 dict(id=0,slug='shikai',name='Shikai',base=0,design='Classic black shihakusho with a white lapel underlayer and white sash, orange spiky hair, oversized broad black Zangetsu cleaver sword with silver cutting edge and a trailing white hilt wrap.'),
 dict(id=2,slug='bankai',name='Bankai',base=11000,design='Classic Tensa Zangetsu Bankai: long fitted black coat with ragged tails, white lining and red inner trim, orange spiky hair, slim straight BLACK katana with black hilt and short dark chain. No mask.'),
 dict(id=3,slug='hollow-mask',name='Hollow mask',base=13000,design='Classic masked Bankai: orange spiky hair, black long Bankai coat, thin black Tensa Zangetsu katana, full white bone Hollow mask covering the face, narrow dark eye sockets with golden eyes, skeletal jaw/teeth and strong dark-red stripes concentrated on one side of the white mask. The mask remains fully visible in every pose.'),
 dict(id=5,slug='vasto-lorde',name='Vasto Lorde',base=17000,design='Full Hollow / Vasto Lorde Ichigo: long flowing orange hair, full white skull helmet with two long forward-curving horns, narrow dark eye slits, white skeletal armored torso with black Hollow chest opening and dark body markings, long black robe trousers and white armored feet, long black sword. White armor covers the entire upper torso. Match the horned fourth reference figure.'),
 dict(id=4,slug='dangai',name='Dangai',base=15000,design='Post-Dangai training Ichigo: longer orange hair reaching the neck, serious mature face, torn sleeveless black shihakusho, black trousers, white sash, exposed muscular arms, black chain wrapped around the right forearm and wrist linking to thin black Tensa Zangetsu katana. No mask, no horns.'),
 dict(id=6,slug='fullbring',name='Fullbring Shikai',base=19000,design='Restored Fullbring-enhanced Shikai Ichigo: short orange hair, black shihakusho and black trousers, white sash, pale bands near chest/upper arms, a large broad black cleaver sword with silver cutting edge and angular inner contours; match the sixth reference figure. No mask or horns.'),
 dict(id=7,slug='fullbring-bankai',name='Fullbring Bankai',base=21000,design='Fullbring-enhanced Bankai Ichigo: short spiky orange hair, fitted long black coat with jagged lower tails, prominent white skeletal crossed collar/chest trim, black forearm guards with white accents, black trousers, thin long black curved katana with silver edge and black chain. No mask or horns.'),
 dict(id=8,slug='true-shikai',name='True Shikai',base=23000,design='Thousand-Year Blood War True Shikai Ichigo: spiky orange hair, black shihakusho, broad white cloth straps crossing the torso/shoulders and white waist sash, TWO solid black Zangetsu blades: a large broad cleaver in the right hand and a short broad blade in the left. Black blade faces with silver cutting edges. No mask, no horns.'),
 dict(id=9,slug='horn-of-salvation',name='Horn of Salvation',base=25000,design='Horn of Salvation True Shikai Ichigo: spiky orange hair, exactly ONE long pale forward-curving horn on the left side of his head, left half of face covered in white Hollow bone material with dark markings, one golden Hollow eye, left arm pale white with dark markings, black shihakusho, crossing white straps and sash, TWO black Zangetsu cleavers one large and one short. Keep the single horn and half-white face visible in every pose.'),
 dict(id=10,slug='true-bankai',name='True Bankai',base=27000,design='Thousand-Year Blood War True Bankai Ichigo: short spiky orange hair, sleeveless black shihakusho with torn tails, white sash and black trousers, a single enormous Zangetsu sword with thick WHITE outer cleaver shell surrounding the black inner blade, a dark chain linking the tip/edge area to the grip, black hilt. No mask or horns.'),
 dict(id=11,slug='true-bankai-hos',name='True Bankai + Horn',base=29000,design='True Bankai with Horn of Salvation: short orange hair, exactly ONE long pale horn curving forward from the left of head, left half face white bone with dark markings and golden Hollow eye, pale left arm with black markings, sleeveless black shihakusho, white sash, black trousers. One huge Zangetsu sword with thick WHITE outer cleaver shell around a black inner blade and a dark chain near the blade. Single horn stays fully visible in all poses.'),
]
BY_ID={f['id']:f for f in FORMS}
def actions(text):
    result={}
    for block in re.split(r'(?=\[Begin Action\s+)',text,flags=re.I):
        m=re.match(r'\[Begin Action\s+(\d+)\]',block,re.I)
        if not m:continue
        rows=[]
        for line in block.splitlines():
            if not re.match(r'^\s*-?\d+\s*,\s*-?\d+\s*,',line):continue
            f=[x.strip() for x in line.split(';',1)[0].split(',')]
            if len(f)<5:continue
            rows.append(dict(key=tuple(map(int,f[:2])),x=int(f[2]),y=int(f[3]),ticks=int(f[4]),fields=f))
        result[int(m[1])]=rows
    return result

def source_folder(root):return Path(root)/'sprite-fighter/characters/ichigo/source/upstream/Ichigo'

def command_routes(text):
    routes=[]
    for block in re.split(r'(?=^\[State\s+-1,)',text,flags=re.I|re.M):
        if not re.search(r'^type\s*=\s*ChangeState',block,re.I|re.M):continue
        command=re.search(r'command\s*=\s*"(SPECIAL [1-6]|SUPER[12])"',block,re.I)
        form=re.search(r'var\(2\)\s*=\s*(\d+)',block,re.I)
        value=re.search(r'^value\s*=\s*([^\n;]+)',block,re.I|re.M)
        cost=re.search(r'power\s*>=\s*(\d+)',block,re.I)
        if not all((command,form,value)):continue
        number=re.fullmatch(r'(\d+)\s*',value[1])
        if not number:number=re.search(r'ifelse\(statetype\s*=\s*A,\s*\d+,\s*(\d+)\)',value[1],re.I)
        if not number:continue
        name=block.splitlines()[0]
        routes.append(dict(form=int(form[1]),command=command[1].upper(),state=int(number[1]),cost=int(cost[1]) if cost else 0,name=name))
    return routes
