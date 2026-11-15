$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$engine = Join-Path $workspace 'sprite-fighter\engine\ikemen-go-v1.0.0'
$engineExe = Join-Path $engine 'Ikemen_GO.exe'
$character = Join-Path $engine 'chars\jinwoo\cmd.cmd'
$config = Join-Path $engine 'save\config.ini'
$inputLog = Join-Path $workspace 'sprite-fighter\jinwoo-input-debug.log'

Get-Process -Name Ikemen_GO -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.Path -eq $engineExe) { Stop-Process -InputObject $_ -Force }
}
Remove-Item -LiteralPath $inputLog -Force -ErrorAction SilentlyContinue

Write-Host '=== JINWOO LIVE DEBUG ===' -ForegroundColor Cyan
Write-Host "Engine:    $engineExe"
Write-Host "Character: $character"
Write-Host "Config:    $config"
Write-Host "CMD saved: $((Get-Item -LiteralPath $character).LastWriteTime)"
Write-Host 'Controller: A=light B=medium X=grab Y=heavy LB=charge RB=ultimate LT=summon RT=super'
Write-Host 'D-pad: Up=Igris Right=Beru Left=Iron Down=Tank'
Write-Host "Input log: $inputLog"

$arguments = @(
    '-config', 'save/config.ini', '-loadmotif',
    '-p1', 'jinwoo', '-p2', 'naruto',
    '-p1.ai', '0', '-p2.ai', '0',
    '-p1.power', '3000', '-p2.power', '3000',
    '-s', 'stages/stage0-720.def', '-time', '-1'
)
$game = Start-Process -FilePath $engineExe -WorkingDirectory $engine -ArgumentList $arguments -PassThru
$bridge = Join-Path $PSScriptRoot 'jinwoo-dpad-bridge.ps1'
$bridgeProcess = Start-Process -FilePath 'powershell.exe' -ArgumentList @(
    '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $bridge,
    '-GameProcessId', $game.Id, '-LogPath', $inputLog
) -WindowStyle Hidden -PassThru

Write-Host "Game PID: $($game.Id); D-pad bridge PID: $($bridgeProcess.Id)" -ForegroundColor Green
Write-Host 'Leave this task running while testing. Close the game to end it.'
Wait-Process -Id $game.Id
if (-not $bridgeProcess.HasExited) { Stop-Process -InputObject $bridgeProcess -Force }
Write-Host 'Jinwoo game closed.' -ForegroundColor Yellow
