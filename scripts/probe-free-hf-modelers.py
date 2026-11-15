"""Read public Space status and API schema without uploading project data."""
from pathlib import Path
from urllib.request import urlopen
from gradio_client import Client
import json
out=Path(__file__).resolve().parents[1]/'characters/will/hf-free-modeler-check'
out.mkdir(exist_ok=True)
results=[]
for space in ['Stable-X/Hi3DGen','VAST-AI/TripoSG']:
    row={'space':space}
    try:
        with urlopen('https://huggingface.co/api/spaces/'+space,timeout=30) as response:meta=json.load(response)
        row.update(runtime=meta.get('runtime'),private=meta.get('private'),host=meta.get('host'))
        if meta.get('runtime',{}).get('stage')=='RUNNING':
            client=Client(space,token=False,verbose=False)
            api=client.view_api(return_format='dict',print_info=False)
            (out/(space.replace('/','-')+'-api.json')).write_text(json.dumps(api,indent=2),encoding='utf-8')
            row['endpoints']=list(api.get('named_endpoints',{}))
    except Exception as error:row['error']=str(error)
    results.append(row);print(json.dumps(row),flush=True)
(out/'space-status.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
