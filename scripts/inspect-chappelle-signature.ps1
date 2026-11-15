param()
$ErrorActionPreference='Stop'
. "$PSScriptRoot/inspect-ikemen-window.ps1"
$codes=@(65,67) # P1 skill + heavy, pressed together in the foreground game.
try {
 foreach($code in $codes){
  if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus changed; no further input'}
  [IkemenWindow]::keybd_event([byte]$code,[byte][IkemenWindow]::MapVirtualKey($code,0),0,[UIntPtr]::Zero)
 }
 Start-Sleep -Milliseconds 350
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus changed; no capture'}
 $rect=New-Object IkemenWindow+RECT
 [IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
 $bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
 $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
 try {
  $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
  $bitmap.Save([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../sprite-fighter/characters/chappelle/signature-keyboard-v3.png')),[System.Drawing.Imaging.ImageFormat]::Png)
 } finally {$graphics.Dispose();$bitmap.Dispose()}
} finally {
 foreach($code in $codes){[IkemenWindow]::keybd_event([byte]$code,[byte][IkemenWindow]::MapVirtualKey($code,0),2,[UIntPtr]::Zero)}
}
Write-Output 'Native A+C signature keyboard capture saved'
