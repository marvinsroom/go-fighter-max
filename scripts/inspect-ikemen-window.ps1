param([string]$Keys='', [int[]]$KeyCodes=@(), [switch]$CaptureSeries,
 [ValidateRange(40,10000)][int]$HoldMilliseconds=120, [switch]$CaptureDuringHold)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName UIAutomationClient
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class IkemenWindow {
 [StructLayout(LayoutKind.Sequential)] public struct RECT {public int Left,Top,Right,Bottom;}
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd,out RECT rect);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd,int cmd);
 [DllImport("user32.dll")] public static extern void keybd_event(byte key,byte scan,uint flags,UIntPtr extra);
 [DllImport("user32.dll")] public static extern uint MapVirtualKey(uint code,uint mapType);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr window,out uint process);
 [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
 [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint first,uint second,bool attach);
}
'@
$game=Get-Process -Name Ikemen_GO | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1
if(-not $game){throw 'No IKEMEN GO game window found'}
$window=$game.MainWindowHandle
[IkemenWindow]::ShowWindow($window,9)|Out-Null
[IkemenWindow]::SetForegroundWindow($window)|Out-Null
$shell=New-Object -ComObject WScript.Shell
$shell.AppActivate($game.Id)|Out-Null
try {[System.Windows.Automation.AutomationElement]::FromHandle($window).SetFocus()} catch {}
Start-Sleep -Milliseconds 500
if([IkemenWindow]::GetForegroundWindow() -ne $window){
 [uint32]$focusOwner=0
 $foregroundThread=[IkemenWindow]::GetWindowThreadProcessId([IkemenWindow]::GetForegroundWindow(),[ref]$focusOwner)
 $currentThread=[IkemenWindow]::GetCurrentThreadId()
 $attached=[IkemenWindow]::AttachThreadInput($currentThread,$foregroundThread,$true)
 try {[IkemenWindow]::SetForegroundWindow($window)|Out-Null}
 finally {if($attached){[IkemenWindow]::AttachThreadInput($currentThread,$foregroundThread,$false)|Out-Null}}
 Start-Sleep -Milliseconds 300
}
if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'IKEMEN is not foreground; no input or capture performed'}
if($Keys){[System.Windows.Forms.SendKeys]::SendWait($Keys);Start-Sleep -Milliseconds 900}
foreach($code in $KeyCodes){
 if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Focus changed; no further input'}
 $scan=[byte][IkemenWindow]::MapVirtualKey($code,0)
 $flags=if($code -ge 37 -and $code -le 40){[uint32]1}else{[uint32]0}
 [IkemenWindow]::keybd_event([byte]$code,$scan,$flags,[UIntPtr]::Zero)
 try {
  Start-Sleep -Milliseconds $HoldMilliseconds
  if($CaptureDuringHold){
   if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Focus changed; no held-key capture'}
   $heldRect=New-Object IkemenWindow+RECT
   [IkemenWindow]::GetWindowRect($window,[ref]$heldRect)|Out-Null
   $heldBitmap=New-Object System.Drawing.Bitmap(($heldRect.Right-$heldRect.Left),($heldRect.Bottom-$heldRect.Top))
   $heldGraphics=[System.Drawing.Graphics]::FromImage($heldBitmap)
   try {
    $heldGraphics.CopyFromScreen($heldRect.Left,$heldRect.Top,0,0,$heldBitmap.Size)
    $heldPath=Join-Path $PSScriptRoot '../sprite-fighter/ikemen-held.png'
    $heldBitmap.Save([IO.Path]::GetFullPath($heldPath),[System.Drawing.Imaging.ImageFormat]::Png)
   } finally {$heldGraphics.Dispose();$heldBitmap.Dispose()}
  }
 } finally {[IkemenWindow]::keybd_event([byte]$code,$scan,($flags -bor 2),[UIntPtr]::Zero)}
 Start-Sleep -Milliseconds 220
}
if($KeyCodes.Count -gt 0){Start-Sleep -Milliseconds 900}
if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Focus changed; no capture performed'}
$rect=New-Object IkemenWindow+RECT
[IkemenWindow]::GetWindowRect($window,[ref]$rect)|Out-Null
$bitmap=New-Object System.Drawing.Bitmap(($rect.Right-$rect.Left),($rect.Bottom-$rect.Top))
$graphics=[System.Drawing.Graphics]::FromImage($bitmap)
try {
 $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
 $path=Join-Path $PSScriptRoot '../sprite-fighter/ikemen-preview.png'
 $bitmap.Save([IO.Path]::GetFullPath($path),[System.Drawing.Imaging.ImageFormat]::Png)
 if($CaptureSeries){
  foreach($sample in 1..3){
   Start-Sleep -Milliseconds 320
   if([IkemenWindow]::GetForegroundWindow() -ne $window){throw 'Focus changed; capture series stopped'}
   $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
   $seriesPath=Join-Path $PSScriptRoot ('../sprite-fighter/ikemen-sequence-'+$sample+'.png')
   $bitmap.Save([IO.Path]::GetFullPath($seriesPath),[System.Drawing.Imaging.ImageFormat]::Png)
  }
 }
} finally {$graphics.Dispose();$bitmap.Dispose()}
Write-Output ('IKEMEN window: '+$game.MainWindowTitle+'; pid '+$game.Id)
