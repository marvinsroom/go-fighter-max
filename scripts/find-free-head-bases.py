"""Fetch public listing metadata and previews; never viewer mesh caches or credentials."""
from pathlib import Path
import json, urllib.request, urllib.error
root=Path(__file__).resolve().parents[1]/'characters/will/base-candidates'
root.mkdir(exist_ok=True)
models={'african-head-sonicvisual':'da5b4f12096a479597dace07c3693a3e',
        'will-regular-size':'270d309aaee94c58bfe269e432686511'}
report=[]
for name,uid in models.items():
    folder=root/name;folder.mkdir(exist_ok=True)
    try:
        request=urllib.request.Request('https://api.sketchfab.com/v3/models/'+uid,headers={'User-Agent':'CharacterAssetReview/1.0'})
        with urllib.request.urlopen(request,timeout=30) as response:metadata=json.load(response)
        (folder/'public-metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
        thumbs=metadata.get('thumbnails',{}).get('images',[])
        if thumbs:
            preview=max(thumbs,key=lambda i:i.get('width',0))
            urllib.request.urlretrieve(preview['url'],folder/'listing-preview.jpg')
        entry={'name':name,'listing':metadata.get('viewerUrl'),'license':metadata.get('license'),
               'downloadable':metadata.get('isDownloadable'),'preview':'listing-preview.jpg'}
        # Official documented download endpoint; a login requirement is a stopping point.
        try:
            with urllib.request.urlopen('https://api.sketchfab.com/v3/models/'+uid+'/download',timeout=30) as response:
                download=json.load(response)
            entry['official_download_status']='Available'
            # Do not print or persist temporary signed URLs.
            formats=[k for k,v in download.items() if isinstance(v,dict) and v.get('url')]
            if formats:
                fmt='glb' if 'glb' in formats else ('gltf' if 'gltf' in formats else formats[0])
                suffix='.glb' if fmt=='glb' else '.zip'
                urllib.request.urlretrieve(download[fmt]['url'],folder/('original'+suffix))
                entry['downloaded']='original'+suffix
        except urllib.error.HTTPError as error:entry['official_download_status']='HTTP '+str(error.code)+'; no login bypass attempted'
        report.append(entry)
    except Exception as error:report.append({'name':name,'error':str(error)})
(root/'sketchfab-candidates.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for entry in report:print(entry['name'],entry.get('official_download_status',entry.get('error')),flush=True)
