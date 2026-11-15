// Runs the actual generated player; frame tokens retain source lengths/timings.
function verifyGokuReview(fixture) {
 const assert=(value,message)=>{if(!value)throw new Error(message)};
 class Element {
  constructor(){this.children=[];this.value='';this.dataset={};this.textContent='';}
  append(child){this.children.push(child);if(this.children.length===1)this.value=child.value;}
  replaceChildren(){this.children=[];this.value='';}
  setAttribute(name,value){this[name]=value;}
 }
 const elements=Object.fromEntries(['clip','play','category','screen','counter','categories','prev','next'].map(id=>[id,new Element()]));
 const timers=new Map();let serial=0,checks=0;
 const data={groups:fixture.data.groups,ticks:fixture.data.ticks,clips:Object.fromEntries(Object.entries(fixture.data.counts).map(([key,count])=>[key,Array.from({length:count},(_,index)=>key+'/'+index)]))};
 const window={[fixture.variable]:data};
 const document={getElementById:id=>elements[id],createElement:()=>new Element()};
 const setTimeout=(fn,ms)=>{timers.set(++serial,{fn,ms});return serial};
 const clearTimeout=id=>timers.delete(id);
 Function('window','document','setTimeout','clearTimeout',fixture.player)(window,document,setTimeout,clearTimeout);
 for(const [group,names] of Object.entries(data.groups)){
  elements.category.value=group;elements.category.onchange();
  assert(elements.clip.children.length===names.length,'Category contents');checks++;
  for(const name of names){
   elements.clip.value=name;elements.clip.onchange();const first=elements.screen.src;
   assert(first===data.clips[name][0]&&timers.size===0,'Select clip');checks++;
   elements.next.onclick();assert(elements.screen.src===data.clips[name][1%data.clips[name].length],'Step next');checks++;
   elements.prev.onclick();assert(elements.screen.src===first,'Step previous');checks++;
   elements.prev.onclick();assert(elements.screen.src===data.clips[name].at(-1),'Wrap previous');checks++;
   elements.play.onclick();assert(timers.size===1,'Start playback');checks++;
   const [id,timer]=[...timers][0];assert(timer.ms>=16,'Timing floor');timers.delete(id);timer.fn();
   assert(elements.screen.src===first&&timers.size===1,'Playback wrap');checks++;
   elements.play.onclick();assert(timers.size===0,'Pause playback');checks++;
   elements.screen.onerror();assert(elements.counter.textContent.includes('unavailable')&&timers.size===0,'Load error');checks++;
   elements.clip.onchange();assert(elements.screen.src===first,'Recover clip');checks++;
  }
 }
 for(const button of elements.categories.children){button.onclick();assert(elements.category.value===button.dataset.category,'Category shortcut');checks++;}
 return {status:'Complete',method:'Mock DOM and timer checks against the generated review script',interaction_checks:checks,clips:Object.keys(data.clips).length,review_sha256:fixture.review_sha256,runtime_sha256:fixture.runtime_sha256};
}
