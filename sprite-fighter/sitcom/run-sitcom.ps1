param(
    [ValidateSet('will_full','prince','tyrone','urkel','yamal')][string]$Character='will_full',
    [ValidateSet('will_full','prince','tyrone','urkel','yamal')][string]$Opponent='prince',
    [switch]$CPU
)
$ErrorActionPreference='Stop'
$engine=Join-Path $PSScriptRoot 'engine/ikemen-go-v1.0.0'
$argsList=@('-config','save/config.ini','-loadmotif','-p1',$Character,'-p2',$Opponent,'-p1.ai','0','-p2.ai',$(if($CPU){'4'}else{'0'}),'-p1.power','3000','-p2.power','3000','-s','stages/stage0-720.def','-time','-1')
Start-Process -FilePath (Join-Path $engine 'Ikemen_GO.exe') -WorkingDirectory $engine -ArgumentList $argsList -WindowStyle Normal | Out-Null
