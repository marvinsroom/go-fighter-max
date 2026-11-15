param([ValidateSet('Play','CPU','Compare','Tests')][string]$Mode='Play',[switch]$Wait,[switch]$RealTime)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
Get-Process -Name Ikemen_GO -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $engineExe} | ForEach-Object {
 $null=$_.CloseMainWindow()
 if(-not $_.WaitForExit(2500)){Stop-Process -InputObject $_}
}
$opponent=if($Mode -eq 'Compare'){'cid_shadow/cid_original.def'}else{'will_full'}
$opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
$arguments=@('-config','save/config.ini','-loadmotif','-p1','cid_shadow','-p2',$opponent,'-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
$options=@{}
if($Mode -eq 'Tests'){
 $arguments=@('-config','save/cid-reference-tests.ini','-loadmotif','-p1','cid_shadow/cid_test.def','-p2','will_full/will_hybrid_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 if(-not $RealTime){$arguments=@('-speedtest','4')+$arguments}
 $options.WindowStyle='Hidden'
}
$game=Start-Process -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace 'sprite-fighter/cid-play-stdout.log') -RedirectStandardError (Join-Path $workspace 'sprite-fighter/cid-play-stderr.log') -PassThru @options
Write-Output "$Mode process: $($game.Id)"
if($Wait){$null=$game.Handle;$game.WaitForExit();if($null -ne $game.ExitCode -and $game.ExitCode -ne 0){throw "Cid process exited with code $($game.ExitCode)"}}
