$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/luffy'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
& $python (Join-Path $PSScriptRoot 'setup-luffy-tests.py') "gameplay-$stamp" '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare full gameplay checks'}
& (Join-Path $PSScriptRoot 'run-luffy-fighter.ps1') -Mode Tests -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Gameplay checks did not pass'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'gameplay-validation.json')
Write-Output "GAMEPLAY_COMPLETE $($report.passed) checks"
& (Join-Path $PSScriptRoot 'record-luffy-gallery.ps1')
& $python (Join-Path $PSScriptRoot 'package-luffy.py')
if($LASTEXITCODE -ne 0){throw 'Cannot package Luffy review'}
& $python (Join-Path $PSScriptRoot 'verify-luffy.py')
if($LASTEXITCODE -ne 0){throw 'Luffy verification failed'}
