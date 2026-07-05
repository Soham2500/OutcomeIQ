[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$OriginalLocation = Get-Location
$ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$ActivateScript = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"
$BackendPath = Join-Path $ProjectRoot "backend"
$ResultCode = 1

try {
    Set-Location $ProjectRoot
    if (-not (Test-Path -LiteralPath $ActivateScript -PathType Leaf)) {
        throw "Virtual environment activation script not found: $ActivateScript"
    }
    . $ActivateScript
    Set-Location $BackendPath
    python scripts/seed_demo_data.py
    $ResultCode = $LASTEXITCODE
}
finally {
    Set-Location $OriginalLocation
}

exit $ResultCode
