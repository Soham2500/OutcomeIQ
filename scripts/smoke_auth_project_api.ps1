[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$TestEmail = "smoke_test_$Timestamp@outcomeiq.local"
$TestPassword = "TestPassword123!"
$OrganizationSlug = "smoke-org-$Timestamp"
$ProjectSlug = "smoke-project-$Timestamp"
$CurrentStep = "health check"

function Get-SafeApiErrorBody {
    param(
        [System.Management.Automation.ErrorRecord]$ErrorRecord,
        [string[]]$SensitiveValues
    )

    $ResponseBody = $ErrorRecord.ErrorDetails.Message
    if ([string]::IsNullOrWhiteSpace($ResponseBody)) {
        $Response = $ErrorRecord.Exception.Response
        try {
            if (
                $null -ne $Response -and
                $null -ne $Response.Content -and
                $null -ne $Response.Content.PSObject.Methods["ReadAsStringAsync"]
            ) {
                $ResponseBody = $Response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
            }
            elseif (
                $null -ne $Response -and
                $null -ne $Response.PSObject.Methods["GetResponseStream"]
            ) {
                $Reader = New-Object System.IO.StreamReader($Response.GetResponseStream())
                try {
                    $ResponseBody = $Reader.ReadToEnd()
                }
                finally {
                    $Reader.Dispose()
                }
            }
        }
        catch {
            $ResponseBody = $null
        }
    }

    if ([string]::IsNullOrWhiteSpace($ResponseBody)) {
        return $null
    }

    foreach ($SensitiveValue in $SensitiveValues) {
        if (-not [string]::IsNullOrWhiteSpace($SensitiveValue)) {
            $ResponseBody = $ResponseBody.Replace($SensitiveValue, "[REDACTED]")
        }
    }
    return $ResponseBody
}

Write-Host "OutcomeIQ auth/project API smoke check" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

try {
    $Health = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($Health.status -ne "ok") {
        throw "Health endpoint returned an unexpected status."
    }

    $CurrentStep = "user registration"
    $RegisterBody = @{
        email = $TestEmail
        full_name = "Smoke Test User"
        password = $TestPassword
    } | ConvertTo-Json
    $RegisteredUser = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $RegisterBody `
        -TimeoutSec 15

    $CurrentStep = "user login"
    $LoginBody = @{
        email = $TestEmail
        password = $TestPassword
    } | ConvertTo-Json
    $Login = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/auth/login" `
        -Method Post `
        -ContentType "application/json" `
        -Body $LoginBody `
        -TimeoutSec 15
    if ([string]::IsNullOrWhiteSpace($Login.access_token)) {
        throw "Login did not return an access token."
    }
    $Headers = @{ Authorization = "Bearer $($Login.access_token)" }

    $CurrentStep = "current-user lookup"
    $CurrentUser = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/auth/me" `
        -Method Get `
        -Headers $Headers `
        -TimeoutSec 10
    if ($CurrentUser.id -ne $RegisteredUser.id) {
        throw "Current-user response did not match the registered user."
    }

    $CurrentStep = "organization creation"
    $OrganizationBody = @{
        name = "API Smoke Organization $Timestamp"
        slug = $OrganizationSlug
    } | ConvertTo-Json
    $Organization = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/organizations" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $OrganizationBody `
        -TimeoutSec 15

    $CurrentStep = "project creation"
    $ProjectBody = @{
        organization_id = $Organization.id
        name = "API Smoke Project $Timestamp"
        slug = $ProjectSlug
        description = "Synthetic local smoke-test project"
    } | ConvertTo-Json
    $Project = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/projects" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $ProjectBody `
        -TimeoutSec 15

    $CurrentStep = "project listing"
    $Projects = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/projects?organization_id=$($Organization.id)" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 10
    )
    if ($Project.id -notin $Projects.id) {
        throw "Created project was not returned by the member-scoped project list."
    }

    $CurrentStep = "project member listing"
    $Members = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/projects/$($Project.id)/members" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 10
    )
    $Owner = $Members | Where-Object {
        $_.user_id -eq $RegisteredUser.id -and $_.role -eq "owner"
    }
    if ($null -eq $Owner) {
        throw "Project owner membership was not found."
    }

    Write-Host "AUTH PROJECT API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "AUTH PROJECT API SMOKE CHECK FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
    $SensitiveValues = @($TestPassword)
    if ($null -ne $Login -and -not [string]::IsNullOrWhiteSpace($Login.access_token)) {
        $SensitiveValues += $Login.access_token
    }
    $SafeResponseBody = Get-SafeApiErrorBody `
        -ErrorRecord $_ `
        -SensitiveValues $SensitiveValues
    if (-not [string]::IsNullOrWhiteSpace($SafeResponseBody)) {
        Write-Host "Response body: $SafeResponseBody" -ForegroundColor DarkYellow
    }
    Write-Host "Start the backend first with: .\scripts\run_backend.ps1" -ForegroundColor Yellow
    exit 1
}
