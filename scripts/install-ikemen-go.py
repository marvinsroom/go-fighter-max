"""Download and extract the official pinned Windows build into this project."""
from pathlib import Path
import hashlib,json,urllib.request,zipfile
root=Path(__file__).resolve().parents[1]
version='v1.0.0';target=root/'sprite-fighter'/'engine'/('ikemen-go-'+version)
downloads=root/'tooling/downloads';downloads.mkdir(exist_ok=True)
request=urllib.request.Request('https://api.github.com/repos/ikemen-engine/Ikemen-GO/releases/tags/'+version,headers={'User-Agent':'SitcomFighterSetup'})
with urllib.request.urlopen(request,timeout=30) as response:release=json.load(response)
asset=next(a for a in release['assets'] if a['name']=='Ikemen_GO-'+version+'-windows.zip')
archive=downloads/asset['name']
if not archive.is_file():
    print('Downloading',asset['name'],asset['size'],'bytes',flush=True)
    urllib.request.urlretrieve(asset['browser_download_url'],archive)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
assert 'sha256:'+digest==asset['digest'],'Official release digest mismatch'
assert not target.exists(),'Existing engine directory preserved; install not overwritten'
with zipfile.ZipFile(archive) as bundle:
    for entry in bundle.infolist():
        path=(target/entry.filename).resolve()
        assert path.is_relative_to(target.resolve()),'Archive entry leaves engine directory'
    target.mkdir(parents=True)
    bundle.extractall(target)
executables=list(target.rglob('Ikemen_GO.exe'));assert len(executables)==1
report={'engine':'IKEMEN GO','version':version,'source':release['html_url'],
        'asset':asset['name'],'sha256':digest,'digest_verified':True,
        'executable':str(executables[0].relative_to(root)),'status':'Extracted; launch validation pending',
        'unreal_project_changed':False}
(root/'sprite-fighter/install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
