"""Verify roster links, exact production hashes, provenance and aggregate proof."""
from manhwa_expansion import BATCH
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'sprite-fighter';E=S/'engine/ikemen-go-v1.0.0'
aggregate=json.loads((S/'manhwa-expansion-validation.json').read_text());assert aggregate['status']=='Complete' and aggregate['total_gameplay']==66*len(BATCH) and aggregate['total_browser']==172*len(BATCH)
select=(E/'data/select.def').read_text(encoding='utf-8')
for slug,p in BATCH.items():
 folder=S/'characters'/slug;b=json.loads((folder/'build-report.json').read_text());r=json.loads((folder/'runtime-validation.json').read_text());v=json.loads((folder/'viewer-validation.json').read_text())
 assert r['status']=='Complete' and r['passed']==66 and not r['failed'] and r['runtime_sha256']==b['runtime_sha256']
 assert v['status']=='PASS' and v['assertions']==172 and v['clips']==39
 assert v['review_sha256']==hashlib.sha256((folder/'review.html').read_bytes()).hexdigest()
 assert len(re.findall('^'+p['id']+r'\s*,',select,re.M))==1
 for name,digest in b['runtime_sha256'].items():assert hashlib.sha256((E/'chars'/p['id']/name).read_bytes()).hexdigest()==digest
 requests=json.loads((folder/'art/illustrated-v1/generation-requests.json').read_text());assert len(requests)==5
 for request in requests:
  assert request['tool']=='built-in image_gen.imagegen' and request['transparent_background']
  assert (folder/'art/illustrated-v1'/request['file']).exists() and (folder/'art/illustrated-v1'/request['prompt']).exists()
  assert Path(request['original_generated_file']).exists()
 for label in ['Play '+p['name']+'.cmd','Fight '+p['name']+' CPU.cmd','Review '+p['name']+'.cmd']:assert (S/label).exists(),label
 assert json.loads((folder/'source/import-search.json').read_text())['status']=='No usable verifiable downloadable release found'
hub=(S/'manhwa-roster.html').read_text(encoding='utf-8');assert hub.count('<article>')==len(BATCH)
for ref in re.findall(r'(?:src|href)="([^"]+)"',hub):assert (S/ref).exists(),ref
for slug in ('baam','jin-mori','vikir','jin-mu-won','lloyd'):assert '../../manhwa-roster.html' in (S/'characters'/slug/'review.html').read_text(encoding='utf-8')
print('MANHWA_EXPANSION_VERIFIED',len(BATCH),'fighters;',66*len(BATCH),'gameplay checks;',172*len(BATCH),'browser assertions')
