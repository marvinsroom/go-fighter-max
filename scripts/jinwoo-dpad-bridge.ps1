param([int]$GameProcessId, [string]$LogPath='')
$ErrorActionPreference='SilentlyContinue'
function Write-BridgeLog([string]$Message) {
 if($LogPath){ Add-Content -LiteralPath $LogPath -Value "$(Get-Date -Format 'HH:mm:ss.fff') $Message" }
}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class JinwooPad {
 [StructLayout(LayoutKind.Sequential)] public struct Gamepad { public ushort Buttons; public byte LT,RT; public short LX,LY,RX,RY; }
 [StructLayout(LayoutKind.Sequential)] public struct State { public uint Packet; public Gamepad Pad; }
 [DllImport("xinput1_4.dll")] public static extern uint XInputGetState(uint index, out State state);
 [DllImport("user32.dll")] public static extern void keybd_event(byte key, byte scan, uint flags, UIntPtr extra);
 public static void Key(byte scan, bool down) { keybd_event(0, scan, down ? 8u : 10u, UIntPtr.Zero); }
}
'@
$last=0
$connected=$false
$lastAcceptedPress=[DateTime]::MinValue
$lastButtons=0
$rightStickDirection='neutral'
function Send-Key([byte]$Scan) {
 [JinwooPad]::Key($Scan,$true)
 Start-Sleep -Milliseconds 150
 [JinwooPad]::Key($Scan,$false)
}
function Send-Triple([byte]$First,[byte]$Second,[byte]$Third) {
 [JinwooPad]::Key($First,$true); [JinwooPad]::Key($Second,$true); [JinwooPad]::Key($Third,$true)
 Start-Sleep -Milliseconds 150
 [JinwooPad]::Key($Third,$false); [JinwooPad]::Key($Second,$false); [JinwooPad]::Key($First,$false)
}
function Send-Chord([byte]$First,[byte]$Second) {
 [JinwooPad]::Key($First,$true); [JinwooPad]::Key($Second,$true)
 Start-Sleep -Milliseconds 150
 [JinwooPad]::Key($Second,$false); [JinwooPad]::Key($First,$false)
}
$padIndex=-1
Write-BridgeLog "Bridge started for game PID $GameProcessId"
while(Get-Process -Id $GameProcessId -ErrorAction SilentlyContinue){
 $state=New-Object JinwooPad+State
 $found=$false
 $start=if($padIndex -ge 0){$padIndex}else{0}
 $end=if($padIndex -ge 0){$padIndex}else{3}
 for($i=$start; $i -le $end; $i++){
  if([JinwooPad]::XInputGetState([uint32]$i,[ref]$state)-eq 0){
   if($padIndex -ne $i){
    $padIndex=$i
    $connected=$true
    Write-BridgeLog "Xbox controller connected on XInput index $i"
   }
   $found=$true
   break
  }
 }
 if($found){
  $buttons=$state.Pad.Buttons
  $pad=$buttons -band 15
  $pressed=$pad -band (-bnot $last)
  # Hardware scan codes: F=21, G=22, H=23, R=13; Q=10.
  # SDL/IKEMEN reads these reliably, unlike injected virtual-key events.
  $key=if($pressed -band 1){0x21}elseif($pressed -band 8){0x22}elseif($pressed -band 4){0x23}elseif($pressed -band 2){0x13}else{0}
  $elapsed=((Get-Date)-$lastAcceptedPress).TotalMilliseconds
  $summonModifier=$state.Pad.LT -gt 80
  $transformModifier=$state.Pad.RT -gt 80
  if($key -and $transformModifier -and $elapsed -ge 350 -and ($key-eq 0x21 -or $key-eq 0x22)){
   $lastAcceptedPress=Get-Date
   if($key-eq 0x21){
    Write-BridgeLog 'RT + D-pad up / transform Kaisel dragon'
    Send-Triple 0x21 0x23 0x13
   } else {
    Write-BridgeLog 'RT + D-pad right / transform Tusk'
    Send-Triple 0x22 0x23 0x13
   }
  } elseif($key -and $summonModifier -and $elapsed -ge 350 -and ($key-eq 0x21 -or $key-eq 0x22)){
   $lastAcceptedPress=Get-Date
   if($key-eq 0x21){
    Write-BridgeLog 'LT + D-pad up / summon Kaisel dragon'
    Send-Chord 0x12 0x21
   } else {
    Write-BridgeLog 'LT + D-pad right / summon Tusk'
    Send-Chord 0x12 0x22
   }
  } elseif($key -and $elapsed -ge 700){
   $lastAcceptedPress=Get-Date
   $direction=if($key-eq 0x21){'Up / Igris'}elseif($key-eq 0x22){'Right / Beru'}elseif($key-eq 0x23){'Left / Iron'}else{'Down / Tank'}
   Write-BridgeLog "D-pad $direction"
   Send-Chord 0x10 ([byte]$key)
  } elseif($key) {
   Write-BridgeLog "Ignored duplicate D-pad edge after $([int]$elapsed) ms"
  }
  $last=$pad

  $newDirection=if($state.Pad.RY -gt 16000){'up'}elseif($state.Pad.RY -lt -16000){'down'}elseif($state.Pad.RX -lt -16000){'left'}elseif($state.Pad.RX -gt 16000){'right'}else{'neutral'}
  if($newDirection-ne 'neutral' -and $newDirection-ne $rightStickDirection){
   switch($newDirection){
    'up'    { Write-BridgeLog 'Right stick up / Mutilate'; Send-Key 0x15 }
    # E+T = logical w+y (pad_monarch); E+Y = logical w+z (pad_spoiler).
    'left'  { Write-BridgeLog 'Right stick left / Monarch Domain'; Send-Chord 0x12 0x14 }
    'right' { Write-BridgeLog 'Right stick right / Spoiler Skill'; Send-Chord 0x12 0x15 }
    'down'  { Write-BridgeLog 'Right stick down / sword change'; Send-Chord 0x1F 0x14 }
   }
  }
  $rightStickDirection=$newDirection

  $newButtonPress=$buttons -band (-bnot $lastButtons)
  if($newButtonPress -band 0x0080){
   Write-BridgeLog 'R3 / Skill 11 (logical d+w)'; Send-Chord 0x10 0x12
  }
  if($newButtonPress -band 0x0040){
   Write-BridgeLog 'L3 / Skill 12 (logical d+y)'; Send-Chord 0x10 0x14
  }
  $lastButtons=$buttons
 } elseif($connected) {
  $connected=$false
  $padIndex=-1
  Write-BridgeLog 'Xbox controller disconnected'
 }
 Start-Sleep -Milliseconds 8
}
Write-BridgeLog 'Bridge stopped'
