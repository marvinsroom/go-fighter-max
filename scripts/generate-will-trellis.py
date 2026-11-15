"""Test the official Microsoft TRELLIS.2 free Space with the cel-shaded Will input.

No tokens, account changes, paid endpoints, or automatic generation retries.
Only the isolated character reference is uploaded; no project files are sent.
"""
from pathlib import Path
import json,time,shutil
from gradio_client import Client,handle_file

root=Path(__file__).resolve().parents[1];out=root/'characters/will/trellis-cel-v1'
source=out/'will-cel-apose-input-v1.png'
result_file=out/'generation-result.json'
report={'service':'microsoft/TRELLIS.2','source':str(source),'resolution':'1024',
        'seed':2718,'target_faces':100000,'texture_size':2048,'status':'Starting'}
def save():result_file.write_text(json.dumps(report,indent=2))
def run(client,endpoint,**kwargs):
    started=time.monotonic();job=client.submit(api_name=endpoint,**kwargs)
    while not job.done():
        if time.monotonic()-started>600:
            job.cancel();raise TimeoutError(endpoint+' exceeded ten minutes')
        print(endpoint,str(job.status()),flush=True);time.sleep(10)
    return job.result()
save()
try:
    client=Client('https://microsoft-trellis-2.hf.space',token=False,verbose=False,download_files=str(out/'downloads'))
    client.predict(api_name='/start_session')
    print('Uploading isolated cel-shaded Will input to the official Microsoft TRELLIS.2 Space.',flush=True)
    processed=run(client,'/preprocess_image',input=handle_file(str(source)))
    report['status']='Generating';save()
    preview=run(client,'/image_to_3d',image=handle_file(processed),seed=2718,resolution='1024')
    if isinstance(preview,str):(out/'generated-preview.html').write_text(preview,encoding='utf-8')
    report['status']='Extracting GLB';save()
    result=run(client,'/extract_glb',decimation_target=100000,texture_size=2048)
    paths=[p for p in (result if isinstance(result,(list,tuple)) else [result]) if isinstance(p,str) and p.lower().endswith('.glb')]
    assert paths,'The Space returned no GLB file'
    final=out/'will-trellis-cel-raw.glb';shutil.copy2(paths[0],final)
    report.update(status='Downloaded',model=str(final),bytes=final.stat().st_size)
    save();print('TRELLIS_MODEL_DOWNLOADED',str(final),final.stat().st_size,flush=True)
except Exception as error:
    report.update(status='Failed',error_type=type(error).__name__,error=str(error));save()
    print('TRELLIS_GENERATION_FAILED',type(error).__name__,str(error),flush=True)
    raise
