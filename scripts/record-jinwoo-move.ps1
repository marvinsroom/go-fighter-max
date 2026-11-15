param([ValidateSet('Arise','Tempest')][string]$Move='Arise',
 [ValidatePattern('^[a-z0-9-]*$')][string]$CaptureName='')
$ErrorActionPreference='Stop'
. "$PSScriptRoot/inspect-ikemen-window.ps1"
$captureKey=if($CaptureName){$CaptureName}else{$Move.ToLower()+'-v3'}
$captureDirectory=Join-Path $PSScriptRoot ("../sprite-fighter/characters/jinwoo/replays/"+$captureKey)
New-Item -ItemType Directory -Path $captureDirectory -Force | Out-Null
function Press-GameKey([byte]$code) {
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost'}
 $scan=[byte][IkemenWindow]::MapVirtualKey($code,0)
 [IkemenWindow]::keybd_event($code,$scan,0,[UIntPtr]::Zero)
 try {Start-Sleep -Milliseconds 70}
 finally {[IkemenWindow]::keybd_event($code,$scan,2,[UIntPtr]::Zero)}
}
Press-GameKey 114
Start-Sleep -Milliseconds 250
$rect=New-Object IkemenWindow+RECT
[IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
$bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
$samples=@()
try {
 Press-GameKey $(if($Move -eq 'Tempest'){84}else{89})
 $timer=[Diagnostics.Stopwatch]::StartNew()
 $frameCount=if($Move -eq 'Tempest'){48}else{78}
 for($i=0;$i -lt $frameCount;$i++) {
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
Write-Output "Captured $Move replay: $captureDirectory"
