"""Create Yamal-specific window capture helpers without editing other fighters."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts'
inspect=(S/'inspect-ikemen-window.ps1').read_text()
inspect=inspect.replace("$game=Get-Process -Name Ikemen_GO | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1", "$game=Get-Process -Id ([int](Get-Content (Join-Path $PSScriptRoot '../sprite-fighter/yamal-process.txt'))) -ErrorAction Stop")
inspect=inspect.replace("../sprite-fighter/ikemen-preview.png","../sprite-fighter/characters/yamal/engine-preview.png")
inspect=inspect.replace("../sprite-fighter/ikemen-held.png","../sprite-fighter/characters/yamal/engine-held.png")
(S/'inspect-yamal-window.ps1').write_text(inspect,encoding='utf-8')
record=(S/'record-urkel-move.ps1').read_text().replace("[ValidateSet('Robot','Gadget','Stefan')]","[ValidateSet('Ultimate','Super')]").replace("$Move='Robot'","$Move='Ultimate'")
record=record.replace('inspect-ikemen-window','inspect-yamal-window').replace('characters/urkel','characters/yamal').replace("'Gadget'","'Super'")
record=record.replace('{30}else{48}','{52}else{92}')
(S/'record-yamal-move.ps1').write_text(record,encoding='utf-8')
print('YAMAL_PREVIEW_HELPERS_READY')
