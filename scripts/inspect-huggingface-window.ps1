param([switch]$OpenSpace)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class HFWindow {
 [StructLayout(LayoutKind.Sequential)] public struct RECT {public int Left,Top,Right,Bottom;}
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT r);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h,int c);
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
'@
[HFWindow]::SetProcessDPIAware() | Out-Null
$browser=Get-Process msedge | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -match 'Hugging Face|TRELLIS|Pixal3D' } | Select-Object -First 1
if (-not $browser) {throw 'No visible Hugging Face browser window.'}
[HFWindow]::ShowWindow($browser.MainWindowHandle,3) | Out-Null
[HFWindow]::SetForegroundWindow($browser.MainWindowHandle) | Out-Null
$keys=New-Object -ComObject WScript.Shell
$keys.AppActivate($browser.Id) | Out-Null
try { [Windows.Automation.AutomationElement]::FromHandle($browser.MainWindowHandle).SetFocus() } catch {}
Start-Sleep -Milliseconds 350
if ([HFWindow]::GetForegroundWindow() -ne $browser.MainWindowHandle) {throw 'Hugging Face browser is not foreground.'}
if ($OpenSpace) {
 $keys.SendKeys('^l');Start-Sleep -Milliseconds 150
 $keys.SendKeys('https://huggingface.co/spaces/microsoft/TRELLIS.2');$keys.SendKeys('{ENTER}')
 Start-Sleep -Seconds 5
}
if ([HFWindow]::GetForegroundWindow() -ne $browser.MainWindowHandle) {throw 'Browser lost foreground.'}
$rect=New-Object HFWindow+RECT
if (-not [HFWindow]::GetWindowRect($browser.MainWindowHandle,[ref]$rect)) {throw 'No browser bounds.'}
$bitmap=New-Object Drawing.Bitmap ($rect.Right-$rect.Left),($rect.Bottom-$rect.Top)
$graphics=[Drawing.Graphics]::FromImage($bitmap)
try {
 $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
 $bitmap.Save((Join-Path $PSScriptRoot '..\tooling\huggingface-browser.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally {$graphics.Dispose();$bitmap.Dispose()}
$window=[Windows.Automation.AutomationElement]::FromHandle($browser.MainWindowHandle)
$elements=$window.FindAll([Windows.Automation.TreeScope]::Descendants,[Windows.Automation.Condition]::TrueCondition)
$rows=foreach ($element in $elements) {
 $info=$element.Current
 if (-not $info.IsOffscreen -and $info.Name -and $info.ControlType -ne [Windows.Automation.ControlType]::Edit) {
  [PSCustomObject]@{Type=$info.ControlType.ProgrammaticName;Name=$info.Name;Bounds=$info.BoundingRectangle.ToString()}
 }
}
$rows | ConvertTo-Json -Depth 3 | Set-Content (Join-Path $PSScriptRoot '..\tooling\huggingface-ui-elements.json')
Write-Output 'Saved target browser screenshot and visible UI labels.'
