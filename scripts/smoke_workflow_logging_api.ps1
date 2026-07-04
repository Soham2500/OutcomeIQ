[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$TestEmail = "workflow_smoke_$Timestamp@outcomeiq.local"
$TestPassword = "TestPassword123!"
$CurrentStep = "health check"
$Login = $null

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

Write-Host "OutcomeIQ workflow logging API smoke check" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

try {
    $Health = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($Health.status -ne "ok") {
        throw "Health endpoint returned an unexpected status."
    }

    $CurrentStep = "user registration"
    $RegisterBody = @{
        email = $TestEmail
        full_name = "Workflow Smoke User"
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

    $CurrentStep = "organization creation"
    $OrganizationBody = @{
        name = "Workflow Smoke Organization $Timestamp"
        slug = "workflow-smoke-org-$Timestamp"
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
        name = "Workflow Smoke Project $Timestamp"
        slug = "workflow-smoke-project-$Timestamp"
        description = "Synthetic workflow logging smoke-test project"
    } | ConvertTo-Json
    $Project = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/projects" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $ProjectBody `
        -TimeoutSec 15

    $CurrentStep = "workflow creation"
    $WorkflowBody = @{
        project_id = $Project.id
        name = "AI Support Ticket Resolution"
        slug = "ai-support-ticket-resolution"
        description = "Synthetic support workflow"
    } | ConvertTo-Json
    $Workflow = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflows" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $WorkflowBody `
        -TimeoutSec 15

    $CurrentStep = "workflow configuration creation"
    $ConfigurationBody = @{
        name = "Balanced smoke configuration"
        version_label = "balanced-v1"
        strategy_name = "balanced"
        config_json = @{ provider_mode = "simulated" }
    } | ConvertTo-Json -Depth 5
    $Configuration = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflows/$($Workflow.id)/configurations" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $ConfigurationBody `
        -TimeoutSec 15

    $CurrentStep = "workflow run start"
    $RunBody = @{
        project_id = $Project.id
        workflow_id = $Workflow.id
        configuration_id = $Configuration.id
        trigger_type = "simulated"
        external_reference = "support-ticket-$Timestamp"
        input_summary = "Synthetic payment issue ticket"
        metadata_json = @{ data_classification = "synthetic" }
    } | ConvertTo-Json -Depth 5
    $WorkflowRun = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $RunBody `
        -TimeoutSec 15

    $CurrentStep = "classification model call"
    $ClassificationBody = @{
        sequence_number = 1
        provider = "simulated"
        model_name = "simulated-classifier-v1"
        call_type = "classification"
        status = "succeeded"
        prompt_tokens = 120
        completion_tokens = 12
        total_tokens = 132
        latency_ms = 180
        request_summary = "Redacted synthetic ticket classification"
        response_summary = "Payment issue category"
    } | ConvertTo-Json
    $null = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/model-calls" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $ClassificationBody `
        -TimeoutSec 15

    $CurrentStep = "ticket status tool call"
    $ToolBody = @{
        sequence_number = 2
        tool_name = "ticket_status_check"
        status = "succeeded"
        latency_ms = 90
        input_summary = "Synthetic ticket reference"
        output_summary = "Payment marked for review"
    } | ConvertTo-Json
    $null = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/tool-calls" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $ToolBody `
        -TimeoutSec 15

    $CurrentStep = "response generation model call"
    $GenerationBody = @{
        sequence_number = 3
        provider = "simulated"
        model_name = "simulated-response-v1"
        call_type = "generation"
        status = "succeeded"
        prompt_tokens = 220
        completion_tokens = 80
        total_tokens = 300
        latency_ms = 420
        request_summary = "Redacted synthetic response context"
        response_summary = "Safe support response generated"
    } | ConvertTo-Json
    $null = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/model-calls" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $GenerationBody `
        -TimeoutSec 15

    $CurrentStep = "workflow run completion"
    $CompleteBody = @{
        output_summary = "Synthetic support response completed"
        latency_ms = 690
        metadata_json = @{ execution_mode = "simulated" }
    } | ConvertTo-Json -Depth 5
    $CompletedRun = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/complete" `
        -Method Post `
        -Headers $Headers `
        -ContentType "application/json" `
        -Body $CompleteBody `
        -TimeoutSec 15
    if ($CompletedRun.status -ne "succeeded") {
        throw "Completed workflow run did not have succeeded status."
    }

    $CurrentStep = "workflow run trace"
    $Trace = Invoke-RestMethod `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($WorkflowRun.id)/trace" `
        -Method Get `
        -Headers $Headers `
        -TimeoutSec 15
    if (@($Trace.model_calls).Count -ne 2 -or @($Trace.tool_calls).Count -ne 1) {
        throw "Workflow trace did not contain the expected simulated calls."
    }
    if ($Trace.workflow_run.id -ne $WorkflowRun.id) {
        throw "Workflow trace returned an unexpected run."
    }

    Write-Host "WORKFLOW LOGGING API SMOKE CHECK PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "WORKFLOW LOGGING API SMOKE CHECK FAILED" -ForegroundColor Red
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
    Write-Host "Apply the reviewed migration first with: .\scripts\db_migrate.ps1" -ForegroundColor Yellow
    exit 1
}
