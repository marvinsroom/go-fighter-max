$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$character=Join-Path $workspace 'sprite-fighter/characters/gt-goku'
$stamp=Get-Date -Format 'yyyyMMddHHmmss'
foreach($group in @('basics','skills','power','intro')){
 $flag=if($group -eq 'intro'){'--intro'}else{"--gallery-$group"}
 $batches=if($group -eq 'intro'){@(0)}else{@(0,2,4)}
 $checks=@();$frames=@();$cases=@();$passed=0
 foreach($first in $batches){
 $capture="gallery-$group-$stamp-$first"
 & $python (Join-Path $PSScriptRoot 'setup-gt-goku-tests.py') $capture $flag "--form-batch=$first"
 if($LASTEXITCODE -ne 0){throw "Cannot prepare $group gallery"}
 if($group -eq 'intro'){& (Join-Path $PSScriptRoot 'run-gt-goku-fighter.ps1') -Mode Tests -RealTime -Wait}
 elseif($group -eq 'basics'){& (Join-Path $PSScriptRoot 'run-gt-goku-fighter.ps1') -Mode Tests -TestSpeed 1 -Wait}
 else{& (Join-Path $PSScriptRoot 'run-gt-goku-fighter.ps1') -Mode Tests -TestSpeed 4 -Wait}
 $report=Get-Content -LiteralPath (Join-Path $character 'runtime-validation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
 if($report.status -ne 'Complete' -or $report.failed -ne 0){throw "$group gallery did not pass"}
 if(@($report.frames).Count -ge 999){throw "$group batch exhausted engine screenshot indices"}
 foreach($frame in $report.frames){$frame | Add-Member -NotePropertyName capture_directory -NotePropertyValue $capture}
 $checks+=@($report.checks);$frames+=@($report.frames);$passed+=$report.passed
 $batchCases=Get-Content -LiteralPath (Join-Path $character "replays/$capture/cases.json") -Raw -Encoding UTF8 | ConvertFrom-Json
 foreach($case in $batchCases){$cases+=$case}
 Copy-Item -LiteralPath (Join-Path $character 'runtime-validation.json') -Destination (Join-Path $character "replays/$capture/validation.json")
 Copy-Item -LiteralPath (Join-Path $workspace 'sprite-fighter/gt-goku-play-stdout.log') -Destination (Join-Path $character "replays/$capture/stdout.log")
 Write-Output "GALLERY_BATCH_COMPLETE $group $first $($report.passed) checks"
 }
 $combined=[ordered]@{status='Complete';failed=0;passed=$passed;checks=$checks;frames=$frames;cases=$cases;capture_directory=$capture;runtime_sha256=$report.runtime_sha256}
 [IO.File]::WriteAllText((Join-Path $character "$group-validation.json"),($combined | ConvertTo-Json -Depth 40),(New-Object Text.UTF8Encoding($false)))
 Write-Output "GALLERY_COMPLETE $group $passed checks"
}
