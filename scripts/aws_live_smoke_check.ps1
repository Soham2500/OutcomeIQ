[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BackendUrl,

    [Parameter(Mandatory = $true)]
    [string]$FrontendUrl
)

$ErrorActionPreference = "Stop"
$BackendUrl = $BackendUrl.TrimEnd("/")
$FrontendUrl = $FrontendUrl.TrimEnd("/")
$Passed = $true

function Test-Url {
    param(
        [string]$Label,
        [string]$Url
    )

    try {
        $Response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec 20 -ErrorAction Stop
        Write-Host "[PASS] $Label returned HTTP $($Response.StatusCode)" -ForegroundColor Green
    }
    catch {
        $script:Passed = $false
        Write-Host "[FAIL] $Label failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "OutcomeIQ AWS live smoke check" -ForegroundColor Cyan
Write-Host "This script checks public surfaces only. It does not login, mutate data, or call payment endpoints." -ForegroundColor DarkCyan

Test-Url -Label "Backend health" -Url "$BackendUrl/api/v1/health"
Test-Url -Label "Backend readiness" -Url "$BackendUrl/api/v1/ready"
Test-Url -Label "Frontend homepage" -Url $FrontendUrl

if ($Passed) {
    Write-Host "AWS LIVE SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "AWS LIVE SMOKE CHECK FAILED" -ForegroundColor Red
exit 1
