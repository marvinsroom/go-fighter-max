param([Parameter(Mandatory=$true)][ValidateSet('Upload','Generate','Extract','Download','ZoomOut')][string]$Action)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$browser=Get-Process msedge | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like '*TRELLIS.2*' } | Select-Object -First 1
if (-not $browser) {throw 'TRELLIS browser tab is not visible.'}
$window=[Windows.Automation.AutomationElement]::FromHandle($browser.MainWindowHandle)
try {$window.SetFocus()} catch {}
if ($Action -eq 'ZoomOut') {
 $keys=New-Object -ComObject WScript.Shell
 $keys.SendKeys('^-');$keys.SendKeys('^-');$keys.SendKeys('^-')
 Write-Output 'Reduced zoom in the TRELLIS tab.'
 exit
}
$name=switch($Action) { 'Upload' {'Drop an image file here to upload'} 'Generate' {'Generate'} 'Extract' {'Extract GLB'} 'Download' {'Download GLB'} }
$condition=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::NameProperty),$name
$matches=$window.FindAll([Windows.Automation.TreeScope]::Descendants,$condition)
$control=@($matches | Where-Object { $_.Current.ControlType -in @([Windows.Automation.ControlType]::Button,[Windows.Automation.ControlType]::Hyperlink) }) | Select-Object -First 1
if (-not $control) {throw ('Missing TRELLIS control: '+$name)}
$scroll=$null
if ($control.TryGetCurrentPattern([Windows.Automation.ScrollItemPattern]::Pattern,[ref]$scroll)) {$scroll.ScrollIntoView()}
if (-not $control.Current.IsEnabled) {throw ($name+' is disabled.')}
$invoke=$control.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern)
$invoke.Invoke()
Write-Output ('Invoked TRELLIS '+$name)
if ($Action -eq 'Upload') {
 Start-Sleep -Seconds 1
 $dialogCondition=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::NameProperty),'Open'
 $dialog=$window.FindFirst([Windows.Automation.TreeScope]::Descendants,$dialogCondition)
 if (-not $dialog) {throw 'Expected browser upload file dialog not found.'}
 $editCondition=New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::ControlTypeProperty),([Windows.Automation.ControlType]::Edit)
 $edits=$dialog.FindAll([Windows.Automation.TreeScope]::Descendants,$editCondition)
 $filename=@($edits | Where-Object { $_.Current.AutomationId -eq '1148' -or $_.Current.Name -like 'File name*' }) | Select-Object -First 1
 if (-not $filename) {throw 'Upload dialog filename box not found.'}
 $inputPath='C:\Users\15168\game1\characters\will\trellis-cel-v1\will-cel-apose-input-v1.png'
 if (-not (Test-Path -LiteralPath $inputPath -PathType Leaf)) {throw 'Prepared input is missing.'}
 $filename.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue($inputPath)
 $buttons=$dialog.FindAll([Windows.Automation.TreeScope]::Descendants,$dialogCondition)
 $open=@($buttons | Where-Object { $_.Current.ControlType -eq [Windows.Automation.ControlType]::Button }) | Select-Object -First 1
 if (-not $open) {throw 'Upload dialog Open button not found.'}
 $open.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
 Write-Output 'Uploaded only the prepared Will character reference.'
}
