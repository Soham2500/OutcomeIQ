[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BackendUrl,

    [Parameter(Mandatory = $true)]
    [string]$FrontendUrl
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$BackendUrl = $BackendUrl.Trim().TrimEnd("/")
$FrontendUrl = $FrontendUrl.Trim().TrimEnd("/")
$Succeeded = $true

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Uri,
        [int[]]$AllowedStatusCodes = @(200)
    )

    try {
        $Response = Invoke-WebRequest `
            -Method Get `
            -Uri $Uri `
            -TimeoutSec 25 `
            -UseBasicParsing
        $StatusCode = [int]$Response.StatusCode
        if ($StatusCode -notin $AllowedStatusCodes) {
            throw "$Name returned HTTP $StatusCode."
        }
        Write-Host "${Name}: HTTP $StatusCode" -ForegroundColor Green
    }
    catch {
        Write-Host "${Name}: FAILED" -ForegroundColor Red
        Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor Yellow
        $script:Succeeded = $false
    }
}

Write-Host "OutcomeIQ live smoke check" -ForegroundColor Cyan
Write-Host "Backend: $BackendUrl"
Write-Host "Frontend: $FrontendUrl"

Test-Endpoint -Name "Backend health" -Uri "$BackendUrl/api/v1/health"
Test-Endpoint -Name "Backend ready" -Uri "$BackendUrl/api/v1/ready" -AllowedStatusCodes @(200, 503)
Test-Endpoint -Name "Frontend homepage" -Uri $FrontendUrl

if ($Succeeded) {
    Write-Host "LIVE SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "LIVE SMOKE CHECK FAILED" -ForegroundColor Red
exit 1
