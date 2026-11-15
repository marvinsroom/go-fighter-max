$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/ichigo'
foreach($group in @('basics','skills','power')){
 & $python (Join-Path $PSScriptRoot 'setup-ichigo-tests.py') "gallery-$group-v4" "--gallery-$group"
 if($LASTEXITCODE -ne 0){throw "Cannot prepare $group gallery"}
 & (Join-Path $PSScriptRoot 'run-ichigo-fighter.ps1') -Mode Tests -TestSpeed 4 -Wait
 $report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
 if($report.status -ne 'Complete' -or $report.failed -ne 0){throw "$group gallery did not pass"}
 Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character "$group-validation.json")
 Copy-Item -LiteralPath (Join-Path $workspace 'sprite-fighter/ichigo-play-stdout.log') -Destination (Join-Path $character "$group-stdout.log")
 Write-Output "GALLERY_COMPLETE $group $($report.passed) checks"
}
& (Join-Path $PSScriptRoot 'record-ichigo-intro.ps1')
