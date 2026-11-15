param([ValidateSet('Play','CPU','Tests')][string]$Mode='Play',[switch]$Wait,[ValidateRange(0.25,8)][double]$TestSpeed=4)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$arguments=@('-config','save/config.ini','-loadmotif','-p1','vikir','-p2','naruto','-p1.ai','0','-p2.ai',$(if($Mode -eq 'CPU'){'4'}else{'0'}),'-p1.power','3000','-s','stages/stage0-720.def','-time','-1')
$options=@{}
if($Mode -eq 'Tests'){$arguments=@('-speedtest',"$TestSpeed",'-config','save/vikir-tests.ini','-loadmotif','-p1','vikir/vikir_test.def','-p2','will_full/will_vikir_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1');$options.WindowStyle='Hidden'}
$logPrefix=if($Mode -eq 'Tests'){'vikir-tests'}else{'vikir'}
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$logPrefix-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$logPrefix-stderr.log") -PassThru @options
Write-Output "$Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Vikir exited with code $($game.ExitCode)"}}
