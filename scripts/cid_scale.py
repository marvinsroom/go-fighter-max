"""Adapt imported cinematic body copies to the illustrated fighter's native size."""
import hashlib,re


def adapt_text(name,text):
    changes=[];state=None;out=[]
    for block in re.split(r'(?=^\[)',text,flags=re.M):
        header=re.match(r'\[statedef\s+(-?\d+)',block,re.I)
        if header:state=int(header[1])
        kind=re.search(r'^\s*type\s*=\s*(\w+)\s*$',block,re.I|re.M)
        if kind and kind[1].lower()=='zoom' and name=='Fx.cns' and state in (801,802,803):
            block=re.sub(r'(?im)^scale\s*=.*$', 'scale = 1',block)
            changes.append({'state':state,'kind':'Stable shared camera','scale':1})
        if kind and kind[1].lower()=='explod':
            anim=re.search(r'^anim\s*=\s*(\d+)\s*$',block,re.I|re.M)
            if anim:
                n=int(anim[1]);scale=None
                if name=='Atomic.cns' and n in (3000,3005,3030):
                    scale='const(size.xscale),const(size.yscale)'
                elif name=='Skills.cns' and 1401<=n<=1409:
                    scale='root,const(size.xscale),root,const(size.yscale)'
                if scale:
                    block=re.sub(r'(?im)^scale\s*=.*$', 'scale = '+scale,block)
                    changes.append({'state':state,'kind':'Body copy matches root','animation':n,'scale':scale})
        out.append(block)
    return ''.join(out),changes


def install(up,out):
    report={}
    for name in ('Atomic.cns','Skills.cns','Fx.cns'):
        original=(up/name).read_text(encoding='cp1252')
        adapted,changes=adapt_text(name,original)
        (out/name).write_text(adapted,encoding='utf-8')
        report[name]={'changes':changes,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest()}
    return report
