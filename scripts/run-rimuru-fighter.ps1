param([ValidateSet('Play','CPU','Tests')][string]$Mode='Play',[switch]$Wait,[switch]$RealTime)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$arguments=@('-config','save/config.ini','-loadmotif','-p1','rimuru','-p2','naruto','-p1.ai','0','-p2.ai',$(if($Mode -eq 'CPU'){'4'}else{'0'}),'-p1.power','3000','-s','stages/stage0-720.def','-time','-1')
$options=@{}
if($Mode -eq 'Tests'){
 $arguments=@('-speedtest','4','-config','save/rimuru-tests.ini','-loadmotif','-p1','rimuru/rimuru_test.def','-p2','will_full/will_rimuru_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 if($RealTime){$arguments=$arguments[2..($arguments.Count-1)]}
 $options.WindowStyle='Hidden'
}
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace 'sprite-fighter/rimuru-stdout.log') -RedirectStandardError (Join-Path $workspace 'sprite-fighter/rimuru-stderr.log') -PassThru @options
Write-Output "$Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Rimuru exited with code $($game.ExitCode)"}}
