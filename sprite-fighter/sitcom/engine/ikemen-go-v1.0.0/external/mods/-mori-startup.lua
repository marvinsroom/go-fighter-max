local tick,shot,ready,pending=0,0,0,nil
local report={runtime_sha256={["1.act"]="4a10e2a4d6de9fc9d25a82e1d30f763e0c6724f6975ff2744729223a020213fd",["common1.cns"]="88f45a78e99c7f2aeab3cc0bbce76384fd8d766ece864422f87a95540be63107",["Jin Mori.cns"]="ed204ef1c66b8fa4065f7bc2b8248054d19157e25107bf9b9280abb4ebba5c60",["Jin Mori.snd"]="2b0e2f8009cee53a727cf40c560b311d32092e6e46bee2b543609ae1b6301d8d",["jin_mori.air"]="f38246d31ce2744917277e334a66c11cc335e4e8ea0c9ddde8b76ddeb3858e45",["jin_mori.cmd"]="e492b924711c7574b5c8924a7568b25107511e7d897fd5b39521a5641c995a05",["jin_mori.def"]="06d1f79910e76e68d612838cb9949933caaf52c9d8472c0b82d9b06ce1ff6d46",["jin_mori.sff"]="abb6e0f54f356d36a78b4855b6faccd0b3e5be5c05c76b33d3b9a8a14a55dc4d"},status='Running',intro_seen=false,greeting_seen=false,frames={}}
hook.add('loop','mori-real-entrance',function()
 if not player(1) then return end
 tick=tick+1
 if pending then
  local f=io.open('../../characters/jin-mori/replays/comic-20261021105435-startup/Mori_startup'..string.format('%03d',shot)..'.png','rb')
  if f then f:close();pending.file='Mori_startup'..string.format('%03d',shot)..'.png';table.insert(report.frames,pending);pending=nil;shot=shot+1 end
 end
 local state=stateNo()
 if roundState()<2 and (state==190 or state==191) then
  report.intro_seen=true
  if spriteVar('group')==62302 and spriteVar('image')==3 then report.greeting_seen=true end
  if tick%6==0 and not pending then
   pending={case_name='Natural round entrance',case_tick=tick,state=state,group=spriteVar('group'),drawing=spriteVar('image'),capture_directory='comic-20261021105435-startup'};screenshot()
  end
 end
 if roundState()==2 then ready=ready+1 end
 if ready>=20 or tick>900 then
  report.status='Complete';report.passed=report.intro_seen and report.greeting_seen and ready>=20
  os.remove('../../characters/jin-mori/startup-validation.json');jsonEncode(report,'../../characters/jin-mori/startup-validation.json');print('MORI_STARTUP '..tostring(report.passed));os.exit()
 end
end)
