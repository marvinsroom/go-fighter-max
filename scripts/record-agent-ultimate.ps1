$ErrorActionPreference='Stop'
# Focus and validate the owned game window using the existing capture helper.
. "$PSScriptRoot/inspect-ikemen-window.ps1"
$captureDirectory=Join-Path $PSScriptRoot '../sprite-fighter/characters/will/ultimate-replay-v2'
New-Item -ItemType Directory -Path $captureDirectory -Force | Out-Null
function Press-GameKey([byte]$code) {
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost'}
 $scan=[byte][IkemenWindow]::MapVirtualKey($code,0)
 [IkemenWindow]::keybd_event($code,$scan,0,[UIntPtr]::Zero)
 try {Start-Sleep -Milliseconds 70}
 finally {[IkemenWindow]::keybd_event($code,$scan,2,[UIntPtr]::Zero)}
}
Press-GameKey 114
Start-Sleep -Milliseconds 300
$rect=New-Object IkemenWindow+RECT
[IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
$bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
$samples=@()
try {
 Press-GameKey 68
 $timer=[Diagnostics.Stopwatch]::StartNew()
 for($i=0;$i -lt 45;$i++) {
  if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost; capture stopped'}
  $milliseconds=$timer.ElapsedMilliseconds
  $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
  $name='frame-{0:D3}.png' -f $i
  $bitmap.Save((Join-Path $captureDirectory $name),[System.Drawing.Imaging.ImageFormat]::Png)
  $samples+=@{file=$name;milliseconds=$milliseconds}
  Start-Sleep -Milliseconds 65
 }
} finally {$graphics.Dispose();$bitmap.Dispose()}
$samples | ConvertTo-Json | Set-Content (Join-Path $captureDirectory 'timing.json')
Press-GameKey 114
Write-Output "Captured ultimate replay: $captureDirectory"
