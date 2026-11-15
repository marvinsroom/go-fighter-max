// Exercise the actual shared player for every character and validate its files.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.resolve(__dirname,'../sprite-fighter/characters');
class Element{
 constructor(){this.children=[];this.value='';this.dataset={};this.textContent='';}
 append(child){this.children.push(child);if(this.children.length===1)this.value=child.value;}
 replaceChildren(){this.children=[];this.value='';}
 removeAttribute(key){delete this[key];}
 setAttribute(key,value){this[key]=value;}
}
function verify(slug){
 const folder=path.join(root,slug),html=fs.readFileSync(path.join(folder,'review.html'),'utf8');
 const elements={};for(const id of ['category','clip','capture','detail','status','play','previous','next','speed','ultimates'])elements[id]=new Element();
 if(html.includes('id="sheets"')){elements.sheets=new Element();elements.atlas=new Element();}
 elements.speed.value='1';const timers=new Map();let nextTimer=0;
 const context={window:{},document:{getElementById:id=>elements[id]||null,createElement:()=>new Element()},setTimeout:(fn,ms)=>{timers.set(++nextTimer,{fn,ms});return nextTimer},clearTimeout:id=>timers.delete(id)};
 vm.createContext(context);for(const m of html.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],context);
 const data=context.window.FIGHTER_REVIEW;assert(data&&data.slug===slug);assert.equal(elements.category.value,'Ultimates');
 assert.equal(elements.ultimates.children.length,{rimuru:3,cid:4,jinwoo:7,pyowol:1}[slug]);
 let checked=0,frames=0;
 for(const [group,names] of Object.entries(data.groups)){
  elements.category.value=group;elements.category.onchange();assert.equal(elements.clip.children.length,names.length);
  for(const name of names){
   elements.clip.value=name;elements.clip.onchange();assert.equal(timers.size,0,'Wait for image load');
   const first=elements.capture.src;elements.capture.onload();assert.equal(timers.size,1,'One playback timer');
   const timer=[...timers.values()][0];assert(timer.ms>=16);timer.fn();assert.equal(timers.size,0);
   elements.previous.onclick();assert.equal(elements.capture.src,first);elements.next.onclick();
   for(const f of data.cases[name]){assert(fs.existsSync(path.join(folder,f.src)),`${slug}: ${f.src}`);frames++;}
   checked++;
  }
 }
 for(const button of elements.ultimates.children){button.onclick();assert.equal(elements.clip.value,button.dataset.clip);assert.equal(button['aria-pressed'],'true');assert.equal(elements.ultimates.children.filter(b=>b['aria-pressed']==='true').length,1);checked++;}
 elements.play.onclick();assert.equal(elements.play.textContent,'Play');elements.capture.onload();assert.equal(timers.size,0);
 elements.play.onclick();assert.equal(elements.play.textContent,'Pause');assert.equal(timers.size,1);
 elements.capture.onerror();assert.equal(timers.size,0);assert.equal(elements.play.textContent,'Play');assert(elements.detail.textContent.includes('Capture unavailable'));
 elements.clip.onchange();elements.capture.onload();elements.play.onclick();assert.equal(timers.size,1);
 if(elements.sheets)for(const button of elements.sheets.children){button.onclick();assert(fs.existsSync(path.join(folder,elements.atlas.src)));}
 assert(!/<script src="review-data/.test(html),'Capture data must travel with the page');
 assert(html.indexOf('id="viewer"')<html.indexOf('id="controls"'),'Captures precede controls');
 for(const target of html.matchAll(/(?:src|href)="([^"]+)"/g))if(!/^(https?:|#|data:)/.test(target[1]))assert(fs.existsSync(path.resolve(folder,target[1].split('?')[0])),target[1]);
 checked+=4;console.log('REVIEW_VERIFIED',slug,checked,'interaction checks;',frames,'frame references');
 return html;
}
exports.verify=verify;
if(require.main===module){
 const pages=['rimuru','cid','jinwoo','pyowol'].map(verify);
 const css=pages.map(p=>p.match(/<style>([\s\S]*?)<\/style>/)[1]);assert(css.every(c=>c===css[0]),'Shared styles');
 const js=pages.map(p=>[...p.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1]);assert(js.every(s=>s===js[0]),'Shared player');
 console.log('REVIEW_CONSISTENCY shared styles and player match across all four pages');
}
