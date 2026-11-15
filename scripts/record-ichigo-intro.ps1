$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
& $python (Join-Path $PSScriptRoot 'setup-ichigo-tests.py') 'intro-school-v4' '--intro'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare school intro capture'}
& (Join-Path $PSScriptRoot 'run-ichigo-fighter.ps1') -Mode Tests -RealTime -Wait
& $python (Join-Path $PSScriptRoot 'package-ichigo-intro.py')
if($LASTEXITCODE -ne 0){throw 'School intro capture verification failed'}
