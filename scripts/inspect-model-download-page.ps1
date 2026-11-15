$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$modelBrowser = Get-Process msedge -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like 'Will Smith*Sketchfab*' -or $_.MainWindowTitle -like 'Will Smith - Download Free 3D model*' } | Select-Object -First 1
if (-not $modelBrowser) { throw 'Will Smith model page window not found.' }
$windowElement = [Windows.Automation.AutomationElement]::FromHandle($modelBrowser.MainWindowHandle)
$documentCondition = New-Object Windows.Automation.PropertyCondition ([Windows.Automation.AutomationElement]::ControlTypeProperty), ([Windows.Automation.ControlType]::Document)
$documents = $windowElement.FindAll([Windows.Automation.TreeScope]::Descendants, $documentCondition)
foreach ($document in $documents) {
    if ($document.Current.Name -notlike '*Will Smith*') { continue }
    $document.Current.Name
    $elements = $document.FindAll([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.Condition]::TrueCondition)
    foreach ($element in $elements) {
        $info = $element.Current
        if (-not $info.IsOffscreen -and $info.Name -and $info.ControlType -ne [Windows.Automation.ControlType]::Edit) {
            '{0}: {1}' -f $info.ControlType.ProgrammaticName, $info.Name
        }
    }
}
