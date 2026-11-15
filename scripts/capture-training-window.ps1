$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class TrainingWindowCapture {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr window, out RECT rect);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr window, IntPtr hdc, uint flags);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr window);
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int command);
}
'@
[TrainingWindowCapture]::SetProcessDPIAware() | Out-Null
$editorProcess = Get-Process UnrealEditor | Where-Object { $_.MainWindowTitle -like '*SitcomFighter*' -and $_.MainWindowHandle -ne 0 } | Sort-Object StartTime -Descending | Select-Object -First 1
if (-not $editorProcess) { throw 'No visible SitcomFighter editor window found.' }
[TrainingWindowCapture]::ShowWindow($editorProcess.MainWindowHandle, 9) | Out-Null
Start-Sleep -Milliseconds 300
$windowRect = New-Object TrainingWindowCapture+RECT
if (-not [TrainingWindowCapture]::GetWindowRect($editorProcess.MainWindowHandle, [ref]$windowRect)) { throw 'Could not read editor window bounds.' }
$bitmap = New-Object Drawing.Bitmap ($windowRect.Right - $windowRect.Left), ($windowRect.Bottom - $windowRect.Top)
$graphics = [Drawing.Graphics]::FromImage($bitmap)
[TrainingWindowCapture]::SetForegroundWindow($editorProcess.MainWindowHandle) | Out-Null
$activate = New-Object -ComObject WScript.Shell
$activate.AppActivate($editorProcess.Id) | Out-Null
Start-Sleep -Milliseconds 400
if ([TrainingWindowCapture]::GetForegroundWindow() -eq $editorProcess.MainWindowHandle) {
    Write-Output 'Capture mode: screen pixels from the foreground editor window'
    $graphics.CopyFromScreen($windowRect.Left, $windowRect.Top, 0, 0, $bitmap.Size)
    $captured = $true
} else {
    Write-Output 'Capture mode: PrintWindow fallback (GPU viewport may be black)'
    $dc = $graphics.GetHdc()
    try { $captured = [TrainingWindowCapture]::PrintWindow($editorProcess.MainWindowHandle, $dc, 2) }
    finally { $graphics.ReleaseHdc($dc) }
}
try {
    if (-not $captured) { throw 'Editor screenshot failed.' }
    $imagePath = Join-Path $PSScriptRoot '..\SitcomFighter\Saved\training-preview.png'
    $bitmap.Save([IO.Path]::GetFullPath($imagePath), [Drawing.Imaging.ImageFormat]::Png)
    Write-Output ([IO.Path]::GetFullPath($imagePath))
}
finally { $graphics.Dispose(); $bitmap.Dispose() }
