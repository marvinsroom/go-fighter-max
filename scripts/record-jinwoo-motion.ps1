param([string]$CaptureName='motion-v2',[switch]$Proportions,[switch]$Transformation)
$ErrorActionPreference='Stop'
. "$PSScriptRoot/inspect-ikemen-window.ps1"
if($CaptureName -notmatch '^[a-z0-9-]+$'){throw 'Invalid capture name'}
$captureDirectory=Join-Path $PSScriptRoot "../sprite-fighter/characters/jinwoo/replays/$CaptureName"
New-Item -ItemType Directory -Force -Path $captureDirectory | Out-Null
$rect=New-Object IkemenWindow+RECT
[IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
$bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
function Set-GameKey([byte]$code,[bool]$down){
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost'}
 $scan=[byte][IkemenWindow]::MapVirtualKey($code,0)
 [IkemenWindow]::keybd_event($code,$scan,$(if($down){0}else{2}),[UIntPtr]::Zero)
}
$events=@(@(0,74,$true),@(700,74,$false),@(1100,76,$true),@(1900,76,$false),
 @(2300,73,$true),@(2480,73,$false),@(3300,70,$true),@(3480,70,$false),
 @(4200,71,$true),@(4380,71,$false),@(5200,72,$true),@(5380,72,$false))
$samples=@();$frames=New-Object 'System.Collections.Generic.List[System.Drawing.Bitmap]'
if($Proportions){
 $events=@(@(0,75,$true),@(800,75,$false),@(1200,72,$true),@(1320,72,$false),
 @(2000,74,$true),@(4400,74,$false),@(4800,81,$true),@(4940,81,$false))
}
if($Transformation){
 $events=@(@(0,221,$true),@(120,221,$false),@(1000,74,$true),@(1600,74,$false),
 @(2100,71,$true),@(2220,71,$false),@(3100,73,$true),@(3220,73,$false),
 @(4600,221,$true),@(4720,221,$false),@(5600,221,$true),@(5720,221,$false))
}
$nextEvent=0;$i=0;$timer=[Diagnostics.Stopwatch]::StartNew()
try{
 while($timer.ElapsedMilliseconds -lt 6500){
  if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Focus lost; capture stopped'}
  while($nextEvent -lt $events.Count -and $timer.ElapsedMilliseconds -ge $events[$nextEvent][0]){
   Set-GameKey $events[$nextEvent][1] $events[$nextEvent][2];$nextEvent++
  }
  $milliseconds=$timer.ElapsedMilliseconds
  $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
  $name='frame-{0:D3}.png' -f $i
  # Defer PNG compression until playback ends, so recording can show the gait.
  $frames.Add($bitmap.Clone())
  $samples+=@{file=$name;milliseconds=$milliseconds};$i++
  Start-Sleep -Milliseconds 60
 }
 for($frameIndex=0;$frameIndex -lt $frames.Count;$frameIndex++){
  $frames[$frameIndex].Save((Join-Path $captureDirectory $samples[$frameIndex].file),[System.Drawing.Imaging.ImageFormat]::Png)
 }
}finally{
 foreach($code in @(74,76,73,70,71,72,75,81,221)){
  $scan=[byte][IkemenWindow]::MapVirtualKey($code,0)
  [IkemenWindow]::keybd_event([byte]$code,$scan,2,[UIntPtr]::Zero)
 }
 foreach($frame in $frames){$frame.Dispose()}
 $graphics.Dispose();$bitmap.Dispose()
}
$samples | ConvertTo-Json | Set-Content (Join-Path $captureDirectory 'timing.json')
Write-Output "Recorded Jinwoo motion: $i native frames"
