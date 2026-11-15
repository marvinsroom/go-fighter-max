"""One free public Hi3DGen geometry attempt using only the isolated head reference."""
from pathlib import Path
import json,time,shutil
from gradio_client import Client,handle_file
root=Path(__file__).resolve().parents[1];out=root/'characters/will/hi3dgen-head-v1'
out.mkdir(exist_ok=True)
source=root/'characters/will/reference-reconstruction/will-head-input-v1.png'
report={'service':'Stable-X/Hi3DGen','source':str(source.relative_to(root)),
        'status':'Starting','seed':2718,'payment_used':False,
        'scope':'Geometry-only head candidate; toon art and likeness not established'}
def save():(out/'generation-result.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
save()
try:
    client=Client('Stable-X/Hi3DGen',token=False,verbose=False,download_files=str(out/'downloads'))
    api=client.view_api(return_format='dict',print_info=False)
    params=api['named_endpoints']['/generate_3d']['parameters']
    names=[p['parameter_name'] for p in params]
    print('GENERATION_PARAMETERS',names,flush=True)
    report['status']='Submitted';save()
    job=client.submit(image=handle_file(str(source)),seed=2718,
        ss_guidance_strength=3,ss_sampling_steps=50,
        slat_guidance_strength=3,slat_sampling_steps=6,api_name='/generate_3d')
    start=time.monotonic()
    while not job.done():
        if time.monotonic()-start>600:
            job.cancel();raise TimeoutError('Generation exceeded ten minutes; no automatic retry')
        print('HI3DGEN',str(job.status()),flush=True);time.sleep(10)
    result=job.result()
    (out/'service-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    def paths(value):
        if isinstance(value,str):yield value
        elif isinstance(value,dict):
            for v in value.values():yield from paths(v)
        elif isinstance(value,(list,tuple)):
            for v in value:yield from paths(v)
    meshes=[Path(p) for p in paths(result) if p.lower().endswith('.glb') and Path(p).is_file()]
    assert meshes,'No downloaded GLB returned'
    target=out/'will-head-raw.glb';shutil.copy2(meshes[0],target)
    report.update(status='Downloaded',model=target.name,bytes=target.stat().st_size,
                  elapsed_seconds=round(time.monotonic()-start,1));save()
    print('HI3DGEN_GLB_DOWNLOADED',target.stat().st_size,flush=True)
except Exception as error:
    report.update(status='Failed',error_type=type(error).__name__,error=str(error));save()
    print('HI3DGEN_FAILED',type(error).__name__,str(error),flush=True)
    raise
