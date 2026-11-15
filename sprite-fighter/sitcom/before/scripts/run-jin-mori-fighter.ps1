param([ValidateSet('Play','CPU','Compare','Tests')][string]$Mode='Play',[switch]$Wait,[switch]$RealTime)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$opponent=if($Mode -eq 'Compare'){'jin_mori_reference'}else{'will_full'}
$opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
$arguments=@('-config','save/config.ini','-loadmotif','-p1','jin_mori','-p2',$opponent,'-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
if($Mode -eq 'CPU'){$arguments=@('-config','save/config.ini','-loadmotif','-p1','will_full','-p2','jin_mori','-p1.ai','0','-p2.ai','4','-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')}
if($Mode -eq 'Tests'){
 $arguments=@('-config','save/mori-tests.ini','-loadmotif','-p1','jin_mori/mori_test.def','-p2','will_full/will_mori_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 if(-not $RealTime){$arguments=@('-speedtest','4')+$arguments}
}
$launchStyle=if($Mode -eq 'Tests'){'Hidden'}else{'Normal'}
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -WindowStyle $launchStyle -RedirectStandardOutput (Join-Path $workspace 'sprite-fighter/mori-stdout.log') -RedirectStandardError (Join-Path $workspace 'sprite-fighter/mori-stderr.log') -PassThru
Write-Output "$Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Jin Mori process exited with code $($game.ExitCode)"}}
