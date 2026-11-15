$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/vikir'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
& $python (Join-Path $PSScriptRoot 'setup-vikir-tests.py') "gameplay-$stamp" '--no-capture'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare Vikir gameplay checks'}
& (Join-Path $PSScriptRoot 'run-vikir-fighter.ps1') -Mode Tests -TestSpeed 8 -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Vikir gameplay checks failed'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'gameplay-validation.json')
$reports=@('gameplay-validation.json')
foreach($bank in 0..2){
 & $python (Join-Path $PSScriptRoot 'setup-vikir-tests.py') "native-$stamp-$bank" '--gallery' "$bank"
 if($LASTEXITCODE -ne 0){throw 'Cannot prepare Vikir gallery'}
 & (Join-Path $PSScriptRoot 'run-vikir-fighter.ps1') -Mode Tests -Wait
 $report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
 if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Vikir native capture checks failed'}
 $name="native-validation-$bank.json"
 Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character $name)
 $reports+=$name
}
& $python (Join-Path $PSScriptRoot 'setup-vikir-tests.py') "power-$stamp" '--power-gallery'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare complete Vikir super captures'}
& (Join-Path $PSScriptRoot 'run-vikir-fighter.ps1') -Mode Tests -TestSpeed 0.5 -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Vikir super capture checks failed'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'power-validation.json')
$reports+='power-validation.json'
& $python (Join-Path $PSScriptRoot 'setup-vikir-tests.py') "guests-$stamp" '--guest-gallery'
if($LASTEXITCODE -ne 0){throw 'Cannot prepare Vikir guest and archery captures'}
& (Join-Path $PSScriptRoot 'run-vikir-fighter.ps1') -Mode Tests -TestSpeed 1 -Wait
$report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if($report.status -ne 'Complete' -or $report.failed -ne 0){throw 'Vikir guest capture checks failed'}
Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character 'guest-validation.json')
$reports+='guest-validation.json'
& $python (Join-Path $PSScriptRoot 'merge-vikir-validation.py') @reports
if($LASTEXITCODE -ne 0){throw 'Cannot aggregate Vikir native evidence'}
& $python (Join-Path $PSScriptRoot 'package-vikir.py')
if($LASTEXITCODE -ne 0){throw 'Cannot package Vikir review'}
& $python (Join-Path $PSScriptRoot 'verify-vikir.py')
if($LASTEXITCODE -ne 0){throw 'Vikir verification failed'}
& $python (Join-Path $PSScriptRoot 'check-vikir-review.py')
if($LASTEXITCODE -ne 0){throw 'Vikir browser review checks failed'}
