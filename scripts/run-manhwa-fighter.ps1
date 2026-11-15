param([ValidateSet('jin-mu-won','lloyd','gang-ryong','mok-gyeongwoon','arthur','cha-yeon-woo','kim-dokja','eugene','zhuo-fan')][string]$Character,[ValidateSet('Play','CPU','Tests','Startup')][string]$Mode='Play',[switch]$Wait,[switch]$RealTime)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$fighterId=$Character.Replace('-','_')
$argsList=@('-config','save/config.ini','-loadmotif','-p1',$fighterId,'-p2','naruto','-p1.ai','0','-p2.ai','0','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
if($Mode -eq 'CPU'){$argsList=@('-config','save/config.ini','-loadmotif','-p1','naruto','-p2',$fighterId,'-p1.ai','0','-p2.ai','4','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')}
if($Mode -eq 'Tests'){$argsList=@('-config',('save/'+$fighterId+'-tests.ini'),'-loadmotif','-p1',($fighterId+'/native-test.def'),'-p2',('will_full/'+$fighterId+'-test.def'),'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1');if(-not $RealTime){$argsList=@('-speedtest','4')+$argsList}}
if($Mode -eq 'Startup'){$argsList=@('-config',('save/'+$fighterId+'-startup.ini'),'-loadmotif','-p1',$fighterId,'-p2','naruto','-p1.ai','4','-p2.ai','0','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')}
$style=if($Mode -in @('Tests','Startup')){'Hidden'}else{'Normal'}
$logStem=$fighterId+$(if($Mode -eq 'Startup'){'-startup'}else{''})
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle $style -RedirectStandardOutput (Join-Path $workspace ('sprite-fighter/'+$logStem+'-stdout.log')) -RedirectStandardError (Join-Path $workspace ('sprite-fighter/'+$logStem+'-stderr.log')) -PassThru
Write-Output "$Character $Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Fighter process exited with code $($game.ExitCode)"}}
