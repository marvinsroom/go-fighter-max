param([ValidateSet('naruto','saitama')][string]$Character='naruto',[ValidateSet('Play','CPU')][string]$Mode='Play')
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine=Join-Path $workspace 'sprite-fighter/engine/ikemen-go-v1.0.0'
$opponentAI=if($Mode -eq 'CPU'){'4'}else{'0'}
$arguments=@('-config','save/config.ini','-loadmotif','-p1',$Character,'-p2','will_full','-p1.ai','0','-p2.ai',$opponentAI,'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
$game=Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $arguments -WindowStyle Normal -PassThru
Write-Output "$Character original MUGEN $Mode process: $($game.Id)"
