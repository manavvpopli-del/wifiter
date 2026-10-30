<#
.SYNOPSIS
  Colorful simulated Wi-Fi scanner demo for Windows PowerShell.
.DESCRIPTION
  Shows fictional networks by default. Use -Live to list networks reported by
  Windows WLAN. This tool is read-only and does not connect to networks.
#>
[CmdletBinding()]
param(
    [switch]$Live,
    [switch]$Json,
    [string]$Csv,
    [ValidateRange(1, 86400)]
    [int]$Watch = 0,
    [switch]$NoAnimation
)

$ErrorActionPreference = 'Stop'

function Get-DemoNetworks {
    @(
        [pscustomobject]@{ SSID = 'VK_5G';              BSSID = '02:5A:11:00:00:01'; Channel = 44; SignalPercent = 92; Band = '5 GHz';   Security = 'WPA2-Personal'; Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = 'Dragon_Network';     BSSID = '02:5A:11:00:00:02'; Channel =  6; SignalPercent = 84; Band = '2.4 GHz'; Security = 'WPA3-Personal'; Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = 'Kali_Lab';           BSSID = '02:5A:11:00:00:03'; Channel = 11; SignalPercent = 71; Band = '2.4 GHz'; Security = 'WPA2-Personal'; Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = 'Cafe_Demo';          BSSID = '02:5A:11:00:00:04'; Channel = 36; SignalPercent = 63; Band = '5 GHz';   Security = 'Open';          Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = 'Guest_WiFi';         BSSID = '02:5A:11:00:00:05'; Channel =  1; SignalPercent = 48; Band = '2.4 GHz'; Security = 'WPA2-Personal'; Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = 'IoT_2.4G';           BSSID = '02:5A:11:00:00:06'; Channel =  3; SignalPercent = 37; Band = '2.4 GHz'; Security = 'WPA2-Personal'; Status = 'SIMULATED' }
        [pscustomobject]@{ SSID = '<hidden SSID demo>'; BSSID = '02:5A:11:00:00:07'; Channel =149; SignalPercent = 25; Band = '5 GHz';   Security = 'WPA2-Personal'; Status = 'SIMULATED' }
    )
}

function Get-LiveNetworks {
    $raw = @(& netsh.exe wlan show networks mode=bssid 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw (($raw | ForEach-Object { "$_" }) -join [Environment]::NewLine)
    }

    $networks = [System.Collections.Generic.List[object]]::new()
    $ssid = ''
    $authentication = ''
    $encryption = ''
    $current = $null
    foreach ($lineObject in $raw) {
        $line = [string]$lineObject
        if ($line -match '^\s*SSID\s+\d+\s*:\s*(.*)$') {
            $ssid = $Matches[1].Trim()
            if (-not $ssid) { $ssid = '<hidden SSID>' }
            $authentication = ''
            $encryption = ''
            $current = $null
            continue
        }
        if ($line -match '^\s*Authentication\s*:\s*(.*)$') {
            $authentication = $Matches[1].Trim()
            continue
        }
        if ($line -match '^\s*Encryption\s*:\s*(.*)$') {
            $encryption = $Matches[1].Trim()
            continue
        }
        if ($line -match '^\s*BSSID\s+\d+\s*:\s*(\S+)') {
            $current = [pscustomobject]@{
                SSID = $ssid
                BSSID = $Matches[1].ToLowerInvariant()
                Channel = ''
                SignalPercent = ''
                Band = ''
                Security = (@($authentication, $encryption) | Where-Object { $_ }) -join ' / '
                Status = ''
            }
            $networks.Add($current)
            continue
        }
        if ($null -eq $current) { continue }
        if ($line -match '^\s*Signal\s*:\s*(\d+)%') {
            $current.SignalPercent = [int]$Matches[1]
        }
        elseif ($line -match '^\s*Channel\s*:\s*(\d+)') {
            $current.Channel = [int]$Matches[1]
        }
        elseif ($line -match '^\s*Band\s*:\s*(.*)$') {
            $current.Band = $Matches[1].Trim()
        }
        elseif ($line -match '^\s*Radio type\s*:\s*(.*)$' -and -not $current.Band) {
            $current.Band = $Matches[1].Trim()
        }
    }

    $interfaceInfo = @(& netsh.exe wlan show interfaces 2>&1)
    if ($LASTEXITCODE -eq 0) {
        $connectedBssids = @(
            foreach ($lineObject in $interfaceInfo) {
                $line = [string]$lineObject
                if ($line -match '^\s*(?:AP\s+)?BSSID\s*:\s*([0-9a-fA-F:]{17})') {
                    $Matches[1].ToLowerInvariant()
                }
            }
        )
        foreach ($network in $networks) {
            if ($connectedBssids -contains $network.BSSID) { $network.Status = 'CONNECTED' }
        }
    }
    return $networks.ToArray()
}

