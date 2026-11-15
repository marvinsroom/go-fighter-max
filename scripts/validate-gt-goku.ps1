$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/gt-goku'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
& $python (Join-Path $PSScriptRoot 'setup-gt-goku-tests.py') "trajectory-$stamp" '--alignment-probe' '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare trajectory checks'}
& (Join-Path $PSScriptRoot 'run-gt-goku-fighter.ps1') -Mode Tests -Wait
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character "replays/trajectory-$stamp/validation.json")
& $python (Join-Path $PSScriptRoot 'verify-goku-alignment.py') 'gt-goku' "trajectory-$stamp"
if($LASTEXITCODE -ne 0){throw 'Trajectory alignment did not pass'}
& $python (Join-Path $PSScriptRoot 'setup-gt-goku-tests.py') "gameplay-$stamp" '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare GT gameplay checks'}
& (Join-Path $PSScriptRoot 'run-gt-goku-fighter.ps1') -Mode Tests -TestSpeed 20 -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'GT gameplay checks did not pass'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'gameplay-validation.json')
Write-Output "GT_GAMEPLAY_COMPLETE $($report.passed) checks"
& (Join-Path $PSScriptRoot 'record-gt-goku-gallery.ps1')
& $python (Join-Path $PSScriptRoot 'package-gt-goku.py')
if($LASTEXITCODE -ne 0){throw 'Cannot package GT review'}
& $python (Join-Path $PSScriptRoot 'verify-gt-goku.py')
if($LASTEXITCODE -ne 0){throw 'GT verification failed'}
