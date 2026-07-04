[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$TestEmail = "cost_smoke_$Timestamp@outcomeiq.local"
$TestPassword = "TestPassword123!"
$CurrentStep = "health check"
$Login = $null

function Invoke-JsonPost {
    param(
        [string]$Uri,
        [hashtable]$Body,
        [hashtable]$Headers = @{}
    )

    $JsonBody = $Body | ConvertTo-Json -Depth 8
    return Invoke-RestMethod `
        -Uri $Uri `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $JsonBody `
        -TimeoutSec 20
}

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

Write-Host "OutcomeIQ cost calculation API smoke check" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

try {
    $Health = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($Health.status -ne "ok") {
        throw "Health endpoint returned an unexpected status."
    }

    $CurrentStep = "user registration"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/auth/register" `
        -Body @{
            email = $TestEmail
            full_name = "Cost Smoke User"
            password = $TestPassword
        }

    $CurrentStep = "user login"
    $Login = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/auth/login" `
        -Body @{ email = $TestEmail; password = $TestPassword }
    if ([string]::IsNullOrWhiteSpace($Login.access_token)) {
        throw "Login did not return an access token."
    }
    $Headers = @{ Authorization = "Bearer $($Login.access_token)" }

    $CurrentStep = "pricing rate check"
    $Rates = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/costs/pricing-rates?provider=simulated" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 15
    )
    $RequiredModels = @(
        "support-classifier-small",
        "support-generator-standard"
    )
    $MissingModels = @(
        $RequiredModels | Where-Object { $_ -notin $Rates.model_name }
    )
    if ($MissingModels.Count -gt 0) {
        Write-Host "Required demo pricing rates are missing." -ForegroundColor Yellow
        Write-Host "Run .\scripts\db_seed_pricing.ps1 first." -ForegroundColor Yellow
        throw "Demo pricing rates are not available."
    }

    $CurrentStep = "organization creation"
    $Organization = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/organizations" `
        -Headers $Headers `
        -Body @{
            name = "Cost Smoke Organization $Timestamp"
            slug = "cost-smoke-org-$Timestamp"
        }

    $CurrentStep = "project creation"
    $Project = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/projects" `
        -Headers $Headers `
        -Body @{
            organization_id = $Organization.id
            name = "Cost Smoke Project $Timestamp"
            slug = "cost-smoke-project-$Timestamp"
            description = "Synthetic cost-calculation smoke project"
        }

    $CurrentStep = "workflow creation"
    $Workflow = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflows" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            name = "AI Support Ticket Resolution"
            slug = "ai-support-ticket-resolution"
            description = "Synthetic support workflow"
        }

    $CurrentStep = "workflow configuration creation"
    $Configuration = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflows/$($Workflow.id)/configurations" `
        -Headers $Headers `
        -Body @{
            name = "Cost smoke configuration"
            version_label = "cost-v1"
            strategy_name = "balanced"
            config_json = @{ provider_mode = "simulated" }
        }

    $CurrentStep = "workflow run start"
    $WorkflowRun = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            workflow_id = $Workflow.id
            configuration_id = $Configuration.id
            trigger_type = "simulated"
            external_reference = "cost-ticket-$Timestamp"
            input_summary = "Synthetic support ticket"
        }

    $CurrentStep = "classifier model call"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/model-calls" `
        -Headers $Headers `
        -Body @{
            sequence_number = 1
            provider = "simulated"
            model_name = "support-classifier-small"
            call_type = "classification"
            status = "succeeded"
            prompt_tokens = 1000
            completion_tokens = 100
            total_tokens = 1100
            latency_ms = 150
            request_summary = "Redacted synthetic classification input"
            response_summary = "Synthetic support category"
        }

    $CurrentStep = "generator model call"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/model-calls" `
        -Headers $Headers `
        -Body @{
            sequence_number = 2
            provider = "simulated"
            model_name = "support-generator-standard"
            call_type = "generation"
            status = "succeeded"
            prompt_tokens = 2000
            completion_tokens = 500
            total_tokens = 2500
            latency_ms = 400
            request_summary = "Redacted synthetic generation input"
            response_summary = "Synthetic response generated"
        }

    $CurrentStep = "tool call"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/tool-calls" `
        -Headers $Headers `
        -Body @{
            sequence_number = 3
            tool_name = "ticket_status_check"
            status = "succeeded"
            latency_ms = 80
            estimated_cost_usd = 0.002
            input_summary = "Synthetic ticket reference"
            output_summary = "Synthetic ticket status"
        }

    $CurrentStep = "workflow run completion"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/complete" `
        -Headers $Headers `
        -Body @{
            output_summary = "Synthetic workflow completed"
            latency_ms = 630
        }

    $CurrentStep = "cost calculation"
    $CalculatedCost = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/costs/workflow-runs/$($WorkflowRun.id)/calculate" `
        -Headers $Headers `
        -Body @{}
    if ($null -eq $CalculatedCost.total_cost_usd) {
        throw "Calculated response did not include total_cost_usd."
    }

    $CurrentStep = "stored cost lookup"
    $StoredCost = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/costs/workflow-runs/$($WorkflowRun.id)" `
        -Method Get `
        -Headers $Headers `
        -TimeoutSec 15
    if ($null -eq $StoredCost.total_cost_usd) {
        throw "Stored cost response did not include total_cost_usd."
    }
    if ([decimal]$StoredCost.total_cost_usd -ne [decimal]$CalculatedCost.total_cost_usd) {
        throw "Stored and calculated cost totals did not match."
    }

    Write-Host "COST CALCULATION API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "COST CALCULATION API SMOKE CHECK FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
    if ($CurrentStep -eq "pricing rate check") {
        Write-Host "Run .\scripts\db_seed_pricing.ps1 first." -ForegroundColor Yellow
    }
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
