"""Fetch and stage original MUGEN fighters before any artwork conversion."""
from pathlib import Path
import importlib.util,json,sys,concurrent.futures,io,re,html,urllib.parse

R=Path(__file__).resolve().parents[1]
QUEUE=R/'sprite-fighter/mugen-expansion/queue.json'

def download(row):
    try:
        spec=importlib.util.spec_from_file_location('archive_fetch',R/'scripts/download-anime-imports.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        source=dict(row['source']);folder=R/'sprite-fighter/characters'/row['slug']/'source'
        if (folder/'source-report.json').exists() and (folder/'upstream').exists():
            return row['slug'],'Source already staged'
        provider=source.pop('provider','mediafire')
        if provider!='mediafire':
            fetch=module.fetch;release=source['release']
            direct=release
            if provider=='google-drive':
                identifier=re.search(r'/d/([^/]+)',release)[1]
                direct='https://drive.google.com/uc?export=download&id='+identifier
                page=fetch(direct).read()
                if page.lstrip().startswith(b'<!DOCTYPE html>'):
                    text=page.decode();form=re.search(r'<form[^>]*id="download-form"[^>]*action="([^"]+)"',text)[1]
                    fields=dict(re.findall(r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"',text))
                    direct=html.unescape(form)+'?'+urllib.parse.urlencode(fields)
            served=False
            def wrapped(url):
                nonlocal served
                if url==release and not served:
                    served=True
                    return io.BytesIO(('<a id="downloadButton" href="'+html.escape(direct,quote=True)+'">Download</a>').encode())
                return fetch(url)
            module.fetch=wrapped
        module.run(row['slug'],source)
        return row['slug'],'Downloaded original archive; import pending'
    except Exception as exc:return row['slug'],'Download failed: '+str(exc)

if __name__=='__main__':
    data=json.loads(QUEUE.read_text(encoding='utf-8'))
    requested=sys.argv[2:]
    if sys.argv[1]=='download':
        rows=[r for r in data['fighters'] if r.get('source') and (not requested or r['slug'] in requested)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for slug,status in pool.map(download,rows):
                next(r for r in data['fighters'] if r['slug']==slug)['status']=status
                QUEUE.write_text(json.dumps(data,indent=2),encoding='utf-8')
                print(slug,status,flush=True)
