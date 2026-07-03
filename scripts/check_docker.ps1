[CmdletBinding()]
param()

$FoundMark = [char]0x2705
$MissingMark = [char]0x274C

Write-Host "OutcomeIQ Docker availability check" -ForegroundColor Cyan

$DockerCommand = Get-Command docker -ErrorAction SilentlyContinue
if ($null -eq $DockerCommand) {
    Write-Host "$MissingMark Docker command was not found." -ForegroundColor Red
    Write-Host "Install and start Docker Desktop, then open a new PowerShell window." -ForegroundColor Yellow
    exit 1
}

$DockerVersion = & docker --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "$MissingMark Docker command exists but could not report its version." -ForegroundColor Red
    Write-Host $DockerVersion -ForegroundColor DarkYellow
    exit 1
}

Write-Host "$FoundMark Docker command found" -ForegroundColor Green
Write-Host "   $DockerVersion"

$ComposeVersion = & docker compose version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "$MissingMark Docker Compose plugin is not available." -ForegroundColor Red
    Write-Host "Update Docker Desktop or install the Docker Compose plugin." -ForegroundColor Yellow
    exit 1
}

Write-Host "$FoundMark Docker Compose command found" -ForegroundColor Green
Write-Host "   $ComposeVersion"
Write-Host "No image was built and no container was started." -ForegroundColor Cyan
exit 0
