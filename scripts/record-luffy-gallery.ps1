$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/luffy'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
foreach($group in @('basics','skills','power','intro')){
 $flag=if($group -eq 'intro'){'--intro'}else{"--gallery-$group"}
 & $python (Join-Path $PSScriptRoot 'setup-luffy-tests.py') "gallery-$group-$stamp" $flag
 if($LASTEXITCODE -ne 0){throw "Cannot prepare $group gallery"}
 if($group -eq 'intro'){& (Join-Path $PSScriptRoot 'run-luffy-fighter.ps1') -Mode Tests -RealTime -Wait}
 else{& (Join-Path $PSScriptRoot 'run-luffy-fighter.ps1') -Mode Tests -TestSpeed 4 -Wait}
 $report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw | ConvertFrom-Json
 if($report.status -ne 'Complete' -or $report.failed -ne 0){throw "$group gallery did not pass"}
 Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character "$group-validation.json")
 Copy-Item -LiteralPath (Join-Path $workspace 'sprite-fighter/luffy-play-stdout.log') -Destination (Join-Path $character "$group-stdout.log")
 Write-Output "GALLERY_COMPLETE $group $($report.passed) checks"
}
