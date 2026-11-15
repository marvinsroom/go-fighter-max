param([Parameter(Mandatory=$true)][string]$Character,[ValidatePattern('^v[0-9]+$')][string]$Revision='v1')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Set-Location -LiteralPath $workspace
$python=Join-Path $workspace 'tooling/mesh-client-venv/Scripts/python.exe'
$folder=Join-Path $workspace ('sprite-fighter/characters/'+$Character)
function Invoke-CheckedPython([string[]]$Arguments){& $python @Arguments;if($LASTEXITCODE -ne 0){throw "Python stage failed: $Arguments"}}
function Assert-Proof([int]$Count){
 $proof=Get-Content -LiteralPath (Join-Path $folder 'runtime-validation.json') -Raw | ConvertFrom-Json
 if($proof.status -ne 'Complete' -or $proof.failed -ne 0 -or $proof.passed -ne $Count){throw "Invalid gameplay proof for $Character : $($proof.passed) passed, $($proof.failed) failed"}
}
Invoke-CheckedPython -Arguments @('scripts/setup-manhwa-tests.py',$Character,('final-'+$Revision))
& (Join-Path $PSScriptRoot 'run-manhwa-fighter.ps1') -Character $Character -Mode Tests -Wait
Assert-Proof 66
$null=New-Item -ItemType Directory -Path (Join-Path $folder 'validation') -Force
Copy-Item -LiteralPath (Join-Path $folder 'runtime-validation.json') -Destination (Join-Path $folder ('validation/final-'+$Revision+'.json'))
Invoke-CheckedPython -Arguments @('scripts/setup-manhwa-tests.py',$Character,('presentation-'+$Revision),'--presentation')
& (Join-Path $PSScriptRoot 'run-manhwa-fighter.ps1') -Character $Character -Mode Tests -Wait -RealTime
Assert-Proof 22
Invoke-CheckedPython -Arguments @('scripts/merge-manhwa-presentation.py',$Character,('final-'+$Revision+'.json'),('presentation-'+$Revision+'.json'))
Invoke-CheckedPython -Arguments @('scripts/setup-manhwa-startup.py',$Character,('startup-'+$Revision))
& (Join-Path $PSScriptRoot 'run-manhwa-fighter.ps1') -Character $Character -Mode Startup -Wait
Invoke-CheckedPython -Arguments @('scripts/manhwa-cinematic-contact.py',$Character)
Invoke-CheckedPython -Arguments @('scripts/package-manhwa.py',$Character)
Invoke-CheckedPython -Arguments @('scripts/verify-manhwa.py',$Character)
Write-Output "MANHWA_PIPELINE_COMPLETE $Character"
