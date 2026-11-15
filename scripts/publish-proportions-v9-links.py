"""Link current artwork while retaining explicitly historical recordings."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1];G=R/'sprite-fighter'
for slug in ['lloyd','jin-mori']:
 p=G/'characters'/slug/'review.html';s=p.read_text(encoding='utf-8');block='<aside id="proportions-v9-current" style="padding:18px;background:#24364a;color:#eef4ff"><a style="color:#b6d9ff" href="../../proportions-v9/review.html">Current Lloyd and Jin Mori redesigns: before/after and walk playback</a>. Smaller heads, longer limbs and leaner builds, installed at the agreed JUS gameplay sizes. Earlier recordings below show previous artwork; fresh recordings are deferred.</aside>'
 s=re.sub(r'<aside id="proportions-v9-current".*?</aside>','',s,flags=re.S);s=s.replace('<main>','<main>'+block,1);s=s.replace('Current comic redraws and prompts','Earlier comic redraws and prompts');p.write_text(s,encoding='utf-8')
 for version in ['comic-style-v4','comic-identity-v3']:
  p=G/'characters'/slug/'art'/version/'design-review.html'
  if p.exists():
   s=p.read_text(encoding='utf-8');mark='<p id="proportions-v9-current"><a href="../../../../proportions-v9/review.html">Current proportion redesigns and installed animation comparison</a>. This page retains earlier artwork.</p>'
   if 'id="proportions-v9-current"' not in s:s=re.sub(r'(<body[^>]*>)',lambda m:m[0]+mark,s,count=1)
   p.write_text(s,encoding='utf-8')
for name,link in [('face-audit/style-v4-review.html','../proportions-v9/review.html'),('size-fix-v8/review.html','../proportions-v9/review.html'),('jus-upgrade/review.html','../proportions-v9/review.html')]:
 p=G/name;s=p.read_text(encoding='utf-8');mark='<p id="proportions-v9-current"><a href="'+link+'">New: Lloyd and Jin Mori proportion redesigns</a> — installed longer limbs, smaller heads and leaner builds at the same JUS gameplay sizes.</p>'
 if 'id="proportions-v9-current"' not in s:s=s.replace('<main>','<main>'+mark,1)
 p.write_text(s,encoding='utf-8')
p=G/'README.md';s=p.read_text(encoding='utf-8');line='**Latest artwork fixes:** [Lloyd and Jin Mori redesigns](proportions-v9/review.html), including Monkey King and full walk cycles. Open **Review Lloyd and Mori Redesigns.cmd**. Recordings remain deferred.\n\n'
if 'Latest artwork fixes' not in s:s=s.replace('\n','\n\n'+line,1)
p.write_text(s,encoding='utf-8');print('PROPORTIONS_LINKS_PUBLISHED')
