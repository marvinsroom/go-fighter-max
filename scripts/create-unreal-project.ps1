$ErrorActionPreference = 'Stop'
$engineRoot = 'C:\Program Files\Epic Games\UE_5.8'
$projectRoot = Join-Path $PSScriptRoot '..\SitcomFighter'
$projectRoot = [IO.Path]::GetFullPath($projectRoot)
if (Test-Path -LiteralPath $projectRoot) { throw 'Project folder already exists; refusing to overwrite it.' }
$templateRoot = Join-Path $engineRoot 'Templates\TP_ThirdPersonBP'
New-Item -ItemType Directory -Path (Join-Path $projectRoot 'Config') -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $templateRoot 'Content') -Destination $projectRoot -Recurse
foreach ($configName in @('DefaultEngine.ini', 'DefaultGame.ini', 'DefaultInput.ini')) {
    Copy-Item -LiteralPath (Join-Path $templateRoot "Config\$configName") -Destination (Join-Path $projectRoot "Config\$configName")
}
foreach ($packName in @('Characters', 'Input', 'LevelPrototyping')) {
    $packContent = Join-Path $engineRoot "Templates\TemplateResources\High\$packName\Content"
    Copy-Item -LiteralPath $packContent -Destination (Join-Path $projectRoot "Content\$packName") -Recurse
}
$variantRoot = Join-Path $engineRoot 'Templates\TemplateResources\Standard\Variant_SideScroller'
Copy-Item -LiteralPath (Join-Path $variantRoot 'Content') -Destination (Join-Path $projectRoot 'Content\Variant_SideScroller') -Recurse
foreach ($externalFolder in @('__ExternalActors__', '__ExternalObjects__')) {
    New-Item -ItemType Directory -Path (Join-Path $projectRoot "Content\$externalFolder") -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $variantRoot $externalFolder) -Destination (Join-Path $projectRoot "Content\$externalFolder\Variant_SideScroller") -Recurse
}
$projectDescriptor = @{
    FileVersion = 3
    EngineAssociation = '5.8'
    Category = 'Games'
    Description = 'Side-view comedy fighting game prototype'
    Plugins = @(
        @{ Name = 'EnhancedInput'; Enabled = $true },
        @{ Name = 'GameplayStateTree'; Enabled = $true },
        @{ Name = 'PythonScriptPlugin'; Enabled = $true; TargetAllowList = @('Editor') },
        @{ Name = 'EditorScriptingUtilities'; Enabled = $true; TargetAllowList = @('Editor') }
    )
}
$projectDescriptor | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $projectRoot 'SitcomFighter.uproject') -Encoding UTF8
$engineConfigPath = Join-Path $projectRoot 'Config\DefaultEngine.ini'
$engineConfig = Get-Content -LiteralPath $engineConfigPath -Raw
$engineConfig = $engineConfig.Replace('GameName=TP_ThirdPersonBP', 'GameName=SitcomFighter')
$engineConfig = $engineConfig.Replace('/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson', '/Game/Variant_SideScroller/Lvl_SideScrolling.Lvl_SideScrolling')
$engineConfig = $engineConfig.Replace('/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C', '/Game/Variant_SideScroller/Blueprints/BP_SideScrollingGameMode.BP_SideScrollingGameMode_C')
$engineConfig = $engineConfig.Replace('bUseSplitscreen=True', 'bUseSplitscreen=False')
Set-Content -LiteralPath $engineConfigPath -Value $engineConfig -Encoding UTF8
$projectGuid = [Guid]::NewGuid().ToString('N')
@("[/Script/EngineSettings.GeneralProjectSettings]", "ProjectID=$projectGuid", 'ProjectName=SitcomFighter', 'Description=Side-view comedy fighting game prototype') | Set-Content -LiteralPath (Join-Path $projectRoot 'Config\DefaultGame.ini') -Encoding UTF8
Write-Output "Created $projectRoot\SitcomFighter.uproject"
