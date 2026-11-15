"""Export the actual review player with compact, validated frame tokens."""
from pathlib import Path
import json,re,sys,hashlib
folder=Path(__file__).resolve().parents[1]/'sprite-fighter/characters'/sys.argv[1]
page=(folder/'review.html').read_text(encoding='utf-8')
script=re.search(r'<script>(window\.[A-Z_]+_REVIEW=.*?)</script>',page,re.S)[1]
variable,payload=script.split('=',1);encoded,player=payload.split(';const data=',1)
data=json.loads(encoded)
for paths in data['clips'].values():
 for path in paths:assert (folder/path).is_file(),path
compact=dict(groups=data['groups'],ticks=data['ticks'],counts={key:len(value) for key,value in data['clips'].items()})
result=dict(variable=variable.removeprefix('window.'),player='const data='+player,data=compact,review_sha256=hashlib.sha256((folder/'review.html').read_bytes()).hexdigest(),runtime_sha256=json.loads((folder/'build-report.json').read_text())['runtime_sha256'])
print(json.dumps(result))
