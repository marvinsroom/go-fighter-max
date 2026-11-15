const data=window.ICHIGO_REVIEW;
const clip=document.getElementById('clip'),play=document.getElementById('play');
const category=document.getElementById('category'),screen=document.getElementById('screen');
let frame=0,timer=null;
function stop(){clearTimeout(timer);timer=null;play.textContent='Play samples'}
function draw(){
 const frames=data.clips[clip.value];if(!frames?.length)return;
 frame=(frame+frames.length)%frames.length;screen.src=frames[frame];
 document.getElementById('counter').textContent=`${category.value} · ${clip.value} · Frame ${frame+1} of ${frames.length}`;
}
function chooseCategory(name){
 stop();category.value=name;clip.replaceChildren();
 for(const name of data.groups[category.value]){
  const option=document.createElement('option');option.value=name;option.textContent=name;clip.append(option);
 }
 frame=0;draw();
 for(const button of document.getElementById('categories').children)button.setAttribute('aria-pressed',String(button.dataset.category===name));
}
function advance(){
 const t=data.ticks[clip.value],delay=frame<t.length-1?Math.max(60,(t[frame+1]-t[frame])*1000/60):500;
 timer=setTimeout(()=>{frame++;draw();advance()},delay);
}
for(const name of Object.keys(data.groups)){
 const option=document.createElement('option');option.value=name;option.textContent=name;category.append(option);
 const button=document.createElement('button');button.textContent=name;button.dataset.category=name;
 button.onclick=()=>chooseCategory(name);document.getElementById('categories').append(button);
}
category.onchange=()=>chooseCategory(category.value);
clip.onchange=()=>{stop();frame=0;draw()};
play.onclick=()=>{if(timer)stop();else{play.textContent='Pause';advance()}};
document.getElementById('prev').onclick=()=>{stop();frame--;draw()};
document.getElementById('next').onclick=()=>{stop();frame++;draw()};
screen.onerror=()=>{stop();document.getElementById('counter').textContent='Capture unavailable. Choose another move.'};
chooseCategory('Intro');
