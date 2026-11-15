param([ValidateSet('Play','CPU','Tests')][string]$Mode='Play',[switch]$AsYamal)
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
if($Mode -eq 'Tests'){
 $arguments=@('-speedtest','4','-config','save/yamal-combat-tests.ini','-loadmotif','-p1','will_full/will_test.def','-p2','yamal/yamal_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 $logPrefix='yamal-tests'
}else{
 $opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
 $firstFighter=if($AsYamal){'yamal'}else{'will_full'}
 $secondFighter=if($AsYamal){'will_full'}else{'yamal'}
 $arguments=@('-loadmotif','-p1',$firstFighter,'-p2',$secondFighter,'-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
 $logPrefix='will-vs-yamal'
}
$launchOptions=@{}
if($Mode -eq 'Tests'){$launchOptions.WindowStyle='Hidden'}
$game=Start-Process @launchOptions -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$logPrefix-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$logPrefix-stderr.log") -PassThru
Set-Content -LiteralPath (Join-Path $workspace "sprite-fighter/yamal-process.txt") -Value $game.Id
Write-Output "$Mode process: $($game.Id)"
