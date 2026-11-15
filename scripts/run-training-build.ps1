$ErrorActionPreference = 'Stop'
$workspaceRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$projectRoot = Join-Path $workspaceRoot 'SitcomFighter'
if (Test-Path -LiteralPath (Join-Path $projectRoot 'Saved\training-build.json')) { throw 'Prototype already built; refusing to overwrite.' }
$draftFolder = [IO.Path]::GetFullPath((Join-Path $projectRoot 'Content\Prototype'))
$archiveFolder = [IO.Path]::GetFullPath((Join-Path $projectRoot ('Saved\FailedPrototypeDrafts\' + [Guid]::NewGuid().ToString('N'))))
if (-not $draftFolder.StartsWith($workspaceRoot + '\', [StringComparison]::OrdinalIgnoreCase) -or -not $archiveFolder.StartsWith($workspaceRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Draft/archive paths are outside workspace.' }
if (Test-Path -LiteralPath $draftFolder) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $archiveFolder) -Force | Out-Null
    Move-Item -LiteralPath $draftFolder -Destination $archiveFolder
}
& 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' (Join-Path $projectRoot 'SitcomFighter.uproject') -run=pythonscript "-script=$PSScriptRoot\build-training-prototype.py" -unattended -nullrhi -nosplash "-abslog=$workspaceRoot\training-build.log" *> (Join-Path $workspaceRoot 'training-build-console.log')
$buildExitCode = $LASTEXITCODE
Get-Content -LiteralPath (Join-Path $workspaceRoot 'training-build.log') | Select-String 'TRAINING_|LogPython: Error:|LogBlueprint: Error:|LogInit: Display: Success|Critical error' | Select-Object -Last 20
exit $buildExitCode
