$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$checks=@(
    @{Name='manga';Engine='sprite-fighter/engine/ikemen-go-v1.0.0';First='zhuo_fan';Second='naruto'},
    @{Name='sitcom';Engine='sprite-fighter/sitcom/engine/ikemen-go-v1.0.0';First='will_full';Second='prince'}
)
$logRoot=Join-Path $taskRoot '.tmp/roster-split-startup'
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
foreach($check in $checks){
    $engine=Join-Path $taskRoot $check.Engine
    $errFile=Join-Path $logRoot ($check.Name+'-stderr.log')
    $outFile=Join-Path $logRoot ($check.Name+'-stdout.log')
    $argsList=@('-config','save/config.ini','-loadmotif','-p1',$check.First,'-p2',$check.Second,'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
    $game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle Hidden -RedirectStandardOutput $outFile -RedirectStandardError $errFile -PassThru
    $null=$game.Handle
    $finished=$game.WaitForExit(20000)
    if(!$finished){Stop-Process -Id $game.Id -Force -ErrorAction SilentlyContinue}
    $errors=Get-Content -LiteralPath $errFile -Raw
    if($errors -match '(?im)Panic:|failed to preload|Unknown color depth|cannot find|stack traceback:'){throw "$($check.Name) startup failed: $errors"}
    if($finished -and $game.ExitCode -ne 0){throw "$($check.Name) exited with $($game.ExitCode)"}
    Write-Output "$($check.Name): startup passed, no capture modules or recordings."
}
