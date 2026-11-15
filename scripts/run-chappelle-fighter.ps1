param([ValidateSet('prince','tyrone')][string]$Character='prince',
 [ValidateSet('Play','CPU','Tests')][string]$Mode='Play',[switch]$AsPlayerOne,
 [ValidateSet('will_full','prince','tyrone')][string]$Opponent='will_full')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/sitcom/engine/ikemen-go-v1.0.0'
if($Mode -eq 'Tests'){
 $arguments=@('-speedtest','4','-config',"save/$Character-paired-tests.ini",'-loadmotif','-p1','will_full/will_test.def','-p2',"$Character/${Character}_paired_test.def",'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
}else{
 $first=if($AsPlayerOne){$Character}else{'will_full'}
 $second=if($AsPlayerOne){$Opponent}else{$Character}
 $opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
 $arguments=@('-config','save/config.ini','-loadmotif','-p1',$first,'-p2',$second,'-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
}
$options=@{}
if($Mode -eq 'Tests'){$options.WindowStyle='Hidden'}
$prefix="$Character-$($Mode.ToLower())"
$game=Start-Process @options -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$prefix-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$prefix-stderr.log") -PassThru
Set-Content -LiteralPath (Join-Path $workspace "sprite-fighter/$Character-process.txt") -Value $game.Id
Write-Output "$Character $Mode process: $($game.Id)"
