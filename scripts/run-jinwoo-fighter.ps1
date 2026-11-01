param([ValidateSet('Play','CPU','Tests','Intro','Preview','Proportions')][string]$Mode='Play')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$engineExe=Join-Path $engine 'Ikemen_GO.exe'
Get-Process -Name Ikemen_GO -ErrorAction SilentlyContinue | Where-Object {$_.Path -eq $engineExe} | ForEach-Object {
 $null=$_.CloseMainWindow()
 if(-not $_.WaitForExit(2500)){Stop-Process -InputObject $_}
}
if($Mode -in @('Tests','Intro','Preview','Proportions')){
 $testConfig=switch($Mode){'Intro'{'save/jinwoo-intro-test.ini'} 'Preview'{'save/jinwoo-focus-tests.ini'} 'Proportions'{'save/jinwoo-proportions.ini'} default{'save/jinwoo-current-tests.ini'}}
 # Every mode must exercise the same canonical runtime used by the roster.
 $fighter=if($Mode -eq 'Tests'){'jinwoo/jinwoo_test.def'}else{'jinwoo/jinwoo.def'}
 $arguments=@('-config',$testConfig,'-loadmotif','-p1',$fighter,'-p2','will_full/will_sword_test.def','-p1.ai','0','-p2.ai','0','-s','stages/stage0-720.def','-time','-1')
}else{
 $opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
 # config.ini keeps the proven Xbox + d-pad-bridge keyboard map
 # (Jinwoo Controls.txt / controller-review). Charge = LB (/d) or Start.
 $arguments=@('-config','save/config.ini','-loadmotif','-p1','jinwoo','-p2','naruto','-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
}
$options=@{FilePath=$engineExe;WorkingDirectory=$engine;ArgumentList=$arguments;PassThru=$true}
if($Mode -in @('Tests','Intro','Preview','Proportions')){
 $options.WindowStyle='Hidden'
 $options.RedirectStandardOutput=Join-Path $workspace 'sprite-fighter/jinwoo-play-stdout.log'
 $options.RedirectStandardError=Join-Path $workspace 'sprite-fighter/jinwoo-play-stderr.log'
}
$game=Start-Process @options
if($Mode -in @('Play','CPU')){
 $bridge=Join-Path $PSScriptRoot 'jinwoo-dpad-bridge.ps1'
 Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',$bridge,'-GameProcessId',$game.Id) -WindowStyle Hidden
}
Write-Output "$Mode process: $($game.Id)"