function Show-DragonAnimation {
    $breaths = @('.', '..', '...', '🔥', '🔥🔥', '🔥🔥🔥')
    foreach ($breath in $breaths) {
        Write-Host ("`r  🐉  " + $breath.PadRight(6) + '  DRAGON SCAN INITIALIZING') -ForegroundColor Magenta -NoNewline
        Start-Sleep -Milliseconds 120
    }
    Write-Host ''
}

function Show-Banner {
    Write-Host ''
    Write-Host '  ╔══════════════════════════════════════════════════════════════════════╗' -ForegroundColor DarkCyan
    Write-Host '  ║   /\_/\\        DRAGON WI-FI SCANNER                         ║' -ForegroundColor Cyan
    Write-Host '  ║  ( o.o )        SCAN • SIMULATE • VISUALIZE                    ║' -ForegroundColor Cyan
    Write-Host '  ║   > ^ <         SAFE READ-ONLY DEMO                            ║' -ForegroundColor Cyan
    Write-Host '  ╚══════════════════════════════════════════════════════════════════════╝' -ForegroundColor DarkCyan
    Write-Host ''
}

function Show-NetworkTable($Networks) {
    $mode = if ($Live) { 'LIVE SCAN' } else { 'SIMULATION — FICTIONAL NETWORKS' }
    $modeColor = if ($Live) { 'Yellow' } else { 'Magenta' }
    Write-Host ("  MODE: {0}" -f $mode) -ForegroundColor $modeColor
    Write-Host ''
    Write-Host ('  {0,-22} {1,-19} {2,4} {3,8} {4,-10} {5,-24} {6,-11}' -f 'SSID', 'BSSID', 'CH', 'SIGNAL', 'BAND', 'SECURITY', 'STATUS') -ForegroundColor White
    Write-Host ('  {0,-22} {1,-19} {2,4} {3,8} {4,-10} {5,-24} {6,-11}' -f ('─' * 22), ('─' * 19), ('─' * 4), ('─' * 8), ('─' * 10), ('─' * 24), ('─' * 11)) -ForegroundColor DarkGray

    foreach ($network in $Networks) {
        $signalColor = if ([int]$network.SignalPercent -ge 70) { 'Green' } elseif ([int]$network.SignalPercent -ge 40) { 'Yellow' } else { 'Red' }
        Write-Host '  ' -NoNewline
        Write-Host ([string]$network.SSID).PadRight(22) -ForegroundColor Cyan -NoNewline
        Write-Host ([string]$network.BSSID).PadRight(20) -ForegroundColor DarkGray -NoNewline
        Write-Host ([string]$network.Channel).PadLeft(4) -ForegroundColor White -NoNewline
        Write-Host (([string]$network.SignalPercent + '%').PadLeft(8)) -ForegroundColor $signalColor -NoNewline
        Write-Host (' ' + ([string]$network.Band).PadRight(10)) -ForegroundColor Blue -NoNewline
        Write-Host ([string]$network.Security).PadRight(25) -ForegroundColor Yellow -NoNewline
        Write-Host ([string]$network.Status).PadRight(11) -ForegroundColor Magenta
    }
    Write-Host ''
    Write-Host ("  TOTAL: {0} network(s)" -f $Networks.Count) -ForegroundColor Green
    if (-not $Live) { Write-Host '  Demo data only — these are not real nearby networks.' -ForegroundColor DarkMagenta }
}

function Invoke-Scanner {
    $networks = if ($Live) { @(Get-LiveNetworks) } else { @(Get-DemoNetworks) }
    if ($Json) {
        [pscustomobject]@{
            Mode = if ($Live) { 'live' } else { 'simulation' }
            ScannedAt = (Get-Date).ToUniversalTime().ToString('o')
            Networks = $networks
        } | ConvertTo-Json -Depth 5
    }
    else {
        if (-not $NoAnimation) { Show-DragonAnimation }
        Show-Banner
        Show-NetworkTable $networks
    }
    if ($Csv) {
        $networks | Export-Csv -Path $Csv -NoTypeInformation -Encoding UTF8
        if (-not $Json) { Write-Host "`n  CSV saved: $Csv" -ForegroundColor Green }
    }
}

try {
    do {
        if ($Watch -gt 0) { Clear-Host }
        Invoke-Scanner
        if ($Watch -gt 0) { Start-Sleep -Seconds $Watch }
    } while ($Watch -gt 0)
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
