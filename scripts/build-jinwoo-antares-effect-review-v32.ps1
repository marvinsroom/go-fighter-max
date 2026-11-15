param(
    [string]$Root = "C:\Users\15168\Development\Vs-Fighter\go-fighter-max\sprite-fighter\characters\jinwoo-mugen\art\naruto-style-v2\loco-final-v32",
    [string]$SourceFolder = "weapon-references",
    [string]$OutputName = "antares-effect-review-v32.png"
)

Add-Type -AssemblyName System.Drawing

$source = Join-Path $Root $SourceFolder
$output = Join-Path $Root $OutputName
$files = Get-ChildItem -LiteralPath $source -Filter "antares-*.png" |
    Where-Object { $_.Name -match '^antares-(cast-(flare|column|core)|impact-|finish-)' } |
    Sort-Object Name

$columns = 4
$cellWidth = 420
$cellHeight = 420
$labelHeight = 44
$rows = [Math]::Ceiling($files.Count / $columns)
$sheet = [System.Drawing.Bitmap]::new($columns * $cellWidth, $rows * $cellHeight)
$graphics = [System.Drawing.Graphics]::FromImage($sheet)
$graphics.Clear([System.Drawing.Color]::FromArgb(255, 24, 24, 30))
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::NearestNeighbor
$font = [System.Drawing.Font]::new("Segoe UI", 13, [System.Drawing.FontStyle]::Regular)
$textBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
$checkerA = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(255, 58, 58, 68))
$checkerB = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(255, 78, 78, 90))

try {
    for ($index = 0; $index -lt $files.Count; $index++) {
        $column = $index % $columns
        $row = [Math]::Floor($index / $columns)
        $originX = $column * $cellWidth
        $originY = $row * $cellHeight
        $contentY = $originY + $labelHeight
        $contentHeight = $cellHeight - $labelHeight

        for ($y = $contentY; $y -lt ($originY + $cellHeight); $y += 24) {
            for ($x = $originX; $x -lt ($originX + $cellWidth); $x += 24) {
                $brush = if ((([Math]::Floor(($x - $originX) / 24) + [Math]::Floor(($y - $contentY) / 24)) % 2) -eq 0) { $checkerA } else { $checkerB }
                $graphics.FillRectangle($brush, $x, $y, 24, 24)
            }
        }

        $image = [System.Drawing.Image]::FromFile($files[$index].FullName)
        try {
            $scale = [Math]::Min(($cellWidth - 24) / $image.Width, ($contentHeight - 24) / $image.Height)
            $drawWidth = [Math]::Max(1, [Math]::Round($image.Width * $scale))
            $drawHeight = [Math]::Max(1, [Math]::Round($image.Height * $scale))
            $drawX = $originX + [Math]::Floor(($cellWidth - $drawWidth) / 2)
            $drawY = $contentY + [Math]::Floor(($contentHeight - $drawHeight) / 2)
            $graphics.DrawImage($image, $drawX, $drawY, $drawWidth, $drawHeight)
            $label = "$($files[$index].Name)  [$($image.Width)x$($image.Height)]"
            $graphics.DrawString($label, $font, $textBrush, $originX + 8, $originY + 10)
        }
        finally {
            $image.Dispose()
        }
    }

    $sheet.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $output
}
finally {
    $checkerA.Dispose()
    $checkerB.Dispose()
    $textBrush.Dispose()
    $font.Dispose()
    $graphics.Dispose()
    $sheet.Dispose()
}
