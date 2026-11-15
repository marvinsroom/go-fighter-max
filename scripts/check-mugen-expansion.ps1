param([string[]]$Fighters=@())
$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if(!$Fighters.Count){$Fighters=@((Get-Content (Join-Path $taskRoot 'sprite-fighter/mugen-expansion/queue.json') -Raw | ConvertFrom-Json).fighters | Where-Object {$_.engine} | ForEach-Object {$_.slug})}
$Fighters=@($Fighters | ForEach-Object {$_ -split ','} | ForEach-Object {$_.Trim()} | Where-Object {$_})
& (Join-Path $taskRoot 'tooling/mesh-client-venv/Scripts/python.exe') (Join-Path $PSScriptRoot 'check-mugen-native.py') @Fighters
if($LASTEXITCODE -ne 0){throw 'Native import verification failed; see per-fighter validation reports.'}
