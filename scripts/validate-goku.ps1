$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/goku'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
& $python (Join-Path $PSScriptRoot 'setup-goku-tests.py') "trajectory-$stamp" '--alignment-probe' '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare trajectory checks'}
& (Join-Path $PSScriptRoot 'run-goku-fighter.ps1') -Mode Tests -Wait
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character "replays/trajectory-$stamp/validation.json")
& $python (Join-Path $PSScriptRoot 'verify-goku-alignment.py') 'goku' "trajectory-$stamp"
if($LASTEXITCODE -ne 0){throw 'Trajectory alignment did not pass'}
& $python (Join-Path $PSScriptRoot 'setup-goku-tests.py') "gameplay-$stamp" '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare full gameplay checks'}
& (Join-Path $PSScriptRoot 'run-goku-fighter.ps1') -Mode Tests -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Gameplay checks did not pass'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'gameplay-validation.json')
Write-Output "GAMEPLAY_COMPLETE $($report.passed) checks"
& $python (Join-Path $PSScriptRoot 'setup-goku-tests.py') "contact-$stamp" '--contact' '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare contact checks'}
& (Join-Path $PSScriptRoot 'run-goku-fighter.ps1') -Mode Tests -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Contact checks did not pass'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'contact-validation.json')
& (Join-Path $PSScriptRoot 'record-goku-gallery.ps1')
& $python (Join-Path $PSScriptRoot 'package-goku.py')
if($LASTEXITCODE -ne 0){throw 'Cannot package Goku review'}
& $python (Join-Path $PSScriptRoot 'verify-goku.py')
if($LASTEXITCODE -ne 0){throw 'Goku verification failed'}
