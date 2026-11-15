local report={status='Running',method='Unmodified production definition; natural entrance and AI combat',frames={},states_seen={},damage=0,combat_ticks=0}
local total,shot,pending=0,0,nil
local function save() jsonEncode(report,'../../characters/saitama/startup-validation.json') end
hook.add('loop','anime-import-startup',function()
 if not player(1) then return end
 total=total+1
 if total>5000 then report.status='Failed';report.error='No completed combat observation';save();os.exit(1) end
 if pending then
  local file=io.open('../../characters/saitama/replays/import-startup-20261022101018/Anime_import'..string.format('%03d',shot)..'.png','rb')
  if file then file:close();table.insert(report.frames,pending);shot=shot+1;pending=nil;save() end
 end
 report.states_seen[tostring(stateNo())]=true
 if roundState()==1 and total%50==0 and shot<3 and not pending then pending={label='Natural entrance',file='Anime_import'..string.format('%03d',shot)..'.png',state=stateNo(),animation=anim()};screenshot() end
 if roundState()>=2 then
  if roundState()==2 then report.combat_ticks=report.combat_ticks+1 end
  player(2);report.damage=math.max(report.damage,1000-life());player(1)
  if not pending and (report.combat_ticks%60==0 or report.damage>0) and shot<12 then pending={label='Natural AI combat',file='Anime_import'..string.format('%03d',shot)..'.png',state=stateNo(),animation=anim(),target_damage=report.damage,form=var(2)};screenshot() end
  if (report.damage>0 and report.combat_ticks>80 or report.combat_ticks>=1800 or roundState()>2) and not pending then
   report.passed=report.damage>0 and report.combat_ticks>0;report.status=report.passed and 'Complete' or 'Failed';save();os.exit(report.passed and 0 or 1)
  end
 end
end)
