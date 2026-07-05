[CmdletBinding()]
param(
    [string]$BackendBaseUrl,

    [string]$FrontendBaseUrl
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

if ([string]::IsNullOrWhiteSpace($BackendBaseUrl)) {
    Write-Host "PRODUCTION SMOKE CHECK FAILED" -ForegroundColor Red
    Write-Host "Reason: BackendBaseUrl is required." -ForegroundColor Yellow
    exit 1
}
if ([string]::IsNullOrWhiteSpace($FrontendBaseUrl)) {
    Write-Host "PRODUCTION SMOKE CHECK FAILED" -ForegroundColor Red
    Write-Host "Reason: FrontendBaseUrl is required." -ForegroundColor Yellow
    exit 1
}

$BackendBaseUrl = $BackendBaseUrl.Trim().TrimEnd("/")
$FrontendBaseUrl = $FrontendBaseUrl.Trim().TrimEnd("/")
$Succeeded = $false

function Test-PublicEndpoint {
    param(
        [string]$Name,
        [string]$Uri,
        [string]$ServiceName
    )

    try {
        $Response = Invoke-WebRequest `
            -Method Get `
            -Uri $Uri `
            -TimeoutSec 20 `
            -UseBasicParsing

        $StatusCode = [int]$Response.StatusCode
        if ($StatusCode -lt 200 -or $StatusCode -ge 400) {
            throw "$Name returned HTTP $StatusCode."
        }

        Write-Host "${Name}: HTTP $StatusCode" -ForegroundColor Green
    }
    catch {
        $StatusCode = $null
        if ($null -ne $_.Exception.Response) {
            try {
                $StatusCode = [int]$_.Exception.Response.StatusCode
            }
            catch {
                $StatusCode = $null
            }
        }

        if ($null -ne $StatusCode) {
            throw "$Name failed with HTTP $StatusCode."
        }

        throw "$ServiceName is unreachable. Verify its public URL and deployment status."
    }
}

Write-Host "OutcomeIQ production smoke check" -ForegroundColor Cyan

try {
    Test-PublicEndpoint `
        -Name "Backend health" `
        -Uri "$BackendBaseUrl/api/v1/health" `
        -ServiceName "Backend"
    Test-PublicEndpoint `
        -Name "Backend docs" `
        -Uri "$BackendBaseUrl/docs" `
        -ServiceName "Backend"
    Test-PublicEndpoint `
        -Name "Frontend homepage" `
        -Uri $FrontendBaseUrl `
        -ServiceName "Frontend"

    $Succeeded = $true
}
catch {
    Write-Host "PRODUCTION SMOKE CHECK FAILED" -ForegroundColor Red
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor Yellow
}

if ($Succeeded) {
    Write-Host "PRODUCTION SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}

exit 1
