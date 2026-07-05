[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")
$Timestamp = Get-Date -Format "yyyyMMddHHmmssfff"
$DemoEmail = "demo@outcomeiq.local"
$DemoPassword = "Demo@12345"
$CurrentStep = "health check"
$Login = $null
$HealthReachable = $false
$UsingUniqueDemoUser = $false

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

function Get-HttpStatusCode {
    param([System.Management.Automation.ErrorRecord]$ErrorRecord)

    try {
        return [int]$ErrorRecord.Exception.Response.StatusCode
    }
    catch {
        return 0
    }
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

function New-DemoWorkflowRun {
    param(
        [pscustomobject]$Specification,
        [string]$ProjectId,
        [string]$WorkflowId,
        [string]$ConfigurationId,
        [string]$ContractId,
        [hashtable]$Headers
    )

    $Label = $Specification.Label
    $script:CurrentStep = "start demo workflow run $Label"
    $Run = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflow-runs" `
        -Headers $Headers `
        -Body @{
            project_id = $ProjectId
            workflow_id = $WorkflowId
            configuration_id = $ConfigurationId
            trigger_type = "simulated"
            external_reference = "demo-$Timestamp-$Label"
            input_summary = "Synthetic support ticket $Label"
        }

    $ClassifierPromptTokens = [int]$Specification.ClassifierPromptTokens
    $ClassifierCompletionTokens = [int]$Specification.ClassifierCompletionTokens
    $GeneratorPromptTokens = [int]$Specification.GeneratorPromptTokens
    $GeneratorCompletionTokens = [int]$Specification.GeneratorCompletionTokens

    $script:CurrentStep = "record model calls for demo run $Label"
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
            prompt_tokens = $ClassifierPromptTokens
            completion_tokens = $ClassifierCompletionTokens
            total_tokens = $ClassifierPromptTokens + $ClassifierCompletionTokens
            latency_ms = 130 + (10 * [int]$Specification.Index)
            request_summary = "Redacted synthetic ticket classification"
            response_summary = "Synthetic ticket category"
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
            prompt_tokens = $GeneratorPromptTokens
            completion_tokens = $GeneratorCompletionTokens
            total_tokens = $GeneratorPromptTokens + $GeneratorCompletionTokens
            latency_ms = 330 + (25 * [int]$Specification.Index)
            request_summary = "Redacted synthetic support context"
            response_summary = "Synthetic support resolution"
        }

    $script:CurrentStep = "record tool call for demo run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/tool-calls" `
        -Headers $Headers `
        -Body @{
            sequence_number = 3
            tool_name = "payment_status_lookup"
            status = "succeeded"
            latency_ms = 75 + (5 * [int]$Specification.Index)
            estimated_cost_usd = [decimal]$Specification.ToolCost
            input_summary = "Synthetic transaction reference"
            output_summary = "Synthetic payment status"
        }

    $script:CurrentStep = "complete demo run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/workflow-runs/$($Run.id)/complete" `
        -Headers $Headers `
        -Body @{
            output_summary = "Synthetic demo run $Label completed"
            latency_ms = 600 + (40 * [int]$Specification.Index)
        }

    $script:CurrentStep = "calculate cost for demo run $Label"
    $Cost = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/costs/workflow-runs/$($Run.id)/calculate" `
        -Headers $Headers `
        -Body @{}
    if ($null -eq $Cost.total_cost_usd) {
        throw "Demo run $Label did not receive a calculated cost."
    }

    $script:CurrentStep = "record outcome for demo run $Label"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/outcomes/workflow-runs/$($Run.id)" `
        -Headers $Headers `
        -Body @{
            outcome_contract_id = $ContractId
            status = [string]$Specification.OutcomeStatus
            verification_source = "simulated"
            outcome_score = [decimal]$Specification.OutcomeScore
            metadata_json = @{
                scenario = "payment_failed_money_deducted"
                demo_run = $Label
            }
        }

    return $Run
}

Write-Host "OutcomeIQ API demo data seed" -ForegroundColor Cyan
Write-Host "Target: $BaseUrl"

try {
    $Health = Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get -TimeoutSec 10
    if ($Health.status -ne "ok") {
        throw "Health endpoint returned an unexpected status."
    }
    $HealthReachable = $true

    $CurrentStep = "demo user login"
    try {
        $Login = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/auth/login" `
            -Body @{ email = $DemoEmail; password = $DemoPassword }
    }
    catch {
        if ((Get-HttpStatusCode $_) -ne 401) {
            throw
        }
        $Login = $null
    }

    if ($null -eq $Login) {
        $CurrentStep = "demo user registration"
        $RegistrationConflict = $false
        try {
            $null = Invoke-JsonRequest `
                -Method Post `
                -Uri "$BaseUrl/api/v1/auth/register" `
                -Body @{
                    email = $DemoEmail
                    full_name = "OutcomeIQ Demo User"
                    password = $DemoPassword
                }
        }
        catch {
            if ((Get-HttpStatusCode $_) -notin @(400, 409)) {
                throw
            }
            $RegistrationConflict = $true
        }

        if ($RegistrationConflict) {
            Write-Host "Demo user already exists with different password." -ForegroundColor Yellow
            Write-Host "Use a unique demo email or reset local database manually." -ForegroundColor Yellow
            $DemoEmail = "demo_$Timestamp@outcomeiq.local"
            $UsingUniqueDemoUser = $true
            $CurrentStep = "unique demo user registration"
            $null = Invoke-JsonRequest `
                -Method Post `
                -Uri "$BaseUrl/api/v1/auth/register" `
                -Body @{
                    email = $DemoEmail
                    full_name = "OutcomeIQ Demo User"
                    password = $DemoPassword
                }
        }

        $CurrentStep = "demo user login after registration"
        $Login = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/auth/login" `
            -Body @{ email = $DemoEmail; password = $DemoPassword }
    }

    if ([string]::IsNullOrWhiteSpace($Login.access_token)) {
        throw "Demo login did not return an access token."
    }
    $Headers = @{ Authorization = "Bearer $($Login.access_token)" }
    $ResourceSuffix = if ($UsingUniqueDemoUser) { "-$Timestamp" } else { "" }
    $OrganizationSlug = "outcomeiq-demo-org$ResourceSuffix"
    $ProjectSlug = "ai-support-cost-optimization-demo$ResourceSuffix"
    $WorkflowSlug = "support-ticket-resolution-workflow$ResourceSuffix"

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

    $CurrentStep = "demo organization lookup"
    $Organizations = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/organizations?limit=100" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    $Organization = $Organizations |
        Where-Object { $_.slug -eq $OrganizationSlug } |
        Select-Object -First 1
    if ($null -eq $Organization) {
        $CurrentStep = "demo organization creation"
        $Organization = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/organizations" `
            -Headers $Headers `
            -Body @{
                name = "OutcomeIQ Demo Org"
                slug = $OrganizationSlug
            }
    }

    $CurrentStep = "demo project lookup"
    $Projects = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/projects?limit=100" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    $Project = $Projects |
        Where-Object {
            $_.organization_id -eq $Organization.id -and
            $_.slug -eq $ProjectSlug
        } |
        Select-Object -First 1
    if ($null -eq $Project) {
        $CurrentStep = "demo project creation"
        $Project = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/projects" `
            -Headers $Headers `
            -Body @{
                organization_id = $Organization.id
                name = "AI Support Cost Optimization Demo"
                slug = $ProjectSlug
                description = "Five simulated support runs for OutcomeIQ dashboard demonstration"
            }
    }

    $CurrentStep = "demo workflow lookup"
    $Workflows = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/workflows?project_id=$($Project.id)&limit=100" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    $Workflow = $Workflows |
        Where-Object { $_.slug -eq $WorkflowSlug } |
        Select-Object -First 1
    if ($null -eq $Workflow) {
        $CurrentStep = "demo workflow creation"
        $Workflow = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/workflows" `
            -Headers $Headers `
            -Body @{
                project_id = $Project.id
                name = "Support Ticket Resolution Workflow"
                slug = $WorkflowSlug
                description = "Simulated payment support resolution workflow"
            }
    }

    $CurrentStep = "demo workflow configuration lookup"
    $Configurations = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/workflows/$($Workflow.id)/configurations?limit=100" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    $Configuration = $Configurations |
        Where-Object { $_.version_label -eq "demo-v1" } |
        Select-Object -First 1
    if ($null -eq $Configuration) {
        $CurrentStep = "demo workflow configuration creation"
        $Configuration = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/workflows/$($Workflow.id)/configurations" `
            -Headers $Headers `
            -Body @{
                name = "Balanced demo configuration"
                version_label = "demo-v1"
                strategy_name = "balanced"
                description = "Simulated classifier, generator and payment lookup"
                config_json = @{ provider_mode = "simulated" }
            }
    }

    $CurrentStep = "demo outcome contract lookup"
    $Contracts = @(
        Invoke-RestMethod `
            -Uri "$BaseUrl/api/v1/outcomes/contracts?project_id=$($Project.id)&workflow_id=$($Workflow.id)&limit=100" `
            -Method Get `
            -Headers $Headers `
            -TimeoutSec 20
    )
    $Contract = $Contracts |
        Where-Object { $_.name -eq "Demo support ticket resolution" } |
        Select-Object -First 1
    if ($null -eq $Contract) {
        $CurrentStep = "demo outcome contract creation"
        $Contract = Invoke-JsonRequest `
            -Method Post `
            -Uri "$BaseUrl/api/v1/outcomes/contracts" `
            -Headers $Headers `
            -Body @{
                project_id = $Project.id
                workflow_id = $Workflow.id
                name = "Demo support ticket resolution"
                description = "Ticket is resolved without an unsuccessful customer outcome"
                success_criteria_json = @{
                    resolved = $true
                    verified = $true
                }
                success_window_hours = 48
            }
    }

    $RunSpecifications = @(
        [pscustomobject]@{ Index = 1; Label = "A"; ClassifierPromptTokens = 700; ClassifierCompletionTokens = 70; GeneratorPromptTokens = 1400; GeneratorCompletionTokens = 320; ToolCost = 0.0015; OutcomeStatus = "succeeded"; OutcomeScore = 1.0 },
        [pscustomobject]@{ Index = 2; Label = "B"; ClassifierPromptTokens = 850; ClassifierCompletionTokens = 90; GeneratorPromptTokens = 1750; GeneratorCompletionTokens = 420; ToolCost = 0.0020; OutcomeStatus = "succeeded"; OutcomeScore = 0.9 },
        [pscustomobject]@{ Index = 3; Label = "C"; ClassifierPromptTokens = 1100; ClassifierCompletionTokens = 110; GeneratorPromptTokens = 2500; GeneratorCompletionTokens = 650; ToolCost = 0.0030; OutcomeStatus = "failed"; OutcomeScore = 0.0 },
        [pscustomobject]@{ Index = 4; Label = "D"; ClassifierPromptTokens = 650; ClassifierCompletionTokens = 65; GeneratorPromptTokens = 1250; GeneratorCompletionTokens = 280; ToolCost = 0.0012; OutcomeStatus = "succeeded"; OutcomeScore = 1.0 },
        [pscustomobject]@{ Index = 5; Label = "E"; ClassifierPromptTokens = 1300; ClassifierCompletionTokens = 140; GeneratorPromptTokens = 3100; GeneratorCompletionTokens = 800; ToolCost = 0.0040; OutcomeStatus = "escalated"; OutcomeScore = 0.2 }
    )

    foreach ($Specification in $RunSpecifications) {
        $null = New-DemoWorkflowRun `
            -Specification $Specification `
            -ProjectId $Project.id `
            -WorkflowId $Workflow.id `
            -ConfigurationId $Configuration.id `
            -ContractId $Contract.id `
            -Headers $Headers
    }

    $CurrentStep = "demo recommendation generation"
    $null = Invoke-JsonRequest `
        -Method Post `
        -Uri "$BaseUrl/api/v1/recommendations/generate" `
        -Headers $Headers `
        -Body @{
            project_id = $Project.id
            workflow_id = $Workflow.id
        }

    Write-Host "Demo login email: $DemoEmail" -ForegroundColor DarkCyan
    Write-Host "Frontend URL: http://127.0.0.1:5173" -ForegroundColor DarkCyan
    Write-Host "DEMO DATA SEED PASSED" -ForegroundColor Green
    exit 0
}
catch {
    Write-Host "DEMO DATA SEED FAILED" -ForegroundColor Red
    Write-Host "Failed step: $CurrentStep" -ForegroundColor Yellow
    Write-Host "Reason: $($_.Exception.Message)" -ForegroundColor DarkYellow
    if ($CurrentStep -eq "pricing rate check") {
        Write-Host "Run .\scripts\db_seed_pricing.ps1 first." -ForegroundColor Yellow
    }
    $SensitiveValues = @($DemoPassword)
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
        Write-Host "Start backend first with .\scripts\run_backend.ps1" -ForegroundColor Yellow
    }
    exit 1
}
