param([ValidateSet('prince','tyrone')][string]$Character='prince',[string]$CaptureName='signatures-v3-final')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/sitcom/engine/ikemen-go-v1.0.0'
if($CaptureName -notmatch '^[a-z0-9-]+$'){throw 'Invalid capture folder'}
$frames=Join-Path $workspace "sprite-fighter/characters/$Character/replays/$CaptureName"
if(Get-ChildItem -LiteralPath $frames -Filter '*.png' -ErrorAction SilentlyContinue){throw 'Capture folder already contains frames; preserve this take and use a fresh folder for a new take.'}
$arguments=@('-speedtest','2','-config',"save/$Character-signature-preview.ini",'-loadmotif',
 '-p1','will_full/will_test.def','-p2',"$Character/${Character}_paired_test.def",'-p1.ai','0','-p2.ai','0',
 '-s','stages/stage0-720.def','-time','-1')
$game=Start-Process -WindowStyle Hidden -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -PassThru `
 -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$Character-signature-preview-stdout.log") `
 -RedirectStandardError (Join-Path $workspace "sprite-fighter/$Character-signature-preview-stderr.log")
Write-Output "$Character signature preview process: $($game.Id)"
