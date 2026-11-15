const data=window.FIGHTER_REVIEW,category=document.getElementById('category'),clip=document.getElementById('clip');
const capture=document.getElementById('capture'),detail=document.getElementById('detail'),play=document.getElementById('play'),ultimateNav=document.getElementById('ultimates');
let index=0,timer=null,playing=true;
function frames(){return data.cases[clip.value]||[]}
function updateShortcuts(){for(const button of ultimateNav.children)button.setAttribute('aria-pressed',String(button.dataset.clip===clip.value))}
function show(delta=0){clearTimeout(timer);const rows=frames();updateShortcuts();if(!rows.length){capture.removeAttribute('src');detail.textContent='No captures available for this selection.';return}index=(index+delta+rows.length)%rows.length;const frame=rows[index];capture.dataset.loaded='pending';capture.src=frame.src+'?v='+data.revision;detail.textContent=`${clip.value} · Frame ${index+1} of ${rows.length} · Tick ${frame.case_tick}`}
function schedule(){clearTimeout(timer);if(!playing||!frames().length||capture.dataset.loaded!=='true')return;const rows=frames(),a=rows[index],b=rows[(index+1)%rows.length];const ms=b.case_tick>a.case_tick?(b.case_tick-a.case_tick)*1000/60:600;timer=setTimeout(()=>show(1),Math.max(16,ms/Number(document.getElementById('speed').value)))}
function chooseCategory(){clip.replaceChildren();for(const name of data.groups[category.value]||[]){const option=document.createElement('option');option.value=name;option.textContent=name;clip.append(option)}index=0;show()}
capture.onload=()=>{capture.dataset.loaded='true';schedule()};
capture.onerror=()=>{clearTimeout(timer);playing=false;play.textContent='Play';capture.dataset.loaded='false';detail.textContent=`Capture unavailable: ${frames()[index]?.src||'No frame selected'}. Reload after restoring the capture files.`};
category.onchange=chooseCategory;clip.onchange=()=>{index=0;show()};
play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play';schedule()};
document.getElementById('previous').onclick=()=>show(-1);document.getElementById('next').onclick=()=>show(1);document.getElementById('speed').onchange=schedule;
for(const name of Object.keys(data.groups)){const option=document.createElement('option');option.value=name;option.textContent=name;category.append(option)}
for(const shortcut of data.shortcuts){const button=document.createElement('button');button.type='button';button.textContent=shortcut.clip.replace(/ hit$| confirmed$/,'');button.dataset.clip=shortcut.clip;button.onclick=()=>{category.value=shortcut.category;chooseCategory();clip.value=shortcut.clip;index=0;show()};ultimateNav.append(button)}
document.getElementById('status').textContent=data.status;
category.value=data.groups.Ultimates?'Ultimates':Object.keys(data.groups)[0];chooseCategory();
const sheets=document.getElementById('sheets');
if(sheets)for(const sheet of data.sheets){const button=document.createElement('button');button.type='button';button.textContent=sheet.name;button.onclick=()=>{const atlas=document.getElementById('atlas');atlas.src=sheet.src;atlas.alt=data.name+' '+sheet.name+' animation sheet';for(const child of sheets.children)child.setAttribute('aria-pressed',String(child===button))};sheets.append(button)}
