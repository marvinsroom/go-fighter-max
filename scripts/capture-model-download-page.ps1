$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class ModelPageCapture {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT rect);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int command);
}
'@
[ModelPageCapture]::SetProcessDPIAware() | Out-Null
$modelBrowser = Get-Process msedge | Where-Object { $_.MainWindowTitle -like 'Will Smith - Download Free 3D model*' } | Select-Object -First 1
if (-not $modelBrowser) { throw 'Model page is not the active browser tab.' }
[ModelPageCapture]::ShowWindow($modelBrowser.MainWindowHandle,9) | Out-Null
[ModelPageCapture]::SetForegroundWindow($modelBrowser.MainWindowHandle) | Out-Null
$activate = New-Object -ComObject WScript.Shell
$activate.AppActivate($modelBrowser.Id) | Out-Null
Start-Sleep -Milliseconds 350
if ([ModelPageCapture]::GetForegroundWindow() -ne $modelBrowser.MainWindowHandle) { throw 'Browser is not foreground; refusing unrelated screen capture.' }
$rect=New-Object ModelPageCapture+RECT
if (-not [ModelPageCapture]::GetWindowRect($modelBrowser.MainWindowHandle,[ref]$rect)) { throw 'Cannot read browser bounds.' }
$bitmap=New-Object Drawing.Bitmap ($rect.Right-$rect.Left),($rect.Bottom-$rect.Top)
$graphics=[Drawing.Graphics]::FromImage($bitmap)
try {
    $graphics.CopyFromScreen($rect.Left,$rect.Top,0,0,$bitmap.Size)
    $bitmap.Save((Join-Path $PSScriptRoot '..\tooling\model-download-page.png'),[Drawing.Imaging.ImageFormat]::Png)
} finally { $graphics.Dispose();$bitmap.Dispose() }
