[CmdletBinding()]
param(
    [string]$BackendUrl = "http://127.0.0.1:8000",
    [string]$Signature = ""
)

$ErrorActionPreference = "Stop"
$BackendUrl = $BackendUrl.TrimEnd("/")

$Payload = @{
    id = "evt_test_outcomeiq_local"
    event = "subscription.activated"
    payload = @{
        subscription = @{
            entity = @{
                id = "sub_test_outcomeiq_local"
                status = "active"
            }
        }
        payment = @{
            entity = @{
                id = "pay_test_outcomeiq_local"
                subscription_id = "sub_test_outcomeiq_local"
                email = "test_customer@outcomeiq.local"
            }
        }
    }
} | ConvertTo-Json -Depth 10

$Headers = @{}
if (-not [string]::IsNullOrWhiteSpace($Signature)) {
    $Headers["X-Razorpay-Signature"] = $Signature
}

Write-Host "OutcomeIQ Razorpay webhook test" -ForegroundColor Cyan
Write-Host "Target: $BackendUrl/api/v1/billing/webhook/razorpay"

try {
    $Response = Invoke-RestMethod `
        -Method Post `
        -Uri "$BackendUrl/api/v1/billing/webhook/razorpay" `
        -ContentType "application/json" `
        -Headers $Headers `
        -Body $Payload `
        -TimeoutSec 20

    Write-Host "Webhook test request completed." -ForegroundColor Green
    Write-Host "stored: $($Response.stored)"
    Write-Host "processed: $($Response.processed)"
    Write-Host "message: $($Response.message)"
    exit 0
}
catch {
    Write-Host "Webhook test request failed." -ForegroundColor Red
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "If RAZORPAY_WEBHOOK_SECRET is configured, provide a valid test signature." -ForegroundColor Yellow
    exit 1
}
