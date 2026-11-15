"""Playable random shadow forms using the four authored shadow pose sets."""
import re

SHADOWS=('igris','beru','iron','tank')


def animations(assets):
    assets.action(2000,[('summon',18),('summon',12),('idle',12)])
    # Copy timing and collision declarations exactly. Only the visible drawing
    # changes, so a form cannot accidentally lose an active attack frame.
    source='\n'.join(assets.air)
    for form,name in enumerate(SHADOWS,1):
        for block in re.split(r'(?=\[Begin Action )',source):
            match=re.match(r'\[Begin Action (\d+)\]',block)
            if not match:continue
            number=int(match[1])
            if number>=6000:continue
            lines=block.strip().splitlines()
            drawings=[i for i,line in enumerate(lines) if re.match(r'50,',line)]
            if not drawings:continue
            lines[0]=f'[Begin Action {form*10000+number}]'
            attacking=number in (200,210,220,400,410,420,600,610,620,800,801,810,811,1000,1200,3010,3210)
            for index,line_index in enumerate(drawings):
                old=lines[line_index].split(',')
                pose=min(3,index*4//len(drawings)) if attacking else 3 if number in (6,10,11,47,5100,5110,5120,5140,5150,5160,5170) or 5000<=number<=5090 else 0
                previous=drawings[index-1]+1 if index else 1
                if attacking and any(line.startswith('Clsn1:') for line in lines[previous:line_index]):pose=2
                if number in (20,21):pose=(index//2)%2
                m=assets.meta[f'{name}_{pose}'];scale=m['scale']
                lines[line_index]=f'51,{m["number"]},0,0,{old[4]},,,{scale:.7f},{scale:.7f},0'
            assets.air.extend(['\n'+'\n'.join(lines)])


def states(state,ctl,end):
    ctl(-2,'Random shadow form drawing','ChangeAnim',
        ['var(45)>0','anim<10000','selfanimexist(anim+var(45)*10000)'],
        value='anim+var(45)*10000',elem='animelemno(0)')
    ctl(-2,'Restore Monarch drawing','ChangeAnim',
        ['var(45)=0','anim>=10000','selfanimexist(anim%10000)'],
        value='anim%10000',elem='animelemno(0)')
    # Add the move later, after the global controllers have been authored.


def move(state,ctl,end):
    state(2000,2000,velset='0,0')
    ctl(2000,'Remember whether returning','VarSet','time=0',**{'var(46)':'var(45)'})
    ctl(2000,'Choose random playable shadow','VarSet','time=18',
        **{'var(45)':'ifelse(var(46)>0,0,1+random%4)'})
    ctl(2000,'Reveal selected form immediately','ChangeAnim','time=18',value=2000,elem=2)
    ctl(2000,'Shadow eruption','Explod','time=18',anim=6405,ID=6900,
        postype='p1',pos='0,-110',removetime=-2,sprpriority=5,ownpal=1)
    ctl(2000,'Transformation cue','PlaySnd','time=18',value='0,3')
    ctl(2000,'Transformation flash','PalFX','time=18',time=12,add='80,20,140',mul='256,256,256')
    end(2000)
