param([ValidateSet('Igris','Beru','Iron','Tank')][string]$Shadow='Igris')
$ErrorActionPreference='Stop'
. "$PSScriptRoot/inspect-ikemen-window.ps1"
# This keyboard check assumes the launcher positions Jinwoo on the right.
$direction=@{Igris=0;Beru=74;Iron=76;Tank=75}[$Shadow]
$delay=@{Igris=500;Beru=420;Iron=700;Tank=500}[$Shadow]
function Key-State([byte]$code,[bool]$down){
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost'}
 [IkemenWindow]::keybd_event($code,[byte][IkemenWindow]::MapVirtualKey($code,0),$(if($down){0}else{2}),[UIntPtr]::Zero)
}
try{
 if($direction){Key-State $direction $true;Start-Sleep -Milliseconds 50}
 Key-State 82 $true;Start-Sleep -Milliseconds $delay
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Game focus lost'}
 $rect=New-Object IkemenWindow+RECT
 [IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
 $bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
 $graphics=[System.Drawing.Graphics]::FromImage($bitmap)
 try{
  $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
  $path=Join-Path $PSScriptRoot ("../sprite-fighter/characters/jinwoo/jinwoo-"+$Shadow.ToLower()+"-v3-engine.png")
  $bitmap.Save([IO.Path]::GetFullPath($path),[System.Drawing.Imaging.ImageFormat]::Png)
 }finally{$graphics.Dispose();$bitmap.Dispose()}
}finally{
 foreach($code in @(82,$direction)){
  if($code){[IkemenWindow]::keybd_event([byte]$code,[byte][IkemenWindow]::MapVirtualKey($code,0),2,[UIntPtr]::Zero)}
 }
}
Write-Output "Captured actual $Shadow input"
