$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $taskRoot 'sprite-fighter/engine/ikemen-go-v1.0.0'
$logRoot=Join-Path $taskRoot '.tmp/size-redesign/startup'
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
foreach($pair in @(@{Name='cid-luffy';First='cid_shadow';Second='luffy'},@{Name='goku-gt';First='goku';Second='gt_goku'})){
    $errFile=Join-Path $logRoot ($pair.Name+'-stderr.log')
    $argsList=@('-config','save/config.ini','-loadmotif','-p1',$pair.First,'-p2',$pair.Second,'-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
    $game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logRoot ($pair.Name+'-stdout.log')) -RedirectStandardError $errFile -PassThru
    $null=$game.Handle;$finished=$game.WaitForExit(15000)
    if(!$finished){Stop-Process -Id $game.Id -Force -ErrorAction SilentlyContinue}
    $errors=Get-Content -LiteralPath $errFile -Raw
    if($errors -match '(?im)Panic:|failed to preload|Unknown color depth|stack traceback:'){throw "$($pair.Name): $errors"}
    if($finished -and $game.ExitCode -ne 0){throw "$($pair.Name): exit $($game.ExitCode)"}
    Write-Output "$($pair.Name): startup passed; no recording modules."
}
