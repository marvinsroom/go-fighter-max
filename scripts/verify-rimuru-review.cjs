// Execute the real review JavaScript against a small DOM model.
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'../sprite-fighter/characters/rimuru');
class Element{
 constructor(){this.children=[];this.value='';this.dataset={};this.textContent='';}
 append(child){this.children.push(child);if(this.children.length===1)this.value=child.value;}
 replaceChildren(){this.children=[];this.value='';}
 removeAttribute(name){delete this[name];}
 setAttribute(name,value){this[name]=value;}
}
const elements={};for(const id of ['category','clip','capture','detail','status','play','previous','next','speed','ultimates'])elements[id]=new Element();elements.speed.value='1';
const context={window:{},document:{getElementById:id=>elements[id],createElement:()=>new Element()},setTimeout:()=>1,clearTimeout:()=>{}};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'review-data.js'),'utf8'),context);
const html=fs.readFileSync(path.join(root,'review.html'),'utf8');
for(const m of html.matchAll(/<script>([\s\S]*?)<\/script>/g))vm.runInContext(m[1],context);
let checks=0;
assert(!html.includes('<script src="review-data.js'), 'Review must contain its own matching capture data');
assert.equal(elements.category.value,'Ultimates');
assert.equal(elements.ultimates.children.length,3);
for(const button of elements.ultimates.children){button.onclick();assert.equal(button['aria-pressed'],'true');assert(elements.clip.value.includes(button.textContent));assert(fs.existsSync(path.join(root,elements.capture.src.split('?')[0])));checks++;}
for(const category of Object.keys(context.window.RIMURU_REVIEW.groups)){
 elements.category.value=category;elements.category.onchange();
 for(const clip of context.window.RIMURU_REVIEW.groups[category]){
  elements.clip.value=clip;elements.clip.onchange();assert(elements.capture.src.includes('replays/'));elements.capture.onload();
  elements.next.onclick();elements.previous.onclick();checks++;
 }
}
elements.play.onclick();assert.equal(elements.play.textContent,'Play');elements.play.onclick();assert.equal(elements.play.textContent,'Pause');
elements.capture.onerror();assert(elements.detail.textContent.includes('Capture unavailable'));checks+=3;
console.log('RIMURU_REVIEW_JS',checks,'interaction checks passed');
