param([int[]]$PreviewProcessIds=@(),[ValidatePattern('^[a-z0-9-]+$')][string]$RunLabel='cinematics-v5')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$exe=Join-Path $engine 'Ikemen_GO.exe'
foreach($previewId in $PreviewProcessIds){
 $preview=Get-Process -Id $previewId -ErrorAction SilentlyContinue
 if($preview -and $preview.Path -eq $exe){Wait-Process -Id $previewId -ErrorAction SilentlyContinue}
}
$games=@()
foreach($slug in @('prince','tyrone')){
 $arguments=@('-speedtest','4','-config',"save/$slug-paired-tests.ini",'-loadmotif','-p1','will_full/will_test.def','-p2',"$slug/${slug}_paired_test.def",'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
 $games+=Start-Process -WindowStyle Hidden -FilePath $exe -WorkingDirectory $engine -ArgumentList $arguments -PassThru -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/$slug-$RunLabel-tests-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/$slug-$RunLabel-tests-stderr.log")
 Write-Output "Started $slug cinematic regression checks"
}
foreach($game in $games){Wait-Process -Id $game.Id -ErrorAction SilentlyContinue}
$arguments=@('-speedtest','4','-config','save/chappelle-paired-match-tests.ini','-loadmotif','-p1','prince/prince_paired_test.def','-p2','tyrone/tyrone_paired_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
$game=Start-Process -WindowStyle Hidden -FilePath $exe -WorkingDirectory $engine -ArgumentList $arguments -PassThru -RedirectStandardOutput (Join-Path $workspace "sprite-fighter/chappelle-$RunLabel-match-stdout.log") -RedirectStandardError (Join-Path $workspace "sprite-fighter/chappelle-$RunLabel-match-stderr.log")
Write-Output 'Started both-side paired matchup checks'
Wait-Process -Id $game.Id -ErrorAction SilentlyContinue
Write-Output 'CHAPPELLE_CINEMATIC_NATIVE_RUNS_FINISHED'
