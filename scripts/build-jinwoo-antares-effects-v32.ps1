param(
    [string]$Root = "C:\Users\15168\Development\Vs-Fighter\go-fighter-max\sprite-fighter\characters\jinwoo-mugen\art\naruto-style-v2\loco-final-v32"
)

Add-Type -AssemblyName System.Drawing

$masters = Join-Path $Root "antares-effect-masters"
$output = Join-Path $Root "antares-effects-normalized"
New-Item -ItemType Directory -Force -Path $output | Out-Null

$canvasSize = 1536
$center = $canvasSize / 2

function Export-EffectFrame {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Destination,
        [Parameter(Mandatory = $true)][double]$Scale,
        [Parameter(Mandatory = $true)][double]$Opacity,
        [ValidateSet("Center", "Bottom")][string]$Anchor = "Center"
    )

    $sourceImage = [System.Drawing.Image]::FromFile($Source)
    $frame = [System.Drawing.Bitmap]::new($canvasSize, $canvasSize, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $graphics = [System.Drawing.Graphics]::FromImage($frame)
    $attributes = [System.Drawing.Imaging.ImageAttributes]::new()
    try {
        $graphics.Clear([System.Drawing.Color]::Transparent)
        $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceOver
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality

        $drawWidth = [Math]::Max(1, [Math]::Round($sourceImage.Width * $Scale))
        $drawHeight = [Math]::Max(1, [Math]::Round($sourceImage.Height * $Scale))
        $drawX = [Math]::Round($center - ($drawWidth / 2))
        $drawY = if ($Anchor -eq "Bottom") { 1488 - $drawHeight } else { [Math]::Round($center - ($drawHeight / 2)) }

        $matrix = [System.Drawing.Imaging.ColorMatrix]::new()
        $matrix.Matrix33 = [single]$Opacity
        $attributes.SetColorMatrix($matrix, [System.Drawing.Imaging.ColorMatrixFlag]::Default, [System.Drawing.Imaging.ColorAdjustType]::Bitmap)
        $destinationRect = [System.Drawing.Rectangle]::new($drawX, $drawY, $drawWidth, $drawHeight)
        $graphics.DrawImage($sourceImage, $destinationRect, 0, 0, $sourceImage.Width, $sourceImage.Height, [System.Drawing.GraphicsUnit]::Pixel, $attributes)
        $frame.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
    }
    finally {
        $attributes.Dispose()
        $graphics.Dispose()
        $frame.Dispose()
        $sourceImage.Dispose()
    }
}

$castMaster = Join-Path $masters "antares-cast-column-master-v32.png"
$impactMaster = Join-Path $masters "antares-impact-x-master-v32.png"
$finishMaster = Join-Path $masters "antares-finish-burst-master-v32.png"

$castFrames = @(
    @{ Name = "antares-cast-flare--1988-7-v32.png"; Source = $finishMaster; Scale = 0.40; Opacity = 0.82; Anchor = "Center" },
    @{ Name = "antares-cast-column--1988-8-v32.png"; Source = $castMaster; Scale = 0.72; Opacity = 0.92; Anchor = "Bottom" },
    @{ Name = "antares-cast-core--1988-10-v32.png"; Source = $castMaster; Scale = 0.43; Opacity = 1.00; Anchor = "Bottom" }
)

$impactScales = @(0.28, 0.46, 0.66, 0.86, 0.98, 1.05)
$impactOpacity = @(0.62, 0.78, 0.92, 1.00, 0.76, 0.46)
$finishScales = @(0.18, 0.28, 0.40, 0.54, 0.70, 0.84, 0.96, 1.04, 1.10, 1.16)
$finishOpacity = @(0.42, 0.58, 0.74, 0.88, 1.00, 1.00, 0.90, 0.70, 0.46, 0.24)

foreach ($spec in $castFrames) {
    Export-EffectFrame -Source $spec.Source -Destination (Join-Path $output $spec.Name) -Scale $spec.Scale -Opacity $spec.Opacity -Anchor $spec.Anchor
}

for ($index = 0; $index -lt $impactScales.Count; $index++) {
    $name = "antares-impact-{0:D2}--2024-{1}-v32.png" -f $index, $index
    Export-EffectFrame -Source $impactMaster -Destination (Join-Path $output $name) -Scale $impactScales[$index] -Opacity $impactOpacity[$index]
}

for ($index = 0; $index -lt $finishScales.Count; $index++) {
    $name = "antares-finish-{0:D2}--2053-{1}-v32.png" -f $index, $index
    Export-EffectFrame -Source $finishMaster -Destination (Join-Path $output $name) -Scale $finishScales[$index] -Opacity $finishOpacity[$index]
}

Get-ChildItem -LiteralPath $output -Filter "*.png" | Sort-Object Name | Select-Object Name, Length
