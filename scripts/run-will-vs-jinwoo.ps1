param([ValidateSet('Play','CPU','Tests')][string]$Mode='Play')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/sitcom/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
Get-Process -Name Ikemen_GO -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $engineExe} | ForEach-Object {
 $null=$_.CloseMainWindow()
 if(-not $_.WaitForExit(2500)){Stop-Process -InputObject $_}
}
if($Mode -eq 'Tests'){
 $arguments=@('-config','save/jinwoo-current-tests.ini','-loadmotif','-p1','jinwoo/jinwoo_test.def','-p2','will_full/will_sword_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 $logPrefix='jinwoo-tests'
}else{
 $opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
 $arguments=@('-loadmotif','-p1','will_full','-p2','jinwoo','-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
 $logPrefix='will-vs-jinwoo'
}
$game=Start-Process -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$logPrefix-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$logPrefix-stderr.log") -PassThru
Write-Output "$Mode process: $($game.Id)"
