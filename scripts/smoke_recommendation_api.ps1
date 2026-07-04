[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$TestEmail = "recommendation_smoke_$Timestamp@outcomeiq.local"
$TestPassword = "TestPassword123!"
$CurrentStep = "health check"
$Login = $null
$HealthReachable = $false

function Invoke-JsonRequest {
    param(
        [string]$Method,
        [string]$Uri,
        [hashtable]$Body,
        [hashtable]$Headers = @{}
    )

    $JsonBody = $Body | ConvertTo-Json -Depth 10
    return Invoke-RestMethod `
        -Uri $Uri `
        -Method $Method `
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

function New-CostedRecommendationRun {
    param(
        [string]$Label,
        [string]$ProjectId,
        [string]$WorkflowId,
        [string]$ConfigurationId,
        [hashtable]$Headers
    )

    $script:CurrentStep = "start recommendation run $Label"
    $Run = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflow-runs" `
        -Headers $Headers `
        -Body @{
            project_id = $ProjectId
            workflow_id = $WorkflowId
            configuration_id = $ConfigurationId
            trigger_type = "simulated"
            external_reference = "recommendation-$Label-$Timestamp"
            input_summary = "Synthetic recommendation ticket $Label"
        }

    $script:CurrentStep = "model calls for recommendation run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
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
    $null = Invoke-JsonRequest `
        -Method Post `
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
            response_summary = "Synthetic support response"
        }

    $script:CurrentStep = "tool call for recommendation run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
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

    $script:CurrentStep = "complete recommendation run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/complete" `
        -Headers $Headers `
        -Body @{
            output_summary = "Synthetic recommendation run $Label completed"
            latency_ms = 630
        }

    $script:CurrentStep = "calculate recommendation run $Label cost"
    $Cost = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/costs/workflow-runs/$($Run.id)/calculate" `
        -Headers $Headers `
        -Body @{}
    if ($null -eq $Cost.total_cost_usd) {
        throw "Recommendation run $Label cost was not calculated."
    }
    return $Run
}

Write-Host "OutcomeIQ recommendation API smoke check" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

try {
    $Health = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($Health.status -ne "ok") {
        throw "Health endpoint returned an unexpected status."
    }
    $HealthReachable = $true

    $CurrentStep = "user registration"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/auth/register" `
        -Body @{
            email = $TestEmail
            full_name = "Recommendation Smoke User"
            password = $TestPassword
        }

    $CurrentStep = "user login"
    $Login = Invoke-JsonRequest `
        -Method Post `
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
        throw "Required demo pricing rates are missing."
    }

    $CurrentStep = "organization creation"
    $Organization = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/organizations" `
        -Headers $Headers `
        -Body @{
            name = "Recommendation Smoke Organization $Timestamp"
            slug = "recommendation-smoke-org-$Timestamp"
        }

    $CurrentStep = "project creation"
    $Project = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/projects" `
        -Headers $Headers `
        -Body @{
            organization_id = $Organization.id
            name = "Recommendation Smoke Project $Timestamp"
            slug = "recommendation-smoke-project-$Timestamp"
            description = "Synthetic recommendation smoke project"
        }

    $CurrentStep = "workflow creation"
    $Workflow = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflows" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            name = "AI Support Ticket Resolution"
            slug = "ai-support-ticket-resolution-$Timestamp"
            description = "Synthetic support workflow"
        }

    $CurrentStep = "workflow configuration creation"
    $Configuration = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflows/$($Workflow.id)/configurations" `
        -Headers $Headers `
        -Body @{
            name = "Recommendation smoke configuration"
            version_label = "recommendation-v1"
            strategy_name = "balanced"
            config_json = @{ provider_mode = "simulated" }
        }

    $RunA = New-CostedRecommendationRun `
        -Label "A" `
        -ProjectId $Project.id `
        -WorkflowId $Workflow.id `
        -ConfigurationId $Configuration.id `
        -Headers $Headers

    $CurrentStep = "outcome contract creation"
    $Contract = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/outcomes/contracts" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            workflow_id = $Workflow.id
            name = "Recommendation support resolution $Timestamp"
            description = "Ticket resolved without escalation"
            success_criteria_json = @{
                resolved = $true
                escalated = $false
            }
            success_window_hours = 48
        }

    $CurrentStep = "successful outcome for run A"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/outcomes/workflow-runs/$($RunA.id)" `
        -Headers $Headers `
        -Body @{
            outcome_contract_id = $Contract.id
            status = "succeeded"
            verification_source = "simulated"
            outcome_score = 1.0
        }

    $RunB = New-CostedRecommendationRun `
        -Label "B" `
        -ProjectId $Project.id `
        -WorkflowId $Workflow.id `
        -ConfigurationId $Configuration.id `
        -Headers $Headers

    $CurrentStep = "failed outcome for run B"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/outcomes/workflow-runs/$($RunB.id)" `
        -Headers $Headers `
        -Body @{
            outcome_contract_id = $Contract.id
            status = "failed"
            verification_source = "simulated"
            outcome_score = 0.0
        }

    $CurrentStep = "recommendation generation"
    $Generated = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/recommendations/generate" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            workflow_id = $Workflow.id
        }
    if ([int]$Generated.generated_count -lt 1) {
        throw "Recommendation generation returned no recommendations."
    }

    $CurrentStep = "recommendation list"
    $Recommendations = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/recommendations?project_id=$($Project.id)&workflow_id=$($Workflow.id)" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    if ($Recommendations.Count -lt 1) {
        throw "Recommendation list returned no items."
    }
    $Recommendation = $Recommendations[0]
    if ([string]::IsNullOrWhiteSpace($Recommendation.title)) {
        throw "Recommendation title is missing."
    }
    if ([string]::IsNullOrWhiteSpace($Recommendation.recommendation_type)) {
        throw "Recommendation type is missing."
    }

    $CurrentStep = "recommendation status update"
    $Updated = Invoke-JsonRequest `
        -Method Patch `
        -Uri "$BaseUrl/api/v1/recommendations/$($Recommendation.id)" `
        -Headers $Headers `
        -Body @{ status = "dismissed" }
    if ($Updated.status -ne "dismissed") {
        throw "Recommendation status was not updated to dismissed."
    }
    if ($null -eq $Updated.dismissed_at) {
        throw "Dismissed recommendation is missing dismissed_at."
    }

    Write-Host "RECOMMENDATION API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "RECOMMENDATION API SMOKE CHECK FAILED" -ForegroundColor Red
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
    if (-not $HealthReachable) {
        Write-Host "Start the backend first with: .\scripts\run_backend.ps1" -ForegroundColor Yellow
    }
    exit 1
}
