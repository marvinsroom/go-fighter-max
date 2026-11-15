"""Test the official free Hunyuan3D Space with our generated Will reference.

No accounts, API tokens, paid inference or automatic retries are used.
"""
from pathlib import Path
import json
import time
import argparse
from gradio_client import Client, handle_file

root = Path(__file__).resolve().parents[1]
out = root / 'characters/will/reference-reconstruction'
image = out / 'will-head-input-v1.png'
result_file = out / 'generation-result.json'
parser=argparse.ArgumentParser()
parser.add_argument('--version',choices=['2','2.1'],default='2')
parser.add_argument('--shape-only',action='store_true')
args=parser.parse_args()
service='tencent/Hunyuan3D-'+args.version
host='https://tencent-hunyuan3d-'+('2-1' if args.version=='2.1' else '2')+'.hf.space/'
client = Client(host,
                download_files=str(out / 'downloads'), verbose=False)
api = client.view_api(return_format='dict', print_info=False)
(out / 'service-api.json').write_text(json.dumps(api, indent=2))
print('Submitting reference image to',service,'shape-only' if args.shape_only else 'textured',flush=True)
started = time.monotonic()
try:
    endpoint='/shape_generation' if args.shape_only else '/generation_all'
    values={'caption':'','image':handle_file(str(image)),
            'mv_image_front':None,'mv_image_back':None,'mv_image_left':None,'mv_image_right':None,
            'steps':30,'guidance_scale':5.0,'seed':2718,'octree_resolution':384,
            'check_box_rembg':False,'num_chunks':8000,'randomize_seed':False}
    params=api['named_endpoints'][endpoint]['parameters']
    arguments=[values[p['parameter_name']] if p['parameter_name'] in values else p.get('parameter_default') for p in params]
    job = client.submit(*arguments,api_name=endpoint)
    while not job.done():
        if time.monotonic()-started > 600:
            job.cancel()
            raise TimeoutError('Generation exceeded 10 minutes; cancelled without retry.')
        print('Generation status:', job.status(), flush=True)
        time.sleep(10)
    result = job.result()
    result_file.write_text(json.dumps({'service':service,
        'elapsed_seconds':time.monotonic()-started,'result':result},indent=2,default=str))
    print('GENERATION_RESULT', json.dumps(result,default=str), flush=True)
except Exception as error:
    result_file.write_text(json.dumps({'service':service,
        'error_type':type(error).__name__,'error':str(error)},indent=2))
    print('GENERATION_FAILED', type(error).__name__, str(error), flush=True)
    raise
