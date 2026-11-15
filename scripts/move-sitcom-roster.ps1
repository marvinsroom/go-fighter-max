$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$gameRoot = Join-Path $taskRoot 'sprite-fighter'
$sitcomRoot = Join-Path $gameRoot 'sitcom'
$mainEngine = Join-Path $gameRoot 'engine/ikemen-go-v1.0.0'
$sitcomEngine = Join-Path $sitcomRoot 'engine/ikemen-go-v1.0.0'
function Assert-WorkspacePath([string]$value) {
    $resolved = [IO.Path]::GetFullPath($value)
    if (!$resolved.StartsWith($taskRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $resolved" }
    return $resolved
}
function Move-WorkspaceItem([string]$source, [string]$destination) {
    $source = Assert-WorkspacePath $source
    $destination = Assert-WorkspacePath $destination
    if (!(Test-Path -LiteralPath $source)) { return }
    if (Test-Path -LiteralPath $destination) { throw "Destination exists: $destination" }
    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($destination)) -Force | Out-Null
    Move-Item -LiteralPath $source -Destination $destination
    Write-Output "Moved $([IO.Path]::GetFileName($source))"
}
New-Item -ItemType Directory -Path $sitcomEngine -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $sitcomRoot 'before') -Force | Out-Null
$selectBackup = Join-Path $sitcomRoot 'before/main-select.def'
if (!(Test-Path -LiteralPath $selectBackup)) { Copy-Item -LiteralPath (Join-Path $mainEngine 'data/select.def') -Destination $selectBackup }
# The two games have independent configs, rosters and native character folders.
foreach ($name in @('data','external','font','lib','save','sound','stages','video')) {
    $destination = Join-Path $sitcomEngine $name
    if (!(Test-Path -LiteralPath $destination)) { Copy-Item -LiteralPath (Join-Path $mainEngine $name) -Destination $destination -Recurse }
}
foreach ($name in @('Ikemen_GO.exe','LICENSES.txt','README.md')) {
    $destination = Join-Path $sitcomEngine $name
    if (!(Test-Path -LiteralPath $destination)) { Copy-Item -LiteralPath (Join-Path $mainEngine $name) -Destination $destination }
}
foreach ($name in @('will_full','will_idle','will_motion','prince','tyrone','urkel','yamal','rick','negan')) {
    Move-WorkspaceItem (Join-Path $mainEngine "chars/$name") (Join-Path $sitcomEngine "chars/$name")
}
foreach ($name in @('will','prince','tyrone','urkel','yamal','rick','negan','chappelle')) {
    Move-WorkspaceItem (Join-Path $gameRoot "characters/$name") (Join-Path $sitcomRoot "characters/$name")
}
foreach ($file in Get-ChildItem -LiteralPath $gameRoot -File) {
    if ($file.Extension -eq '.cmd' -and $file.Name -match '(?i)will|prince|tyrone|urkel|yamal|chappelle|rick|negan') {
        Move-WorkspaceItem $file.FullName (Join-Path $sitcomRoot "archive/launchers/$($file.Name)")
    } elseif ($file.Extension -in @('.log','.txt') -and $file.Name -match '^(?i:will|prince|tyrone|urkel|yamal|chappelle|rick|negan)[-]') {
        Move-WorkspaceItem $file.FullName (Join-Path $sitcomRoot "logs/$($file.Name)")
    }
}
Move-WorkspaceItem (Join-Path $gameRoot 'WILL_CONTROLS.md') (Join-Path $sitcomRoot 'WILL_CONTROLS.md')
Write-Output 'Sitcom character files preserved in a separate engine. Configure rosters and launchers next.'
