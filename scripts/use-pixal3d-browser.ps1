param([Parameter(Mandatory=$true)][ValidateSet('Upload','Balanced','Generate','Extract','Download','ReduceMesh')][string]$Action)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @'
using System; using System.Runtime.InteropServices;
public class PixalUI {
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x,int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint flags,uint dx,uint dy,uint data,UIntPtr extra);
}
'@
$browser=Get-Process msedge | Where-Object {$_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like '*Pixal3D*'} | Select-Object -First 1
if(-not $browser){throw 'Pixal3D browser is not visible.'}
$window=[Windows.Automation.AutomationElement]::FromHandle($browser.MainWindowHandle)
[PixalUI]::SetForegroundWindow($browser.MainWindowHandle) | Out-Null
$activate=New-Object -ComObject WScript.Shell;$activate.AppActivate($browser.Id) | Out-Null
try{$window.SetFocus()}catch{}
Start-Sleep -Milliseconds 350
function Find-Name([string]$Name) {
 $cond=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::NameProperty),$Name
 $window.FindFirst([Windows.Automation.TreeScope]::Descendants,$cond)
}
function Activate-Control($element) {
 if(-not $element){throw 'Expected Pixal3D control not found.'}
 if(-not $element.Current.IsEnabled){throw 'Pixal3D control is disabled.'}
 $pattern=$null
 if($element.TryGetCurrentPattern([Windows.Automation.InvokePattern]::Pattern,[ref]$pattern)){$pattern.Invoke();return}
 $scroll=$null
 if($element.TryGetCurrentPattern([Windows.Automation.ScrollItemPattern]::Pattern,[ref]$scroll)){$scroll.ScrollIntoView();Start-Sleep -Milliseconds 300}
 if([PixalUI]::GetForegroundWindow() -ne $browser.MainWindowHandle){throw 'Pixal3D browser is not foreground; no click sent.'}
 $r=$element.Current.BoundingRectangle
 if($element.Current.IsOffscreen -or $r.Width -lt 1 -or $r.Height -lt 1){throw 'Pixal3D control is outside the visible page.'}
 [PixalUI]::SetCursorPos([int]($r.X+$r.Width/2),[int]($r.Y+$r.Height/2)) | Out-Null
 [PixalUI]::mouse_event(2,0,0,0,[UIntPtr]::Zero);[PixalUI]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
}
if($Action -eq 'Balanced') {
 $cond=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::AutomationIdProperty),'resolution'
 $combo=$window.FindFirst([Windows.Automation.TreeScope]::Descendants,$cond)
 if(-not $combo){throw 'Pixal3D resolution field not found.'}
 $combo.GetCurrentPattern([Windows.Automation.ExpandCollapsePattern]::Pattern).Expand()
 $option=Find-Name '1024 (Balanced)'
 if(-not $option){throw 'Balanced option not found.'}
 $option.GetCurrentPattern([Windows.Automation.SelectionItemPattern]::Pattern).Select()
 Write-Output 'Selected Pixal3D 1024 balanced generation.';exit
}
if($Action -eq 'ReduceMesh') {
 Activate-Control (Find-Name 'ADVANCED ENGINE')
 Start-Sleep -Milliseconds 500
 $cond=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::AutomationIdProperty),'decimation'
 $slider=$window.FindFirst([Windows.Automation.TreeScope]::Descendants,$cond)
 if(-not $slider){throw 'Pixal3D decimation slider not found.'}
 $slider.GetCurrentPattern([Windows.Automation.RangeValuePattern]::Pattern).SetValue(100000)
 Write-Output 'Requested 100000 faces for mesh export.';exit
}
$name=switch($Action){'Upload'{'Upload Reference'} 'Generate'{'Start Generation'} 'Extract'{'Extract Mesh (GLB)'} 'Download'{'Download Asset'}}
Activate-Control (Find-Name $name)
Write-Output ('Invoked Pixal3D '+$name)
if($Action -eq 'Upload') {
 Start-Sleep -Seconds 2
 $condition=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::ControlTypeProperty),([Windows.Automation.ControlType]::Window)
 $dialog=$window.FindAll([Windows.Automation.TreeScope]::Descendants,$condition) | Where-Object {$_.Current.Name -eq 'Open'} | Select-Object -First 1
 if(-not $dialog){throw 'Pixal3D browser upload dialog not found.'}
 try{$dialog.SetFocus()}catch{}
 $keys=New-Object -ComObject WScript.Shell;$keys.AppActivate('Open') | Out-Null
 Start-Sleep -Milliseconds 350
 if([PixalUI]::GetForegroundWindow().ToInt64() -ne $dialog.Current.NativeWindowHandle){throw 'Upload dialog is not foreground; no typing sent.'}
 $keys.SendKeys('%n');$keys.SendKeys('C:\Users\15168\game1\characters\will\trellis-cel-v1\will-cel-apose-input-v1.png');$keys.SendKeys('{ENTER}')
 Write-Output 'Uploaded only the prepared Will reference.'
}
