param([ValidateSet('Play','CPU','Compare','Tests')][string]$Mode='Play',[switch]$Wait,[switch]$RealTime)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
$opponent=if($Mode -eq 'Compare'){'edward_reference'}else{'will_full'}
$opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
$arguments=@('-config','save/config.ini','-loadmotif','-p1','edward','-p2',$opponent,'-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
if($Mode -eq 'Tests'){
 $arguments=@('-config','save/edward-tests.ini','-loadmotif','-p1','edward/edward_test.def','-p2','will_full/will_edward_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 if(-not $RealTime){$arguments=@('-speedtest','4')+$arguments}
}
$options=@{}
if($Mode -eq 'Tests'){$options.WindowStyle='Hidden'}
$game=Start-Process -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace 'sprite-fighter/edward-play-stdout.log') -RedirectStandardError (Join-Path $workspace 'sprite-fighter/edward-play-stderr.log') -PassThru @options
Write-Output "$Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Edward process exited with code $($game.ExitCode)"}}
