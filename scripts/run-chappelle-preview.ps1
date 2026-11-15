param([ValidateSet('prince','negan','rick')][string]$Character='prince')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/sitcom/engine/ikemen-go-v1.0.0'
$argsList=@('-config',"save/$Character-native-preview.ini",'-loadmotif','-p1','will_full/will_test.def','-p2',"$Character/${Character}_test.def",'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle Hidden -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$Character-preview-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$Character-preview-stderr.log") -PassThru
Write-Output "$Character preview process: $($game.Id)"
