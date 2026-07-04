[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$TestEmail = "outcome_smoke_$Timestamp@outcomeiq.local"
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

function New-CostedSyntheticRun {
    param(
        [string]$Label,
        [string]$ProjectId,
        [string]$WorkflowId,
        [string]$ConfigurationId,
        [hashtable]$Headers
    )

    $script:CurrentStep = "start workflow run $Label"
    $Run = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs" `
        -Headers $Headers `
        -Body @{
            project_id = $ProjectId
            workflow_id = $WorkflowId
            configuration_id = $ConfigurationId
            trigger_type = "simulated"
            external_reference = "outcome-$Label-$Timestamp"
            input_summary = "Synthetic support ticket $Label"
        }

    $script:CurrentStep = "classifier call for run $Label"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/model-calls" `
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

    $script:CurrentStep = "generator call for run $Label"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/model-calls" `
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

    $script:CurrentStep = "tool call for run $Label"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/tool-calls" `
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

    $script:CurrentStep = "complete workflow run $Label"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/complete" `
        -Headers $Headers `
        -Body @{
            output_summary = "Synthetic workflow $Label completed"
            latency_ms = 630
        }

    $script:CurrentStep = "calculate cost for run $Label"
    $Cost = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/costs/workflow-runs/$($Run.id)/calculate" `
        -Headers $Headers `
        -Body @{}
    if ($null -eq $Cost.total_cost_usd) {
        throw "Run $Label cost response did not include total_cost_usd."
    }
    return $Run
}

Write-Host "OutcomeIQ outcome tracking API smoke check" -ForegroundColor Cyan
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
            full_name = "Outcome Smoke User"
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
    if (@($RequiredModels | Where-Object { $_ -notin $Rates.model_name }).Count -gt 0) {
        Write-Host "Run .\scripts\db_seed_pricing.ps1 first." -ForegroundColor Yellow
        throw "Required demo pricing rates are missing."
    }

    $CurrentStep = "organization creation"
    $Organization = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/organizations" `
        -Headers $Headers `
        -Body @{
            name = "Outcome Smoke Organization $Timestamp"
            slug = "outcome-smoke-org-$Timestamp"
        }

    $CurrentStep = "project creation"
    $Project = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/projects" `
        -Headers $Headers `
        -Body @{
            organization_id = $Organization.id
            name = "Outcome Smoke Project $Timestamp"
            slug = "outcome-smoke-project-$Timestamp"
            description = "Synthetic outcome tracking smoke project"
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
            name = "Outcome smoke configuration"
            version_label = "outcome-v1"
            strategy_name = "balanced"
            config_json = @{ provider_mode = "simulated" }
        }

    $RunA = New-CostedSyntheticRun `
        -Label "A" `
        -ProjectId $Project.id `
        -WorkflowId $Workflow.id `
        -ConfigurationId $Configuration.id `
        -Headers $Headers

    $CurrentStep = "outcome contract creation"
    $Contract = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/outcomes/contracts" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            workflow_id = $Workflow.id
            name = "Verified support resolution $Timestamp"
            description = "Ticket resolved without escalation and not reopened within 48 hours"
            success_criteria_json = @{
                resolved = $true
                escalated = $false
                not_reopened_within_hours = 48
            }
            success_window_hours = 48
        }

    $CurrentStep = "successful outcome for run A"
    $OutcomeA = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/outcomes/workflow-runs/$($RunA.id)" `
        -Headers $Headers `
        -Body @{
            outcome_contract_id = $Contract.id
            status = "succeeded"
            verification_source = "simulated"
            outcome_score = 1.0
            notes = "Synthetic verified success"
        }
    if ($null -eq $OutcomeA.verified_at) {
        throw "Succeeded outcome did not receive verified_at."
    }

    $RunB = New-CostedSyntheticRun `
        -Label "B" `
        -ProjectId $Project.id `
        -WorkflowId $Workflow.id `
        -ConfigurationId $Configuration.id `
        -Headers $Headers

    $CurrentStep = "escalated outcome for run B"
    $null = Invoke-JsonPost `
        -Uri "$BaseUrl/api/v1/outcomes/workflow-runs/$($RunB.id)" `
        -Headers $Headers `
        -Body @{
            outcome_contract_id = $Contract.id
            status = "escalated"
            verification_source = "simulated"
            outcome_score = 0.0
            notes = "Synthetic escalation"
        }

    $CurrentStep = "cost per successful outcome metrics"
    $MetricsUri = (
        "$BaseUrl/api/v1/outcomes/metrics/cost-per-success" +
        "?project_id=$($Project.id)" +
        "&workflow_id=$($Workflow.id)" +
        "&configuration_id=$($Configuration.id)"
    )
    $Metrics = Invoke-RestMethod `
        -Uri $MetricsUri `
        -Method Get `
        -Headers $Headers `
        -TimeoutSec 20
    if ([int]$Metrics.total_runs -lt 2) {
        throw "Outcome metrics did not include both synthetic workflow runs."
    }
    if ([int]$Metrics.successful_runs -lt 1) {
        throw "Outcome metrics did not include a successful workflow run."
    }
    if ($null -eq $Metrics.total_cost_usd) {
        throw "Outcome metrics did not include total_cost_usd."
    }
    if ($null -eq $Metrics.cost_per_successful_outcome_usd) {
        throw "Outcome metrics did not include cost_per_successful_outcome_usd."
    }

    Write-Host "OUTCOME TRACKING API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "OUTCOME TRACKING API SMOKE CHECK FAILED" -ForegroundColor Red
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
