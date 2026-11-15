$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $taskRoot 'sprite-fighter/engine/ikemen-go-v1.0.0'
$logRoot=Join-Path $taskRoot 'sprite-fighter/proportions-v9/startup'
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
$errFile=Join-Path $logRoot 'lloyd-mori-stderr.log'
$argsList=@('-config','save/config.ini','-loadmotif','-p1','lloyd','-p2','jin_mori','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logRoot 'lloyd-mori-stdout.log') -RedirectStandardError $errFile -PassThru
$null=$game.Handle;$finished=$game.WaitForExit(15000)
if(!$finished){Stop-Process -Id $game.Id -Force -ErrorAction SilentlyContinue}
$errors=Get-Content -LiteralPath $errFile -Raw
if($errors -match '(?im)Panic:|failed to preload|Unknown color depth|stack traceback:'){throw "Lloyd/Mori: $errors"}
if($finished -and $game.ExitCode -ne 0){throw "Lloyd/Mori: exit $($game.ExitCode)"}
@{status='PASS';fighters=@('lloyd','jin_mori');production_config='save/config.ini';recordings='Deferred; no recording modules used';duration_seconds=15} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $logRoot 'validation.json') -Encoding UTF8
Write-Output 'Lloyd/Mori production startup passed; no recording modules.'
