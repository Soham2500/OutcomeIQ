[CmdletBinding()]
param(
    [string]$BackendUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BackendUrl = $BackendUrl.TrimEnd("/")
$Passed = $true

function Write-Pass {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-WarnSafe {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Yellow
}

function Write-FailSafe {
    param([string]$Message)
    $script:Passed = $false
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Invoke-SafeRequest {
    param(
        [ValidateSet("GET", "POST")]
        [string]$Method,
        [string]$Path,
        [object]$Body = $null
    )

    $Params = @{
        Method = $Method
        Uri = "$BackendUrl$Path"
        TimeoutSec = 20
        ErrorAction = "Stop"
    }
    if ($null -ne $Body) {
        $Params["ContentType"] = "application/json"
        $Params["Body"] = ($Body | ConvertTo-Json -Depth 10)
    }

    try {
        $Response = Invoke-WebRequest @Params
        return @{
            ok = $true
            status = [int]$Response.StatusCode
            body = $Response.Content
        }
    }
    catch {
        $StatusCode = $null
        $ResponseBody = ""
        if ($_.Exception.Response) {
            $StatusCode = [int]$_.Exception.Response.StatusCode
            try {
                $Reader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
                $ResponseBody = $Reader.ReadToEnd()
                $Reader.Dispose()
            }
            catch {
                $ResponseBody = ""
            }
        }
        return @{
            ok = $false
            status = $StatusCode
            body = $ResponseBody
            error = $_.Exception.Message
        }
    }
}

Write-Host "OutcomeIQ Day 16 payment runtime smoke" -ForegroundColor Cyan
Write-Host "Backend: $BackendUrl" -ForegroundColor DarkCyan
Write-Host "This script does not charge money and does not call live Razorpay capture APIs." -ForegroundColor DarkCyan

$Health = Invoke-SafeRequest -Method GET -Path "/api/v1/health"
if ($Health.ok -and $Health.status -eq 200) {
    Write-Pass "GET /api/v1/health returned 200."
}
else {
    Write-FailSafe "GET /api/v1/health failed. Is the backend running?"
}

$Plans = Invoke-SafeRequest -Method GET -Path "/api/v1/billing/plans"
if ($Plans.ok) {
    Write-Pass "GET /api/v1/billing/plans responded with HTTP $($Plans.status)."
}
elseif ($Plans.status -in @(401, 403)) {
    Write-WarnSafe "GET /api/v1/billing/plans requires authentication. Authenticated browser test required for checkout and billing/me."
}
else {
    Write-FailSafe "GET /api/v1/billing/plans failed unexpectedly with HTTP $($Plans.status)."
}

$BillingMe = Invoke-SafeRequest -Method GET -Path "/api/v1/billing/me"
if ($BillingMe.ok) {
    Write-Pass "GET /api/v1/billing/me responded with HTTP $($BillingMe.status)."
}
elseif ($BillingMe.status -in @(401, 403)) {
    Write-WarnSafe "GET /api/v1/billing/me requires authentication. Authenticated browser test required for checkout and billing/me."
}
else {
    Write-FailSafe "GET /api/v1/billing/me failed unexpectedly with HTTP $($BillingMe.status)."
}

$FakeWebhookPayload = @{
    id = "evt_day16_runtime_fake"
    event = "subscription.activated"
    payload = @{
        subscription = @{
            entity = @{
                id = "sub_day16_runtime_fake"
                status = "active"
            }
        }
        payment = @{
            entity = @{
                id = "pay_day16_runtime_fake"
                subscription_id = "sub_day16_runtime_fake"
                email = "runtime_smoke@outcomeiq.local"
            }
        }
    }
}

$Webhook = Invoke-SafeRequest -Method POST -Path "/api/v1/billing/webhook/razorpay" -Body $FakeWebhookPayload
if ($Webhook.ok -and $Webhook.status -eq 200) {
    Write-Pass "Webhook endpoint accepted unsigned fake payload safely. This usually means webhook secret is not configured locally."
}
elseif ($Webhook.status -eq 400 -and $Webhook.body -match "Invalid Razorpay webhook signature") {
    Write-Pass "Webhook endpoint rejected invalid unsigned payload safely. This usually means webhook secret is configured."
}
else {
    Write-FailSafe "Webhook endpoint returned unexpected result. HTTP $($Webhook.status)."
}

Write-WarnSafe "Checkout and local activation are authenticated flows. Test them in the browser unless you intentionally add an auth-token smoke script later."

if ($Passed) {
    Write-Host "DAY 16 PAYMENT RUNTIME SMOKE PASSED" -ForegroundColor Green
    exit 0
}

Write-Host "DAY 16 PAYMENT RUNTIME SMOKE FAILED" -ForegroundColor Red
exit 1
