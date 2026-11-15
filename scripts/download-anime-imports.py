"""Fetch creator-linked Naruto/Saitama packages and extract character data only."""
from pathlib import Path,PurePosixPath
import urllib.request,re,html,json,hashlib,subprocess,concurrent.futures,sys
R=Path(__file__).resolve().parents[1];SEVEN=Path('C:/Program Files/7-Zip/7z.exe')
SPECS={
 'saitama':dict(creator='BoyBoyz',listing='https://mugenfreeforall.com/topic/27366-saitama-one-punch-man-13-mar-2017/',release='https://www.mediafire.com/?5g9ey4rupgd6ot5',archive='Saitama.zip'),
 'naruto':dict(creator='ViniciuSonico; upstream credits to be confirmed from package',listing='https://www.youtube.com/watch?v=l4aXsRu5Yr4',release='https://www.mediafire.com/file/si0mmjlhlmgf638/Naruto_JUS2.7z/file',archive='Naruto_JUS2.7z'),
 'gojo':dict(creator='RyoumenS, based on Arthur Mugen; verify package credits',listing='https://www.youtube.com/watch?v=7i9ZrSwWMI8',release='https://www.mediafire.com/file/wczf6d44hvnk1yr/Gojo_Satoru_%2528Shinjuku%2529.rar/file',archive='Gojo_Satoru.rar')}
def fetch(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=90)
def run(slug,spec):
 out=R/'sprite-fighter/characters'/slug/'source';out.mkdir(parents=True,exist_ok=True)
 archive=out/spec['archive']
 with fetch(spec['release']) as response:page=response.read().decode('utf-8',errors='replace')
 (out/'download-page.html').write_text(page,encoding='utf-8')
 tag=next(t for t in re.findall(r'<a\b[^>]*>',page) if 'id="downloadButton"' in t);direct=html.unescape(re.search(r'href="([^"]+)"',tag)[1])
 if not archive.exists():
  with fetch(direct) as response,archive.with_suffix(archive.suffix+'.part').open('wb') as stream:
   total=0
   while chunk:=response.read(1024*1024):
    total+=len(chunk);assert total<512*1024*1024,'Unexpected archive size';stream.write(chunk)
  archive.with_suffix(archive.suffix+'.part').rename(archive)
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()
 result=subprocess.run([str(SEVEN),'l','-slt','-ba','-sccUTF-8',str(archive)],capture_output=True,check=True)
 listing=result.stdout.decode('utf-8').replace('\r\n','\n');(out/'archive-listing.txt').write_text(listing,encoding='utf-8');selected=[]
 allowed={'.def','.cns','.cmd','.cmnd','.air','.sff','.snd','.act','.txt','.zss','.st','.st1','.st2','.st3','.st4','.reb1','.png','.jpg','.jpeg','.gif','.pcx','.wav','.mp3','.ogg','.pal','.ini'}
 for block in listing.split('\n\n'):
  m=re.search(r'^Path = (.+)$',block,re.M)
  if not m or re.search(r'^Folder = \+',block,re.M):continue
  path=m[1].strip().replace('\\','/');parts=PurePosixPath(path)
  assert not parts.is_absolute() and '..' not in parts.parts and ':' not in path and not path.startswith('-'),path
  assert not re.search(r'^(Symbolic Link|Hard Link) =[^\S\n]*\S',block,re.M),path
  if parts.suffix.lower() in allowed:selected.append(m[1].strip())
 assert selected
 subprocess.run([str(SEVEN),'x',str(archive),'-o'+str(out/'upstream'),'-y',*selected],capture_output=True,check=True)
 for p in (out/'upstream').rglob('*'):assert p.resolve().is_relative_to((out/'upstream').resolve())
 record=dict(status='Downloaded original archive; native import pending',**spec,download=direct,bytes=archive.stat().st_size,sha256=digest,extracted_data_files=selected,policy='Original archive retained unchanged; only character data and artwork extracted; no bundled executables run')
 (out/'source-report.json').write_text(json.dumps(record,indent=2));print('ANIME_SOURCE_READY',slug,record['bytes'],len(selected),flush=True)
 for p in (out/'upstream').rglob('*.def'):print(slug,str(p.relative_to(out)),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for result in pool.map(lambda pair:run(*pair),[(k,v) for k,v in SPECS.items() if not sys.argv[1:] or k in sys.argv[1:]]):pass
