[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$FoundMark = [char]0x2705
$MissingMark = [char]0x274C
$AllChecksPassed = $true
$ServerReachable = $true

Write-Host "OutcomeIQ API smoke check" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

$Endpoints = @(
    @{ Name = "Root"; Path = "/"; Property = "service"; Expected = "OutcomeIQ API" },
    @{ Name = "Health"; Path = "/api/v1/health"; Property = "status"; Expected = "ok" },
    @{ Name = "Readiness"; Path = "/api/v1/ready"; Property = "status"; Expected = "ready" }
)

foreach ($Endpoint in $Endpoints) {
    $Uri = $BaseUrl.TrimEnd("/") + $Endpoint.Path
    try {
        $Response = Invoke-RestMethod -Uri $Uri -Method Get -TimeoutSec 5
        $ActualValue = $Response.($Endpoint.Property)

        if ($ActualValue -eq $Endpoint.Expected) {
            Write-Host "$FoundMark $($Endpoint.Name): $Uri" -ForegroundColor Green
        }
        else {
            Write-Host "$MissingMark $($Endpoint.Name): unexpected $($Endpoint.Property) value '$ActualValue'" -ForegroundColor Red
            $AllChecksPassed = $false
        }
    }
    catch {
        Write-Host "$MissingMark $($Endpoint.Name): $Uri" -ForegroundColor Red
        Write-Host "   $($_.Exception.Message)" -ForegroundColor DarkYellow
        $AllChecksPassed = $false
        $ServerReachable = $false
    }
}

if (-not $ServerReachable) {
    Write-Host "The API server may not be running." -ForegroundColor Yellow
    Write-Host "Start it in another PowerShell window with: .\scripts\run_backend.ps1" -ForegroundColor Yellow
}

if ($AllChecksPassed) {
    Write-Host "API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "API SMOKE CHECK FAILED" -ForegroundColor Red
exit 1
