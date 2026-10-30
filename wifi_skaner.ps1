<#
.SYNOPSIS
  Read-only nearby Wi-Fi scanner for Windows.
.DESCRIPTION
  Uses Windows' built-in netsh WLAN commands. It does not connect to networks,
  capture traffic, inject packets, or attempt to recover passwords.
#>
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$Csv,
    [ValidateRange(1, 86400)]
    [int]$Watch = 0
)

$ErrorActionPreference = 'Stop'

function Get-WifiNetworks {
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
                SSID           = $ssid
                BSSID          = $Matches[1].ToLowerInvariant()
                Channel        = ''
                SignalPercent  = ''
                RadioType      = ''
                Authentication = $authentication
                Encryption     = $encryption
                InUse          = $false
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
        elseif ($line -match '^\s*Radio type\s*:\s*(.*)$') {
            $current.RadioType = $Matches[1].Trim()
        }
    }

    # Mark the currently connected access point, when there is one.
    $interfaceInfo = @(& netsh.exe wlan show interfaces 2>&1)
    if ($LASTEXITCODE -eq 0) {
        $connectedBssids = @(
            foreach ($lineObject in $interfaceInfo) {
                $line = [string]$lineObject
                if ($line -match '^\s*BSSID\s*:\s*([0-9a-fA-F:]{17})') {
                    $Matches[1].ToLowerInvariant()
                }
            }
        )
        foreach ($network in $networks) {
            if ($connectedBssids -contains $network.BSSID) {
                $network.InUse = $true
            }
        }
    }
    return $networks.ToArray()
}

function Show-WifiNetworks {
    $networks = @(Get-WifiNetworks)
    if ($Json) {
        [pscustomobject]@{
            ScannedAt = (Get-Date).ToUniversalTime().ToString('o')
            Networks  = $networks
        } | ConvertTo-Json -Depth 5
    }
    else {
        if ($networks.Count -gt 0) {
            $networks |
                Sort-Object @{ Expression = { [int]$_.SignalPercent }; Descending = $true } |
                Format-Table SSID, BSSID, Channel, SignalPercent, RadioType, Authentication, Encryption, InUse -AutoSize |
                Out-Host
        }
        else {
            Write-Host 'No Wi-Fi networks found. Check that the Wi-Fi adapter is enabled and in range.'
        }
        Write-Host ("Total: {0} network(s)" -f $networks.Count)
    }
    if ($Csv) {
        $networks | Export-Csv -Path $Csv -NoTypeInformation -Encoding UTF8
        if (-not $Json) { Write-Host "CSV saved: $Csv" }
    }
}

try {
    do {
        if ($Watch -gt 0) { Clear-Host }
        Show-WifiNetworks
        if ($Watch -gt 0) { Start-Sleep -Seconds $Watch }
    } while ($Watch -gt 0)
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
