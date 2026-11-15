param(
    [string]$Root = "C:\Users\15168\Development\Vs-Fighter\go-fighter-max\sprite-fighter\characters\jinwoo-mugen\art\naruto-style-v2\loco-final-v32"
)

Add-Type -AssemblyName System.Drawing

$source = Join-Path $Root "runtime-preview"
$output = Join-Path $Root "antares-runtime-review-v32.png"
$files = Get-ChildItem -LiteralPath $source -Filter "Jinwoo_Antares_v32*.png" | Sort-Object Name
if ($files.Count -ne 10) { throw "Expected 10 runtime captures; found $($files.Count)" }

$columns = 2
$cellWidth = 640
$cellHeight = 400
$labelHeight = 34
$rows = [Math]::Ceiling($files.Count / $columns)
$sheet = [System.Drawing.Bitmap]::new($columns * $cellWidth, $rows * $cellHeight)
$graphics = [System.Drawing.Graphics]::FromImage($sheet)
$font = [System.Drawing.Font]::new("Segoe UI", 12, [System.Drawing.FontStyle]::Regular)
$textBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
try {
    $graphics.Clear([System.Drawing.Color]::FromArgb(255, 16, 16, 22))
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    for ($index = 0; $index -lt $files.Count; $index++) {
        $column = $index % $columns
        $row = [Math]::Floor($index / $columns)
        $originX = $column * $cellWidth
        $originY = $row * $cellHeight
        $image = [System.Drawing.Image]::FromFile($files[$index].FullName)
        try {
            $scale = [Math]::Min($cellWidth / $image.Width, ($cellHeight - $labelHeight) / $image.Height)
            $drawWidth = [Math]::Round($image.Width * $scale)
            $drawHeight = [Math]::Round($image.Height * $scale)
            $drawX = $originX + [Math]::Floor(($cellWidth - $drawWidth) / 2)
            $drawY = $originY + $labelHeight + [Math]::Floor((($cellHeight - $labelHeight) - $drawHeight) / 2)
            $graphics.DrawImage($image, $drawX, $drawY, $drawWidth, $drawHeight)
            $graphics.DrawString("Checkpoint $index - $($files[$index].Name)", $font, $textBrush, $originX + 8, $originY + 7)
        }
        finally {
            $image.Dispose()
        }
    }
    $sheet.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output $output
}
finally {
    $textBrush.Dispose()
    $font.Dispose()
    $graphics.Dispose()
    $sheet.Dispose()
}
