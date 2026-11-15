param([ValidateSet('Tests','Play','CPU','Forms')][string]$Mode='Play')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/sitcom/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
Get-Process -Name Ikemen_GO -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $engineExe} | ForEach-Object {
 $null=$_.CloseMainWindow()
 if(-not $_.WaitForExit(2500)){Stop-Process -InputObject $_}
}
if($Mode -eq 'Tests'){
 $arguments=@('-config','save/will-combat-tests.ini','-loadmotif','-p1','will_full/will_test.def','-p2','will_full/will_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 $logPrefix='combat-tests'
}else{
 $opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
 $roundTime=if($Mode -eq 'Forms'){'-1'}else{'99'}
 $arguments=@('-loadmotif','-p1','will_full','-p2','will_full','-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time',$roundTime)
 $logPrefix='will-combat'
}
$game=Start-Process -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$logPrefix-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$logPrefix-stderr.log") -PassThru
Write-Output "$Mode process: $($game.Id)"
