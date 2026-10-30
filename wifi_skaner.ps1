<#
.SYNOPSIS
  Offline Wi-Fi security simulation for Windows PowerShell.
.DESCRIPTION
  Displays fictional access points and plays a harmless, simulated attack flow.
  It does not scan, connect to, attack, or recover passwords from Wi-Fi networks.
#>
[CmdletBinding()]
param(
    [switch]$NoAnimation,
    [ValidateRange(1, 5000)]
    [int]$DelayMilliseconds = 220
)

$ErrorActionPreference = 'Stop'

$networks = @(
    [pscustomobject]@{ SSID = 'HomeNetwork_5G';      BSSID = '02:5A:11:00:00:01'; Channel = 44; Signal = 92; Band = '5 GHz';   Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0001' }
    [pscustomobject]@{ SSID = 'TPLink_A47C';         BSSID = '02:5A:11:00:00:02'; Channel =  6; Signal = 84; Band = '2.4 GHz'; Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0002' }
    [pscustomobject]@{ SSID = 'ASUS_2.4GHz';         BSSID = '02:5A:11:00:00:03'; Channel = 11; Signal = 77; Band = '2.4 GHz'; Security = 'WPA3-Personal'; FakeKey = 'FICTIONAL-KEY-0003' }
    [pscustomobject]@{ SSID = 'NETGEAR_EXT';         BSSID = '02:5A:11:00:00:04'; Channel = 36; Signal = 69; Band = '5 GHz';   Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0004' }
    [pscustomobject]@{ SSID = 'DIRECT-8C-HP-Office'; BSSID = '02:5A:11:00:00:05'; Channel =  1; Signal = 61; Band = '2.4 GHz'; Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0005' }
    [pscustomobject]@{ SSID = 'Apartment_WiFi';      BSSID = '02:5A:11:00:00:06'; Channel =  9; Signal = 55; Band = '2.4 GHz'; Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0006' }
    [pscustomobject]@{ SSID = 'Home-Guest';          BSSID = '02:5A:11:00:00:07'; Channel = 40; Signal = 48; Band = '5 GHz';   Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0007' }
    [pscustomobject]@{ SSID = 'Router_5G_91B2';      BSSID = '02:5A:11:00:00:08'; Channel = 48; Signal = 42; Band = '5 GHz';   Security = 'WPA3-Personal'; FakeKey = 'FICTIONAL-KEY-0008' }
    [pscustomobject]@{ SSID = 'Pixel_Hotspot';       BSSID = '02:5A:11:00:00:09'; Channel =  6; Signal = 35; Band = '2.4 GHz'; Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0009' }
    [pscustomobject]@{ SSID = 'Linksys_2G';          BSSID = '02:5A:11:00:00:0A'; Channel =  3; Signal = 28; Band = '2.4 GHz'; Security = 'WPA2-Personal'; FakeKey = 'FICTIONAL-KEY-0010' }
)

function Show-DragonAnimation {
    $breaths = @('.', '..', '...', '🔥', '🔥🔥', '🔥🔥🔥')
    foreach ($breath in $breaths) {
        Write-Host ("`r  🐉  " + $breath.PadRight(6) + '  SCANNING THE SIMULATED AIRWAVES') -ForegroundColor Magenta -NoNewline
        Start-Sleep -Milliseconds $DelayMilliseconds
    }
    Write-Host ''
}

function Show-Banner {
    Write-Host ''
    Write-Host '  ╔══════════════════════════════════════════════════════════════════════╗' -ForegroundColor DarkCyan
    Write-Host '  ║   /\_/\\        DRAGON WI-FI SECURITY LAB                     ║' -ForegroundColor Cyan
    Write-Host '  ║  ( o.o )        OFFLINE SIMULATION • NO RADIO ACTIONS            ║' -ForegroundColor Cyan
    Write-Host '  ║   > ^ <         FICTIONAL NETWORKS AND KEYS                      ║' -ForegroundColor Cyan
    Write-Host '  ╚══════════════════════════════════════════════════════════════════════╝' -ForegroundColor DarkCyan
    Write-Host ''
}

function Show-NetworkTable {
    Write-Host ('  {0,2} {1,-23} {2,-19} {3,4} {4,8} {5,-10} {6,-20}' -f '#', 'SSID', 'BSSID', 'CH', 'SIGNAL', 'BAND', 'SECURITY') -ForegroundColor White
    Write-Host ('  {0,2} {1,-23} {2,-19} {3,4} {4,8} {5,-10} {6,-20}' -f '--', ('─' * 23), ('─' * 19), ('─' * 4), ('─' * 8), ('─' * 10), ('─' * 20)) -ForegroundColor DarkGray
    for ($i = 0; $i -lt $networks.Count; $i++) {
        $n = $networks[$i]
        $signalColor = if ($n.Signal -ge 70) { 'Green' } elseif ($n.Signal -ge 40) { 'Yellow' } else { 'Red' }
        Write-Host ('  {0,2} ' -f ($i + 1)) -ForegroundColor Magenta -NoNewline
        Write-Host (([string]$n.SSID).PadRight(24)) -ForegroundColor Cyan -NoNewline
        Write-Host (([string]$n.BSSID).PadRight(20)) -ForegroundColor DarkGray -NoNewline
        Write-Host ([string]$n.Channel).PadLeft(4) -ForegroundColor White -NoNewline
        Write-Host (([string]$n.Signal + '%').PadLeft(8)) -ForegroundColor $signalColor -NoNewline
        Write-Host (' ' + ([string]$n.Band).PadRight(10)) -ForegroundColor Blue -NoNewline
        Write-Host (([string]$n.Security).PadRight(20)) -ForegroundColor Yellow
    }
    Write-Host ''
    Write-Host ("  {0} fictional access points" -f $networks.Count) -ForegroundColor Green
}

function Invoke-FakeAttack($Network, [int]$Number) {
    Write-Host ''
    Write-Host ("  Target selected: [{0}] {1}" -f $Number, $Network.SSID) -ForegroundColor Cyan
    Write-Host '  Starting a pretend handshake capture...' -ForegroundColor DarkCyan
    foreach ($percent in @(12, 29, 47, 68, 86, 100)) {
        $filled = [Math]::Floor($percent / 5)
        $bar = ('█' * $filled).PadRight(20, '░')
        Write-Host ("`r  [{0}] {1,3}%  Simulated process" -f $bar, $percent) -ForegroundColor Green -NoNewline
        Start-Sleep -Milliseconds $DelayMilliseconds
    }
    Write-Host ''
    Write-Host '  Pretend attack complete.' -ForegroundColor Green
    Write-Host ("  Fictional key: {0}" -f $Network.FakeKey) -ForegroundColor Yellow
    Write-Host '  This key is fabricated; no real network or password was accessed.' -ForegroundColor DarkGray
}

if (-not $NoAnimation) { Show-DragonAnimation }
Show-Banner
Show-NetworkTable

while ($true) {
    $choice = Read-Host 'Enter a number (1-10) to run the simulation, or Q to quit'
    if ($choice -match '^[Qq]$') { break }
    if ($choice -notmatch '^\d+$' -or [int]$choice -lt 1 -or [int]$choice -gt $networks.Count) {
        Write-Host ("  Choose a number from 1 to {0}, or Q." -f $networks.Count) -ForegroundColor Red
        continue
    }
    $number = [int]$choice
    Invoke-FakeAttack -Network $networks[$number - 1] -Number $number
}

Write-Host '  Session ended. No Wi-Fi activity was performed.' -ForegroundColor DarkCyan
